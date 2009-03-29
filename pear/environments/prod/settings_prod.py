"""Settings for the production environment.
"""

#TODO(marcotte): This is not configured yet!

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

import os


# Database setup
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'pear_sandbox'
DATABASE_USER = 'u'
DATABASE_PASSWORD = 'p'
DATABASE_HOST = ''
DATABASE_PORT = ''

# Server configuration
SERVER_HOSTNAME = 'http://localhost:8000'


# Media configuration
STATIC_SERVE = True
ADMIN_MEDIA_PREFIX = '/admin_media'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/'))
MEDIA_URL = 'http://localhost:8000'


# Django configuration
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)

# E-Mail Configuration
ENABLE_EMAIL = True
EMAIL_SERVER = 'smtp.google.com'
EMAIL_SENDER = 'pairgramming@gmail.com'
EMAIL_PASSWORD = ''
EMAIL_PORT = 587

# Version info
PEAR_VERSION = 'Pre-Release'