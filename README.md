# SAÉ 5 - Outil de gestion commerciale des Jardins de Cocagne

Projet de SAÉ 5 du BUT Informatique (3e année), IUT de Saint-Dié-des-Vosges - Université de Lorraine, année 2026-2027.

**Binôme** : Timothé Belcour et Abdoulaye Kaba. Chaque rendu est réalisé à deux, avec un pilote par rendu.

**Jeu de rôle** : développeurs juniors de Software Architecture Évolutions, une entreprise de services du numérique fictive, nous réalisons pour le Réseau Cocagne une partie de son futur outil de gestion : le socle technique, le module de composition des paniers avec reconnaissance des légumes par IA et la visite virtuelle du jardin.

**Suivi du projet** : [tableau Trello « SAÉ 5 - Belcour Kaba »](https://trello.com/b/7u7PKu88)

## Rendus

| Rendu | Document | État |
|---|---|---|
| 1 - Analyse comparative | [Rapport en anglais](rendus/rendu1-analyse-comparative/SAE5_Benchmark_Report_Belcour_Kaba.pdf) | Rapport rendu le 22/09/2026 ; oral le 19/10/2026 |
| 3 - Proposition technique | [Diaporama](rendus/rendu3-proposition-technique/Belcour_Kaba_Rendu3_PropositionTechnique.pdf) | Rendu le 15/10/2026 |
| 4 - Proposition financière | [Devis](rendus/rendu4-proposition-financiere/Belcour_Kaba_Rendu4_PropositionFinanciere.pdf) | Rendu le 30/10/2026 |
| 7 - Environnement de développement | Ce dépôt (branches, Docker, CI/CD à venir) et un document d'explication (à venir) | En cours, à rendre vers le 25/01/2027 |

## Organisation du dépôt

```text
.
├── app/                 application Django et dépendances Python
├── docker/              Dockerfile Django et configuration Caddy
├── compose.yaml         services communs : Django, PostgreSQL/PostGIS et Caddy
├── compose.override.yaml réglages de développement, chargés automatiquement
├── .env.example         variables à copier dans .env
├── .github/             modèle de pull request (GitHub Actions à venir)
├── rendus/              documents rendus (PDF), un dossier par rendu
├── CONTRIBUTING.md      nos règles de travail : branches, commits, pull requests
└── README.md
```

- **Code et configuration** : publiés, pour que le dépôt soit utilisable et vérifiable par tous.
- **Documents** : seuls les PDF rendus sont publiés. Les fichiers de travail (Word, PowerPoint, Excel, brouillons) restent en local : voir `.gitignore`.
- **Secrets** : aucun mot de passe n'est publié (`.env` est ignoré par Git).

## Lancer l'application avec Docker

Prérequis : Docker Desktop démarré, en mode conteneurs Linux. Docker Compose 2.24.4 minimum est nécessaire pour remplacer les ports avec `!override`. Python n'a pas besoin d'être installé sur le poste.

Toutes les commandes suivantes se lancent à la racine du dépôt.

1. Copier `.env.example` en `.env` :

   Windows (PowerShell) : `Copy-Item .env.example .env`

   Mac / Linux : `cp .env.example .env`

2. Remplir les trois valeurs vides dans `.env` :
   - `DJANGO_SECRET_KEY` : une longue chaîne aléatoire propre au poste ;
   - `POSTGRES_PASSWORD` : un mot de passe propre à la base locale ;
   - `DJANGO_SUPERUSER_PASSWORD` : `sae5`, pour le compte `admin` imposé par la consigne.

   Pour générer une valeur aléatoire sans installer Python sur le poste :
   ```bash
   docker run --rm python:3.13-slim-bookworm python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   `.env` reste sur le poste et ne doit jamais être publié.

3. Vérifier la configuration puis démarrer les services :
   ```bash
   docker compose config --quiet
   docker compose up --build -d
   docker compose logs -f web
   ```
   Le service `dependances` installe les outils Python dans un volume puis s'arrête. Django attend que cette installation soit terminée et que PostgreSQL soit prêt, puis applique les migrations et récupère les fichiers statiques.

   Quand le serveur est prêt, ouvrir http://localhost:8000. L'administration est sur http://localhost:8000/admin/. `Ctrl+C` quitte les logs en laissant les services démarrés.

4. Créer le compte d'administration une seule fois :
   ```bash
   docker compose exec web python manage.py createsuperuser --noinput
   ```
   Se connecter avec `admin` et `sae5`.

## Services et données

| Service | Rôle |
|---|---|
| `db` | PostgreSQL 17 avec PostGIS 3.7 pour les futures données géographiques |
| `web` | Application Django 5.2, avec rechargement automatique en développement |
| `proxy` | Caddy : seul point d'entrée HTTP, avec les fichiers statiques de l'administration |
| `dependances` | Installation ponctuelle des dépendances de développement |

Le code est monté depuis `app/` : les changements Python sont pris en compte sans reconstruire l'image. Après une modification des dépendances, relancer `docker compose up --build -d`.

PostgreSQL n'est pas exposé sur le poste. Django le joint via `db:5432` sur le réseau interne. Les données sont conservées dans le volume `postgres_data`, y compris après `docker compose down`. Un changement de `POSTGRES_PASSWORD` dans `.env` ne modifie pas le mot de passe d'une base déjà créée.

L'image PostGIS est exécutée en `linux/amd64`. Sur les Mac Apple Silicon, Docker Desktop utilise l'émulation pour ce service, ce qui peut rendre son premier démarrage plus lent. Django et Caddy utilisent l'architecture du poste.

PostGIS est activé dans la base, mais Django utilise pour l'instant son moteur PostgreSQL classique. GeoDjango sera ajouté si des modèles géographiques sont nécessaires.

## Commandes utiles

```bash
# Voir l'état des services et leurs logs
docker compose ps -a
docker compose logs -f web db

# Vérifier le projet avant une pull request
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec web ruff check .
docker compose exec web ruff format --check .

# Préparer et appliquer une évolution des modèles
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Ouvrir une session SQL dans la base
docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'

# Arrêter les services en gardant les données
docker compose down
```

Si le port 8000 est déjà utilisé, modifier `HTTP_PORT` dans `.env`, puis relancer `docker compose up -d`. Si le site ne répond pas, regarder `docker compose logs dependances web db`.

## Configuration commune et déploiement

`compose.yaml` contient l'image Django avec Gunicorn, PostgreSQL/PostGIS, Caddy et les volumes persistants. `compose.override.yaml` ajoute seulement le développement : code local, dépendances, serveur Django et accès HTTP sur le port 8000.

Pour construire et vérifier la configuration commune seule :

```bash
docker compose -f compose.yaml config --quiet
docker compose -f compose.yaml build web
```

Un déploiement reste à configurer avec son domaine dans `SITE_ADDRESS`, ses hôtes autorisés dans `DJANGO_ALLOWED_HOSTS` et ses propres secrets. Avec `compose.yaml` seul, le debug est désactivé, Caddy utilise les ports 80 et 443, et aucun code du poste n'est monté dans le conteneur. Les migrations et les fichiers statiques sont alors préparés explicitement avant de lancer les services :

```bash
docker compose -f compose.yaml run --rm web python manage.py migrate --noinput
docker compose -f compose.yaml run --rm web python manage.py collectstatic --noinput
docker compose -f compose.yaml up --build -d
```

## Contribuer

Toute modification passe par une branche et une pull request : voir [CONTRIBUTING.md](CONTRIBUTING.md).
