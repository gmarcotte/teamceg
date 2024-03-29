"""Manipulation of upstream change log files.

The upstream change log files format handled is simpler than the one
often used such as those generated by the default Emacs changelog mode.

Sample ChangeLog format::

  Change log for project Yoo
  ==========================
  
   --
      * add a new functionnality

  2002-02-01 -- 0.1.1
      * fix bug #435454
      * fix bug #434356
    
  2002-01-01 -- 0.1
      * initial release
    

There is 3 entries in this change log, one for each released version and one
for the next version (i.e. the current entry).
Each entry contains a set of messages corresponding to changes done in this
release.
All the non empty lines before the first entry are considered as the change
log title.

:copyright: 2003-2008 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

import sys
from stat import S_IWRITE

BULLET = '*'
SUBBULLET = '-'
INDENT = ' ' * 4

class NoEntry(Exception):
    """raised when we are unable to find an entry"""

class EntryNotFound(Exception):
    """raised when we are unable to find a given entry"""

class Version(tuple):
    """simple class to handle soft version number has a tuple while
    correctly printing it as X.Y.Z
    """
    def __new__(klass, versionstr):
        if isinstance(versionstr, basestring):
            versionstr = versionstr.strip(' :')
            try:
                parsed = [int(i) for i in versionstr.split('.')]
            except ValueError, ex:
                raise ValueError("invalid literal for version '%s' (%s)"%(versionstr,ex))
        else:
            parsed = versionstr
        return tuple.__new__(klass, parsed)
        
    def __str__(self):
        return '.'.join([str(i) for i in self])

# upstream change log #########################################################

class ChangeLogEntry(object):
    """a change log entry, ie a set of messages associated to a version and
    its release date
    """
    version_class = Version
    
    def __init__(self, date=None, version=None, **kwargs):
        self.__dict__.update(kwargs)
        if version:
            self.version = self.version_class(version)
        else:
            self.version = None
        self.date = date
        self.messages = []
        
    def add_message(self, msg):
        """add a new message"""
        self.messages.append(([msg],[]))

    def complete_latest_message(self, msg_suite):
        """complete the latest added message
        """
        if not self.messages:
            raise ValueError('unable to complete last message as there is no previous message)')
        if self.messages[-1][1]: # sub messages
            self.messages[-1][1][-1].append(msg_suite)
        else: # message
            self.messages[-1][0].append(msg_suite)

    def add_sub_message(self, sub_msg, key=None):
        if not self.messages:
            raise ValueError('unable to complete last message as there is no previous message)')
        if key is None:
            self.messages[-1][1].append([sub_msg])
        else:
            raise NotImplementedError("sub message to specific key are not impemented yet")

    def write(self, stream=sys.stdout):
        """write the entry to file """
        stream.write('%s  --  %s\n' % (self.date or '', self.version or ''))
        for msg, sub_msgs in self.messages:
            stream.write('%s%s %s\n' % (INDENT, BULLET, msg[0]))
            stream.write(''.join(msg[1:]))
            if sub_msgs:
                stream.write('\n')
            for sub_msg in sub_msgs:
                stream.write('%s%s %s\n' % (INDENT * 2, SUBBULLET, sub_msg[0]))
                stream.write(''.join(sub_msg[1:]))
            stream.write('\n')

        stream.write('\n\n')

class ChangeLog(object):
    """object representation of a whole ChangeLog file"""
    
    entry_class = ChangeLogEntry
    
    def __init__(self, changelog_file, title=''):
        self.file = changelog_file
        self.title = title
        self.additional_content = ''
        self.entries = []
        self.load()

    def __repr__(self):
        return '<ChangeLog %s at %s (%s entries)>' % (self.file, id(self),
                                                      len(self.entries))
    
    def add_entry(self, entry):
        """add a new entry to the change log"""
        self.entries.append(entry)

    def get_entry(self, version='', create=None):
        """ return a given changelog entry
        if version is omited, return the current entry 
        """
        if not self.entries:
            if version or not create:
                raise NoEntry()
            self.entries.append(self.entry_class())
        if not version:
            if self.entries[0].version and create is not None:
                self.entries.insert(0, self.entry_class())
            return self.entries[0]
        version = self.version_class(version)
        for entry in self.entries:
            if entry.version == version:
                return entry
        raise EntryNotFound()

    def add(self, msg, create=None):
        """add a new message to the latest opened entry"""
        entry = self.get_entry(create=create)
        entry.add_message(msg)
    
    def load(self):
        """ read a logilab's ChangeLog from file """
        try:
            stream = open(self.file)
        except IOError:
            return
        last = None
        expect_sub = False
        for line in stream.readlines():
            sline = line.strip()
            words = sline.split()
            # if new entry
            if len(words) == 1 and words[0] == '--':
                expect_sub = False
                last = self.entry_class()
                self.add_entry(last)
            # if old entry
            elif len(words) == 3 and words[1] == '--':
                expect_sub = False
                last = self.entry_class(words[0], words[2])
                self.add_entry(last)
            # if title
            elif sline and last is None:
                self.title = '%s%s' % (self.title, line)
            # if new entry
            elif sline and sline[0] == BULLET:
                expect_sub = False
                last.add_message(sline[1:].strip())
            # if new sub_entry
            elif expect_sub and sline and sline[0] == SUBBULLET:
                last.add_sub_message(sline[1:].strip())
            # if new line for current entry
            elif sline and last.messages:
                last.complete_latest_message(line)
            else:
                expect_sub = True
                self.additional_content += line
        stream.close()
        
    def format_title(self):
        return '%s\n\n' % self.title.strip()
    
    def save(self):
        """write back change log"""
        # filetutils isn't importable in appengine, so import locally
        from logilab.common.fileutils import ensure_fs_mode
        ensure_fs_mode(self.file, S_IWRITE)
        self.write(open(self.file, 'w'))
            
    def write(self, stream=sys.stdout):
        """write changelog to stream"""
        stream.write(self.format_title())
        for entry in self.entries:
            entry.write(stream)

