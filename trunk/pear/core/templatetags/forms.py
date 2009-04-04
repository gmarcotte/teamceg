"""Template tags that are commonly used in forms go here."""

__author__ = ['Chris Chan (ckctwo@princeton.edu)']


# Django Modules
from django import template
from django.forms import fields
from django.forms import forms
from django.utils import safestring


register = template.Library()


def print_form_css(form):
  """Prints out all css associated with form.
  
  Usage::
  
      {{ form|print_form_css }} 
  """
  
  if not isinstance(form, forms.BaseForm):
    raise template.TemplateSyntaxError(
        "'print_form_css' can only be applied to a Django form instance.")
  
  css = form.media.render_css()  # itertools.chain object
  return (safestring.mark_safe("\n".join(css)))
register.filter(print_form_css)
   

def print_form_js(form):
  """Prints out all js associated with form.
  
  Usage::    
      {{ form|print_form_js }}
  """
  if not isinstance(form, forms.BaseForm):
    raise template.TemplateSyntaxError(
        "'print_form_js' can only be applied to a Django form instance.")

  js = form.media.render_js() # itertools.chain object
  return (safestring.mark_safe("\n".join(js)))
register.filter(print_form_js) 


def print_form_row(value, arg):
  """Prints the form row associated with argument and form value.
  
  If there's a first_name field in the form, then you can use it as::
  
      {{ form|print_form_row:"first_name" }}
      
  """
  # Must have field name as an argument
  if not arg:
    raise template.TemplateSyntaxError(
        "'print_form_row' requires a field name as argument")
  
  if not isinstance(value, forms.BaseForm):
    raise template.TemplateSyntaxError(
        "'print_form_row' can only be applied to a Django form instance.")
  
  # Get field
  field = value.__getitem__(arg.strip())
  
  html = []
  form_row_classes =[]
  form_row_styles = []
  label_classes = []
  
  # Grab label classes
  if field.field.required:
    label_classes.append('required')
      
  if isinstance(field.field, fields.BooleanField):
    form_row_classes.append('checkbox-row')
    label_classes.append('vCheckboxLabel')
      
  if isinstance(field.field, fields.DateField):
     form_row_styles.append('overflow: visible;')
  
  html.append(u'<div id="%s_row_id" class="form-row %s" style="%s">' 
              % (arg.strip(), 
                 ' '.join(form_row_classes), 
                 ' '.join(form_row_styles)))
  
  if isinstance(field.field, fields.BooleanField):
    html.append(u' %s' % (field))
    html.append(u' <label class="%s" for="id_%s">%s</label>' 
                % (' '.join(label_classes), arg.strip(), field.label))
  else:
    html.append(u' <label class="%s" for="id_%s">%s</label>' 
                % (' '.join(label_classes), arg.strip(), field.label))
    html.append(u' %s' % (field))
  
  if field.help_text:
    html.append(u'<p class="help">%s</p>' % (field.help_text))
  
  if field.errors:
    html.append(u'<span class="error">%s</span>' % (field.errors))
      
  html.append(u'</div>')

  return safestring.mark_safe(''.join(html))
register.filter(print_form_row)