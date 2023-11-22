
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA


class ChatBot:

    def __init__(
        self,
        bedrock_credential:str,
        vector_db:str,
    ) -> None:
        pass
        # ================= Authenticator for AWS =================
        self.authenticate(bedrock_credential=bedrock_credential)

        # ================= Basic chain components =================
        self._load_vector_store(vector_db=vector_db)
        self._load_memory()
        self._load_prompt()


    def authenticate(
        self, 
        bedrock_credential
    )-> None:
        try:
            # Attempt AWS authentication using the provided credential profile
            boto3.Session(profile_name=bedrock_credential)
        except botocore.exceptions.ProfileNotFound as e:
            raise  Exception("An error occurred while connecting to AWS") from e
        
        try:
            self.embeddings = BedrockEmbeddings(
                    credentials_profile_name=bedrock_credential, region_name="us-west-2"
                )
        except Exception as e:
            raise Exception("An error occurred while initializing BedrockEmbeddings") from e

        try:
            bedrock_runtime = boto3.client(
                    service_name="bedrock-runtime",
                    region_name="us-west-2",
                )
            from langchain.chat_models import BedrockChat
            self.titan_llm = BedrockChat(
                model_id="anthropic.claude-v2", 
                client=bedrock_runtime, 
                credentials_profile_name=bedrock_credential
            )
            self.titan_llm.model_kwargs = {"temperature": 0,'max_tokens_to_sample':700}
        except Exception as e:
            raise Exception("An error occurred while initializing Bedrock LLM") from e
    
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