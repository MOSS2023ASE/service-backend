from rest_framework import serializers
from service_backend.apps.years.models import Year


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id', 'content']
