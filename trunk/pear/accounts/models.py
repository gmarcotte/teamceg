#accounts: models.py
#CCI: 3/27/09
from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

from pear.core import timestamp

import paramiko
import os
import sys


class PearUser(auth_models.User):
  """This model is used to extend the functionality of the Django user model
  without changing the actual Django code.  We can only add methods and
  attributes here, we can't add any new database fields.
  """
  class Meta:
    proxy = True
    
  def __unicode__(self):
    return "%s: %s" % (self.email, self.get_full_name())
  
  @property
  def created_at(self):
    return self.profile.created_at
  
  @property
  def updated_at(self):
    return self.profile.updated_at
  
  @property
  def update_count(self):
    return self.profile.update_count
  
# This is causing problems.  We don't really use the update/created stats
# for anything, so we don't need it here.
#  def save(self):
#    if self.profile:
#      self.profile.save()
#    super(PearUser, self).save()
    
  def delete(self):
    u = auth_models.User.objects.get(pk=self.id)
    u.delete()
        
  @property
  def current_meeting(self):
    if self.driver_for.count():
      return self.driver_for.latest('id')
    if self.passenger_for.count():
      return self.passenger_for.latest('id')
    return None
  
  # URL Accessors
  def get_key_regen_url(self):
    return '/accounts/regen_keys/'


class Profile(timestamp.TimestampedModel):
  major = models.CharField(max_length=30)
  class_year = models.CharField(max_length=30)
  user = models.OneToOneField(PearUser, related_name='profile', primary_key=True)
  
  def delete(self):
    if os.path.exists(self.get_private_file()):
      os.remove(self.get_private_file())
    if os.path.exists(self.get_public_file()):
      os.remove(self.get_public_file())
    super(Profile, self).delete()
  
  ######## RSA Key Methods ############
  def get_private_file(self):
    return "%s/%d" % (settings.RSA_KEY_DIR, self.pk)
  
  def get_public_file(self):
    return "%s.pub" % self.get_private_file()
  
  def has_keys(self):
    return (os.path.exists(self.get_private_file()) and
            os.path.exists(self.get_public_file()))
    
  def refresh_keys(self):
    """Generate a new public/private key pair for this user"""
    if os.path.exists(self.get_private_file()):
      os.remove(self.get_private_file())
    if os.path.exists(self.get_public_file()):
      os.remove(self.get_public_file())
    newkey = paramiko.RSAKey.generate(2048)
    newkey.write_private_key_file(self.get_private_file())
    pubkey = open(self.get_public_file(), 'w')
    pubkey.write('ssh-rsa %s root@%s' % (newkey.get_base64(), settings.SSH_SERVER_HOST))
    pubkey.close()