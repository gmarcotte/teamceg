from Basic import Basic
from pyjamas.ui import MenuBar, MenuItem, Frame
from pyjamas import Window

class Menu(MenuBar):

  def __init__(self):
    MenuBar.__init__(self)
    
    # info
    menu_info = MenuBar(vertical=True)
    menu_info.addItem("User: ellenkim, Partner: bwk", MenuCmd(self, "onMenuInfoInfo"))
    
    # mode
    menu_mode = MenuBar(vertical=True)
    collab_menu = MenuBar(vertical=True)
    collab_menu.addItem("<b>User 1</b>", True, MenuCmd(self, "onCollabUser1"))
    collab_menu.addItem("User 2", True, MenuCmd(self, "onCollabUser2"))
    indep_menu = MenuBar(vertical=True)
    indep_menu.addItem("Synchronize", True, MenuCmd(self, "onIndepSync"))
    indep_menu.addItem("Discard changes", True, MenuCmd(self, "onIndepDisc"))
    menu_mode.addItem("Collaborative mode &#187;", True, collab_menu)
    menu_mode.addItem("Independent mode &#187;", True, indep_menu)
    
    # ink
    menu_ink = MenuBar(vertical=True)
    menu_ink.addItem("Highlight", True, MenuCmd(self, "onMenuInk"))
    menu_ink.addItem("Pen", True, MenuCmd(self, "onMenuInk"))
    menu_ink.addItem("Clear marks", True, MenuCmd(self, "onMenuInk"))
    menu_ink.addItem("Show/hide mouse", True, MenuCmd(self, "onMenuInk"))

    # audio
    menu_audio = MenuBar(vertical=True)
    menu_audio.addItem("Mic controls", True, MenuCmd(self, "onMenuAudioMic"))
    menu_audio.addItem("Volume controls", True, MenuCmd(self, "onMenuAudioVolume"))

    # files
    menu_files = MenuBar(vertical=True)
    menu_files.addItem("I'll need to look into whether I can put a tree here; but do we really want to make them click \"files\" before showing them the file tree?  Should it pop up in a dockable window or...?  Should we have a \"miscellaneous\" section on the screen where stuff like this goes?", True)

    # put menu bar all together
    self.addItem(MenuItem("Info", menu_info))
    self.addItem(MenuItem("Mode", menu_mode))
    self.addItem(MenuItem("Audio", menu_audio))
    self.addItem(MenuItem("Files", menu_files))

  def onMenuInfoInfo(self):
    Window.alert("You want more info?  I don't have any more.")
    
  def onCollabUser1(self):
    Window.alert("User 1 is already 'driving'")
    
  def onCollabUser2(self):
    Window.alert("So you want User 2 to drive?")
    
  def onIndepSync(self):
    Window.alert("You are submitting your changes to svn control")
    
  def onIndepDisc(self):
    Window.alert("You will lose all changes since last synchronize point")
    
  def onMenuInk(self):
    Ink_contents = Frame("www.google.com/")
    Window.alert(Ink_contents)
  
  def onMenuAudioMic(self):
    Window.alert("This should pop open a microphone controls window")
  
  def onMenuAudioVolume(self):
    Window.alert("Let them change how loud the volume is from this app without making them turn down the entire system volume")
    
class MenuCmd:
  def __init__(self, object, handler):
    self._object = object
    self._handler = handler
    
  def execute(self):
    handler = getattr(self._object, self._handler)
    handler()