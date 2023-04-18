from django.urls import path
from service_backend.apps.images import views

urlpatterns = [
    path('upload/', views.UploadImage.as_view()),
]
