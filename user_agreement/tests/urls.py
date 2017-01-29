from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse


def index(request):
    return HttpResponse('index_page')


def some_page(request):
    return HttpResponse('some_page')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^some_page/$', some_page, name='some_page'),
    url(r'^user_agreement/', include('user_agreement.urls')),
]
