import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Encoders import encode_base64

from django.template import loader
from django.conf import settings

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
  if settings.ENABLE_EMAIL:
    gmailUser = settings.EMAIL_USER
    gmailPassword = settings.EMAIL_PASSWORD
    gmailServer = settings.EMAIL_SERVER
    gmailPort = settings.EMAIL_PORT
  
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
  
    mailServer = smtplib.SMTP(gmailServer, gmailPort)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()