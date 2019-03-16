# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from urlparse import urljoin


# Celery settings

BROKER_URL = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Django settings

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
BASE_DIR = here('..', '..')

path = lambda *x: os.path.join(os.path.abspath(BASE_DIR), *x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            path('peripteras/templates/jinja2'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'peripteras.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path('peripteras/templates/django'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



STATICFILES_DIRS = (
    path('peripteras/static/peripteras'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'sorl.thumbnail',
    'rest_framework',
    'import_export',
    'corsheaders',
    'peripteras.kiosks',
    'peripteras.users',
    'peripteras.public'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'peripteras.urls'

WSGI_APPLICATION = 'peripteras.wsgi.application'

# Rest Framework settings
REST_FRAMEWORK = {
    # this removes the browsable DRF api
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

CORS_URLS_REGEX = r'^/api/v1/.*$'

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
#USE_TZ = True
TIME_ZONE = 'Europe/Athens'


# Login urls
LOGIN_URL = '/login/'

# Static files (CSS, JavaScript, Images)
MEDIA_ROOT = path('media')
MEDIA_URL = '/media/'


STATIC_ROOT = path('static')

STATIC_URL = '/static/'

COMPANIES_LOGO_DIR = 'uploads/companies'

# Set default logo for companies
DEFAULT_LOGO = 'img/default_logo.png'
DEFAULT_LOGO_URL = urljoin(MEDIA_URL, DEFAULT_LOGO)
DEFAULT_LOGO_PATH = os.path.join(MEDIA_ROOT, DEFAULT_LOGO)

KIOSK_DIMENSIONS = '100x100'
AVATAR_DIMENSIONS = '50x50'


ITEM_LOGO_DIR = 'items'

# Set configuration file for training app
CONFIG_FILE = 'config/training.cfg'
CONFIG_FILE_URL = urljoin(MEDIA_URL, CONFIG_FILE)
CONFIG_FILE_PATH = os.path.join(MEDIA_ROOT, CONFIG_FILE)

# Sorl settings
THUMBNAIL_DUMMY = True
THUMBNAIL_PREFIX = 'uploads/sorl-cache/'
LOGO_DIMENSIONS = '160x160'


# Employee Valid Session
GAME_SESSION_DAYS = 7

ALLOW_INCOMPLETE_TRAININGS = True  # ?
EMPLOYEE_MAX_AGE = 7


EXCEL_FORMATS = list((
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel'),)


CSV_FORMATS = ['text/csv', ]

THUMBNAIL_FORMAT = 'PNG'
