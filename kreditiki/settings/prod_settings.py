from kreditiki.settings.base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# TODO Сделать стэйджинг конфиг с True
DEBUG = os.environ['DEBUG'] == "True"

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

# TODO Включить, когда будет https
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# TODO поменять?
# Heroku-recommended settings
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
