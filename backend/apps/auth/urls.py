from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth_login'),

]