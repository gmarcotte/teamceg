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
LOGIN_URL = "/accounts/login/"
AUTH_PROFILE_MODULE = 'pear.accounts.models.PearUser'

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
    'django.contrib.sessions', #this might be killing the other session code?
    'django.contrib.sites',
    'pear.accounts',
    'pear.projects',
    'pear.remote',
    'pear.meetings',
    'pear.support',
    
    # This one must be last
    'pear.core.templatetags',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "pear.middleware.pearuser.PearUserMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

# Princeton LDAP Configuration
USE_LDAP = False

# Get the environment-specific settings
#pylint: disable-msg=W0401
#pylint: disable-msg=W0614
# Pylint complains because this is a wildcard import and because we don't
# actually use anything that is imported in this file.  However, those are
# both okay here since it is a configuration file and we need everything
# accessible in the settings module
from settings_local import *