import sys
from .github_api import get_user_repo_commit_counts

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src <github_user>")
        sys.exit(2)
    user = sys.argv[1]
    try:
        pairs = get_user_repo_commit_counts(user)
        if not pairs:
            print(f"No repositories found for user: {user}")
            return
        for repo, n in pairs:
            print(f"Repo: {repo} Number of commits: {n}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
