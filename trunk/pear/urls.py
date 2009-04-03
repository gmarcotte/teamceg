"""Top level URL routing definitions.

Here, we primarily include the URL definitions from other sub-apps.
"""

__author__ = ['Garrett Marcotte (marcotte@princeton.edu)']


from django.conf import settings
from django.conf.urls import defaults

#for admin...
from django.contrib import admin
admin.autodiscover()

#pylint: disable-msg=C0103
# Django forces us to use this name, even though our standard would
# expect URLPATTERNS as a valid module-level name
urlpatterns = defaults.patterns('',
    (r'^$', 'pear.projects.views.index'),
    
    (r'^accounts/', defaults.include('pear.accounts.urls')),
    
    (r'^admin/', include(admin.site.urls)),
)

if settings.STATIC_SERVE:
  urlpatterns += defaults.patterns('',
      ((r'^(?P<path>(.*\.(jpg|swf|css|js|gif|png|JPG|'
        'GIF|PNG|htm|ico|PDF|pdf)))$'), 
       'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  )