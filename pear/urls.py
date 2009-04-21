"""Top level URL routing definitions.

Here, we primarily include the URL definitions from other sub-apps.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


from django.conf import settings
from django.conf.urls import defaults

# Configure the admin
from django.contrib import admin
from pear.core import base_admin
admin.site = base_admin.PearAdminSite()
admin.autodiscover()

#pylint: disable-msg=C0103
# Django forces us to use this name, even though our standard would
# expect URLPATTERNS as a valid module-level name
urlpatterns = defaults.patterns('',
    (r'^$', 'pear.projects.views.index'),
    (r'^accounts/', defaults.include('pear.accounts.urls')),
    (r'^projects/', defaults.include('pear.projects.urls')),
    (r'^remote/', defaults.include('pear.remote.urls')),
    (r'^admin/', defaults.include(admin.site.urls)),
    
)

if settings.STATIC_SERVE:
  urlpatterns += defaults.patterns('',
      ((r'^(?P<path>(.*\.(jpg|swf|css|js|gif|png|JPG|'
        'GIF|PNG|htm|ico|PDF|pdf|html)))$'), 
       'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  )