from django.urls import path
from service_backend.apps.subjects import views

urlpatterns = [
    path('', views.SubjectList.as_view()),
    path('create', views.SubjectCreate.as_view()),
    path('update', views.SubjectUpdate.as_view()),
    path('delete', views.SubjectDelete.as_view())
]
