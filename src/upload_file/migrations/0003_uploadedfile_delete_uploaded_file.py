# Generated by Django 4.1.4 on 2022-12-17 10:50

from django.db import migrations, models
import upload_file.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_file', '0002_uploaded_file_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('file_field', models.FileField(upload_to=upload_file.models.user_directory_path)),
            ],
        ),
        migrations.DeleteModel(
            name='Uploaded_file',
        ),
    ]