import requests
import pyarrow as pa
import pyarrow.parquet as pq

GITHUB_API = "https://api.github.com"
REPO_OWNER = "kubernetes"
REPO_NAME = "kubernetes"
TOKEN = "your_github_token_here"

def fetch_contributors():
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contributors"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_parquet(data, file_name):
    table = pa.Table.from_pydict(data)
    pq.write_table(table, file_name)

if __name__ == "__main__":
    contributors = fetch_contributors()
    data = {
        "id": [contributor["id"] for contributor in contributors],
        "login": [contributor["login"] for contributor in contributors],
        "contributions": [contributor["contributions"] for contributor in contributors]
    }
    save_to_parquet(data, "data/contributors.parquet")
    print("Contributors saved to data/contributors.parquet")
