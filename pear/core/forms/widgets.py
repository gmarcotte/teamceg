"""Custom widgets for use across dp2007 forms."""

__author__ = ["Chris Chan (ckctwo@princeton.edu)",
              "Garrett Marcotte (marcotte@princeton.edu)"]


# Django modules
from django.conf import settings
from django.forms import util
from django.forms import widgets as django_widgets
from django.utils import safestring


class ModelHasManyWidget(django_widgets.Widget):
  """Widget that AJAXifies has-many relationships selections."""
  def __init__(self, attrs=None, url="", obj_name=None, model=[]):
    self.attrs = attrs or {}
    self.attrs.update({'size': '50', 'class': 'vModelHasManyWidget', 
                       'alt': obj_name, 'src': url})
    self.obj_name = obj_name
    self.model = model

  def render(self, name, value, attrs=None):
    if value is None: 
      value = ()
    
    # We need this because value can sometimes be a string
    if isinstance(value, basestring) and value: 
      value = value.split(',')
    
    final_attrs = self.build_attrs(attrs, name=name)
    output = ['<input type="text" id="id_%ss_input" name="%ss_input" value="" %s>'
              % (self.obj_name, self.obj_name, util.flatatt(final_attrs))]
    output.append('<input type="hidden" id="id_%ss" name="%s" value="%s">' 
                  % (self.obj_name, name, ','.join(map(str, value))))
    output.append(u'<ul id="id_%ss_list" class="show_bullets">' % (self.obj_name))
    
    for obj in self.model.objects.filter(id__in=value):
        output.append(u'<li id="%s_%s">%s <a href="#" '
                      'onclick="remove_assign_id(\'%s\', \'%s\'); return false;">'
                      '[Remove]</a></li>' 
                      % (self.obj_name, obj.id, obj, self.obj_name, obj.id))
    
    output.append(u'</ul>')
    return safestring.mark_safe(u''.join(output))
  
  class Media:
    js = ("%s/js/bsn.AutoSuggest_2.1.3.js" % settings.MEDIA_URL, 
          "%s/js/AutoSuggestHasMany.js" % settings.MEDIA_URL,)
    css = {
           'all': ("%s/css/autosuggest_inquisitor.css" % settings.MEDIA_URL,
                   "%s/css/forms.css" % settings.MEDIA_URL)}