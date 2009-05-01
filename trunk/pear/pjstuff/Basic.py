from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, PopupPanel, FlowPanel, FormPanel, ScrollPanel, Label, HasAlignment, VerticalPanel, TextArea, TextBox, DialogBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel, MouseListener, KeyboardListener, Hyperlink
from pyjamas.Timer import Timer
from Tooltip import TooltipListener
from pyjamas import Window
from pyjamas.JSONService import JSONProxy

MEDIA_URL = 'http://localhost:8000'

class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/projects/services/", ["get_username", "get_meetinginfo","send_chatmessage","receive_chatmessage","send_flash","receive_flash","send_editor","receive_editor","user_quit",])

class Basic:
  def onModuleLoad(self):
    
    self.remote = DataService()
    
    # Figure out session info -- am i driver or passenger, etc.
    self.remote.get_meetinginfo(self)
    
    # start the timer for updates from server
    self.onTimer()
    
    
    # building the menu bar
    self.info = Button("Info", getattr(self, "onInfoClick"))
    self.mode = Button("Mode", getattr(self, "onModeClick"))
    self.audio = Button("Audio", getattr(self, "onAudioClick"))
    self.flash = Button("Flash ON", getattr(self, "setFlash"))
    self.quit = Button("Quit", getattr(self, "quit_pyjs"))
    self.testquit = Button("Test quit..", getattr(self, "testquit"))
    self.menu_body = SimplePanel()
    self.menu_contents = HTMLPanel("<img src='/pj/images/header_no_description.jpg' height='20px'>")
    self.menu_body.setWidget(self.menu_contents)
    self.flash.isActive = False  # is it currently the on-flash color?
    self.flash.Flash = False
    # put them together
    self.head = HorizontalPanel()
    self.head.add(self.info)
    self.head.add(self.mode)
    self.head.add(self.audio)
    self.head.add(self.flash)
    self.head.add(self.quit)
    self.head.add(self.testquit)
    self.head.add(Label("|"))
    self.head.add(self.menu_body)
    
    # the left side
    # editor
    editor = HTMLPanel("<textarea id='editarea' style='height: 610px; width: 100%;' name='test_1'></textarea><script>SetUpEditArea();</script>")
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
    console.setWidth("400px")
    console.setHeight("100%")
    # not so hacky -- indeed, pretty decent little text chat
    #self.text_area = TextArea() ## Let's try changing this to an HTML panel
    self.driver = Label("Unset")
    self.passenger = Label("Unset")
    self.text_area = ScrollPanel()
    self.text_area.setStyleName("text-area")
    self.text = HTML("(There is a 600 character limit on messages)")
    self.text_area.setWidget(self.text)
    self.text_area.setSize("400px", "150px")
    self.text_box = TextBox()
    self.text_box.setVisibleLength("53")
    self.text_box.setMaxLength("600")
    self.text_box.addKeyboardListener(self)
    text_send = Button("Send", getattr(self, "onTextSend"))
    text_entry = HorizontalPanel()
    text_entry.add(self.text_box)
    text_entry.add(text_send)
    text_entry.setWidth("340px")
    fake_chat = VerticalPanel()
    #fake_chat.add(self.chat_transcript)
    fake_chat.add(self.text_area)
    self.text_area.setScrollPosition(999999)
    fake_chat.add(text_entry)
    #js_tester = HTMLPanel(" my text in here. <script> myfunction(); </script> <div id='lame'></div>")
    #js_tester = SimplePanel()
    
    vp.add(console)
    vp.add(fake_chat)
    #vp.add(js_tester)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "50%")
    #vp.setCellHeight(js_tester, "50%")
    vp.setCellHeight(fake_chat, "50%")
    
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
    self.panel.setWidth("1000px")  # out of 1024
    self.panel.setHeight("700px")  # out of 768
    
    RootPanel().add(self.panel)
    
  def onInfoClick(self):
    id = self.remote.get_meetinginfo(self)
    if id < 0:
      console.error("Server Error or Invalid Response")
    self.menu_body.setWidget(HTML("User: %s, Partner: %s" % (self.driver.getText(), self.passenger.getText())))
  def onRemoteResponse(self, response, request_info):
    if request_info.method == 'get_username':
      if (len(response[3]) < 1):  # if there is no passenger
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
          self.passenger.setText("None")
        self.menu_body.setWidget(HTML("User: %s, Partner: %s" % (self.driver.getText(), self.passenger.getText())))
      else: 
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
          self.passenger.setText("%s" % tpl[3])
        self.menu_body.setWidget(HTML("User: %s, Partner: %s" % (self.driver.getText(), self.passenger.getText())))          
    elif request_info.method == 'get_meetinginfo':
      self.list = []
      for tpl in response:
        self.list.append("%s" % tpl[1])
      
      # set the local vars
      if (str(self.list[0]) == 'true'):
        self.isdriver = True
      else:
        self.isdriver = False
      self.project = Label("%s" % self.list[1])
      self.driver = Label("%s" % self.list[2])
      self.drivername = Label("%s" % self.list[3])
      self.passenger = Label("%s" % self.list[4]) # sometimes will be blank
      self.passengername = Label("%s" % self.list[5]) # sometimes will be blank
      if len(self.list[4]) < 1:
        self.passenger.setText("No Passenger")  # so passenger is not undefined,
        self.passengername.setText("No Passenger")
        
    elif request_info.method == 'send_chatmessage':
      for tpl in response:
        self.text.setHTML(self.text.getHTML() + "<br>" + str(tpl[1]))
        self.text_area.setWidget(self.text)
        self.text_area.setScrollPosition(999999)
    elif request_info.method == 'receive_chatmessage':
      for tpl in response:
        self.text.setHTML(self.text.getHTML() + "<br>" + str(tpl[1]))
        self.text_area.setWidget(self.text)
        self.text_area.setScrollPosition(999999)
    elif request_info.method == 'send_flash':
      self.Flash = self.Flash
    elif request_info.method == 'receive_flash':
      for tpl in response:
        if str(tpl[1]) == "off":
          if self.Flash:
            self.flashOff()
        else:
          if not self.Flash:
            self.flashOn()
    elif request_info.method == 'user_quit':
      for tpl in response:
        window.alert("%s" %tpl[1])
    else:
      console.error("Error in onRemoteResponse function in Basic.py")
  
  def onRemoteError(self, response, request_info):
    #window.alert("ERROR")
    pass
      
  def onModeClick(self):
    modepanel = HorizontalPanel()
    modebutt = Button("Switch Drivers", getattr(self, "onSwitchDriversClick"))
    modebutt.setStyleName("supp-button")
    modepanel.add(modebutt)
    self.menu_body.setWidget(modepanel)
    
  def onSwitchDriversClick(self):
    window.alert("You are trying to switch drivers")
    
    
  def onAudioClick(self):
    audiopanel = HorizontalPanel()
    audiobutton = Button("Skype Call", getattr(self, "onSkypeClick"))
    audiobutton.setStyleName("supp-button")
    audiopanel.add(audiobutton)
    #audiopanel.add(HTML("<a href='callto://YourUserNameHere'>Skype call</a>"))
    self.menu_body.setWidget(audiopanel)
  def onSkypeClick(self):
    window.alert("you are trying to make a skype call")
    
  def onAudioClose(self, sender):
    self.audiobox.hide()
  
  def onTimer(self):
    # do server update stuff here
    self.remote.receive_chatmessage(self)
    self.remote.receive_flash(self)
    
    # do flash stuff here
    if self.Flash:
      if self.isActive:
        self.panel.setStyleName("NORMAL")
        self.isActive = False
        Timer(1000, self)
        return
      else:  # if not self.isActive:
        self.panel.setStyleName("FLASH")
        self.isActive = True
        Timer(1000, self)
        return
    else:
      Timer(1000, self)
      return
    
  def flashOn(self):
    self.Flash = True
    self.onTimer()
    self.flash.setText("Flash OFF")
  
  def flashOff(self):
    self.Flash = False
    self.panel.setStyleName("WHITE")
    self.flash.setText("Flash ON")
              
  def setFlash(self):
    #alert("setting flash")
    # switch flash state message
    if not self.Flash:
      # turning flash on, tell our partner
      self.flashOn()
      self.remote.send_flash("on",self)
      return
    else:  # if self.Flash:
      # turning flash off, tell our partner
      self.flashOff()
      self.remote.send_flash("off",self)
      self.onTimer()
  
  def quit_pyjs(self):
    self.remote.user_quit(self)
    window.alert("We hope you had a productive session, come back soon! :)")
      
  def onClose(self):
    self._dialog.hide()
    
  def onTextSend(self):
    id = self.remote.get_username(self)
    if id < 0:
      console.error("Server Error or Invalid Response")
    self.remote.receive_chatmessage(self)
    # wait until we get the response
    if self.isdriver:
        msg = self.drivername.getText() + ": " + self.text_box.getText()
    else:  # if not self.isdriver:
      msg = self.passengername.getText() + ": " + self.text_box.getText()
    self.remote.send_chatmessage(msg, self)
    self.text_box.setText("")
    
  def onKeyUp(self, sender, keyCode, modifers):
    pass
  def onKeyDown(self, sender, keyCode, modifiers):
    pass
  def onKeyPress(self, sender, keyCode, modifiers):
    if keyCode == KeyboardListener.KEY_ENTER and sender == self.text_box:
      id = self.remote.get_username(self)
      if id < 0:
        console.error("Server Error or Invalid Response")
      #window.alert("you clicked enter")
      self.remote.receive_chatmessage(self)
      if self.isdriver:
        msg = self.drivername.getText() + ": " + self.text_box.getText()
      else:  # if not self.isdriver:
        msg = self.passengername.getText() + ": " + self.text_box.getText()
      self.remote.send_chatmessage(msg, self)
      self.text_box.setText("")
      
  def testquit(self):
    window.close()
    #pass