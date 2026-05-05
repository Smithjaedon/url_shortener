from celery import shared_task
from .models import Url
import datetime


@shared_task
def url_garbage_collection():
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=5)

    deleted, _ = Url.objects.filter(last_accessed__lt=time_threshold).delete()
    return f"Deleted {deleted} inactive urls"
