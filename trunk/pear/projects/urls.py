from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^$', 'global_project_listing'),
    (r'^create/$', 'create_project'),
    (r'^my_projects/$', 'project_index'),
    (r'^(?P<project_id>\d+)/add_partners/$', 'add_partners'),
    (r'^(?P<project_id>\d+)/edit/$', 'edit_project'),
    (r'^(?P<project_id>\d+)/join/', 'join_project'),
    (r'^(?P<project_id>\d+)/leave/', 'leave_project'),
    (r'^(?P<project_id>\d+)/delete/', 'delete_project'),
    (r'^(?P<project_id>\d+)/resurrect/', 'resurrect_project'),
    
    # Ajax Views
    (r'^ajax/coursesearch/$', 'ajax_course_search'),
)