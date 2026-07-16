from django_filters import rest_framework as filters

from apps.orders.serializers import OrderSerializer


class OrderFilter(filters.FilterSet):
    order = filters.OrderingFilter(fields=OrderSerializer.Meta.fields)

