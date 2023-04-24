from django.db import models

from service_backend.apps.utils.models import MyModel
from service_backend.apps.years.models import Year
from service_backend.apps.users.models import User


# Create your models here.
class Subject(MyModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='subjects')
    content = models.CharField(max_length=3071)

    class Meta:
        db_table = 'subjects'


class UserSubject(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_subjects')

    class Meta:
        db_table = 'user_subjects'
