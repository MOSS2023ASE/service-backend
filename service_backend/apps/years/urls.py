from django.urls import path
from service_backend.apps.years import views

urlpatterns = [
    path('', views.YearList.as_view()),
    path('create', views.YearCreate.as_view()),
    path('update', views.YearUpdate.as_view()),
    path('delete', views.YearDelete.as_view()),
    path('update_current', views.YearCurrentUpdate.as_view())
]
