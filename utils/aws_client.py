from abc import ABC, abstractmethod
import boto3
import botocore
from langchain.embeddings import BedrockEmbeddings
from utils.Config import Config

class AWSClient(ABC):

    @abstractmethod
    def authenticate(self, bedrock_credential)-> None:
        """Authenticate AWS client using provided credentials."""
        pass

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




class AWSBedrockEembedding(AWSClient, CloudEmbeddingModel):
    
    def __init__(self, config:Config)-> None:
        self.config = config
        self.session = None

    def authenticate(self) -> None:
        try:
            # Attempt AWS authentication using the provided credential profile
            self.session = boto3.Session(profile_name=self.config.bedrock_credential)
        except botocore.exceptions.ProfileNotFound as e:
            raise  Exception("An error occurred while connecting to AWS") from e

    
    def get_embedding_model(self)-> BedrockEmbeddings:      
        if not self.session:
            self.authenticate()

        try:
            # Attempt to create a BedrockEmbeddings object
            embeddings = BedrockEmbeddings(
                credentials_profile_name=self.config.bedrock_credential, region_name=self.config.region_name,
            )
        except Exception as e:
            raise Exception("An error occurred while initializing BedrockEmbeddings") from e
        
        return embeddings

class AWSS3Bucket(AWSClient, CloudStorage):

    def __init__(self, config:Config)-> None:
        self.config = config
        self.session = None

    def authenticate(self) -> None:
        try:
            # Attempt AWS authentication using the provided credential profile
            self.session = boto3.Session(profile_name=self.config.s3_credential)
        except botocore.exceptions.ProfileNotFound as e:
            raise  Exception("An error occurred while connecting to AWS") from e

    def connect_to_cloud_storage(self) -> any:
        if not self.session:
            self.authenticate()

        try:
            s3 = self.session.resource('s3')
            bucket = s3.Bucket(self.config.s3_bucket_name)
        except botocore.exceptions.ProfileNotFound as e:
            raise  Exception("An error occurred while connecting to AWS S3") from e

        return bucket


#%%
# Test

# from Config import AWSConfig


# config = AWSConfig(
#     bedrock_credential="bedrock",
#     s3_credential="default"
# )


# s3_bucket = AWSS3Bucket(config)
# embeddings = AWSBedrockEembedding(config).get_embedding_model()

















        

# %%
