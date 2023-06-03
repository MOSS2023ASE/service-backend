from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.issues.models import Comment
from service_backend.apps.notifications.models import Notification, NotificationReceiver
from service_backend.apps.users.models import User
from service_backend.apps.utils.constants import UserRole, CommentErrorCode, NotificationErrorCode, NotificationCategory
from service_backend.apps.utils.views import response_json, check_role
from service_backend.apps.issues.serializer_comment import CommentSerializer
from service_backend.apps.issues.views_issue import find_issue, find_comment


class CommentList(APIView):
    @find_issue()
    def post(self, request, issue):
        commet_serializer = CommentSerializer(issue.comments, many=True)
        data = {"comment_list": commet_serializer.data}
        return Response(response_json(
            success=True,
            data=data
        ))


class CommentCreate(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    @find_issue()
    def post(self, request, issue, action_user: User):
        content = request.data['content']
        comment = Comment(content=content, issue=issue, user=action_user)
        try:
            comment.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_SAVED_FAILED,
                message="can't save comment! probably have sensitive word!"
            ), status=404)

        if action_user.user_role == UserRole.TUTOR:
            try:
                notification = Notification(
                    title="【issue回复通知】",
                    content="你的问题:\"{}\" 有辅导师的新回答～".format(issue.title),
                    category=NotificationCategory.ISSUE
                )
                notification.save()
            except Exception:
                return Response(response_json(
                    success=False,
                    code=NotificationErrorCode.NOTIFICATION_SAVE_FAILED,
                    message="can't save notification!"
                ))

            try:
                notification_receive = NotificationReceiver(notification=notification, receiver=issue.user)
                notification_receive.save()
            except Exception:
                return Response(response_json(
                    success=True,
                    code=NotificationErrorCode.NOTIFICATION_RECEIVER_SAVE_FAILED,
                    message="can't save notification-receiver"
                ))

        return Response(response_json(
            success=True,
            message="create comment success!",
            data={"comment_id": comment.id}
        ))


class CommentUpdate(APIView):
    @find_comment()
    def post(self, request, comment):
        comment.content = request.data['content']
        try:
            comment.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_SAVED_FAILED,
                message="can't save comment! probably have sensitive word!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="update comment success!"
        ))


class CommentDelete(APIView):
    @find_comment()
    def delete(self, request, comment):
        try:
            comment.delete()
        except Exception:
            return Response(response_json(
                success=False,
                code=CommentErrorCode.COMMENT_DELETE_FAILED,
                message="can't delete comment!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="delete comment success!"
        ))
