#!/usr/bin/env python3
"""
push_to_github.py
-----------------
Uploads the yos-reader plugin source to yj000018/YOS/plugins/yos-reader/
via the GitHub Contents API (PUT /repos/{owner}/{repo}/contents/{path}).

Requirements:
  - Python 3.8+
  - A GitHub PAT with contents=write on yj000018/YOS
    (fine-grained: Repository permissions → Contents → Read and write)

Usage:
  export GITHUB_PAT=github_pat_...
  python3 scripts/push_to_github.py

Or pass the token directly:
  python3 scripts/push_to_github.py --token github_pat_...
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

OWNER = "yj000018"
REPO  = "YOS"
BASE_PATH = "plugins/yos-reader"   # destination path in the repo
BRANCH = "main"
COMMIT_MESSAGE = "archive: Y-OS Reader MVP B v0.3.0 — Better YMD Reader (tag v0.3.0-mvp-b)"

# Files to upload (relative to project root = parent of scripts/)
INCLUDE_PATTERNS = [
    "src/main.ts",
    "src/parser/semanticTypes.ts",
    "src/parser/ymdParser.ts",
    "src/panels/SemanticPanel.ts",
    "test/testNote.md",
    "test/testNoteB.md",
    "test/validateParser.mjs",
    "manifest.json",
    "package.json",
    "tsconfig.json",
    "esbuild.config.mjs",
    "README.md",
    "styles.css",
    "main.js",
    ".gitignore",
]

def api_request(method: str, url: str, token: str, data: dict | None = None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "yos-reader-push-script/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return json.loads(body) if body else {}, e.code

def get_existing_sha(token: str, repo_path: str) -> str | None:
    """Return the blob SHA if the file already exists in the repo."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{repo_path}?ref={BRANCH}"
    result, status = api_request("GET", url, token)
    if status == 200:
        return result.get("sha")
    return None

def upload_file(token: str, local_path: Path, repo_path: str) -> bool:
    content = base64.b64encode(local_path.read_bytes()).decode()
    existing_sha = get_existing_sha(token, repo_path)

    payload = {
        "message": COMMIT_MESSAGE,
        "content": content,
        "branch": BRANCH,
    }
    if existing_sha:
        payload["sha"] = existing_sha  # required for updates

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{repo_path}"
    result, status = api_request("PUT", url, token, payload)

    if status in (200, 201):
        action = "updated" if existing_sha else "created"
        print(f"  ✅ {action}: {repo_path}")
        return True
    else:
        print(f"  ❌ FAILED ({status}): {repo_path} — {result.get('message','?')}")
        return False

def push_tag(token: str, tag_name: str, commit_sha: str, tag_message: str) -> bool:
    """Create an annotated tag object then a ref pointing to it."""
    # 1. Create tag object
    url_tag = f"https://api.github.com/repos/{OWNER}/{REPO}/git/tags"
    result, status = api_request("POST", url_tag, token, {
        "tag": tag_name,
        "message": tag_message,
        "object": commit_sha,
        "type": "commit",
    })
    if status not in (200, 201):
        print(f"  ❌ Tag object creation failed ({status}): {result.get('message','?')}")
        return False
    tag_sha = result["sha"]

    # 2. Create ref
    url_ref = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs"
    result2, status2 = api_request("POST", url_ref, token, {
        "ref": f"refs/tags/{tag_name}",
        "sha": tag_sha,
    })
    if status2 in (200, 201, 422):  # 422 = already exists
        exists = "(already existed)" if status2 == 422 else ""
        print(f"  ✅ Tag ref created: refs/tags/{tag_name} {exists}")
        return True
    else:
        print(f"  ❌ Tag ref failed ({status2}): {result2.get('message','?')}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default=os.environ.get("GITHUB_PAT", ""))
    args = parser.parse_args()

    token = args.token.strip()
    if not token:
        print("ERROR: No token. Set GITHUB_PAT env var or pass --token")
        sys.exit(1)

    # Verify token identity
    user_result, _ = api_request("GET", "https://api.github.com/user", token)
    print(f"Authenticated as: {user_result.get('login','?')}")

    project_root = Path(__file__).parent.parent  # yos-reader/
    artifacts_dir = project_root / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    # Copy ZIPs into artifacts/ if they exist at parent level
    for zip_name in ["yos-reader-install.zip", "yos-reader-mvp-b.zip"]:
        src = project_root.parent / zip_name
        dst = artifacts_dir / zip_name
        if src.exists() and not dst.exists():
            dst.write_bytes(src.read_bytes())

    print(f"\nUploading to {OWNER}/{REPO}/{BASE_PATH}/\n")
    success = 0
    failed = 0

    for rel_path in INCLUDE_PATTERNS:
        local = project_root / rel_path
        if not local.exists():
            print(f"  ⚠️  SKIP (not found): {rel_path}")
            continue
        repo_path = f"{BASE_PATH}/{rel_path}"
        ok = upload_file(token, local, repo_path)
        if ok:
            success += 1
        else:
            failed += 1
        time.sleep(0.3)  # stay under rate limit

    print(f"\n{'='*50}")
    print(f"Uploaded: {success}  Failed: {failed}")

    if failed == 0:
        # Get the latest commit SHA on main to tag
        ref_result, _ = api_request(
            "GET",
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
            token,
        )
        commit_sha = ref_result.get("object", {}).get("sha", "")
        if commit_sha:
            print(f"\nLatest commit on {BRANCH}: {commit_sha}")
            print("\nCreating tag v0.3.0-mvp-b...")
            push_tag(token, "v0.3.0-mvp-b", commit_sha, "MVP B — Better YMD Reader v0.3.0")
        else:
            print("Could not retrieve commit SHA for tagging.")
    else:
        print("Skipping tag creation due to upload failures.")

    print("\nDone.")

if __name__ == "__main__":
    main()
