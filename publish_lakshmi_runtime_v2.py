import json
import subprocess
import re

DB_ID = "4ae2fa35-d24f-4c44-be88-dbb808ea14cd" # Artifact Registry

docs = [
    {"file": "Lakshmi_Runtime_Architecture_v2.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "Lakshmi_Runtime_Data_Model_v1.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "Lakshmi_Open_Loops_Rules_v1.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "Lakshmi_CEO_Briefing_Template_v1.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "Lakshmi_Dashboard_Schema_v1.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "ADR-0018_Lakshmi_Runtime_MVP.md", "type": "Architecture Package", "producer": "Brahma", "consumer": "Hanuman", "mission": "MISS-LAKSHMI-V2"},
    {"file": "Lakshmi_Build_Report_v1.md", "type": "Build Report", "producer": "Hanuman", "consumer": "Ganesha", "mission": "MISS-LAKSHMI-V2"}
]

def mcp_call(tool, payload):
    cmd = ['manus-mcp-cli', 'tool', 'call', tool, '--server', 'notion', '--input', json.dumps(payload)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout + r.stderr

for doc in docs:
    print(f"Publishing {doc['file']}...")
    with open(doc['file'], 'r') as f:
        content = f.read()
        
    payload = {
        'parent': {'data_source_id': DB_ID},
        'pages': [{
            'properties': {
                'Name': doc['file'].replace('.md', ''),
                'Artifact Type': doc['type'],
                'Mission ID': doc['mission'],
                'Producer': doc['producer'],
                'Consumer': doc['consumer'],
                'Status': 'Done'
            },
            'content': content
        }]
    }
    
    out = mcp_call('notion-create-pages', payload)
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    if m:
        print(f"✅ {doc['file']} -> {m.group(0)}")
    else:
        print(f"❌ Failed: {out[-200:]}")
