from io import BytesIO

from core.pagination import PagePagination
from core.permissions import (IsActiveUser, IsAdminOrManagerRole,
                              IsAssignmentManager)
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl import Workbook
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import (GenericAPIView, ListCreateAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.orders.filters import OrderFilter
from apps.orders.models import (CommentModel, GroupModel, OrderModel,
                                OrderStatusModel)
from apps.orders.serializers import (CommentSerializer, GroupSerializer,
                                     OrderSerializer)


class OrderListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = PagePagination


class CommentsView(ListCreateAPIView):
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
    permission_classes = [IsAuthenticated, IsActiveUser, IsAssignmentManager]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'


class GroupListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminOrManagerRole]
    queryset = GroupModel.objects.all()
    serializer_class = GroupSerializer


class ExcelExport(APIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminOrManagerRole]

    def get(self, request, *args, **kwargs):
        base_queryset = OrderModel.objects.select_related('manager', 'group').all()
        filtered_qs = OrderFilter(request.GET, queryset=OrderModel.objects.all()).qs
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Orders'

        headers = [
            'id', 'name', 'surname', 'email', 'phone', 'age', 'course',
            'course_format', 'course_type', 'status', 'sum', 'alreadyPaid',
            'group_name', 'created_at', 'manager_email', 'message', 'utm'
        ]
        sheet.append(headers)

        for order in filtered_qs:
            created_at = order.created_at.replace(tzinfo=None) if order.created_at else None
            sheet.append([
                order.id,
                order.name,
                order.surname,
                order.email,
                order.phone,
                order.age,
                order.course,
                order.course_format,
                order.course_type,
                order.status,
                order.sum,
                order.alreadyPaid,
                order.group.group_name if order.group else None,
                created_at,
                order.manager.email if order.manager else None,
                order.message,
                order.utm,
            ])

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'
        return response
