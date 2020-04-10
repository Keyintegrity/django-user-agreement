from collections import OrderedDict

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.utils.translation import ugettext_lazy as _

from .models import Agreement, UserAgreement


class BaseModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        if request.POST.get('post'):
            for obj in queryset:
                obj.delete()
        else:
            return delete_selected_(self, request, queryset)

    delete_selected.short_description = _('Delete')

    def _get_base_actions(self):
        actions_dict = OrderedDict(
            (name, (func, name, description))
            for func, name, description in super()._get_base_actions()
        )
        return list(actions_dict.values())


class AgreementAdmin(BaseModelAdmin):
    fields = ('active', 'content')
    list_display = ('created', 'active')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(AgreementAdmin, self).save_model(request, obj, form, change)

        active_agreements_count = Agreement.objects.filter(active=True).count()
        if active_agreements_count > 1:
            messages.warning(request, 'Multiple active agreements')
        elif active_agreements_count == 0:
            messages.warning(request, 'No active agreements')


admin.site.register(Agreement, AgreementAdmin)


class UserAgreementAdmin(BaseModelAdmin):
    list_display = ('user', 'agreement')


admin.site.register(UserAgreement, UserAgreementAdmin)
