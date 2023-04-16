from django.urls import path
from service_backend.apps.users import views

urlpatterns = [
    path('user_login', views.UserLogin.as_view()),
    path('modify_user_info', views.ModifyUserInfo.as_view()),
    path('get_user_info', views.GetUserInfo.as_view())
]
