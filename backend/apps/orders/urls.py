from django.urls import path

from apps.orders.views import (CommentsView, EditOrdersView, OrderListView,
                               ReleaseOrderManager)

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/release/', ReleaseOrderManager.as_view(), name='release_order'),
    path('<int:order_id>/comments/', CommentsView.as_view(), name='comment_list'),
    path('<int:order_id>/edit/', EditOrdersView.as_view(), name='edit_orders'),
]
