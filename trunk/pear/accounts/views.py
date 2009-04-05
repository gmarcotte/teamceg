from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django import http
from django.core import exceptions
from django.views.decorators import cache
from django.db import models

import pear.accounts.forms
import pear.accounts.models
from pear.remote import localkeys
from pear.remote import sshmanager
from pear.core import emailer


MAX_STAFF_AJAX_SEARCH_RESULTS = 10


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
    
# Toy Shell stuff  ######################    
def toy(request):
  """."""
  redirect_to = request.REQUEST.get('next', '/')
  id = 0
  servresponse = ''
  rawresponse = ''
  if request.user.is_authenticated():
    if request.method == "POST":
      form = pear.accounts.forms.ToyForm(request.user, data=request.POST)
      # do the stuff to add the server!
      usr = request.user
      # do stuff
      if form.is_valid():
        if (id == 0):
          ## weird method, but is proof that we can hold onto a session over multiple calls to 
          ## the localkeys code
          rawresponse = sshmanager.ssh_login(form.cleaned_data['user_name'], form.cleaned_data['server_name'], usr.profile.get().get_private_key(),'')#form.cleaned_data['command'])
          id = rawresponse[0]
          servresponse = rawresponse[1]
          rawresponse = sshmanager.ssh_command(id, form.cleaned_data['command'])
          servresponse = servresponse + rawresponse[1] 
          rawresponse = sshmanager.ssh_command(id, form.cleaned_data['command2'])
          servresponse = servresponse + rawresponse[1] 
          rawresponse = sshmanager.ssh_command(id, form.cleaned_data['command3'])
          servresponse = servresponse + rawresponse[1] 
          rawresponse = sshmanager.ssh_command(id)
          servresponse = servresponse + rawresponse[1]
          sshmanager.ssh_close(id) 
      return shortcuts.render_to_response(
          'global/accounts/toy.html',
          {'page_title': 'Toy Shell',
           'form':form,
           'feedback': servresponse},
          context_instance=template.RequestContext(request))
      
    else:
      id = 0
      form = pear.accounts.forms.ToyForm(request.user)
      return shortcuts.render_to_response(
          'global/accounts/toy.html',
          {'page_title': 'Toy Shell',
           'form':form,
           'feedback':'Type stuff in...'},
          context_instance=template.RequestContext(request))

  else:
    return http.HttpResponseRedirect('/accounts/login')  
  
### IGNORE!!!
def toyshell(request):
  """."""
  redirect_to = request.REQUEST.get('next', '/')
  servresponse = ''
  if request.user.is_authenticated():
    # get the ajaxterm going
    if servresponse != '':
      return http.HttpResponseRedirect('/accounts/login') 
    else:
      form = pear.accounts.forms.ToyForm(request.user)
      return shortcuts.render_to_response(
          'global/accounts/toyshell.html',
          {'page_title': 'Toy Shell',
           'form':form,
           'feedback':'Type stuff in...'},
          context_instance=template.RequestContext(request))

  else:
    return http.HttpResponseRedirect('/accounts/login')

# End Toy Shell stuff  ###################### 

  
################ AJAX VIEWS ####################################################

@cache.never_cache
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