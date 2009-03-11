from django.pimentech import network
from pear.todo import models

service = network.JSONRPCService()

@network.jsonremote(service)
def getTasks(request):
  l = []
  for task in models.Todo.objects.all():
    l.append( (str(task), task.id) )
  return l


@network.jsonremote(service)
def addTask(request, taskFromJson):
  t = models.Todo()
  t.task = taskFromJson
  t.save()
  return getTasks(request)

@network.jsonremote(service)
def deleteTask(request, idFromJson):
  t = models.Todo.objects.get(pk=idFromJson)
  t.delete()
  return getTasks(request)