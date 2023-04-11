from django.db import models

from service_backend.apps.utils.models import MyModel
from service_backend.apps.subjects.models import Subject


# Create your models here.
class Chapter(MyModel):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    content = models.TextField()

    class Meta:
        db_table = 'chapters'
