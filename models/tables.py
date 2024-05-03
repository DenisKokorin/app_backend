from sqlalchemy import MetaData, String, Integer, ForeignKey, Table, Column, Text, ARRAY, Float, Boolean, JSON, LargeBinary

metadata = MetaData()

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
    Column("data", String)
)

review = Table(
    "reviews",
    metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("rating", Integer),
    Column("text", String)
)
