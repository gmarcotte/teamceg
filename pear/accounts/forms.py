from django import forms


class RegistrationForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', max_length=50, required=False)
  last_name = forms.CharField('Last Name', max_length=50, required=False)
  class_year = forms.CharField('Class Year', max_length=4, required=False)
  major = forms.CharField('Major', max_length=50, required=False)


class LoginForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  password = forms.CharField('Password', max_length=50)