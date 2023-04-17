from django.urls import path
from service_backend.apps.users import views

urlpatterns = [
    path('user_login', views.UserLogin.as_view()),
    path('password_modify', views.PasswordModify.as_view()),
    path('modify_user_info', views.ModifyUserInfo.as_view()),
    path('get_user_info', views.GetUserInfo.as_view()),
    path('get_user_subject', views.GetUserSubject.as_view()),
    path('modify_user_subject', views.ModifyUserSubject.as_view()),
    path('check_user_subject', views.CheckUserSubject.as_view()),
    path('get_review_issue', views.GetReviewIssue.as_view()),
    path('get_adopt_issue', views.GetAdoptIssue.as_view()),
    path('get_ask_issue', views.GetAskIssue.as_view()),
    path('get_follow_issue', views.GetFollowIssue.as_view()),
]
