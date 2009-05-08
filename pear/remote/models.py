from django.db import models
from django.conf import settings

from pear.core import timestamp
import pear.accounts.models

if settings.USE_PEXPECT:
  import pexpect
import sys

class AvailableSSHManager(models.Manager):
  """A custom manager to only get SSH connections that have valid RSA keys installed."""
  def get_query_set(self):
    return super(
        AvailableSSHManager, self).get_query_set().filter(has_valid_keys=True)


class SSHConnection(timestamp.TimestampedModel):
  server = models.CharField(max_length=50)
  user_name = models.CharField(max_length=30)
  user = models.ForeignKey(pear.accounts.models.PearUser, related_name='servers')
  num_active = models.IntegerField()
  has_valid_keys = models.BooleanField()
  base_dir = models.CharField(max_length=100, blank=True)
  
  active_servers = AvailableSSHManager()
  objects = models.Manager()
  
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
      resp = self.read_output(session)
      # If the SSH prompts for a password, then our connection failed
      if resp.find("Password:") >= 0:
        session.close()
        return None
      self.num_active += 1
      self.save()
      return session
    else:
      return None
    
  def read_output(self, session):
    if settings.USE_PEXPECT:
      txt = ''
      while(True):
        try:
          txt += session.read_nonblocking(timeout=1)
        except:
          break
      return txt
    return ''

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
      resp = self.read_output(session)
      lines = resp.split('\n')
      resp = '\n'.join(lines[1:-1])
      return resp
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
      resp = self.read_output(session)
      lines = resp.split('\n')
      resp = '\n'.join(lines[1:-1])
      return resp

  def close(self, session):
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
      session = self.connect()
      if session:
        resp = self.execute(session, 'rm -f .ssh/authorized_keys')
        self.close(session)
        raise Exception(resp)

    # See if clearing worked
    session = self.connect()
    if session:
      self.has_valid_keys = True
      self.save()
      self.close(session)
      return False
    else:
      self.has_valid_keys = False
      self.save()
      return True

  def set_remote_keys(self, password):
    """Sets the RSA key for the user on the server. The plaintext
    password must be given as an argument, raising a potential security risk.
    """
    if settings.USE_PEXPECT:
      pub_key = open(self.user.profile.get_public_file(), 'r').read().strip()
      login = 'ssh %s "echo %s >> .ssh/authorized_keys"' % (self, pub_key)
      ssh = pexpect.spawn(login)
      ssh.expect(':')
      ssh.sendline('yes')
      ssh.expect(':')
      ssh.sendline(password)
      ssh.close()
          
    # See if setting worked
    session = self.connect()
    if session:
      self.has_valid_keys = True
      self.save()
      self.close(session)
      return False
    else:
      self.has_valid_keys = False
      self.save()
      return True