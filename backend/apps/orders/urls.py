from django.urls import path

from apps.orders.views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list')
]