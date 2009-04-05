from django.conf.urls import defaults

urlpatterns = defaults.patterns('pear.projects.views',
    (r'^newproject/$', 'create_project'),
    (r'^viewprojects/$', 'project_index'),
    (r'^addpartner/$', 'add_partner'),
    
    # Ajax Views
    (r'^ajax/coursesearch/$', 'ajax_course_search'),
)