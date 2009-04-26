from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, PopupPanel, FlowPanel, FormPanel, Label, HasAlignment, VerticalPanel, TextArea, TextBox, DialogBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel, MouseListener, Image
from pyjamas.Timer import Timer
from Tooltip import TooltipListener
from pyjamas import Window
from pyjamas.JSONService import JSONProxy

MEDIA_URL = 'http://localhost:8000'

class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/projects/services/", ["get_username", "get_meetinginfo", "send_chatmessage","receive_chatmessage",])

class Basic:
  def onModuleLoad(self):
    
    self.remote = DataService()
    
    # building the menu bar
    self.info = Button("Info", getattr(self, "onInfoClick"))
    self.mode = Button("Mode", getattr(self, "onModeClick"))
    self.audio = Button("Audio", getattr(self, "onAudioClick"))
    self.flash = Button("Flash ON", getattr(self, "setFlash"))
    self.menu_body = SimplePanel()
    self.menu_contents = HTMLPanel("<img src='/pj/images/header_no_description.jpg' height='30px'>")
    self.menu_body.setWidget(self.menu_contents)
    self.flash.isActive = False  # is it currently the on-flash color?
    self.flash.Flash = False
    # the header
    self.banner = Image("/pj/images/header_no_description.jpg")
    self.banner.setHeight("20px")
    self.banner.addMouseListener(TooltipListener("^--", 5000, "MOUSE"))
    # put them together
    self.head = HorizontalPanel()
    self.head.add(self.info)
    self.head.add(self.mode)
    self.head.add(self.audio)
    self.head.add(self.flash)
    self.head.add(Label("|"))
    self.head.add(self.menu_body)
    
    # the left side
    # editor
    editor = HTMLPanel("<div id='myhelene'></div> <script> sethelene(); </script> ")
    editor.setWidth("100%")
    editor.setHeight("100%")
    
    # the right side
    vp = VerticalPanel()
    vp.setBorderWidth(1)
    # the console
    console = Label("Console")
    term = HTMLPanel(" <script> setterm(); </script> <div id='term'></div>")  #Frame("http://127.0.0.1:8023/")
    term.setWidth("100%")
    term.setHeight("426px")
    console = SimplePanel()
    console.add(term)
    console.setWidth("100%")
    console.setHeight("100%")
    # hacky little "text chat"

    msg_line = TextArea()
    msg_line.setHeight("150px")
    msg_line.setWidth("470px")
    text_box = TextBox()
    text_box.setVisibleLength("60")
    text_box.setMaxLength("60")

    text_send = Button("Send", getattr(self, "onTextSend"))
    text_entry = HorizontalPanel()
    text_entry.add(self.text_box)
    text_entry.add(text_send)
    #text_entry.add(msg_line)
    text_entry.setWidth("500px")
    fake_chat = VerticalPanel()

    fake_chat.add(msg_line)

    fake_chat.add(text_entry)
    #js_tester = HTMLPanel(" my text in here. <script> myfunction(); </script> <div id='lame'></div>")
    #js_tester = SimplePanel()
    
    vp.add(console)
    vp.add(fake_chat)
    #vp.add(chat_form)
    #vp.add(js_tester)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "50%")
    #vp.setCellHeight(js_tester, "50%")
    vp.setCellHeight(fake_chat, "50%")
    #vp.setCellHeight(chat_form, "50%")
    
    # putting the left and right sides together
    hp = HorizontalPanel()
    hp.setBorderWidth(1)
    hp.setHorizontalAlignment(HasAlignment.ALIGN_CENTER)
    hp.setVerticalAlignment(HasAlignment.ALIGN_MIDDLE)
    hp.add(editor)
    hp.add(vp)
    hp.setCellWidth(editor, "50%")
    hp.setCellWidth(vp, "50%")
    #hp.setCellVerticalAlignment(editor, HasAlignment.ALIGN_JUSTIFY)
    hp.setCellVerticalAlignment(console, HasAlignment.ALIGN_TOP)
    hp.setWidth("100%")
    hp.setHeight("100%")
    
    # footer label
    self.footer = Label("A TeamCEG production")
    self.footer.setStyleName("footer")
    
    # putting it all together
    self.panel = DockPanel()
    self.panel.add(self.head, DockPanel.NORTH)
    self.panel.add(hp, DockPanel.CENTER)
    self.panel.add(self.footer, DockPanel.SOUTH)
    self.panel.setCellWidth(hp, "100%")
    self.panel.setCellHeight(hp, "100%")
    self.panel.setCellWidth(self.head, "100%")
    self.panel.setWidth("1002px")
    self.panel.setHeight("655px")
    
    # visible mouse cursor stuff.. EK
    RootPanel().add(self.panel)
    #RootPanel().addMouseListener(TooltipListener("BLAHBLAHBLAH", 5000, "MOUSE"))
  
  
  def onTextSend(self):
    # get the text 
    self.remote.send_chatmessage("My message", self)
    self.remote.receive_chatmessage(self)
        
  def onInfoClick(self):
    #window.alert('Getting username')
    id = self.remote.get_username(self)
    #id = self.remote.get_meetinginfo(self)
    if id < 0:
      console.error("Server Error or Invalid Response")
    #window.alert('Sent username request') 
    self.menu_body.setWidget(HTML("User: %s, Partner: %s" % (self.driver.getText(), self.passenger.getText())))

  def onRemoteResponse(self, response, request_info):
    #window.alert('Received remote response')
    #console.info("response received")  # DO NOT USE THESE; FIREFOX DOESN'T LIKE IT
    if request_info.method == 'get_username':
      if len(response[3]) < 1:  # if there is no passenger
        #window.alert("No passenger")
        for tpl in response:
          self.driver = Label("%s" % tpl[1])
          self.passenger = Label("None")
          #window.alert("%s" % tpl[3])
      else:  # if len(response[3]) > 0:  # if there is a passenger
        window.alert("There is a passenger")
        for tpl in response:
          self.driver = Label("%s" % tpl[1])
          self.passenger = Label("%s" % tpl[3])
    elif request_info.method == 'get_meetinginfo':
      for tpl in response:
        window.alert("Returned: %s" % tpl[1])
        self.driver = Label("%s" % tpl[2])
        self.project = Label("%s" % tpl[1])
        self.passenger = Label("%s" % tpl[3]) # sometimes will be blank
    if request_info.method == 'send_chatmessage':
      for tpl in response:
        window.alert("Returned: %s" % tpl[1])
    if request_info.method == 'send_chatmessage':
      for tpl in response:
        window.alert("Returned: %s" % tpl[1])
    else:
      console.error("Error in onRemoteResponse function in Basic.py")
  
  def onRemoteError(self, response, request_info):
    window.alert("ERROR")
      
  def onModeClick(self):
    modepanel = HorizontalPanel()
    modepanel.add(Button("Switch Drivers", getattr(self, "onSwitchDriversClick")))
    self.menu_body.setWidget(modepanel)
    
  def onSwitchDriversClick(self):
    window.alert("You are trying to switch drivers")
    
  def onAudioClick(self):
    audiopanel = HorizontalPanel()
    audiobutton = Button("Skype Call", getattr(self, "onSkypeClick"))
    audiopanel.add(audiobutton)
    #audiopanel.add(HTML("<a href='callto://YourUserNameHere'>Skype call</a>"))
    self.menu_body.setWidget(audiopanel)
  def onSkypeClick(self):
    window.alert("you are trying to make a skype call")
    
  def onTimer(self):
    if self.Flash:
      #Window.alert("should be flashing..")
      if self.isActive:
        self.panel.setStyleName("NORMAL")
        #vp.setStyleName("NORMAL")
        self.isActive = False
        Timer(500, self)
        #Window.alert("STOPPED FLASH")
        return
      if not self.isActive:
        self.panel.setStyleName("FLASH")
        #vp.setStyleName("FLASH")
        self.isActive = True
        Timer(500, self)
        #Window.alert("STARTED FLASH")
        return
    #else:  # if not self.Flash:
      #Timer(1000, getattr(self, "offTimer"))
  def setFlash(self):
    if not self.Flash:
      self.Flash = True
      self.onTimer()
      self.flash.setText("Flash OFF")
      #Window.alert("turned on flashing")
      return
    else:  # if self.Flash:
      self.Flash = False
      self.panel.setStyleName("WHITE")
      self.flash.setText("Flash ON")
    
  def onClose(self):
    self._dialog.hide()
    
  def onTextSend(self):
    #window.alert("onTextSend called")
    new_chat_text = Label("%s" % self.text_box.getText())
    #window.alert("%s" % new_chat_text.getText())
    self.text_area.setText(self.text_area.getText() + "\n" + new_chat_text.getText())
    self.text_box.setText("")