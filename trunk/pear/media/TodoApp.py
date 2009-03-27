from ui import Label, RootPanel, VerticalPanel, TextBox, KeyboardListener, ListBox
from JSONService import JSONProxy
  
class TodoApp:
  def onModuleLoad(self):
    self.remote = DataService()
    panel = VerticalPanel()

    self.todoTextBox = TextBox()
    self.todoTextBox.addKeyboardListener(self)

    self.todoList = ListBox()
    self.todoList.setVisibleItemCount(7)
    self.todoList.setWidth("400px")
    self.todoList.addClickListener(self)

    panel.add(Label("Add New Todo:"))
    panel.add(self.todoTextBox)
    panel.add(Label("Click to Remove:"))
    panel.add(self.todoList)
    RootPanel().add(panel)


  def onKeyUp(self, sender, keyCode, modifiers):
    pass
  
  def onKeyDown(self, sender, keyCode, modifiers):
    pass
  
  def onKeyPress(self, sender, keyCode, modifiers):
    """
    This functon handles the onKeyPress event, and will add the item in the text box to the list when the user presses the enter key.  In the future, this method will also handle the auto complete feature.
    """
    if keyCode == KeyboardListener.KEY_ENTER and sender == self.todoTextBox:
      id = self.remote.addTask(sender.getText(),self)
      sender.setText("")
      
    if id<0:
      self.todoList.setText("error")
      console.error("Server Error or Invalid Response")


  def onClick(self, sender):
    id = self.remote.deleteTask(sender.getValue(sender.getSelectedIndex()),self)
    if id<0:
      console.error("Server Error or Invalid Response")

  def onRemoteResponse(self, response, request_info):
    console.info("response received")
    if request_info.method == 'getTasks' or request_info.method == 'addTask' or request_info.method == 'deleteTask':
      console.info("HERE!")
      self.todoList.clear()
      for task in response:
        self.todoList.addItem(task[0])
        self.todoList.setValue(self.todoList.getItemCount()-1,task[1])
    else:
      console.error("none!")

  def onRemoteError(self, code, message, request_info):
    self.todoTextBox.setText("SERIOUS ERROR")
    self.todoList.addItem(message)
    self.todoList.addItem(code)
    self.todoList.addItem(request_info)
    console.error("Server Error or Invalid Response: ERROR " + code + " - " + message)

class DataService(JSONProxy):
  def __init__(self):
    JSONProxy.__init__(self, "/services/", ["getTasks", "addTask","deleteTask"])

