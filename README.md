# Kubernetes Data Warehouse

## Description
Ce dépôt contient les scripts, outils, et documentation nécessaires pour collecter et organiser les données issues de GitHub en vue de créer un entrepôt de données décisionnel pour Kubernetes.

## Outil utilisé
- **API REST GitHub** : Documentation disponible ici : [API REST GitHub](https://docs.github.com/fr/rest).

## Sources de données identifiées
Les données brutes suivantes sont collectées pour alimenter l'entrepôt de données :

1. **Issues** : `/repos/{owner}/{repo}/issues`
2. **Pull Requests** : `/repos/{owner}/{repo}/pulls`
3. **Contributeurs** : `/repos/{owner}/{repo}/contributors`
4. **Couverture des tests** : Collecte via outils tiers (Codecov, Coveralls).
5. **Statistiques GitHub** : `/repos/{owner}/{repo}/stats/contributors`
6. **Trafic Documentation** : `/repos/{owner}/{repo}/traffic/views`
7. **Labels** : `/repos/{owner}/{repo}/labels`
8. **Commentaires Issues** : `/repos/{owner}/{repo}/issues/{issue_number}/comments`
9. **Branches** : `/repos/{owner}/{repo}/branches`

## Étapes suivantes
1. Collecte des données via des scripts Python ou des requêtes `curl`.
2. Transformation des données pour correspondre à la modélisation dimensionnelle.
3. Chargement des données dans l'entrepôt.
