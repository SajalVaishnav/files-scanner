from .MongoCollection import MongoCollection
from .InvalidQueryException import InvalidQueryException
from typing import Tuple

class SensitiveKeywordsCollection(MongoCollection):

    def __init__(self, db_name: str, host: str, port: int) -> None:
        super().__init__(db_name, host, port)
        self.collection = self.db_handle.sens_keywords_collection
        self.is_updated = True
        self.sens_words_values = {}
    
    def check_valid_document_filter(self, doc_filter: dict) -> bool:
        return True

    def get_document(self, doc_filter: dict) -> Tuple[bool, dict]:
        doc = self.collection.find_one()
        self.is_updated = False
        if doc:
            return True, doc
        else:
            return False, doc
    
    
    def check_valid_insert_document(self, doc_data: dict) -> bool:
        return True
        

    def insert_document(self, doc_data: dict) -> None:
        self.is_updated = True
        self.collection.find_one_and_replace({}, doc_data, upsert = True)
    
    def get_kws_dict(self) -> dict:
        if(self.is_updated):
            found, doc = self.get_document({})
            self.sens_words_values = {}
            if found:
                for key in doc:
                    if(key == "_id"):
                        continue
                    self.sens_words_values[key] = doc[key]
        else:
            print("keywords not updated")
            
        return self.sens_words_values
        
        