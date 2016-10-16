from kreditiki.settings.base_settings import *

INTERNAL_IPS = ['127.0.0.1']

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
