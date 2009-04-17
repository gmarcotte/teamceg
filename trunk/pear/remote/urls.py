from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.remote.views',
    (r'^servers/$', 'manage_servers'),
    (r'^servers/create/$', 'create_servers'),
)