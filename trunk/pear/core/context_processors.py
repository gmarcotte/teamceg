"""Custom context processors for variables commonly used in templates."""
from django.conf import settings

def settings_vars(request):
  """Common variables defined in the settings files."""
  return {
      'MEDIA_URL': settings.MEDIA_URL,
      'HTML_TITLE_BASE': settings.HTML_TITLE_BASE,
      'PEAR_VERSION': settings.PEAR_VERSION,
      'SERVER_HOSTNAME': settings.SERVER_HOSTNAME,
  }