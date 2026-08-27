from rest_framework import serializers

from apps.orders.models import CommentModel, GroupModel, OrderModel
from apps.user.models import UserModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        group = serializers.SlugRelatedField(slug_field='group_name', queryset=GroupModel.objects.all(), required=False)
        manager = serializers.SlugRelatedField(slug_field='name', queryset=UserModel.objects.all(), required=False)
        fields = ('id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type', 'status',
                  'sum', 'alreadyPaid', 'group', 'created_at', 'manager', 'message', 'utm')
        read_only_fields = ('id','manager', 'utm', 'created_at',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        user = serializers.StringRelatedField()
        fields = ('id', 'order', 'user', 'message', 'created_at')
        read_only_fields = ('order', 'user', 'created_at', 'id')

class OrdersStatisticsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    agree = serializers.IntegerField()
    in_work = serializers.IntegerField()
    disagree = serializers.IntegerField()
    dubbing = serializers.IntegerField()
    new = serializers.IntegerField()

