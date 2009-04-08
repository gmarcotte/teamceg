from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, Label, HasAlignment, VerticalPanel, TextArea, Frame, NamedFrame, Image
from pyjamas import Window
from Menu import Menu, MenuCmd, onMenuInfoInfo

class Basic:
  def onModuleLoad(self):
    self.panel = DockPanel()
    
    # the header
    self.header = Image("images/header_no_description.jpg")
    self.header.setHeight("45px")
    
    # the menu bar at the top
    self.menu_bar = Menu()
    
    # the left side
    # editor
    editor = TabPanel()
    plain = Frame("http://www.editpad.org/")
    plain.setWidth("100%")
    plain.setHeight("540px")
    editor_plain = SimplePanel()
    editor_plain.add(plain)
    editor_plain.setWidth("100%")
    editor_plain.setHeight("100%")
    highlight = Frame("http://helene.muze.nl/ariadne/loader.php/helene/demo/")
    highlight.setWidth("100%")
    highlight.setHeight("540px")
    editor_highlight = SimplePanel()
    editor_highlight.add(highlight)
    editor_highlight.setWidth("100%")
    editor_highlight.setHeight("100%")
    editor.add(editor_plain, "Plain Text Editor")
    editor.add(editor_highlight, "Syntax Highlighted Editor")
    editor.setWidth("100%")
    editor.setHeight("100%")
    editor.selectTab(0)
    
    # the right side
    vp = VerticalPanel()
    vp.setBorderWidth(1)
    # the console
    console = Label("Console")
    #console = Frame("") # goosh.org didn't work :(
    #console.setWidth("100%")
    # text chat
    # use sth like "flash chat"? do you really want to write your own?..
    text_chat = Label("Text Chat")
    vp.add(console)
    vp.add(text_chat)
    vp.setWidth("100%")
    vp.setHeight("100%")
    vp.setCellHeight(console, "70%")
    vp.setCellHeight(text_chat, "30%")
    
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
    self.panel.add(self.header, DockPanel.NORTH)
    self.panel.add(self.menu_bar, DockPanel.NORTH)
    self.panel.add(hp, DockPanel.CENTER)
    self.panel.add(self.footer, DockPanel.SOUTH)
    self.panel.setCellWidth(hp, "100%")
    self.panel.setCellHeight(hp, "100%")
    self.panel.setWidth("100%")
    self.panel.setHeight("100%")
    
    RootPanel().add(self.panel)