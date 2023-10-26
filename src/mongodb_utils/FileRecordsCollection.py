from .MongoCollection import MongoCollection
from .InvalidQueryException import InvalidQueryException
from typing import Tuple
from pymongo import DESCENDING

class FileRecordsCollection(MongoCollection):

    def __init__(self, db_name: str, host: str, port: int) -> None:
        super().__init__(db_name, host, port)
        self.collection = self.db_handle.file_records_collection
        self.collection.create_index([("sensitivity_score", DESCENDING)])
    
    def check_valid_document_filter(self, doc_filter: dict) -> bool:
        if(type(doc_filter) != dict):
            return False

        if('file_name' not in doc_filter):
            return False
        
        if('user' not in doc_filter):
            return False

        return True

    def get_document(self, doc_filter: dict) -> Tuple[bool, dict]:
        if not self.check_valid_document_filter(doc_filter):
            raise InvalidQueryException("""Please provide a valid JSON-style dict with the following keys: 
                                        \n1. file_name 
                                        \n2. user 
                                        """)
        
        doc = self.collection.find_one(doc_filter)

        if doc:
            file_record = {
                'file_name': (doc['file_name']),
                'user': doc['user'],
                'sensitivity_score': str(doc['sensitivity_score']),
                'sensitivity_level': doc['sensitivity_level'],
                'sharing_status': doc['sharing_status']
            }
            return True, file_record

        return False, doc
    
    def check_valid_insert_document(self, doc_data: dict) -> bool:
        if not self.check_valid_document_filter(doc_data):
            return False

        if(len(doc_data.keys()) != 6):
            return False
        
        if("sensitivity_score" not in doc_data):
            return False

        if("sensitivity_level" not in doc_data):
            return False

        if("sharing_status" not in doc_data):
            return False
        
        if("file_uploaded_at" not in doc_data):
            return False

        return True

    def insert_document(self, doc_data: dict) -> None:
        if not self.check_valid_insert_document(doc_data):
            raise InvalidQueryException("""Please provide a valid JSON-style dict with the following keys: 
                                        \n1. file_name 
                                        \n2. user
                                        \n3. sensitivity_score 
                                        \n4. sensitivity_level
                                        \n5. sharing_status 
                                        \n6. file_uploaded_at
                                        """)
        
        self.collection.find_one_and_replace({
                                                "file_name": doc_data["file_name"],
                                                "user": doc_data["user"]
                                            }, 
                                            doc_data, 
                                            upsert = True)

    def get_user_list(self) -> list:
        return self.collection.distinct("user")
    
    def get_store_metadata(self) -> dict:
        # Total files in the system
        files_count = self.collection.count_documents({})
        # Total of high, medium, low sensitive level files
        high_sens_files_count = self.collection.count_documents({"sensitivity_level": "High"})
        med_sens_files_count = self.collection.count_documents({"sensitivity_level": "Medium"})
        low_sens_files_count = self.collection.count_documents({"sensitivity_level": "Low"})
        # Top 10 files that have highest sensitive score
        top_ten_risk_files = self.collection.find().sort('sensitivity_score', DESCENDING).limit(10)
        top_ten_risk_files_list = []
        for doc in top_ten_risk_files:
            file_summary = {
                'file_name': doc['file_name'],
                'user': doc['user'],
                'sensitivity_score': doc['sensitivity_score'],
                'file_uploaded_at': doc['file_uploaded_at']
            }
            top_ten_risk_files_list.append(file_summary)
        
        return {
            'files_count': files_count,
            'high_sens_files_count': high_sens_files_count,
            'med_sens_files_count': med_sens_files_count, 
            'low_sens_files_count': low_sens_files_count,           
            'top_ten_risk_files': top_ten_risk_files_list
        } 