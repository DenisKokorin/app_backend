from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.UserManager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate, UserUpdate

app = FastAPI(
    title="Приложение для книг"
)

@app.get("/")
def main_page():
    return "Главная страница"


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/log",
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