from django.db import models

from service_backend.apps.utils.filter import Filter
from service_backend.apps.utils.models import MyModel
from service_backend.apps.users.models import User
from service_backend.apps.chapters.models import Chapter


# Create your models here.
class Issue(MyModel):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=3071)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_issues')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='issues')
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counselor_issues', null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_issues', null=True)
    counsel_at = models.DateTimeField(null=True)
    review_at = models.DateTimeField(null=True)
    status = models.IntegerField()
    anonymous = models.IntegerField()
    score = models.IntegerField(null=True)
    likes = models.IntegerField(default=0)
    follows = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # filter
        flt = Filter()
        if flt.has_sensitive_word(self.title) or flt.has_sensitive_word(self.content):
            raise Exception
        return super(Issue, self).save(*args, **kwargs)

    class Meta:
        db_table = 'issues'


class Comment(MyModel):
    content = models.CharField(max_length=3071)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def save(self, *args, **kwargs):
        # filter
        flt = Filter()
        if flt.has_sensitive_word(self.content):
            return False
        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        db_table = 'comments'


class FollowIssues(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_issues')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='follow_issues')

    class Meta:
        db_table = 'follow_issues'


class LikeIssues(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_issues')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='like_issues')

    class Meta:
        db_table = 'like_issues'


class AdoptIssues(MyModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='adopt_issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adopt_issues')
    status = models.IntegerField()

    class Meta:
        db_table = 'adopt_issues'


class ReviewIssues(MyModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='review_issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review_issues')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_review_issues')
    status = models.IntegerField(null=True)

    class Meta:
        db_table = 'review_issues'


class UserDraft(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_draft')
    title = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=3071, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='draft_chapter', null=True)
    anonymous = models.IntegerField(null=True)

    class Meta:
        db_table = 'user_drafts'


class IssueAssociations(MyModel):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='associate_issues_as_from')
    associate_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='associate_issues_as_to')

    class Meta:
        db_table = 'issue_associations'
