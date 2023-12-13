from utils.Config import ChatConfig
from utils.aws_client import (
    AWSBedRockLLM, 
    AWSBedrockEembedding, 
    AWSS3Bucket
)

from src.ChainConstructor import RetrieverChainConstructor
from src.ChatBot import ChatBot
from src.SyncDBHandler import SyncS3DBHandler

from typing import (
    List,
    Dict
)

import os
import logging
logging.basicConfig(level=logging.INFO)

    
def chat(
    version:str, 
    payload:dict = {}
) -> Dict[str, str]:
    
    chat_data = {
        'answer':str(),
        'metadata': List[str],
        'config':Dict[str, str]
    }
    
    # 1. ================== Random check ==================
    if version != 'v1':
        raise Exception('Wrong version.')

    # 2. ================== Check payload ==================
    logging.info('Chek payload.............start')
    
    vector_db_path = payload.get('vector_db_path', None)
    if not vector_db_path:
        raise Exception('Vector DB is not set, please check the request body.')
    
    prompt_db_path = payload.get('prompt_db_path', None)
    if not prompt_db_path:
        raise Exception('Prompt DB is not set, please check the request body.')
    
    prompt_name = payload.get('prompt_name', None)
    if not prompt_name:
        raise Exception('Prompt name is not set, please check the request body.')
    
    query = payload.get('query','')
    
    logging.info('Chek payload.............Done')

    # 3. ================== Chain Construction ==================  
    config = ChatConfig(
            vector_db_path=vector_db_path,
            prompt_db_path=prompt_db_path,
            prompt_name=prompt_name,
            retriever_threshold=.5,
    )
    logging.info(
        f"Config: {config.describe()}"
    )

    s3_bucket = AWSS3Bucket(config).connect_to_cloud_storage()
    embeddings = AWSBedrockEembedding(config).get_embedding_model()
    llm = AWSBedRockLLM(config).get_llm_model()
    db_handler = SyncS3DBHandler(aws_s3_bucket=s3_bucket)

    chain_constructor = RetrieverChainConstructor(
        config=config, 
        DBHandler=db_handler, 
        Embeddings=embeddings, 
        LLM=llm
    )

     # 4. ================== Get Reply ==================
    bot = ChatBot(query=query, chain_constructor=chain_constructor)
    answer, metadata = bot.make_response()

    chat_data['answer'] = answer
    chat_data['metadata'] = metadata
    chat_data['config'] = config.describe()
    
    return chat_data

