from django import shortcuts
from django import template
from django import http

import pear.accounts.models
import pear.projects.models


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
