from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.issues.models import Issue, IssueAssociations
from service_backend.apps.issues.serializer_issue import IssueSearchSerializer
from service_backend.apps.issues.views_issue import find_issue, allow_relate
from service_backend.apps.utils.constants import UserRole, IssueErrorCode
from service_backend.apps.utils.views import check_role, response_json


class AddAssociation(APIView):
    @find_issue()
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    def post(self, request, issue, action_user):
        if allow_relate(issue, action_user) != 1:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)
        try:
            associate_issue = Issue.objects.get(id=request.data['issue_associate_id'])
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_NOT_FOUND,
                message="can't find issue!"
            ), status=404)
        if IssueAssociations.objects.filter(issue=issue, associate_issue=associate_issue):
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_RELATE_FAILED,
                message="already relate!"
            ))

        association = IssueAssociations(issue=issue, associate_issue=associate_issue)
        try:
            association.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_RELATE_FAILED,
                message="add relate success!"
            ))
        return Response(response_json(
            success=True,
            message="add relate success!"
        ))


class GetAssociation(APIView):
    @find_issue()
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    def post(self, request, issue, action_user):
        associate_issues = [i.associate_issue for i in issue.associate_issues_as_from.all()]
        issue_list = IssueSearchSerializer(associate_issues, many=True).data
        return Response(response_json(
            success=True,
            data={
                "issue_list": issue_list
            }
        ))


class DeleteAssociation(APIView):
    @find_issue()
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    def post(self, request, issue, action_user):
        try:
            associate_issue = Issue.objects.get(id=request.data['issue_associate_id'])
        except Exception:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_NOT_FOUND,
                message="can't find issue!"
            ), status=404)
        associations = IssueAssociations.objects.filter(issue=issue, associate_issue=associate_issue)
        if associations:
            associations.delete()
        return Response(response_json(
            success=True,
            message="delete association success!"
        ))
