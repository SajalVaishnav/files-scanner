from django.http import HttpResponse
from django.conf import settings
from django.views import View

class GetReport(View):

    invalid_user_or_filename_res = HttpResponse("""Please provide a valid username and file name as url parameters.
                                                \n eg. get_report/?user=u1&file=temp.txt""", 
                                    content_type="text/plain")
    
    no_record_found_res = HttpResponse("""No records found for the specified user and file. Please check the following:
                                    \n1. That the user name and file name specified are correct (file name should include the file type extension)
                                    \n2. If user and the file name are accurate, then the file is still being processed. Please try the query later.
                                    \n3. Lastly, it is possible that something went wrong during the file upload so please upload the file and try again.""", 
                                    content_type="text/plain")
    
    def dict_to_readable_string(self, doc: dict) -> str:
        final_str = ""
        for key, value in doc.items():
            if(type(value) != list):
                final_str += str(key) + ": " + str(value) + "\n"
            else:
                final_str += str(key) + ":\n"
                for element in value:
                    final_str += "\t" + str(element) + "\n"

        return final_str 

    def get(self, request):
        file_name = request.GET.get('file', '')
        user = request.GET.get('user', '')

        if(len(user) == 0 or len(file_name) == 0):
            return self.invalid_user_or_filename_res

        found, doc = settings.FILE_RECORDS_COLLECTION.get_document({
                                                            "file_name": file_name,
                                                            "user": user
                                                        })
        
        if found:
            store_metadata = settings.FILE_RECORDS_COLLECTION.get_store_metadata()
            
            file_record_as_string = self.dict_to_readable_string(doc)
            store_metadata_as_string = self.dict_to_readable_string(store_metadata)
            return HttpResponse(
                                file_record_as_string + store_metadata_as_string, 
                                headers={
                                            'Content-Type': 'text/plain',
                                            'Content-Disposition': 'attachment; filename=report_{}'.format(doc['file_name']),
                                        }
                                )
        else:
            return self.no_record_found_res
        



                                                                                                                                                                                                                                        