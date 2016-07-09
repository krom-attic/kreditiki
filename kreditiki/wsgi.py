"""
WSGI config for kreditiki project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Дефолтный вариант
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kreditiki.settings")

# Этот вариант имеет смысл, если деплоить стэйджинг на хероку
# if 'DYNO' in os.environ:
#     from dj_static import Cling
#     application = Cling(get_wsgi_application())
# else:
application = get_wsgi_application()
