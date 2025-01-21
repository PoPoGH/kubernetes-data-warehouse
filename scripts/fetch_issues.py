import requests
import pandas as pd
from pathlib import Path
import os
from tqdm import tqdm

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'kubernetes'
REPO_NAME = 'kubernetes'
DATA_DIR = Path('data')

def fetch_issues():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    try:
        all_issues = []
        page = 1
        
        while True:
            response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})
            response.raise_for_status()
            
            issues = response.json()
            if not issues:
                break
                
            all_issues.extend(issues)
            page += 1
            
            # Show progress
            print(f"Fetched {len(all_issues)} issues...")
            
        df = pd.DataFrame(all_issues)
        
        # Save to parquet
        DATA_DIR.mkdir(exist_ok=True)
        df.to_parquet(DATA_DIR / 'issues.parquet')
        print(f"Saved {len(df)} issues to {DATA_DIR / 'issues.parquet'}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues: {e}")

if __name__ == "__main__":
    fetch_issues()
