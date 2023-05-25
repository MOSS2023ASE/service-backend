from django.db import models

from service_backend.apps.utils.models import MyModel


# Create your models here.
class Year(MyModel):
    content = models.CharField(max_length=255, unique=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = 'years'
