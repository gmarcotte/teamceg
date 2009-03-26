#!/usr/bin/python
"""A thin wrapper around PyLint to conform to our style standards.
Usage:
  >> python pear-pylint.py file1 file2 ....
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

# Python Modules
import os
import sys

# Pear Modules
import python_path

# Update the Python path so that PyLint knows about our vendor modules
vendor_path = os.path.join(os.path.dirname(__file__), '../vendor')
python_path.add_sys_path(vendor_path)

# Pylint Modules
from pylint import lint

opts = [
    "--rcfile=pear-pylintrc.cfg",
]
opts.extend(sys.argv[1:])

command = "pylint %s" % (' '.join(opts))
print "Running: %s" % command

lint.Run(opts)