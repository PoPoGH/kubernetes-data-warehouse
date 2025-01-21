# Entrepôt de Données Kubernetes

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Ce projet collecte et analyse les données du projet Kubernetes depuis GitHub.

## Table des Matières
1. [Structure du Projet](#structure-du-projet)
2. [Fonctionnalités](#fonctionnalités)
3. [Utilisation](#utilisation)
4. [Sources de Données](#sources-de-données)
5. [Schéma de la Base de Données](#schéma-de-la-base-de-données)
6. [Gestion des Limites d'API](#gestion-des-limites-dapi)
7. [Dépendances](#dépendances)
8. [Configuration](#configuration)
9. [Contribuer](#contribuer)
10. [Licence](#licence)
11. [Dépannage](#dépannage)

## Structure du Projet

```
kubernetes-data-warehouse/
├── data/                   # Contient les données collectées au format parquet
├── scripts/                # Scripts de collecte et traitement des données
│   ├── fetch_contributors.py
│   ├── fetch_issues.py
│   ├── fetch_pull_requests.py
│   ├── fetch_labels.py
│   ├── fetch_comments.py
│   ├── fetch_branches.py
│   ├── load_to_duckdb.py   # Script Python pour charger les données dans DuckDB
│   ├── run_all.py # Script principal pour exécuter tous les collecteurs
└── README.md
```

## Fonctionnalités

Le projet permet de :
- Collecter les données GitHub du projet Kubernetes
- Stocker les données dans des fichiers Parquet
- Charger les données dans une base DuckDB
- Analyser les données via SQL
- Gérer les limites de taux d'API GitHub
- Mettre en cache les résultats pour éviter les collectes répétées

## Utilisation

### Pré-requis
- Python 3.8 ou supérieur
- Compte GitHub avec token d'accès

### Installation
1. Cloner le dépôt :
```bash
git clone https://github.com/votre-utilisateur/kubernetes-data-warehouse.git
cd kubernetes-data-warehouse
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer le token GitHub :
   - Créer un fichier `.env` avec votre token :
   ```
   GITHUB_TOKEN=your_token_here
   ```

4. Exécuter les scripts de collecte :
```bash
# Collecte unique
python scripts/fetch_issues.py
python scripts/fetch_pull_requests.py
python scripts/fetch_contributors.py
python scripts/fetch_labels.py
python scripts/fetch_comments.py
python scripts/fetch_branches.py

# Ou utiliser le script principal
python scripts/run_all.py
```

3. Charger les données dans DuckDB :
```bash
python scripts/load_to_duckdb.py
```

4. Explorer la base de données avec DBeaver :
   - Créer une nouvelle connexion DuckDB
   - Chemin de la base : `kubernetes_data.db`

## Sources de Données

Les données suivantes sont collectées :
- Issues (tickets)
- Pull Requests (demandes de fusion)
- Contributeurs
- Labels (étiquettes)
- Commentaires sur les issues
- Branches (branches Git)

## Schéma de la Base de Données

La base contient les tables suivantes :
- raw_issues : Données brutes des issues
- raw_pull_requests : Données brutes des pull requests
- raw_contributors : Données brutes des contributeurs
- raw_labels : Données brutes des labels
- raw_comments : Données brutes des commentaires
- raw_branches : Données brutes des branches

Chaque table contient les données brutes du fichier parquet correspondant.

## Gestion des Limites d'API

Le système gère automatiquement :
- Les limites de taux de l'API GitHub
- Les tentatives de récupération en cas d'échec
- La mise en cache des résultats pour 1 heure
- Le parallélisme contrôlé des collectes

## Dépendances

- Python 3.8+
- Bibliothèques Python :
  - requests
  - pandas
  - pyarrow
  - duckdb
  - python-dotenv
  - tqdm

## Configuration

Les paramètres de configuration principaux sont dans `scripts/run_all.py` :
- Propriétaire du dépôt (kubernetes)
- Nom du dépôt (kubernetes)
- Nombre de tentatives en cas d'échec
- Délai entre les tentatives
- Nombre de workers parallèles

## Contribuer

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committer vos changements (`git commit -m 'Ajout d'une AmazingFeature'`)
4. Pousser la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

## Dépannage

### Problèmes courants

1. **Erreur 401 - Non autorisé**
   - Vérifiez que votre token GitHub est valide
   - Assurez-vous que le fichier `.env` est correctement configuré

2. **Limite de taux API atteinte**
   - Le système gère automatiquement les limites
   - Vous pouvez augmenter le délai entre les requêtes dans `scripts/run_all.py`

3. **Erreurs de dépendances**
   - Vérifiez que vous utilisez Python 3.8+
   - Réinstallez les dépendances : `pip install -r requirements.txt`
