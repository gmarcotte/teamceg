from django.pimentech import network
from pear.meetings.models import Meeting
from pear.meetings.models import ChatMessage
from pear.projects.models import Project
from pear.accounts.models import PearUser
service = network.JSONRPCService()


@network.jsonremote(service)
def get_username(request):
  if request.user.is_authenticated():
    return [('username', request.user.email)]
  else:
    return [('username', 'Anonymous')]

# sends a chat message, and returns any latent messages to display, including
# the message just sent
@network.jsonremote(service)
def send_chatmessage(request,message):
  if request.user.is_authenticated():
    r = []

    # get the meeting
    meeting = None
    meetings = Meeting.objects.all()#pear.meetings.models.Meeting.objects.get(driver_id=request.user.id)

    for meet in meetings:
      # Check to see if it is the right meeting
      if request.user.id == meet.driver_id:
        meeting = meet
      if request.user.id == meet.passenger_id:
        meeting = meet
    if meeting == None:
      r.append('Error','ERROR: could not find active meeting')
      return r

    # make the message
    msg = ChatMessage()

    msg.sender = request.user
    
    if meeting.driver_id == request.user.id:
      msg.receiver = PearUser.objects.get(pk=meeting.passenger_id)
    else:
      msg.receiver = PearUser.objects.get(pk=meeting.driver_id)
    
    msg.message = message
    msg.save()
    # add this message to the queue in the database
    if meeting.unsent_messages == None:
      meeting.unsent_messages = []
    meeting.unsent_messages.add(msg)
    meeting.save()
    
    # now look and see if there are any latent messages
    if meeting.unsent_messages == None:
      r.append(('success',message))
      return r
    
    msgs = meeting.unsent_messages.all()

    # find the unsent messages for this user
    for msg in msgs:
      if str(msg.receiver_id) == str(request.user.id):
        r.append(('msg',msg.message))
        # delete the message from unsent and put it in sent
        meeting.sent_messages.add(msg)
        meeting.unsent_messages.remove(msg)
    #return r
    
    r.append(('success',message))
    return r

@network.jsonremote(service)
def receive_chatmessage(request):
  if request.user.is_authenticated():
    r = []

    # get the meeting
    meeting = None
    meetings = Meeting.objects.all()

    for meet in meetings:
      # Check to see if it is the right meeting
      if request.user.id == meet.driver_id:
        meeting = meet
      if request.user.id == meet.passenger_id:
        meeting = meet
    if meeting == None:
      r.append('Error','ERROR: could not find active meeting')
      return r

    
    if meeting.unsent_messages == None:
      r.append(('alert','No Messages'))
      return r
    
    msgs = meeting.unsent_messages.all()

    # find the unsent messages for this user
    for msg in msgs:
      if str(msg.receiver_id) == str(request.user.id):
        r.append(('msg',msg.message))
        # delete the message from unsent and put it in sent
        meeting.sent_messages.add(msg)
        meeting.unsent_messages.remove(msg)
    return r


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
    
    
@network.jsonremote(service)
def receive_flash(request):
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
      return r
    
    if meeting.flash == True:
      r.append(('flash','on'))
    else:
      r.append(('flash','off'))
    
    return r
    
    
@network.jsonremote(service)
def send_flash(request, state):
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
      return r
    
    if str(state) == 'on':
      meeting.flash = True
      meeting.save()
      r.append(('flash','on'))
    else:
      meeting.flash = False
      meeting.save()
      r.append(('flash','off'))
        
    return r