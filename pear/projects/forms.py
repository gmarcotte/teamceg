from django import forms
from django.template import loader, Template

import pear.projects.models

class NewProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False)
  directory = forms.CharField('Directory', required=False)
  programmers = forms.CharField('Programmers names', required=False)
  course = forms.CharField('Course Affiliation', required=False)
  
  def save(self):
    # Create the new project
    pr = pear.projects.models.Project(
        name = self.cleaned_data['name'],
        description = self.cleaned_data['description'],
        directory = self.cleaned_data['directory'],
        #nEED tO aDD pROGRAMMERS
        #nEED tO aDD rEPOS
        #nEED tO aDD cOURSE
    )
    pr.save()