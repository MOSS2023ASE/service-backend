from rest_framework import serializers
from service_backend.apps.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    tag_id = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['tag_id', 'content']

    def get_tag_id(self, obj):
        return obj.id
