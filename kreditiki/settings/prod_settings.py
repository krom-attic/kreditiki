from kreditiki.settings.base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# TODO Сделать стэйджинг конфиг с True
DEBUG = os.environ['DEBUG'] == "True"

# Allow host headers
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

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
