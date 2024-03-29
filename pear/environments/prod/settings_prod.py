"""Settings for the production environment.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

import os


# Database setup
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'pear_prod'
DATABASE_USER = 'u'
DATABASE_PASSWORD = 'p'
DATABASE_HOST = ''
DATABASE_PORT = ''

# Server configuration
SERVER_HOSTNAME = 'http://teamceg.princeton.edu'

# Subversion Access
SVN_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
SVN_BASE_URL = 'http://teamceg.princeton.edu/repos'

# Media configuration
STATIC_SERVE = True
ADMIN_MEDIA_PREFIX = '/admin_media'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/'))
MEDIA_URL = 'http://teamceg.princeton.edu'

AJAXTERM_URL = 'http://teamceg.princeton.edu/ajaxterm/'


# Django configuration
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/pj/')),
)

# E-Mail Configuration
ENABLE_EMAIL = True
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_SENDER = 'pairgramming@gmail.com'
EMAIL_PASSWORD = ''
EMAIL_PORT = 587

# SSH Configuration options
RSA_KEY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../keys'))
SSH_SERVER_HOST = 'teamceg.princeton.edu'

# Version info
PEAR_VERSION = 'Pre-Release'