from django.conf import settings

AGREEMENT_FOR_USER = getattr(settings, 'AGREEMENT_FOR_USER', '')
AGREEMENT_URLS_BLACKLIST = getattr(settings, 'AGREEMENT_URLS_BLACKLIST', [])
AGREEMENT_URLS_WHITELIST = getattr(settings, 'AGREEMENT_URLS_WHITELIST', [])

