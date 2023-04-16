from rest_framework import serializers

from service_backend.apps.chapters.models import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    chapter_id = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['chapter_id', 'name', 'content']

    def get_chapter_id(self, obj):
        return obj.id
