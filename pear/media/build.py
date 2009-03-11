#!/usr/bin/python
"""Invokes Pyjamas to compile the client-side code into Javascript.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

import os
import sys

current_dir = os.path.dirname(__file__)
pyjamas_build = os.path.abspath(os.path.join(current_dir, '../../vendor/pyjamas/builder/build.py'))
app_name = "TodoApp.py"

command = "python %s %s" % (pyjamas_build, app_name)

print "Starting build with command:"
print
print command
print
print "********************************************************************"
print

os.system(command)