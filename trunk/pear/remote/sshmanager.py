#
#  sshmanager.py
#  sandbox
#
#  Created by Christina Ilvento on 4/4/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django.conf import settings
if settings.USE_PEXPECT:
  import pexpect
import sys

# does a test login  
def ssh_login(username, server, key_file, command = ''):
  if settings.USE_PEXPECT:
    login = "ssh -i "+ key_file + " " + username + "@" + server
    ssh = pexpect.spawn(login)
    #ssh.interact()
    response = ssh.read_nonblocking(size=10000, timeout=10)
    ssh.sendline(command)
    response + ssh.read_nonblocking(size=2000,timeout=10)
    return [ssh, response + ssh.read_nonblocking(size=2000,timeout=10)]


def ssh_command(session, command=''):
  if settings.USE_PEXPECT:
    session.sendline(command)
    resp = session.read_nonblocking(size=3, timeout=10)
    #resp = session.read_nonblocking(size=2000,timeout=10)
    #resp = resp + session.read_nonblocking(size=2000,timeout=10)
    #resp = resp + session.read_nonblocking(size=2000,timeout=10)
    #resp = resp + session.read_nonblocking(size=2000,timeout=10)
    return [session, resp + session.read_nonblocking(size=2000, timeout=10)]
    
def ssh_close(session):
  session.sendline('exit')
  session.close()