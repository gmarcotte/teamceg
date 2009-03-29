from django import forms
from django.template import loader
from django.contrib.auth import models as auth_models
from django.contrib import auth

import pear.accounts.models
import pear.accounts.util


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
                                'Please choose another.')
      
  def save(self):
    # Create the new user
    # The authentication library did not like what we were doing before, so
    # this has been changed CCI
    password = auth_models.User.objects.make_random_password()
    username = pear.accounts.util.make_username_from_email(self.cleaned_data['email'])
    u = auth_models.User.objects.create_user(username,'junk@addr.com',password)
    u.first_name = self.cleaned_data['first_name']
    u.last_name = self.cleaned_data['last_name']
    u.email = self.cleaned_data['email']
    u.save()
    
    # Create a profile for the new user
    p = pear.accounts.models.Profile(
        class_year = self.cleaned_data['class_year'],
        major = self.cleaned_data['major'],
        user = u
    )
    p.save()
    
    # TODO: Send an email to the user


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