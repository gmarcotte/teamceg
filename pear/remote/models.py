from django.db import models
from django.conf import settings

from pear.core import timestamp
import pear.accounts.models

import os
import paramiko
import time

class SSHConnection(timestamp.TimestampedModel):
  server = models.CharField(max_length=50)
  user_name = models.CharField(max_length=30)
  user = models.ForeignKey(pear.accounts.models.PearUser, related_name='servers')
  num_active = models.IntegerField()
  has_valid_keys = models.BooleanField()
  base_dir = models.CharField(max_length=100, blank=True)
  
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
    """Initiate an SSH connection to this server.  Returns a paramiko
    object that must be kept alive until the connection is closed.
    """
    key_file = self.user.profile.get_private_file()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      client.connect(
          hostname = self.server,
          username = self.user_name,
          key_filename = key_file)
    except:
      return None
    client.exec_command('cd %s' % self.base_dir)
    self.num_active += 1
    self.save()
    return client

  def execute(self, client, command):
    """Execute a remote command over ssh, and return the response.
    Args:
      client: The paramiko object returned when initializing the connection.
      command: The command to run on the remote server

    Returns:
      A 2-tuple, with the first entry indicating the success of the command.
      True indicates the response is from stdout, False indicates the
      response is from stderr.  The second entry is the response
      from the server.
    """
    stdin, stdout, stderr = client.exec_command(command)
    out_resp = stdout.read()
    err_resp = stderr.read()
    if err_resp:
      return (False, err_resp)
    else:
      return (True, out_resp)
  
  def close(self, client):
    """Close an SSH session to a remote server.
    Args:
      session: The paramiko object returned when initializing the connection.
    """
    client.close()
    self.num_active -= 1
    self.save()  
  
  ########## Authentication Methods #############
  def clear_remote_keys(self):
    """Removes the RSA keys from the server, so that we can no
    longer log in to their account.
    """
    client = self.connect()
    if client:
      resp = self.execute(client, 'rm -f ~/.ssh/authorized_keys')
      self.close(client)

    # See if clearing worked
    client = self.connect()
    if client:
      self.has_valid_keys = True
      self.save()
      self.close(client)
      return False
    else:
      self.has_valid_keys = False
      self.save()
      return True

  def set_remote_keys(self, password):
    """Sets the RSA key for the user on the server. The plaintext
    password must be given as an argument, raising a potential security risk.
    """
    pub_key = open(self.user.profile.get_public_file(), 'r').read().strip()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      client.connect(
          hostname = self.server,
          username = self.user_name,
          password = password)
      client.exec_command('echo %s >> ~/.ssh/authorized_keys' % (pub_key))
      client.close()
    except:
      pass
    
    time.sleep(.5)
    # See if setting worked
    session = self.connect()
    if session:
      self.has_valid_keys = True
      self.save()
      self.close(session)
      return True
    else:
      self.has_valid_keys = False
      self.save()
      return False
    
  # Common remote operations
  def get_relative_filename(self, filepath):
    return os.path.normcase(os.path.normpath(os.path.join(self.base_dir, filepath)))
  
  def save_file(self, session, filename, string=''):   
    filepath = self.get_relative_filename(filename)
    self.execute(session, 'rm -f %s' % filepath)
    for line in string.split('\n'):
      self.execute(session, "echo '%s' >> %s" % (line, filepath))
    resp = self.execute(session, 'cat %s' % filepath)
    return resp
  
  def make_directory(self, session, dirname):
    dirpath = self.get_relative_filename(dirname)
    resp = self.execute(session, 'mkdir -p -v %s' % dirpath)
    return resp
  
  def load_file(self, session, filename):
    filepath = self.get_relative_filename(filename)
    resp = self.execute(session, 'cat %s' % filepath)
    return resp
  
  def read_file_tree(self, session, root_dir):
    dirpath = self.get_relative_filename(root_dir)
    cmd = 'find %s -ls' % dirpath
    status,output = self.execute(session, cmd)
    lines = output.strip().split('\n')
    tree = []
    for line in lines:
      bits = line.split()
      perms = bits[2]
      file = bits[10]
      if file.find('.svn') > 0:
        continue
      file = file.lstrip(dirpath)
      file_bits = file.split('/')
      depth = len(file_bits)
      if perms[0] == 'd':
        tag = 'dir'
      else:
        tag = 'file'
      tree.append(("%d%s" % (depth, file_bits[-1]), tag, file.lstrip(root_dir)))      
    return tree
  
  def delete_file(self, session, filename):
    filepath = self.get_relative_filename(filename)
    resp = self.execute(session, 'rm -f %s' % filepath)
    return resp
    
  def svn_add(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn add %s' % fullpath
    self.execute(session, cmd)
    return resp
  
  def svn_checkout(self, session, repos, working_copy):
    dirpath = self.get_relative_filename(working_copy)
    cmd = 'svn co %s %s' % (repos, dirpath)
    resp = self.execute(session, cmd)
    return resp
  
  def svn_update(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn update %s' % fullpath
    resp = self.execute(session, cmd)
    return resp
  
  def svn_delete(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn delete %s' % fullpath
    status,text = self.execute(session, cmd)
    if not status:
      return (status, text)
    cmd = 'svn commit %s -m "Deleting %s"' % (fullpath, filepath)
    resp = self.execute(session, cmd)
    return resp
  
  def svn_test(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn status %s' % fullpath
    status,text = self.execute(session, cmd)
    return status
  
  def svn_revert(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn revert %s' % fullpath
    resp = self.execute(session, cmd)
    return resp
  
  def svn_commit(self, session, filepath):
    fullpath = self.get_relative_filename(filepath)
    cmd = 'svn commit %s -m "Saving changes to %s"' % (fullpath, filepath)
    resp = self.execute(session, cmd)
    return resp
    