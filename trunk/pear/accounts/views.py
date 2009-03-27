from django import shortcuts
from django import template
from django.contrib import auth
from django.contrib.auth import models as auth_models
from django import http
from django.core import exceptions

import pear.accounts.forms

def register(request):
  """Allows a new user to register an account.
     Following successful registration, redirects to home page.   
  """
  if request.method == 'POST':
    form = pear.accounts.forms.RegistrationForm(request.POST)
     
    if form.is_valid():
      new_user = form.save()
      return http.HttpResponseRedirect('/')
  
  else:
    form = pear.accounts.forms.RegistrationForm()
   
  return shortcuts.render_to_response(
      'global/accounts/register-email.html',
      {'form': form,},
      context_instance=template.RequestContext(request))
  

def login(request):
  """Login using email account."""
  redirect_to = request.REQUEST.get('next', '/')
  
  if request.user.is_authenticated():
    return http.HttpResponse("previously authenticated")#http.HttpResponseRedirect(redirect_to)

  if request.method == "POST":
    form = pear.accounts.forms.LoginForm(request.POST)
    
    try:
      user = None
      user_name = auth_models.User.objects.get(
          email=request.POST['email']).username
      if auth.models.check_password(request.POST['password'],auth_models.User.objects.get(email=request.POST['email']).password):
        user = auth_models.User.objects.get(email=request.POST['email'])
    except exceptions.ObjectDoesNotExist: 
      user = None

    if user is not None:
      if not user.is_active:
        return http.HttpResponse("account not activated.")#shortcuts.render_to_response(
            #'global/accounts/login.html',
            # TODO(marcotte): Change this to use the user message functions. 
            #{'login_message': ('Your account has not been activated. ' 
            #                   'Please check your email to activate.'), 
            # 'form':form},
            #context_instance=template.RequestContext(request))
        
      # User exists and is activated
      # auth.login(request, user)# generates error??
      return http.HttpResponse("user exists and is authenticated.")#http.HttpResponseRedirect(redirect_to)
        
    else:
      str = "login info incorrect: " + auth_models.User.objects.get(email=request.POST['email']).username + " " +auth_models.User.objects.get(email=request.POST['email']).password
      return http.HttpResponse(str)#shortcuts.render_to_response(
          #'global/accounts/login.html',
          # TODO(marcotte): Change this to use the user message functions. 
          #{'login_message': 'Login information incorrect. Please try again.', 
          # 'form': form},
          #context_instance=template.RequestContext(request))
          
  form = pear.accounts.forms.LoginForm(label_suffix="")
  return shortcuts.render_to_response(
      'global/accounts/login.html', 
      {'form': form},
      context_instance=template.RequestContext(request))