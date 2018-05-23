from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin

from user_agreement.models import Agreement

agreement_url = reverse('user_agreement')


class UserAgreementMiddleware(MiddlewareMixin):
    def path_in_list(self, path, url_list):
        result = [url for url in url_list if path.startswith(url)]
        return any(result)

    def path_in_blacklist(self, path):
        black_list = getattr(settings, 'AGREEMENT_URLS_BLACKLIST', [])
        return self.path_in_list(path, black_list)

    def path_in_whitelist(self, path):
        white_list = getattr(settings, 'AGREEMENT_URLS_WHITELIST', [])
        return self.path_in_list(path, white_list)

    def skip_agreement_checking(self, request):
        if self.path_in_whitelist(request.path_info):
            return True

        if request.method != 'GET':
            return True

        if request.is_ajax():
            return True

        if request.path_info == agreement_url:
            return True

        if not request.user.is_authenticated():
            return True

        if not Agreement.get_current_agreement(request.user):
            return True

        if Agreement.get_current_agreement(request.user).is_accepted(request.user.pk):
            return True

    def process_request(self, request):
        if self.path_in_blacklist(request.path_info):
            if not self.skip_agreement_checking(request):
                redirect_to = request.path_info
                querystring = request.META['QUERY_STRING']
                if querystring:
                    redirect_to += '?' + querystring
                response = HttpResponseRedirect(agreement_url + '?redirect_to={}'.format(redirect_to))
                add_never_cache_headers(response)
                return response

