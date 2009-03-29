from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django import http
from django.core import exceptions

import pear.accounts.forms
from pear.core import emailer

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


def change_password(request):
  """Allow the currently logged in user to change passwords."""
  redirect_to = request.REQUEST.get('next', '/')
  
  if not request.user.is_authenticated():
      return http.HttpResponseRedirect(redirect_to)
  
  if request.method == "POST":
    form = pear.accounts.forms.PasswordChangeForm(request.user, data=request.POST)
    if form.is_valid():
      form.save()
      return http.HttpResponseRedirect(redirect_to)
  else:
    form = pear.accounts.forms.PasswordChangeForm(request.user)
    
  return shortcuts.render_to_response(
      'global/accounts/change_password.html',
      {'form': form},
      context_instance=template.RequestContext(request))


def reset_password(request):
  """Allow a user to reset password via email."""
  redirect_to = request.REQUEST.get('next', '/')
  
  if request.method == "POST":
    form = pear.accounts.forms.PasswordResetForm(request.POST)
    if form.is_valid():
      form.save()
      return http.HttpResponseRedirect(redirect_to)
  else:
    form = pear.accounts.forms.PasswordResetForm() # ERROR
  
  return shortcuts.render_to_response(
      'global/accounts/reset_password.html',
      {'form': form},
      context_instance=template.RequestContext(request))
  return http.HttpResponseRedirect(redirect_to)


def delete(request):
  """Delete all information associated with user."""
  if request.user.is_authenticated():
    if request.method == "POST":
      #log out the user
      usr = request.user
      auth.logout(request)
      #delete the user
      emailer.render_and_send(usr.email,
                            'Your Pairgramming account has been deleted',
                            'emails/delete_account.txt', {})
      usr.delete()
      return shortcuts.render_to_response('global/index.html')
    else:
      return shortcuts.render_to_response('global/accounts/delete.html')
      
  else:
    form = pear.accounts.forms.LoginForm()
    return shortcuts.render_to_response(
      'global/accounts/login.html', 
      {'form': form},
      context_instance=template.RequestContext(request))