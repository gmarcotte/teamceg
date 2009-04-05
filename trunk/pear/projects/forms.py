from django import forms

import pear.accounts.models
import pear.projects.models
from pear.projects.models import Project
from pear.core.forms import fields as pear_fields
from django.contrib.auth import models as auth_models
from django.contrib import auth
from pear.core import emailer


class NewProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False)
  directory = forms.CharField('Directory', required=False)
  
  partners = pear_fields.ModelHasManyField(
      label="Partners",
      required=False,
      model=pear.accounts.models.PearUser,
      obj_name='partner',
      url='/accounts/ajax/usersearch/?')
  
  course = pear_fields.ModelHasOneField(
      label="Course",
      required=False,
      model=pear.projects.models.Course,
      obj_name='course',
      url='/projects/ajax/coursesearch/?')
  
  is_public = forms.BooleanField(
      label="Make Public?",
      required=False,
      help_text="Check this box to list this project in the public directory.")
  
  def save(self, user):
    # Create the new project
    pr = pear.projects.models.Project()
    pr.is_active = True
    pr.is_deleted = False
    
    pr.name = self.cleaned_data['name'],
    pr.description = self.cleaned_data['description'],
    pr.directory = self.cleaned_data['directory'],
    pr.course = self.cleaned_data['course'],
    pr.is_public = self.cleaned_data['is_public'],
    pr.save()
    
    pr.programmers = self.cleaned_data['partners']
    pr.programmers.add(user)

class EditProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False)
  directory = forms.CharField('Directory', required=False)
  
  course = pear_fields.ModelHasOneField(
      label="Course",
      required=False,
      model=pear.projects.models.Course,
      obj_name='course',
      url='/projects/ajax/coursesearch/?')
  
  is_public = forms.BooleanField(
      label="Make Public?",
      required=False,
      help_text="Check this box to list this project in the public directory.")
  
  def save(self, pr):
    # Save the project
    pr.name = self.cleaned_data['name']
    pr.description = self.cleaned_data['description']
    pr.directory = self.cleaned_data['directory']
    pr.course = self.cleaned_data['course']
    pr.is_public = self.cleaned_data['is_public']
    is_public = self.cleaned_data['is_public']
    raise Exception
    pr.save()

class AddPartnerForm(forms.Form):
  partners = pear_fields.ModelHasManyField(
      label="Partners",
      required=True,
      model=pear.accounts.models.PearUser,
      obj_name='partner',
      url='/accounts/ajax/usersearch/?')
  
  def save(self, project):
    for partner in self.cleaned_data['partners']:
      project.programmers.add(partner)