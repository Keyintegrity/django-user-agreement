# coding: utf-8

from __future__ import unicode_literals
from user_agreement.models import Agreement, UserAgreement
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings


@override_settings(AGREEMENT_URLS_BLACKLIST=['/some_page/',])
class ViewsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            'user', 'user@example.com', 'user'
        )

        Agreement.objects.create(
            active=True,
            content='Agreement content',
            author=user
        )

    user_agreement_url = reverse('user_agreement')

    def test_user_agreement_page_access_user_not_authorized(self):
        self.assertEqual(Agreement.objects.count(), 1)
        response = self.client.get(self.user_agreement_url)
        self.assertEqual(response.status_code, 404)

    def test_user_agreement_page_access_user_authorized(self):
        self.client.login(username='user', password='user')
        response = self.client.get(self.user_agreement_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_agreement'], Agreement.objects.first())

    @override_settings(AGREEMENT_URLS_BLACKLIST=[])
    def test_none_redirect_to_user_agreement_page_with_empty_black_list(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('some_page'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('some_page_in_blacklist'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_user_agreement_page_with_black_list(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('some_page'))
        self.assertRedirects(response, self.user_agreement_url + '?redirect_to=/some_page/')
        response = self.client.get(reverse('some_page_in_blacklist'))
        self.assertRedirects(response, self.user_agreement_url + '?redirect_to=/some_page/in_blacklist/')

    @override_settings(AGREEMENT_URLS_BLACKLIST=[])
    def test_none_redirect_to_user_agreement_page_with_querystring_with_empty_black_list(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        querystring = 'a=1&b=2'
        response = self.client.get('{}?{}'.format(reverse('some_page'), querystring))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_user_agreement_page_with_querystring_with_black_list(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        querystring = 'a=1&b=2'
        response = self.client.get('{}?{}'.format(reverse('some_page'), querystring))
        self.assertRedirects(response, '{}?{}?{}'.format(self.user_agreement_url, 'redirect_to=/some_page/', querystring))

    def test_user_accept_agreement(self):
        self.client.login(username='user', password='user')
        response = self.client.post(self.user_agreement_url, data={'redirect_to': '/some_page/'})
        self.assertEqual(UserAgreement.objects.count(), 1)
        self.assertRedirects(response, '/some_page/')

    def test_access_to_page_when_agreement_accepted(self):
        UserAgreement.objects.create(
            agreement=Agreement.objects.first(),
            user=User.objects.get(username='user')
        )
        self.assertEqual(UserAgreement.objects.count(), 1)

        self.client.login(username='user', password='user')
        response = self.client.get(reverse('some_page'))
        self.assertEqual(response.status_code, 200)
        cache.clear()

    def test_user_agreement_cache(self):
        user = User.objects.get(username='user')
        agreement = Agreement.objects.first()
        user_agreement = UserAgreement.objects.create(
            agreement=agreement,
            user=User.objects.get(username='user')
        )
        self.assertTrue(cache.get(UserAgreement.cache_key_pattern.format(user.pk, agreement.pk)))

        user_agreement.delete()
        self.assertIsNone(cache.get(UserAgreement.cache_key_pattern.format(user.pk, agreement.pk)))

    @override_settings(AGREEMENT_URLS_WHITELIST=['/some_page/in_whitelist/', ])
    def test_access_to_page_in_whitelist(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('some_page'))
        self.assertRedirects(response, self.user_agreement_url + '?redirect_to=/some_page/')
        response = self.client.get(reverse('some_page_in_whitelist'))
        self.assertEqual(response.status_code, 200)

