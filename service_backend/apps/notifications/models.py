from django.db import models

# Create your models here.
from service_backend.apps.users.models import User
from service_backend.apps.utils.models import MyModel


class Notification(MyModel):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    category = models.IntegerField(default=0)

    class Meta:
        db_table = 'notifications'


class NotificationReceiver(MyModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notification_receivers')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'notification_receivers'

