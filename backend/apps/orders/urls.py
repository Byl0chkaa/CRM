from django.urls import path

from apps.orders.views import (AddCommentView, CommentsListView, OrderListView,
                               ReleaseOrderManager)

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/comments/', AddCommentView.as_view(), name='add_comment'),
    path('<int:order_id>/release/', ReleaseOrderManager.as_view(), name='release_order'),
    path('<int:order_id>/comments/', CommentsListView.as_view(), name='comment_list'),
]
