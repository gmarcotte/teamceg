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
    pr = pear.projects.models.Project(
        name = self.cleaned_data['name'],
        description = self.cleaned_data['description'],
        directory = self.cleaned_data['directory'],
        course = self.cleaned_data['course'],
        is_public = self.cleaned_data['is_public'],
        is_active = True,
        is_deleted = False
    )
    pr.save()
    
    pr.programmers = self.cleaned_data['partners']
    pr.programmers.add(user)


class AddPartnerForm(forms.Form):
  partners = pear_fields.ModelHasManyField(
      label="Partners",
      required=False,
      model=pear.accounts.models.PearUser,
      obj_name='partner',
      url='/accounts/ajax/usersearch/?')
  project = forms.CharField('Project Name', required=True)
  
  def save(self, user):
    pr = Project.objects.get(name__exact=self.cleaned_data['project'])
    pr.programmers = self.cleaned_data['partners']
    pr.programmers.add(user)


class InviteUserForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', required=False)
  
  def clean_email(self):
    """Validates that no user already exists with this email address."""
    try:
      user = auth_models.User.objects.get(email__exact=self.cleaned_data['email'])
    except auth_models.User.DoesNotExist:
      return self.cleaned_data['email']
    raise forms.ValidationError('This email address is already registered.  '
                                'This person must already have a Pairgramming '
                                'account.')
  
  def save(self):
    # Send an email to the person
    dict = {"email": self.cleaned_data['email'],
            "fname": self.cleaned_data['first_name'],}
    emailer.send_mail(self.cleaned_data['email'], 'Pairgramming is awesome',
                            'Hey, you should register a Pairgramming account by going to OUR WEB SITE!')