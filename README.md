# Приложение для чтения книг
Приложение позволяет пользователям добавлять книги из каталога в свою личную библиотеку. Книги делятся на 2 типа: бесплатные и требующие от пользователя подписки. Это описание backend части данного приложения.

## Авторизация
В приложении используется готовая библиотека FastAPIusers для реализации аутентификации. Был использован набор cookie + JWT 

' cookie_transport = CookieTransport(cookie_name="login",cookie_max_age=86400)
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400) '
