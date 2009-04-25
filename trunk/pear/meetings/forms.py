#
#  forms.py
#  sandbox
#
#  Created by Christina Ilvento on 4/24/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django import forms
from django.contrib import auth
from django.contrib.auth import models as auth_models

import pear.meetings.models
import pear.accounts.models
import pear.projects.models

### Admin ###
class AdminSessionForm(forms.ModelForm):
  
  driver = pear_fields.ModelHasManyField(
      label="Driver",
      required=True,
      model=pear.accounts.models.PearUser,
      obj_name='driver',
      url='/accounts/ajax/usersearch/?')
  passenger = pear_fields.ModelHasManyField(
      label="Passenger",
      required=True,
      model=pear.accounts.models.PearUser,
      obj_name='passenger',
      url='/accounts/ajax/usersearch/?')
  
  project = pear_fields.ModelHasOneField(
      label="Project",
      required=True,
      model=pear.projects.models.Project,
      obj_name='project',
      url='/projects/ajax/coursesearch/?')
  
  class Meta:
    model = pear.projects.models.Session