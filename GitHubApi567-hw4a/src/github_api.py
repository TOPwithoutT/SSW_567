import requests

def get_user_repo_commit_counts(user: str):

    repos_url = f"https://api.github.com/users/{user}/repos"
    r = requests.get(repos_url, timeout=15)
    if r.status_code == 404:
        raise ValueError("User not found")
    r.raise_for_status()
    repos = r.json()

    results = []
    for repo in repos:
        name = repo.get("name", "")

        commits_url = f"https://api.github.com/repos/{user}/{name}/commits"
        rc = requests.get(commits_url, timeout=20)

        if rc.status_code == 409:
            results.append((name, 0))
            continue

        rc.raise_for_status()
        commits = rc.json()
        results.append((name, len(commits)))

    return results
