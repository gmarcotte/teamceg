from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, Label, HasAlignment, VerticalPanel, FlowPanel, TextArea, TextBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel, MouseListener, Image, PopupPanel
from pyjamas.Timer import Timer
from Tooltip import TooltipListener
from pyjamas import Window
from pyjamas.JSONService import JSONProxy

MEDIA_URL = 'http://localhost:8000'

class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/projects/services/", ["get_username",])

class Basic:
  def onModuleLoad(self):
    
    self.remote = DataService()
    
    # the menu bar at the top
    #self.menu_bar = Menu()
    # the info button
    self.info = Button("Info", getattr(self, "onInfoClick"))
    self.flash = Button("Flash ON", getattr(self, "setFlash"))
    self.flash.isActive = False  # is it currently the on-flash color?
    self.flash.Flash = False
    # the header (menu bar & title)
    self.banner = Image("/pj/images/header_no_description.jpg")
    self.banner.setHeight("24px")
    self.banner.addMouseListener(TooltipListener("^--", 5000, "MOUSE"))
    # put them together
    self.header = DockPanel()
    #self.header.add(self.menu_bar, DockPanel.WEST)
    self.header.add(self.info, DockPanel.WEST)
    self.header.add(self.flash, DockPanel.WEST)
    self.header.add(self.banner, DockPanel.EAST)
    #self.header.setCellWidth(self.menu_bar, "11%")
    self.header.setCellWidth(self.info, "4%")
    self.header.setCellWidth(self.flash, "9%")
    self.header.setCellWidth(self.banner, "87%")
    self.header.setWidth("100%")
    self.header.setBorderWidth(0)
    
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
    term = HTMLPanel(" <script> setterm(); </script> <div id='term'></div>")#Frame("http://127.0.0.1:8023/")
    term.setWidth("100%")
    term.setHeight("426px")
    console = SimplePanel()
    console.add(term)
    console.setWidth("100%")
    console.setHeight("100%")
    # text chat
    # use sth like "flash chat"? do you really want to write your own?..
    text_area = TextArea()
    text_area.setHeight("215px")
    text_area.setWidth("657px")
    text_box = TextBox()
    text_box.setVisibleLength("85")
    text_box.setMaxLength("45")
    text_send = Button("Send", getattr(self, "onTextSend"))
    text_entry = HorizontalPanel()
    text_entry.add(text_box)
    text_entry.add(text_send)
    js_tester = HTMLPanel(" my text in here. <script> myfunction(); </script> <div id='lame'></div>")
    #js_tester = SimplePanel()
    
    vp.add(console)
    vp.add(js_tester)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "50%")
    vp.setCellHeight(js_tester, "50%")
    #vp.setCellHeight(fake_chat, "50%")
    
    # putting the left and right sides together
    hp = HorizontalPanel()
    hp.setBorderWidth(1)
    hp.setHorizontalAlignment(HasAlignment.ALIGN_CENTER)
    hp.setVerticalAlignment(HasAlignment.ALIGN_MIDDLE)
    hp.add(editor)
    hp.add(vp)
    hp.setCellWidth(editor, "52.5%")
    hp.setCellWidth(vp, "47.5%")
    #hp.setCellVerticalAlignment(editor, HasAlignment.ALIGN_JUSTIFY)
    hp.setCellVerticalAlignment(console, HasAlignment.ALIGN_TOP)
    hp.setWidth("100%")
    hp.setHeight("100%")
    
    # footer label
    self.footer = Label("A TeamCEG production")
    self.footer.setStyleName("footer")
    
    # putting it all together
    self.panel = DockPanel()
    self.panel.add(self.header, DockPanel.NORTH)
    self.panel.add(hp, DockPanel.CENTER)
    self.panel.add(self.footer, DockPanel.SOUTH)
    self.panel.setCellWidth(hp, "100%")
    self.panel.setCellHeight(hp, "100%")
    self.panel.setCellWidth(self.header, "100%")
    self.panel.setWidth("100%")
    self.panel.setHeight("100%")
    
    # visible mouse cursor stuff.. EK
    RootPanel().add(self.panel)
    #RootPanel().addMouseListener(TooltipListener("BLAHBLAHBLAH", 5000, "MOUSE"))
    
  def onInfoClick(self):
    #window.alert('Getting username')
    id = self.remote.get_username(self)
    if id < 0:
      console.error("Server Error or Invalid Response")
    #window.alert('Sent username request') 
    infocontents = HTML("Username: %s <br>Partner: %s" % (self.name.getText(), "bwk ^^"))
    infocontents.addClickListener(getattr(self, "onPopupClick"))
    self.popup = PopupPanel(autoHide = True)
    self.popup.add(infocontents)
    self.popup.setStyleName("gwt-PopupPanel")
    left = self.info.getAbsoluteLeft() + 1
    top = self.info.getAbsoluteTop() + 20
    self.popup.setPopupPosition(left, top)
    self.popup.show()
  def onPopupClick(self):
    self.popup.hide()
  def onRemoteResponse(self, response, request_info):
    #window.alert('Received remote response')
    console.info("response received")
    if request_info.method == 'get_username':
      console.info("got the username!")
      for tpl in response:
        #window.alert("User: %s" % tpl[1])
        self.name = Label("%s" % tpl[1])
    else:
      console.error("Error in onRemoteResponse")
    
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
    