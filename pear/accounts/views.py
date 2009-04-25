from django import http
from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import decorators as auth_decorators
from django.contrib.auth import models as auth_models
from django.core import exceptions
from django.db import models
from django.views.decorators import cache

import pear.accounts.forms
import pear.accounts.models
from pear.core import emailer


MAX_STAFF_AJAX_SEARCH_RESULTS = 10


def register(request):
  """Allows a new user to register an account.
     Following successful registration, redirects to home page.   
  """
  if request.method == 'POST':
    form = pear.accounts.forms.RegistrationForm(request.POST)
     
    if form.is_valid():
      if form.save():
        return http.HttpResponseRedirect('/')
      
  else:
    form = pear.accounts.forms.RegistrationForm()
   
  return shortcuts.render_to_response(
      'global/accounts/register.html',
      {'form': form,},
      context_instance=template.RequestContext(request))


def registered(request):
  return shortcuts.render_to_response('global/accounts/registered.html')


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


@auth_decorators.login_required
def logout(request):
  """Logout the current user."""
  redirect_to = request.REQUEST.get('next', '/')
  auth.logout(request)
  return http.HttpResponseRedirect(redirect_to)


@auth_decorators.login_required
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


@auth_decorators.login_required
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
  

@auth_decorators.login_required
def invite_user(request):
  if request.method == 'POST':
      form = pear.accounts.forms.InviteUserForm(request.POST)
      if form.is_valid():
        form.save()
        return http.HttpResponseRedirect('/')
  else:
      form = pear.accounts.forms.InviteUserForm()
  return shortcuts.render_to_response(
      'global/accounts/inviteuser.html',
      {'page_title': 'Invite a Friend', 'form': form,},
      context_instance=template.RequestContext(request))  
  
################ AJAX VIEWS ####################################################

@cache.never_cache
@auth_decorators.login_required
def ajax_user_search(request):
  """AJAX call that returns a JSON array of staff members matching search field.
  
  The method looks for the GET parameter 'q' for search terms. One can change
  the default max search results by passing a GET parameter 'max'.
  """
  
  # Default max results
  if request.GET.has_key('max'):
    max_results = int(request.GET['max'])
  else:
    max_results = MAX_STAFF_AJAX_SEARCH_RESULTS
  
  if request.GET.has_key('q'):
    users = pear.accounts.models.PearUser.objects.filter(is_active = 1)
    
    for word in request.GET['q'].split(' '):
      users = users.filter(models.Q(first_name__icontains=word) | 
                           models.Q(last_name__icontains=word) |
                           models.Q(email__icontains=word))
    new_list = []
    for user in users[:max_results]:
      new_list.append('{"id": "%s", "value": "%s %s"}' 
                      % (user.id, user.first_name, user.last_name))
    
    return http.HttpResponse('{"results": [%s]}' % (','.join(new_list)))              
  else:    
    return http.HttpResponse('{"results": []}')