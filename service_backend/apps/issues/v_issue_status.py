import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.issues.v_issue import find_issue, status_trans_permit
from service_backend.apps.issues.models import AdoptIssues, ReviewIssues
from service_backend.apps.utils.constants import UserRole, IssueStatus, IssueErrorCode, IssueReviewerErrorCode, \
    OtherErrorCode
from service_backend.apps.utils.views import response_json, check_role


class IssueAdopt(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[0] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.counselor = action_user
        issue.counsel_at = datetime.datetime.now()
        issue.status = IssueStatus.ADOPTING
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't adopt issue!"
            ), status=404)
        adopt_issue = AdoptIssues(issue=issue, user=action_user, status=0)
        try:
            adopt_issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueReviewerErrorCode.REVIEWER_ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="adopt issue success!"
        ))


class IssueCancel(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[1] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.status = IssueStatus.INVALID_ISSUE
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't cancel issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="cancel issue success!"
        ))


class IssueReject(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[2] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.counselor = None
        issue.counsel_at = None
        issue.status = IssueStatus.NOT_ADOPT
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't reject issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="reject issue success!"
        ))


class IssueAgree(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[3] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.status = IssueStatus.NOT_REVIEW
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="agree review success!"
        ))


class IssueReview(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[4] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.reviewer = action_user
        issue.status = IssueStatus.REVIEWING
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)

        reviewer_issue = ReviewIssues(issue=issue, user=action_user, reviewed=issue.counselor)
        try:
            reviewer_issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueReviewerErrorCode.REVIEWER_ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="adopt review success!"
        ))


class IssueReadopt(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[5] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.status = IssueStatus.ADOPTING
        issue.counselor = action_user
        issue.counsel_at = datetime.datetime.now()

        adopt_issue = AdoptIssues(issue=issue, user=action_user, status=0)
        try:
            adopt_issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueReviewerErrorCode.REVIEWER_ISSUE_SAVED_FAILED,
                message="can't readopt issue!"
            ), status=404)

        reviewer_issue = ReviewIssues.objects.filter(issue=issue, user=action_user)
        reviewer_issue.first().status = 0

        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't readopt issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="readopt issue success!"
        ))


class IssueClassify(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user):
        if status_trans_permit(issue, action_user)[6] != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        if request.data['is_valid'] == 1:
            issue.status = IssueStatus.VALID_ISSUE
        elif request.data['is_valid'] == 0:
            issue.status = IssueStatus.INVALID_ISSUE
        else:
            return Response(response_json(
                success=False,
                code=OtherErrorCode.UNEXPECTED_JSON_FORMAT,
                message="is_valid is not valid!"
            ), status=404)
        reviewer_issue = ReviewIssues.objects.filter(issue=issue, user=action_user)
        reviewer_issue.first().status = 1
        try:
            issue.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't classify issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="classify issue success!"
        ))
