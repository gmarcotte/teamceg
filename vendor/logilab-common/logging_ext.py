# -*- coding: utf-8 -*-

"""Extends the logging module from the standard library.

:copyright: 2000-2008 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: General Public License version 2 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

import os
import sys
import logging

from logilab.common.textutils import colorize_ansi


def set_log_methods(cls, logger):
    """bind standart logger's methods as methods on the class"""
    cls.__logger = logger
    for attr in ('debug', 'info', 'warning', 'error', 'critical', 'exception'):
        setattr(cls, attr, getattr(logger, attr))


def xxx_cyan(record):
    if 'XXX' in record.message:
        return 'cyan'

class ColorFormatter(logging.Formatter):
    """
    A color Formatter for the logging standard module.

    By default, colorize CRITICAL and ERROR in red, WARNING in orange, INFO in
    green and DEBUG in yellow.

    self.colors is customizable via the 'color' constructor argument (dictionnary).

    self.colorfilters is a list of functions that get the LogRecord
    and return a color name or None.
    """

    def __init__(self, fmt=None, datefmt=None, colors=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.colorfilters = []
        self.colors = {'CRITICAL': 'red',
                       'ERROR': 'red',
                       'WARNING': 'magenta',
                       'INFO': 'green',
                       'DEBUG': 'yellow',
                       }
        if colors is not None:
            assert isinstance(colors, dict)
            self.colors.update(colors)

    def format(self, record):
        msg = logging.Formatter.format(self, record)
        if record.levelname in self.colors:
            color = self.colors[record.levelname]
            return colorize_ansi(msg, color)
        else:
            for cf in self.colorfilters:
                color = cf(record)
                if color: 
                    return colorize_ansi(msg, color)
        return msg

def set_color_formatter(logger=None, **kw):
    """
    Install a color formatter on the 'logger'. If not given, it will
    defaults to the default logger.

    Any additional keyword will be passed as-is to the ColorFormatter
    constructor.
    """
    if logger is None:
        logger = logging.getLogger()
        if not logger.handlers:
            logging.basicConfig()
    format_msg = logger.handlers[0].formatter._fmt
    fmt = ColorFormatter(format_msg, **kw)
    fmt.colorfilters.append(xxx_cyan)
    logger.handlers[0].setFormatter(fmt)


LOG_FORMAT = '%(asctime)s - (%(name)s) %(levelname)s: %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def init_log(debug=False, syslog=False, logthreshold=None, logfile=None,
             logformat=LOG_FORMAT, logdateformat=LOG_DATE_FORMAT):
    """init the log service"""
    if os.environ.get('APYCOT_ROOT'):
        logthreshold = logging.CRITICAL
        # redirect logs to stdout to avoid apycot output parsing failure
        handler = logging.StreamHandler(sys.stdout)
    else:
        if debug:
            handler = logging.StreamHandler()
        elif logfile is None:
            if syslog:
                from logging import handlers
                handler = handlers.SysLogHandler()
            else:
                handler = logging.StreamHandler()
        else:
            try:
                handler = logging.FileHandler(logfile)
            except IOError:
                handler = logging.StreamHandler()
        if logthreshold is None:
            logthreshold = logging.ERROR
        elif isinstance(logthreshold, basestring):
            logthreshold = getattr(logging, THRESHOLD_MAP.get(logthreshold,
                                                              logthreshold))
    # configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logthreshold)
    # only addHandler and removeHandler method while I would like a
    # setHandler method, so do it this way :$
    logger.handlers = [handler]
    isatty = hasattr(sys.__stdout__, 'isatty') and sys.__stdout__.isatty()
    if debug and isatty:
        fmt = ColorFormatter(logformat, logdateformat)
        def col_fact(record):
            if 'XXX' in record.message:
                return 'cyan'
            if 'kick' in record.message:
                return 'red'
        fmt.colorfilters.append(col_fact)
    else:
        fmt = logging.Formatter(logformat, logdateformat)
    handler.setFormatter(fmt)
    return handler

# map logilab.common.logger thresholds to logging thresholds
THRESHOLD_MAP = {'LOG_DEBUG':  'DEBUG',
                 'LOG_INFO':   'INFO',
                 'LOG_NOTICE': 'INFO',
                 'LOG_WARN':   'WARNING',
                 'LOG_ERR':    'ERROR',
                 'LOG_CRIT':   'CRITICAL',
                 }
