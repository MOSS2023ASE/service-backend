from django.urls import path
from service_backend.apps.admins import views

urlpatterns = [
    path('single_create', views.UserCreate.as_view()),
]
