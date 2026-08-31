from core.pagination import PagePagination
from core.permissions import (IsActiveUser, IsAdminOrManagerRole, IsAdminRole,
                              IsAssignmentManager, IsManagerRole)
from django.db.models import manager
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListCreateAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.orders.filters import OrderFilter
from apps.orders.models import CommentModel, OrderModel, OrderStatusModel
from apps.orders.serializers import CommentSerializer, OrderSerializer


class OrderListView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = PagePagination


class CommentsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminOrManagerRole]
    serializer_class = CommentSerializer

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return CommentModel.objects.filter(order_id=order_id).select_related('user')

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(OrderModel, id=order_id)
        user = request.user

        if order.manager is not None and order.manager != user:
            raise PermissionDenied('This order already has a manager')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, user=user)

        if order.manager is None or order.status == OrderStatusModel.NEW:
            order.manager = user
            order.status = OrderStatusModel.INWORK
            order.save(update_fields=['manager', 'status'])

        return Response({'comment': serializer.data, 'order': OrderSerializer(order).data},
                        status=status.HTTP_201_CREATED)


class ReleaseOrderManager(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsActiveUser, IsAssignmentManager]
    queryset = OrderModel.objects.all()

    def patch(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(OrderModel, id=order_id)
        user = self.request.user

        if order.manager != user:
            raise ValidationError('This order has another manager')

        order.manager = None
        order.status = OrderStatusModel.NEW
        order.save(update_fields=['manager', 'status'])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditOrdersView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsActiveUser, IsAssignmentManager]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer



