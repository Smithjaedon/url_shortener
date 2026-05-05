import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_shortener.settings")

app = Celery("url_shortener")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "cleanup-inactive-urls": {
        "task": "shortener.tasks.url_garbage_collection",
        "schedule": crontab(minute="*/1"),
    }
}
