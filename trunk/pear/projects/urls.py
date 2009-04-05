from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^$', 'global_project_listing'),
    (r'^newproject/$', 'create_project'),
    (r'^viewprojects/$', 'project_index'),
    (r'^addpartner/$', 'add_partner'),
    (r'^inviteuser/$', 'invite_user'),
    (r'^(?P<project_id>\d+)/join/', 'join_project'),
    
    # Ajax Views
    (r'^ajax/coursesearch/$', 'ajax_course_search'),
)