from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.accounts.views',
    (r'^login/$', 'login'),
    (r'^register/$', 'register'),
    (r'^logout/$', 'logout'),
    (r'^passwordchange/$', 'change_password'),
    (r'^passwordreset/$', 'reset_password'),
    (r'^delete/$', 'delete'),
)