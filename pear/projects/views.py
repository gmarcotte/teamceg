from django import shortcuts
from django import template
from django import http
from django.core import exceptions
from django.views.decorators import cache
from django.db import models
from django.contrib.auth import decorators as auth_decorators
from django.core import paginator

import pear.projects.models
from pear.meetings.models import Meeting
from pear.accounts.models import PearUser
import pear.projects.forms
import pear.remote.models
from pear.core import util as pear_util


MAX_COURSE_AJAX_SEARCH_RESULTS = 10


def index(request):
  """Display the main landing page"""
  return shortcuts.render_to_response(
      'global/index.html',
      {'page_title': 'Welcome'},
      context_instance=template.RequestContext(request))


def launch_project(request, project_id):
  """Launch the Pyjamas app for a given project"""
  redirect_to = request.GET.get('next', '/my_projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(redirect_to)
  
  meetings = Meeting.objects.filter(project=project_id)
  
  # User has specified to actually launch
  if request.method == 'POST':
    ssh_id = request.POST.get('server', 0)
    try:
      ssh = request.user.servers.get(pk=ssh_id, has_valid_keys=True)
      server = ssh.server
      user_name = ssh.user_name
    except exceptions.ObjectDoesNotExist:
      server = 'localhost'
      user_name = 'teamceg'
      
    if meetings:
      meeting = meetings[0]
      meeting.passenger = request.user
    else:
      meeting = Meeting()
      meeting.driver = request.user
      meeting.passenger = None
      meeting.project = project
      # set some other things
      meeting.flash = False
      meeting.console = ''
      meeting.editor = ''
    meeting.save()
    return shortcuts.render_to_response(
        'Basic.html',
        {'page_title': 'Project Workspace',
         'project': project,
         'meeting': meeting,
         'server_host': server,
         'server_logon': user_name},
        context_instance=template.RequestContext(request))
  
  # Display a summary of the project session status before launching
  available_servers = request.user.servers.filter(has_valid_keys=True)
  if meetings:
    driver = meetings[0].driver
    passenger = request.user
  else:
    driver = request.user
    passenger = None
  return shortcuts.render_to_response(
      'global/projects/launch_project.html', 
      {'page_title': 'Launch Project', 
       'driver': driver, 
       'passenger': passenger, 
       'project': project,
       'available_servers': available_servers,},
      context_instance=template.RequestContext(request))


@auth_decorators.login_required
def create_project(request):
    if request.method == 'POST':
      form = pear.projects.forms.NewProjectForm(request.POST)
      if form.is_valid():
        form.save(request.user)
        return http.HttpResponseRedirect('/')
    else:
      form = pear.projects.forms.NewProjectForm()
    return shortcuts.render_to_response(
        'global/projects/newproject.html',
        {'page_title': 'New Project', 'form': form,},
        context_instance=template.RequestContext(request))

@auth_decorators.login_required
def project_index(request):
  u = request.user
  project_list = u.projects.all()  # returns all projects associated with that user
  return shortcuts.render_to_response(
      'global/projects/viewprojects.html',
      {'page_title': 'View Projects', 
       'project_list': project_list,},
      context_instance=template.RequestContext(request))
  
@auth_decorators.login_required
def edit_project(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if request.user not in project.programmers.all() or project.is_deleted:
    return http.HttpResponseRedirect(next)
  
  if request.method == 'POST':
      form = pear.projects.forms.EditProjectForm(request.POST)
      if form.is_valid():
        form.save(project)
        return http.HttpResponseRedirect(next)
  else:
    initial = pear_util.instance_dict(project)
    form = pear.projects.forms.EditProjectForm(initial)
  return shortcuts.render_to_response(
      'global/projects/edit_project.html',
      {'page_title': 'Edit Project', 'form': form,},
      context_instance=template.RequestContext(request))


def global_project_listing(request):
  """Displays a list of all active, public projects."""
  
  get_data = {
      'active': 1,
      'per_page': 20,
      'orphans': 10,
      'page': 1
  }
  for key in request.GET.keys():
    get_data[key] = int(request.GET.get(key))
    
  raise Exception(str(get_data))
  
  projects = pear.projects.models.Project.objects.filter(is_public = True)
  
  if get_data['active'] in [0, 1]:  
    projects = projects.filter(is_active = get_data['active'])
  
  try:
    project_pages = paginator.Paginator(projects, 
                                        get_data['per_page'], 
                                        get_data['orphans'], 
                                        False)
    try:
      page = project_pages.page(get_data['page'])
    except paginator.InvalidPage:
      page = project_pages.page(1)
  except paginator.EmptyPage:
    project_pages = None
    page = None
  
  return shortcuts.render_to_response(
      'global/projects/public_list.html',
      {'page_title': "Browse Public Projects",
       'project_pages': project_pages,
       'page': page,
       'get_data': get_data,}, 
       context_instance=template.RequestContext(request))
  
@auth_decorators.login_required
def leave_project(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if request.user not in project.programmers.all() or project.is_deleted:
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('cancel'):
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('leave'):
    project.programmers.remove(request.user)
    if not project.programmers.all():
      project.is_active = False
      project.save()
    return http.HttpResponseRedirect(next)
  
  return shortcuts.render_to_response(
      'global/projects/leave.html',
      {'page_title': "Leave Project %s" % project.name,
       'project': project,},
      context_instance=template.RequestContext(request))
  
@auth_decorators.login_required
def delete_project(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if (request.user not in project.programmers.all() or 
      project.programmers.count() == 1 or
      project.is_deleted):
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('cancel'):
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('delete'):
    project.is_deleted = True
    project.save()
    return http.HttpResponseRedirect(next)
  
  return shortcuts.render_to_response(
      'global/projects/delete_project.html',
      {'page_title': "Delete Project %s" % project.name,
       'project': project,},
      context_instance=template.RequestContext(request))
  

@auth_decorators.login_required
def resurrect_project(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if request.user not in project.programmers.all() or not project.is_deleted:
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('cancel'):
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('resurrect'):
    project.is_deleted = False
    project.save()
    return http.HttpResponseRedirect(next)
  
  return shortcuts.render_to_response(
      'global/projects/resurrect_project.html',
      {'page_title': "Resurrect Project %s" % project.name,
       'project': project,},
      context_instance=template.RequestContext(request))


@auth_decorators.login_required
def join_project(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if request.user in project.programmers.all() or project.is_deleted:
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('cancel'):
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('join'):
    project.programmers.add(request.user)
    if not project.is_active:
      project.is_active = True
      project.save()
    return http.HttpResponseRedirect(next)
  
  else:
    return shortcuts.render_to_response(
        'global/projects/join.html',
        {'page_title': "Join Project %s" % project.name,
         'project': project,},
        context_instance=template.RequestContext(request))
    
@auth_decorators.login_required
def add_partners(request, project_id):
  next = request.REQUEST.get('next', '/projects/')
  try:
    project = pear.projects.models.Project.objects.get(pk=project_id)
  except exceptions.ObjectDoesNotExist:
    return http.HttpResponseRedirect(next)
  
  if request.user not in project.programmers.all():
    return http.HttpResponseRedirect(next)
  
  if request.POST.has_key('cancel'):
    return http.HttpResponseRedirect(next)
  
  if request.method == 'POST':
    form = pear.projects.forms.AddPartnersForm(request.POST)
    if form.is_valid():
      form.save(project)
      return http.HttpResponseRedirect(next)
  else:
    form = pear.projects.forms.NewProjectForm()
  return shortcuts.render_to_response(
      'global/projects/add_partners.html',
      {'page_title': 'Add Partners to %s' % project.name, 
       'form': form,},
      context_instance=template.RequestContext(request))
    
  
  
##################### AJAX VIEWS ###############################################

@auth_decorators.login_required
def ajax_course_search(request):
  """AJAX call that returns a JSON array of courses matching the search field.
  
  The method looks for the GET parameter 'q' for search terms. One can change
  the default max search results by passing a GET parameter 'max'.
  """
  
  # Default max results
  if request.GET.has_key('max'):
    max_results = int(request.GET['max'])
  else:
    max_results = MAX_COURSE_AJAX_SEARCH_RESULTS
  
  if request.GET.has_key('q'):
    courses = pear.projects.models.Course.objects.all()
    
    for word in request.GET['q'].split(' '):
      courses = courses.filter(models.Q(name__icontains=word) | 
                               models.Q(department__icontains=word) |
                               models.Q(number__icontains=word))
    new_list = []
    for course in courses[:max_results]:
      new_list.append('{"id": "%s", "value": "%s"}' 
                      % (course.id, str(course)))
    
    return http.HttpResponse('{"results": [%s]}' % (','.join(new_list)))              
  else:    
    return http.HttpResponse('{"results": []}')
