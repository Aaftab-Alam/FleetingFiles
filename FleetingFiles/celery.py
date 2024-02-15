"""
Celery Configuration

This module configures Celery for the FleetingFiles project.

Functions:
- debug_task(self): A Celery task for debugging purposes.

"""

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery("FleetingFiles")
app.conf.enable_utc = True

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# celery -A FleetingFiles.celery worker --pool=solo  -l info
