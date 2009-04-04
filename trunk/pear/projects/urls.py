from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^newproject/$', 'CreateProject'),
    (r'^viewprojects/$', 'ProjectIndex'),
)