import requests

def get_user_repo_commit_counts(user: str):
    """
    输入 GitHub 用户名，返回 [(repo_name, commit_count), ...]
    简化实现：不处理分页、只做最基本错误处理，够用即可。
    """
    # 1) 列出用户仓库
    repos_url = f"https://api.github.com/users/{user}/repos"
    r = requests.get(repos_url, timeout=15)
    if r.status_code == 404:
        raise ValueError("User not found")
    r.raise_for_status()
    repos = r.json()

    results = []
    for repo in repos:
        name = repo.get("name", "")
        # 2) 列出该仓库的提交（简化：直接 len(json)）
        commits_url = f"https://api.github.com/repos/{user}/{name}/commits"
        rc = requests.get(commits_url, timeout=20)

        # 空仓库会返回 409；这里就当作 0 次提交
        if rc.status_code == 409:
            results.append((name, 0))
            continue

        # 仓库不存在或其他错误先抛；简单起见
        rc.raise_for_status()
        commits = rc.json()
        results.append((name, len(commits)))

    return results
