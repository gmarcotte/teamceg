from django.db import models
from django.conf import settings

from pear.core import timestamp
import pear.accounts.models

if settings.USE_PEXPECT:
  import pexpect
import sys


class SSHConnection(timestamp.TimestampedModel):
  server = models.CharField(max_length=50)
  user_name = models.CharField(max_length=30)
  user = models.ForeignKey(pear.accounts.models.PearUser, related_name='servers')
  num_active = models.IntegerField()
  has_valid_keys = models.BooleanField()
  
  def __unicode__(self):
    return '%s@%s' % (self.user_name, self.server)
  
  ########### URL Mapping Methods ###############
  def get_delete_url(self):
    return '/remote/servers/%d/delete/' % self.id
  
  def get_refresh_url(self):
    return '/remote/servers/%d/refresh/' % self.id
  
  def get_clear_url(self):
    return '/remote/servers/%d/clear/' % self.id  
  
  ########## Connection Methods #################
  def connect(self):
    """Initiate an SSH connection to this server.  Returns a pExpect
    object that must be kept alive until the connection is closed.
    """
    if settings.USE_PEXPECT:
      key_file = self.user.profile.get_private_file()
      login = "ssh -i "+ key_file + " " + self.user_name + "@" + self.server
      session = pexpect.spawn(login)
      self.num_active += 1
      self.save()
      return session
    else:
      return None
    
  def execute(self, session, command):
    """Execute a remote command over ssh, and return the response.
    Args:
      session: The pExpect object returned when initializing the connection.
      command: The command to run on the remote server
    
    Returns:
      The output of running the command on the remote server.
    """
    if settings.USE_PEXPECT:
      session.sendline(command)
      resp = session.read_nonblocking(size=2000, timeout=10)
      return resp + session.read_nonblocking(size=2000, timeout=10)
    else:
      return ''
  
  def send_control(self, session, control):
    """Send a control character to the remote server.
    Args:
      session: The pExpect object returned when initializing the connection.
      command: The control character to send.
    
    Returns:
      The output of sending the control character to the remote server.
    """
    if settings.USE_PEXPECT:
      session.sendcontrol(control)
      resp = session.read_nonblocking(size=2000, timeout=10)
      return resp + session.read_nonblocking(size=2000, timeout=10)
  
  def close(session):
    """Close an SSH session to a remote server.
    Args:
      session: The pExpect object returned when initializing the connection.
    """
    session.sendline('exit')
    session.close()
    self.num_active -= 1
    self.save()
  
  
  ########## Authentication Methods #############
  def clear_remote_keys(self):
    """Removes the RSA keys from the server, so that we can no
    longer log in to their account.
    """
    if settings.USE_PEXPECT:
      cat = "cat " + self.user.profile.get_public_file()
      listener = pexpect.spawn(cat)
      pub_key = listener.read(800)
      
      session = self.connect()
      self.execute(session, 'cd .ssh')
      self.execute(session, 'rm -f authorized_keys')
      self.close(session)
      self.has_valid_keys = False
      self.save()
      return True
    return False
  
  def set_remote_keys(self, password):
    """Sets the RSA key for the user on the server. The plaintext
    password must be given as an argument, raising a potential security risk.
    """
    if settings.USE_PEXPECT:
      cat = "cat " + self.user.profile.get_public_file()
      listener = pexpect.spawn(cat)
      pub_key = listener.read(800)
      login = "ssh " + self.username + "@" + self.server
      ssh = pexpect.spawn(login)
      ssh.expect(':')
      ssh.sendline(password)
      ssh.sendline('cd .ssh')
      ssh.sendline('rm -f authorized_keys')
      ech = "echo '" + pub_key + "' > authorized_keys"
      ssh.sendline(ech)
      ssh.sendline('exit')
      ssh.close()
      self.has_valid_keys = True
      self.save()
      return True
    return False