#
#  models.py
#  sandbox
#
#  Created by Christina Ilvento on 4/3/09.
#
class SSHConnection(timestamp.TimestampedModel):
  sever = models.CharField(max_length=50) # the server name
  user_name = models.CharField(max_length=30) # the specific user name for this server
  user = models.ForeignKey(auth_models.User, related_name='profile')
  
  def __unicode__(self):
    return str(self.major) + str(self.class_year)