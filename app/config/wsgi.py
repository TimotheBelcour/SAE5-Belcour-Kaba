"""Point d'entrée WSGI, utilisé par le serveur d'application (Gunicorn) dans Docker."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
