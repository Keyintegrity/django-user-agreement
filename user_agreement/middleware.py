from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin

from user_agreement.models import Agreement

agreement_url = reverse_lazy('user_agreement')


class UserAgreementMiddleware(MiddlewareMixin):
    def path_in_list(self, path, url_list):
        for url in url_list:
            if path.startswith(url):
                return True
        return False

    def path_in_blacklist(self, path):
        return self.path_in_list(path, settings.AGREEMENT_URLS_BLACKLIST)

    def path_in_whitelist(self, path):
        return self.path_in_list(path, settings.AGREEMENT_URLS_WHITELIST)

    def skip_agreement_checking(self, request):
        if self.path_in_whitelist(request.path_info):
            return True

        if request.method != 'GET':
            return True

        if request.is_ajax():
            return True

        if request.path_info == agreement_url:
            return True

        if not request.user.is_authenticated:
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

