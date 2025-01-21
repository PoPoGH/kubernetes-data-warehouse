import os
import requests
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"
REPO_OWNER = "kubernetes"
REPO_NAME = "kubernetes"
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_pull_requests():
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_parquet(data, file_name):
    table = pa.Table.from_pydict(data)
    pq.write_table(table, file_name)

if __name__ == "__main__":
    prs = fetch_pull_requests()
    data = {
        "id": [pr["id"] for pr in prs],
        "title": [pr["title"] for pr in prs],
        "state": [pr["state"] for pr in prs],
        "created_at": [pr["created_at"] for pr in prs],
        "merged_at": [pr.get("merged_at") for pr in prs],
        "user": [pr["user"]["login"] for pr in prs]
    }
    save_to_parquet(data, "data/pull_requests.parquet")
    print("Pull Requests saved to data/pull_requests.parquet")
