from django import template

# Make common template tags universally accessible
template.add_to_builtins('pear.core.templatetags.forms')
template.add_to_builtins('pear.core.templatetags.common')
template.add_to_builtins('pear.core.templatetags.smart_if')
template.add_to_builtins('pear.core.templatetags.flash')