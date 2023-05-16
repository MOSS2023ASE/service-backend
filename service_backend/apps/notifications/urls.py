from django.urls import path
from service_backend.apps.notifications import views

urlpatterns = [
    path('clear_all', views.NotificationClear.as_view()),
    path('get', views.NotificationRead.as_view()),
    path('user_receive', views.NotificationList.as_view()),
    path('broadcast', views.NotificationBroadcast.as_view()),
]
