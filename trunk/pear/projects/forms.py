from django import forms
from django.contrib import auth
from django.contrib.auth import models as auth_models

from pear.core import emailer
from pear.core.forms import fields as pear_fields
import pear.accounts.models
import pear.projects.models


class NewProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False,
                              widget=forms.Textarea())
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
    
    pr.name = self.cleaned_data['name']
    pr.description = self.cleaned_data['description']
    pr.directory = self.cleaned_data['directory']
    pr.course = self.cleaned_data['course']
    pr.is_public = self.cleaned_data['is_public']
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
      
      
######## ADMIN SITE FORMS #######
class AdminCourseForm(forms.ModelForm):
  
  professor = pear_fields.ModelHasManyField(
      label="Professors",
      required=False,
      model=pear.accounts.models.PearUser,
      obj_name='professor',
      url='/accounts/ajax/usersearch/?')
  
  tas = pear_fields.ModelHasManyField(
      label="TAs",
      required=False,
      model=pear.accounts.models.PearUser,
      obj_name='tas',
      url='/accounts/ajax/usersearch/?')
  
  class Meta:
    model = pear.projects.models.Course
        

class AdminProjectForm(forms.ModelForm):
  
  programmers = pear_fields.ModelHasManyField(
      label="Programmers",
      required=False,
      model=pear.accounts.models.PearUser,
      obj_name='programmer',
      url='/accounts/ajax/usersearch/?')
  
  course = pear_fields.ModelHasOneField(
      label="Course",
      required=False,
      model=pear.projects.models.Course,
      obj_name='course',
      url='/projects/ajax/coursesearch/?')
  
  class Meta:
    model = pear.projects.models.Project
    
    
    
    
    
    
    