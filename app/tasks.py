from celery import shared_task
import time


@shared_task(time_limit=10)
def add(x, y):
    time.sleep(2)
    return x + y
