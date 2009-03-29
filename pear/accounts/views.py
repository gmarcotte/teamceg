from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django import http
from django.core import exceptions

import pear.accounts.forms

def register(request):
  """Allows a new user to register an account.
     Following successful registration, redirects to home page.   
  """
  if request.method == 'POST':
    form = pear.accounts.forms.RegistrationForm(request.POST)
     
    if form.is_valid():
      new_user = form.save()
      return http.HttpResponseRedirect('/')
  
  else:
    form = pear.accounts.forms.RegistrationForm()
   
  return shortcuts.render_to_response(
      'global/accounts/register.html',
      {'form': form,},
      context_instance=template.RequestContext(request))
  

def login(request):
  """Login using email account."""
  redirect_to = request.REQUEST.get('next', '/')
  
  if request.user.is_authenticated():
    return http.HttpResponseRedirect(redirect_to)

  if request.method == "POST":
    form = pear.accounts.forms.LoginForm(request.POST)
    if form.is_valid():
      auth.login(request, form.cleaned_data['user'])
      return http.HttpResponseRedirect(redirect_to)
  else:
    form = pear.accounts.forms.LoginForm()
    
  return shortcuts.render_to_response(
      'global/accounts/login.html', 
      {'form': form},
      context_instance=template.RequestContext(request))
  
def logout(request):
  """Logout the current user."""
  redirect_to = request.REQUEST.get('next', '/')
  auth.logout(request)
  return http.HttpResponseRedirect(redirect_to)