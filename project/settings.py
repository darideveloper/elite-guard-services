import os
import sys
import locale
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Setup .env file
load_dotenv()
ENV = os.getenv('ENV')
env_path = os.path.join(BASE_DIR, f'.env.{ENV}')
load_dotenv(env_path)
print(f'\nEnvironment: {ENV}')

# Env variables
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
LANDING_HOST = os.getenv('LANDING_HOST')
STORAGE_AWS = os.environ.get("STORAGE_AWS") == "True"
HOST = os.getenv('HOST')

print(f"DEBUG: {DEBUG}")
print(f"STORAGE_AWS: {STORAGE_AWS}")
print(f"HOST: {HOST}")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # Custom apps
    'core',
    'employees',
    'services',
    'assistance',
    
    # Template admin
    'jazzmin',
    
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Manage static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# Setup database for testing and production
IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

if IS_TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'testing.sqlite3'),
        }
    }
else:

    options = {}
    if os.environ.get("DB_ENGINE") == "django.db.backends.mysql":
        options = {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }

    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("DB_ENGINE"),
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
            'OPTIONS': options,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Setup language and time zone
LANGUAGE_CODE = 'es-mx'
locale.setlocale(locale.LC_TIME, "es_MX.UTF-8")
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin (layout template) settings
JAZZMIN_SETTINGS = {
    # Text
    "site_title": "Elite Guard Services",
    "site_header": "Admin",
    "site_brand": "EGS Dashboard",
    "welcome_sign": "Bienvenido a Elite Guard Services Dashboard",
    "copyright": "",

    # Media
    "site_logo": "core/imgs/logo.webp",
    "login_logo": "core/imgs/logo.webp",
    "login_logo_dark": "core/imgs/logo.webp",
    "site_logo_classes": "img-circle",
    "site_icon": "core/imgs/favicon.ico",
    
    # Search model in header
    "search_model": [],

    # Field name on user model that contains avatar
    # ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # {"name": "Landing", "url": LANDING_HOST},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right
    # ("app" url type is not allowed)
    "usermenu_links": [
        # {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [
        "employees.Neighborhood",
        "employees.Municipality",
        "employees.MaritalStatus",
        "employees.Status",
        "employees.Bank",
        "employees.Relationship",
        "services.Schedule",
    ],

    # List of apps (and/or models) to base side menu ordering off of
    # (does not need to contain all apps/models)
    "order_with_respect_to": [],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        # "books": [{
        #     "name": "Make Messages",
        #     "url": "make_messages",
        #     "icon": "fas fa-comments",
        #     "permissions": ["books.view_book"]
        # }]
    },

    # Custom icons for side menu apps/models
    # See https://fontawesome.com/icons?d=gallery&m=free
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "employees.Employee": "fas fa-users",
        "employees.Loan": "fas fa-money-bill",
        "employees.Ref": "fas fa-people-arrows",
        "employees.Relative": "fas fa-user-friends",
        "services.agreement": "fas fa-handshake",
        "services.service": "fas fa-briefcase",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "jazzmin/css/custom.css",
    "custom_js": "jazzmin/js/custom.js",
    # Whether to link font from fonts.googleapis.com
    # (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
}

# Setup logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": ".log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}

# Cors
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://elite-guard-services.apps.darideveloper.com",
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Storage settings
if STORAGE_AWS:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'project.storage_backends.StaticStorage'
    # s3 public media settings

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'project.storage_backends.PublicMediaStorage'

    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'project.storage_backends.PrivateMediaStorage'
    
    # Disable Django's own staticfiles handling in favour of WhiteNoise
    # for greater consistency between gunicorn and
    STATIC_ROOT = None
    MEDIA_ROOT = None
else:
    # Local development (Windows or local server)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'