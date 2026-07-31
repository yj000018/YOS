#!/usr/bin/env python3
"""
redact_secrets.py — Redact API keys and secrets from Manus fact sheets
before pushing to GitHub (to pass secret scanning protection).
"""
import re
from pathlib import Path

FACTSHEETS_DIR = Path("/home/ubuntu/yos/github_yos/08_LOGS/session-ledger/sessions/manus")

# Patterns to redact (regex → replacement)
REDACT_PATTERNS = [
    # Replicate tokens (r8_...)
    (r'r8_[A-Za-z0-9]{30,}', '[REDACTED:replicate-token]'),
    # GitHub PATs (ghp_...)
    (r'ghp_[A-Za-z0-9]{30,}', '[REDACTED:github-pat]'),
    # OpenAI / Anthropic / xAI style (sk-...)
    (r'sk-[A-Za-z0-9_\-]{20,}', '[REDACTED:api-key]'),
    # BFL API keys
    (r'BFL_API_KEY["\s=:]+[A-Za-z0-9_\-]{20,}', 'BFL_API_KEY=[REDACTED]'),
    # Generic long hex/base64 tokens after "token", "key", "secret" keywords
    (r'(?i)(api[_\-]?key|secret|token|password)["\s:=]+[A-Za-z0-9+/=_\-]{32,}', r'\1=[REDACTED]'),
    # JWT tokens (eyJ...)
    (r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', '[REDACTED:jwt]'),
]

def redact_file(path: Path) -> int:
    """Redact secrets from a file. Returns number of replacements made."""
    content = path.read_text(encoding='utf-8', errors='replace')
    original = content
    total = 0
    for pattern, replacement in REDACT_PATTERNS:
        new_content, count = re.subn(pattern, replacement, content)
        content = new_content
        total += count
    if total > 0:
        path.write_text(content, encoding='utf-8')
    return total

def main():
    files = list(FACTSHEETS_DIR.glob("*.md"))
    files = [f for f in files if not f.name.startswith("_") and f.name != "INDEX.md"]
    
    total_files = 0
    total_replacements = 0
    
    for f in files:
        count = redact_file(f)
        if count > 0:
            print(f"  Redacted {count} secrets in {f.name}")
            total_files += 1
            total_replacements += count
    
    print(f"\nDone: {total_replacements} secrets redacted in {total_files} files")

if __name__ == "__main__":
    main()
