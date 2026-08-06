from rest_framework import serializers

from apps.orders.models import OrderModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ('id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type', 'status',
                  'sum', 'alreadyPaid', 'group', 'created_at', 'manager')
