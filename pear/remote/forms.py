from django import forms

import pear.remote.models


class ServerAddForm(forms.Form):
  server = forms.CharField(
      'Server Name (ie hats.princeton.edu)',
      widget = forms.TextInput(attrs={'size': '40'}))
  user_name = forms.CharField(
      'Username on server',
      widget = forms.TextInput(attrs={'size': '20'}))
  base_dir = forms.CharField(
      'Base Directory',
      help_text = "The top-level directory for storing all Pairgramming projects.",
      widget=forms.TextInput(attrs={'size': '20'}))
      
  password = forms.CharField(
      'Password',
      required=False,
      help_text=("We never store your password in any way. Read more about our "
                 "password policy below"),
      widget = forms.PasswordInput(attrs={'size': '20'}))
  
  def save(self, u):
    new_serv = pear.remote.models.SSHConnection(
        server = self.cleaned_data['server'],
        user_name = self.cleaned_data['user_name'],
        base_dir = self.cleaned_data['base_dir'],
        num_active = 0,
        has_valid_keys = False,
        user = u)
    new_serv.has_valid_keys = new_serv.set_remote_keys(self.cleaned_data['password'])
    new_serv.setup_base_dir()
    new_serv.save()