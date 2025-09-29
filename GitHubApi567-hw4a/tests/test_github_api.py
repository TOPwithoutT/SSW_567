import json
from src.github_api import get_user_repo_commit_counts

class FakeResp:
    def __init__(self, status=200, data=None):
        self.status_code = status
        self._data = data if data is not None else []
        self.text = json.dumps(self._data)

    def json(self):
        return self._data

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"status={self.status_code}")

def test_happy_path(monkeypatch):
    # 模拟：用户有两个仓库 A,B；A 有 2 次提交，B 是空仓库(409)
    calls = []

    def fake_get(url, timeout=10):
        calls.append(url)
        if url.endswith("/users/alice/repos"):
            return FakeResp(200, [{"name": "A"}, {"name": "B"}])
        if url.endswith("/repos/alice/A/commits"):
            return FakeResp(200, [{"sha": "1"}, {"sha": "2"}])
        if url.endswith("/repos/alice/B/commits"):
            return FakeResp(409, {"message": "empty"})
        return FakeResp(404, {"message": "Not Found"})

    monkeypatch.setattr("requests.get", fake_get)

    out = get_user_repo_commit_counts("alice")
    assert out == [("A", 2), ("B", 0)]
    # 简单校验调用顺序
    assert "/users/alice/repos" in calls[0]

def test_user_not_found(monkeypatch):
    def fake_get(url, timeout=10):
        if "/users/bob/repos" in url:
            return FakeResp(404, {"message":"Not Found"})
        return FakeResp(200, [])
    monkeypatch.setattr("requests.get", fake_get)

    try:
        get_user_repo_commit_counts("bob")
        assert False, "should raise"
    except ValueError as e:
        assert "User not found" in str(e)
