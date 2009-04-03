"""Base class for all models that adds basic timestamp information."""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']

from django.db import models


class TimestampedModel(models.Model):
  class Meta:
    abstract = True
    
  created_at = models.DateTimeField(editable=False, auto_now_add=True)
  updated_at = models.DateTimeField(editable=False, auto_now=True)
  update_count = models.IntegerField(editable=False, default=0)
  
  def save(self):
    self.update_count += 1
    super(TimestampedModel, self).save()