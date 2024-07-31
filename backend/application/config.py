from celery.schedules import crontab

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

    LIBRARIAN = {
        "email": "wiz@gmail.com",
        "password": "wiz",
        "name": "Wiz",
    }

    REDIS_URL = 'redis://127.0.0.1:6379'

    CACHE_TYPE = "RedisCache"

    CACHE_REDIS_URL = 'redis://127.0.0.1:6379'

    CACHE_DEFAULT_TIMEOUT = 300

    CELERY = {
        "broker_url": "redis://127.0.0.1:6379/0",
        "result_backend": "redis://127.0.0.1:6379/1",
        "task_ignore_result": True,
        "beat_schedule": {
            "send-daily-reminders": {
                "task": "application.tasks.send_daily_emails",
                "schedule": crontab(hour=21, minute=42)
            },
            "generate_activity_report": {
                "task": "application.tasks.generate_activity_report",
                "schedule": crontab(hour=21, minute=42)
            }
        },
        "beat_max_loop_interval": 5,
        "timezone": "Asia/Kolkata"
    }