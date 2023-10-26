from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to uploads/username/<filename>
    return 'uploads/{0}/{1}'.format(instance.username, filename)

class UploadedFile(models.Model):
    username = models.CharField(max_length=255)
    file_field = models.FileField(upload_to=user_directory_path)
