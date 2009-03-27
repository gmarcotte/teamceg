from django import forms


class RegistrationForm(forms.Form):
  username = forms.CharField('Username', max_length=50)
  email = forms.EmailField('E-Mail Address')
  first_name = forms.CharField('First Name', max_length=50, required=False)
  last_name = forms.CharField('Last Name', max_length=50, required=False)
  class_year = forms.CharField('Class Year', max_length=4, required=False)
  major = forms.CharField('Major', max_length=50, required=False)


  def Register(request):
    if request.method == 'POST':  # If the form has been submitted...
    form = RegistrationForm(request.POST)  #A form bound to the POST data
    if form.is_valid():
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      class_year = form.cleaned_data['class_year']
      major = form.cleaned_data['major']
      
      import pear.accounts.models
      p = profile(major=major, classyr=class_year)
      p.save()
      
      return HttpResponseRedirect('/thanks/')
      
    else:
      form = RegistrationForm()
      
    return render_to_response('contact.html', {
      'form': form,
      })

class LoginForm(forms.Form):
  email = forms.EmailField('E-Mail Address')
  password = forms.CharField('Password', max_length=50)