class Config(object):
    SECRET_KEY = "MySecretKey"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_ECHO = False

    JWT_SECRET_KEY = "55636ca23ddfec580723bcb4"
    JWT_TOKEN_LOCATION = ["cookies"]

    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_IN_COOKIES = False
    JWT_CSRF_METHODS = []

    JWT_ACCESS_TOKEN_EXPIRES = 1800

    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = None

    LIBRARIAN_EMAILS =[
        "new@gmail.com",
    ]