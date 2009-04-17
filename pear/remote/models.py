from django.db import models

from pear.core import timestamp
import pear.accounts.models

class SSHConnection(timestamp.TimestampedModel):
  server = models.CharField(max_length=50) # the server name
  user_name = models.CharField(max_length=30) # the specific user name for this server
  user = models.ForeignKey(pear.accounts.models.PearUser, related_name='servers')
  
  def __unicode__(self):
    return '%s@%s' % (self.user_name, self.server)

