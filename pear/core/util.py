"""Utility functions for use across the pear codebase."""

from django.db.models.fields import related as related_fields
from django.db.models.fields import files

import re


def make_get_string(get_data):
  return '?%s' % '&'.join(['%s=%s' % (key, value) for (key, value) in get_data.iteritems()])


def instance_dict(instance, key_format=None):
  """Determine field names and values for a given object instance.
  
  Note: From Django Snippet #199 (www.djangosnippets.org)
  
  Args:
    instance: An instance of a class.
    key_format: A string, indicating a special way of formatting the keys
        of the dictionary. This string must contain a %s to indicate the
        location of the name of each field.  The default is "%s".  
        For example, for instance of a "parrot" class, you might use:
          key_format = "parrot_%s"
          field.name = "species"
          field.value = "Norwegian Blue"
        Then the return dictionary would have an entry:
          {'parrot_species': 'Norwegian Blue'}
  
  Returns:
    A dictionary whose key/value pairs are the (optionally formatted) field
    names and values of the given class instance.
  
  Raises:
    ValueError: The given key_format parameter doesn't contain a "%s" string.           
  """
  if key_format:
    if not '%s' in key_format:
      raise ValueError('key_format must contain a %s')
  key = lambda key: key_format and key_format % key or key

  d = {}
  for field in instance._meta.fields:
    attr = field.name
    value = getattr(instance, attr)
    if value and isinstance(field, related_fields.ForeignKey):
      value = value._get_pk_val()
    if value and (isinstance(field, files.ImageField) or isinstance(field, files.FileField)):
      value = value.path
    d[key(attr)] = value
  for field in instance._meta.many_to_many:
    d[key(field.name)] = [obj._get_pk_val() for obj 
                          in getattr(instance, field.attname).all()]
  return d


def instance_file_dict(instance):
  """Build dictionary for the File and Image Fields in forms.
  
  Args:
    instance: A Form instance.
  
  Returns:
    A dictionary whose keys are the names of FileField or ImageField fields
    in the form, and whose values are the filename and filecontents of
    those fields. 
  """
  
  d = {}
  for field in instance._meta.fields:
    attr = field.name
    value = getattr(instance, attr)
    
    if value and (isinstance(field, files.ImageField) 
                  or isinstance(field, files.FileField)):
      filepath = eval('instance.%s.path' % field.name)
      file = open(filepath, 'rb')
      contents = file.read()
      file.close()
      
      content_type = 'application/octet-stream'
      
      filename = re.compile(r'^(\d{8})-').sub('', os.path.basename(filepath))
      d[field.name] = uploadedfile.SimpleUploadedFile(filename, 
                                                      contents,
                                                      content_type)
  return d