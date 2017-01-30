from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from user_agreement.models import Agreement

agreement_url = reverse('user_agreement')


class UserAgreementMiddleware(object):
    def skip_agreement_checking(self, request):
        if request.method != 'GET':
            return True

        if request.is_ajax():
            return True

        if request.path_info == agreement_url:
            return True

        if not request.user.is_authenticated():
            return True

        if not Agreement.get_current_agreement():
            return True

        if Agreement.get_current_agreement().is_accepted(request.user.pk):
            return True

    def process_request(self, request):
        if self.skip_agreement_checking(request):
            return

        response = HttpResponseRedirect('{}?redirect_to={}'.format(agreement_url, request.path_info))
        add_never_cache_headers(response)
        return response
