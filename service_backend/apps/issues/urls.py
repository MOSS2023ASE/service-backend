from django.urls import path

from service_backend.apps.issues import issue_views, issue_comment_views, issue_status_views, issue_draft_views

urlpatterns = [
    path('get', issue_views.IssueGet.as_view()),
    path('follow_check', issue_views.IssueFollowCheck.as_view()),
    path('follow', issue_views.IssueFollow.as_view()),
    path('favorite', issue_views.IssueFavorite.as_view()),
    path('like', issue_views.IssueLike.as_view()),
    path('update', issue_views.IssueUpdate.as_view()),
    path('commit', issue_views.IssueCommit.as_view()),
    path('tags', issue_views.IssueTagList.as_view()),
    path('tags_update', issue_views.IssueTagListUpdate.as_view()),
    path('', issue_views.IssueSearch.as_view()),

    path('cancel', issue_status_views.IssueCancel.as_view()),
    path('classify', issue_status_views.IssueClassify.as_view()),
    path('readopt', issue_status_views.IssueReadopt.as_view()),
    path('review', issue_status_views.IssueReview.as_view()),
    path('agree', issue_status_views.IssueAgree.as_view()),
    path('reject', issue_status_views.IssueReject.as_view()),
    path('adopt', issue_status_views.IssueAdopt.as_view()),

    path('comments', issue_comment_views.CommentList.as_view()),
    path('comment', issue_comment_views.CommentDelete.as_view()),
    path('comment/update', issue_comment_views.CommentUpdate.as_view()),
    path('comment/create', issue_comment_views.CommentCreate.as_view()),

    path('save_draft', issue_draft_views.SaveDraft.as_view()),
    path('load_draft', issue_draft_views.LoadDraft.as_view())
]
