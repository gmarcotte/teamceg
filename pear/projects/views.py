#
#  views.py
#  sandbox
#
#  Created by Christina Ilvento on 3/26/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django import shortcuts
import pear.accounts.models
import pear.projects.models
from django import http

def index(request):
  if (request.user.is_authenticated()):
	  #display all of their projects
		#project_list = blah?
    return shortcuts.render_to_response('global/projectView.html')
  else:
    #display the registration/login page
	  return shortcuts.render_to_response('global/index.html')
