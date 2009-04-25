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


# Media configuration
STATIC_SERVE = True
ADMIN_MEDIA_PREFIX = '/admin_media'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                          '../media/'))
MEDIA_URL = 'http://localhost:8000'


# Django configuration
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)

# E-Mail Configuration
ENABLE_EMAIL = False
EMAIL_SENDER = ''
EMAIL_USER = ''
EMAIL_PASSWORD = ''
EMAIL_PORT = 0

# Initialization Options
ALLOW_INITIALIZE_SCRIPT = True

# SSH Configuration options
USE_PEXPECT = False
RSA_KEY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../keys'))

# Version info
PEAR_VERSION = 'Sandbox'