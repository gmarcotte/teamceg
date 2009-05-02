from django import forms
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django.conf import settings

from pear.accounts import models as accounts_models
import pear.accounts.util
from pear.core import emailer


class InviteUserForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', required=False)
  
  def clean_email(self):
    """Validates that no user already exists with this email address."""
    try:
      user = accounts_models.PearUser.objects.get(email__exact=self.cleaned_data['email'])
    except accounts_models.PearUser.DoesNotExist:
      return self.cleaned_data['email']
    raise forms.ValidationError('This email address is already registered.  '
                                'This person must already have a Pairgramming '
                                'account.')
  
  def save(self):
    # Send an email to the person
    dict = {"email": self.cleaned_data['email'],
            "fname": self.cleaned_data['first_name'],}
    emailer.send_mail(self.cleaned_data['email'], 
                      'Pairgramming is awesome',
                      ('Hey, you should register a Pairgramming account by '
                       'going to OUR WEB SITE!'))
    
    
class RegistrationForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', required=False)
  last_name = forms.CharField('Last Name', required=False)
  class_year = forms.CharField('Class Year', required=False)
  major = forms.CharField('Major', required=False)
  
  def clean_email(self):
    """Validates that no user already exists with this email address."""
    try:
      user = auth_models.User.objects.get(email__exact=self.cleaned_data['email'])
    except auth_models.User.DoesNotExist:
      return self.cleaned_data['email']
    raise forms.ValidationError('This email address is already registered.  '
                                'Please choose another, or try to login '
                                'with the link below.')
      
  def save(self):
    # Create the new user
    # The authentication library did not like what we were doing before, so
    # this has been changed CCI
    
    password = auth_models.User.objects.make_random_password()
    username = pear.accounts.util.make_username_from_email(self.cleaned_data['email'])
    u = auth_models.User()
    u.first_name = self.cleaned_data['first_name']
    u.last_name = self.cleaned_data['last_name']
    u.email = self.cleaned_data['email']
    u.username = username
    u.set_password(password)
    u.save()
    
    # Create a profile for the new user
    p = pear.accounts.models.Profile(
        class_year = self.cleaned_data['class_year'],
        major = self.cleaned_data['major'],
        user = u
    )
    p.save()
    
    p.refresh_keys()
    
    # Send an email to the user
    dict = {"email": u.email, 
            "password": password, 
            "lname": u.last_name, 
            "fname": u.first_name, 
            "year": p.class_year, 
            "major": p.major}
    try:
      emailer.render_and_send(u.email,
                              'Thank you for registering with Pairgramming!',
                              'emails/registration_confirm.txt', dict)
      return True
    except:
      p.delete()
      u.delete()
      return False
      

class LoginForm(forms.Form):
  email = forms.EmailField(
      'E-Mail Address',
      widget = forms.TextInput(attrs={'size': '20'}))
  
  password = forms.CharField(
      'Password',
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  def clean(self):
    user = auth.authenticate(username=self.cleaned_data['email'],
                             password=self.cleaned_data['password'])
    if not user:
      raise forms.ValidationError(
            'That email/password combination was not recognized.  Please try'
            ' again or reset your password by clicking on the link below.')
    else:
      self.cleaned_data['user'] = user
    return self.cleaned_data
  

class PasswordResetForm(forms.Form):
  email = forms.EmailField(
      'E-Mail Address',
      widget = forms.TextInput(attrs={'size': '20'}))
  
  def clean_email(self):
    users = auth_models.User.objects.filter(email__exact = self.cleaned_data['email'])
    if users:
      return self.cleaned_data['email']
    else:
      raise forms.ValidationError(
          'That email address has not been registered.  Please try another '
          'address or click on the link below to register a new account.')
      
  def save(self):
    user = auth_models.User.objects.get(email__exact = self.cleaned_data['email'])
    new_password = auth_models.User.objects.make_random_password()
    user.set_password(new_password)
    user.save()
    
    dict = {"email": self.cleaned_data['email'], 
            "password": new_password}
    emailer.render_and_send(self.cleaned_data['email'],
                            'Your new Pairgramming password',
                            'emails/reset_password.txt', 
                            dict)
    

class PasswordChangeForm(forms.Form):
  old_password = forms.CharField(
      'Current Password',
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  new_password = forms.CharField(
      'New Password',
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  new_password_confirm = forms.CharField(
      'Confirm New Password',
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  def __init__(self, user, *args, **kwargs):
    self.user = user
    super(PasswordChangeForm, self).__init__(*args, **kwargs)
  
  def clean_old_password(self):
    """Validate that the user entered the correct current password."""
    if not self.user.check_password(self.cleaned_data['old_password']):
      raise forms.ValidationError(
          'Incorrect Password.  Please try again or click the link below '
          'to reset your password.')
    return self.cleaned_data['old_password']
  
  def clean(self):
    """Validates that the user entered the same password in both boxes."""
    if not (self.cleaned_data['new_password'] == self.cleaned_data['new_password_confirm']):
      raise forms.ValidationError(
           'The new passwords did not match. Please try again.')
    return self.cleaned_data
  
  def save(self):
    self.user.set_password(self.cleaned_data['new_password'])
    self.user.save()
    
    emailer.render_and_send(self.user.email,
                            'Your Pairgramming password has been changed',
                            'emails/change_password.txt', {})   