"""
Django settings for mysite project.
"""
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qsl
#import dj_database_url
#from dotenv import load_dotenv
 
#load_dotenv()
 

# -----------------------------------------------------------------------------------
# BASE SETTINGS
# -----------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ymlh*=xpx@+jf^l49kc+esn*9e+ai96gg6+9!@x#b+0klz=w6@'

DEBUG = os.environ.get('DEBUG', '1') == '1'

ALLOWED_HOSTS = ['*']


# -----------------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
]


# -----------------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------------------------------------------------------------
# URL / WSGI
# -----------------------------------------------------------------------------------

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# -----------------------------------------------------------------------------------
# DATABASE (Correct Neon PostgreSQL config)
# -----------------------------------------------------------------------------------



def inferDatabaseConfiguration():
    if os.getenv("DATABASE_URL"):
        tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
        print("neon db")
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    else:
        print("sqlite db")
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
 
 
DATABASES = {
    "default": inferDatabaseConfiguration()
}


# -----------------------------------------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------------
# STATIC FILES (required for Azure)
# -----------------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# -----------------------------------------------------------------------------------
# DEFAULT FIELD
# -----------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
