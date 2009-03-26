#!/usr/bin/python
"""Sets up the vendor packages.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


import os
import shutil
import stat

def main():
  
  ### Set up pimentech's libcommonDjango libraries ###
  #if hasattr(os, 'symlink'):
   # print "Symlinking pimentech..."
    #if os.path.exists('django/pimentech'):
     # os.remove('django/pimentech')
    #os.symlink('pimentech', 'django/pimentech')
    
  #else:
  print "Copying pimentech..."
  # If pimentech is already in Django, it is old so get rid of it
  if os.path.exists('django/pimentech'):
    # First we have to make all of .svn writeable
    for (root, dirs, files) in os.walk('django/pimentech', topdown=False):
      for name in files:
        os.chmod(os.path.join(root, name), stat.S_IWRITE)
      for name in dirs:
        os.chmod(os.path.join(root, name), stat.S_IWRITE)
    shutil.rmtree('django/pimentech')
  shutil.copytree('pimentech', 'django/pimentech')
  ####################################################
  
  ## Set up Logilab Common ##
  try:
    import logilab.common
    print "logilab-common already installed..."
  except ImportError, e:
    print "Installing Common..."
    os.chdir("logilab-common")
    os.system("python setup.py install")
    os.chdir("..")
  
  try:
    import logilab.common
  except ImportError, e:
    print "Errors installing logilab-common! Please perform manual install!"
  #####################################################
  
  ## Set up Logilab ASTNG ##
  try:
    import logilab.astng
    print "logilab-astng already installed..."
  except ImportError, e:
    print "Installing ASTNG..."
    os.chdir("logilab-astng")
    os.system("python setup.py install")
    os.chdir("..")
  
  try:
    import logilab.astng
  except ImportError, e:
    print "Errors installing logilab-astng! Please perform manual install!"
  #####################################################
  
  ## Set up PyLint ##
  try:
    import pylint
    print "PyLint already installed..."
  except ImportError, e:
    print "Installing PyLint..."
    os.chdir('pylint')
    os.system("python setup.py install")
    os.chdir("..")  
  
  try:
    import pylint
  except ImportError, e:
    print "Errors installing PyLint! Please perform manual install!"
  ####################################################
  
  
if __name__ == '__main__':
  main()