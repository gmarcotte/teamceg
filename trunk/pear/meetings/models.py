#
#  models.py
#  sandbox
#
#  Created by Christina Ilvento on 4/24/09.
#  Copyright (c) 2009 Princeton University. All rights reserved.
#
from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

from pear.core import timestamp

import pear.accounts.models
import pear.projects.models


class ChatMessage(timestamp.TimestampedModel):
  # actual message
  message = models.TextField()
  # to-user
  receiver = models.ForeignKey(pear.accounts.models.PearUser, related_name='messages_received', null=True)
  # from-user
  sender = models.ForeignKey(pear.accounts.models.PearUser, related_name='messages_sent')

class Meeting(timestamp.TimestampedModel):
  # Driver
  driver = models.ForeignKey(pear.accounts.models.PearUser, related_name='driver_for')
  # Passenger
  passenger = models.ForeignKey(pear.accounts.models.PearUser, related_name='passenger_for', null=True)
  # Project
  project = models.ForeignKey(pear.projects.models.Project)
  # Console session id for driver and passenger
  passengerconsole = models.IntegerField(null=True)
  driverconsole = models.IntegerField()
  # ssh connections for driver and passenger
  passengerssh = models.ForeignKey(pear.remote.models.SSHConnection, related_name='active')
  driverssh = models.ForeignKey(pear.remote.models.SSHConnection, related_name='inactive', null=True)
  # Editor state -- Note that we might need to change this to deal with maliciously long documents
  editor = models.TextField()
  # Chat state (queue of messages for each user and all messages)
  unsent_messages = models.ManyToManyField(ChatMessage, related_name='unsent', null=True)
  sent_messages = models.ManyToManyField(ChatMessage, related_name='sent', null=True)
  # Ping/Flash state
  flash = models.BooleanField()



