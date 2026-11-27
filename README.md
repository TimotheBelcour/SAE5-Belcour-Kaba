# SAÉ 5 – Outil de gestion commerciale des Jardins de Cocagne

Projet de SAÉ 5 du BUT Informatique (3e année), IUT de Saint-Dié-des-Vosges – Université de Lorraine, année 2026-2027.

**Binôme** : Timothé Belcour et Abdoulaye Kaba. Chaque rendu est réalisé à deux, avec un pilote par rendu.

**Jeu de rôle** : développeurs juniors de Software Architecture Évolutions, une entreprise de services du numérique fictive, nous réalisons pour le Réseau Cocagne une partie de son futur outil de gestion : le socle technique, le module de composition des paniers avec reconnaissance des légumes par IA et la visite virtuelle du jardin.

**Suivi du projet** : [tableau Trello « SAÉ 5 – Belcour Kaba »](https://trello.com/b/7u7PKu88)

## Rendus

| Rendu | Document | État |
|---|---|---|
| 1 – Analyse comparative | [Rapport en anglais](rendus/rendu1-analyse-comparative/SAE5_Benchmark_Report_Belcour_Kaba.pdf) | Rapport rendu le 22/09/2026 ; oral le 19/10/2026 |
| 3 – Proposition technique | [Diaporama](rendus/rendu3-proposition-technique/Belcour_Kaba_Rendu3_PropositionTechnique.pdf) | Rendu le 15/10/2026 |
| 4 – Proposition financière | [Devis](rendus/rendu4-proposition-financiere/Belcour_Kaba_Rendu4_PropositionFinanciere.pdf) | Rendu le 30/10/2026 |
| 7 – Environnement de développement | Ce dépôt (branches, CI/CD, Docker) et un document d'explication (à venir) | En cours, à rendre vers le 25/01/2027 |

## Organisation du dépôt

```text
.
├── app/                 application Django (en construction)
├── docker/              configuration des services Docker (reverse proxy…)
├── .github/             vérifications automatiques (GitHub Actions) et modèle de pull request
├── rendus/              documents rendus (PDF), un dossier par rendu
├── CONTRIBUTING.md      nos règles de travail : branches, commits, pull requests
└── README.md
```

- **Code et configuration** : publiés, pour que le dépôt soit utilisable et vérifiable par tous.
- **Documents** : seuls les PDF rendus sont publiés. Les fichiers de travail (Word, PowerPoint, Excel, brouillons) restent en local : voir `.gitignore`.
- **Secrets** : aucun mot de passe n'est publié (`.env` est ignoré par Git).

## Lancer l'application en local (sans Docker)

Prérequis : Python 3.13. Le lancement avec Docker sera décrit ici à la prochaine étape.

1. Copier `.env.example` en `.env` (à la racine) et remplacer les valeurs `a-remplacer` :
   - `DJANGO_SECRET_KEY` : une clé générée sur son poste, avec `python -c "import secrets; print(secrets.token_urlsafe(50))"` ;
   - `DJANGO_SUPERUSER_PASSWORD` : le mot de passe du compte imposé par la consigne (`sae5`, pour le compte `admin`).
2. Créer l'environnement virtuel et installer les dépendances, depuis le dossier `app/` :

   Mac / Linux :
   ```bash
   cd app
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```

   Windows (PowerShell) :
   ```powershell
   cd app
   py -3.13 -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements-dev.txt
   ```
3. Préparer la base, créer le compte d'administration et lancer le serveur :
   ```bash
   python manage.py migrate
   python manage.py createsuperuser --noinput
   python manage.py runserver
   ```
   Le site répond sur http://127.0.0.1:8000 et l'administration sur http://127.0.0.1:8000/admin/.
4. Vérifier le code avant une pull request :
   ```bash
   python manage.py test
   ruff check .
   ruff format --check .
   ```

## Contribuer

Toute modification passe par une branche et une pull request : voir [CONTRIBUTING.md](CONTRIBUTING.md).
