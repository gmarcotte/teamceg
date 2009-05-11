"""Settings for the sandbox (developer computer, non-server) environment.
"""

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

# Subversion Access
SVN_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
SVN_BASE_URL = 'file://%s' % SVN_BASE_DIR

# Media configuration
STATIC_SERVE = True
ADMIN_MEDIA_PREFIX = '/admin_media'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/'))
MEDIA_URL = 'http://localhost:8000'

AJAXTERM_URL = 'http://localhost:8022/'


# Django configuration
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/pj')),
)

# E-Mail Configuration
ENABLE_EMAIL = False
EMAIL_SERVER = ''
EMAIL_SENDER = ''
EMAIL_PASSWORD = ''
EMAIL_PORT = 0

# Initialization Options
ALLOW_INITIALIZE_SCRIPT = True

# SSH Configuration options
RSA_KEY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../keys'))
SSH_SERVER_HOST = 'localhost'

# Version info
PEAR_VERSION = 'Sandbox'