from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.auth.views import RecoverPasswordView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recovery/', RecoverPasswordView.as_view(), name='password_recovery'),
]