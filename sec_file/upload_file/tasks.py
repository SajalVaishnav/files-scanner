from celery import Celery
from celery import shared_task
from django.core.files import File
from django.conf import settings 
import re
import datetime
import os

def get_sens_score(sens_words_values: dict, word_counts: dict, num_users: int) -> int:
    sens_score = 0
    for word in word_counts:
        sens_score += word_counts[word] * sens_words_values[word]
    
    sens_score *= num_users
    return sens_score

def get_sens_level(sens_score: int) -> str:
    sens_level = ""
    if(sens_score >= 100):
        sens_level = "High"
    elif(sens_score >= 51):
        sens_level = "Medium"
    elif(sens_score >= 1):
        sens_level = "Low"
    else:
        sens_level = "Non-sensitive" 
    
    return sens_level

def FSS_calculator(file_name: str, username: str, sens_words_values: dict, user_list: list, is_prod: bool) -> dict:
    if username in user_list:
        num_users = len(user_list)
    else:
        num_users = len(user_list) + 1

    word_counts = {}
    for word in sens_words_values:
        word_counts[word] = 0
    
    share_status = "Succesfully shared."

    uploads_directory = 'test_files/'
    if is_prod:
        uploads_directory = 'uploads/'

    with open(uploads_directory + username + "/" + file_name, 'r') as f:
        user_file = File(f)
        for chunk in user_file.chunks():
            # print(chunk)
            for word in sens_words_values:
                word_counts[word] = chunk.count(word) + word_counts[word]
            if re.match(r'[\w.+-]+@[\w-]+\.[\w.-]+', chunk):
                share_status = "File was discarded due to security reasons."
        # print(word_counts)
    
    sens_score = get_sens_score(sens_words_values, word_counts, num_users)

    sens_level = get_sens_level(sens_score)
    if(sens_level == "High"):
        share_status = "File was discarded due to security reasons."

    file_report = {
        "file_name": file_name,
        "user": username,
        "sensitivity_score": sens_score,
        "sensitivity_level": sens_level,
        "sharing_status": share_status,
        "file_uploaded_at": datetime.datetime.utcnow()
    }

    return file_report


@shared_task()
def FSS(file_name: str, username: str) -> None:
    sens_words_values = settings.SENS_KEYWORDS_COLLECTION.get_kws_dict()

    user_list = settings.FILE_RECORDS_COLLECTION.get_user_list()

    
    file_report = FSS_calculator(file_path, username, sens_words_values, user_list, True)

    settings.FILE_RECORDS_COLLECTION.insert_document(file_report)

    uploads_directory = 'test_files/'
    if is_prod:
        uploads_directory = 'uploads/'
    file_path = uploads_directory + username + "/" + file_name
    os.remove(file_path)

    return file_report
    