#
#  views.py
#  sandbox
#
#  Created by Christina Ilvento on 3/26/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django.template import Context, loader
from pear.accounts.models import Profile
from pear.projects.models import Project
from pear.projects.models import Course
from django.http import HttpResponse

def index(request):
    if (request.User.is_authenticated()):
	    #display all of their projects
		#project_list = blah?
        return render_to_response('global/projectView.html')#,{'':project_list})
    else:
	    #display the registration/login page
	    return render_to_response('global/index.html')
