from django import forms


class AgreementForm(forms.Form):
    redirect_to = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.HiddenInput()
    )
