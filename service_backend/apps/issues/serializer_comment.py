from rest_framework import serializers
from service_backend.apps.issues.models import Comment


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
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

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
