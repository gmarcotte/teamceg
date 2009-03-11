from django.db import models

class Todo(models.Model):
  task = models.CharField(max_length=30)
  
  def __unicode__(self):
    return str(self.task)