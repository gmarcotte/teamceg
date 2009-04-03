"""
File:    initialize.py
Author:  Chris Chan
Date:    12/04/2007

Modified by Garrett Marcotte - 4/3/2009

This script creates an initial 

Call the script as:
    python initialize.py

Script must be placed in 'pear/environments/sandbox/initialize.py'
"""

import os, sys, re, shutil

# Update python path to include vendors folder
# This is a bit hack-ish because we have to change folders
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../vendor'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../pear'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../../..'))

# Import django
from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

# Import dp settings file
try:
    import settings
    
    # Setup django environment
    setup_environ(settings)
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. \n" % __file__)
    sys.exit(1)

# Import MySQLdb
try:
    import MySQLdb
except ImportError:
    sys.stderr.write("Error: Can't import MySQLdb. Make sure the module is installed. \n")
    sys.exit(1)

# Directory/file locations 
current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.abspath(os.path.join(current_path, '../..'))


def write_msg(message, output_file=None, stream=None):
    """
    Write message to given stream and/or global output file.
    """
    
    if stream: 
        stream.write(message)
    
    if output_file:
        output_file.write(message)


def ask_boolean_question(question):
    """
    Asks the given question and returns True/False depending of whether user
    replied with a 'Yes' or 'No'
    """
    
    sys.stdout.write(question)
    
    answer = sys.stdin.readline()
    while answer:
        sys.stdout.write("\n")
        
        # Remove answer of newlines and strip whitespace
        answer = answer.replace('\n', '').strip()
        
        if answer in ('yes', 'Yes', 'YES'):
            return True
        elif answer in ('no', 'No', 'NO'):
            return False
        else:
            sys.stdout.write(question)
            answer = sys.stdin.readline()
    
    return False


def ask_input_question(question, default=''):
    """
    Asks user for an input and returns it stripped of ending newlines and extra spaces.
    """
    
    sys.stdout.write(question)
    answer = sys.stdin.readline()
    answer = answer.replace('\n', '').strip()
    if not answer:
      answer = default


def create_root_user():
  """Create a superuser for testing purposes"""
  from pear.accounts import forms
  from pear.accounts import models
  
  if models.PearUser.objects.all():
    write_msg('ERROR: User #1 already exists, cannot create root user\n',
              output_file, sys.stdout)
    return
    
  data = {
      'email' : 'pairgramming@gmail.com',
      'first_name' : 'Team',
      'last_name' : 'CEG',
      'class_year' : '2010',
      'department' : 'ELE!'}
  frm = forms.RegistrationForm(data)
  if frm.is_valid():
    frm.save()
    
        

def set_root_password(output_file=None):
  """
  Set the admin root user password
  """
  from pear.accounts import models
  from django.core import exceptions
  
  write_msg("Setting root user password... \n", output_file, sys.stdout)
  
  try:
    root_user = models.PearUser.objects.get(id=1)
    root_password = ask_input_question('Enter password for admin root user: ', 'pw')
    
    root_user.set_password(root_password)
    root_user.save
    
    # Check that password was correctly saved
    if not root_user.check_password(root_password):
        raise Exception, "Root password improperly saved."        
    else:
        write_msg("Successfully changed password for admin root user. \n\n", output_file, sys.stdout)
      
  except exceptions.ObjectDoesNotExist:
    write_msg("Error: could not find admin root user!. \n\n", output_file, sys.stdout)
  
  
def main(argv=None):
    """Main function"""
    
    sys.stdout.write("----------------- INITIALIZING SANDBOX -----------------\n")
    
    # To prevent accidental use of this script, we make sure it's not run on production
    try:
        if not settings.ALLOW_INITIALIZE_SCRIPT:
            sys.stderr.write("To run this script, set ALLOW_INITIALIZE_SCRIPT=True to the settings file. \n")
            sys.exit(1)
        
        if settings.DATABASE_NAME.find('sandbox') < 0 or settings.STATIC_SERVE == False:
            sys.stdout.write("It looks like this script is being run on an environment besides sandbox. \n")
            
            if not ask_boolean_question("Continue with script on '%s'? (yes/no):" % (settings.DATABASE_NAME)):
                sys.stdout.write("Exiting %s. \n" % __file__)
                sys.exit()
        
    except AttributeError:
        sys.stderr.write("To run this script, add ALLOW_INITIALIZE_SCRIPT=True to the settings file. \n")
        sys.exit(1)
    
    # Make connection to database
    # We do this first just to make sure username/password are correct
    try:
        conn = MySQLdb.connect(host="localhost", user=settings.DATABASE_USER, passwd=settings.DATABASE_PASSWORD, db=settings.DATABASE_NAME)
    except Exception, e:
        sys.stderr.write("Error: can't connect to local mysql db using settings.py. Check your 'settings_local.py'. \n" % (e))
        sys.exit()
    
    # Make sure we're ok to wipe out database
    if not ask_boolean_question("This script will clear existing data in %s. Continue? (yes/no): " % (settings.DATABASE_NAME)):
        sys.stdout.write("Exiting %s. \n" % __file__)
        sys.exit()
    
    cursor = conn.cursor()
    
    # DROP and recreate database
    sys.stdout.write("DROP DATABASE %s \n" % settings.DATABASE_NAME)
    cursor.execute("DROP DATABASE %s" % settings.DATABASE_NAME)
    
    sys.stdout.write("CREATE DATABASE %s CHARACTER SET utf8 \n" % settings.DATABASE_NAME)
    cursor.execute("CREATE DATABASE %s CHARACTER SET utf8" % settings.DATABASE_NAME)
    
    # Execute "python manage.py syncdb"
    os.chdir(root_path)
    os.system("python manage.py syncdb")
    os.chdir(current_path)
    
    cursor.execute("USE %s" % settings.DATABASE_NAME)
    cursor.execute("TRUNCATE auth_user")
    
    # Set up a superuser
    create_root_user()
    
    # Change root password
    set_root_password()
    
    # Close connection
    conn.close()
    
    sys.stdout.write("----------------- FINISHED INITIALIZING SANDBOX -----------------\n")
    
if __name__ == "__main__":
    sys.exit(main())
