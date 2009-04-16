from pyjamas.ui import RootPanel, HTML, MenuBar, MenuItem, DockPanel, HorizontalPanel, TabPanel, SimplePanel, Label, HasAlignment, VerticalPanel, FlowPanel, TextArea, TextBox, Frame, NamedFrame, Image, Button, DialogBox, CheckBox, RadioButton, HTMLPanel
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
    self.header.setCellWidth(self.menu_bar, "11%")
    self.header.setCellWidth(self.ink, "3%")
    self.header.setCellWidth(self.banner, "86%")
    self.header.setWidth("100%")
    self.header.setBorderWidth(0)
    
    # the left side
    # editor
    editor = TabPanel()
    plain = Frame("http://www.editpad.org/")
    plain.setWidth("100%")
    plain.setHeight("657px")
    editor_plain = SimplePanel()
    editor_plain.add(plain)
    editor_plain.setWidth("100%")
    editor_plain.setHeight("100%")
    highlight = Frame("http://helene.muze.nl/ariadne/loader.php/helene/demo/")
    highlight.setWidth("100%")
    highlight.setHeight("657px")
    editor_highlight = SimplePanel()
    editor_highlight.add(highlight)
    editor_highlight.setWidth("100%")
    editor_highlight.setHeight("100%")
    ink1 = Frame("http://www.williamfawcett.com/websketch/")
    # open source: http://rogue-development.com/experiments/DrawpadSandbox.swf
    # this one's not but it has nice features: http://www.scriblink.com/
    ink1.setWidth("100%")
    ink1.setHeight("657px")
    editor_ink1 = SimplePanel()
    editor_ink1.add(ink1)
    editor_ink1.setWidth("100%")
    editor_ink1.setHeight("600px")
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
    term = Frame("http://127.0.0.1:8023/")
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
    #fake_chat = VerticalPanel()
    #fake_chat.add(text_area)
    #fake_chat.add(text_entry)
    #fake_chat.setCellHeight(text_area, "215px")
    #fake_chat.setCellHeight(text_entry, "35px")
    #id1 = Panel.createUniqueId()
    #id2 = HTMLPanel.createUniqueId()
    #html = HTML('<div id="term"></div>')
    js_tester = HTMLPanel(" my text in here. <script> myfunction(); </script> <div id='lame'></div>")
    #js_tester = SimplePanel()
    
    #js_tester.add(Button("Hi there"), id1)
    #js_tester.add(Label("This label intentionally left blank"), id2)
    vp.add(console)
    vp.add(js_tester)
    #js_tester.add(html)
    #vp.add(fake_chat)
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