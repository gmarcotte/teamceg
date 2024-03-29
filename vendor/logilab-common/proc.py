"""module providing:
* process information (linux specific: rely on /proc)
* a class for resource control (memory / time / cpu time)

:organization: Logilab
:copyright: 2007-2008 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

import os
from os.path import exists
import stat

from logilab.common.tree import Node

class NoSuchProcess(Exception): pass

def proc_exists(pid):
    """check the a pid is registered in /proc
    raise NoSuchProcess exception if not
    """
    if not exists('/proc/%s' % pid):
        raise NoSuchProcess()

PPID = 3
UTIME = 13
STIME = 14
CUTIME = 15
CSTIME = 16
VSIZE = 22

class ProcInfo(Node):
    """provide access to process information found in /proc"""

    def __init__(self, pid):
        self.pid = int(pid)
        Node.__init__(self, self.pid)
        proc_exists(self.pid)
        self.file = '/proc/%s/stat' % self.pid
        self.ppid = int(self.status()[PPID])

    def memory_usage(self):
        """return the memory usage of the process in Ko"""
        try :
            return int(self.status()[VSIZE])
        except IOError:
            return 0
    
    def lineage_memory_usage(self):
        return self.memory_usage() + sum(child.lineage_memory_usage() for child in self.children)

    def time(self, children=0):
        """return the number of jiffies that this process has been scheduled
        in user and kernel mode"""
        status = self.status()
        time = int(status[UTIME]) + int(status[STIME])
        if children:
            time += int(status[CUTIME]) + int(status[CSTIME])
        return time

    def status(self):
        """return the list of fields found in /proc/<pid>/stat"""
        return open(self.file).read().split()

    def name(self):
        """return the process name found in /proc/<pid>/stat
        """
        return self.status()[1].strip('()')

    def age(self):
        """return the age of the process
        """
        return os.stat(self.file)[stat.ST_MTIME]

class ProcInfoLoader:
    """manage process information"""
    
    def __init__(self):
        self._loaded = {}

    def list_pids(self):
        """return a list of existant process ids"""
        for subdir in os.listdir('/proc'):
            if subdir.isdigit():
                yield int(subdir)

    def load(self, pid):
        """get a ProcInfo object for a given pid"""
        pid = int(pid)
        try:
            return self._loaded[pid]
        except KeyError:
            procinfo = ProcInfo(pid)
            procinfo.manager = self
            self._loaded[pid] = procinfo
            return procinfo
        
    
    def load_all(self):
        """load all processes information"""
        for pid in self.list_pids():
            try:
                procinfo = self.load(pid)
                if procinfo.parent is None and procinfo.ppid:
                    pprocinfo = self.load(procinfo.ppid)
                    pprocinfo.append(procinfo)
            except NoSuchProcess:
                pass


import tempfile
import traceback
from signal import signal
try:
    from signal import SIGXCPU, SIGKILL, SIGUSR2, SIGUSR1
    from os import killpg, getpid, setpgrp
    from resource import getrlimit, setrlimit, RLIMIT_CPU, RLIMIT_AS
except ImportError:
  pass

from threading import Timer, currentThread, Thread, Event
from time import time



try:
    class ResourceError(BaseException):
        """Error raise when resource limit is reached"""
        limit = "Unknow Resource Limit"
except NameError:
    class ResourceError(Exception):
        """Error raise when resource limit is reached"""
        limit = "Unknow Resource Limit"


class XCPUError(ResourceError):
    """Error raised when CPU Time limite is reached"""
    limit = "CPU Time"

class LineageMemoryError(ResourceError):
    """Error raised when the total amount of memory used by a process and
    it's child is reached"""
    limit = "Lineage total Memory"

class TimeoutError(ResourceError):
    """Error raised when the process is running for to much time"""
    limit = "Real Time"

# Can't use subclass because the StandardError MemoryError raised
RESOURCE_LIMIT_EXCEPTION = (ResourceError, MemoryError)

try:
  class MemorySentinel(Thread):
      """A class checking a process don't use too much memory in a separated
      daemonic thread
      """
      def __init__(self, interval, memory_limit, gpid=getpid()):
          Thread.__init__(self, target=self._run, name="Test.Sentinel")
          self.memory_limit = memory_limit
          self._stop = Event()
          self.interval = interval
          self.setDaemon(True)
          self.gpid = gpid
          
      def stop(self):
          """stop ap"""
          self._stop.set()
          
      def _run(self):
          pil = ProcInfoLoader()
          while not self._stop.isSet():
              if self.memory_limit <= pil.load(self.gpid).lineage_memory_usage():
                  killpg(self.gpid, SIGUSR1)
              self._stop.wait(self.interval)
except NameError:
  class MemorySentinel(Thread):
    def __init__(self, interval, memory_limit, gpid):
      raise NotImplementedError, "MemorySentinel class only available on UNIX"

try:
  class ResourceController:
  
      def __init__(self, max_cpu_time=None, max_time=None, max_memory=None,
                   max_reprieve=60):
          if SIGXCPU == -1:
              raise RuntimeError("Unsupported platform")
          self.max_time = max_time
          self.max_memory = max_memory
          self.max_cpu_time = max_cpu_time
          self._reprieve = max_reprieve
          self._timer = None
          self._msentinel = None
          self._old_max_memory = None
          self._old_usr1_hdlr = None
          self._old_max_cpu_time = None
          self._old_usr2_hdlr = None
          self._old_sigxcpu_hdlr = None
          self._limit_set = 0
          self._abort_try = 0
          self._start_time = None
          self._elapse_time = 0
  
      def _hangle_sig_timeout(self, sig, frame):
          raise TimeoutError()
      
      def _hangle_sig_memory(self, sig, frame):
          if self._abort_try < self._reprieve:
              self._abort_try += 1
              raise LineageMemoryError("Memory limit reached")
          else:
              killpg(getpid(), SIGKILL)
  
      def _handle_sigxcpu(self, sig, frame):
          if self._abort_try < self._reprieve:
              self._abort_try += 1
              raise XCPUError("Soft CPU time limit reached")
          else:
              killpg(getpid(), SIGKILL)
  
      def _time_out(self):
          if self._abort_try < self._reprieve:
              self._abort_try += 1
              killpg(getpid(), SIGUSR2)
              if self._limit_set > 0:
                  self._timer = Timer(1, self._time_out)
                  self._timer.start()
          else:
              killpg(getpid(), SIGKILL)
      
      def setup_limit(self):
          """set up the process limit"""
          assert currentThread().getName() == 'MainThread'
          setpgrp()
          if self._limit_set <= 0:
              if self.max_time is not None:
                  self._old_usr2_hdlr = signal(SIGUSR2, self._hangle_sig_timeout)
                  self._timer = Timer(max(1, int(self.max_time) - self._elapse_time),
                                      self._time_out)
                  self._start_time = int(time())
                  self._timer.start()
              if self.max_cpu_time is not None:
                  self._old_max_cpu_time = getrlimit(RLIMIT_CPU)
                  cpu_limit = (int(self.max_cpu_time), self._old_max_cpu_time[1])
                  self._old_sigxcpu_hdlr = signal(SIGXCPU, self._handle_sigxcpu)
                  setrlimit(RLIMIT_CPU, cpu_limit)
              if self.max_memory is not None:
                  self._msentinel = MemorySentinel(1, int(self.max_memory) )
                  self._old_max_memory = getrlimit(RLIMIT_AS)
                  self._old_usr1_hdlr = signal(SIGUSR1, self._hangle_sig_memory)
                  as_limit = (int(self.max_memory), self._old_max_memory[1])
                  setrlimit(RLIMIT_AS, as_limit)
                  self._msentinel.start()
          self._limit_set += 1
  
      def clean_limit(self):
          """reinstall the old process limit"""
          if self._limit_set > 0:
              if self.max_time is not None:
                  self._timer.cancel()
                  self._elapse_time += int(time())-self._start_time
                  self._timer = None
                  signal(SIGUSR2, self._old_usr2_hdlr)
              if self.max_cpu_time is not None:
                  setrlimit(RLIMIT_CPU, self._old_max_cpu_time)
                  signal(SIGXCPU, self._old_sigxcpu_hdlr)
              if self.max_memory is not None:
                  self._msentinel.stop()
                  self._msentinel = None
                  setrlimit(RLIMIT_AS, self._old_max_memory)
                  signal(SIGUSR1, self._old_usr1_hdlr)
          self._limit_set -= 1
except NameError:
  class ResourceController:
    def __init__(self, max_cpu_time=None, max_time=None, 
                 max_memory=None, max_reprieve=60):
      raise NotImplementedError, "ResourceController only available on UNIX"
