import requests
import pandas as pd
from pathlib import Path
import os
from tqdm import tqdm

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'kubernetes'
REPO_NAME = 'kubernetes'
DATA_DIR = Path('data')

def fetch_contributors():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contributors'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    try:
        all_contributors = []
        page = 1
        
        while True:
            response = requests.get(url, headers=headers, params={
                'page': page,
                'per_page': 100
            })
            response.raise_for_status()
            
            contributors = response.json()
            if not contributors:
                break
                
            all_contributors.extend(contributors)
            page += 1
            
            # Show progress
            print(f"Fetched {len(all_contributors)} contributors...")
            
        df = pd.DataFrame(all_contributors)
        
        # Save to parquet
        DATA_DIR.mkdir(exist_ok=True)
        df.to_parquet(DATA_DIR / 'contributors.parquet')
        print(f"Saved {len(df)} contributors to {DATA_DIR / 'contributors.parquet'}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching contributors: {e}")

if __name__ == "__main__":
    fetch_contributors()
