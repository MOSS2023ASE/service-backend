from django.urls import path

from service_backend.apps.issues import v_issue, v_issue_comment, v_issue_status

urlpatterns = [
    path('get', v_issue.IssueGet.as_view()),
    path('follow_check', v_issue.IssueFollowCheck.as_view()),
    path('follow', v_issue.IssueFollow.as_view()),
    path('favorite', v_issue.IssueFavorite.as_view()),
    path('like', v_issue.IssueLike.as_view()),
    path('update', v_issue.IssueUpdate.as_view()),
    path('commit', v_issue.IssueCommit.as_view()),
    path('tags', v_issue.IssueTagList.as_view()),
    path('tags_update', v_issue.IssueTagListUpdate.as_view()),
    path('', v_issue.IssueSearch.as_view()),

    path('cancel', v_issue_status.IssueCancel.as_view()),
    path('classify', v_issue_status.IssueClassify.as_view()),
    path('readopt', v_issue_status.IssueReadopt.as_view()),
    path('review', v_issue_status.IssueReview.as_view()),
    path('agree', v_issue_status.IssueAgree.as_view()),
    path('reject', v_issue_status.IssueReject.as_view()),
    path('adopt', v_issue_status.IssueAdopt.as_view()),

    path('comments', v_issue_comment.CommentList.as_view()),
    path('comment', v_issue_comment.CommentDelete.as_view()),
    path('comment/update', v_issue_comment.CommentUpdate.as_view()),
    path('comment/create', v_issue_comment.CommentCreate.as_view()),
]
