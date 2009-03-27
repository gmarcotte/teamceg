from django import forms
from django.template import loader
from django.contrib.auth import models as auth_models

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
    password = auth_models.User.objects.make_random_password()
    
    u = auth_models.User(
        email = self.cleaned_data['email'],
        first_name = self.cleaned_data['first_name'],
        last_name = self.cleaned_data['last_name'],
        username = pear.accounts.util.make_username_from_email(self.cleaned_data['email']),
        password = password
    )
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
  email = forms.EmailField('E-Mail Address')
  password = forms.CharField('Password')