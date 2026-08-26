from typing import Type

from apps.user.serializers import UserModel
from core.enums.action_token_enum import ActionTokenEnum
from core.exceptions.jwt_exception import JWTException
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import BlacklistMixin, Token


class ActionToken(BlacklistMixin, Token):
    pass

ActionTokenClassType = Type[ActionToken]

class ActivateToken(ActionToken):
    token_type = ActionTokenEnum.ACTIVATE.token_type
    lifetime = ActionTokenEnum.ACTIVATE.lifetime

class RecoveryToken(ActionToken):
    token_type = ActionTokenEnum.RECOVERY.token_type
    lifetime = ActionTokenEnum.RECOVERY.lifetime

class JWTService:
    @staticmethod
    def create_token(user, token_class: ActionTokenClassType):
        return token_class.for_user(user)

    @staticmethod
    def verify_token(token, token_class: ActionTokenClassType):
        try:
            token_res = token_class(token)
            token_res.check_blacklist()
        except TokenError:
            raise JWTException

        user_id = token_res.payload['user_id']
        return get_object_or_404(UserModel, pk=user_id)

