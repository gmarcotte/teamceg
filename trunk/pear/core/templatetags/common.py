"""Template tags that are commonly used across the site."""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


# Django Modules
from django import template
from django.utils import safestring

from pear.core import util

register = template.Library()

@register.simple_tag
def print_paginator_links(page, get_data):
  links = []
  if page.has_previous():
    if page.paginator.page(page.number - 1).has_previous():
      get_data['page'] = 1
      links.append('<a href="%s"> << First </a>' % util.make_get_string(get_data))
    get_data['page'] = page.number - 1
    links.append('<a href="%s"> < Previous </a>' % util.make_get_string(get_data))
  
  links.append('Viewing %s-%s of %s' % (page.start_index(), page.end_index(), page.paginator.count))
  
  if page.has_next():
    get_data['page'] = page.number + 1
    links.append('<a href="%s"> Next > </a>' % util.make_get_string(get_data))
    if page.paginator.page(page.number + 1).has_next():
      get_data['page'] = page.paginator.num_pages
      links.append('<a href="%s"> Last >> </a>' % util.make_get_string(get_data))
    
  return safestring.mark_safe(' | '.join(links))
      
      
  