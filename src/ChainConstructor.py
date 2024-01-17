from abc import ABC, abstractmethod
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from utils.aws_client import AWSBedRockLLM, AWSBedrockEembedding
from utils.Config import Config
from langchain.vectorstores.faiss import FAISS
from src.SyncDBHandler import SyncS3DBHandler

import os
from utils import Logger
logger = Logger.setup_logger()
error_logger = Logger.setup_logger('error')

class BaseChainConstructor(ABC):

    @abstractmethod
    def form_chain(self) -> RetrievalQA:
        """Abstract method to form the chain."""


class RetrieverChainConstructor(BaseChainConstructor):

    def __init__(
        self,
        config:Config,
        DBHandler:SyncS3DBHandler,
        Embeddings:AWSBedrockEembedding,
        LLM:AWSBedRockLLM=None,
    ) -> None:
        self.config = config
        self.remote_vector_db_path = os.path.basename(config.vector_db_path) +'/'
        self.remote_prompt_db_path = os.path.basename(config.prompt_db_path) +'/'
        self.db_handler = DBHandler
        self.embeddings = Embeddings
        self.llm = LLM

        self._load_prompt()
        self._load_vector_store()
        self._get_retriever()        

    def form_chain(self) -> RetrievalQA:
        try:
            chain_type_kwargs = {"prompt": self.prompt}
            qa_chain = RetrievalQA.from_chain_type(llm=self.llm, 
                                            chain_type="stuff", 
                                            retriever=self.retriever,
                                            verbose=True,
                                            return_source_documents=True,
                                            chain_type_kwargs=chain_type_kwargs)
            logger.info(f"QA Chain Construction.............Done")
            return qa_chain
        except Exception as e:
            error_logger.error(f"Error forming chain: {e}", exc_info=True)
            raise ValueError(f"Error forming chain: {e}")

    def _load_prompt(self) -> None:
        try:
            if not os.path.exists(self.config.prompt_db_path):
                self.db_handler.sync_from_cloud(s3_prefix=self.remote_prompt_db_path, local_folder=self.config.prompt_db_path)
            
            with open(os.path.join(self.config.prompt_db_path, self.config.prompt_name), 'r', encoding='utf-8') as file:
                prompt_template = file.read()
            
            self.prompt = PromptTemplate(
                template=prompt_template, input_variables=["context","question"]
            )
            logger.info(f"Prompt Construction.............Done")
        except Exception as e:
            error_logger.error(f"Error loading prompt: {e}", exc_info=True)
            raise ValueError(f"Error loading prompt: {e}")

        
    def _load_vector_store(self)-> None:
        try:
            vector_db_path = self.config.vector_db_path
            if not os.path.exists(vector_db_path) or not any(file in os.listdir(vector_db_path) for file in ["index.faiss", "index.pkl"]):
                self.db_handler.sync_from_cloud(s3_prefix=self.remote_vector_db_path, local_folder=vector_db_path)
            
            self.vector_store = FAISS.load_local(
                                    self.config.vector_db_path, self.embeddings, normalize_L2=True
                                )
            logger.info(f"Vector Store Construction.............Done")
        except Exception as e:
            error_logger.error(f"Error loading vector store: {e}", exc_info=True)
            raise ValueError(f"Error loading vector store: {e}")
        
    def _get_retriever(self) -> None:
        try:
            if self.config.retriever_threshold:
                self.retriever = self.vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": self.config.retriever_threshold})
                logger.info(f"Retriever Construction.............Done")
            else:
                self.retriever = self.vector_store.as_retriever(search_kwargs={"k": self.config.retriever_topk})
                logger.info(f"Retriever Construction.............Done")
        except Exception as e:
            error_logger.error(f"Error loading retriever: {e}", exc_info=True)
            raise ValueError(f"Error loading retriever: {e}")















