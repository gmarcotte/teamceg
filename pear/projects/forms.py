from django import forms
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django.conf import settings

from pear.core import emailer
from pear.core.forms import fields as pear_fields
import pear.accounts.models
import pear.projects.models
import pear.meetings.models


class NewProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False,
                              widget=forms.Textarea())
  directory = forms.CharField(
      'Directory', required=True,
      help_text=('Files for this project will be stored in this directory '
                 '(relative to the base directory that you specify for '
                 'your SSH connection)'))
  
  #repository = forms.CharField(
  #    'SVN Repository', required=False,
  #    help_text=('To use an existing Subversion repository, enter the URL '
  #               'here. If you leave this blank, a repository will be created '
  #               'for your project on our server.'))
  
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
    
   # if not self.cleaned_data['repository']:
    pr.repos = 'project%d' % pr.id
   # else:
   #   pr.repository = self.cleaned_data['repository']
    pr.create_repository()
    pr.save()
    
    pr.programmers = self.cleaned_data['partners']
    pr.programmers.add(user)

# This will be removed later, or made more graceful
class LaunchForm(forms.Form):
  # maybe try this instead later? forms.ModelChoiceField()
  name = forms.CharField('Project Name', required=False) # change this to a foreign key field
  
  def save(self, user, project, passenger):
    meet = pear.meetings.models.Meeting()
    meet.driver = user
    meet.passenger = passenger
    meet.project = project
    # set some other things
    meet.flash = False
    console = ''
    editor = ''
    meet.save()

class EditProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False,
                                widget=forms.Textarea())
  directory = forms.CharField('Directory', required=True)
  
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
    
    
    
    
    
    
    