from django.conf.urls import defaults


urlpatterns = defaults.patterns('',
    (r'^$', 'pear.projects.views.index'),
    
    (r'^accounts/', defaults.include('pear.accounts.urls')),
    
)


if settings.STATIC_SERVER:
  urlpatterns += defaults.patterns('',
      (r'^(?P<path>(.*\.(jpg|swf|css|js|gif|png|JPG|GIF|PNG|htm|ico|PDF|pdf)))$', 
       'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  )