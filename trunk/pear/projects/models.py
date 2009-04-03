#projects: models.py
#CCI 3/27/09
from django.db import models
from django.contrib.auth.models import User

from pear.core import timestamp


YEAR_CHOICES = (
    (1,'08-09'),
    (2,'09-10'),
    (3,'10-11'),
    (4,'11-12'),
)

SEM_CHOICES = (
    (0,'Fall'),
    (1,'Spring'),
)


class Course(timestamp.TimestampedModel):
  name = models.CharField(
      max_length=100, blank=True)
  
  department = models.CharField(
      max_length=10, blank=True)
  
  number = models.CharField(
      max_length=10, blank=True)
  
  professor = models.ManyToManyField(
      User, related_name='courses_taught')
  
  year = models.PositiveSmallIntegerField(
      choices=YEAR_CHOICES, null=True)
  
  semester = models.PositiveSmallIntegerField(
      choices=SEM_CHOICES, null=True)
  
  tas = models.ManyToManyField(
      User, related_name='courses_taed')
  
  def __unicode__(self):
    return ("%s %s: %s, %s %s" 
            % (self.department, self.number, self.name,
               self.year, self.semester))


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
      User, related_name='projects')
  
  course = models.ForeignKey(
      Course, related_name='projects')
  
  def __unicode__(self):
    return self.name