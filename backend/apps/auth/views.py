from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

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


class LogoutView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
