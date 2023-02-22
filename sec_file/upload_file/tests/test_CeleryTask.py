from django.test import TestCase
from upload_file.tasks import FSS_calculator

class CeleryTaskTest(TestCase):

    def test_FSS_calculator(self):
        salary_content_dict = FSS_calculator('salary.txt', 'test_user', {'salary': 10}, [], False)
        self.assertEquals(salary_content_dict['sensitivity_score'], 10)
        
        email_content_dict = FSS_calculator('contains_email.txt', 'test_user', {'salary': 10}, [], False)
        self.assertEquals(email_content_dict['sharing_status'] , 'File was discarded due to security reasons.')