from django_filters import rest_framework as filters

from apps.orders.models import (CourseFormatModel, CourseModel,
                                CourseTypeModel, OrderModel, OrderStatusModel)
from apps.orders.serializers import OrderSerializer


class OrderFilter(filters.FilterSet):
    order = filters.OrderingFilter(fields=OrderSerializer.Meta.fields)

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    surname = filters.CharFilter(field_name='surname', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')
    age = filters.NumberFilter(field_name='age', lookup_expr='exact')
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    course = filters.ChoiceFilter(choices=CourseModel.choices)
    course_format = filters.ChoiceFilter(choices = CourseFormatModel.choices)
    course_type = filters.ChoiceFilter(choices = CourseTypeModel.choices)
    status = filters.ChoiceFilter(choiсes = OrderStatusModel.choices)
    group = filters.CharFilter(field_name='group__group_name', lookup_expr='exact')

    filter_my=filters.BooleanFilter(method='filter_my_orders')

    class Meta:
        model = OrderModel
        fields = []

    def filter_my_orders(self, queryset, name, value):
        if value:
            current_manager = self.request.user
            return queryset.filter(manager=current_manager)
        return queryset