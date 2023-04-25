# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

app = Celery('auth')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    'run-task-every-30-seconds': {
        "task": "api.tasks.hello",
        "schedule": 10.0,
    },
    'send-daily-user-signup-email': {
        'task': 'api.tasks.send_daily_user_signup_email',
        'schedule': crontab(minute=0, hour=0),
    },
    'check-db-health': {
        "task": "api.tasks.check_db_health",
        "schedule": 60.0,
    },
}
