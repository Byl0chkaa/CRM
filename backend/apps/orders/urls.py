from django.urls import path

from apps.orders.views import OrderList

urlpatterns = [
    path('', OrderList.as_view(), name='order_list')
]