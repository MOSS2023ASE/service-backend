from django.db import models

from service_backend.apps.utils.models import MyModel
from service_backend.apps.years.models import Year


# Create your models here.
class Subject(MyModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='subjects')
    password_digest = models.CharField(max_length=255)
    mail = models.EmailField()
    avatar = models.CharField(max_length=255)

    class Meta:
        db_table = "subjects"
