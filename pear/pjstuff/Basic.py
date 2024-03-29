from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, PopupPanel, FlowPanel, FormPanel, ScrollPanel, Label, HasAlignment, VerticalPanel, TextArea, TextBox, DialogBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel, MouseListener, KeyboardListener, Hyperlink, Tree, TreeItem, FileUpload
from pyjamas.Timer import Timer
from Tooltip import TooltipListener
from pyjamas import Window, History, DOM
from pyjamas.JSONService import JSONProxy
from ContextMenuPopupPanel import ContextMenuPopupPanel


class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/projects/services/", ["get_username", "get_meetinginfo","send_chatmessage","receive_chatmessage","send_flash","receive_flash","send_editor","receive_editor","user_quit", "driver_status","switch_driver","new_file","new_directory","open_file","save_file","get_file_tree","delete_file","sync_all"])

class Basic:
  def onModuleLoad(self):
    self.remote = DataService()
    self.initEditor = False
    # this tells us whether or not we are trying to quit...
    self.quitting = False
    self.switching = False
   
    # file info
    self.current_open = None
    self.modified = False
    self.originalContents = ""
   
    # Figure out session info -- am i driver or passenger, etc.
    self.remote.get_meetinginfo(self)
   
    # building the menu bar
    self.active_menu = Label("")
    self.info = Button("Info", getattr(self, "onInfoClick"))
    self.file_list = []
    self.remote.get_file_tree(self) # will need to change rd to actual root directory.
   
    self.files = Button("Files", getattr(self, "onFilesClick"))
    #self.FileContext = SimplePanel("La di da")
    self.mode = Button("Mode", getattr(self, "onModeClick"))
    self.audio = Button("Audio", getattr(self, "onAudioClick"))
    self.flash = Button("Start Flash", getattr(self, "toggleFlash"))
    self.quit = Button("Quit", getattr(self, "onQuitClick"))
    self.menu_body = SimplePanel()
    self.menu_contents = HTMLPanel("<img src='/pj/images/logo_clean_long.jpg' height='21px'>")
    self.menu_body.setWidget(self.menu_contents)
    self.active_flash = Label("Off")
    self.color = Label("white")
    # put them together
    self.head = HorizontalPanel()
    self.head.add(Label("|"))
    self.head.add(self.info)
    self.head.add(self.files)
    self.head.add(self.mode)
    self.head.add(self.audio)
    self.head.add(self.flash)
    self.head.add(self.quit)
    self.head.add(Label("|"))
    self.head.add(self.menu_body)
   
    # the left side
    # editor
    # The editorID is the id of the actual editor text area
    # the functionID is the id of the setupeditarea and set_listener/set_editable() functions
    # the synchID is the id of the interval command for setting synchEditors/synchListeners based on
    #     whether driver or passenger.
    ### For now let's try hard-coding these
    self.editorID = "MYeditorID"
    self.editorHTMLID = "MYeditorHTMLID"
    self.functionID = "MYfunctionID"
    self.synchID = "MYsynchID"
    self.chatID = "MYchatID"
    self.intervalID = "MYintervalID"
    self.editorsynchID = "MYeditorsynchID"
    self.listensynchID = "MYlistensynchID"
    self.termfunctionID = "MYtermfunctionID"
   
    # This is where we store the stuff going back and forth from the editor in driver mode.
    # listenID no longer exists, fix after demo.
    self.functionHTML = HTML("<script>SetUpEditArea('" + self.editorID +"','"+self.listenID+ "'); </script>")
    self.editorHTML = HTML(" ")
    self.editorHTML.setVisible(False)
    self.editorHTML.setID(self.editorHTMLID)
   
    # this gets the contents of the editor into the div area so we can send it
    self.driversynch = """
    <script>
    clearInterval(window.listenInterval);
    clearInterval(window.editorInterval);
    window.editorInterval = setInterval('syncheditor()', 100);
     
    function syncheditor() {
    // see if this helps with actually setting it to be editable again
    //alert("synching editor")
    editAreaLoader.execCommand('MYeditorID', 'set_editable', true);
    var content = editAreaLoader.getValue('MYeditorID');
    var listener = document.getElementById('MYeditorHTMLID');
    listener.innerHTML = "<div id=\\"MYeditorHTMLID\\" style=\\"white-space: normal; display: none;\\" class=\\"gwt-HTML\\">"+ content + "</div>";
    }</script>"""
   
    #<div style="white-space: normal;" class="gwt-HTML"><script> </script> </div>
    self.passengersynch = """
    <script>
    clearInterval(window.editorInterval);
    clearInterval(window.listenInterval);
    window.listenInterval = setInterval('synchlisten()', 100);
    //document.getElementById('MYeditorHTMLID').innerHTML="<div id='MYeditorHTMLID' style='white-space: normal; display: none;' class='gwt-HTML'>Initial Text</div>"
    function synchlisten() {
    //alert("synching listen")
    var currentfocus = document.activeElement;
    var content = document.getElementById('MYeditorHTMLID').innerHTML;//innerHTML;
    content = content.substring(86, content.length-6);
    editAreaLoader.setValue('MYeditorID', content);
    editAreaLoader.execCommand('MYeditorID', 'set_editable', false);
    currentfocus.focus()
    }</script>"""
   
    initialcontent = """<script> </script> """
   

    self.editor = HTMLPanel("<div id='"+self.synchID+"'</div><div id='" + self.editorHTMLID + "'></div>"+ "<textarea id='"+self.editorID+"' style='height: 575px; width: 100%;'></textarea> <div id='" + self.functionID + "'></div>")

    self.editorTextArea = TextArea()
    self.editorTextArea.setID(self.editorID)
    self.editor.add(self.editorTextArea, self.editorID)
    self.editor.add(self.functionHTML, self.functionID)
    self.editor.add(self.editorHTML, self.editorHTMLID)
   
    self.editor.add(HTML(initialcontent), self.synchID)
    self.editor.setWidth("100%")
    self.editor.setHeight("100%")
   
    #innerhtml = "<div id='MYeditorHTMLID' style='white-space: normal; display: none;' class='gwt-HTML'></div>";
    #DOM.setInnerHTML(DOM.getElementById(self.editorHTMLID), innerhtml)#tpl[1]) was innerText
   
   
   
    # the right side
    vp = VerticalPanel()
    vp.setBorderWidth(1)
    # the console
    self.term = HTMLPanel(" <script> setterm(''); </script> <div id='term'></div><div id='MYtermfunctionID'></div>")  #Frame("http://127.0.0.1:8023/")
    self.term.setWidth("100%")
    self.term.setHeight("390px")
    console = SimplePanel()
    console.add(self.term)
    console.setWidth("400px")
    console.setHeight("100%")
    # not so hacky -- indeed, pretty decent little text chat
    self.text_area = ScrollPanel()
    self.text_area.setStyleName("text-area")
    self.text = HTML("(There is a 600 character limit on messages)")
    self.text_area.setWidget(self.text)
    self.text_area.setSize("487px", "151px")
    self.text_box = TextBox()
    self.text_box.setVisibleLength("58")
    self.text_box.setMaxLength("600")
    self.text_box.setID(self.chatID)
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
   
    vp.add(console) # console and chat added to vertical panel
    vp.add(real_chat)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "50%")
    vp.setCellHeight(real_chat, "50%")
   
    # putting the left and right sides together
    hp = HorizontalPanel()
    hp.setBorderWidth(1)
    hp.setHorizontalAlignment(HasAlignment.ALIGN_CENTER)
    hp.setVerticalAlignment(HasAlignment.ALIGN_MIDDLE)
    hp.add(self.editor)
    hp.add(vp)
    hp.setCellWidth(self.editor, "50%")
    hp.setCellWidth(vp, "50%")
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
    self.panel.setWidth("995px")  # out of 1024
    self.panel.setHeight("400px")  # out of 768
   
    RootPanel().add(self.panel)
   
    # start the timer for updates from server
    self.currpass = Label("No Partner logged in")
    self.onTimer()
     
  def onRemoteResponse(self, response, request_info):
    if request_info.method == 'get_username':
      if (len(response[3]) < 1):  # if there is no passenger
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
      else:
        for tpl in response:
          self.driver.setText("%s" % tpl[1])
          self.passenger.setText("%s" % tpl[3])
    elif request_info.method == 'get_meetinginfo':
      haspassenger = False
      previousconsoleID = self.consoleID
      for tpl in response:
        if str(tpl[0]) == 'isdriver':
          if str(tpl[1]) == 'True':
            self.isdriver = True
            if self.initEditor == False:
              self.editor.add(HTML(self.driversynch), self.synchID)
              self.initEditor = True
          else:
            self.isdriver = False
            self.editor.add(HTML(self.passengersynch), self.synchID)
        if str(tpl[0]) == 'project':
          self.project = Label("%s" % tpl[1])
        if str(tpl[0]) == 'driver':
          self.driver = Label("%s" % tpl[1])
        if str(tpl[0]) == 'drivername':
          self.drivername = Label("%s" % tpl[1])
        if str(tpl[0]) == 'new_sid':
          self.consoleID = str(tpl[1])
        if str(tpl[0]) == 'new_ssh':
          self.ssh = str(tpl[1])
        if str(tpl[0]) == 'new_user':
          self.usr = str(tpl[1])
        if str(tpl[0]) == 'new_key':
          self.key = str(tpl[1])
        if str(tpl[0]) == 'passenger':
          self.passenger = Label("%s" % tpl[1])
          haspassenger = True
        if str(tpl[0]) == 'passengername':
          self.passengername = Label("%s" % tpl[1])
      if haspassenger == False:
        self.passenger = Label("")
        self.passengername = Label("")
        self.passenger.setText("No Partner logged in")  # so passenger is not undefined,
        self.passengername.setText("No Partner logged in")
      if str(self.consoleID) != str(previousconsoleID):
        #window.alert("Changing console in get_meetinginfo")
        self.term.add(HTML("<script>changeSID('"+self.consoleID+"','"+self.ssh +"','"+self.usr+ "','"+self.key+"','"+self.isdriver+ "')</script>"), self.termfunctionID)
     
       
    elif request_info.method == 'send_chatmessage':
      for tpl in response:
        #alert(str(tpl[1]))
        self.text.setHTML(self.text.getHTML() + "<br>" + str(tpl[1]))
        self.text_area.setWidget(self.text)
        self.text_area.setScrollPosition(999999)
    elif request_info.method == 'receive_chatmessage':
      for tpl in response:
        #alert(str(tpl[1]))
        self.text.setHTML(self.text.getHTML() + "<br>" + str(tpl[1]))
        self.text_area.setWidget(self.text)
        self.text_area.setScrollPosition(999999)
    elif request_info.method == 'send_flash':
      pass
    elif request_info.method == 'receive_flash':
      for tpl in response:
        if str(tpl[1]) == "off":
          if self.Flash:
            self.toggleFlash()
        else:
          if not self.Flash:
            self.toggleFlash()
    elif request_info.method == 'send_editor':
      #window.alert("sent editor")
      pass
    elif request_info.method == 'receive_editor':
      # check to see if maybe there is an error here because of empty string?
      for tpl in response:
        #alert(str(tpl[1]))
        content = tpl[1]
        innerhtml = "<div id='MYeditorHTMLID' style='white-space: normal; display: none;' class='gwt-HTML'>" + content+"</div>";
        DOM.setInnerHTML(DOM.getElementById(self.editorHTMLID), innerhtml)#tpl[1]) was innerText
        #self.editorHTML.setVisible(False)
   
    elif request_info.method == 'driver_status':
      if self.switching == False:
        self.switching = True
        for tpl in response:
          if (str(tpl[0])) == 'new_sid':
            self.consoleID = str(tpl[1])
          if (str(tpl[0])) == 'new_ssh':
            self.ssh = str(tpl[1])
          if (str(tpl[0])) == 'new_user':
            self.usr = str(tpl[1])
          if (str(tpl[0])) == 'new_key':
            self.key = str(tpl[1])
          if (str(tpl[0])) == 'isdriver':
            if str(tpl[1]) == 'False':
              if self.isdriver == True:
                self.isdriver = False
                self.editor.add(HTML(self.passengersynch), self.synchID)
                #window.alert("Doing a console set from isdriver False in driverstatus")
                self.term.add(HTML("<script>changeSID('"+self.consoleID+"','"+self.ssh +"','"+self.usr+ "','"+self.key+"','"+self.isdriver+ "')</script>"), self.termfunctionID)
            if str(tpl[1]) == 'True':
              if self.isdriver == False:
                self.isdriver = True
                self.editor.add(HTML(self.driversynch), self.synchID)
                #new_ssh,new_user,new_key,
                #window.alert("Doing a console set from isdriver true in driverstatus")
                self.term.add(HTML("<script>changeSID('"+self.consoleID+"','"+self.ssh +"','"+self.usr+ "','"+self.key+"','"+self.isdriver+ "')</script>"), self.termfunctionID)
          self.switching = False
         
    elif request_info.method == 'switch_driver':
      for tpl in response:
        if (str(tpl[0])) == 'new_sid':
            self.consoleID = str(tpl[1])
        if (str(tpl[0])) == 'new_ssh':
          self.ssh = str(tpl[1])
        if (str(tpl[0])) == 'new_user':
          self.usr = str(tpl[1])
        if (str(tpl[0])) == 'new_key':
          self.key = str(tpl[1])
        if (str(tpl[0])) == 'isdriver':
          if (str(tpl[1])) == "True":
            if self.isdriver == False:
              self.isdriver = True
              self.editor.add(HTML(self.driversynch), self.synchID)
              self.switching = False
              #window.alert("console set from switch-driver isdriver true")
              self.term.add(HTML("<script>changeSID('"+self.consoleID+"','"+self.ssh +"','"+self.usr+ "','"+self.key+"','"+self.isdriver+ "')</script>"), self.termfunctionID)
              # need to hold off until we know the id self.term.add(HTML("<script>changeSID('"+self.consoleID+"');</script>"),"MYtermfunctionID")
          elif str(tpl[1]) == "False":
            if self.isdriver == True:
              self.isdriver = False
              self.editor.add(HTML(self.passengersynch), self.synchID)
              self.switching = False
              #window.alert("console set from switch-driver isdriver FALSE")
              self.term.add(HTML("<script>changeSID('"+self.consoleID+"','"+self.ssh +"','"+self.usr+ "','"+self.key+"','"+self.isdriver+ "')</script>"), self.termfunctionID)
              # self.term.add(HTML("<script>changeSID('"+self.consoleID+"');</script>"),"MYtermfunctionID")
         
    elif request_info.method == 'new_file':
      for tpl in response:
        window.alert(str(tpl[1]))
    elif request_info.method == 'new_directory':
      for tpl in response:
        window.alert(str(tpl[1]))
    elif request_info.method == 'open_file':
      for tpl in response:
        #window.alert(str(tpl[1]))
        # todo: SAVE whatever is currently in the editor
        # add response text to editor
        contents = str(tpl[1])
        contents = contents.replace('\n','\\n')
        self.editor.add(HTML("<script>editAreaLoader.setValue('MYeditorID','"+contents+"');</script>"), self.functionID)
        self.originalContents = str(tpl[1])
        self.modified = False
    elif request_info.method == 'save_file':
      self.modified = False
      for tpl in response:
        window.alert(str(tpl[1]))
       
    elif request_info.method == 'delete_file':
      for tpl in response:
        window.alert(str(tpl[1]))
    elif request_info.method == 'get_file_tree':
      self.file_list = []
      for tpl in response:
        #window.alert(str(tpl[0])+ " " + str(tpl[1]) + " " + str(tpl[2]))
        self.file_list.append(tpl)
       
     
    elif request_info.method == 'user_quit':
      self.location = Window.getLocation()
      self.location.setHref("http://teamceg.princeton.edu/")
    elif request_info.method == 'sync_all':
      pass
    else:
      console.error("Error in onRemoteResponse function in Basic.py")
 
  def onRemoteError(self, response, request_info):
    pass
     
  def onInfoClick(self):

    if self.active_menu.getText() == "Info":
      self.active_menu.setText("")
      self.menu_body.setWidget(self.menu_contents)
    else:
      self.active_menu.setText("Info")
      infomsg = Label("Driver: %s, Passenger: %s" % (self.driver.getText(), self.passenger.getText()))
      infomsg.setStyleName("not-button")
      self.menu_body.setWidget(infomsg)

  def onFilesClick(self):
    if self.active_menu.getText() == "Files":
      self.active_menu.setText("")
      self.menu_body.setWidget(self.menu_contents)
    else:
      self.active_menu.setText("Files")
      filepanel = HorizontalPanel()
      filetreebutton = Button("File Tree", getattr(self, "onFileTreeOpenClick"))
      filesavebutton = Button("Save", getattr(self,"onFileSave"))
      filetreebutton.setStyleName("supp-button")
      filesavebutton.setStyleName("supp-button")
      filepanel.add(filetreebutton)
      filepanel.add(filesavebutton)
      self.menu_body.setWidget(filepanel)
 
  def onFileSave(self):
    # get the text from the editor and send a save command to the server.
    if self.isdriver == True:
      content = DOM.getInnerText(DOM.getElementById(self.editorHTMLID))
      self.remote.save_file(str(self.current_open[2]),content, self)
      self.originalContents = content
 
  def onFileUploadOpenClick(self):
    self.uploadform = FormPanel()
    self.uploadform.setEncoding(FormPanel.ENCODING_MULTIPART)
    self.uploadform.setMethod(FormPanel.METHOD_POST)
    self.uploadform.setAction("http://www.google.com")
    self.uploadform.setTarget("results")
    upload_hp = HorizontalPanel()
    upload_hp.setSpacing(7)
    upload_hp.add(Label("Upload file:"))
    self.fileup = FileUpload()
    self.fileup.setName("file")
    upload_hp.add(self.fileup)
    fileuploadsubmitbutt = Button("Submit", getattr(self, "onFileUploadSubmitClick"))
    fileuploadclosebutt = Button("Cancel", getattr(self, "onFileUploadCloseClick"))
    uploadbutt_hp = HorizontalPanel()
    uploadbutt_hp.setSpacing(7)
    uploadbutt_hp.add(fileuploadsubmitbutt)
    uploadbutt_hp.add(fileuploadclosebutt)
    upload_vp = VerticalPanel()
    upload_vp.setSpacing(4)
    upload_vp.add(upload_hp)
    results = NamedFrame("results")
    upload_vp.add(results)
    upload_vp.add(uploadbutt_hp)
    upload_vp.setCellHorizontalAlignment(uploadbutt_hp, HasAlignment.ALIGN_CENTER)
    self.uploadform.add(upload_vp)
    self.upload_box = DialogBox()
    self.upload_box.setHTML("File Upload")
    self.upload_box.setWidget(self.uploadform)
    self.upload_box.setPopupPosition(350, 150)
    self.upload_box.show()
  def onFileUploadSubmitClick(self):
    self.uploadform.submit()
    self.upload_box.hide()
  def onFileUploadCloseClick(self):
    self.upload_box.hide()
  def onFileDirOpenClick(self):
    pass ###
  def onFileTreeOpenClick(self):
    filetree = Tree()
    filetree.addTreeListener(self)
    i = 0
    ## Values will be full paths of the files, so we can send them directly
    ## Names will be filename within the directory or the directory name
    self.remote.get_file_tree(self)
    while (i < len(self.file_list)) and (self.file_list[i][0][0] == "1"):
      s1 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])#"root/")
      i = i + 1
      while (i < len(self.file_list)) and (self.file_list[i][0][0] == "2"):
        s2 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
        s1.addItem(s2)
        s1.setState(True, fireEvents=False)
        i = i + 1
        while (i < len(self.file_list)) and (self.file_list[i][0][0] == "3"):
          s3 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
          s2.addItem(s3)
          s2.setState(False, fireEvents=False)
          i = i + 1
          while (i < len(self.file_list)) and (self.file_list[i][0][0] == "4"):
            s4 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
            s3.addItem(s4)
            s3.setState(False, fireEvents=False)
            i = i + 1
            while (i < len(self.file_list)) and (self.file_list[i][0][0] == "5"):
              s5 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
              s4.addItem(s5)
              s4.setState(False, fireEvents=False)
              i = i + 1
              while (i < len(self.file_list)) and (self.file_list[i][0][0] == "6"):
                s6 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
                s5.addItem(s5)
                s5.setState(False, fireEvents=False)
                i = i + 1
                while (i < len(self.file_list)) and (self.file_list[i][0][0] == "7"):
                  s7 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
                  s6.addItem(s5)
                  s6.setState(False, fireEvents=False)
                  i = i + 1
                  while (i < len(self.file_list)) and (self.file_list[i][0][0] == "8"):
                    s8 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
                    s7.addItem(s5)
                    s7.setState(False, fireEvents=False)
                    i = i + 1
                    while (i < len(self.file_list)) and (self.file_list[i][0][0] == "9"):
                      s9 = self.createTreeItem(str(self.file_list[i][0][1:]), value=self.file_list[i][2])
                      s8.addItem(s5)
                      s8.setState(False, fireEvents=False)
                      i = i + 1
      #  s1.setState(True, fireEvents=False)
      filetree.addItem(s1)      
    filetreepanel = VerticalPanel()
    filetreepanel.setSpacing(7)
    filetreepanel.setCellHorizontalAlignment(filetree, HasAlignment.ALIGN_LEFT)
    filetreepanel.add(filetree)
    filetreebutt = Button("Close", getattr(self, "onFileTreeCloseClick"))
    filetreepanel.add(filetreebutt)
    filetreepanel.setCellHorizontalAlignment(filetreebutt, HasAlignment.ALIGN_CENTER)
    filetreepanel.setWidth("400px")
    self.file_box = DialogBox()
    if self.current_open != None:
      self.file_box.setHTML("<b>File Navigation</b> Currently Editing: <i>%s</i>" % str(self.current_open[2]))
    else:
      self.file_box.setHTML("<b>File Navigation</b>")
    self.file_box.setWidget(filetreepanel)
    self.file_box.setPopupPosition(350, 200)
    self.file_box.show()
  def createTreeItem(self, label, value=None):
    item = TreeItem(label)
    DOM.setStyleAttribute(item.getElement(), "cursor", "pointer")
    #Will not work don't bother ##item.setContextMenu(self) # this needs latest version of pjs
    if value != None:
      item.setUserObject(value)
    return item
  def onTreeItemSelected(self, item):
    acted = False
    value = item.getUserObject()
    # prevent non-driver from modifying file tree structure
    if self.isdriver == False:
      return
    # check if the file currently opened has been modified
    currentcontent = DOM.getInnerText(DOM.getElementById(self.editorHTMLID))
   
    if str(currentcontent) != self.originalContents:
      if self.originalContents != None:
        self.modified = True
   
    # if it is a file -> open it.
    for thing in self.file_list:
      if str(thing[2]) == str(value):
        if str(thing[1])=="file":
          # Is there currently a file open?
          if self.current_open != None:
            if self.modified == True:
              # force the user to save or discard
              self.nextfile = thing
              guts = VerticalPanel()
              guts.setSpacing(4)
              guts.add(HTML('Unsaved changes were detected in an open file. Would you like to save your changes?'))
              gutshp = HorizontalPanel()
              gutshp.setSpacing(7)
              gutshp.add(Button("Save", getattr(self, "onDialogSave")))
              gutshp.add(Button("Discard", getattr(self, "onDialogDiscard")))
              guts.add(gutshp)
              guts.setCellHorizontalAlignment(gutshp, HasAlignment.ALIGN_CENTER)
              self.savediscard_box = DialogBox()
              self.savediscard_box.setHTML("<b>Warning: Unsaved Changes</b>")
              self.savediscard_box.setWidget(guts)
              self.savediscard_box.setPopupPosition(200, 200)
              self.savediscard_box.show()
              acted = True
            else:
              self.remote.open_file(str(value),self)
              acted = True
              self.modified = False
              self.current_open = thing
          else:
            self.remote.open_file(str(value),self)
            acted = True
            self.modified = False
            self.current_open = thing
    # if it is a directory -> make a popup to add/delete files dirs
    if acted == False:
      #window.alert("Will display a dialog window to manage directory: " + str(value))
      self.current_directory = str(value) + "/"
      contents = VerticalPanel()
      contents.setSpacing(4)
      contents.add(HTML('Add or delete files and directories.'))
      contentshp = HorizontalPanel()
      contentshp.setSpacing(7)
      contentshp.add(Button("Add",getattr(self,"onAddDialog")))
      contentshp.add(Button("Delete",getattr(self,"onDeleteDialog")))
      contentshp.add(Button("Cancel",getattr(self,"onCancelManageDialog")))
      contents.add(contentshp)
      contents.setCellHorizontalAlignment(contentshp, HasAlignment.ALIGN_CENTER)
      self.manage_directory_box = DialogBox()
      self.manage_directory_box.setHTML("<b>Manage Directory</b>")
      self.manage_directory_box.setWidget(contents)
      self.manage_directory_box.setPopupPosition(200,200)
      self.manage_directory_box.show()

  def onTreeItemStateChanged(self, item):
    pass  
  def onFileTreeCloseClick(self):
    self.file_box.hide()
 
  def onAddDialog(self):
    contents = VerticalPanel()
    contents.setSpacing(4)
    contents.add(HTML('Add files and directories.'))
    contentshpfd = HorizontalPanel()
    self.NewDir = RadioButton("group1","directory")
    self.NewFile = RadioButton("group1","file")
    self.NewFile.setChecked(True)
    contentshpfd.add(self.NewDir)
    contentshpfd.add(self.NewFile)
    
    contentshpn = HorizontalPanel()
    contentshpn.setSpacing(7)
    self.NewFileName = TextBox()
    self.NewFileName.setID(self.chatID) # This should protect it from ajaxterm stealing...
    contentshpn.add(self.NewFileName)
    contentshp = HorizontalPanel()
    contentshp.setSpacing(7)
    contentshp.add(Button("Add",getattr(self,"onAddOK")))
    contentshp.add(Button("Cancel",getattr(self,"onCancelAdd")))
    contents.add(contentshpfd)
    contents.add(contentshpn)
    contents.add(contentshp)
    contents.setCellHorizontalAlignment(contentshp, HasAlignment.ALIGN_CENTER)
    self.manage_add_box = DialogBox()
    self.manage_add_box.setHTML("<b>Add</b>")
    self.manage_add_box.setWidget(contents)
    self.manage_add_box.setPopupPosition(200,200)
   
    self.manage_add_box.show()
    # hide the manage directory box, and the file tree -- it's distracting
    self.manage_directory_box.hide()
    self.file_box.hide()
       
  def onAddOK(self):
    newfile = self.current_directory + self.NewFileName.getText()
    newfile = newfile.lstrip("/")
    if self.NewDir.isChecked():
      self.remote.new_directory(newfile,self)
      self.remote.get_file_tree(self)
    else:
      self.remote.new_file(newfile,self)
      self.remote.get_file_tree(self)
    self.manage_add_box.hide()
   
  def onCancelAdd(self):
    self.manage_add_box.hide()
 
  def onDeleteDialog(self):
    contents = VerticalPanel()
    contents.setSpacing(4)
    contents.add(HTML('Delete files and directories.'))
    contentshpfd = HorizontalPanel()
    self.DelDir = RadioButton("group2","whole directory")
    self.DelFile = RadioButton("group2","files")
    self.DelFile.setChecked(True)
    self.DelFile.addClickListener(getattr(self,"onFileClick"))
    self.DelDir.addClickListener(getattr(self,"onDirClick"))
    contentshpfd.add(self.DelDir)
    contentshpfd.add(self.DelFile)
    contentshpn = VerticalPanel()
    contentshpn.setSpacing(7)
    self.FilesToDelete = []
    # find the files in this directory
    level = "0"
    for i in range(0,len(self.file_list)):
      if str(self.file_list[i][2]) == str(self.current_directory)[:len(str(self.current_directory))-1]:
        level = str(int(self.file_list[i][0][0]) + 1)
        start = i
    for i in range(start+1, len(self.file_list)):
      if self.file_list[i][0][0] == level:
        self.FilesToDelete.append(CheckBox(str(self.file_list[i][2])))
      else:
        level = "0"


    for i in range(0,len(self.FilesToDelete)):
      contentshpn.add(self.FilesToDelete[i])
    contentshp = HorizontalPanel()
    contentshp.setSpacing(7)
    contentshp.add(Button("Delete",getattr(self,"onDelOK")))
    contentshp.add(Button("Cancel",getattr(self,"onCancelDel")))
    contents.add(contentshpfd)
    contents.add(contentshpn)
    contents.add(contentshp)
    contents.setCellHorizontalAlignment(contentshp, HasAlignment.ALIGN_CENTER)
    self.manage_del_box = DialogBox()
    self.manage_del_box.setHTML("<b>Delete</b>")
    self.manage_del_box.setWidget(contents)
    self.manage_del_box.setPopupPosition(200,200)
   
    self.manage_del_box.show()
    # hide the manage directory box, and the file tree -- it's distracting
    self.manage_directory_box.hide()
    self.file_box.hide()
   
  def onFileClick(self):
    for i in range(0, len(self.FilesToDelete)):
      self.FilesToDelete[i].setEnabled(True)
 
  def onDirClick(self):
    for i in range(0, len(self.FilesToDelete)):
      self.FilesToDelete[i].setChecked(True)
      self.FilesToDelete[i].setEnabled(False)
 
  def onDelOK(self):
    if self.DelDir.isChecked():
      dir = self.current_directory[:len(self.current_directory)]
      dir = dir.lstrip("/")
      dir = dir.rstrip("/")
      self.remote.delete_file(dir,self) # do we need to prevent root?
   
    # just files
    else:
      for i in range(0, len(self.FilesToDelete)):
        if self.FilesToDelete[i].isChecked():
          fname = self.current_directory + self.FilesToDelete[i].getText() # we put file names (not full paths)in the list
          fname = fname.lstrip("/")
          self.remote.delete_file(fname,self)
    self.remote.get_file_tree(self)
    self.manage_del_box.hide()
     
  def onCancelDel(self):
    self.manage_del_box.hide()
 
  def onCancelManageDialog(self):
    self.manage_directory_box.hide()
     
  def onDialogSave(self):
    content = DOM.getInnerText(DOM.getElementById(self.editorHTMLID))
    self.remote.save_file(str(self.current_open[2]), content, self) #self.current_open
    self.remote.open_file(str(self.nextfile[2]),self) #self.nextfile
    self.modified = False
    # set the content to none
    self.current_open = self.nextfile
    self.savediscard_box.hide()
 
  def onDialogDiscard(self):
    self.remote.open_file(str(self.nextfile[2]),self) # self.nextfile
    self.modified = False
    # set the content to None
    self.current_open = self.nextfile
    self.savediscard_box.hide()
 
  def onModeClick(self):
    if self.active_menu.getText() == "Mode":
      self.active_menu.setText("")
      self.menu_body.setWidget(self.menu_contents)
    else:
      self.active_menu.setText("Mode")
      modepanel = HorizontalPanel()
      modebutt = Button("Switch Drivers", getattr(self, "onSwitchDriversClick"))
      modebutt.setStyleName("supp-button")
      modepanel.add(modebutt)
      self.menu_body.setWidget(modepanel)
   
  def onSwitchDriversClick(self):
    #window.alert("You are trying to switch drivers")
    if self.isdriver == True:
      self.switching = True
      self.editor.add(HTML("<script>clearInterval(window.editorInterval);</script>"), self.functionID)
      self.remote.switch_driver(self)
      #window.alert("Just sent switch command.")
    else:
      window.alert("Passengers cannot elect to switch!")
   
  def onAudioClick(self):
    if self.active_menu.getText() == "Audio":
      self.active_menu.setText("")
      self.menu_body.setWidget(self.menu_contents)
    else:
      self.active_menu.setText("Audio")
      audiopanel = HorizontalPanel()
      audiobutton = Button("Skype Call", getattr(self, "onSkypeClick"))
      audiobutton.setStyleName("supp-button")
      audiopanel.add(audiobutton)
      self.menu_body.setWidget(audiopanel)
  def onSkypeClick(self):
    #window.alert("you are trying to make a skype call")
    #audiopanel.add(HTML("<a href='skype:NAME?call'>Skype call</a>"))
    DOM.getElementById('Skype call').click()
    self.location = Window.getLocation()
    self.location.setHref("skype:NAME?call")
 
  def onTimer(self):
    # Check for new passenger
    if self.isdriver:
      self.remote.get_meetinginfo(self)
      if self.currpass.getText() != self.passenger.getText():
        self.currpass.setText(self.passenger.getText())
        if self.passenger.getText() == "No Partner logged in":
          #window.alert("No partners logged in")
          pass
        else:
          window.alert("New passenger %s detected" % self.passenger.getText())
       
    if self.quitting == False and self.switching == False:
      # do server update stuff here
      self.remote.receive_chatmessage(self)
      self.remote.receive_flash(self)
      # this only really matters for passengers
      if self.isdriver == False:
        self.remote.driver_status(self)
     
      if self.isdriver == True:
        content = DOM.getInnerText(DOM.getElementById(self.editorHTMLID))
        if len(content) > 0:
          self.remote.send_editor(content, self)
        else:
          self.remote.send_editor(" ", self)
      else:
        self.remote.receive_editor(self)
     
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
    msg = self.text_box.getText()
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
      self.remote.receive_chatmessage(self)
      msg = self.text_box.getText()
      self.remote.send_chatmessage(msg, self)
      self.text_box.setText("")
     
  def onQuitClick(self):
    # We're trying to quit, pause communications
    self.quitting = True
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
    self.quit_box.setPopupPosition(350, 200)  # (left, top)
    self.quit_box.show()
  def onQuitCancel(self):
    self.quit_box.hide()
    # we're not trying to escape anymore, restart regular communications
    self.quitting = False
  def onQuitConfirm(self):
    self.quit_box.hide()
    self.remote.sync_all(self)
    self.remote.user_quit(self)
