"""
Django settings for bestbuyproject project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import dj_database_url
from pathlib import Path
import os
from decouple import config



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

#SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'f^=5pd1lso=1zxm*da!r$=@%o937%zv+4n7pvtgkoiuk3tkps('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app','.now.sh']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'adminpanel',
    'category',
    'store',
    'cart',
    'django_extensions',
    'crispy_forms',
    'mathfilters',
    'orders',
    'wishlist',
   
  

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     

]

ROOT_URLCONF = 'bestbuyproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_list.menu_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'bestbuyproject.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

""""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME'  : config('NAME'),
         'USER'  : config('USER'),
         'PASSWORD' : config('PASSWORD'),
         'HOST' : 'localhost',
         'PORT' : '5432',

    }
}

DATABASES = {
     'default': dj_database_url.config(
         default=config('DATABASE_URL')
     )
 }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}"""

DATABASES = {
     'default': dj_database_url.config(
         default=config('DATABASE_URL')
     )
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

"""STATIC_URL = '/static/'
STATICFILES_DIRS = [ 
    os.path.join('static')
]"""

"""STATICFILES_DIRS = [
    BASE_DIR / "static",]"""
#STATIC_ROOT  = os.path.join(BASE_DIR, 'bestbuyproject/staticfiles')
# settings.py
#STATIC_DIR=os.path.join(BASE_DIR,'static')
#print(STATIC_DIR)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
#media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



"""RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')
ACCOUNT_SECURITY_API_KEY = config('ACCOUNT_SECURITY_API_KEY')"""






#twilio
"""
ACCOUNT_SID = config('ACCOUNT_SID')
AUTH_TOKEN = config('AUTH_TOKEN')
SERVICES = config('SERVICES')"""
AUTH_USER_MODEL = 'accounts.Account'