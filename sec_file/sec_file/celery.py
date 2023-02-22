import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sec_file.settings")
app = Celery("sec_file")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()