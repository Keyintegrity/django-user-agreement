from __future__ import unicode_literals
from future.builtins import object
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

        redirect_to = request.path_info
        querystring = request.META['QUERY_STRING']
        if querystring:
            redirect_to += '?' + querystring
        response = HttpResponseRedirect(agreement_url + '?redirect_to={}'.format(redirect_to))
        add_never_cache_headers(response)
        return response
