"""
Django settings for datacollation project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv 

# Load environment variables from a .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g#ezbrxlfhl#$*g#r7wq6_k$@o!h5=yynh*dx6lmz3)pb(%hyw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'bootstrap5',
    'import_export',
    'django.contrib.humanize',  # For better UI numbers
    'data_collection',  # Custom app for data collection
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# AUTH_USER_MODEL = 'data_collection.Member'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # This is for the default user model
    'data_collection.auth_backends.MonitorBackend',  # Add your custom backend for monitor authentication
    'data_collection.auth_backends.AgentCodeBackend'
]







ROOT_URLCONF = 'datacollation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'datacollation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'datacollation_db',
        'USER': 'root',
        'PASSWORD': '1718',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



# Session settings (ensure session engine is set to use database-backed sessions)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'

  # Custom user model for admins


STATIC_URL = '/static/'

# If using additional folders for static files, include them like this:
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# In production, Django needs to know where to collect static files
# If you're using `collectstatic` in production, set this:
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# LOGIN_URL = '/member/login/'  # Redirect unauthorized users here

# LOGOUT_REDIRECT_URL = '/member/login/'  # Redirect to member login page after logout

# LOGIN_REDIRECT_URL = '/member/dashboard/'


LOGIN_URL = '/member/login/'  # Redirect to login page if the user is not authenticated
LOGIN_REDIRECT_URL = '/member/dashboard/'  # Where to go after successful login

# Email backend for sending agent codes (use a real email backend in production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Crispy Forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False  # Set this to False for debugging
CSRF_COOKIE_SECURE = False    # Make sure this is False in development
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'