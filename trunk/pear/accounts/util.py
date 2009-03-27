from django.core import exceptions
from django.contrib.auth import models as auth_models

def make_username_from_email(email):
  """Returns a unique username from the email address.
 
  This function is used for creating generating a username for django-auth
  when creating staffusers and publicusers.
 
  The username must be alpha-numeric and unique, so we do some "hacking"
  to derive a username from an email.
 
  Args:
    email: A string, an email address.
 
  Returns:
    A string containing the corresponding unique username
 
  Raises:
    ValueError: A unique username cannot be created.
  """
 
  # Because username has max length of 30, we need to truncate email
  new_username = email
 
  if len(email) > 19:
    new_username = new_username[0:19]
 
  # Replace '@' character to preserve alpha-
  new_username = new_username.replace('@', 'a')
  # Replate '.'
  new_username = new_username.replace('.', 'd')
 
  # Try 10 times to come up with a name by appending digit to username
  for i in range(0,10):
    try:
      u = auth_models.User.objects.get(username=new_username + str(i))
    except exceptions.ObjectDoesNotExist:
      return new_username + str(i)
 
  # Raise error if all usernames taken up
  raise ValueError