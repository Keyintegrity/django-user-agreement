from __future__ import unicode_literals
from future.builtins import str
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext as _


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
    current_agreement_cache_key = 'user_agreement.current_theme'

    class Meta:
        abstract = True


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

    def __unicode__(self):
        return str(self.created)

    def __init__(self, *args, **kwargs):
        super(Agreement, self).__init__(*args, **kwargs)
        self.old_active = self.active

    def save(self, *args, **kwargs):
        super(Agreement, self).save(*args, **kwargs)
        if self.active:
            Agreement.objects.exclude(id=self.id).update(active=False)
            cache.set(self.current_agreement_cache_key, self)
        else:
            if self.active != self.old_active:
                cache.delete(self.current_agreement_cache_key)

    def delete(self, *args, **kwargs):
        super(Agreement, self).delete(*args, **kwargs)
        if self.active:
            cache.delete(self.current_agreement_cache_key)

    @classmethod
    def get_current_agreement(cls):
        current_agreement = cache.get(cls.current_agreement_cache_key)
        if current_agreement:
            return current_agreement

        try:
            current_agreement = cls.objects.get(active=True)
        except cls.DoesNotExist:
            return

        cache.set(cls.current_agreement_cache_key, current_agreement)
        return current_agreement

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
