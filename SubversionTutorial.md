# Basic Subversion #

**NOTE: This tutorial was originally written for the web team of the
Daily Princetonian.  You will likely not have access to the repository
listed here.  I will see about changing it at some point, but in the
meantime, try to make it work using our Google Code repository wherever
the tutorial repository is listed.**

Also, Google Code generally requires the --username flag to be added
to all checkouts and commits.  Follow the instructions on the Source->Checkout
page, and use the password in your Google Code profile.


This tutorial covers operating Subversion from the command line.
Before doing this tutorial, make sure that Subversion is installed on your computer.


NOTE: Due to an unsigned certificate on our server, you may get a warning such as:
```
Error validating server certificate for 'https://svn.dailyprincetonian.com'
.....
(R)eject, abort, (t)emporarily, (p)ermanently?
```

This is expected, and will not cause any problems for your machine.  Whenever this appears, press p to accept the certificate.

### What is Subversion? ###
Subversion is a free, open-source version control system.  It provides:
  * Versioned file management that is able to remember every version of a given file or directory
  * Intelligently handling of changes to files so that multiple people can work on the same source simultaneously without overwriting each others' work.
  * Logging easily understand how files have changed over time.


### Running Subversion ###

Subversion is run from the terminal using the command:
```
  >> svn [subcommand]
```

You can see all the available subcommands by running:
```
  >> svn help
```

The rest of this tutorial covers the usage of some of these subcommands.

### Checkouts ###

All files and directories managed in Subversion are stored in a '''repository''', which is stored on our server.
The first step when you want to edit any files stored in a Subversion repository is to get the files from the
repository onto your local computer.  A local version of a Subversion repository is called a '''working copy'''.

The repository that we will use for this tutorial is located at: https://svn.dailyprincetonian.com/repos/svntut/

Run the following command to checkout a working copy of the svntut repository:

```
  >> svn checkout https://svn.dailyprincetonian.com/repos/svntut
```

You should now see a directory called svntut in your current working directory.

You can also use the shortened subcommand '''co''' in place of '''checkout''' and you can also name the
working copy directory something different than the repository name.  Let's check out another working copy
called "svntut-2" by running the command:

```
  >> svn co https://svn.dailyprincetonian.com/repos/svntut svntut-2
```

### Modifying Files ###

Now look in the newly created svntut directory.  You'll see that there is a directory called ''.svn'', which
contains information Subversion uses to manage the files.  Never change anything in the .svn directory.

You'll also see a file called ''attendance.txt''.  Open this file in your favorite editor, and add your name to
the "People Who Completed This Tutorial" list.  Now save the file and go back to the terminal.

Run the command:
```
  >> svn status
```

You should get the following output:
```
  M     attendance.txt
```

The "M" indicates that we have modified the working copy file attendance.txt.  It is important to note that we have not actually
changed attendance.txt in the repository yet.  Anyone that checks out a copy of svntut right now will not see our modifications.
This is one of the primary benefits of using Subversion.


### Adding Files and Directories ###

Now we're going to add a directory to the repository.  In all of the following commands, replace netID with your netID.
Create a directory called netID in the svntut directory.

Now run "svn status" again and you'll see the output:
```
  M      attendance.txt
  ?      netID
```

The ? indicates that the directory netID is not currently being managed by Subversion.

Now run the following commands to add the directory to the repository:
```
  >> svn add netID
  >> svn status
```

The results should be:
```
  M      attendance.txt
  A      netID
```

The "A" indicates that the directory netID has been added to Subversion control.

'''Exercise:''' Create a file called birthday.txt in the netID directory and add it to Subversion.

### Reverting Changes ###

Let's say that you make some changes to a working copy file, or add a file to Subversion, and then later
decide that's not actually what you want to do.  Since Subversion remembers all past versions of a file
in the repository, it is easy to revert any file or directory to the last version checked out of the repository.

Try reverting attendance.txt and your birthday.txt files by running the commands:
```
  >> svn revert attendance.txt
  >> svn revert netID/birthday.txt
  >> svn status
```

You should see the output:
```
  A    netID
  ?    netID/birthday.txt
```

The absence of attendance.txt indicates that it is unchanged from when it was originally checked out.  You can also
see that netID/birthday.txt is no longer under the control of Subversion.  Actually look at the contents of attendance.txt
and birthday.txt.  You'll see that revert actually removed your changes from attendance.txt, but left the contents of
birthday.txt unchanged.  This is an important point to note if you don't want to accidentally lose data: when you revert
a modified file, you permanently lose all changes that were made to the file; when you revert an added file, you simply remove
it from Subversion control and the contents are unchanged.

### Committing Changes ###

Now add birthday.txt back to Subversion and restore your name to the list in attendance.txt.  We're ready to send our changes
to the repository.  This is called "committing" changes, and is done with the ''commit'' command.

Each commit is accompanied by a log message.  WRITE INFORMATIVE LOG MESSAGES! The log messages provide a concise, readable record
for the changes that have been made to a repository.

Run the following command:
```
  >> svn commit -m "Adding netID to attendance list and creating directory and birthday file for netID."
```

The output should look like:
```
  Sending   attendance.txt
  Adding    netID
  Adding    netID/birthday.txt
  Transmitting file data .....
  Committed revision 7
```

Your revision number may differ, but you may notice that it is approximately 1 more than the revision you initially checked out.

You can also only commit certain files with a command like:
```
  svn commit file1.txt file2.txt -m "log message"
```


### Updating a Working Copy ###

If you now run "svn status", there should not be any output, indicating that all of the file in your working copy are unchanged
since you last committed changes or checked out files.

But now let's look at the other working copy we originally checked out, in the "svntut-2" directory.  You will notice that this
directory does not have your directory or birthday.txt file.  This again shows that once you checkout a working copy, the files in the working copy don't change
even if the repository files change.  You can force an update of your working copy, however, with the ''update'' command:
{{
> >> svn update
}}

You should see output like:
```
  M    attendance.txt
  A    netID
  A    netID/birthday.txt
  Updated to revision 7.
```

Again, the revision may differ, but it should the same as the revision that you just committed repository.  This indicates
that your working copy now includes all of your changes.  You can look at the files and directories to see that this is the case.

Subversion tries to be intelligent when it updates files.  For example, if you have made a change to a working copy file, and after you
checked it out someone else committed code that changes that file, Subversion will try to reconcile the changes within the file.  If
Subversion cannot reconcile the changes, a ''conflict'' occurs, and you must resolve it.  This does not happen too often, so we won't cover
it in this tutorial.  More information on conflicts, merging and resolution will be provided in the Advanced Subversion tutorial.


### Conclusion ###

Congratulations! You've now completed the Basic Subversion tutorial.  There are no additional exercises or submission necessary for this tutorial.
Key things to remember are:
  * Subversion keeps track of versions of files
  * Working copy files are totally separate from repository files, unless forcibly committed or updated.
  * Most common subcommands are: checkout, commit, add, revert, and status.
  * WRITE GOOD LOG MESSAGES!