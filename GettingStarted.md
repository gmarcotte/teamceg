# Preliminaries #

You must have the following installed:
  * Python 2.5 (http://www.python.org/download/releases/2.5.4/)
  * MySQL (http://dev.mysql.com/downloads/mysql/5.1.html)
  * python-mysql bindings (http://sourceforge.net/project/showfiles.php?group_id=22307&package_id=15775)

# Checkout #

Follow the instructions under the Source tab.  Make sure you actually check out the entire trunk folder.

# Vendor Setup #

Open a console and cd into the vendor directory.  Run the install.py script.


# Database Setup #

Run MySQL and log in as the root user (that you set up during installation).
Then run the following (you can replace pear\_user and PEAR333 with whatever
username and password you want (created in advance!)):
```
mysql> create database pear_sandbox;
mysql> grant all on pear_sandbox.* to pear_user identified by 'PEAR333';
mysql> quit;
```
Make sure you can log back in with the new user credentials.

Now copy the pear/environments/settings\_sandbox.py file into the pear
directory and rename it settings\_local.py.  Then change the DATABASE\_USER
and DATABASE\_PASSWORD variables to match the user you just created.

Now cd into the pear directory and run:
```
$ python manage.py syncdb
```

# Test the Setup #
From in the pear directory, run:
```
$ python manage.py shell
...python loads...
>> import django
>> import pear
>> import logilab.astng
>> import logilab.common
>> import pylint
>> quit()
...python exits...
$ python pear-pylint.py urls.py
```

In the current file, you have to move the import statement to **after** the path setting. (CCI)

You should not get any import errors in python, or complaints from django or pylint.  Pylint may give errors about the urls.py file (that's its job), but it should have
no problems running.

# Run the Tutorial App #

cd into the pear/media folder and run:
```
>> python build.py
```

It should run without errors, and eventually tell you to load the TodoApp.html file in a browser.  Don't do this, it won't work.  Instead you want to access it through Django.

cd back into the pear folder and start the local Django server:
```
$ python manage.py runserver
```

then open a browser and go to:

http://localhost:8000/site_media/output/TodoApp.html

Make sure the Task entry AJAX works properly (add with enter, click to delete)

Yay! All set up!