"""Point d'entrée ASGI (non utilisé pour l'instant, gardé pour un éventuel besoin de temps réel)."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
