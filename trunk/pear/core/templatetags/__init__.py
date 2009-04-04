from django import template

# Make common template tags universally accessible
template.add_to_builtins('pear.core.templatetags.forms')