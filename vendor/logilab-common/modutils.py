# -*- coding: utf-8 -*-
"""Python modules manipulation utility functions.

:author: Logilab
:copyright: 2000-2008 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses

:type PY_SOURCE_EXTS: tuple(str)
:var PY_SOURCE_EXTS: list of possible python source file extension

:type STD_LIB_DIR: str
:var STD_LIB_DIR: directory where standard modules are located

:type BUILTIN_MODULES: dict
:var BUILTIN_MODULES: dictionary with builtin module names has key
"""
__docformat__ = "restructuredtext en"

import sys
import os
from os.path import walk, splitext, join, abspath, isdir, dirname, exists
from imp import find_module, load_module, C_BUILTIN, PY_COMPILED, PKG_DIRECTORY

from logilab.common import STD_BLACKLIST

if sys.platform.startswith('win'):
    PY_SOURCE_EXTS = ('py', 'pyw')
    PY_COMPILED_EXTS = ('dll', 'pyd')
    STD_LIB_DIR = join(sys.prefix, 'lib')
else:
    PY_SOURCE_EXTS = ('py',)
    PY_COMPILED_EXTS = ('so',)
    STD_LIB_DIR = join(sys.prefix, 'lib', 'python%s' % sys.version[:3])
    
BUILTIN_MODULES = dict(zip(sys.builtin_module_names,
                           [1]*len(sys.builtin_module_names)))


class NoSourceFile(Exception):
    """exception raised when we are not able to get a python
    source file for a precompiled file
    """

class LazyObject(object):
    def __init__(self, module, obj):
        self.module = module
        self.obj = obj
        self._imported = None
        
    def __getobj(self):
        if self._imported is None:
           self._imported = getattr(load_module_from_name(self.module),
                                    self.obj)
        return self._imported
    
    def __getattribute__(self, attr):
        try:
            return super(LazyObject, self).__getattribute__(attr)
        except AttributeError, ex:
            return getattr(self.__getobj(), attr)
        
    def __call__(self, *args, **kwargs):
        return self.__getobj()(*args, **kwargs)


def load_module_from_name(dotted_name, path=None, use_sys=1):
    """Load a Python module from it's name.

    :type dotted_name: str
    :param dotted_name: python name of a module or package

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :type use_sys: bool
    :param use_sys:
      boolean indicating whether the sys.modules dictionary should be
      used or not


    :raise ImportError: if the module or package is not found
    
    :rtype: module
    :return: the loaded module
    """
    return load_module_from_modpath(dotted_name.split('.'), path, use_sys)


def load_module_from_modpath(parts, path=None, use_sys=1):
    """Load a python module from it's splitted name.

    :type parts: list(str) or tuple(str)
    :param parts:
      python name of a module or package splitted on '.'

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :type use_sys: bool
    :param use_sys:
      boolean indicating whether the sys.modules dictionary should be used or not

    :raise ImportError: if the module or package is not found
    
    :rtype: module
    :return: the loaded module
    """
    if use_sys:
        try:
            return sys.modules['.'.join(parts)]
        except KeyError:
            pass
    modpath = []
    prevmodule = None
    for part in parts:
        modpath.append(part)
        curname = ".".join(modpath)
        module = None
        if len(modpath) != len(parts):
            # even with use_sys=False, should try to get outer packages from sys.modules
            module = sys.modules.get(curname)
        if module is None:
            mp_file, mp_filename, mp_desc = find_module(part, path)
            module = load_module(curname, mp_file, mp_filename, mp_desc)
        if prevmodule:
            setattr(prevmodule, part, module)
        _file = getattr(module, "__file__", "")
        if not _file and len(modpath) != len(parts):
            raise ImportError("no module in %s" % ".".join(parts[len(modpath):]) )
        path = [dirname( _file )]
        prevmodule = module
    return module


def load_module_from_file(filepath, path=None, use_sys=1):
    """Load a Python module from it's path.

    :type filepath: str
    :param filepath: path to the python module or package

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :type use_sys: bool
    :param use_sys:
      boolean indicating whether the sys.modules dictionary should be
      used or not


    :raise ImportError: if the module or package is not found
    
    :rtype: module
    :return: the loaded module
    """
    return load_module_from_modpath(modpath_from_file(filepath), path, use_sys)


def modpath_from_file(filename):
    """given a file path return the corresponding splitted module's name
    (i.e name of a module or package splitted on '.')

    :type filename: str
    :param filename: file's path for which we want the module's name


    :raise ImportError:
      if the corresponding module's name has not been found

    :rtype: list(str)
    :return: the corresponding splitted module's name
    """
    base = splitext(abspath(filename))[0]
    for path in sys.path:
        path = abspath(path)
        if path and base[:len(path)] == path:
            if filename.find('site-packages') != -1 and \
                   path.find('site-packages') == -1:
                continue
            mod_path = [module for module in base[len(path):].split(os.sep)
                        if module]
            for part in mod_path[:-1]:
                path = join(path, part)
                if not _has_init(path):
                    break
            else:
                break
    else:
        raise ImportError('Unable to find module for %s in %s' % (
            filename, ', \n'.join(sys.path)))
    return mod_path



def file_from_modpath(modpath, path=None, context_file=None):
    """given a mod path (ie splited module / package name), return the
    corresponding file, giving priority to source file over precompiled
    file if it exists

    :type modpath: list or tuple
    :param modpath:
      splitted module's name (i.e name of a module or package splitted
      on '.')
      (this means explicit relative imports that start with dots have
      empty strings in this list!)

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :type context_file: str or None
    :param context_file:
      context file to consider, necessary if the identifier has been
      introduced using a relative import unresolvable in the actual
      context (i.e. modutils)
      
    :raise ImportError: if there is no such module in the directory

    :rtype: str or None
    :return:
      the path to the module's file or None if it's an integrated
      builtin module such as 'sys'
    """
    if context_file is not None:
        context = dirname(context_file)
    else:
        context = context_file
    if modpath[0] == 'xml':
        # handle _xmlplus
        try:
            return _file_from_modpath(['_xmlplus'] + modpath[1:], path, context)
        except ImportError:
            return _file_from_modpath(modpath, path, context)
    elif modpath == ['os', 'path']:
        # FIXME: currently ignoring search_path...
        return os.path.__file__
    return _file_from_modpath(modpath, path, context)


    
def get_module_part(dotted_name, context_file=None):
    """given a dotted name return the module part of the name :
    
    >>> get_module_part('logilab.common.modutils.get_module_part')
    'logilab.common.modutils'

    
    :type dotted_name: str
    :param dotted_name: full name of the identifier we are interested in

    :type context_file: str or None
    :param context_file:
      context file to consider, necessary if the identifier has been
      introduced using a relative import unresolvable in the actual
      context (i.e. modutils)

    
    :raise ImportError: if there is no such module in the directory
    
    :rtype: str or None
    :return:
      the module part of the name or None if we have not been able at
      all to import the given name

    XXX: deprecated, since it doesn't handle package precedence over module
    (see #10066)
    """
    # os.path trick
    if dotted_name.startswith('os.path'):
        return 'os.path'
    parts = dotted_name.split('.')
    if context_file is not None:
        # first check for builtin module which won't be considered latter
        # in that case (path != None)
        if parts[0] in BUILTIN_MODULES:
            if len(parts) > 2:
                raise ImportError(dotted_name)
            return parts[0]
        # don't use += or insert, we want a new list to be created !
    path = None
    starti = 0
    if parts[0] == '':
        assert context_file is not None, \
                'explicit relative import, but no context_file?'
        path = [] # prevent resolving the import non-relatively
        starti = 1
    while parts[starti] == '': # for all further dots: change context
        starti += 1
        context_file = dirname(context_file)
    for i in range(starti, len(parts)):
        try:
            file_from_modpath(parts[starti:i+1],
                    path=path, context_file=context_file)
        except ImportError:
            if not i >= max(1, len(parts) - 2):
                raise
            return '.'.join(parts[:i])
    return dotted_name


    
def get_modules(package, src_directory, blacklist=STD_BLACKLIST):
    """given a package directory return a list of all available python
    modules in the package and its subpackages

    :type package: str
    :param package: the python name for the package

    :type src_directory: str
    :param src_directory:
      path of the directory corresponding to the package

    :type blacklist: list or tuple
    :param blacklist:
      optional list of files or directory to ignore, default to
      the value of `logilab.common.STD_BLACKLIST`

    :rtype: list
    :return:
      the list of all available python modules in the package and its
      subpackages
    """
    def func(modules, directory, fnames):
        """walk handler"""
        # remove files/directories in the black list
        for norecurs in blacklist:
            try:
                fnames.remove(norecurs)
            except ValueError:
                continue
        # check for __init__.py
        if not '__init__.py' in fnames:
            while fnames:
                fnames.pop()
        elif directory != src_directory:
            #src = join(directory, file)
            dir_package = directory[len(src_directory):].replace(os.sep, '.')
            modules.append(package + dir_package)
        for filename in fnames:
            src = join(directory, filename)
            if isdir(src):
                continue
            if _is_python_file(filename) and filename != '__init__.py':
                module = package + src[len(src_directory):-3]
                modules.append(module.replace(os.sep, '.'))
    modules = []
    walk(src_directory, func, modules)
    return modules



def get_module_files(src_directory, blacklist=STD_BLACKLIST):
    """given a package directory return a list of all available python
    module's files in the package and its subpackages

    :type src_directory: str
    :param src_directory:
      path of the directory corresponding to the package

    :type blacklist: list or tuple
    :param blacklist:
      optional list of files or directory to ignore, default to the value of
      `logilab.common.STD_BLACKLIST`

    :rtype: list
    :return:
      the list of all available python module's files in the package and
      its subpackages
    """
    def func(files, directory, fnames):
        """walk handler"""
        # remove files/directories in the black list
        for norecurs in blacklist:
            try:
                fnames.remove(norecurs)
            except ValueError:
                continue
        # check for __init__.py
        if not '__init__.py' in fnames:
            while fnames:
                fnames.pop()            
        for filename in fnames:
            src = join(directory, filename)
            if isdir(src):
                continue
            if _is_python_file(filename):
                files.append(src)
    files = []
    walk(src_directory, func, files)
    return files


def get_source_file(filename, include_no_ext=False):
    """given a python module's file name return the matching source file
    name (the filename will be returned identically if it's a already an
    absolute path to a python source file...)

    :type filename: str
    :param filename: python module's file name


    :raise NoSourceFile: if no source file exists on the file system
    
    :rtype: str
    :return: the absolute path of the source file if it exists
    """
    base, orig_ext = splitext(abspath(filename))
    for ext in PY_SOURCE_EXTS:
        source_path = '%s.%s' % (base, ext)
        if exists(source_path):
            return source_path
    if include_no_ext and not orig_ext and exists(base):
        return base
    raise NoSourceFile(filename)



def is_python_source(filename):
    """
    rtype: bool
    return: True if the filename is a python source file
    """
    return splitext(filename)[1][1:] in PY_SOURCE_EXTS


    
def is_standard_module(modname, std_path=(STD_LIB_DIR,)):
    """try to guess if a module is a standard python module (by default,
    see `std_path` parameter's description)
    
    :type modname: str
    :param modname: name of the module we are interested in

    :type std_path: list(str) or tuple(str)
    :param std_path: list of path considered has standard


    :rtype: bool
    :return:
      true if the module:
      - is located on the path listed in one of the directory in `std_path`
      - is a built-in module
    """
    modpath = modname.split('.')
    modname = modpath[0]
    try:
        filename = file_from_modpath(modpath)
    except ImportError:
        # import failed, i'm probably not so wrong by supposing it's
        # not standard...
        return 0
    # modules which are not living in a file are considered standard
    # (sys and __builtin__ for instance)
    if filename is None:
        return 1
    filename = abspath(filename)
    for path in std_path:
        path = abspath(path)
        if filename.startswith(path):
            pfx_len = len(path)
            if filename[pfx_len+1:pfx_len+14] != 'site-packages':
                return 1
            return 0
    return False

    

def is_relative(modname, from_file):
    """return true if the given module name is relative to the given
    file name
    
    :type modname: str
    :param modname: name of the module we are interested in

    :type from_file: str
    :param from_file:
      path of the module from which modname has been imported
    
    :rtype: bool
    :return:
      true if the module has been imported relativly to `from_file`
    """
    if not isdir(from_file):
        from_file = dirname(from_file)
    if from_file in sys.path:
        return False
    try:
        find_module(modname.split('.')[0], [from_file])
        return True
    except ImportError:
        return False


# internal only functions #####################################################

def _file_from_modpath(modpath, path=None, context=None):
    """given a mod path (ie splited module / package name), return the
    corresponding file

    this function is used internally, see `file_from_modpath`'s
    documentation for more information
    """
    assert len(modpath) > 0
    if context is not None:
        try:
            mtype, mp_filename = _module_file(modpath, [context])
        except ImportError:
            mtype, mp_filename = _module_file(modpath, path)
    else:
        mtype, mp_filename = _module_file(modpath, path)
    if mtype == PY_COMPILED:
        try:
            return get_source_file(mp_filename)
        except NoSourceFile:
            return mp_filename
    elif mtype == C_BUILTIN:
        # integrated builtin module
        return None
    elif mtype == PKG_DIRECTORY:
        mp_filename = _has_init(mp_filename)
    return mp_filename

def _module_file(modpath, path=None):
    """get a module type / file path

    :type modpath: list or tuple
    :param modpath:
      splitted module's name (i.e name of a module or package splitted
      on '.'), with leading empty strings for explicit relative import

    :type path: list or None
    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

      
    :rtype: tuple(int, str)
    :return: the module type flag and the file path for a module
    """
    while modpath:
        _, mp_filename, mp_desc = find_module(modpath[0], path)
        modpath.pop(0)
        mtype = mp_desc[2]
        if modpath:
            if mtype != PKG_DIRECTORY:
                raise ImportError('No module %r' % '.'.join(modpath))
            path = [mp_filename]
    return mtype, mp_filename

def _is_python_file(filename):
    """return true if the given filename should be considered as a python file

    .pyc and .pyo are ignored
    """
    for ext in ('.py', '.so', '.pyd', '.pyw'):
        if filename.endswith(ext):
            return True
    return False


def _has_init(directory):
    """if the given directory has a valid __init__ file, return its path,
    else return None
    """
    mod_or_pack = join(directory, '__init__')
    for ext in ('.py', '.pyw', '.pyc', '.pyo'):
        if exists(mod_or_pack + ext):
            return mod_or_pack + ext
    return None
