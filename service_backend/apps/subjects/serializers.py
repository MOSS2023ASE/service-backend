from rest_framework import serializers

from service_backend.apps.subjects.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    subject_id = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'content']

    def get_subject_id(self, obj):
        return obj.id
