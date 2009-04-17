from django.contrib import admin
from django.db import models as django_models

from pear.projects import models
from pear.projects import forms


class CourseOptions(admin.ModelAdmin):
  form = forms.AdminCourseCreateForm
  list_display = ('name', 'department', 'number', 'year_display', 'professor_display', 'ta_display')
  list_display_links = ('name',)
  
  def year_display(self, obj):
    if obj.semester:
      return '%s %s' % (obj.get_semester_display(), obj.get_year_display())
    else:
      return obj.get_year_display()
  year_display.short_description = 'Offered'
  year_display.admin_order_field = 'year'
  
  def professor_display(self, obj):
    profs = []
    for prof in obj.professor.all():
      profs.append(prof.get_full_name())
    return '<br />'.join(profs)
  professor_display.short_description = 'Professors'
  professor_display.allow_tags = True
  
  def ta_display(self, obj):
    tas = []
    for ta in obj.tas.all():
      tas.append(ta.get_full_name())
    return '<br />'.join(tas)
  ta_display.short_description = 'TAs'
  ta_display.allow_tags = True
admin.site.register(models.Course, CourseOptions)


admin.site.register(models.Project, admin.ModelAdmin)
  