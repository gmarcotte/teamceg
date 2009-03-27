"""Authenticates by email rather than username."""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

# Django Modules
from django.contrib.auth import backends
from django.contrib.auth import models
from django.forms import fields


class BasicBackend(backends.ModelBackend):
  def get_user(self):
    try:
      return models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
      return None


class EmailBackend(BasicBackend):
  def authenticate(self, username=None, password=None):
    if fields.email_re.search(username):
      try:
        user = models.User.objects.get(email=username)
      except models.User.DoesNotExist:
        return None
    
    if user.check_password(password):
      return user