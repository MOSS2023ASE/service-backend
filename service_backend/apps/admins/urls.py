from django.urls import path
from service_backend.apps.admins import views

urlpatterns = [
    path('update_privilege', views.UpdateUserRole.as_view()),
    path('users', views.UserList.as_view()),
    path('freeze_user', views.FreezeUser.as_view()),
    path('issue/delete', views.DeleteIssue.as_view()),
    path('create_user', views.CreateUser.as_view()),
    path('create_user_batch', views.CreateUser.as_view()),
]
