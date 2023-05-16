from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.notifications.models import Notification, NotificationReceiver
from service_backend.apps.users.models import User
from service_backend.apps.utils.views import response_json, encode_password, check_role
from service_backend.apps.utils.constants import UserErrorCode, UserRole, OtherErrorCode, DEFAULT_AVATAR, NotificationErrorCode


# Create your views here.
class NotificationRead(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            notification_receiver = NotificationReceiver.objects.get(Q(receiver_id=action_user.id) & Q(notification_id=request.data['notification_id']))
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_RECEIVER_LOAD_FAILED,
                message="can't load notification-receiver!"
            ))
        try:
            notification_receiver.status = 1
            notification_receiver.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_RECEIVER_SAVE_FAILED,
                message="can't save notification-receiver!"
            ))
        return Response(response_json(
            success=True,
            message="get notification successfully!",
            data={
                "title": notification_receiver.notification.title,
                "content": notification_receiver.notification.content,
                "time": str(notification_receiver.notification.created_at),
                "category": notification_receiver.notification.category,
                "status": notification_receiver.status
            }
        ))


class NotificationClear(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            notification_list = Notification.objects.filter(notification_receivers__receiver_id=action_user.id)
            notification_list.delete()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_DELETE_FAILED,
                message="can't delete notification!"
            ))
        return Response(response_json(
            success=True,
            message="delete notification successfully!",
        ))


class NotificationList(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            page_no, notification_per_page = request.data['page_no'], request.data['notification_per_page']
            notification_list = NotificationReceiver.objects.filter(
                receiver_id=action_user.id).order_by(
                '-created_at').distinct()
            notification_list = notification_list[(page_no - 1) * notification_per_page: page_no * notification_per_page].select_related('notification')
        except Exception as e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_RECEIVER_LOAD_FAILED,
                message="can't get notification-receiver!"
            ))
        return Response(response_json(
            success=True,
            message="get notification successfully!",
            data={
                'notification_list': [
                    {
                        'id': n.notification.id,
                        'title': n.notification.title,
                        'content': n.notification.content,
                        'time': str(n.notification.created_at),
                        'category': n.notification.category,
                        'status': n.status
                    }
                    for n in notification_list
                ]
            },
        ))


class NotificationBroadcast(APIView):

    @check_role(UserRole.ADMIN_ONLY)
    def post(self, request, action_user: User = None):
        try:
            notification = Notification(
                title=request.data['title'],
                content=request.data['content'],
                category=request.data['category']
            )
            notification.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_SAVE_FAILED,
                message="can't save notification!"
            ))
        try:
            NotificationReceiver.objects.bulk_create([
                NotificationReceiver(notification_id=notification.id, receiver_id=receiver.id, status=0)
                for receiver in User.objects.all()
            ])
        except Exception as e:
            return Response(response_json(
                success=False,
                code=NotificationErrorCode.NOTIFICATION_LOAD_FAILED,
                message="can't save notification-receiver!"
            ))
        return Response(response_json(
            success=True,
            message="broadcast notification successfully!"
        ))
