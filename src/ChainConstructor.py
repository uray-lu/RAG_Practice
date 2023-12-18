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
logger = Logger.setup_logger(__name__)

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

        self._load_memory()
        self._load_prompt()
        self._load_vector_store()
        self._get_retriever()        

    def form_chain(self) -> RetrievalQA:
        chain_type_kwargs = {"prompt": self.prompt,"memory":self.memory}
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, 
                                        chain_type="stuff", 
                                        retriever=self.retriever,
                                        verbose=True,
                                        return_source_documents=True,
                                        chain_type_kwargs=chain_type_kwargs)
        logger.info(f"QA Chain Construction.............Done")
        return qa_chain

    def _load_prompt(self) -> None:
        if not os.path.exists(self.config.prompt_db_path):
            self.db_handler.sync_from_cloud(s3_prefix=self.remote_prompt_db_path, local_folder=self.config.prompt_db_path)
        
        with open(os.path.join(self.config.prompt_db_path, self.config.prompt_name), 'r', encoding='utf-8') as file:
            prompt_template = file.read()
        
        self.prompt = PromptTemplate(
            template=prompt_template, input_variables=["chat_history","context","question"]
        )
        logger.info(f"Prompt Construction.............Done")
    
    def _load_memory(self) -> None:
        self.memory =  ConversationBufferMemory(                        
                        memory_key="chat_history",
                        input_key="question" ,
                        output_key='output_text',
                        return_messages=True,
                        k=3
        )
        logger.info(f"Memory Construction.............Done")

    def _load_vector_store(self)-> None:
        if not os.path.exists(self.config.vector_db_path):
           self.db_handler.sync_from_cloud(s3_prefix=self.remote_vector_db_path, local_folder=self.config.vector_db_path)
        
        self.vector_store = FAISS.load_local(
                                self.config.vector_db_path, self.embeddings, normalize_L2=True
                            )
        logger.info(f"Vector Store Construction.............Done")

    def _get_retriever(self) -> None:
        if self.config.retriever_threshold:
            self.retriever = self.vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": self.config.retriever_threshold})
            logger.info(f"Retriever Construction.............Done")
        else:
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": self.config.retriever_topk})
            logger.info(f"Retriever Construction.............Done")
















