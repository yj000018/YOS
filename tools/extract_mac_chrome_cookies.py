#!/usr/bin/env python3
"""
Y-OS Chrome Cookie Extractor — macOS → JSON
Version: 1.0 (2026-07-30)
Stored: /home/ubuntu/yos/tools/extract_mac_chrome_cookies.py (CC — persistent)

MUST run in GUI context (Terminal.app) for Keychain access.
Called automatically by: /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh

Usage:
  python3 extract_mac_chrome_cookies.py [host_filter]
  python3 extract_mac_chrome_cookies.py chatgpt.com   # default
  python3 extract_mac_chrome_cookies.py openai.com

Output: /Users/yannickjolliet/chatgpt_cookies_fresh.json

Decryption details:
  - Chrome macOS: AES-128-CBC, key=PBKDF2-HMAC-SHA1(keychain_password, 'saltysalt', 1003, 16)
  - IV = 16 spaces (b' ' * 16)
  - Prefix: 'v10' (3 bytes) + 32 bytes Chrome metadata → skip first 35 bytes of decrypted output
  - Remaining bytes = actual cookie value (UTF-8)
"""
import subprocess
import sqlite3
import json
import shutil
import hashlib
import sys
from pathlib import Path

OUTPUT_PATH = '/Users/yannickjolliet/chatgpt_cookies_fresh.json'
CHROME_METADATA_PREFIX = 32  # bytes to skip after AES decryption

def get_browser_key(browser='brave'):
    """Get browser AES-128 key via Keychain + PBKDF2-HMAC-SHA1."""
    # Brave uses 'Brave Safe Storage', Chrome uses 'Chrome Safe Storage'
    service_map = {
        'brave': ('Brave Safe Storage', 'Brave'),
        'chrome': ('Chrome Safe Storage', 'Chrome'),
    }
    service, account = service_map.get(browser, service_map['brave'])
    result = subprocess.run(
        ['security', 'find-generic-password', '-w', '-s', service, '-a', account],
        capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        # Fallback: try without -a
        result = subprocess.run(
            ['security', 'find-generic-password', '-w', '-s', service],
            capture_output=True, text=True
        )
    if result.returncode != 0 or not result.stdout.strip():
        raise Exception(f"Keychain access failed for {browser} (rc={result.returncode}). Must run in GUI Terminal.")
    password = result.stdout.strip().encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha1', password, b'saltysalt', 1003, dklen=16)
    return key

# Keep backward compat
def get_chrome_key():
    return get_browser_key('chrome')

def decrypt_value(enc_bytes, key):
    """
    Decrypt a Chrome cookie encrypted_value field.
    Format: b'v10' + AES-CBC(payload), IV=b' '*16
    After decryption: 32 bytes Chrome metadata + actual value
    """
    if not enc_bytes or len(enc_bytes) < 4:
        return ''
    
    if enc_bytes[:3] not in (b'v10', b'v11'):
        # Unencrypted (old format)
        try:
            return enc_bytes.decode('utf-8')
        except:
            return ''
    
    payload = enc_bytes[3:]
    if not payload:
        return ''
    
    try:
        from Crypto.Cipher import AES
        iv = b' ' * 16
        # Ensure multiple of 16
        remainder = len(payload) % 16
        if remainder:
            payload = payload + bytes([16 - remainder] * (16 - remainder))
        
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        dec = cipher.decrypt(payload)
        
        # Remove PKCS7 padding
        pad_byte = dec[-1]
        if isinstance(pad_byte, int) and 1 <= pad_byte <= 16:
            dec = dec[:-pad_byte]
        
        # Skip Chrome metadata prefix (32 bytes)
        actual_value = dec[CHROME_METADATA_PREFIX:]
        return actual_value.decode('utf-8', errors='replace')
    except Exception as e:
        return f'[decrypt_error:{e}]'

def main():
    host_filter = sys.argv[1] if len(sys.argv) > 1 else 'chatgpt.com'
    browser = sys.argv[2] if len(sys.argv) > 2 else 'brave'  # brave or chrome
    
    print(f"[Y-OS Cookie Extractor] host={host_filter} browser={browser}")
    
    key = get_browser_key(browser)
    print(f"[OK] Keychain key obtained ({len(key)} bytes)")
    
    # Browser DB paths
    db_paths = {
        'brave': Path.home() / 'Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies',
        'chrome': Path.home() / 'Library/Application Support/Google/Chrome/Default/Cookies',
    }
    db_src = db_paths.get(browser, db_paths['brave'])
    db_copy = Path(f'/Users/yannickjolliet/yos_{browser}_tmp.db')
    shutil.copy2(db_src, db_copy)
    print(f"[OK] DB copied ({db_copy.stat().st_size} bytes)")
    
    conn = sqlite3.connect(str(db_copy))
    cur = conn.cursor()
    cur.execute("""
        SELECT name, encrypted_value, host_key, path, is_secure, is_httponly, samesite, expires_utc
        FROM cookies WHERE host_key LIKE ?
        ORDER BY name
    """, (f'%{host_filter}%',))
    rows = cur.fetchall()
    conn.close()
    db_copy.unlink()
    
    print(f"[OK] Found {len(rows)} cookies")
    
    samesite_map = {-1: 'Lax', 0: 'None', 1: 'Lax', 2: 'Strict'}
    cookies = []
    for name, enc_val, host, path, secure, httponly, samesite, expires in rows:
        value = decrypt_value(enc_val, key)
        cookie = {
            'name': name,
            'value': value,
            'domain': host,
            'path': path,
            'secure': bool(secure),
            'httpOnly': bool(httponly),
            'sameSite': samesite_map.get(samesite, 'Lax'),
        }
        if expires > 0:
            cookie['expirationDate'] = (expires - 11644473600000000) // 1000000
        cookies.append(cookie)
        preview = value[:50].replace('\n', '') if value else '(empty)'
        print(f"  {name}: len={len(value)}, {preview}")
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(cookies, f, indent=2)
    
    print(f"\n[DONE] {len(cookies)} cookies → {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
