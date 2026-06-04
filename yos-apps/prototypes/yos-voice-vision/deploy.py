#!/usr/bin/env python3
"""
Y-OS Voice & Vision — Vercel Deployment Script
Uses Vercel REST API v13 for deployment
"""

import json
import os
import subprocess
import sys
import time
import base64
import zipfile
import io
from pathlib import Path

VERCEL_TOKEN = "vcp_REDACTED_TOKEN"
PROJECT_NAME = "yos-voice-vision"
PROJECT_DIR = Path("/home/ubuntu/yos-voice-vision")

import urllib.request
import urllib.error

def api(method, path, data=None):
    url = f"https://api.vercel.com{path}"
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {VERCEL_TOKEN}",
            "Content-Type": "application/json",
        }
    )
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return json.loads(body) if body else {"error": str(e)}

def get_project():
    return api("GET", f"/v9/projects/{PROJECT_NAME}")

def set_env_vars(project_id):
    """Set environment variables on Vercel project"""
    env_vars = []
    
    # Read from .env.local
    env_file = PROJECT_DIR / ".env.local"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                if value and not key.startswith('NEXT_PUBLIC'):
                    env_vars.append({
                        "key": key.strip(),
                        "value": value.strip(),
                        "type": "sensitive",
                        "target": ["production", "preview", "development"]
                    })
                elif key.startswith('NEXT_PUBLIC'):
                    env_vars.append({
                        "key": key.strip(),
                        "value": value.strip(),
                        "type": "plain",
                        "target": ["production", "preview", "development"]
                    })
    
    for var in env_vars:
        if not var["value"]:
            continue
        result = api("POST", f"/v10/projects/{project_id}/env", var)
        if "error" in result:
            # Try updating if already exists
            print(f"  Env {var['key']}: {result.get('error', {}).get('message', 'error')}")
        else:
            print(f"  Env {var['key']}: set ✓")

def collect_files():
    """Collect all project files for deployment"""
    files = []
    
    # Files to include
    include_patterns = [
        "src/**/*",
        "public/**/*",
        "package.json",
        "tsconfig.json",
        "next.config.js",
        "tailwind.config.ts",
        "postcss.config.js",
        ".env.local",
    ]
    
    exclude_dirs = {'.next', 'node_modules', '.git', 'out', 'build'}
    
    for path in PROJECT_DIR.rglob("*"):
        if path.is_file():
            # Check if in excluded dirs
            parts = set(path.relative_to(PROJECT_DIR).parts)
            if parts & exclude_dirs:
                continue
            
            rel = str(path.relative_to(PROJECT_DIR))
            try:
                content = path.read_bytes()
                files.append({
                    "file": rel,
                    "data": base64.b64encode(content).decode(),
                    "encoding": "base64"
                })
            except Exception as e:
                print(f"  Skip {rel}: {e}")
    
    return files

def deploy():
    print("=== Y-OS Voice & Vision — Vercel Deploy ===\n")
    
    # 1. Get project
    project = get_project()
    if "error" in project:
        print(f"Project error: {project}")
        return
    
    project_id = project.get("id", "")
    print(f"Project: {project.get('name')} (ID: {project_id})")
    
    # 2. Set env vars
    print("\nSetting environment variables...")
    set_env_vars(project_id)
    
    # 3. Collect files
    print("\nCollecting files...")
    files = collect_files()
    print(f"  {len(files)} files collected")
    
    # 4. Create deployment
    print("\nCreating deployment...")
    deploy_payload = {
        "name": PROJECT_NAME,
        "project": project_id,
        "files": files,
        "projectSettings": {
            "framework": "nextjs",
            "buildCommand": "pnpm build",
            "installCommand": "pnpm install",
            "outputDirectory": ".next"
        },
        "target": "production"
    }
    
    result = api("POST", "/v13/deployments", deploy_payload)
    
    if "error" in result:
        print(f"Deploy error: {result}")
        return
    
    deploy_id = result.get("id", "")
    deploy_url = result.get("url", "")
    print(f"  Deploy ID: {deploy_id}")
    print(f"  URL: https://{deploy_url}")
    
    # 5. Poll for completion
    print("\nWaiting for deployment...")
    for i in range(60):
        time.sleep(5)
        status_result = api("GET", f"/v13/deployments/{deploy_id}")
        state = status_result.get("readyState", "UNKNOWN")
        print(f"  [{i*5}s] State: {state}")
        
        if state == "READY":
            final_url = f"https://{status_result.get('url', deploy_url)}"
            print(f"\n✅ DEPLOYED: {final_url}")
            return final_url
        elif state in ("ERROR", "CANCELED"):
            print(f"\n❌ Deploy failed: {state}")
            # Get error details
            if "errorMessage" in status_result:
                print(f"Error: {status_result['errorMessage']}")
            return None
    
    print("\n⚠️ Timeout — check Vercel dashboard")
    return f"https://{deploy_url}"

if __name__ == "__main__":
    result = deploy()
    if result:
        print(f"\nFinal URL: {result}")
