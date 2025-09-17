from pathlib import Path

import requests


def get_github_latest_release_tag(repo_owner: str, repo_name: str) -> str:
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    key = "tag_name"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    tag_name = data.get(key)

    if not tag_name:
        raise Exception(f"Response doesn't contain key '{key}'")

    return tag_name


def get_project_root(origin: Path = Path(__file__)):
    for directory in [origin.resolve()] + list(origin.resolve().parents):
        if (directory / "pyproject.toml").exists():
            return directory

    raise FileNotFoundError("Could not find project root")
