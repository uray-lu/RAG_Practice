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
        s3_bucket_name:str='qaai-pdf',
        vector_db_path:str=None,
        prompt_db_path:str=None,
        prompt_name:str=None,
        retriever_topk:int=5,
        retriever_threshold:float=None,
        region_name:str="us-west-2",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.s3_bucket_name = s3_bucket_name
        self.vector_db_path = vector_db_path
        self.prompt_db_path = prompt_db_path
        self.prompt_name = prompt_name
        self.retriever_topk = retriever_topk
        self.retriever_threshold = retriever_threshold
        self.region_name = region_name

    def describe(self):
        return self.__dict__
    
class TrulensConfig(Config):
    """save Trulens Config"""
    def __init__(self):
        self.methods = ['groundness', 'context_relevancy', 'answer_relevancy']

    def describe(self):
        return self.__dict__

class RagasConfig(Config):
    """save Ragas Config"""
    def __init__(self):
        self.methods = ['context_precision']

    def describe(self):
        return self.__dict__

trulens_config = TrulensConfig()
ragas_config = RagasConfig()
