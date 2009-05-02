from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, PopupPanel, FlowPanel, FormPanel, ScrollPanel, Label, HasAlignment, VerticalPanel, TextArea, TextBox, DialogBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel, MouseListener, KeyboardListener, Hyperlink
from pyjamas.Timer import Timer
from Tooltip import TooltipListener
from pyjamas import Window, History, DOM
from pyjamas.JSONService import JSONProxy


class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/projects/services/", ["get_username", "get_meetinginfo","send_chatmessage","receive_chatmessage","send_flash","receive_flash","send_editor","receive_editor","user_quit",])

class Basic:
  def onModuleLoad(self):
    
    self.remote = DataService()
    
    # Figure out session info -- am i driver or passenger, etc.
    self.remote.get_meetinginfo(self)
    
    # building the menu bar
    self.active_menu = Label("")
    self.info = Button("Info", getattr(self, "onInfoClick"))
    self.mode = Button("Mode", getattr(self, "onModeClick"))
    self.audio = Button("Audio", getattr(self, "onAudioClick"))
    self.flash = Button("Flash ON", getattr(self, "toggleFlash"))
    self.quit = Button("Quit", getattr(self, "onQuitClick"))
    self.menu_body = SimplePanel()
    self.menu_body.setWidth("600px")
    self.menu_contents = HTMLPanel("<img src='/pj/images/header_no_description.jpg' height='20px'>")
    self.menu_body.setWidget(self.menu_contents)
    self.active_flash = Label("Off")
    self.color = Label("white")
    # put them together
    self.head = HorizontalPanel()
    self.head.add(Label("|"))
    self.head.add(self.info)
    self.head.add(self.mode)
    self.head.add(self.audio)
    self.head.add(self.flash)
    self.head.add(self.quit)
    self.head.add(Label("|"))
    self.head.add(self.menu_body)
    self.head.add(self.menu_contents)
    
    # the left side
    # editor
    editor = HTMLPanel("<textarea id='editarea' style='height: 610px; width: 100%;' name='test_1'></textarea><script>SetUpEditArea();</script>")
    editor.setWidth("100%")
    editor.setHeight("100%")
    
    # the right side
    vp = VerticalPanel()
    vp.setBorderWidth(1)
    # the console
    term = HTMLPanel(" <script> setterm(); </script> <div id='term'></div>")  #Frame("http://127.0.0.1:8023/")
    term.setWidth("100%")
    term.setHeight("426px")
    console = SimplePanel()
    console.add(term)
    console.setWidth("400px")
    console.setHeight("100%")
    # not so hacky -- indeed, pretty decent little text chat
    self.driver = Label("Unset")
    self.passenger = Label("Unset")
    self.text_area = ScrollPanel()
    self.text_area.setStyleName("text-area")
    self.text = HTML("(There is a 600 character limit on messages)")
    self.text_area.setWidget(self.text)
    self.text_area.setSize("487px", "151px")
    self.text_box = TextBox()
    self.text_box.setVisibleLength("68")
    self.text_box.setMaxLength("600")
    self.text_box.addKeyboardListener(self)
    text_send = Button("Send", getattr(self, "onTextSend"))
    text_entry = HorizontalPanel()
    text_entry.add(self.text_box)
    text_entry.add(text_send)
    text_entry.setWidth("340px")
    real_chat = VerticalPanel()
    #real_chat.add(self.chat_transcript)
    real_chat.add(self.text_area)
    self.text_area.setScrollPosition(999999)
    real_chat.add(text_entry)
    real_chat.setStyleName("whitebg")
    #js_tester = HTMLPanel(" my text in here. <script> myfunction(); </script> <div id='lame'></div>")
    #js_tester = SimplePanel()
    
    vp.add(console)
    vp.add(real_chat)
    #vp.add(js_tester)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "50%")
    #vp.setCellHeight(js_tester, "50%")
    vp.setCellHeight(real_chat, "50%")
    
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
    self.panel.setHeight("650px")  # out of 768
    
    RootPanel().add(self.panel)
    
    # start the timer for updates from server
    self.onTimer()
    
  def onInfoClick(self):
    if self.active_menu.getText() == "Info":
      self.active_menu.setText("")
      self.menu_body.setWidget(Label(""))
    else:
      self.active_menu.setText("Info")
      id = self.remote.get_meetinginfo(self)
      if id < 0:
        console.error("Server Error or Invalid Response")
      infomsg = Label("Driver: %s, Passenger: %s" % (self.driver.getText(), self.passenger.getText()))
      infomsg.setStyleName("not-button")
      self.menu_body.setWidget(infomsg)

  def onRemoteResponse(self, response, request_info):
    if request_info.method == 'get_username':
      if (len(response[3]) < 1):  # if there is no passenger
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
          self.passenger.setText("None")
      else:  # if len(response[3]) > 0:  # if there is a passenger
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
          self.passenger.setText("%s" % tpl[3])
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
        self.passenger.setText("No Partner logged in")  # so passenger is not undefined,
        self.passengername.setText("No Partner logged in")
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
    if self.active_menu.getText() == "Mode":
      self.active_menu.setText("")
      self.menu_body.setWidget(Label(""))
    else:
      self.active_menu.setText("Mode")
      modepanel = HorizontalPanel()
      modebutt = Button("Switch Drivers", getattr(self, "onSwitchDriversClick"))
      modebutt.setStyleName("supp-button")
      modepanel.add(modebutt)
      self.menu_body.setWidget(modepanel)
    
  def onSwitchDriversClick(self):
    window.alert("You are trying to switch drivers")
    
    
  def onAudioClick(self):
    if self.active_menu.getText() == "Audio":
      self.active_menu.setText("")
      self.menu_body.setWidget(Label(""))
    else:
      self.active_menu.setText("Audio")
      audiopanel = HorizontalPanel()
      audiobutton = Button("Skype Call", getattr(self, "onSkypeClick"))
      audiobutton.setStyleName("supp-button")
      audiopanel.add(audiobutton)
      #audiopanel.add(HTML("<a href='callto://YourUserNameHere'>Skype call</a>"))
      self.menu_body.setWidget(audiopanel)
  def onSkypeClick(self):
    window.alert("you are trying to make a skype call")
  
  def onTimer(self):
    # do server update stuff here
    self.remote.receive_chatmessage(self)
    self.remote.receive_flash(self)
    
    # do flash stuff here
    if self.active_flash.getText() == "Flashing":
      if self.color.getText() == "pink":
        self.color.setText("green")
        self.panel.setStyleName("green")
      else:
        self.color.setText("pink")
        self.panel.setStyleName("pink")
    else:
      self.color.setText("white")
      self.panel.setStyleName("white")
    
    Timer(500, self)
    
  def toggleFlash(self):
    if self.active_flash.getText() == "Flashing":
      self.active_flash.setText("Off")
      self.flash.setText("Start Flash")
    else:
      self.active_flash.setText("Flashing")
      self.flash.setText("Stop Flash")
    
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
      
  def onQuitClick(self):
    #self.remote.user_quit(self)
    quitvp = VerticalPanel()
    quitvp.setSpacing(4)
    quitvp.add(HTML("We hope you had a productive session, come back soon!"))
    quithp = HorizontalPanel()
    quithp.setSpacing(7)
    quithp.add(Button("Wait, don't quit yet!", getattr(self, "onQuitCancel")))
    quithp.add(Button("Save and quit", getattr(self, "onQuitConfirm")))
    quitvp.add(quithp)
    quitvp.setCellHorizontalAlignment(quithp, HasAlignment.ALIGN_CENTER)
    self.quit_box = DialogBox()
    self.quit_box.setHTML("Quit Confirmation")
    self.quit_box.setWidget(quitvp)
    left = 350
    top = 200
    self.quit_box.setPopupPosition(left, top)
    self.quit_box.show()
  def onQuitCancel(self):
    self.quit_box.hide()
  def onQuitConfirm(self):
    self.quit_box.hide()
    ##save everything for them
    self.location = Window.getLocation()
    self.location.setHref("http://teamceg.princeton.edu/")