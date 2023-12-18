from abc import ABC, abstractmethod
import boto3
import botocore
from langchain.embeddings import BedrockEmbeddings
from langchain.chat_models import BedrockChat
from utils import Logger
logger = Logger.setup_logger()
error_logger = Logger.setup_logger('error')

class AWSClient(ABC):
    def __init__(self, config):
        self.config = config
        self.session = None

    def authenticate(self):
        if self.session is None:
            try:
                self.session = boto3.Session()
            except botocore.exceptions.ProfileNotFound as e:
                error_logger.error("An error occurred while connecting to AWS", exc_info=True)
                raise Exception("An error occurred while connecting to AWS") from e

class CloudEmbeddingModel(ABC):
    
    @abstractmethod
    def get_embedding_model(self, **kwargs)-> BedrockEmbeddings:
        """Retrieve or create a cloud embedding model."""
        pass

class CloudStorage(ABC):

    @abstractmethod
    def connect_to_cloud_storage(self, *kwargs) -> any:
        """Connect to cloud storage service."""
        pass    

class CloudLLMModel(ABC):
    
    @abstractmethod
    def get_llm_model(self, *kwargs) -> any:
        """Retrieve or create a cloud LLM."""
        pass


class AWSBedrockEembedding(AWSClient, CloudEmbeddingModel):
    def get_embedding_model(self)-> BedrockEmbeddings:      
        self.authenticate()
        try:
            # Attempt to create a BedrockEmbeddings object
            embeddings = BedrockEmbeddings(client=self.session.client(
                    service_name="bedrock-runtime",
                    region_name="us-west-2",
                )
            )
        except Exception as e:
            error_logger.error("An error occurred while initializing BedrockEmbeddings", exc_info=True)
            raise Exception("An error occurred while initializing BedrockEmbeddings") from e
        
        return embeddings

class AWSS3Bucket(AWSClient, CloudStorage):
    def connect_to_cloud_storage(self) -> any:
        self.authenticate()
        try:
            s3 = self.session.resource('s3')
            bucket = s3.Bucket(self.config.s3_bucket_name)
        except botocore.exceptions.ProfileNotFound as e:
            error_logger.error("An error occurred while connecting to AWS S3", exc_info=True)
            raise  Exception("An error occurred while connecting to AWS S3") from e

        return bucket

class AWSBedRockLLM(AWSClient, CloudLLMModel):
    def get_llm_model(self) -> any:
        if not self.session:
            self.authenticate()
        
        try:
            llm = BedrockChat(
                client=self.session.client(
                    service_name="bedrock-runtime",
                    region_name="us-west-2",
                ),
                model_id="anthropic.claude-v2" 
            )
            llm.model_kwargs = {"temperature": 0,'max_tokens_to_sample':700}
        except Exception as e:
            error_logger.error("An error occurred while initializing Bedrock LLM", exc_info=True)
            raise Exception("An error occurred while initializing Bedrock LLM") from e

        return llm