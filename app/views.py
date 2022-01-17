from django.http import HttpResponse

from .tasks import add


def test_celery(request):
    add.delay(3, 5)
    return HttpResponse("Celery works")
