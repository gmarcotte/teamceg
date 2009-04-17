from django import shortcuts
from django.contrib.auth import decorators as auth_decorators
from django import template

from pear.remote import localkeys
from pear.remote import sshmanager
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
def create_servers(request):
  """Allow a user to create a new SSH connection"""
  redirect_to = request.REQUEST.get('next', '/')
  if request.method == "POST":
    form = pear.remote.forms.ServerAddForm(request.POST)
    usr = request.user
    if form.is_valid():
      form.save(usr)
      localkeys.set_remote_keys(form.cleaned_data['user_name'], form.cleaned_data['password'],form.cleaned_data['server_name'], usr.profile.get().get_public_key())
    return http.HttpResponseRedirect(redirect_to)
  else:
    form = pear.remote.forms.ServerAddForm()
  return shortcuts.render_to_response(
      'global/remote/create_server.html',
      {'page_title': 'Add a new server',
       'form':form},
      context_instance=template.RequestContext(request))


# Toy Shell stuff  ######################   
@auth_decorators.login_required 
def toy(request):
  """."""
  redirect_to = request.REQUEST.get('next', '/')
  id = 0
  servresponse = ''
  rawresponse = ''
  if request.method == "POST":
    form = pear.remote.forms.ToyForm(request.user, data=request.POST)
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
        'global/remote/toy.html',
        {'page_title': 'Toy Shell',
         'form':form,
         'feedback': servresponse},
        context_instance=template.RequestContext(request))
    
  else:
    id = 0
    form = pear.remote.forms.ToyForm(request.user)
    return shortcuts.render_to_response(
        'global/accounts/toy.html',
        {'page_title': 'Toy Shell',
         'form':form,
         'feedback':'Type stuff in...'},
        context_instance=template.RequestContext(request))