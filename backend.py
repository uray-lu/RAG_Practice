"""
Backend Service
"""

from typing import List, Dict
from system_config import SystemConfig
from utils.Config import ChatConfig
from utils.aws_client import (
    AWSBedRockLLM,
    AWSBedrockEembedding,
    AWSS3Bucket
)
from utils import Logger
from src.ChainConstructor import RetrieverChainConstructor
from src.ChatBot import ChatBot
from src.SyncDBHandler import SyncS3DBHandler

logger = Logger.setup_logger()
error_logger = Logger.setup_logger('error')


def Backend(
        version: str,
        payload: dict = None
) -> Dict[str, str]:
    """
    Backend Srvice for Chatbot
    """
    if payload is None:
        payload = {}

    chat_data = {
        'answer': str(),
        'metadata': List[str],
        'config': Dict[str, str]
    }
    # 1. ================== Version Check ==================
    if version != SystemConfig.get_default_version():
        error_logger.error(f'Unsupported version: {version}')
        raise ValueError(f'Unsupported version: {version}')
    # 2. ================== Required fields Check ==================
    db_required_fields = SystemConfig.get_required_db_fields()
    validate_requires_db_fields(required_fields=db_required_fields)

    chatbot_required_fields = SystemConfig.get_required_chatbot_fields()
    validate_requires_chatbot_fields(required_fields=chatbot_required_fields)
    # 3. ================== Chain Construction ==================
    chat_config = ChatConfig(
        vector_db_path=db_required_fields['vector_db_path'],
        prompt_db_path=db_required_fields['prompt_db_path'],
        prompt_name=db_required_fields['prompt_name'],
        retriever_threshold=chatbot_required_fields['retriever_threshold'],
        retriever_topk=chatbot_required_fields['retriever_topk']
    )
    logger.info(f"chat_config: {chat_config.describe()}")

    s3_bucket = AWSS3Bucket(chat_config).connect_to_cloud_storage()
    embeddings = AWSBedrockEembedding(chat_config).get_embedding_model()
    llm = AWSBedRockLLM(chat_config).get_llm_model()
    db_handler = SyncS3DBHandler(aws_s3_bucket=s3_bucket)

    chain_constructor = RetrieverChainConstructor(
        config=chat_config,
        DBHandler=db_handler,
        Embeddings=embeddings,
        LLM=llm
    )
    # 4. ================== Get Reply ==================
    query = payload.get('query', '')
    answer, metadata = ChatBot(query=query, chain_constructor=chain_constructor).make_response()

    chat_data['answer'] = answer
    chat_data['metadata'] = metadata
    chat_data['config'] = chat_config.describe()

    logger.info(f"Query:{query}, Chat Detail: {chat_data}")
    return chat_data


def validate_requires_db_fields(required_fields: dict):
    for key in required_fields.keys():
        if not required_fields[key]:
            raise ValueError(f'{key} is not set, please check the system config setting.')
    logger.info('Database Fields validation complete.')


def validate_requires_chatbot_fields(required_fields: dict):
    if not required_fields:
        raise ValueError(f'CHATBOT FIELD is not set, please check the system config setting.')
    logger.info('Chatbot Fields validation complete.')


if __name__ == '__main__':
    pass
