from abc import ABC, abstractmethod

class Config(ABC):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @abstractmethod
    def describe(self):
        pass
    
class ChatConfig(Config):
    def __init__(
        self,
        s3_bucket_name='qaai-pdf',
        vector_db_path=None,
        prompt_db_path=None,
        prompt_name=None,
        region_name="us-west-2",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.s3_bucket_name = s3_bucket_name
        self.vector_db_path = vector_db_path
        self.prompt_db_path = prompt_db_path
        self.prompt_name = prompt_name
        self.region_name = region_name

    def describe(self):
        return self.__dict__
    
