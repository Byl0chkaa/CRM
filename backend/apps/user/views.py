from core.pagination import PagePagination
from core.permissions import IsActiveUser, IsAdminRole
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken
from django.db.models import Count
from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.user.models import UserRole
from apps.user.serializers import (ManagerCreateSerializer, UserModel,
                                   UserSerializer)


class ManagerListView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return UserModel.objects.annotate(total_orders=Count('orders'))
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole, IsActiveUser]
    pagination_class = PagePagination


class CreateManagerView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = ManagerCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole, IsActiveUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(role=UserRole.MANAGER)
        token = JWTService.create_token(instance, ActivateToken)
        activation_link = f'api/auth/activate/{token}'
        return Response({'activation_link': activation_link, 'user': serializer.data},
                        status=status.HTTP_201_CREATED)


class GenerateRecoveryLinkView(GenericAPIView):
    queryset = UserModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole, IsActiveUser]

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(UserModel, id=pk)
        if user.is_active:
            token = JWTService.create_token(user, RecoveryToken)
            recovery_link = f'api/auth/recovery/{token}'
            return Response({'recovery_link': recovery_link}, status=status.HTTP_200_OK)
        return Response({'error': 'User account is disabled'}, status=status.HTTP_400_BAD_REQUEST)

class BanUnbanUserView(GenericAPIView):
    queryset = UserModel.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole, IsActiveUser]

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(UserModel, id=pk)
        data = request.data
        is_active = data.get('is_active')

        if is_active is None:
            return Response({'error': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)

        if user.role != UserRole.MANAGER:
            return Response({'error': 'Only manager accounts can be banned or unbanned'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.is_active == is_active:
            state = 'active' if is_active else 'banned'
            return Response({'error': f'User is already {state}'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = is_active
        user.save()
        return Response({'user': UserSerializer(user).data}, status=status.HTTP_200_OK)


