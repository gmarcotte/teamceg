from django import shortcuts
from django import template
from django import http
from django.core import exceptions
from django.http import HttpResponse

import pear.projects.models
import pear.projects.forms

def index(request):
  if (request.user.is_authenticated()):
	  #display all of their projects
		#project_list = blah?
    return shortcuts.render_to_response(
        'global/index.html',
        {'page_title': 'My Projects',},
        context_instance=template.RequestContext(request))
    
  else:
    #display the registration/login page
	  return shortcuts.render_to_response(
        'global/index.html',
        {'page_title': 'Welcome'},
        context_instance=template.RequestContext(request))


def CreateProject(request):
    if request.method == 'POST':
      form = pear.projects.forms.NewProjectForm(request.POST)
      if form.is_valid():
        form.save()
        return http.HttpResponseRedirect('/')
    else:
      form = pear.projects.forms.NewProjectForm()
    return shortcuts.render_to_response(
        'global/projects/newproject.html',
        {'page_title': 'New Project', 'form': form,},
        context_instance=template.RequestContext(request))

def ProjectIndex(request):
  u = request.user
  list = u.projects.all()  # returns all projects associated with that user
  n = len(list)
  return shortcuts.render_to_response('global/projects/viewprojects.html',
      {'page_title': 'View Projects', 'list': list,})