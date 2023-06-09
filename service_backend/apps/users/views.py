from django.db.models import Count
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.users.models import User, BlackList
from service_backend.apps.subjects.models import UserSubject, Subject
from service_backend.apps.issues.models import ReviewIssues, FollowIssues, LikeIssues, AdoptIssues, Issue
from service_backend.apps.utils.views import response_json, encode_password, generate_jwt, check_role
from service_backend.apps.utils.constants import UserErrorCode, SubjectErrorCode, IssueErrorCode, UserRole, IssueStatus, \
    OtherErrorCode

top_k_max = 10


# Create your views here.
def _issue_list_to_json(issue_list):
    return \
        {'issue_list': [
            {
                'issue_id': issue.id,
                'create_at': str(issue.created_at),
                'update_at': str(issue.updated_at),
                'title': issue.title,
                'content': issue.content,
                'user_id': issue.user_id,
                'chapter_id': issue.chapter_id,
                'chapter_name': issue.chapter.name,
                'subject_id': issue.chapter.subject_id,
                'subject_name': issue.chapter.subject.name,
                'status': issue.status,
                'anonymous': issue.anonymous,
                'score': issue.score,
                'user_name': issue.user.name
            }
            for issue in issue_list
        ]
        }


def cal_popular():
    pass


class UserLogin(APIView):
    def post(self, request):
        # print(request.data)
        # get user
        try:
            # if no invalid id, User.objects.get will raise exception
            user = User.objects.get(student_id=request.data['student_id'])
        except Exception as _e:
            return Response(
                response_json(
                    success=False,
                    code=UserErrorCode.USER_NOT_FOUND,
                    message='user not found!'
                )
            )
        # check password
        try:
            password_digest = encode_password(request.data['password'])
            if password_digest != user.password_digest:
                raise Exception()
            jwt_token = generate_jwt(user.id)
            # print(jwt_token)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        # login success
        return Response(
            response_json(
                success=True,
                message='login success!',
                data={
                    'jwt': jwt_token,
                    'role': user.user_role
                }
            )
        )


class UserLogout(APIView):
    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        expired_token = BlackList(token=request.data['jwt'])
        expired_token.save()
        return Response(response_json(
            success=True,
            message="user logout successfully!"
        ))


class PasswordModify(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        if action_user.password_digest != encode_password(request.data['password_old']):
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        try:
            action_user.password_digest = encode_password(request.data['password_new'])
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify password successfully!"
        ))


class GetUserInfo(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        return Response(response_json(
            success=True,
            message='get user information successfully!',
            data={
                'user_id': action_user.id,
                'student_id': action_user.student_id,
                'name': action_user.name,
                'mail': action_user.mail,
                'avatar': action_user.avatar,
                'role': action_user.user_role
            }
        ))


class ModifyUserInfo(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            action_user.avatar = request.data['avatar']
            action_user.mail = request.data['mail']
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify user information successfully!"
        ))


class GetUserSubject(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        # check tutor id
        try:
            tutor_id = request.data['tutor_id']
            tutor = User.objects.get(id=tutor_id)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message='user not found!',
            ))
        # get subject list
        try:
            subject_id_set = {user_subject.subject.id for user_subject in UserSubject.objects.filter(user_id=tutor_id)}
            subject_list = [Subject.objects.get(id=subject_id) for subject_id in subject_id_set]
        except:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message='subject not found!',
            ))
        # return
        return Response((response_json(
            success=True,
            message="get tutor's subjects successfully!",
            data={
                'subject_list': [
                    {
                        'subject_id': subject.id,
                        'subject_name': subject.name
                    }
                    for subject in subject_list
                ]
            }
        )))


class ModifyUserSubject(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        tutor_student_id, subject_id_list = request.data['tutor_id'], request.data['subject_id_list']
        # print(tutor_student_id)
        try:
            user = User.objects.get(student_id=tutor_student_id)
            tutor_id = user.id
            UserSubject.objects.filter(user_id=tutor_id).delete()
            user_subject_list = [UserSubject(user_id=tutor_id, subject_id=subject_id)
                                 for subject_id in subject_id_list]
            UserSubject.objects.bulk_create(user_subject_list)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_LIST_UPDATE_FAILED,
                message='subject list update failed'
            ))
        return Response(response_json(
            success=True,
            message='subject list update successfully!'
        ))


class CheckUserSubject(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        tutor_id, subject_id = request.data['tutor_id'], request.data['subject_id']
        result = 1 if UserSubject.objects.filter(user_id=tutor_id, subject_id=subject_id).exists() else 0
        return Response(response_json(
            success=True,
            message='user is a tutor of this subject!' if result else 'user is not a tutor of this subject!',
            data={
                'result': result
            }
        ))


class GetReviewIssue(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        page_no, issue_per_page = request.data['page_no'], request.data['issue_per_page']
        try:
            issue_list = Issue.objects.filter(review_issues__user_id=action_user.id).order_by(
                '-updated_at').distinct()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.REVIEW_ISSUE_QUERY_FAILED,
                message="query review issue failed!"
            ))
        issue_list = issue_list[(page_no - 1) * issue_per_page: page_no * issue_per_page].select_related(
            'chapter').select_related('chapter__subject')
        return Response(response_json(
            success=True,
            message="query review issue successfully!",
            data=_issue_list_to_json(issue_list)
        ))


class GetAdoptIssue(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        page_no, issue_per_page = request.data['page_no'], request.data['issue_per_page']
        try:
            issue_list = Issue.objects.filter(adopt_issues__user_id=action_user.id).order_by(
                '-updated_at').distinct()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ADOPT_ISSUE_QUERY_FAILED,
                message="query adopt issue failed!"
            ))
        issue_list = issue_list[(page_no - 1) * issue_per_page: page_no * issue_per_page]
        return Response(response_json(
            success=True,
            message="query adopt issue successfully!",
            data=_issue_list_to_json(issue_list)
        ))


class GetFollowIssue(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        page_no, issue_per_page = request.data['page_no'], request.data['issue_per_page']
        try:
            issue_list = Issue.objects.filter(follow_issues__user_id=action_user.id).order_by(
                '-updated_at').distinct()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.FOLLOW_ISSUE_QUERY_FAILED,
                message="query follow issue failed!"
            ))
        issue_list = issue_list[(page_no - 1) * issue_per_page: page_no * issue_per_page]
        return Response(response_json(
            success=True,
            message="query follow issue successfully!",
            data=_issue_list_to_json(issue_list)
        ))


class GetAskIssue(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        page_no, issue_per_page = request.data['page_no'], request.data['issue_per_page']
        try:
            issue_list = Issue.objects.filter(user_id=action_user.id).order_by(
                '-updated_at').distinct()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ASK_ISSUE_QUERY_FAILED,
                message="query ask issue failed!"
            ))
        issue_list = issue_list[(page_no - 1) * issue_per_page: page_no * issue_per_page]
        return Response(response_json(
            success=True,
            message="query ask issue successfully!",
            data=_issue_list_to_json(issue_list)
        ))


class GetPopularIssue(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        # 选择前k个有效的issue, 按照likes数量降序排列
        # 可选项last_week:展示最近一周(按照review_at的时间判断)的popular issue
        # TODO: 可以把week扩展到month以及all time
        last_week = False
        top_k = request.data['top_k']
        if top_k > top_k_max:
            return Response(response_json(
                success=False,
                code=OtherErrorCode.TOO_LARGE_TOPK,
                message='expect top_k no more than 10!'
            ))
        issue_list = Issue.objects.all().filter(status=IssueStatus.VALID_ISSUE).order_by('-likes')
        if last_week:
            issue_list = [issue for issue in issue_list if
                          (datetime.now() - datetime.fromisoformat(issue.review_at)).seconds < 7 * 24 * 3600]
        issue_list = issue_list[:top_k]
        return Response(response_json(
            success=True,
            data={
                "issue_list": [
                    {
                        'issue_id': issue.id,
                        'create_at': str(issue.created_at),
                        'update_at': str(issue.updated_at),
                        'title': issue.title,
                        'content': issue.content,
                        'user_id': issue.user_id,
                        'user_name': issue.user.name,
                        'user_avatar': issue.user.avatar,
                        'counselor_id': issue.counselor_id,
                        'counsel_at': str(issue.counsel_at),
                        'reviewer_id': issue.reviewer_id,
                        'reviewer_at': issue.review_at,
                        'chapter_id': issue.chapter_id,
                        'chapter_name': issue.chapter.name,
                        'subject_id': issue.chapter.subject_id,
                        'subject_name': issue.chapter.subject.name,
                        'status': issue.status,
                        'anonymous': issue.anonymous,
                        'score': issue.score,
                        'like_count': issue.likes,
                        'follow_count': issue.follows
                    } for issue in issue_list]
            }
        ))


class GetActiveUser(APIView):
    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            top_k = request.data['top_k']
            if top_k > top_k_max:
                return Response(response_json(
                    success=False,
                    code=OtherErrorCode.TOO_LARGE_TOPK,
                    message='expect top_k no more than 10!'
                ))
            user_list = User.objects.all().annotate(total_issue=Count('user_issues')).order_by('-total_issue')
            user_list = user_list[:top_k]
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_LOAD_FAILED,
                message="can't get user list!"
            ))
        return Response(response_json(
            success=True,
            message="get active user successfully!",
            data={
                "user_list": [{
                    "user_id": user.id,
                    "student_id": user.student_id,
                    "name": user.name,
                    "user_role": user.user_role,
                    "frozen": user.frozen,
                    "avatar": user.avatar
                } for user in user_list]
            }
        ))
