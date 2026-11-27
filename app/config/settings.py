"""Réglages du projet Django.

Tous les réglages qui changent d'un poste à l'autre (clé secrète, mode debug, hôtes autorisés,
base de données) sont lus dans les variables d'environnement : aucun secret dans le dépôt.
En local, ces variables viennent du fichier `.env` à la racine du dépôt (modèle : `.env.example`).
Dans Docker, elles seront fournies par Docker Compose (étape 3).
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# Dossier app/ (celui de manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env de la racine du dépôt s'il existe.
# Une variable déjà définie dans l'environnement n'est jamais écrasée.
load_dotenv(BASE_DIR.parent / ".env")


def env_bool(nom: str, defaut: bool = False) -> bool:
    """Lit une variable d'environnement booléenne (true/1/yes/oui)."""
    valeur = os.environ.get(nom)
    if valeur is None:
        return defaut
    return valeur.strip().lower() in {"1", "true", "yes", "oui"}


def env_liste(nom: str, defaut: str = "") -> list[str]:
    """Lit une variable d'environnement contenant une liste séparée par des virgules."""
    elements = os.environ.get(nom, defaut).split(",")
    return [element.strip() for element in elements if element.strip()]


# --- Sécurité ---------------------------------------------------------------

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "La variable DJANGO_SECRET_KEY est absente : copier .env.example en .env et la remplir."
    )

# Désactivé par défaut : il faut l'activer explicitement en développement.
DEBUG = env_bool("DJANGO_DEBUG")

ALLOWED_HOSTS = env_liste("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")


# --- Applications -----------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Applications du projet
    "accueil",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Gabarits communs à tout le site (base.html)
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Base de données --------------------------------------------------------
# SQLite pour commencer sans Docker. PostgreSQL + PostGIS arrive à l'étape 3 (Docker).

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Mots de passe ----------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Langue et fuseau horaire -----------------------------------------------

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True


# --- Fichiers statiques -----------------------------------------------------

STATIC_URL = "static/"
# Dossier rempli par `collectstatic`, servi par le reverse proxy en production (ignoré par Git)
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
