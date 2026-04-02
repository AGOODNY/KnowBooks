"""
Django settings for KnowBooks_backend project.
"""

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# 基础配置
# ========================

SECRET_KEY = 'django-insecure-y%)d#y#x%0g@kuxfm9dzvz#n@7h#0a&$er8t=n)&&b9^)8=6(_'
DEBUG = True
ALLOWED_HOSTS = []

# ========================
# 应用注册
# ========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方
    'rest_framework',
    'corsheaders',

    # apps
    'apps.users',
    'apps.interactions',
    'apps.recommendations',
]

# ========================
# 中间件（增加跨域）
# ========================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须放前面
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================
# 跨域配置（前后端分离必须）
# ========================

CORS_ALLOW_ALL_ORIGINS = True

# ========================
# URL / 模板
# ========================

ROOT_URLCONF = 'KnowBooks_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'KnowBooks_backend.wsgi.application'

# ========================
# 数据库
# ========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================
# 密码校验
# ========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# 国际化
# ========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# ========================
# 静态文件
# ========================

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================
# DRF 配置（关键）
# ========================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# ========================
# JWT 配置
# ========================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ========================
# 自定义用户模型（后面会用到）
# ========================
AUTH_USER_MODEL = 'users.User'