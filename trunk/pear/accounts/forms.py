from django import forms


class RegistrationForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', max_length=50, required=False)
  last_name = forms.CharField('Last Name', max_length=50, required=False)