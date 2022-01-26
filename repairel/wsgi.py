"""
WSGI config for repairel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from lecigon.settings import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lecigon.settings')

if DEBUG:
    print("---STARTING DEVELOPMENT SERVER---")
else:
    print("---STARTING PRODUCTION SERVER---")
application = get_wsgi_application()

application = get_wsgi_application()