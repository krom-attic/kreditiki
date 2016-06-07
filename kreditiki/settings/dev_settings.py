from kreditiki.settings.base_settings import *

INSTALLED_APPS.append('debug_toolbar')

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'auto_yandex',
    #     'USER': 'postgres',
    #     'PASSWORD': 'postgres',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auto_yandex',
        'USER': 'auto_yandex',
        'PASSWORD': 'auto_yandex',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# TODO чё эта?
# LOGGING_CONFIG = None

STATIC_ROOT = 'static_dev'
