from django.conf.urls import defaults
from django.conf import settings

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^$', 'global_project_listing'),
    (r'^create/$', 'create_project'),
    (r'^my_projects/$', 'project_index'),
    (r'^(?P<project_id>\d+)/add_partners/$', 'add_partners'),
    (r'^(?P<project_id>\d+)/edit/$', 'edit_project'),
    (r'^(?P<project_id>\d+)/join/$', 'join_project'),
    (r'^(?P<project_id>\d+)/leave/$', 'leave_project'),
    (r'^(?P<project_id>\d+)/delete/$', 'delete_project'),
    (r'^(?P<project_id>\d+)/resurrect/$', 'resurrect_project'),
    (r'^(?P<project_id>\d+)/launch/$', 'launch_project'),
    (r'^(?P<project_id>\d+)/add_file/$', 'add_file'),
    # Ajax Views
    (r'^ajax/coursesearch/$', 'ajax_course_search'),
)

if settings.STATIC_SERVE:
  urlpatterns += defaults.patterns('',
      ((r'^\d+/launch/(?P<path>(.*\.(jpg|swf|css|js|gif|png|JPG|'
        'GIF|PNG|htm|ico|PDF|pdf|html)))$'), 
       'django.views.static.serve', {'document_root': "%s/pj/" % settings.MEDIA_ROOT}),
  )


# JSON RPC Calls
urlpatterns += defaults.patterns('pear.projects.json_views',
    (r'^services/$', 'service'),
)