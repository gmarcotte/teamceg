from django import forms

import pear.accounts.models
import pear.projects.models
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