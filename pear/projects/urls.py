from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^newproject/$', 'projtest'),
)