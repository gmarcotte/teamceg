#accounts: models.py
#CCI: 3/27/09
from django.db import models
from django.contrib.auth import models as auth_models

from pear.core import timestamp

class PearUser(auth_models.User):
  """This model is used to extend the functionality of the Django user model
  without changing the actual Django code.  We can only add methods and
  attributes here, we can't add any new database fields.s
  """
  class Meta:
    proxy = True
    
  def __unicode__(self):
    return "%s: %s" % (self.email, self.get_full_name())
  
  def get_profile(self):
    return self.profile.get()
  
  @property
  def created_at(self):
    return self.get_profile().created_at
  
  @property
  def updated_at(self):
    return self.get_profile().updated_at
  
  @property
  def update_count(self):
    return self.get_profile().update_count
  
  def save(self):
    self.get_profile().save()
    super(PearUser, self).save()


class Profile(timestamp.TimestampedModel):
  major = models.CharField(max_length=30)
  class_year = models.CharField(max_length=30)
  user = models.ForeignKey(auth_models.User, related_name='profile')
  private_key = models.CharField(max_length=500)
  public_key = models.CharField(max_length=500)
  
  def __unicode__(self):
    return str(self.major) + str(self.class_year)
  
  def get_public_key(self):
    return self.public_key