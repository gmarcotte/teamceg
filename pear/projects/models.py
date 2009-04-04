#projects: models.py
#CCI 3/27/09
from django.db import models

from pear.core import timestamp
import pear.accounts.models


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
      max_length=100, blank=True)
  
  department = models.CharField(
      max_length=10, blank=True)
  
  number = models.CharField(
      max_length=10, blank=True)
  
  professor = models.ManyToManyField(
      pear.accounts.models.PearUser, 
      related_name='courses_taught')
  
  year = models.PositiveSmallIntegerField(
      choices=YEAR_CHOICES, null=True)
  
  semester = models.PositiveSmallIntegerField(
      choices=SEM_CHOICES, null=True)
  
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
      max_length=20)
  
  repos = models.CharField(
      max_length=100, blank=True)
  
  programmers = models.ManyToManyField(
      pear.accounts.models.PearUser, related_name='projects')
  
  course = models.ForeignKey(
      Course, related_name='projects', null=True)
  
  def __unicode__(self):
    return self.name