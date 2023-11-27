from abc import ABC, abstractmethod

class Config(ABC):

    def __init__(self, **kwargs):
        self._config = kwargs
    
    @abstractmethod
    def describe(self):
        pass


class AWSConfig(Config):
    def __init__(
        self,
        bedrock_credential=None,
        s3_credential=None,
        s3_bucket_name='qaai-pdf',
        source_folder_path=None,
        vector_folder_path=None,
        region_name="us-west-2",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.bedrock_credential = bedrock_credential
        self.s3_credential = s3_credential
        self.s3_bucket_name = s3_bucket_name
        self.source_folder_path = source_folder_path
        self.vector_folder_path = vector_folder_path
        self.region_name = region_name

    def describe(self):
        config = {}
        for key, value in self._config.items():
            config[key] = value
        return config

class ChatConfig(Config):
    def __init__(
        self,
        bedrock_credential=None,
        s3_credential=None,
        s3_bucket_name='qaai-pdf',
        vector_folder_path=None,
        region_name="us-west-2",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.bedrock_credential = bedrock_credential
        self.s3_credential = s3_credential
        self.s3_bucket_name = s3_bucket_name
        self.vector_folder_path = vector_folder_path
        self.region_name = region_name

    def describe(self):
        config = {}
        for key, value in self._config.items():
            config[key] = value
        return config