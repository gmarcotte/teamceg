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
      r.append(('Error','ERROR: could not find active meeting'))
      return r

    # make the message
    msg = ChatMessage()

    msg.sender = request.user
    
    if meeting.driver_id == request.user.id:
      # if no passenger, receiver == null
      if meeting.passenger_id > 0:
        msg.receiver = PearUser.objects.get(pk=meeting.passenger_id)
      else:
        msg.receiver = None
    else:
      msg.receiver = PearUser.objects.get(pk=meeting.driver_id)
    fullmessage = request.user.first_name + ": "+ message
    msg.message = fullmessage
    msg.save()
    # add this message to the queue in the database
    if meeting.unsent_messages == None:
      meeting.unsent_messages = []
    meeting.unsent_messages.add(msg)
    meeting.save()
    
    # now look and see if there are any latent messages
    if meeting.unsent_messages == None:
      r.append(('msg',fullmessage))
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
    
    r.append(('success',fullmessage))
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
      r.append(('Error','ERROR: could not find active meeting'))
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
      if (str(driver.id) == str(request.user.id)):
        r.append(('isdriver', 'True'))
      else:
        r.append(('isdriver', 'False'))
      r.append(('project', project.name))
      r.append(('driver', driver.email))
      r.append(('drivername', driver.first_name))
      #r.append(('consoleID',meeting.driverconsole))
      if meeting.passenger_id > 0:
        passenger = PearUser.objects.get(pk=meeting.passenger_id)
        r.append(('passenger', passenger.email))
        r.append(('passengername', passenger.first_name))
      
      r.append(('new_sid', str(meeting.driverconsole)))
      r.append(('new_ssh', str(meeting.driverssh.server)))
      r.append(('new_user', str(meeting.driverssh.user_name)))
      r.append(('new_key', str(meeting.driver_id))) 
    return r
    # if meeting, return info
  else:
    r = []
    r.append(('Error','No meeting'))
    return r
    
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
    
@network.jsonremote(service)
def send_editor(request, content):
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
    
    # if the user is the driver, make the passenger the driver
    if str(request.user.id) == str(meeting.driver_id):
      meeting.editor = content
      meeting.save()
      r.append(('seteditor','it worked'))
      return r

@network.jsonremote(service)
def receive_editor(request):
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
    
    # if the user is the driver, make the passenger the driver
    if str(request.user.id) != str(meeting.driver_id):
      r.append(('content', meeting.editor))
      return r


@network.jsonremote(service)
def driver_status(request):
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
    
    r.append(('new_sid', str(meeting.driverconsole)))
    r.append(('new_ssh', str(meeting.driverssh.server)))
    r.append(('new_user', str(meeting.driverssh.user_name)))
    r.append(('new_key', str(meeting.driver_id)))    
    ##r.append(('consoleid',str(meeting.driverconsole)))
    # if the user is the driver return true 
    if str(request.user.id) == str(meeting.driver_id):
        r.append(('isdriver','True'))
    
    # if the user is the passenger return false
    else:
      r.append(('isdriver','False'))
        
    return r


@network.jsonremote(service)
def switch_driver(request):
  if request.user.is_authenticated():
    r = []
    meeting = None
    # get the meeting associated with this user
    meetings = Meeting.objects.all()
    for meet in meetings:
      # Check to see if it is the right meeting
      if request.user.id == meet.driver_id:
        meeting = meet
      if request.user.id == meet.passenger_id:
        meeting = meet
    
    if (meeting == None):
      r.append(('error', 'ERROR: no active meeting!'))
      return r
    
    
    # if the user is the driver, make the passenger the driver
    if str(request.user.id) == str(meeting.driver_id):
      if meeting.passenger_id > 0:
        # make the passenger the driver
        tempid = meeting.passengerconsole
        meeting.passengerconsole = meeting.driverconsole
        meeting.driverconsole = tempid
        temp = meeting.driver_id
        meeting.driver_id = meeting.passenger_id
        meeting.passenger_id = temp
        tempssh = meeting.passengerssh
        meeting.passengerssh = meeting.driverssh 
        meeting.driverssh = tempssh
        meeting.save()
        #r.append(('notice','we switched drivers'))
        r.append(('new_sid', str(meeting.driverconsole)))
        r.append(('new_ssh', str(meeting.driverssh.server)))
        r.append(('new_user', str(meeting.driverssh.user_name)))
        r.append(('new_key', str(meeting.driver_id)))
        r.append(('isdriver','False'))
        
      else:
        r.append(('new_sid', str(meeting.driverconsole)))
        r.append(('new_ssh', str(meeting.driverssh.server)))
        r.append(('new_user', str(meeting.driverssh.user_name)))
        r.append(('new_key', str(meeting.driver_id)))
        # if there is no passenger, do nothing
        #r.append(('notice','no passenger'))
        r.append(('isdriver','True'))
    
    # error case that should NEVER happen
    else:
      r.append(('notice','passenger should not call this method!'))
    r.append(('consoleID',str(meeting.driverconsole)))
    return r
  else:
    r = []
    r.append(('error','not authenticated.'))
    return r
    
@network.jsonremote(service)
def user_quit(request):
  if request.user.is_authenticated():
    r = []
    meeting = None
    # get the meeting associated with this user
    meetings = Meeting.objects.all()
    for meet in meetings:
      # Check to see if it is the right meeting
      if request.user.id == meet.driver_id:
        meeting = meet
      if request.user.id == meet.passenger_id:
        meeting = meet
    
    if (meeting == None):
      r.append(('error', 'ERROR: no active meeting!'))
      return r
    
    # if the user is the driver, make the passenger the driver
    if str(request.user.id) == str(meeting.driver_id):
      if meeting.passenger_id > 0:
        # make the passenger the driver
        meeting.driver_id = meeting.passenger_id
        meeting.passenger = None
        meeting.driverconsole = meeting.passengerconsole
        meeting.passengerconsole = None
        meeting.driverssh = meeting.passengerssh
        meeting.passengerssh = None
        
        meeting.save()
        r.append(('notice','there was a passenger, and we switched drivers'))
        
        
      else:
        # if no passenger, clear the relevant info from the meeting
        meeting.project_id = 0
        meeting.passenger = None
        # note that driver cannot be none...
        meeting.driver_id = 0
        meeting.save()
        r.append(('notice','there was no passenger, quitting'))
    
    # if the user is the passenger, just delete them
    else:
      meeting.passenger = None
      meeting.save()
      r.append(('notice','there was a passenger, and we deleted them'))
        
    return r
  
@network.jsonremote(service)
def new_file(request, filename):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  ssh.save_file(client, project.get_path(filename))
  ssh.svn_add(client, project.get_path(filename))    
  ssh.close(client)
  return [('notice', 'Created file %s' % filename)]

@network.jsonremote(service)
def new_directory(request, dirname):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  ssh.make_directory(client, project.get_path(dirname))
  ssh.close(client)
  return [('notice', 'Created directory %s' % dirname)]


@network.jsonremote(service)
def open_file(request, filename):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  status,text = ssh.load_file(client, project.get_path(filename))
  ssh.close(client)
  if status:
    return [('filetext', text)]
  else:  
    return [('error', 'Error reading %s: %s' % (filename, text))]


@network.jsonremote(service)
def save_file(request, filename, text):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  status,text = ssh.save_file(client, project.get_path(filename), text)
  ssh.close(client)
  if status:
    return [('filetext', 'Saved %s' % filename)]#'The new text of %s is %s' % (filename, text))]
  else:
    return [('error', 'Error saving %s: %s' % (filename, text))]
  
    
@network.jsonremote(service)
def get_file_tree(request):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  tree = ssh.read_file_tree(client, project.directory)
  ssh.close(client)
  return tree
  
  
@network.jsonremote(service)
def sync_all(request):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  ssh.svn_commit(client, project.directory)
  ssh.close(client)
  return [('notice', 'I synced the entire project')]

@network.jsonremote(service)
def delete_file(request, filename):
  meeting = request.user.current_meeting
  if meeting is None:
    return [('error', 'ERROR: no active meeting')]
  project = meeting.project
  ssh = meeting.driverssh
  client = ssh.connect()
  status,text = ssh.svn_delete(client, project.get_path(filename))
  ssh.close(client)
  return [('notice', 'I deleted %s' % filename)]