#projects: models.py
#CCI 3/27/09
from django.db import models
from django.conf import settings

from pear.core import timestamp
import pear.accounts.models

import os


YEAR_CHOICES = (
    (1,'08-09'),
    (2,'09-10'),
    (3,'10-11'),
    (4,'11-12'),
)

SEM_CHOICES = (
    (1,'Fall'),
    (2,'Spring'),
)


class Course(timestamp.TimestampedModel):
  name = models.CharField(
      max_length=100)
  
  department = models.CharField(
      max_length=10, blank=True)
  
  number = models.CharField(
      max_length=10, blank=True)
  
  professor = models.ManyToManyField(
      pear.accounts.models.PearUser, 
      related_name='courses_taught')
  
  year = models.PositiveSmallIntegerField(
      choices=YEAR_CHOICES, null=True,
      blank=True)
  
  semester = models.PositiveSmallIntegerField(
      choices=SEM_CHOICES, null=True, blank=True)
  
  tas = models.ManyToManyField(
      pear.accounts.models.PearUser, 
      related_name='courses_taed')
  
  def __unicode__(self):
    if self.semester:
      return ("%s %s: %s, %s %s" 
              % (self.department, self.number, self.name,
                 self.get_semester_display(), self.get_year_display()))
    else:
      return ("%s %s: %s, %s"
              % (self.department, self.number, self.name, 
                 self.get_year_display()))


class Project(timestamp.TimestampedModel):
  name = models.CharField(
      max_length=50)
  
  description = models.TextField(
      blank=True)
  
  directory = models.CharField(
      max_length=20, blank=True)
  
  repos = models.CharField(
      max_length=100, blank=True, editable=False)
  
  programmers = models.ManyToManyField(
      pear.accounts.models.PearUser, related_name='projects')
  
  course = models.ForeignKey(
      Course, related_name='projects', null=True)
  
  is_active = models.BooleanField(editable=False, default=True)
  
  is_public = models.BooleanField()
  
  is_deleted = models.BooleanField(editable=False, default=False)
  
  # Display Methods
  def __unicode__(self):
    return self.name
  
  # Available URLs
  def edit_url(self):
    return '/projects/%s/edit/' % self.id
  
  def launch_url(self):
    return '/projects/%s/launch/' % self.id
  
  def join_url(self):
    return '/projects/%s/join/' % self.id
  
  def leave_url(self):
    return '/projects/%s/leave/' % self.id
  
  def delete_url(self):
    return '/projects/%s/delete/' % self.id
  
  def resurrect_url(self):
    return '/projects/%s/resurrect/' % self.id
  
  # Subversion/filesystem interaction methods
  def get_path(self, filename):
    return os.path.normcase(os.path.normpath(os.path.join(self.directory, filepath)))
  
  def get_repository_dir(self):
    return "%s%s%s" % (settings.SVN_BASE_DIR, os.sep, self.repos)
  
  def get_repository_url(self):
    return "%s/%s" % (settings.SVN_BASE_URL, self.repos)
  
  def create_repository(self):
    if os.path.exists(self.get_repository_dir()):
      return False
    else:
      cmd = "svnadmin create %s" % self.get_repository_dir()
      os.system(cmd)

  
  