#!/usr/bin/env python3
"""Register all 8 E2E Run v1 artifacts in the Notion Artifact Registry."""
import json, subprocess, re
from datetime import datetime

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"
DB_ID = "8cd17557340e434698507291face328e"
TODAY = datetime.now().strftime("%Y-%m-%d")

def mcp_call(tool, payload):
    r = subprocess.run(
        ['manus-mcp-cli', 'tool', 'call', tool, '--server', 'notion', '--input', json.dumps(payload)],
        capture_output=True, text=True, timeout=90
    )
    return r.stdout + r.stderr

def create_page_with_content(title, content):
    """Create a Notion page under the parent and return its URL."""
    payload = {
        'parent': {'page_id': PARENT_ID},
        'pages': [{'properties': {'title': title}, 'content': content}]
    }
    out = mcp_call('notion-create-pages', payload)
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f'ERR: {out[-200:]}'

def create_db_entry(artifact_id, artifact_type, mission_id, producer, consumer, review_owner, status, version, uri, parent_artifact="", acceptance_notes="", rejection_notes=""):
    """Create a row in the Artifact Registry DB."""
    content = f"""# {artifact_id}

**Artifact Type:** {artifact_type}
**Mission ID:** {mission_id}
**Producer:** {producer}
**Consumer:** {consumer}
**Review Owner:** {review_owner}
**Status:** {status}
**Version:** {version}
**URI:** {uri}
**Parent Artifact:** {parent_artifact}
**Acceptance Notes:** {acceptance_notes}
**Rejection Notes:** {rejection_notes}
"""
    payload = {
        'data_source_id': DB_ID,
        'pages': [{
            'properties': {
                'title': artifact_id,
                'Artifact Type': artifact_type,
                'Mission ID': mission_id,
                'Producer': producer,
                'Consumer': consumer,
                'Review Owner': review_owner,
                'Status': status,
                'Version': version,
                'URI': uri,
                'Acceptance Notes': acceptance_notes,
                'Rejection Notes': rejection_notes,
            },
            'content': content
        }]
    }
    out = mcp_call('notion-create-pages', payload)
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f'ERR: {out[-200:]}'

# Step 1: Publish all artifact content pages
print("Publishing artifact content pages...")
artifact_files = [
    ('ART-E2E-001 — Strategy Brief', '/home/ubuntu/yreg/run_v1_01_strategy_brief.md'),
    ('ART-E2E-002 — Execution Plan', '/home/ubuntu/yreg/run_v1_02_execution_plan.md'),
    ('ART-E2E-003 — Architecture Package', '/home/ubuntu/yreg/run_v1_03_architecture_package.md'),
    ('ART-E2E-004a — CEO Briefing (Build Artifact)', '/home/ubuntu/yreg/run_v1_04a_ceo_briefing.md'),
    ('ART-E2E-004b — Build Report', '/home/ubuntu/yreg/run_v1_04b_build_report.md'),
    ('ART-E2E-005 — Delivery Report', '/home/ubuntu/yreg/run_v1_05_delivery_report.md'),
    ('ART-E2E-006 — Lakshmi Review', '/home/ubuntu/yreg/run_v1_06_lakshmi_review.md'),
    ('ART-E2E-007 — Learning Report', '/home/ubuntu/yreg/run_v1_07_learning_report.md'),
]

artifact_urls = {}
for title, path in artifact_files:
    print(f"  Publishing: {title}...")
    with open(path) as f: content = f.read()
    url = create_page_with_content(title, content)
    artifact_urls[title] = url
    print(f"    → {url}")

# Step 2: Register artifacts in the DB
print("\nRegistering artifacts in the Artifact Registry DB...")
artifacts = [
    ('ART-E2E-001', 'Strategy Brief', 'MISS-E2E-V1', 'Krishna', 'Ganesha', 'Ganesha', 'Accepted', '1.0', artifact_urls.get('ART-E2E-001 — Strategy Brief', ''), '', 'Accepted by Ganesha. Clear objective, scope and risks.'),
    ('ART-E2E-002', 'Execution Plan', 'MISS-E2E-V1', 'Ganesha', 'Brahma', 'Brahma', 'Accepted', '1.0', artifact_urls.get('ART-E2E-002 — Execution Plan', ''), 'ART-E2E-001', 'Accepted by Brahma. Sequence and roles are clear.'),
    ('ART-E2E-003', 'Architecture Package', 'MISS-E2E-V1', 'Brahma', 'Hanuman', 'Hanuman', 'Accepted', '1.0', artifact_urls.get('ART-E2E-003 — Architecture Package', ''), 'ART-E2E-002', 'Accepted by Hanuman. Build path is unambiguous.'),
    ('ART-E2E-004a', 'Build Artifact', 'MISS-E2E-V1', 'Hanuman', 'CEO', 'Ganesha', 'Accepted', '1.0', artifact_urls.get('ART-E2E-004a — CEO Briefing (Build Artifact)', ''), 'ART-E2E-003', 'CEO Briefing generated per Lakshmi spec.'),
    ('ART-E2E-004b', 'Build Report', 'MISS-E2E-V1', 'Hanuman', 'Ganesha', 'Ganesha', 'Accepted', '1.0', artifact_urls.get('ART-E2E-004b — Build Report', ''), 'ART-E2E-003', 'Build completed with zero deviations.'),
    ('ART-E2E-005', 'Delivery Report', 'MISS-E2E-V1', 'Ganesha', 'CEO', 'CEO', 'Accepted', '1.0', artifact_urls.get('ART-E2E-005 — Delivery Report', ''), 'ART-E2E-004b', 'Mission delivered. All success criteria met.'),
    ('ART-E2E-006', 'Delivery Report', 'MISS-E2E-V1', 'Lakshmi', 'CEO', 'CEO', 'Accepted', '1.0', artifact_urls.get('ART-E2E-006 — Lakshmi Review', ''), 'ART-E2E-005', 'Executive review complete. 2 open loops identified.'),
    ('ART-E2E-007', 'Learning Report', 'MISS-E2E-V1', 'Saraswati', 'System', 'CEO', 'Accepted', '1.0', artifact_urls.get('ART-E2E-007 — Learning Report', ''), 'ART-E2E-006', 'Y-OS v1 declared operationally valid. 4 improvements identified.'),
]

db_urls = {}
for art in artifacts:
    print(f"  Registering: {art[0]}...")
    url = create_db_entry(*art)
    db_urls[art[0]] = url
    print(f"    → {url}")

print("\n=== ALL ARTIFACTS REGISTERED ===")
all_urls = {**artifact_urls, **db_urls}
for k, v in all_urls.items():
    print(f"{k}: {v}")

with open("/home/ubuntu/yreg/run_v1_urls.json", "w") as f:
    json.dump(all_urls, f, indent=2)
