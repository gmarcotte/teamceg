#accounts: models.py
#CCI: 3/27/09
from django.db import models
from django.contrib.auth import models as auth_models

class Profile(models.Model):
  major = models.CharField(max_length=30)
  class_year = models.CharField(max_length=30)
  user = models.ForeignKey(auth_models.User, related_name='profile')
  
  def __unicode__(self):
    return str(self.major) + str(self.class_year)