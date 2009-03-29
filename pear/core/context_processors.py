"""Custom context processors for variables commonly used in templates."""
from django.conf import settings

def settings_vars(request):
  """Common variables defined in the settings files."""
  return {
      'MEDIA_URL': settings.MEDIA_URL
  }