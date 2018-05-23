from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from future.builtins import str
from future.utils import python_2_unicode_compatible

from .helpers import import_obj


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Date of creation')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    cache_key_pattern = 'user.{}.agreement.{}.accepted'

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Agreement(BaseModel):
    class Meta:
        verbose_name = _('Agreement')
        verbose_name_plural = _('Agreements')

    active = models.BooleanField(
        default=False,
        verbose_name=_('Current agreement')
    )
    content = models.TextField(verbose_name=_('Content'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return str(self.created)

    def __init__(self, *args, **kwargs):
        super(Agreement, self).__init__(*args, **kwargs)
        self.old_active = self.active

    @classmethod
    def get_current_agreement(cls, user):
        func_path = settings.AGREEMENT_FOR_USER

        if func_path:
            func = import_obj(func_path)
            if callable(func):
                return func(user)

        return Agreement.objects.filter(active=True).first()

    def is_accepted(self, user_id):
        accepted = cache.get(self.cache_key_pattern.format(user_id, self.pk))
        if accepted is not None:
            return accepted

        accepted = self.useragreement_set.filter(user_id=user_id).exists()
        cache.set(self.cache_key_pattern.format(user_id, self.pk), accepted)
        return accepted

    def accept(self, user):
        UserAgreement.objects.get_or_create(
            agreement=self,
            user=user
        )


class UserAgreement(BaseModel):
    class Meta:
        verbose_name = _('Accepted user agreement')
        verbose_name_plural = _('Accepted user agreements')

    agreement = models.ForeignKey(Agreement, verbose_name=_('User agreement'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))

    def save(self, *args, **kwargs):
        super(UserAgreement, self).save(*args, **kwargs)
        cache.set(self.cache_key_pattern.format(self.user_id, self.agreement_id), True)

    def delete(self, *args, **kwargs):
        super(UserAgreement, self).delete(*args, **kwargs)
        cache.delete(self.cache_key_pattern.format(self.user_id, self.agreement_id))
