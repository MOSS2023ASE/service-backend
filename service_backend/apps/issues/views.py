import datetime
import math
from functools import wraps

from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.chapters.views import _find_chapter
from service_backend.apps.subjects.models import UserSubject
from service_backend.apps.tags.models import IssueTag, Tag
from service_backend.apps.issues.models import Issue, Comment, LikeIssues, FollowIssues, AdoptIssues, ReviewIssues
from service_backend.apps.utils.constants import UserRole, IssueStatus, IssueErrorCode, CommentErrorCode, \
    IssueLikeErrorCode, IssueFollowErrorCode, IssueTagErrorCode, IssueReviewerErrorCode, OtherErrorCode
from service_backend.apps.utils.views import response_json, check_role
from service_backend.apps.issues.serializers import IssueSerializer, CommentSerializer, IssueSearchSerializer
from service_backend.apps.utils.filter import Filter


def _find_issue():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                issue = Issue.objects.get(id=args[1].data['issue_id'])
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=IssueErrorCode.ISSUE_NOT_FOUND,
                    message="can't find issue!"
                ), status=404)
            return func(*args, **kwargs, issue=issue)

        return wrapper

    return decorated


def status_trans_permit(issue, action_user):
    status = [0, 0, 0, 0, 0, 0, 0]
    if issue.status == IssueStatus.NOT_ADOPT and \
            action_user.user_role == UserRole.TUTOR and \
            UserSubject.objects.filter(user=action_user, subject=issue.chapter.subject):
        adopt_issues = AdoptIssues.objects.filter(issue=issue).all()
        adopted = [adopt_issue.user for adopt_issue in adopt_issues]
        if action_user not in adopted:
            status[0] = 1
    if issue.status == IssueStatus.NOT_ADOPT and \
            action_user.user_role == UserRole.STUDENT and \
            issue.user == action_user:
        status[1] = 1
    if issue.status == IssueStatus.ADOPTING and \
            action_user.user_role == UserRole.STUDENT and \
            issue.user == action_user:
        status[2] = 1
        status[3] = 1
    if issue.status == IssueStatus.NOT_REVIEW and \
            action_user.user_role == UserRole.TUTOR and \
            UserSubject.objects.filter(user=action_user, subject=issue.chapter.subject) and \
            issue.counselor != action_user:
        status[4] = 1
    if issue.status == IssueStatus.REVIEWING and \
            action_user.user_role == UserRole.TUTOR and \
            issue.reviewer == action_user:
        status[5] = 1
        status[6] = 1
    return status


def allow_comment(issue, action_user):
    allow = 0
    if issue.status == IssueStatus.NOT_ADOPT and \
            action_user.user_role == UserRole.STUDENT and \
            action_user == issue.user:
        allow = 1
    if issue.status == IssueStatus.ADOPTING and \
            (action_user.user_role == UserRole.STUDENT or action_user.user_role == UserRole.TUTOR) and \
            (action_user == issue.user or action_user == issue.counselor):
        allow = 1
    return allow


# Create your views here.

class IssueGet(APIView):
    @check_role(UserRole.ALL_USERS)
    @_find_issue()
    def post(self, request, issue, action_user):
        if action_user.user_role == UserRole.STUDENT and \
                action_user.id != issue.user_id and \
                issue.status != IssueStatus.VALID_ISSUE:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue_serializer = IssueSerializer(issue)
        data = issue_serializer.data
        adopter_issues = AdoptIssues.objects.filter(issue=issue).order_by('created_at')
        counselor_list = [{
            "user_id": adopter_issue.user.id,
            "user_name": adopter_issue.user.name,
            "user_avatar": adopter_issue.user.avatar
        } for adopter_issue in adopter_issues]
        reviewer_issues = ReviewIssues.objects.filter(issue=issue).order_by('created_at')
        reviewer_list = [{
            "user_id": reviewer_issue.user.id,
            "user_name": reviewer_issue.user.name,
            "user_avatar": reviewer_issue.user.avatar
        } for reviewer_issue in reviewer_issues]
        data['allow_comment'] = allow_comment(issue, action_user)
        data['status_trans_permit'] = status_trans_permit(issue, action_user)
        data['counselor_list'] = counselor_list
        data['reviewer_list'] = reviewer_list
        return Response(response_json(
            success=True,
            data=data
        ))


class IssueReview(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.NOT_REVIEW or \
                action_user.id == issue.counselor_id:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)
        issue.reviewer = action_user
        issue.status = IssueStatus.REVIEWING
        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)

        reviewer_issue = ReviewIssues(issue=issue, user=action_user, reviewed=issue.counselor)
        try:
            reviewer_issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueReviewerErrorCode.REVIEWER_ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="adopt review success!"
        ))


class IssueAgree(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.ADOPTING or \
                (action_user.user_role == UserRole.STUDENT and
                 action_user.id != issue.user_id):
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.status = IssueStatus.NOT_REVIEW
        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't review issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="agree review success!"
        ))


class IssueReject(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.ADOPTING and \
                (action_user.user_role == UserRole.STUDENT and
                 action_user.id != issue.user_id):
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
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't reject issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="reject issue success!"
        ))


class IssueAdopt(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        adopt_issues = AdoptIssues.objects.filter(issue=issue).all()
        adopted = [adopt_issue.user for adopt_issue in adopt_issues]
        if issue.status != IssueStatus.NOT_ADOPT or \
                action_user in adopted:
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
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't adopt issue!"
            ), status=404)
        adopt_issue = AdoptIssues(issue=issue, user=action_user, status=0)
        try:
            adopt_issue.save()
        except Exception as e:
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
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.NOT_ADOPT or \
                (action_user.user_role == UserRole.STUDENT and
                 action_user.id != issue.user_id):
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_ACTION_REJECT,
                message="you have no access to this issue!"
            ), status=404)

        issue.status = IssueStatus.INVALID_ISSUE
        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't cancel issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="cancel issue success!"
        ))


class IssueClassify(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.REVIEWING or \
                (action_user.id != issue.reviewer_id):
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
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't classify issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="classify issue success!"
        ))


class IssueReadopt(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        if issue.status != IssueStatus.REVIEWING or \
                (action_user.id != issue.reviewer_id):
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
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueReviewerErrorCode.REVIEWER_ISSUE_SAVED_FAILED,
                message="can't readopt issue!"
            ), status=404)

        reviewer_issue = ReviewIssues.objects.filter(issue=issue, user=action_user)
        reviewer_issue.first().status = 0

        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't readopt issue!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="readopt issue success!"
        ))


class IssueTagList(APIView):
    @check_role(UserRole.ALL_USERS)
    @_find_issue()
    def post(self, request, issue, action_user):
        issue_tags = IssueTag.objects.filter(issue=issue)
        tags = [issue_tag.tag for issue_tag in issue_tags]
        data = {
            "tag_list": [
                {
                    "tag_id": tag.id,
                    "tag_content": tag.content
                }
                for tag in tags
            ]
        }
        return Response(response_json(
            success=True,
            data=data
        ))


class IssueTagListUpdate(APIView):
    @check_role([UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        # 是否有更加优美的实现方式？
        tag_id_list = request.data['tag_list']
        tags = [Tag.objects.get(id=tag_id) for tag_id in tag_id_list]
        for tag in tags:
            issue_tag = IssueTag.objects.filter(issue=issue, tag=tag)
            if not issue_tag:
                obj = IssueTag(issue=issue, tag=tag)
                try:
                    obj.save()
                except Exception as e:
                    return Response(response_json(
                        success=False,
                        code=IssueTagErrorCode.ISSUE_TAG_SAVED_FAILED,
                        message="can't save issue tag!"
                    ), status=404)
        issue_tags = IssueTag.objects.filter(issue=issue)
        now_tags = [issue_tag.tag for issue_tag in issue_tags]
        for tag in now_tags:
            if tag not in tags:
                issue_tag = IssueTag.objects.filter(issue=issue, tag=tag)
                try:
                    issue_tag.delete()
                except Exception as e:
                    return Response(response_json(
                        success=False,
                        code=IssueTagErrorCode.ISSUE_TAG_DELETE_FAILED,
                        message="can't delete issue tag!"
                    ), status=404)

        return Response(response_json(
            success=True
        ))


class IssueFollowCheck(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        is_follow = FollowIssues.objects.filter(issue=issue, user=action_user)
        if not is_follow:
            return Response(response_json(
                success=True,
                data={
                    "is_follow": 0,
                    "follow_count": issue.follows
                }
            ))
        else:
            return Response(response_json(
                success=True,
                data={
                    "is_follow": 1,
                    "follow_count": issue.follows
                }
            ))


class IssueFollow(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        is_follow = FollowIssues.objects.filter(issue=issue, user=action_user)
        if not is_follow:
            follow = FollowIssues(issue=issue, user=action_user)
            issue.follows = issue.follows + 1
            try:
                follow.save()
                issue.save()
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=IssueFollowErrorCode.ISSUE_FOLLOW_SAVED_FAILED,
                    message="follow issue failed!"
                ), status=404)
            return Response(response_json(
                success=True,
                data={
                    "is_follow": 1,
                    "follow_count": issue.follows
                }
            ))
        else:
            try:
                is_follow.delete()
                issue.follows = issue.follows - 1
                issue.save()
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=IssueFollowErrorCode.ISSUE_FOLLOW_DELETE_FAILED,
                    message="cancel follow failed!"
                ), status=404)
            return Response(response_json(
                success=True,
                data={
                    "is_follow": 0,
                    "follow_count": issue.follows
                }
            ))


class IssueFavorite(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        is_like = LikeIssues.objects.filter(issue=issue, user=action_user)
        if not is_like:
            return Response(response_json(
                success=True,
                data={
                    "is_like": 0,
                    "like_count": issue.likes
                }
            ))
        else:
            return Response(response_json(
                success=True,
                data={
                    "is_like": 1,
                    "like_count": issue.likes
                }
            ))


class IssueLike(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        is_like = LikeIssues.objects.filter(issue=issue, user=action_user)
        if not is_like:
            like = LikeIssues(issue=issue, user=action_user)
            issue.likes = issue.likes + 1
            try:
                like.save()
                issue.save()
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=IssueLikeErrorCode.ISSUE_LIKE_SAVED_FAILED,
                    message="like issue failed!!"
                ), status=404)
            return Response(response_json(
                success=True,
                data={
                    "is_like": 1,
                    "like_count": issue.likes
                }
            ))
        else:
            try:
                is_like.delete()
                issue.likes = issue.likes - 1
                issue.save()
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=IssueLikeErrorCode.ISSUE_LIKE_DELETE_FAILED
                ), status=404)
            return Response(response_json(
                success=True,
                data={
                    "is_like": 0,
                    "like_count": issue.likes
                }
            ))


class IssueUpdate(APIView):
    @_find_chapter()
    @_find_issue()
    def post(self, request, issue, chapter):
        issue.title = request.data['title']
        issue.content = request.data['content']
        issue.anonymous = request.data['anonymous']
        issue.chapter = chapter
        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't save issue!"
            ), status=404)
        return Response(response_json(
            success=True
        ))


class IssueCommit(APIView):
    @check_role([UserRole.STUDENT, UserRole.ADMIN, ])
    @_find_chapter()
    def post(self, request, chapter, action_user):
        title = request.data['title']
        content = request.data['content']
        anonymous = request.data['anonymous']
        status = IssueStatus.NOT_ADOPT
        issue = Issue(title=title, content=content, user=action_user, chapter=chapter, status=status,
                      anonymous=anonymous)
        try:
            issue.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_SAVED_FAILED,
                message="can't save issue!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="issue commit success!"
        ))


class IssueSearch(APIView):
    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user):
        keyword = request.data['keyword']
        tag_list = request.data['tag_list']
        status_list = request.data['status_list']
        chapter_list = request.data['chapter_list']
        order = request.data['order']
        page_no = request.data['page_no']
        issue_per_page = request.data['issue_per_page']
        issues = Issue.objects.all()
        if keyword:
            issues = Issue.objects.filter(title__contains=keyword)

        if status_list:
            q = []
            for status in status_list:
                q = q.union(issues.filter(status=status)) if q else issues.filter(status=status)
            issues = issues & q
        if chapter_list:
            q = []
            for chapter in chapter_list:
                q = q.union(issues.filter(chapter_id=chapter)) if q else issues.filter(chapter_id=chapter)
            issues = issues & q
        if tag_list:
            q = []
            for tag in tag_list:
                q = q.union(issues.filter(tag_id=tag)) if q else issues.filter(tag_id=tag)
            issues = issues & q

        if order == 0:
            issues = issues.order_by('-created_at')
        elif order == 1:
            issues = issues.order_by('created_at')
        elif order == 2:
            issues = issues.annotate(heat=F('likes') + 5 * F('follows')).order_by('-heat')
        else:
            pass

        # 0：最近优先，1：最早优先，2：最热优先，3：综合排序（综合排序方式待定，可以先随便排，之后再调整）
        total_page = math.ceil(len(issues) / issue_per_page)
        begin = (page_no - 1) * issue_per_page
        end = page_no * issue_per_page
        issues = issues[begin:end]
        issue_list = IssueSearchSerializer(issues, many=True)
        issue_list = issue_list.data
        for issue_json in issue_list:
            issue = Issue.objects.get(id=issue_json['issue_id'])
            issue_json['status_trans_permit'] = status_trans_permit(issue, action_user)
        return Response(response_json(
            success=True,
            data={
                "issue_list": issue_list,
                "total_page": total_page
            }
        ))


# Comment
def _find_comment():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                comment = Comment.objects.get(id=args[1].data['comment_id'])
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=CommentErrorCode.COMMENT_NOT_FOUND,
                    message="can't find comment!"
                ), status=404)
            return func(*args, **kwargs, comment=comment)

        return wrapper

    return decorated


class CommentList(APIView):
    @_find_issue()
    def post(self, request, issue):
        commet_serializer = CommentSerializer(issue.comments, many=True)
        data = {"comment_list": commet_serializer.data}
        return Response(response_json(
            success=True,
            data=data
        ))


class CommentCreate(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @_find_issue()
    def post(self, request, issue, action_user):
        content = request.data['content']
        comment = Comment(content=content, issue=issue, user=action_user)
        try:
            comment.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_SAVED_FAILED,
                message="can't save comment!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="create comment success!",
            data={"comment_id": comment.id}
        ))


class CommentUpdate(APIView):
    @_find_comment()
    def post(self, request, comment):
        comment.content = request.data['content']
        try:
            comment.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_SAVED_FAILED,
                message="can't save comment!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="update comment success!"
        ))


class CommentDelete(APIView):
    @_find_comment()
    def delete(self, request, comment):
        try:
            comment.delete()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_DELETE_FAILED,
                message="can't delete comment!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="delete comment success!"
        ))
