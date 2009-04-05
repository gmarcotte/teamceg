from django import forms

import pear.accounts.models
import pear.projects.models
from pear.projects.models import Project
from pear.core.forms import fields as pear_fields

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
  
  def save(self, user):
    # Create the new project
    pr = pear.projects.models.Project(
        name = self.cleaned_data['name'],
        description = self.cleaned_data['description'],
        directory = self.cleaned_data['directory'],
        course = self.cleaned_data['course'],
        #nEED tO aDD rEPOS
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