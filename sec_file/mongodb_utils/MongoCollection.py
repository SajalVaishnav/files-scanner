from pymongo import MongoClient
from abc import ABC, abstractmethod
from typing import Tuple

class MongoCollection:
    
    def __init__(self, db_name: str, host: str, port: int) -> None:
        client = MongoClient(host,
                        port
                    )
        self.db_handle = client[db_name]
    
    @abstractmethod
    def get_document(self, doc_filter: dict) -> Tuple[bool, dict]:
        pass
    
    @abstractmethod
    def insert_document(self, doc_data: dict) -> bool:
        pass
    
    @abstractmethod
    def check_valid_document_filter(self, doc_filter: dict) -> bool:
        pass
    
    @abstractmethod
    def check_valid_insert_document(self, doc_data: dict) -> bool:
        pass
    