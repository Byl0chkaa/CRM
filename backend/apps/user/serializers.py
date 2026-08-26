from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login')
        read_only_fields = ('id', 'is_active', 'last_login')

class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login')
        read_only_fields = ('id', 'is_active', 'last_login')
    def create(self, validated_data):
        is_active = False
        user = UserModel.objects.create_user(is_active=is_active, **validated_data)
        return user
