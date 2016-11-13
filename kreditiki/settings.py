"""
Django settings for kreditiki project.
"""

import logging.config
import os

# Нужно подняться на два уровня
PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps'
]

THIRDPARTY_APPS = [
    'compressor',
]

HOMEBREW_APPS = [
    'kreddb',
]

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + HOMEBREW_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # must appear before other middleware that intercepts 404 errors, such as Locale- or FlatpageFallbackMiddleware
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'kreditiki.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

WSGI_APPLICATION = 'kreditiki.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/media/'

# Измененённый дефолт!
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# это обнулятор стандартной настройки логирования, чтобы она не путалась с кастомной
LOGGING_CONFIG = None

# https://docs.djangoproject.com/en/1.10/topics/logging/#django-s-default-logging-configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(levelname)s: [%(server_time)s] %(message)s',
        },
        'default_formatter': {
            'format': '[%(levelname)5.5s] %(asctime)s [%(module)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'to_file': {  # на проде -- в файл
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('LOG_ROOT', '') + 'app.log',
            'formatter': 'default_formatter'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'to_file', 'mail_admins'],
            'level': 'INFO',
        },
        'kreddb': {
            'handlers': ['console', 'to_file', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING)

# Настройки, идущие ниже, зависят от среды

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

if SECRET_KEY is None:
    SECRET_KEY = '9pb4en8!fqh9jtk@iipkk%hc4rb__78aadii))3fj+vqi87t+_'

    DEBUG = os.environ.get('DEBUG') != 'False'

    INTERNAL_IPS = ['127.0.0.1']

    INSTALLED_APPS.append('debug_toolbar')

    # You should include the Debug Toolbar middleware as early as possible in the list. However, it must come after
    # any other middleware that encodes the response’s content, such as GZipMiddleware.
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    # Static asset configuration
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # если удалить, не будут отправляться письма через mail_managers()
    MANAGERS = [
        'Dummy manager', 'manager@example.com'
    ]
else:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = os.environ['DEBUG'] == "True"

    # безопасность
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    # настройка определения безопасного соединения, прошедшего через прокси
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

    MEDIA_ROOT = os.path.join(os.environ['WWW_ROOT'], os.environ['MEDIA_DIR'])

    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

    ADMINS = [
        (os.environ['ADMIN_NAME'], os.environ['ADMIN_EMAIL'])
    ]

    MANAGERS = ADMINS + [
        (os.environ['MANAGER_NAME'], os.environ['MANAGER_EMAIL'])
    ]

    SERVER_EMAIL = os.environ['SERVER_EMAIL']

    # TODO использовать кэширующий загрузчик шаблонов
    # https://docs.djangoproject.com/en/1.10/ref/templates/api/#template-loaders

    # TODO использовать постоянное соединение с БД
    # https://docs.djangoproject.com/en/1.10/ref/databases/#persistent-database-connections

# Allow host headers
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '3306',
    }
}
