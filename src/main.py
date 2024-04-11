from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.auth.UserManager import get_user_manager
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.database import User
from src.catalog import router_catalog
from src.library import router_library

app = FastAPI(
    title="Приложение для книг"
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(router_catalog.router)
app.include_router(router_library.router)