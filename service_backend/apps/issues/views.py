from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.issues.models import Issue
from service_backend.apps.utils.views import response_json
from service_backend.apps.issues.serializers import IssueSerializer


# TODO
def _find_issue(func):
    def wrapper(request, *args, **kwargs):
        try:
            issue = Issue.objects.get(id=request.data['issue_id'])
        except Exception as e:
            return Response(response_json(
                success=False,
                # TODO
                code=1,
                message="can't find issue!"
            ))
        return func(request, issue, *args, **kwargs)

    return wrapper


# Create your views here.
@_find_issue
class IssueGet(APIView):
    def get(self, request, issue):
        issue_serializer = IssueSerializer(issue)
        data = issue_serializer.data

        print(data)
        counselors = issue.adopt_issues.user
        print(counselors)


@_find_issue
class IssueReview(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueAgree(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueReject(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueAdopt(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueCancel(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueClassify(APIView):
    def post(self, request, issue):
        pass


@_find_issue
class IssueReadopt(APIView):
    def post(self, request, issut):
        pass


@_find_issue
class IssueTags(APIView):
    pass


@_find_issue
class IssueTagsUpdate(APIView):
    pass


@_find_issue
class IssueFollowCheck(APIView):
    pass


@_find_issue
class IssueFollow(APIView):
    pass


@_find_issue
class IssueFavorite(APIView):
    pass


@_find_issue
class IssueLike(APIView):
    pass


@_find_issue
class IssueUpdate(APIView):
    pass


@_find_issue
class IssueCommit(APIView):
    pass


class IssueSearch(APIView):
    pass
