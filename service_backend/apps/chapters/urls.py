from django.urls import path
from service_backend.apps.chapters import views

urlpatterns = [
    path('', views.ChapterList.as_view()),
    path('create', views.ChapterCreate.as_view()),
    path('update', views.ChapterUpdate.as_view()),
    path('delete', views.ChapterDelete.as_view())
]
