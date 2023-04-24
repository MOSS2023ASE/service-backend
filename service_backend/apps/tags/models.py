from django.db import models

from service_backend.apps.utils.models import MyModel
from service_backend.apps.issues.models import Issue

# Create your models here.
class Tag(MyModel):
    content = models.CharField(max_length=255)

    class Meta:
        db_table = 'tags'


class IssueTag(MyModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='issue_tags')

    class Meta:
        db_table = 'issue_tags'
