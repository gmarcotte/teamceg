from django import shortcuts
from django.core import exceptions
from django.contrib.auth import decorators as auth_decorators
from django import template
from django import http

import pear.remote.forms
import pear.remote.models

@auth_decorators.login_required
def manage_servers(request):
  server_list = request.user.servers.all()
  return shortcuts.render_to_response(
      'global/remote/servers.html',
      {'page_title': 'Manage Server Connections',
       'server_list': server_list},
      context_instance=template.RequestContext(request))
  
@auth_decorators.login_required
def delete_server(request, server_id):
  redirect_to = request.REQUEST.get('next', '/remote/servers/')
  try:
    server = pear.remote.models.SSHConnection.objects.get(pk=server_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(redirect_to)
  
  if request.user != server.user:
    return http.HttpResponseRedirect(redirect_to)
  
  if request.method == 'POST':
    if request.POST.has_key('confirm'):
      request.session['flash_params'] = {'type': 'success'}
      request.session['flash_msg'] = 'Successfully Deleted %s' % server
      server.delete()
    return http.HttpResponseRedirect(redirect_to)
  else:
    return shortcuts.render_to_response(
        'global/remote/delete_server.html',
        {'page_title': "Delete Server Connection",
         'server': server},
        context_instance=template.RequestContext(request))


@auth_decorators.login_required
def test_keys(request, server_id):
  redirect_to = request.REQUEST.get('next', '/remote/servers/')
  try:
    server = pear.remote.models.SSHConnection.objects.get(pk=server_id, user=request.user)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(redirect_to)
  
  if server.test_remote_keys():
    request.session['flash_params'] = {'type': 'success'}
    request.session['flash_msg'] = 'Successfully connected to %s' % server
  else:
    request.session['flash_params'] = {'type': 'error'}
    request.session['flash_msg'] = 'Failed to connect to %s.  Please try refreshing or reinstalling the RSA keys.' % server
  return http.HttpResponseRedirect(redirect_to)

@auth_decorators.login_required
def clear_keys(request, server_id):
  redirect_to = request.REQUEST.get('next', '/remote/servers/')
  try:
    server = pear.remote.models.SSHConnection.objects.get(pk=server_id, user=request.user)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(redirect_to)
  
  if request.method == 'POST':
    if request.POST.has_key('confirm'):
      server.clear_remote_keys()
    return http.HttpResponseRedirect(redirect_to)
  else:
    return shortcuts.render_to_response(
        'global/remote/clear_keys.html',
        {'page_title': "Clear Server Keys",
         'server': server},
        context_instance=template.RequestContext(request))


@auth_decorators.login_required
def refresh_keys(request, server_id):
  """Reinstall the user's key on the server."""
  redirect_to = request.REQUEST.get('next', '/remote/servers/')
  try:
    server = pear.remote.models.SSHConnection.objects.get(pk=server_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(redirect_to)
  
  if request.user != server.user:
      return http.HttpResponseRedirect(redirect_to)
  
  if request.method == 'POST':
    server.set_remote_keys(request.POST['password'])
    return http.HttpResponseRedirect(redirect_to)
  
  else:
    return shortcuts.render_to_response(
        'global/remote/refresh_keys.html',
        {'page_title': 'Refresh Server Keys',
         'server': server},
        context_instance=template.RequestContext(request))


@auth_decorators.login_required
def create_server(request):
  """Allow a user to create a new SSH connection"""
  redirect_to = request.REQUEST.get('next', '/remote/servers/')
  if request.method == "POST":
    form = pear.remote.forms.ServerAddForm(request.POST)
    if form.is_valid():
      form.save(request.user)
      return http.HttpResponseRedirect(redirect_to)
  else:
    form = pear.remote.forms.ServerAddForm()
  return shortcuts.render_to_response(
      'global/remote/create_server.html',
      {'page_title': 'Add a new server',
       'form':form},
      context_instance=template.RequestContext(request))