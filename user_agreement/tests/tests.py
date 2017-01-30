# coding: utf-8

from user_agreement.models import Agreement, UserAgreement
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase


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

    def test_redirect_to_user_agreement_page(self):
        self.assertEqual(UserAgreement.objects.count(), 0)
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('some_page'))
        self.assertRedirects(response, self.user_agreement_url + '?redirect_to=/some_page/')

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

    def test_create_new_active_agreement(self):
        Agreement.objects.create(
            active=True,
            content='Second agreement content',
            author=User.objects.get(username='user')
        )
        self.assertEqual(Agreement.objects.count(), 2)
        self.assertFalse(Agreement.objects.first().active)
        self.assertTrue(Agreement.objects.last().active)

    def test_create_current_agreement_in_cache(self):
        self.assertEqual(cache.get('user_agreement.current_theme'), Agreement.objects.first())

    def test_delete_current_agreement_from_cache(self):
        Agreement.objects.first().delete()
        self.assertIsNone(cache.get(Agreement.current_agreement_cache_key))

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

