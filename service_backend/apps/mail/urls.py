from django.urls import path

from service_backend.apps.mail import views

urlpatterns = [
    path('send', views.SendMail.as_view()),
    path('confirm', views.ConfirmMail.as_view())
]
