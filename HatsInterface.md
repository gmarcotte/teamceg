# Introduction #

As per Ellen's conversation with Prof. D, it seems like a big sticking point for him is that we are not currently planning on interfacing with hats, and it seems like we would be able to get him on board as a "client" if we **do** interface with hats.

I think we would do well to interface with hats, and leave the squickiness of handling shell commands to hats, and focus more on shell emulation and synchronization. Also, this takes the burden of file maintenance/backup off of us, and gives our users an escape-route to their files if your server is down or if they don't want to use pairgramming some of the time.

Also, I think this fits a different role than we were originally thinking of, more as a mediator between the user and a separate server and less acting as the server ourselves. This also might allow us to interface with more and varied types of servers, if we leave the interaction with the server (other than basic directory/file setup) to the user.

# Underlying Technologies/Strategies #
  1. We can generate a private SSH key for each user once and then never ask them for their LDAP password again. This will allow us to log into hats on their behalf forever after without making them give us their LDAP password every time, which is desirable.
  1. We can set permissions on specific folders such that the folder lives in the "owner's" directory on hats, but that the partner and ONLY the partner can access it as well.

# Changes to Registration #
When users register, they must give us a legitimate LDAP username (we can interface with LDAP CAS to verify this without getting the plain-text password just to verify their username, and to verify partner's usernames)

Registration Steps
  1. User gives us their LDAP username, first name, last name, email, year, major
  1. We verify the username to be legitimate and immediately tell the user (ie "your username has been verified, and you will receive an email with a temporary password soon)
  1. The first time the user logs in
    1. We generate the private/public RSA key pair
    1. We have the user log in to hats through us (ie giving us their ldap password)
    1. We set the SSH settings to allow us to use this private RSA key (script running in the background) [ALSO: We can also allow squeamish users to do this themselves if they don't want to give us their LDAP password, and give them instructions for how to set the keys that we generate for them.]
    1. We create a directory in the user's home directory: >~/pairgramming

# Project Creation #
  1. Owner
    1. Create a directory on hats in the owner's pairgramming directory with this project name: >~/pairgramming/projectname
    1. Grant permissions to the partner (must know partner's ldap username): chmod partnername+rwx
  1. Partner
    1. When partner logs in and selects the project, we make a symbolic link in their pairgramming directory to the project directory in the owner's pairgramming directory


# Independent Mode #
  1. Make 2 new folders in the project folder (user1, user2) and do the equivalent of an svn checkout into them.
  1. Automatically cd each user into their respective folder.
  1. Let each person edit their files
  1. SVN-style merge when they re-synch
This may actually be preferable to our other design, because they can edit the same files if they want and then merge them.


# The Shell #
  * Takes commands from the user verbatim
  * Displays response from hats verbatim
  * Should feel exactly like you're typing into bash on your local machine ssh-ed into hats
  * Should we allow multiple shell windows to be open?

# The Editor #
  * Emacs + mouse?
  * Use the file-browser to open directly into the editor (in independent mode be certain to open the right version)
  * Buffer files on our server for faster editing (if the user is editing a file in the editor and not in the shell in emacs)

