import django.dispatch

user_agreement_accepted = django.dispatch.Signal(providing_args=["user", "agreement"])
