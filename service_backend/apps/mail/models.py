from django.db import models

from service_backend.apps.users.models import User
from service_backend.apps.utils.models import MyModel


# Create your models here.

class MailConfirm(MyModel):
    email = models.CharField(max_length=255)
    vcode = models.CharField(max_length=255)

    class Meta:
        db_table = 'mail_confirms'
