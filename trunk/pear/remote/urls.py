from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.remote.views',
    (r'^servers/$', 'manage_servers'),
    (r'^servers/create/$', 'create_server'),
    (r'^servers/(?P<server_id>\d+)/delete/', 'delete_server'),
    (r'^servers/(?P<server_id>\d+)/refresh/', 'refresh_keys'),
    (r'^servers/(?P<server_id>\d+)/clear/', 'clear_keys'),
    (r'^servers/(?P<server_id>\d+)/test/', 'test_keys'),
)