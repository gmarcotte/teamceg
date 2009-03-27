#accounts: models.py
#CCI: 3/27/09
from django.db import models

class profile(models.Model):
  major = models.CharField(max_length=30)
  classyr = models.CharField(max_length=30)
  
  def __unicode__(self):
    stri = str(self.major) + str(self.classyr)
    return stri