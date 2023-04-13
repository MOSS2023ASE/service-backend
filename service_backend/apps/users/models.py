from django.db import models

from service_backend.apps.utils.models import MyModel


# Create your models here.
class User(MyModel):
    student_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    password_digest = models.CharField(max_length=255)
    mail = models.EmailField()
    avatar = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'


class Privilege(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='privileges')
    statistics = models.IntegerField(default=0)
    delete = models.IntegerField(default=0)
    report = models.IntegerField(default=0)
    frozen = models.IntegerField(default=0)
    user_role = models.IntegerField(default=0)

    class Meta:
        db_table = 'privileges'
