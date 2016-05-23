"""
Django settings for blindshop project.

Generated by 'django-admin startproject' using Django 1.8.11. 

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u6f-($m)%tg0=@2c*@oo(=5c3eew53(3s)fpk_j+m(jl5e%fy4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = (
    ("Brian", "citylock77@gmail.com"),
    )

ALLOWED_HOSTS = ['*']

# Email HOST setting
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sydnobleblinds@gmail.com' 
EMAIL_HOST_PASSWORD = 'sydnoble' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True

''' 
If using gmail, you will need to
unlock Captcha to enable Django 
to  send for you:
https://accounts.google.com/displayunlockcaptcha
'''


# Application definition

INSTALLED_APPS = (
    # django app 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps 
    'crispy_forms', 
    'registration', 
    # my apps 
    'carts',
    'newsletter', 
    'orders',
    'products'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'blindshop.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'blindshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
print DEBUG

if not DEBUG: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'noble',
            'USER': 'noble_admin',
            'PASSWORD': 'syd1q2w',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/blindshop/staticfiles'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# uploaded files by users
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/html/blindshop/mediafiles' 

#Crispy FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#DJANGO REGISTRATION REDUX
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'