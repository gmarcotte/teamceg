# Copyright 2006 James Tauber and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyjamas import DOM
#from PopupPanel import PopupPanel
from pyjamas.ui import PopupPanel

class MenuBarPopupPanel(PopupPanel):
    def __init__(self, item):
        self.item = item
        PopupPanel.__init__(self, True)

        self.setWidget(item.getSubMenu())
        item.getSubMenu().onShow()

    def onEventPreview(self, event):
        type = DOM.eventGetType(event)
        if type == "click":
            target = DOM.eventGetTarget(event)
            parentMenuElement = self.item.getParentMenu().getElement()
            if DOM.isOrHasChild(parentMenuElement, target):
                return False
        return PopupPanel.onEventPreview(self, event)


