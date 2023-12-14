from src.ChainConstructor import BaseChainConstructor
import os 
from collections import defaultdict

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
            
            return answer, metadata
        else:
            answer = "對不起，根據已我知的資訊，我無法回答您的問題。"
            metadata = "------------------------------------\n參考資料:\n無\n------------------------------------\n" 
            
            return answer, metadata 
    
    
    def _get_reply(self) -> dict[str, str]:
        if self._is_retrieve():
            qa_chain = self.chain_constructor.form_chain()
            return qa_chain({"query":self.query})
        else:
            return None   
    
    def _is_retrieve(self) -> bool:
        return self.retriever.get_relevant_documents(self.query) != []
        
    
           