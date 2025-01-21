import requests
import pandas as pd
from pathlib import Path
import os
from tqdm import tqdm

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'kubernetes'
REPO_NAME = 'kubernetes'
DATA_DIR = Path('data')

def fetch_pull_requests():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    try:
        all_prs = []
        page = 1
        
        while True:
            response = requests.get(url, headers=headers, params={
                'page': page,
                'per_page': 100,
                'state': 'all'
            })
            response.raise_for_status()
            
            # Check rate limits
            remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            
            if remaining <= 1:
                import time
                sleep_time = max(reset_time - time.time(), 0) + 1
                print(f"Rate limit reached. Sleeping for {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                continue
                
            prs = response.json()
            if not prs:
                break
                
            all_prs.extend(prs)
            page += 1
            
            # Initialize progress bar on first page
            if page == 1:
                total = int(response.headers.get('X-Total-Count', 0))
                pbar = tqdm(total=total, desc="Fetching PRs", unit="PR")
            
            # Update progress bar if it exists
            if 'pbar' in locals():
                pbar.update(len(prs))
            
        df = pd.DataFrame(all_prs)
        
        # Save to parquet
        DATA_DIR.mkdir(exist_ok=True)
        df.to_parquet(DATA_DIR / 'pull_requests.parquet')
        print(f"Saved {len(df)} pull requests to {DATA_DIR / 'pull_requests.parquet'}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pull requests: {e}")

if __name__ == "__main__":
    fetch_pull_requests()
