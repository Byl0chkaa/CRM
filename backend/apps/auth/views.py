from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.auth.serializers import PasswordSerializer
from apps.user.serializers import UserSerializer


class ActivateManagerView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        data = self.request.data
        token = kwargs["token"]
        serializer = PasswordSerializer(data=data)
        user = JWTService.verify_token(token, ActivateToken)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data['password'])
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecoverPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        token = kwargs["token"]
        serializer = PasswordSerializer(data=data)
        user = JWTService.verify_token(token, RecoveryToken)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
