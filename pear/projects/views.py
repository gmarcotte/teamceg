from django import shortcuts
from django import template
from django import http
from django.core import exceptions
from django.views.decorators import cache
from django.db import models

import pear.projects.models
import pear.projects.forms


MAX_COURSE_AJAX_SEARCH_RESULTS = 10


def index(request):
  """Display the main landing page"""
  return shortcuts.render_to_response(
      'global/index.html',
      {'page_title': 'Welcome'},
      context_instance=template.RequestContext(request))


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


def project_index(request):
  u = request.user
  list = u.projects.all()  # returns all projects associated with that user
  return shortcuts.render_to_response(
      'global/projects/viewprojects.html',
      {'page_title': 'View Projects', 'list': list,},
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
