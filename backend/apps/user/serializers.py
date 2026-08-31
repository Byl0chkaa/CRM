from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    read_only_fields = ('id', 'is_active', 'last_login')
    total = serializers.IntegerField(source='total_orders', read_only=True)
    in_work = serializers.IntegerField(read_only=True)
    agree = serializers.IntegerField(read_only=True)
    disagree = serializers.IntegerField(read_only=True)
    dubbing = serializers.IntegerField(read_only=True)
    new = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login', 'total', 'in_work', 'agree', 'disagree',
                  'dubbing', 'new')
        read_only_fields = ('id', 'is_active', 'last_login', 'total', 'in_work', 'agree', 'disagree', 'dubbing', 'new')
        def get_total(self, obj):
            return getattr(obj, 'total', obj.orders.count())


class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login')
        read_only_fields = ('id', 'is_active', 'last_login')

    def create(self, validated_data):
        is_active = False
        user = UserModel.objects.create_user(is_active=is_active, **validated_data)
        return user
