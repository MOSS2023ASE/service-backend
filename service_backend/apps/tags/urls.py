from django.urls import path
from service_backend.apps.tags import views

urlpatterns = [
    path('', views.TagList.as_view()),
    path('create', views.TagCreate.as_view()),
    path('update', views.TagUpdate.as_view()),
    path('delete', views.TagDelete.as_view())
]
