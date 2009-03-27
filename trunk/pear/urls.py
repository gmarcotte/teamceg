from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^$', 'pear.projects.views.index'),
    (r'^login$', 'pear.accounts.views.login'),
    (r'^register$', 'pear.accounts.views.register'),
    
)