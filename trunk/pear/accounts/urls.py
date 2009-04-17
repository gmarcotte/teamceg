from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.accounts.views',
    (r'^login/$', 'login'),
    (r'^register/$', 'register'),
    (r'^logout/$', 'logout'),
    (r'^change_password/$', 'change_password'),
    (r'^reset_password/$', 'reset_password'),
    (r'^delete/$', 'delete'),
    (r'^invite/$', 'invite_user'),
    
    
    # AJAX Views
    (r'^ajax/usersearch/$', 'ajax_user_search'),
)