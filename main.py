from utils.Config import ChatConfig
from utils.aws_client import (
    AWSBedRockLLM, 
    AWSBedrockEembedding, 
    AWSS3Bucket
)
from src.backend import ChatBot
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

    # 3. ================== Bot Construct ==================  
    config = ChatConfig(
            vector_db_path=vector_db_path,
            prompt_db_path=prompt_db_path,
            prompt_name=prompt_name
    )
    logging.info(
        f"Config: {config.describe()}"
    )

    s3_bucket = AWSS3Bucket(config).connect_to_cloud_storage()
    embeddings = AWSBedrockEembedding(config).get_embedding_model()
    llm = AWSBedRockLLM(config).get_llm_model()
    db_handler = SyncS3DBHandler(aws_s3_bucket=s3_bucket)

    bot = ChatBot(
        config=config, 
        DBHandler=db_handler, 
        Embeddings=embeddings, 
        LLM=llm).form_chain()
    
    # 4. ================== Get Reply ==================
    try:
        reply = bot({"query":query})
    except:
        raise Exception('Something wrong when getting reply')
     
    answer = reply['result']
    
    #TODO:Deal with this
    source_documents_info =[doc.metadata for doc in reply['source_documents']]

    from collections import defaultdict
    raw_metadata = defaultdict(set)
    for data in source_documents_info:
        document_path = data['source']
        document_name = os.path.basename(document_path)
        raw_metadata[document_name].add(f"page.{int(data['page'])+1}")
    
    first_metadata, pages = next(iter(dict(raw_metadata).items()))

    metadata = "------------------------------------\n參考資料:\n"
    metadata += f" {first_metadata},\n Page: {', '.join(pages)}\n------------------------------------\n" 

    chat_data['answer'] = answer
    chat_data['metadata'] = metadata
    chat_data['config'] = config.describe()
    
    return chat_data

