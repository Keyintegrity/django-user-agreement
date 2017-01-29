# coding: utf-8

from django.http import Http404, HttpResponseRedirect
from django.views.generic import FormView
from user_agreement.forms import AgreementForm
from user_agreement.models import Agreement


class AgreementView(FormView):
    template_name = 'user_agreement/agreement.html'
    form_class = AgreementForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise Http404()

        return super(AgreementView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AgreementView, self).get_context_data(**kwargs)
        context['current_agreement'] = Agreement.get_current_agreement()
        return context

    def get_initial(self):
        initial = super(AgreementView, self).get_initial()
        initial['redirect_to'] = self.request.GET.get('redirect_to')
        return initial

    def form_valid(self, form):
        Agreement.get_current_agreement().accept(self.request.user)
        redirect_to = form.cleaned_data['redirect_to'] or '/'
        return HttpResponseRedirect(redirect_to)
