"""Utility functions for use across the pear codebase."""


def make_get_string(get_data):
  return '?%s' % '&'.join(['%s=%s' % (key, value) for (key, value) in get_data.iteritems()])