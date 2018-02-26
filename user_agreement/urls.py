from __future__ import unicode_literals
from user_agreement.views import AgreementView
from django.conf.urls import url


urlpatterns = [
    url(r'^$', AgreementView.as_view(), name='user_agreement'),
]
