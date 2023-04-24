from rest_framework import serializers
from service_backend.apps.years.models import Year


class YearSerializer(serializers.ModelSerializer):
    year_id = serializers.SerializerMethodField()

    class Meta:
        model = Year
        fields = ['year_id', 'content']

    def get_year_id(self, obj):
        return obj.id
