"""
DJANGO SNIPPET #319

To function this requires the following to be installed:

TEMPLATE_CONTEXT_PROCESSORS
django.core.context_processors.request

MIDDLEWARE_CLASSES
django.contrib.sessions.middleware.SessionMiddleware

Usage:
Do something like this in your view ..
>>>request.session['flash_msg'] = 'Your changes have been save'
>>>request.session['flash_params'] = {'type': 'success'}

And maybe put something like this in your template:
{% load flash %}
{% flash %}
  <h2>{{ params.type }}</h2>
  {{ msg }}
{% endflash %}

@author: Robert Conner (rtconner)
"""

# Django modules
from django import template
from django.conf import settings
from django.contrib.sessions import models

# Python modules
import datetime


register = template.Library()


def session_clear(session):
  """Private function, clear flash msgsfrom the session."""
  try:
    del session['flash_msg']
  except KeyError:
    pass
  
  try:
    del session['flash_params']
  except KeyError:
    pass
  
  # Save changes to session
  if(session.session_key):
    cookie_duration = datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)
    models.Session.objects.save(
        session.session_key, session._session,
        datetime.datetime.now() + cookie_duration)


class RunFlashBlockNode(template.Node):
  def __init__(self, nodelist):
      self.nodelist = nodelist
      
  def render(self, context):
    session = context['request'].session
    ret = None
    if session.get('flash_msg', False):
      ret = {'msg': session['flash_msg']}
      if 'flash_params' in session:
        ret['params'] = session.get('flash_params', False)
        ret['autoescape'] = False
      session_clear(session);
        
    if ret is not None:
      return self.nodelist.render(template.Context(ret))
    return ''


class RunFlashTemplateNode(template.Node):
  def __init__(self):
    pass
  
  def render(self, context):
    session = context['request'].session
    if session.get('flash_msg', False):
      ret = {'msg': session['flash_msg']}
      if 'flash_params' in session:
        ret['params'] = session.get('flash_params', False)
          
      session_clear(session);
      try:
        template = settings.FLASH_TEMPLATE
      except AttributeError:
        template = 'elements/flash.html'
      t = template.load_template(template)
      return t.render(template.Context(ret)) 
    return ''


@register.tag(name="flash_template")
def do_flash_template(parser, token):
  """Call template if there is flash message in session.
      
  Runs a check if there is a flash message in the session.
  If the flash message exists it calls settings.FLASH_TEMPLATE
  and passes the template the variables 'msg' and 'params'.
  Calling this clears the flash from the session automatically
  
  To set a flash msg, in a view call:
  request.session['flash_msg'] = 'sometihng'
  request.session[flash_'params'] = {'note': 'remember me'}
  
  In the template {{ msg }} and {{ params.note }} are available
  """
  return RunFlashTemplateNode()


@register.tag(name="flash")
def do_flash_block(parser, token):
  """
  A block section where msg and params are both available.
  Calling this clears the flash from the session automatically
  
  If there is no flash msg, then nothing inside this block
  gets rendered
  
  Example:
  {% flash %}
      {{msg}}<br>
      {{params.somekey}}
  {% endflash %}
  """
  nodelist = parser.parse(('endflash',))
  parser.delete_first_token()
  return RunFlashBlockNode(nodelist)