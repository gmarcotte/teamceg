from django.pimentech import network

service = network.JSONRPCService()

@network.jsonremote(service)
def get_username(request):
  if request.user.is_authenticated():
    return [('username', request.user.email)]
  else:
    return [('username', 'Anonymous')]