from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import Settings


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealCoolRoom.settings')

app = Celery('RealCoolRoom')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.conf.enable_utc = False
app.conf.update(timezone = 'Africa/Lagos')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_mail_to_users_with_due_date': {
        'task': 'BookingApp.tasks.send_expiration_mail',
        'schedule': crontab(day_of_week='*')
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')