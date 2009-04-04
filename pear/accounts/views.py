from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django import http
from django.core import exceptions

import pear.accounts.forms
from pear.remote import localkeys
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
      {'page_title': "Log In",
       'form': form,},
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
      {'page_title': 'Change Password',
       'form': form},
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
      {'page_title': 'Reset Password',
       'form': form},
      context_instance=template.RequestContext(request))
  return http.HttpResponseRedirect(redirect_to)


def delete(request):
  """Delete all information associated with user."""
  redirect_to = request.REQUEST.get('next', '/')
  
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
      return http.HttpResponseRedirect(redirect_to)
    else:
      return shortcuts.render_to_response(
          'global/accounts/delete.html',
          {'page_title': 'Permanently Delete Account',},
          context_instance=template.RequestContext(request))

  else:
    return http.HttpResponseRedirect('/accounts/login')

def servers(request):
  """Delete all information associated with user."""
  redirect_to = request.REQUEST.get('next', '/')
  
  if request.user.is_authenticated():
    if request.method == "POST":
      form = pear.accounts.forms.ServerAddForm(request.user, data=request.POST)
      # do the stuff to add the server!
      usr = request.user
      if form.is_valid():
        localkeys.set_remote_keys(form.cleaned_data['user_name'],form.cleaned_data['password'],form.cleaned_data['server_name'], usr.profile.get().get_public_key())
      return http.HttpResponseRedirect(redirect_to)
    else:
      form = pear.accounts.forms.ServerAddForm(request.user)
      return shortcuts.render_to_response(
          'global/accounts/servers.html',
          {'page_title': 'Add a new server',
           'form':form},
          context_instance=template.RequestContext(request))

  else:
    return http.HttpResponseRedirect('/accounts/login')
    
    
def toy(request):
  """Delete all information associated with user."""
  redirect_to = request.REQUEST.get('next', '/')
  servresponse = ''
  if request.user.is_authenticated():
    if request.method == "POST":
      form = pear.accounts.forms.ToyForm(request.user, data=request.POST)
      # do the stuff to add the server!
      usr = request.user
      # do stuff
      if form.is_valid():
        servresponse = localkeys.ssh_login(form.cleaned_data['user_name'], form.cleaned_data['server_name'], usr.profile.get().get_private_key(),form.cleaned_data['command'])
      return shortcuts.render_to_response(
          'global/accounts/toy.html',
          {'page_title': 'Toy Shell',
           'form':form,
           'feedback': servresponse},
          context_instance=template.RequestContext(request))
      
    else:
      form = pear.accounts.forms.ToyForm(request.user)
      return shortcuts.render_to_response(
          'global/accounts/toy.html',
          {'page_title': 'Toy Shell',
           'form':form,
           'feedback':'Type stuff in...'},
          context_instance=template.RequestContext(request))

  else:
    return http.HttpResponseRedirect('/accounts/login')