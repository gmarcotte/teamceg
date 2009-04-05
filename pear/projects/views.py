from django import shortcuts
from django import template
from django import http
from django.core import exceptions
from django.views.decorators import cache
from django.db import models
from django.contrib.auth import decorators as auth_decorators
from django.core import paginator

import pear.projects.models
import pear.projects.forms


MAX_COURSE_AJAX_SEARCH_RESULTS = 10


def index(request):
  """Display the main landing page"""
  return shortcuts.render_to_response(
      'global/index.html',
      {'page_title': 'Welcome'},
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
  list = u.projects.all()  # returns all projects associated with that user
  return shortcuts.render_to_response(
      'global/projects/viewprojects.html',
      {'page_title': 'View Projects', 'list': list,},
      context_instance=template.RequestContext(request))
  
@auth_decorators.login_required
def add_partner(request):
  if request.method == 'POST':
      form = pear.projects.forms.AddPartnerForm(request.POST)
      if form.is_valid():
        form.save(request.user)
        return http.HttpResponseRedirect('/')
  else:
      form = pear.projects.forms.AddPartnerForm()
  return shortcuts.render_to_response(
      'global/projects/addpartner.html',
      {'page_title': 'Add Partner', 'form': form,},
      context_instance=template.RequestContext(request))
  
def global_project_listing(request):
  """Displays a list of all active, public projects."""
  
  get_data = {
      'active': 1,
      'per_page': 20,
      'orphans': 10,
      'page': 1
  }
  get_data.update(request.GET)
  
  projects = pear.projects.models.Project.objects.all()
  
  if get_data['active'] in [0, 1]:  
    projects = pear.projects.models.Project.objects.filter(
        is_active = get_data['active'])
  
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
       'page': page,}, 
       context_instance=template.RequestContext(request))
  
##################### AJAX VIEWS ###############################################

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
