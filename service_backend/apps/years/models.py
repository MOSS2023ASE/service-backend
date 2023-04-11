from django.db import models

from service_backend.apps.utils.models import MyModel


# Create your models here.
class Year(MyModel):
    content = models.TextField(unique=True)

    class Meta:
        db_table = 'years'
