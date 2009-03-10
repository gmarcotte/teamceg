#!/usr/bin/python
"""Sets up the vendor packages.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


import os
import shutil
import sys

def main():
  
  if hasattr(os, 'symlink'):
    print "Symlinking pimentech..."
    if os.path.exists('django/pimentech'):
      os.remove('django/pimentech')
    os.symlink('pimentech', 'django/pimentech')
    
  else:
    print "Copying pimentech..."
    # If pimentech is already in Django, it is old so get rid of it
    if os.path.exists('django/pimentech'):
      shutil.rmtree('django/pimentech')
    shutil.copytree('pimentech', 'django/pimentech')  
  
if __name__ == '__main__':
  main()