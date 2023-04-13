from django.urls import path
from service_backend.apps.users import views

urlpatterns = [
    path('user_login', views.UserLogin.as_view()),
]
