"""Views for the admin site to override existing Django admin views."""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

from django import http
from django.contrib import admin
from django.contrib import auth
from django.views.decorators import cache

LOGIN_ERROR_MESSAGE = ("Please enter a correct username and password. "
                       "Note that both fields are case-sensitive.")
LOGIN_FORM_KEY = 'this_is_the_login_form'

class PearAdminSite(admin.AdminSite):
  
  def __init__(self, *args, **kwargs):
    super(PearAdminSite, self).__init__(*args, **kwargs)
    self.root_path = '/admin/'
  
  @cache.never_cache
  def login(self, request):
    """
    Displays the login form for the given HttpRequest.
    """
    # If this isn't already the login page, display it.
    if not request.POST.has_key(LOGIN_FORM_KEY):
      if request.POST:
        message = "Please log in again, because your session has expired."
      else:
        message = ""
      return self.display_login_form(request, message)
  
    # Check that the user accepts cookies.
    if not request.session.test_cookie_worked():
      message = "Looks like your browser isn't configured to accept cookies. Please enable cookies, reload this page, and try again."
      return self.display_login_form(request, message)
    else:
      request.session.delete_test_cookie()
  
    # Check the password.
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = auth.authenticate(username=username, password=password)
    if user is None:
      return self.display_login_form(request, LOGIN_ERROR_MESSAGE)
  
    # The user data is correct; log in the user in and continue.
    else:
      if user.is_active and user.is_staff:
        auth.login(request, user)
        return http.HttpResponseRedirect(request.get_full_path())
      else:
        return self.display_login_form(request, LOGIN_ERROR_MESSAGE)