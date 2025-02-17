"""Django settings for local environment."""
# Local Vars
from .base import *  # noqa
from .base import env


# ------------------------------------------------------------------------------
# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="!!!SET DJANGO_SECRET_KEY!!!")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "192.168.17.14"]
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http:\/\/localhost:*([0-9]+)?$",
    r"^http:\/\/127.0.0.1:*([0-9]+)?$",
    r"^http:\/\/192.168.17.14:*([0-9]+)?$",
]

# ------------------------------------------------------------------------------
# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# ------------------------------------------------------------------------------
# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# #middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# #internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
# For docker development
if env("USE_DOCKER", default="N") == "Yes":
    # Standard Library
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# ------------------------------------------------------------------------------
# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest
# /installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
