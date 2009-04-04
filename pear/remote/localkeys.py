#
#  localkeys.py
#  sandbox
#
#  Created by Christina Ilvento on 4/3/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#

# generates the RSA key pair for the user to use
import pexpect
import sys

# create the keys
# returns the name of the public key file generated
def create_keys(keyfile):
  local = pexpect.spawn('ssh-keygen -t dsa')
  # all of the expects are what we actually see from the console.
  # if these need to be changed, it will probably be minimal
  local.expect('Generating public/private dsa key pair.')
  # the filename for the key
  local.expect(':')
  local.sendline(keyfile)
  # makes sure that we over-write if already present
  local.sendline('y')
  # the passcode, this will be blank
  local.expect(':')
  local.sendline('')
  # passcode confirmation, also blank
  local.expect(':')
  local.sendline('')
  return keyfile + ".pub"
  
# Sets the RSA key for the user on the server. Their plaintext
# password must be given as an argument, or the user can do it
# him/herself. The pub_key_file name will be returned by
# create_keys  
def set_remote_keys(username, password, server, pub_key_file):
  cat = "cat " + pub_key_file
  listener = pexpect.spawn(cat)
  pub_key = listener.read(800)
  #return stringy
  # do stuff to pubkey to strip off stuff at the end...
  pub_key
  login = "ssh " + username + "@" + server
  ssh = pexpect.spawn(login)
  ssh.expect(':')
  ssh.sendline(password)
  ssh.sendline('cd .ssh')
  ssh.sendline('rm "-f" authorized_keys')
  ech = "echo '" + pub_key + "' > authorized_keys"
  ssh.sendline(ech)
  ssh.sendline('exit')
  # the interact is necessary... it's a bit magical
  ssh.interact()
  
  
# does a test login  
def test_login(username, server, key_file):
  login = "ssh -i "+ key_file + " " + username + "@" + server
  ssh = pexpect.spawn(login)
  ssh.interact()
  
# testing method  
#k = create_keys('mykey')
#print 'Created new key-set, now trying to login....'
#set_remote_keys('cilvento', '', 'hats.princeton.edu', k)  
#print 'Okay, apparently the keys have been set.... lets check!'
#test_login('cilvento', 'hats.princeton.edu', 'mykey')
