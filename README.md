# Entrepôt de Données Kubernetes

Ce projet collecte et analyse les données du projet Kubernetes depuis GitHub.

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
│   ├── run_all_optimized.py # Script principal pour exécuter tous les collecteurs
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

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer le token GitHub :
   - Créer un fichier `.env` avec votre token :
   ```
   GITHUB_TOKEN=your_token_here
   ```

2. Exécuter les scripts de collecte :
```bash
# Collecte unique
python scripts/fetch_issues.py
python scripts/fetch_pull_requests.py
python scripts/fetch_contributors.py

# Ou utiliser le script principal
python scripts/run_all_optimized.py
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

Les paramètres de configuration sont dans `scripts/run_all_optimized.py` :
- Propriétaire du dépôt (kubernetes)
- Nom du dépôt (kubernetes)
- Nombre de tentatives en cas d'échec
- Délai entre les tentatives
- Nombre de workers parallèles
