from pathlib import Path

from dotenv import load_dotenv
import os

from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tv^d=u%wlo!gqe51gw#3@$xye$f((d$p(#)yosn0u!rko&*^u!'

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

    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',

    # Third party api
    'algoliasearch_django',

    # User apps
    'api',
    'products',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_URLS_REGEX = r"^/api/.*"
CORS_ALLOWED_ORIGINS = []
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8111",
        "https://127.0.0.1:8111",
    ]

ROOT_URLCONF = 'cfehome.urls'

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

WSGI_APPLICATION = 'cfehome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

auth_class = ['rest_framework.authentication.TokenAuthentication', 'rest_framework_simplejwt.authentication.JWTAuthentication',]

if DEBUG:
    auth_class = ['rest_framework.authentication.SessionAuthentication','rest_framework_simplejwt.authentication.JWTAuthentication',
                  'rest_framework.authentication.TokenAuthentication',
                   ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : 
    auth_class,
    'DEFAULT_PERMISSION_CLASSES' :
    ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_PAGINATION_CLASS': 
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10

}

ALGOLIA = {
    'APPLICATION_ID': os.environ.get('ALGOLIA_APPLICATION_ID'),
    'API_KEY': os.environ.get('ALGOLIA_API_KEY'),
    'INDEX_PREFIX': 'DRF'
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=5),
    
    "AUTH_HEADER_TYPES": ("Bearer",),
    
}