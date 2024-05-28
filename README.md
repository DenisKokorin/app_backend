# Приложение для чтения книг
Приложение позволяет пользователям добавлять книги из каталога в свою личную библиотеку. Книги делятся на 2 типа: бесплатные и требующие от пользователя подписки. Это описание backend части данного приложения.

## База данных
В проекте используется база данных postresql. Таблицы содержат информацию о пользователях, книгах, отзывах, ролях и сами книги.

```python
role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String, nullable=False),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role_id", Integer, ForeignKey("role.id")),
    Column("library", ARRAY(Integer)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

book = Table(
    "book",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("year", Integer),
    Column("description", Text),
    Column("genre", String),
    Column("number_of_pages", Integer),
    Column("access", Integer, ForeignKey("role.id")),
    Column("publishing_house", String),
)

review = Table(
    "reviews",
    metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("rating", Integer),
    Column("text", String)
)


data_book = Table(
    "data_book",
    metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("data", String)
)

```

## Авторизация
В приложении используется готовая библиотека FastAPIusers для реализации аутентификации. Был использован набор cookie + JWT 

``` python
cookie_transport = CookieTransport(cookie_name="login",cookie_max_age=86400)
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400)
```

## Роуты
* "/catalog":
* "/" - главня страница, где показываются рекомендуемые книги. Пользователь, имеющий достаточные права, может добавлять или изменять книги
* "/{book_id}" - просмотр конкретной книги по id. Можно добавлять в библиотеку или удалять из неё
* "/{book_id}/reviews" - просмотр отзывов книги. Можно добавлять, изменять или удалять отзыв. У пользователя может быть доступен только 1 отзыв у книги

* "/library":
* "/{user_id}" - просмотр библиотеки конкретного пользователя
* "/read/{book_id}" - открытие книги, доступная в библиотеке пользователя 


