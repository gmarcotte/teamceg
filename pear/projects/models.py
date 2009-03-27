#projects: models.py
#CCI 3/27/09
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
  YEAR_CHOICES = (
    (1,'08-09'),
	(2,'09-10'),
	(3,'10-11'),
	(4,'11-12'),
  )
  SEM_CHOICES = (
    ('F','Fall'),
	('S','Spring'),
  )
  name = models.CharField(max_length=30)
  department = models.CharField(max_length=10)
  number = models.CharField(max_length=10)
  professor = models.ManyToManyField(User, related_name='courses taught')
  year = models.PositiveSmallIntegerField(max_length=1, choices=YEAR_CHOICES)
  semester = models.CharField(max_length=1, choices=SEM_CHOICES)
  TAs = models.ManyToManyField(User, related_name='courses TA-ed')
  
  def __unicode__(self):
    stri = str(name) + str(department) + str(number) + str(professor)
    return stri
	
class Project(models.Model):
  programmers = models.ManyToManyField(User)
  course = models.ForeignKey(Course)
  
  def __unicode__(self):
    stri = str(self.course) + str(self.programmers)
    return stri