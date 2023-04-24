from django.urls import path

from service_backend.apps.issues import views

urlpatterns = [
    path('get', views.IssueGet.as_view()),
    path('cancel', views.IssueCancel.as_view()),
    path('classify', views.IssueClassify.as_view()),
    path('readopt', views.IssueReadopt.as_view()),
    path('review', views.IssueReview.as_view()),
    path('agree', views.IssueAgree.as_view()),
    path('reject', views.IssueReject.as_view()),
    path('adopt', views.IssueAdopt.as_view()),
    path('follow_check', views.IssueFollowCheck.as_view()),
    path('follow', views.IssueFollow.as_view()),
    path('favorite', views.IssueFavorite.as_view()),
    path('like', views.IssueLike.as_view()),
    path('update', views.IssueUpdate.as_view()),
    path('commit', views.IssueCommit.as_view()),
    path('tags', views.IssueTagList.as_view()),
    path('tags_update', views.IssueTagListUpdate.as_view()),
    path('', views.IssueSearch.as_view()),
    path('comments', views.CommentList.as_view()),
    path('comment', views.CommentDelete.as_view()),
    path('comment/update', views.CommentUpdate.as_view()),
    path('comment/create', views.CommentCreate.as_view()),
]
