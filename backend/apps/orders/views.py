from core.pagination import PagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.orders.filters import OrderFilter
from apps.orders.models import OrderModel
from apps.orders.serializers import OrderSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter = OrderFilter
    pagination_class = PagePagination