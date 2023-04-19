from rest_framework import serializers
from service_backend.apps.issues.models import Issue, Comment


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    chapter_id = serializers.SerializerMethodField()
    chapter_name = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()

    def get_issue_id(self, obj):
        return obj.id

    def get_user_id(self, obj):
        if obj.anonymous:
            return 0
        else:
            return obj.user.id

    def get_user_name(self, obj):
        if obj.anonymous:
            return "匿名"
        else:
            return obj.user.name

    def get_user_avatar(self, obj):
        if obj.anonymous:
            return None
        else:
            return obj.user.avatar

    def get_chapter_id(self, obj):
        return obj.chapter.id

    def get_chapter_name(self, obj):
        return obj.chapter.name

    def get_subject_id(self, obj):
        return obj.chapter.subject.id

    def get_subject_name(self, obj):
        return obj.chapter.subject.name

    def get_tag_list(self, obj):
        issue_tags = obj.issue_tags.all()
        tags_content = [issue_tag.tag.content for issue_tag in issue_tags]
        return tags_content

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'content', 'user_id', 'user_name', 'user_avatar', 'chapter_id', 'chapter_name',
                  'subject_id', 'subject_name', 'tag_list', 'status', 'anonymous', 'score', 'created_at', 'updated_at']


class IssueSearchSerializer(serializers.ModelSerializer):
    issue_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    chapter_id = serializers.SerializerMethodField()
    chapter_name = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    issue_title = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    follow_count = serializers.SerializerMethodField()

    def get_issue_id(self, obj):
        return obj.id

    def get_issue_title(self, obj):
        return obj.title

    def get_user_id(self, obj):
        if obj.anonymous == 1:
            return 0
        else:
            return obj.user.id

    def get_user_name(self, obj):
        if obj.anonymous == 1:
            return "匿名"
        else:
            return obj.user.name

    def get_user_avatar(self, obj):
        if obj.anonymous == 1:
            return None
        else:
            return obj.user.avatar

    def get_chapter_id(self, obj):
        return obj.chapter.id

    def get_chapter_name(self, obj):
        return obj.chapter.name

    def get_subject_id(self, obj):
        return obj.chapter.subject.id

    def get_subject_name(self, obj):
        return obj.chapter.subject.name

    def get_counselor_id(self, obj):
        return obj.counselor.id

    def get_reviewer_id(self, obj):
        return obj.reviewer.id

    def get_like_count(self, obj):
        return obj.likes

    def get_follow_count(self, obj):
        return obj.follows

    class Meta:
        model = Issue
        fields = ['issue_id', 'issue_title', 'content', 'user_id', 'user_name', 'user_avatar', 'chapter_id',
                  'chapter_name', 'subject_id', 'subject_name', 'status', 'anonymous', 'score',
                  'created_at', 'updated_at', 'counselor_id', 'reviewer_id', 'like_count', 'follow_count']


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_comment_id(self, obj):
        return obj.id

    def get_time(self, obj):
        return obj.updated_at

    def get_user_id(self, obj):
        if obj.issue.user_id == obj.user_id and \
                obj.issue.anonymous == 1:
            return 0
        else:
            return obj.user.id

    def get_user_role(self, obj):
        return obj.user.user_role

    def get_avatar(self, obj):
        if obj.issue.user_id == obj.user_id and \
                obj.issue.anonymous == 1:
            return None
        else:
            return obj.user.avatar

    def get_name(self, obj):
        if obj.issue.user_id == obj.user_id and \
                obj.issue.anonymous == 1:
            return "匿名"
        else:
            return obj.user.name

    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'time', 'user_id', 'user_role', 'avatar', 'name']
