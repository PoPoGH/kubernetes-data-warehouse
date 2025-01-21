import requests
import pyarrow as pa
import pyarrow.parquet as pq

GITHUB_API = "https://api.github.com"
REPO_OWNER = "kubernetes"
REPO_NAME = "kubernetes"
TOKEN = "your_github_token_here"  # Remplacez par votre token GitHub

def fetch_issues():
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_parquet(data, file_name):
    table = pa.Table.from_pydict(data)
    pq.write_table(table, file_name)

if __name__ == "__main__":
    issues = fetch_issues()
    data = {
        "id": [issue["id"] for issue in issues],
        "title": [issue["title"] for issue in issues],
        "state": [issue["state"] for issue in issues],
        "created_at": [issue["created_at"] for issue in issues],
        "closed_at": [issue.get("closed_at") for issue in issues],
        "labels": [[label["name"] for label in issue["labels"]] for issue in issues]
    }
    save_to_parquet(data, "data/issues.parquet")
    print("Issues saved to data/issues.parquet")
