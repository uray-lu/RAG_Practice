from src.backend import (
    ChatBot,
)

from typing import (
    List,
    Dict
)

import os
import logging
logging.basicConfig(level=logging.INFO)

profile = os.environ.get('AWS_PROFILE')
    
def chat(
    version:str, 
    payload:dict = {}
) -> Dict[str, str]:
    
    chat_data = {
        'answer':str(),
        'metadata': List[str]
    }
    
    # 1. ================== Random check ==================
    if version != 'v1':
        raise Exception('Wrong version.')

    # 2. ================== Check payload ==================
    logging.info('Chek payload.............start')
    
    vector_db = payload.get('vector_db', None)
    if not vector_db:
        raise Exception('Vector DB is not set, please check the request body.')

    query = payload.get('query','')
    logging.info('Chek payload.............Done')

    # 3. ================== Reply ==================  
    bot = ChatBot(
        bedrock_credential=profile,
        vector_db= vector_db
    ).form_chain()

    try:
        reply = bot({"query":query})
    except:
        raise Exception('Something wrong when getting reply')
     
    answer = reply['result']
    source_documents_info =[doc.metadata for doc in reply['source_documents']]
    
    from collections import defaultdict
    raw_metadata = defaultdict(set)
    for data in source_documents_info:
        document_path = data['source']
        document_name = os.path.basename(document_path)
        raw_metadata[document_name].add(f"P.{int(data['page'])+1}")

    metadata = "------------------------------------\n參考資料:\n"
    for index,(file_name,pages) in enumerate(raw_metadata.items()):
        metadata += f"{index+1}. {file_name} , page:{pages}\n------------------------------------\n" 

    chat_data['answer'] = answer
    chat_data['metadata'] = metadata.replace('{', '').replace('}', '').replace("'", '')
    
    
    return chat_data

