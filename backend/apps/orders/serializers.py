from rest_framework import serializers

from apps.orders.models import CommentModel, GroupModel, OrderModel
from apps.user.models import UserModel


class OrderSerializer(serializers.ModelSerializer):
    group = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    manager = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = OrderModel
        fields = ('id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type', 'status',
                  'sum', 'alreadyPaid', 'group', 'created_at', 'manager', 'message', 'utm')
        read_only_fields = ('id', 'utm', 'created_at',)

    def update(self, instance, validated_data):
        if 'group' in validated_data:
            group_name = validated_data.pop('group')
            if group_name:
                group_obj, created = GroupModel.objects.get_or_create(group_name=group_name)
                instance.group = group_obj
            else:
                instance.group = None
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = CommentModel
        fields = ('id', 'order', 'user', 'message', 'created_at')
        read_only_fields = ('order', 'user', 'created_at', 'id')


class OrdersStatisticsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    agree = serializers.IntegerField()
    in_work = serializers.IntegerField()
    disagree = serializers.IntegerField()
    dubbing = serializers.IntegerField()
    new = serializers.IntegerField()
