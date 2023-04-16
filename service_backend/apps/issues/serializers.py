from rest_framework import serializers
from service_backend.apps.issues.models import Issue

# TODO
class IssueSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()
    chapter_id = serializers.SerializerMethodField()
    chapter_name = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user.id

    def get_user_name(self, obj):
        return obj.user.name

    def get_user_avatar(self, obj):
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
        return obj.issue_tags.tag

    class Meta:
        model = Issue
        fields = ['year_id', 'title', 'content', 'user_id', 'user_name', 'user_avatar', 'chapter_id', 'chapter_name',
                  'subject_id', 'subject_name', 'tag_list', 'status', 'anonymous', 'created_at', 'updated_at']
