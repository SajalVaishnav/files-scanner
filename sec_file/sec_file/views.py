from django.views import View
from django.http import HttpResponse

class BaseView(View):

    def get(self, request):
        return HttpResponse("""This is the home page. Go to...
                            \n1. /upload_file to upload a file
                            \n2. /keywords/set to set the keywords
                            \n3./get_report to download the report for an uploaded file""", 
                            content_type="text/plain")
