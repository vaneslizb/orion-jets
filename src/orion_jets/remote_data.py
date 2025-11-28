"""
Functions for downloading FITS data files from the sister repo (orion-jets-data) on GitHub
"""

import json
import urllib.request
import urllib.error

# Repository configuration
OWNER = "unam-irya-will-henney"
REPO = "orion-jets-data"
BRANCH = "main"
REMOTE_PATH = "data"  # path within the repository

API_URL = (
    f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{REMOTE_PATH}?ref={BRANCH}"
)


def list_remote_fits_files():
    """Return a list of (filename, download_url) for .fits files."""
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "orion-jets-fetch-data",
            "Accept": "application/vnd.github.v3+json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            entries = json.load(resp)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print("Error contacting GitHub API:", e)
        return []

    files = []
    for entry in entries:
        if entry.get("type") != "file":
            continue

        name = entry.get("name")
        url = entry.get("download_url")

        if not name or not url:
            continue

        if not name.lower().endswith(".fits"):
            continue

        files.append((name, url))

    return files


def download_file(url, dest_path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  → Downloading {url} → {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
    except urllib.error.URLError as e:
        print("  ! Failed to download:", e)
