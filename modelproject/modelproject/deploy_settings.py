"""배포 환경"""

import pymysql

from .settings_base import *
from decouple import config

pymysql.install_as_MySQLdb()

# 기본 설정은 settings_base.py 를 따르되,
# 여기서는 데이터베이스와 보안 옵션만 약간 다르게 가져갑니다.

DEBUG = False

# 배포 서버의 IP 주소 및 도메인 (원한다면 자유롭게 수정/삭제 가능)
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INTERNAL_IPS = [
    "127.0.0.1",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF 신뢰 도메인(https 필수) – 필요 없으면 빈 리스트로 두어도 됩니다.
CSRF_TRUSTED_ORIGINS: list[str] = []

# CORS – 로컬/프론트 주소만 남겨두었습니다.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# MySQL 데이터베이스 설정 (배포 환경에서만 사용, 로컬은 local_settings.py 의 SQLite 사용)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME", default="couponbook"),  # DB(스키마) 이름
        "USER": config("DB_USER", default="root"),        # 유저 이름
        "PASSWORD": config("DB_PASSWORD", default=""),    # DB 비밀번호
        "HOST": config("DB_HOST", default="127.0.0.1"),   # DB 엔드포인트
        "PORT": 3306,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
            "use_unicode": True,
        },
    }
}

