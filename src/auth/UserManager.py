from typing import Optional, Dict, Any

from fastapi import Depends, Request
from fastapi.openapi.models import Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from src import config
from src.auth.database import User, get_user_db

SECRET = config.SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User has registered with name {user.name} and id {user.id}.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_update(
            self,
            user: User,
            update_dict: Dict[str, Any],
            request: Optional[Request] = None,
    ):
        print(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_login(
            self,
            user: User,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ):
        print(f"User {user.id} logged in. Hello, {user.name}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)