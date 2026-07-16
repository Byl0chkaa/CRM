from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login')
        read_only_fields = ('id', 'is_active', 'last_login')