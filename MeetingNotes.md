# Introduction #
Running record of notes from our team meetings.

# Thu, May 7 #
## CEG meeting ##
  1. Temporarily fixed chat (yes, ajaxterm was stealing focus)
  1. File tree UI set up
  1. Prepared demo presentation
  1. Got Editor set up for two users, pushed to server

# Wed, May 6 #
## CEG ish meeting ##
  1. (what did we accomplish in ele lab?..)

# Tue, May 5 #
## Individual ##
  1. Started demo presentation
  1. Update timeline to present
  1. Worked on editor
  1. (anything else you guys worked on Tues)

# Fri, May 1 #
## CEG Meeting ##
  1. (I'm not sure what you guys worked on.. please update)
  1. Some more UI changes/fixes

## Individual ##
  1. Pyjamas Quit button takes us back to django homepage

# Thu, April 30 #
## Group Meeting ##
  1. Made more progress on UI bugs/changes
  1. Pushed text chat to the server
  1. Got the new editor integrated, but will have to do significant work to write the python wrapper so that we can interact with it through pyjamas/django
  1. Worked on getting ajaxterm going.

# Sun, April 27 #
## Individual ##
  1. Chat is in HTML
  1. Fixed more Pyjamas/UI bugs

# Sat, April 26 #
## Individual ##
  1. Chat implemented -- clunky but works
  1. Meetings model finished
  1. Chat model finished

## CEG Meeting ##
  1. Progress on Meetings model (formerly Sessions, but Django already has Sessions..); can launch a Meeting, & partner can launch and be added as Passenger
  1. Started integration of Meetings info with UI (Driver, Passenger)
  1. One-person basic chat implemented
  1. Major change to menu UI

# Fri, April 25 #
## Group Meeting ##
  1. Added basic Audio and Mode boxes to menu
  1. Added post-registration welcome page
  1. Added delete account e-mail contents
  1. Worked on SSH on our server
  1. Worked on Sessions

# Thu, April 24 #
## Group Meeting ##
  1. Fixed more Helene bugs
  1. Wrote console listener
  1. Got username into Info popup (yay Django+Pyjamas)
  1. Finished SSH stuff, but haven't been able to test it yet (doesn't work in Windows)

## For Tomorrow ##
  * Test SSH stuff
  * Work out sessions stuff!
  * Intelligently launch sessions from Django

# Wed, April 23 #
## Group Meeting ##
  1. Got console running on web server
  1. Flash condensed to 1 button
  1. More bug fixing in Helene/console

# Mon, April 20 #
## Group Meeting ##
  1. Did the first integration of pyjamas and django
  1. Updated the server

## Individual Work for Next Time ##
  1. Write up ssh documentation (C)
  1. Write up webserver update procedure (G)

# Thu, April 16 #
## Group Meeting ##
  1. Got the webserver working
  1. Integrated Helene into pyjamas
  1. Worked on tool-tip as mouse display
  1. Decided we don't want to write our own audio code after all (><); possibility includes embedding skype links
  1. Got a basic listener text-area working

## Individual Progress ##
  1. Fixed several bugs in Helene editor code
  1. Got flash working for the window


# Wed, April 15 #
## Group Meeting ##
Met briefly with whole group.
  1. Progress slower than we wanted (car lab and independent work issues)
  1. C - finished remote ssh execution code for our remote scripts
  1. E - window flash
  1. G - will work on server
  1. Committing to using Helene v. 9 (C fixed highlighting offset bug)
## To Do Tomorrow ##
  1. Finish setting up webserver and link pyjamas and django
  1. Decide how to approach audio and then, based on that, text chat
  1. Start write-up
  1. Basic flash

# Fri, April 10 #
  1. Started setting up server, decided to switch to just using plain mac server
  1. Started experimenting with embedding javascript in panels directly rather than using frames
  1. Looked at open source text editor/audio/chat


# Thu, April 9 #
## For the Alpha Test ##
  1. Django done
  1. Console finished (in IE/Safari and Firefox)
  1. Session Plumbing
  1. Text Chat
  1. Audio
  1. File tree/navigation
  1. Webserver up

## To Demo Next Week ##
  1. Single user file editing and console functionality
  1. Webserver

## To Demo Tomorrow (Prototype) ##
  1. Setting up server connections
    1. file tree
    1. text editor
  1. Preliminary project stuff
  1. Demo of console and UI

## Planning ##
  1. Django finalization - This week -> Garrett
  1. Session Plumbing - This weekend -> Christina (Garrett)
  1. Switch Drivers
  1. SVN/ file in/out, clean sync/update - Started by Next Week -> Garrett
  1. Console - Finish this week -> Christina
  1. Text Editor w/ highlighting
  1. Text Chat - This week -> Christina/Ellen
  1. Audio - This week -> Ellen
  1. Cursor (viewable by both users)
  1. Interface
  1. User settings/configuration
  1. Inking Tab
  1. File Tree - Next Week -> Garrett (UI Ellen)
  1. Additional Tabs
  1. Ping/Flash
  1. Integrating Pyjamas with Django

## Group Progress ##
  * UI considerably more spiffy
  * Worked on getting webserver working
  * Worked on making console compatible with IE and safari (keypress events are not being issued properly)

### Web Server ###
  * Tried getting basic port forwarding to work (we already have ssh capabilities) as per the vmware documentation

# Wed, April 8 #
## Progress ##
  * Ellen got the basic user interface written in pyjamas
  * Christina got the console hooked into the basic UI
Ready to do a basic demo on Friday

# Sat, April 4 #
## Group Progress ##
### For Next Time ###
  1. Set up console
  1. Finish up all Django site setup
  1. Prepare for prototype demo on Fri 4/10
### Accomplished ###
  1. Look into open src console
  1. Join a public project
  1. Invite someone to create a Pairgramming account
  1. Add partner to existing project

# Fri, April 3 #
## Group Progress ##
### For Next Time ###
  1. User join project (already existing)
  1. Subversion Interface to project files
  1. Streaming for SSH/etc.
  1. Web-server accessible

### Accomplished ###
  1. SSH Connection and RSA key pair Generation
  1. Admin Interface for all models
  1. SSH connection model and configuration by user
  1. Project model
  1. User project creation
  1. User project index
## TA Meeting ##
Met with Peng and discussed our project from the prior week, demo-ed our user registration/login
  * One issue we ran into was gmail requiring us to login manually for the pairgramming account using a CAPTCHA, this may be an issue going forward, but we are not sure

# Thu, April 2 #
## Progress ##
  * Met with Prof. Dondero and discussed some design changes, enlisted him as client and tester

# Sat, March 28 #
## Progress ##
  * Can now actually get into the testbed server remotely
  * Christina got user authentication partially working

## Group Work ##
  1. User Login
  1. Email users with initial passwords
  1. Setup pairgramming@gmail.com
  1. Setup reset password
  1. Setup password changing and email
  1. Some changes to UI including banner
  1. Account Deletion
  1. Account Deletion email

# Thu, March 26 #
## Group Work ##
  * Started some real coding!
    * Garrett started working on authentication stuff
    * Christina started working on interfacing with LDAP and wrote the profile, project and course models
    * Ellen started working on the front-end of the login page in Pyjamas
  * Started learning how to compile Pyjamas to javascript and actually test our stuff
  * Decided to use Django forms for registration, login and project selection

## Current Functionality ##
  * Got registration working
    * Still cannot login
    * Do not send emails with random passwords yet
    * Data **is** stored in the database

## Model Structure ##
### Profile ###
  * major
  * class year
### Project ###
  * programmers (model User)
  * course (model Course)
### Course ###
  * name
  * department
  * course number
  * professor (model User) (still a wishlist feature)
  * year
  * semester
  * TAs (model User) (still a wishlist feature)
We put in some things that we might not end up using so that just in case we have time we won't have to make changes to our basic model types.

## Authentication Scheme ##
  1. User navigates to our page
  1. We re-direct them to LDAP
  1. They authenticate themselves
  1. We use the returned netid as their username
Authentication and project selection are going to be in Django. We will only use Pyjamas once we are actually in the Pairgramming part of the site.


# Tue, March 24 #
## Spring Break Progress ##
  * Minimal progress
  * Testbed server now ssh-able
  * Tutorials completed

## During Meeting ##
  * Setup server so we can program on the server
  * Got Ellen's local machine working

# Mon, March 9 #

## For This Week and Spring Break ##
  * Christina
    * needs to get the server working, seems like there might be an issue with OIT and our server doing evil NAT things
    * Pyjamas HelloWorld
  * Ellen
    * Pyjamas HelloWorld
  * Garrett
    * Pyjamas HelloWorld

## Working on the Design Document ##
  * Ellen did some preliminary work on the design document over the weekend
  * Christina and Garrett mostly finished it together today
  * Whole group met to go over the final design document
  * Design document is done?



# Sun, March 1 #

## For Next Week ##
  * Start working on the design document (this is due right before spring break).
  * Try to be able to connect to our sever (waiting on response from OIT).

## Server Notes ##
Ubuntu server has been installed on old mac. Seems to be working at least locally, but we cannot ping it or ssh to it. We sent a request to OIT to figure out how to make this work. The alias is teamceg.princeton.edu.

Server also has Django already.

## Pyjamas and other Things ##
Pyjamas, Django and a few other things are now in source.

## SVN ##
Everyone now is able to checkout from SVN and has a version of trunk on their local machine.



# Sun, Feb 22 #

## Discuss Design Ideas ##

### Container ###

  * Flashable
  * Pop-out
  * In-place resize
  * Drag & drop

### Configuration Options ###
  * Flash rate
  * Ping noise on/off

### Revision Browser ###

### Sketch Pad ###
  * Save
  * Draw

### File Navigator ###
  * Color scheme
  * Tree structure
  * Buttons for operation

### Interactive (AJAX) Text Windows ###
#### All can ink highlight ####
#### Code (Editor & Eavesdrop) ####
  * Syntax highlighting
  * Monospaced font
  * Synch to server (project-level)
  * Discard changes since last synch (project-level)
  * Save a working copy (user-level)
#### Text Chat ####
#### Console ####
  * Monospaced font
  * Commands: compile, run, debug

### Technologies ###
  * PyJamas, Django, Testbed Server