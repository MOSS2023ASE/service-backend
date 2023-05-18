from django.urls import path

from service_backend.apps.issues import views_issue, views_issue_comment, views_issue_status, views_issue_draft, \
    views_issue_association

urlpatterns = [
    path('get', views_issue.IssueGet.as_view()),
    path('follow_check', views_issue.IssueFollowCheck.as_view()),
    path('follow', views_issue.IssueFollow.as_view()),
    path('favorite', views_issue.IssueFavorite.as_view()),
    path('like', views_issue.IssueLike.as_view()),
    path('update', views_issue.IssueUpdate.as_view()),
    path('commit', views_issue.IssueCommit.as_view()),
    path('tags', views_issue.IssueTagList.as_view()),
    path('tags_update', views_issue.IssueTagListUpdate.as_view()),
    path('', views_issue.IssueSearch.as_view()),

    path('cancel', views_issue_status.IssueCancel.as_view()),
    path('classify', views_issue_status.IssueClassify.as_view()),
    path('readopt', views_issue_status.IssueReadopt.as_view()),
    path('review', views_issue_status.IssueReview.as_view()),
    path('agree', views_issue_status.IssueAgree.as_view()),
    path('reject', views_issue_status.IssueReject.as_view()),
    path('adopt', views_issue_status.IssueAdopt.as_view()),

    path('comments', views_issue_comment.CommentList.as_view()),
    path('comment', views_issue_comment.CommentDelete.as_view()),
    path('comment/update', views_issue_comment.CommentUpdate.as_view()),
    path('comment/create', views_issue_comment.CommentCreate.as_view()),

    path('save_draft', views_issue_draft.SaveDraft.as_view()),
    path('load_draft', views_issue_draft.LoadDraft.as_view()),

    path('associate', views_issue_association.AddAssociation.as_view()),
    path('associate/get', views_issue_association.GetAssociation.as_view()),
    path('associate/delete', views_issue_association.DeleteAssociation.as_view())
]
