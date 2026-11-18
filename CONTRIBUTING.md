# Contribuer au projet

Ce dépôt est partagé par le binôme Timothé Belcour et Abdoulaye Kaba. Ces règles servent à travailler à deux sans se gêner, et à garder une branche `main` qui fonctionne toujours.

## Le principe : une branche par tâche (GitHub Flow)

- `main` contient uniquement du travail terminé et testé. **Personne ne pousse directement sur `main`** : tout passe par une pull request.
- Chaque tâche se fait sur sa propre branche, créée à partir de `main`, puis fusionnée dans `main` par une pull request.
- Les tâches sont suivies sur le [tableau Trello](https://trello.com/b/7u7PKu88) : une carte Trello correspond à une branche et à une pull request.

Nous avons choisi GitHub Flow plutôt que Git Flow (avec une branche `develop` et des branches de version) : à deux, avec des livraisons fréquentes, une seule branche principale suffit et reste simple à suivre.

## Les étapes d'une contribution

1. **Partir de `main` à jour** :
   ```
   git switch main
   git pull
   ```
2. **Créer la branche** de la tâche :
   ```
   git switch -c feat/composition-paniers
   ```
3. **Travailler et commiter** souvent, par petites étapes (voir les conventions ci-dessous).
4. **Pousser la branche** et ouvrir une pull request sur GitHub :
   ```
   git push -u origin feat/composition-paniers
   ```
   Remplir le modèle de pull request (quoi, pourquoi, carte Trello, comment vérifier).
5. **Attendre que la CI soit verte** : les vérifications automatiques (tests, qualité du code) doivent passer.
6. **Fusionner** avec « Create a merge commit ». L'auteur peut fusionner lui-même dès que la CI est verte.
7. **Supprimer la branche** (GitHub le fait automatiquement après la fusion), puis revenir sur `main` et faire `git pull`.

## La relecture

- La relecture par l'autre membre **n'est pas obligatoire pour fusionner** : à deux, attendre l'autre bloquerait le travail. Ce sont les vérifications automatiques qui garantissent que `main` fonctionne.
- L'autre membre **relit chaque pull request**, avant ou après la fusion, et laisse ses remarques en commentaire.
- Une remarque qui demande une correction donne lieu à une nouvelle branche et une nouvelle pull request.

## Conventions

### Noms de branches

`type/description-courte`, en minuscules, avec des tirets :

| Type | Pour |
|---|---|
| `feat/` | une nouvelle fonctionnalité |
| `fix/` | une correction de bug |
| `docs/` | la documentation, les PDF des rendus |
| `ci/` | les vérifications automatiques (GitHub Actions) |
| `chore/` | la configuration, Docker, les dépendances |

### Messages de commit

`type: description`, en français, avec le même `type` que pour les branches. Une seule idée par commit.

```
feat: ajouter le calcul du poids d'un panier
fix: corriger le tri des légumes par saison
docs: ajouter le guide d'installation
```

### Fusion

Nous fusionnons avec un **commit de fusion** (« Create a merge commit ») : l'historique garde la trace de chaque branche et de chaque contribution.

## Règles à respecter

- **Aucun mot de passe sur GitHub** : les secrets vont dans `.env` (non publié). Seul `.env.example`, sans vraie valeur, est publié.
- **Identité Git** : chacun configure son nom et son **adresse universitaire**, utilisée pour les statistiques de contribution :
  ```
  git config --global user.name "Prénom Nom"
  git config --global user.email "prenom.nom@etu.univ-lorraine.fr"
  ```
- **Fins de ligne** : `.gitattributes` impose le format LF pour tout le monde, Mac comme Windows. Sans cela, les scripts lancés dans les conteneurs Linux peuvent échouer.
- **Documents des rendus** : seuls les PDF finaux sont publiés dans `rendus/`. Les brouillons (Word, PowerPoint, Excel) restent en local.
