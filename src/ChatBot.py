from src.ChainConstructor import BaseChainConstructor
import os 
from collections import defaultdict
from utils import Logger
logger = Logger.setup_logger()
error_logger = Logger.setup_logger('error')

class ChatBot:

    def __init__(
        self,
        query:str,
        chain_constructor:BaseChainConstructor,
    ) -> None:
        
        self.query = query
        self.chain_constructor = chain_constructor
        self.retriever = chain_constructor.retriever
        
    def make_response(self) -> dict[str, str]:
        reply = self._get_reply()
        if reply != None:
            answer = reply['result']

            source_documents_info =[doc.metadata for doc in reply['source_documents']]

            raw_metadata = defaultdict(set)
            for data in source_documents_info:
                document_path = data['source']
                document_name = os.path.basename(document_path)
                raw_metadata[document_name].add(f"page.{int(data['page'])+1}")
            
            first_metadata, pages = next(iter(dict(raw_metadata).items()))

            metadata = "------------------------------------\n參考資料:\n"
            metadata += f" {first_metadata},\n Page: {', '.join(pages)}\n------------------------------------\n" 
            
            logger.info(f"Make response.............Done")
            return answer, metadata
        else:
            answer = "您好，對不起，根據已知的資訊，我無法回答您的問題。請您換一個問題，或是詢問台灣遊戲橘子流程辦法相關的問題，讓我能更好的為您服務，謝謝您。\n 您可以試著詢問我如: \n 如何申請Tableau權限 \n 資訊安全相關規範的注意事項 \n 需求工單如何作業 " 
            metadata = "------------------------------------\n參考資料:\n無\n------------------------------------\n" 
            
            logger.info(f"Make default response.............Done")
            return answer, metadata 
    
    
    def _get_reply(self) -> dict[str, str]:
        if self._is_retrieve():
            qa_chain = self.chain_constructor.form_chain()
            return qa_chain({"query":self.query})
        else:
            return None   
    
    def _is_retrieve(self) -> bool:
        return self.retriever.get_relevant_documents(self.query) != []
        
    
           