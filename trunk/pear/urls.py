from django.conf.urls import defaults


urlpatterns = defaults.patterns('',
    (r'^$', 'pear.projects.views.index'),
    
    (r'^accounts/', defaults.include('pear.accounts.urls')),
    
)