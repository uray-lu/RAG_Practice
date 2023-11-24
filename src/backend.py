
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from utils.aws_client import AWSBedRockLLM
from utils.Config import Config
from langchain.vectorstores.faiss import FAISS
from SyncVectorDBHandler import S3SyncVectorDBHandler

import os

#TODO: 搞定vector_db
class ChatBot:

    def __init__(
        self,
        config:Config,
        VectorDBHandler:S3SyncVectorDBHandler,
        LLM:AWSBedRockLLM,
    ) -> None:
        self.config = config
        self.llm = LLM

        self.s3_vector_path = os.path.basename(config.vector_folder_path) +'/'
        self.folder

        
        
        
        
        
        # ================= Basic chain components =================
        self._load_vector_store(vector_db=vector_db)
        self._load_memory()
        self._load_prompt()


    
    #TODO: Change to ConversationRetrievalQA
    #TODO: Think about async
    def form_chain(self) -> RetrievalQA:
        chain_type_kwargs = {"prompt": self.prompt,"memory":self.memory}
        qa_chain = RetrievalQA.from_chain_type(llm=self.titan_llm, 
                                        chain_type="stuff", 
                                        retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                                        verbose=True,
                                        return_source_documents=True,
                                        chain_type_kwargs=chain_type_kwargs)
        return qa_chain
    
    #TODO:new feature like cross vectordb
    def _load_vector_store(
        self,
        vector_db
    )-> None:
        #TODO:download files from AWS if not os.path.exist(vector_db)

        if not os.path.exists(vector_db):
            raise Exception("The vector store is not existed, please check files again.")
        
        self.vector_store = FAISS.load_local(
                                vector_db, self.embeddings
                            )

    #TODO: Think how to make it easier to change-> config.json or config.yaml
    def _load_prompt(self) -> None:
        prompt_template = """
        You are a helpful chatbot only speak Traditional Chinese and having a conversation with user.
        Use the following information to make a recap to answer the question at the end. If you don't know the answer, 
        just say that you don't know and ask the user for more informations, don't try to make up an answer.
        
        Context:{context}
        
        History: {chat_history}
        
        Question: {question}
        Answer (Must in Traditional Chinese(繁體中文)):
        """
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
        
