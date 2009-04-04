from pear.accounts import models as accounts_models

class PearUserMiddleware(object):
  def process_request(self, request):
    assert hasattr(request, 'user'), "PearUserMiddleware requires that the user attribute of request be available.  Be sure AuthenticationMiddleware is accessed before PearUserMiddlware"
    if request.user.is_authenticated():
      request.user = accounts_models.PearUser.objects.get(pk=request.user.id)
    return None