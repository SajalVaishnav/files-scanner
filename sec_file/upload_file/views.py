from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
from django.core.files.storage import default_storage
from pathlib import Path
from sec_file.settings import BASE_DIR
from .tasks import FSS
from django.views import View


class UploadFile(View):

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            file_name = request.FILES['file'].name
            file_instance = UploadedFile(username=username, file_field=request.FILES['file'])
            
            file_path = Path(str(BASE_DIR) + '/uploads/' + username + "/" + file_name)
            if(default_storage.exists(file_path)):
                default_storage.delete(file_path)

            file_instance.save()

            FSS.delay(file_name, username)
            
            return HttpResponseRedirect('success')
        return render(request, 'upload_file/upload.html', {'form': form})
            

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'upload_file/upload.html', {'form': form})

class FileUploadedSuccessfully(View):
    
    def get(self, request):
        return HttpResponse("""File has been added to the processing queue!
                            \nYou can get the report by going to the /get_report/ end point.
                            """, 
                            content_type="text/plain")