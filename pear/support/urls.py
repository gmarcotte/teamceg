from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.support.views',
    (r'^help/$', 'help'),
    (r'^faq/$', 'faq'),
    
)