"""
Django settings for nosta project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fg+@^71lbdwcl@5(6wil#b792q83f)i%s)848497h7x!i^xce&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'fontawesomefree',
    'corsheaders',
    'appadmin',
    'appauth',
    'db',
    'market',
    'regi',
    'shop',
    'ticket',
    'top',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:5000',
    'https://nosta.prasic-plus.com'
]

ROOT_URLCONF = 'nosta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

WSGI_APPLICATION = 'nosta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'development_db.sqlite3',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

EMAIL_HOST = 'smtp.email.ap-sydney-1.oci.oraclecloud.com'
EMAIL_HOST_USER = 'ocid1.user.oc1..aaaaaaaapiyved63mmxxg7rcbla2xuzlsf7qijnjebz6kneuryuvooptgjua@ocid1.tenancy.oc1..aaaaaaaaaxnytjnf26pq2sblch27njgo3h26wur6t7bzcvm2nhpnapxajcba.yr.com'
EMAIL_HOST_PASSWORD = '(pW;gm>+!vALa4KhQcb5'
EMAIL_PORT = '587' #メールサーバーで指定されているポート
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@nosta.prasic-plus.com'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# 画像を保存する先の指定
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 画像をdjango側で読み込むための設定
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'top:home'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '224291454090-fu17l5f6bu2me6721o7eroodsmrqq76r.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
LOGOUT_REDIRECT_URL = "login"