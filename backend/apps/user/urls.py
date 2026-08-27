from django.urls import path

from apps.user.views import (BanUnbanUserView, CreateManagerView,
                             GenerateRecoveryLinkView, ManagerListView)

urlpatterns = [
    path ('', ManagerListView.as_view(), name='admin_panel'),
    path ('create/', CreateManagerView.as_view(), name='create_manager'),
    path('<int:pk>/recovery/', GenerateRecoveryLinkView.as_view(), name='recover_password'),
    path('<int:pk>/status/', BanUnbanUserView.as_view(), name='change_status'),

]