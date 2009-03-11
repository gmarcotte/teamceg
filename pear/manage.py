#!/usr/bin/python
"""Loads the Django environment and accesses Django-admin commands.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


# Add our vendor folders to the Python Path
import os
import python_path

vendor_path = os.path.join(os.path.dirname(__file__), '../vendor')
python_path.add_sys_path(vendor_path)


# Start up Django
from django.core.management import execute_manager
try:
  import settings
except ImportError:
  import sys
  sys.stderr.write(("Error: Can't find the file 'settings.py' in the directory "
                    "containing %r. It appears you've customized things.\nYou'll"
                    " have to run django-admin.py, passing it your settings "
                    "module.\n(If the file settings.py does indeed exist, it's "
                    "causing an ImportError somehow.)\n" % __file__))
  sys.exit(1)


if __name__ == '__main__':
  execute_manager(settings)