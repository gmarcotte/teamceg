#
#  admin.py
#  sandbox
#
#  Created by Christina Ilvento on 4/24/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django.contrib import admin

from pear.meetings import models

class SessionOptions(admin.ModelAdmin):
  list_display = ('driver','passenger','project','console','editor','unsent_messages','sent_messages','flash')

#admin.site.register(models.Session, SessionOptions)