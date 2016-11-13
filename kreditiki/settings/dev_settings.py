from kreditiki.settings.base_settings import *

SECRET_KEY = '9pb4en8!fqh9jtk@iipkk%hc4rb__78aadii))3fj+vqi87t+_'

DEBUG = True

# включить это если нужно будет сделать DEBUG = False
# ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS.append('debug_toolbar')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auto_yandex_test',
        'USER': 'auto_yandex',
        'PASSWORD': 'auto_yandex',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

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
