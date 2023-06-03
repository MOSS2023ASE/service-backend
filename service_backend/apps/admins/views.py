from datetime import date, datetime, timedelta, time
from math import ceil

from django.db.models import Q, Count, FloatField, F, Sum, Max, Min
from django.db.models.functions import Cast
from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User
from service_backend.apps.issues.models import Issue, IssueApiCall
from service_backend.apps.utils.views import response_json, encode_password, check_role
from service_backend.apps.utils.constants import UserErrorCode, UserRole, OtherErrorCode, IssueErrorCode, \
    DEFAULT_AVATAR, StatisticsErrorCode


def _upper(x:float):
    return float(ceil(2.0 * x)) / 2


# Create your views here.
class CreateUser(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        # create user
        # print(request.data)
        student_id, name, password, role = request.data['student_id'], request.data['name'], request.data[
            'password'], request.data['role']
        try:
            if User.objects.filter(student_id=student_id).exists():
                user = User.objects.get(student_id=student_id)
                user.name, user.password_digest, user.user_role = name, encode_password(password), role
                user.mail = user.mail if user.mail else f"{student_id}@buaa.edu.cn"
                user.avatar = user.avatar if user.avatar else DEFAULT_AVATAR
            else:
                user = User(student_id=student_id, name=name, password_digest=encode_password(password), user_role=role,
                            mail=f"{student_id}@buaa.edu.cn", avatar=DEFAULT_AVATAR)
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        # success
        return Response(response_json(
            success=True,
            message="create user successfully!"
        ))


class CreateUserBatch(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        # print('user_id is:' + str(user_id))
        # preprocess list
        name_list = request.data['name_list']
        student_id_list = request.data['student_id_list']
        password_list = request.data['password_list']
        role_list = request.data['role_list']
        if len({len(name_list), len(student_id_list), len(password_list), len(role_list)}) != 1:
            return Response(response_json(
                success=False,
                code=OtherErrorCode.UNEXPECTED_JSON_FORMAT,
                message="inequal list length!"
            ))
        # iterate
        for name, student_id, password, role in zip(name_list, student_id_list, password_list, role_list):
            # create user
            try:
                if User.objects.filter(student_id=student_id).exists():
                    user = User.objects.get(student_id=student_id)
                    user.name, user.password_digest, user.user_role = name, encode_password(password), role
                    user.mail = user.mail if user.mail else f"{student_id}@buaa.edu.cn"
                    user.avatar = user.avatar if user.avatar else DEFAULT_AVATAR
                else:
                    user = User(student_id=student_id, name=name, password_digest=encode_password(password),
                                user_role=role, mail=f"{student_id}@buaa.edu.cn", avatar=DEFAULT_AVATAR)
                user.save()
            except Exception as _e:
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.USER_SAVE_FAILED,
                    message="can't save user!"
                ))
        # success
        return Response(response_json(
            success=True,
            message="batch create user successfully!"
        ))


class UserList(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        user_list = User.objects.all()
        # user_serializar = UserSerializer(user, many=True)
        return Response(response_json(
            success=True,
            message="get user list successfully!",
            data={
                'user_list': [
                    {
                        'user_id': user.id,
                        'student_id': user.student_id,
                        'name': user.name,
                        'user_role': user.user_role,
                        'frozen': user.frozen
                    }
                    for user in user_list
                ]
            }
        ))


class UpdateUserRole(APIView):
    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        # get user
        try:
            user = User.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify user role
        user.user_role = request.data['user_role']
        # save user role
        try:
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="update user role successfully!"
        ))


class FreezeUser(APIView):
    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        # get user
        try:
            user = User.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify frozen status
        user.frozen = request.data['frozen']
        # save frozen status
        try:
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="update frozen status successfully!"
        ))


class DeleteIssue(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        try:
            issue = Issue.objects.get(id=request.data['issue_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_NOT_FOUND,
                message="can't find issue!"
            ))
        try:
            issue.delete()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_DELETE_FAILED,
                message="can't delete issue!"
            ))
        return Response(response_json(
            success=True,
            message="delete issue successfully!"
        ))


class GetStatistics(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        tp, indicator = request.data['type'], request.data['indicator']
        begin_date, end_date = date.fromisoformat(str(request.data['begin_date']).strip()), date.fromisoformat(
            str(request.data['end_date']).strip())
        begin_datetime, end_datetime = datetime.combine(begin_date, time.min), datetime.combine(end_date, time.max)
        res_list = []
        if indicator == 0:
            issue_query_set = Issue.objects.all().filter(
                Q(counsel_at__gte=begin_datetime) & Q(counsel_at__lte=end_datetime))
            if tp == 0:
                cur_date = begin_date
                while cur_date <= end_date:
                    cnt = issue_query_set.filter(Q(counsel_at__gte=datetime.combine(cur_date, time.min)) & Q(
                        counsel_at__lte=datetime.combine(cur_date, time.max))).count()
                    res_list.append(cnt)
                    cur_date += timedelta(days=1)
            else:
                count_list = issue_query_set.values('counselor_id').annotate(count=Count('counselor_id'))
                res_list = [cnt['count'] for cnt in count_list]
        elif indicator == 1:
            issue_query_set = Issue.objects.all().filter(
                Q(review_at__gte=begin_datetime) & Q(review_at__lte=end_datetime))
            if tp == 0:
                cur_date = begin_date
                while cur_date <= end_date:
                    cnt = issue_query_set.filter(Q(review_at__gte=datetime.combine(cur_date, time.min)) & Q(
                        review_at__lte=datetime.combine(cur_date, time.max))).count()
                    res_list.append(cnt)
                    cur_date += timedelta(days=1)
            else:
                count_list = issue_query_set.values('reviewer_id').annotate(count=Count('reviewer_id'))
                res_list = [cnt['count'] for cnt in count_list]
        elif indicator == 2:
            api_call_query_set = IssueApiCall.objects.all().filter(
                Q(created_at__gte=begin_datetime) & Q(created_at__lte=end_datetime))
            if tp == 0:
                cur_date = begin_date
                while cur_date <= end_date:
                    cnt = api_call_query_set.filter(Q(created_at__gte=datetime.combine(cur_date, time.min)) & Q(
                        created_at__lte=datetime.combine(cur_date, time.max))).count()
                    res_list.append(cnt)
                    cur_date += timedelta(days=1)
            else:
                count_list = api_call_query_set.values('issue_id').annotate(count=Count('issue_id'))
                res_list = [cnt['count'] for cnt in count_list]
        else:
            pass
        # res_list = sorted(res_list)
        return Response(response_json(
            success=True,
            message="get statistics successfully!",
            data={
                'list': res_list
            }
        ))


class GetTutorBonus(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        bonus_per_counsel, bonus_per_review = float(request.data['bonus_per_counsel']), float(
            request.data['bonus_per_review'])
        begin_date, end_date = date.fromisoformat(str(request.data['begin_date']).strip()), date.fromisoformat(
            str(request.data['end_date']).strip())
        begin_datetime, end_datetime = datetime.combine(begin_date, time.min), datetime.combine(end_date, time.max)
        min_bonus, max_bonus = float(request.data['min_bonus']), float(request.data['max_bonus'])
        # statistic
        counsel_issue = Issue.objects.all().filter(Q(counsel_at__gte=begin_datetime) & Q(counsel_at__lte=end_datetime))
        review_issue = Issue.objects.all().filter(Q(review_at__gte=begin_datetime) & Q(review_at__lte=end_datetime))
        counsel_count = counsel_issue.values('counselor_id').annotate(int_count=Count('counselor_id'))
        review_count = review_issue.values('reviewer_id').annotate(int_count=Count('reviewer_id'))
        value_dict = dict()
        for item in counsel_count:
            if item['counselor_id'] in value_dict:
                value_dict[item['counselor_id']] += item['int_count'] * bonus_per_counsel
            else:
                value_dict[item['counselor_id']] = item['int_count'] * bonus_per_counsel
        for item in review_count:
            if item['reviewer_id'] in value_dict:
                value_dict[item['reviewer_id']] += item['int_count'] * bonus_per_review
            else:
                value_dict[item['reviewer_id']] = item['int_count'] * bonus_per_review
        max_value, min_value = max(value_dict.values()), min(value_dict.values())
        # linear_projection = max_value > max_bonus or min_value < min_bonus
        # linear_projection = linear_projection and (bonus_per_counsel >= 0.0 and bonus_per_review >= 0.0 and 0.0 <= min_bonus < max_bonus)
        linear_projection = False
        if linear_projection:
            total_bonus = [{'id': k, 'bonus': (v - min_value) * (max_bonus - min_bonus) / (max_value - min_value) + min_bonus} for k, v in value_dict.items()]
        else:
            total_bonus = [{'id': k, 'bonus': v} for k, v in value_dict.items()]
        # to list
        res_list = []
        for item in total_bonus:
            user = User.objects.get(id=item['id'])
            res_list.append(
                {
                    "id": item["id"],
                    "student_id": user.student_id,
                    "name": user.name,
                    "bonus": _upper(item["bonus"])
                }
            )
        return Response(response_json(
            success=True,
            message="get bonus list successfully!",
            data={
                'bonus_list': res_list
            }
        ))


class GetStudentBonus(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        bonus_per_issue = float(request.data['bonus_per_issue'])
        begin_date, end_date = date.fromisoformat(str(request.data['begin_date']).strip()), date.fromisoformat(
            str(request.data['end_date']).strip())
        begin_datetime, end_datetime = datetime.combine(begin_date, time.min), datetime.combine(end_date, time.max)
        min_bonus, max_bonus = float(request.data['min_bonus']), float(request.data['max_bonus'])
        # statistic
        issue_query_set = Issue.objects.all().filter(Q(created_at__gte=begin_datetime) & Q(created_at__lte=end_datetime))
        issue_count = issue_query_set.values('user_id').annotate(int_count=Count('user_id'))
        issue_count = issue_count.annotate(float_count=Cast('int_count', FloatField()))
        issue_count = issue_count.annotate(count=F('float_count') * bonus_per_issue)
        issue_count = issue_count.values('user_id', 'count')
        issue_count = issue_count.annotate(id=F('user_id'))
        total_value = issue_count.annotate(value=F('count'))
        total_value = total_value.values('id', 'value')
        max_value, min_value = total_value.aggregate(Max('value'))['value__max'], total_value.aggregate(Min('value'))['value__min']
        if min_value == max_value:
            return Response(response_json(
                success=False,
                code=StatisticsErrorCode.BONUS_ALL_THE_SAME,
                message='volunteer time bonus all the same!'
            ))
        # check whether proj
        # linear_projection = bonus_per_issue >= 0.0 and 0.0 <= min_bonus < max_bonus
        linear_projection = False
        if linear_projection:
            total_bonus = total_value.annotate(bonus=F('value') * (max_bonus - min_bonus) / (max_value - min_bonus) + min_bonus).values('id', 'bonus')
        else:
            total_bonus = total_value.annotate(bonus=F('value')).values('id', 'bonus')
        # to list
        res_list = []
        for item in total_bonus:
            user = User.objects.get(id=item['id'])
            res_list.append(
                {
                    "id": item["id"],
                    "student_id": user.student_id,
                    "name": user.name,
                    "bonus": _upper(item["bonus"])
                }
            )
        return Response(response_json(
            success=True,
            message="get bonus list successfully!",
            data={
                'bonus_list': res_list
            }
        ))
