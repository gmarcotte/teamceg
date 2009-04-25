from django.pimentech import network
from pear.meetings.models import Meeting
from pear.projects.models import Project
from pear.accounts.models import PearUser
service = network.JSONRPCService()

@network.jsonremote(service)
def get_username(request):
  if request.user.is_authenticated():
    return [('username', request.user.email)]
  else:
    return [('username', 'Anonymous')]

@network.jsonremote(service)
def get_meetinginfo(request):
  if request.user.is_authenticated():
    r = []
    meeting = None
    # get the meeting associated with this user
    meetings = Meeting.objects.all()#pear.meetings.models.Meeting.objects.get(driver_id=request.user.id)
    for meet in meetings:
      # Check to see if it is the right meeting
      if request.user.id == meet.driver_id:
        meeting = meet
      if request.user.id == meet.passenger_id:
        meeting = meet
    
    if (meeting == None):
      r.append(('error', 'ERROR: no active meeting!'))
    
    else:
      project = Project.objects.get(pk=meeting.project_id)
      driver = PearUser.objects.get(pk=meeting.driver_id)
      
      r.append(('project', project.name))
      r.append(('driver', driver.email))
      if meeting.passenger_id > 0:
        passenger = PearUser.objects.get(pk=meeting.passenger_id)
        r.append(('passenger', passenger.email))
      
    return r
    # if meeting, return info