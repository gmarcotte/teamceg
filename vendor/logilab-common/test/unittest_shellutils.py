"""unit tests for logilab.common.shellutils"""

import sys, os, tempfile, shutil
from os.path import join
import datetime, time

from logilab.common.testlib import TestCase, unittest_main

from logilab.common.shellutils import globfind, find, ProgressBar, acquire_lock, release_lock
from logilab.common.proc import NoSuchProcess
from StringIO import StringIO

DATA_DIR = join('data','find_test')

class FindTC(TestCase):
    def test_include(self):
        files = set(find(DATA_DIR, '.py'))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['__init__.py', 'module.py',
                                                       'module2.py', 'noendingnewline.py',
                                                       'nonregr.py', join('sub', 'momo.py')]]))
        files = set(find(DATA_DIR, ('.py',), blacklist=('sub',)))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['__init__.py', 'module.py',
                                                       'module2.py', 'noendingnewline.py',
                                                       'nonregr.py']]))
        
    def test_exclude(self):
        files = set(find(DATA_DIR, ('.py', '.pyc'), exclude=True))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['foo.txt',
                                                       'newlines.txt',
                                                       'normal_file.txt',
                                                       'test.ini',
                                                       'test1.msg',
                                                       'test2.msg',
                                                       'spam.txt',
                                                       join('sub', 'doc.txt'),
                                                       'write_protected_file.txt',
                                                       ]]))

    def test_globfind(self):
        files = set(globfind(DATA_DIR, '*.py'))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['__init__.py', 'module.py',
                                                       'module2.py', 'noendingnewline.py',
                                                       'nonregr.py', join('sub', 'momo.py')]]))
        files = set(globfind(DATA_DIR, 'mo*.py'))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['module.py', 'module2.py',
                                                             join('sub', 'momo.py')]]))
        files = set(globfind(DATA_DIR, 'mo*.py', blacklist=('sub',)))
        self.assertSetEqual(files,
                            set([join(DATA_DIR, f) for f in ['module.py', 'module2.py']]))


class ProgressBarTC(TestCase):
    def test_refresh(self):
        pgb_stream = StringIO()
        expected_stream = StringIO()
        pgb = ProgressBar(20,stream=pgb_stream)
        self.assertEquals(pgb_stream.getvalue(), expected_stream.getvalue()) # nothing print before refresh
        pgb.refresh()
        expected_stream.write("\r["+' '*20+"]")
        self.assertEquals(pgb_stream.getvalue(), expected_stream.getvalue())

    def test_refresh_g_size(self):
        pgb_stream = StringIO()
        expected_stream = StringIO()
        pgb = ProgressBar(20,35,stream=pgb_stream)
        pgb.refresh()
        expected_stream.write("\r["+' '*35+"]")
        self.assertEquals(pgb_stream.getvalue(), expected_stream.getvalue())
        
    def test_refresh_l_size(self):
        pgb_stream = StringIO()
        expected_stream = StringIO()
        pgb = ProgressBar(20,3,stream=pgb_stream)
        pgb.refresh()
        expected_stream.write("\r["+' '*3+"]")
        self.assertEquals(pgb_stream.getvalue(), expected_stream.getvalue())
    
    def _update_test(self, nbops, expected, size = None):
        pgb_stream = StringIO()
        expected_stream = StringIO()
        if size is None:
            pgb = ProgressBar(nbops, stream=pgb_stream)
            size=20
        else:
            pgb = ProgressBar(nbops, size, stream=pgb_stream)
        last = 0
        for round in expected:
            if not hasattr(round, '__int__'):
                dots, update = round
            else:
                dots, update = round, None
            pgb.update()
            if update or (update is None and dots != last):
                last = dots
                expected_stream.write("\r["+('.'*dots)+(' '*(size-dots))+"]")
            self.assertEquals(pgb_stream.getvalue(), expected_stream.getvalue())

    def test_default(self):
        self._update_test(20, xrange(1,21))

    def test_nbops_gt_size(self):
        """Test the progress bar for nbops > size"""
        def half(total):
            for counter in range(1,total+1):
                yield counter / 2
        self._update_test(40, half(40))

    def test_nbops_lt_size(self):
        """Test the progress bar for nbops < size"""
        def double(total):
            for counter in range(1,total+1):
                yield counter * 2
        self._update_test(10, double(10))

    def test_nbops_nomul_size(self):
        """Test the progress bar for size % nbops !=0 (non int number of dots per update)"""
        self._update_test(3, (6,13,20))

    def test_overflow(self):
        self._update_test(5, (8, 16, 25, 33, 42, (42, True)), size=42)


class AcquireLockTC(TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.lock = join(self.tmpdir, 'LOCK')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_acquire_normal(self):
        self.assertTrue(acquire_lock(self.lock, 1, 1))
        self.assertTrue(os.path.exists(self.lock))
        release_lock(self.lock)
        self.assertFalse(os.path.exists(self.lock))

    def test_no_possible_acquire(self):
        self.assertRaises(Exception, acquire_lock, self.lock, 0)

    def test_wrong_process(self):
        fd = os.open(self.lock, os.O_EXCL | os.O_RDWR | os.O_CREAT)
        os.write(fd, '1111111111')
        os.close(fd)
        self.assertTrue(os.path.exists(self.lock))
        self.assertRaises(Exception, acquire_lock, self.lock, 1, 1)

    def test_wrong_process_and_continue(self):
        fd = os.open(self.lock, os.O_EXCL | os.O_RDWR | os.O_CREAT)
        os.write(fd, '1111111111')
        os.close(fd)
        self.assertTrue(os.path.exists(self.lock))
        self.assertTrue(acquire_lock(self.lock))

    def test_locked_for_one_hour(self):
        self.assertTrue(acquire_lock(self.lock))
        touch = datetime.datetime.fromtimestamp(time.time() - 3601).strftime("%m%d%H%M")
        os.system("touch -t %s %s" % (touch, self.lock))
        self.assertRaises(UserWarning, acquire_lock, self.lock, max_try=2, delay=1)


if __name__ == '__main__':
    unittest_main()
