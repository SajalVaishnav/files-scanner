from django.test import TestCase
from mongodb_utils.FileRecordsCollection import FileRecordsCollection

class FileRecordsCollectionTest(TestCase):
    
    invalid_query = {
        "not_file_name": "temp.txt",
        "not_user": "not_u1"
    }

    valid_query = {
        "file_name": "temp.txt",
        "user": "not_u1"
    }

    invalid_doc_insert = {
        "file_name": "temp.txt",
        "user": "not_u1"
    }

    valid_doc_insert = {
        'file_name': 'file_name',
        'user': 'user',
        'sensitivity_score': 'sensitivity_score',
        'sensitivity_level': 'sensitivity_level',
        'sharing_status': 'sharing_status',
        'file_uploaded_at': 'some-date'
    }

    def setUp(self):
        self.TEST_COLLECTION = FileRecordsCollection('test_database', 'localhost', 27017)

    def test_check_valid_insert_document(self):
        self.assertTrue(self.TEST_COLLECTION.check_valid_insert_document(self.valid_doc_insert))
        self.assertFalse(self.TEST_COLLECTION.check_valid_insert_document(self.invalid_doc_insert))
    
    def test_check_valid_document_filter(self):
        self.assertTrue(self.TEST_COLLECTION.check_valid_document_filter(self.valid_query))
        self.assertFalse(self.TEST_COLLECTION.check_valid_document_filter(self.invalid_query))