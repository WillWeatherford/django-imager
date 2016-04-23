"""
Django settings for imagersite project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'imager_images',
    'imager_profile',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imagersite.urls'

TEMPLATES = [
    {
        # 'TEMPLATE_DEBUG': DEBUG,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'imagersite', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imagersite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

user = os.environ.get('DATABASE_USER', '')
password = os.environ.get('DATABASE_PASSWORD', '')

DATABASES = {
    'default':
        dj_database_url.config()
        # {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'django-imager',
        # 'USER': user,
        # 'HOST': 'localhost',
        # 'PORT': '5432',
        # 'PASSWORD': password
        # }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'image_cache_table',
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': ('django.contrib.auth.password_validation.'
              'UserAttributeSimilarityValidator')},
    {'NAME': ('django.contrib.auth.password_validation.'
              'MinimumLengthValidator')},
    {'NAME': ('django.contrib.auth.password_validation.'
              'CommonPasswordValidator')},
    {'NAME': ('django.contrib.auth.password_validation.'
              'NumericPasswordValidator')},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/profile'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_SSL = True
