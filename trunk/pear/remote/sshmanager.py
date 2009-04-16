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

# does a login  
# ie username = cilvento
#    server = hats.princeton.edu
#    key_file = /usr/cilvento/mykey  (the PRIVATE key, not the .pub)
#    command = ''  (this is optional, and just executes immediately)
def ssh_login(username, server, key_file, command = ''):
  if settings.USE_PEXPECT:
    login = "ssh -i "+ key_file + " " + username + "@" + server
    ssh = pexpect.spawn(login)
    response = ssh.read_nonblocking(size=10000, timeout=10)
    ssh.sendline(command)
    response = response + ssh.read_nonblocking(size=2000,timeout=10)
    return [ssh, response + ssh.read_nonblocking(size=2000,timeout=10)]

# execute a remote command over ssh, and get back the response from the remote host 
# ie session = whatever you got back from ssh_login()
#    command = 'ls'  (no need to append newline)
def ssh_command(session, command=''):
  if settings.USE_PEXPECT:
    session.sendline(command)
    resp = session.read_nonblocking(size=2000, timeout=10)
    return [session, resp + session.read_nonblocking(size=2000, timeout=10)]

# sends a control character
# ie session = whatever you got back from ssh_login()
#    control='c'   the control character you want to execute
def ssh_control(session, control=''):
  if settings.USE_PEXPECT:
    session.sendcontrol(control)
    resp = session.read_nonblocking(size=2000, timeout=10)
    return [session, resp + session.read_nonblocking(size=2000, timeout=10)]

# close an ssh session    
def ssh_close(session):
  session.sendline('exit')
  session.close()