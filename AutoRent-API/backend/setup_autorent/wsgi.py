"""
WSGI config for setup_autorent project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'backend.setup_autorent.settings'
)

application = get_wsgi_application()