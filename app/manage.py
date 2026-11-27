#!/usr/bin/env python
"""Outil en ligne de commande de Django (serveur, migrations, tests…)."""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django est introuvable : l'environnement virtuel est-il activé "
            "et les dépendances installées (pip install -r requirements-dev.txt) ?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
