from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse


def index(request):
    return HttpResponse('index_page')


def some_page(request):
    return HttpResponse('some_page')


def some_page_in_blacklist(request):
    return HttpResponse('some_page_in_blacklist')


def some_page_in_whitelist(request):
    return HttpResponse('some_page_in_whitelist')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^some_page/$', some_page, name='some_page'),
    url(r'^some_page/in_blacklist/$', some_page_in_blacklist, name='some_page_in_blacklist'),
    url(r'^some_page/in_whitelist/$', some_page_in_whitelist, name='some_page_in_whitelist'),
    url(r'^user_agreement/', include('user_agreement.urls')),
]
