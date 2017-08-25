from __future__ import unicode_literals
from .models import Agreement, UserAgreement
from django.contrib import admin
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.utils.translation import ugettext_lazy as _


class BaseModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        if request.POST.get('post'):
            for obj in queryset:
                obj.delete()
        else:
            return delete_selected_(self, request, queryset)

    delete_selected.short_description = _('Delete')


class AgreementAdmin(BaseModelAdmin):
    fields = ('active', 'content')
    list_display = ('created', 'active')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(AgreementAdmin, self).save_model(request, obj, form, change)


admin.site.register(Agreement, AgreementAdmin)


class UserAgreementAdmin(BaseModelAdmin):
    list_display = ('user', 'agreement')


admin.site.register(UserAgreement, UserAgreementAdmin)
