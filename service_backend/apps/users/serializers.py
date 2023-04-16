from rest_framework import serializers
from service_backend.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'password_digest', 'mail', 'avatar', 'frozen', 'user_role']
