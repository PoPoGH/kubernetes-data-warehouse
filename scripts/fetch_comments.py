import requests
import pandas as pd
from pathlib import Path
import os
from tqdm import tqdm

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'kubernetes'
REPO_NAME = 'kubernetes'
DATA_DIR = Path('data')

def fetch_issue_comments():
    # First get all issues
    issues_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    try:
        # Get all issues
        response = requests.get(issues_url, headers=headers)
        response.raise_for_status()
        issues = response.json()
        
        all_comments = []
        
        # Fetch comments for each issue
        for issue in tqdm(issues, desc="Fetching comments"):
            if issue['comments'] > 0:
                comments_url = issue['comments_url']
                comments_response = requests.get(comments_url, headers=headers)
                comments_response.raise_for_status()
                comments = comments_response.json()
                
                # Add issue reference to each comment
                for comment in comments:
                    comment['issue_number'] = issue['number']
                    all_comments.append(comment)
        
        # Save to parquet
        df = pd.DataFrame(all_comments)
        DATA_DIR.mkdir(exist_ok=True)
        df.to_parquet(DATA_DIR / 'issue_comments.parquet')
        print(f"Saved {len(df)} comments to {DATA_DIR / 'issue_comments.parquet'}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {e}")

if __name__ == "__main__":
    fetch_issue_comments()
