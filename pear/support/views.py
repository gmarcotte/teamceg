from django import http
from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import decorators as auth_decorators
from django.contrib.auth import models as auth_models
from django.core import exceptions
from django.db import models
from django.views.decorators import cache

from pear.core import emailer


def help(request):
  return shortcuts.render_to_response(
      'global/support/help.html', {},
      context_instance=template.RequestContext(request)
  )

def faq(request):
  return shortcuts.render_to_response(
      'global/support/faq.html', {},
      context_instance=template.RequestContext(request)
  )
  