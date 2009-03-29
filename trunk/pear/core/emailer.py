#
#  emailer.py
#  sandbox
#
#  Created by Christina Ilvento on 3/28/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#

import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Encoders import encode_base64

from django.template import loader, Template

def render_and_send(recipient, subject, template, dictionary):
"""Sends mail to the specified account with the given template and dictionary 
   and subject line.
"""
  text = loader.render_to_string(template, dictionary)
  send_mail(recipient, subject, text)

# send mail from pairgramming@gmail.com, text should already be 
# rendered if you use this function
def send_mail(recipient, subject, text):
  """Sends mail to the specified account.    
  """
  gmailUser = 'pairgramming@gmail.com'
  gmailPassword = 'weheartbwk'

  msg = MIMEMultipart()
  msg['From'] = gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))

  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()