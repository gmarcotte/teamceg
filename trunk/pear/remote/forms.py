from django import forms

from pear.remote import localkeys
import pear.remote.models


class ServerAddForm(forms.Form):
  server = forms.CharField(
      'Server Name (ie hats.princeton.edu)',
      widget = forms.TextInput(attrs={'size': '40'}))
  user_name = forms.CharField(
      'Username on server',
      widget = forms.TextInput(attrs={'size': '20'}))
      
  password = forms.CharField(
      'Password',
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  def save(self, u):
    new_serv = pear.remote.models.SSHConnection(
               server = self.cleaned_data['server'],
               user_name = self.cleaned_data['user_name'],
               user = u)
    new_serv.save()
  
    
class ToyForm(forms.Form):
  server_name = forms.CharField(
      'Server Name (ie hats.princeton.edu)',
      widget = forms.TextInput(attrs={'size': '40'}))
  user_name = forms.CharField(
      'Username on server',
      widget = forms.TextInput(attrs={'size': '20'}))
  command = forms.CharField(
      'First command to execute',
      widget = forms.TextInput(attrs={'size': '100'}))
  command2 = forms.CharField(
      'Second command to execute',
      widget = forms.TextInput(attrs={'size': '100'}))
  command3 = forms.CharField(
      'Third command to execute',
      widget = forms.TextInput(attrs={'size': '100'}))
  
  def __init__(self, user, *args, **kwargs):
    self.user = user
    super(ToyForm, self).__init__(*args, **kwargs)