from kreditiki.settings.base_settings import *

INSTALLED_APPS.append('debug_toolbar')

# DEBUG_TOOLBAR_PANELS_DEFAULT = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]
#
# DEBUG_TOOLBAR_PANELS = DEBUG_TOOLBAR_PANELS_DEFAULT + [
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]

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

# TODO чё эта?
# LOGGING_CONFIG = None

STATIC_ROOT = 'static_dev'
