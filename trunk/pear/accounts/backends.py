"""Authenticates by email rather than username."""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

# Django Modules
from django.contrib.auth import backends
from django.contrib.auth import models
from django.forms import fields


class BasicBackend(backends.ModelBackend):
  def get_user(self, user_id):
    try:
      return models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
      return None


class EmailBackend(BasicBackend):
  def authenticate(self, username=None, password=None):
    if fields.email_re.search(username):
      users = models.User.objects.filter(email__exact = username)
      if not users:
        return None
      if not users[0].check_password(password):
        return None
      return users[0]      
	  
	  
# from the oit CAS page https://sp.princeton.edu/oit/sdp/CAS/Wiki%20Pages/Python.aspx
import sys, os, cgi, urllib, re
form = cgi.FieldStorage()
class CASClient:
   def __init__(self):
      self.cas_url = 'https://fed.princeton.edu/cas/'
   def Authenticate(self):
      # If the request contains a login ticket, try to validate it
      if form.has_key('ticket'):
         netid = self.Validate(form['ticket'].value)
         if netid != None:
            return netid
      # No valid ticket; redirect the browser to the login page to get one
      login_url = self.cas_url + 'login' \
         + '?service=' + urllib.quote(self.ServiceURL())
      print 'Location: ' + login_url
      print 'Status-line: HTTP/1.1 307 Temporary Redirect'
      print ""
      sys.exit(0)
   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?service=' + urllib.quote(self.ServiceURL()) + \
         '&ticket=' + urllib.quote(ticket)
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return r[1].strip()
      return None
   def ServiceURL(self):
      if os.environ.has_key('REQUEST_URI'):
         ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
         ret = re.sub(r'ticket=[^&]*&?', '', ret)
         ret = re.sub(r'\?&?$|&$', '', ret)
         return ret
      return "error: request_uri fails"
