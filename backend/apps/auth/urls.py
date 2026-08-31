from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.auth.views import ActivateManagerView, RecoverPasswordView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('activate/<str:token>/', ActivateManagerView.as_view(), name='activate_manager'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recovery/<str:token>/', RecoverPasswordView.as_view(), name='password_recovery'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
