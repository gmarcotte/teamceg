from django.conf.urls import defaults
from django.conf import settings


urlpatterns = defaults.patterns('',
    (r'^$', 'pear.projects.views.index'),
    
    (r'^accounts/', defaults.include('pear.accounts.urls')),
    
)


if settings.STATIC_SERVE:
  urlpatterns += defaults.patterns('',
      (r'^(?P<path>(.*\.(jpg|swf|css|js|gif|png|JPG|GIF|PNG|htm|ico|PDF|pdf)))$', 
       'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  )