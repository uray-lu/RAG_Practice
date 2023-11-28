
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from utils.aws_client import AWSBedRockLLM, AWSBedrockEembedding
from utils.Config import Config
from langchain.vectorstores.faiss import FAISS
from src.SyncDBHandler import SyncS3DBHandler

import os

class ChatBot:

    def __init__(
        self,
        config:Config,
        DBHandler:SyncS3DBHandler,
        Embeddings:AWSBedrockEembedding,
        LLM:AWSBedRockLLM,
    ) -> None:
        self.config = config
        self.remote_vector_db_path = os.path.basename(config.vector_db_path) +'/'
        self.remote_prompt_db_path = os.path.basename(config.prompt_db_path) +'/'
        self.db_handler = DBHandler
        self.embeddings = Embeddings
        self.llm = LLM

        self._load_vector_store()
        self._load_memory()
        self._load_prompt()

    #TODO: Change to ConversationRetrievalQA
    def form_chain(self) -> RetrievalQA:
        chain_type_kwargs = {"prompt": self.prompt,"memory":self.memory}
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, 
                                        chain_type="stuff", 
                                        retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                                        verbose=True,
                                        return_source_documents=True,
                                        chain_type_kwargs=chain_type_kwargs)
        return qa_chain
    
    def _load_vector_store(self)-> None:
        if not os.path.exists(self.config.vector_db_path):
           self.db_handler.sync_from_cloud(s3_prefix=self.remote_vector_db_path, local_folder=self.config.vector_db_path)
        
        self.vector_store = FAISS.load_local(
                                self.config.vector_db_path, self.embeddings
                            )

    def _load_prompt(self) -> None:
        if not os.path.exists(self.config.prompt_db_path):
            self.db_handler.sync_from_cloud(s3_prefix=self.remote_prompt_db_path, local_folder=self.config.prompt_db_path)
        
        with open(os.path.join(self.config.prompt_db_path, self.config.prompt_name), 'r', encoding='utf-8') as file:
            prompt_template = file.read()
        self.prompt = PromptTemplate(
            template=prompt_template, input_variables=["chat_history","context","question"]
        )

    def _load_memory(self) -> None:
        self.memory =  ConversationBufferMemory(                        
                        memory_key="chat_history",
                        input_key="question" ,
                        output_key='output_text',
                        return_messages=True,
                        k=3
        )
        



















