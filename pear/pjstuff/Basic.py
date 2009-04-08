from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, Label, HasAlignment, VerticalPanel, FlowPanel, TextArea, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton
from pyjamas import Window
from Menu import Menu, MenuCmd, onMenuInfoInfo

class Basic:
  def onModuleLoad(self):
    
    # the menu bar at the top
    self.menu_bar = Menu()
    # the ink button
    self.ink = Button("Ink", getattr(self, "onInkClick"))
    # the header (menu bar & title)
    self.banner = Image("images/header_no_description.jpg")
    self.banner.setHeight("24px")
    # put them together
    self.header = DockPanel()
    self.header.add(self.menu_bar, DockPanel.WEST)
    self.header.add(self.ink, DockPanel.WEST)
    self.header.add(self.banner, DockPanel.EAST)
    self.header.setCellWidth(self.menu_bar, "10%")
    self.header.setCellWidth(self.ink, "5%")
    self.header.setCellWidth(self.banner, "85%")
    self.header.setWidth("100%")
    self.header.setBorderWidth(1)
    
    # the left side
    # editor
    editor = TabPanel()
    plain = Frame("http://www.editpad.org/")
    plain.setWidth("100%")
    plain.setHeight("585px")
    editor_plain = SimplePanel()
    editor_plain.add(plain)
    editor_plain.setWidth("100%")
    editor_plain.setHeight("100%")
    highlight = Frame("http://helene.muze.nl/ariadne/loader.php/helene/demo/")
    highlight.setWidth("100%")
    highlight.setHeight("585px")
    editor_highlight = SimplePanel()
    editor_highlight.add(highlight)
    editor_highlight.setWidth("100%")
    editor_highlight.setHeight("100%")
    ink1 = Frame("http://www.williamfawcett.com/websketch/")
    # open source: http://rogue-development.com/experiments/DrawpadSandbox.swf
    # this one's not but it has nice features: http://www.scriblink.com/
    ink1.setWidth("100%")
    ink1.setHeight("585px")
    editor_ink1 = SimplePanel()
    editor_ink1.add(ink1)
    editor_ink1.setWidth("100%")
    editor_ink1.setHeight("409px")
    editor.add(editor_plain, "Plain Text Editor")
    editor.add(editor_highlight, "Syntax Highlighted Editor")
    editor.add(editor_ink1, "Ink Pad")
    editor.setWidth("100%")
    editor.setHeight("100%")
    editor.selectTab(0)
    
    # the right side
    vp = VerticalPanel()
    vp.setBorderWidth(1)
    # the console
    console = Label("Console")
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
    self.panel = DockPanel()
    self.panel.add(self.header, DockPanel.NORTH)
    self.panel.add(hp, DockPanel.CENTER)
    self.panel.add(self.footer, DockPanel.SOUTH)
    self.panel.setCellWidth(hp, "100%")
    self.panel.setCellHeight(hp, "100%")
    self.panel.setCellWidth(self.header, "100%")
    self.panel.setWidth("100%")
    self.panel.setHeight("100%")
    
    RootPanel().add(self.panel)
    
  def onInkClick(self):
    # highlighting
    high_check = CheckBox("Highlighter")
    Ink_high = FlowPanel()
    Ink_high.add(high_check)
    # pen
    pen_check = CheckBox("Pen")
    Ink_pen = FlowPanel()
    Ink_pen.add(pen_check)
    # clear ink marks
    
    # show/hide mouse to partner
    # put it together
    Ink_contents = VerticalPanel()
    Ink_contents.setSpacing(4)
    Ink_contents.add(Ink_high)
    Ink_contents.add(Ink_pen)
    Ink_contents.add(Button("Close", getattr(self, "onClose")))
    Ink_contents.setStyleName("Contents")
    
    self._dialog = DialogBox()
    self._dialog.setHTML('<b>Ink Settings</b>')
    self._dialog.setWidget(Ink_contents)    
    left = (Window.getClientWidth() - 200) / 2
    top = (Window.getClientHeight() - 100) / 2
    self._dialog.setPopupPosition(left, top)
    self._dialog.show()
    
  def onClose(self):
    self._dialog.hide()