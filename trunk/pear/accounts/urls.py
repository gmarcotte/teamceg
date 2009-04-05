from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.accounts.views',
    (r'^login/$', 'login'),
    (r'^register/$', 'register'),
    (r'^logout/$', 'logout'),
    (r'^passwordchange/$', 'change_password'),
    (r'^passwordreset/$', 'reset_password'),
    (r'^delete/$', 'delete'),
    (r'^servers/$', 'servers'),
    (r'^toy/$', 'toy'),
    (r'^toyshell/$','toyshell'),
    # AJAX Views
    (r'^ajax/usersearch/$', 'ajax_user_search'),
)