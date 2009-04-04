from django import forms
from django.template import loader, Template

import pear.projects.models

class NewProjectForm(forms.Form):
  name = forms.CharField('Project Name', required=True)
  description = forms.CharField('Project Description', required=False)
    # it doesn't like TextField for description for some reason?
  directory = forms.CharField('Directory', required=False)
  programmers = forms.CharField('Programmers\' names', required=False)
  course = forms.CharField('Course Affiliation', required=False)

  def save(self):
    # Create the new project
    pr = pear.projects.models.Project(
        name = name,
        description = description,
        directory = directory,
        programmers = None,
        repos = '',
        course = course
    )
    pr.save()