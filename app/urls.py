from django.urls import path

from app import views

urlpatterns = [
    path('test/', views.test_celery, name="test_celery")
]
