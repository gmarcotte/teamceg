"""Custom fields with general application to DP2007 forms."""

__author__ = ["Chris Chan (ckctwo@princeton.edu)",
              "Garrett Marcotte (marcotte@princeton.edu)"]

# Django Modules
from django.forms import fields
from django.core import exceptions

# Pear Modules
from pear.core.forms import widgets as pear_widgets


class ModelHasManyField(fields.Field):
  def __init__(self, model, obj_name, url, *args, **kwargs):
    self.model = model
    self.widget = pear_widgets.ModelHasManyWidget(url=url, 
                                                  obj_name=obj_name, 
                                                  model=model)
    super(ModelHasManyField, self).__init__(*args, **kwargs)
  
  def clean(self, value):
    """
    Returns a list of the model objects associated with the ids in this field.
    """
    if isinstance(value, basestring) and value: 
      value = value.split(',')
    if value:
      return self.model.objects.filter(id__in=value)
    else:
      return []
    

class ModelHasOneField(fields.Field):
  def __init__(self, model, obj_name, url, *args, **kwargs):
    self.model = model
    self.widget = pear_widgets.ModelHasOneWidget(url=url,  
                                                 model=model)
    super(ModelHasOneField, self).__init__(*args, **kwargs)
  
  def clean(self, value):
    """
    Returns the model object associated with the id in this field.
    """
    if value:
      try:
        return self.model.objects.get(pk=value)
      except exceptions.ObjectDoesNotExist:
        return None
    else:
      return None