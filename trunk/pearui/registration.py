from pyjamas.ui import SimplePanel, FormPanel, VerticalPanel, HorizontalPanel, TextBox, Label, Button

class registration():
    def __init__(self):
        SimplePanel.__init__(self)

        self.form = FormPanel()

        vp = VerticalPanel()
        vp.add(HTML("E-mail address:"))
        vp.add(self.createTextThing(self.fTextBox))
        vp.add(HTML("Password:"))
        vp.add(self.createTextThing(self.fPasswordText))
        vp.add(HTML("Confirm password:"))
        vp.add(self.createTextThing(self.fPasswordText))
        vp.add(HTML("First name:"))
        vp.add(self.createTextThing(self.fTextBox))
        vp.add(HTML("Last name:"))
        vp.add(self.createTextThing(self.fTextBox))
        vp.add(HTML("Class year:"))
        vp.add(self.createTextThing(self.fTextBox))
        vp.add(HTML("Major:"))
        vp.add(self.createTextThing(self.fTextBox))

        vp.add(Button("Create my account!", getattr(self, "onBtnClick")))

        self.form.add(vp)
        self.add(self.form)

    def createTextThing(self, textBox):
        hp = HorizontalPanel()
        hp.add(textBox)
        return hp

    def onBtnClick(self):
        self.form.submit()


    #def onSubmitComplete(self, event):
        # When the form submission is successfully completed, this event is
        # fired. Assuming the service returned a response of type text/plain,
        # we can get the result text here (see the FormPanel documentation for
        # further explanation).
        #Window.alert(event.getResults())

    #def onSubmit(self, event):
        # This event is fired just before the form is submitted. We can take
        # this opportunity to perform validation.
        #if (self.tb.getText().length == 0):
            #Window.alert("The text box must not be empty")
            #event.setCancelled(true)