#!/usr/bin/python
"""Functions for manipulating the system Python path.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

import os
import sys

def add_sys_path(new_path):
  """Adds a given path to the system python search path.
  Args:
    new_path: A string, the path to add
  """
  
  # Standardize
  new_path = os.path.abspath(new_path)
  
  # Use lowercase for MS-Windows
  if sys.platform == 'win32':
    new_path = new_path.lower()
      
  ret = -1
  if os.path.exists(new_path):
    ret = 1
    
    for x in sys.path:
      x = os.path.abspath(x)
      if sys.platform == 'win32':
        x = x.lower()
      if new_path in (x, x + os.sep):
        ret = 0
    
    if ret:
      sys.path.append(new_path)
  
  return ret