import requests
import pandas as pd
from pathlib import Path
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'kubernetes'
REPO_NAME = 'kubernetes'
DATA_DIR = Path('data')

def fetch_branches():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        branches = response.json()
        df = pd.DataFrame(branches)
        
        # Save to parquet
        DATA_DIR.mkdir(exist_ok=True)
        df.to_parquet(DATA_DIR / 'branches.parquet')
        print(f"Saved {len(df)} branches to {DATA_DIR / 'branches.parquet'}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching branches: {e}")

if __name__ == "__main__":
    fetch_branches()
