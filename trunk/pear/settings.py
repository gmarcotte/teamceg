"""Global settings that apply to all runtime environments.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


# Project Ownership / Management
ADMINS = (
    ('Christina Ilvento', 'cilvento@princeton.edu'),
    ('Ellen Kim', 'ellenkim@princeton.edu'),
    ('Garrett Marcotte', 'marcotte@princeton.edu'),
)
MANAGERS = ADMINS

# Localization
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
DEBUG = True

# Branding
HTML_TITLE_BASE = 'Pairgramming'

# Django Setup
SECRET_KEY = "-y9__BvT\u-ioaA_dy_-m8v;_7Uf*_p4-t7-zH4*Z&t4V_Q}85*"
ROOT_URLCONF = 'pear.urls'
APPEND_SLASH = True

AUTHENTICATION_BACKENDS = (
    'pear.accounts.backends.EmailBackend',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'pear.core.context_processors.settings_vars',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pear.accounts',
    'pear.projects',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

# Princeton LDAP Configuration
USE_LDAP = False

# Get the environment-specific settings
from settings_local import *