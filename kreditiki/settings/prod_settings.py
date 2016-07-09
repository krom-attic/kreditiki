from kreditiki.settings.base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# TODO Сделать стэйджинг конфиг с такими параметрами, а тут сделать жёстко False
DEBUG = True

# Allow host headers
ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]

# INSTALLED_APPS are listed in the base settings

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

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

# Static asset configuration
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


# TODO Включить, когда будет https
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# TODO поменять?
# Heroku-recommended settings
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# TODO See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/ for production optimisations
