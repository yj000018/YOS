import os
import json
import subprocess
import datetime
from openai import OpenAI

def mcp_call(tool_name, payload):
    cmd = [
        "manus-mcp-cli", "tool", "call", tool_name,
        "--server", "notion",
        "--input", json.dumps(payload)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return r.stdout + r.stderr

def fetch_registry_data():
    print("Fetching Artifact Registry data...")
    payload = {"query": "ART-", "query_type": "internal"}
    out = mcp_call('notion-search', payload)
    
    artifacts = []
    try:
        json_start = out.find('{"results"')
        if json_start == -1:
            raise ValueError("No JSON found")
        json_str = out[json_start:].split('\nTool execution')[0].strip()
        data = json.loads(json_str)
        
        for r in data.get('results', []):
            title = r.get('title', '')
            if title.startswith('ART-') and '—' not in title:
                artifacts.append(r)
                
    except Exception as e:
        print(f"Error parsing registry data: {e}")
        
    return artifacts

def process_artifacts(raw_artifacts):
    missions = {}
    open_loops = []
    metrics = {
        "total_artifacts": len(raw_artifacts),
        "artifacts_in_draft": 0,
        "artifacts_in_review": 0
    }
    
    for r in raw_artifacts:
        art_id = r.get('title', '').split()[0]
        status = "Accepted" # Mocked for E2E
        mission_id = "MISS-E2E-V1"
        mission_status = "Completed" # New field from v1.1
        
        if mission_id not in missions:
            missions[mission_id] = {
                "id": mission_id,
                "name": "First End-to-End Run",
                "status": mission_status,
                "health": "Green",
                "current_phase": "Learning",
                "artifacts": []
            }
            
        missions[mission_id]["artifacts"].append(art_id)
        
        if status == "Draft": metrics["artifacts_in_draft"] += 1
        if status == "Ready For Review": metrics["artifacts_in_review"] += 1
        
    metrics["total_missions"] = len(missions)
    metrics["active_missions"] = sum(1 for m in missions.values() if m["status"] == "Active")
    metrics["blocked_missions"] = sum(1 for m in missions.values() if m["status"] == "Blocked")
    metrics["completed_missions"] = sum(1 for m in missions.values() if m["status"] == "Completed")
    
    # Mocking an open loop for demonstration
    if "MISS-E2E-V1" in missions:
        open_loops.append({
            "id": "OL-001",
            "mission_id": "MISS-E2E-V1",
            "artifact_id": "ART-E2E-007",
            "rule_id": "L-02",
            "severity": "P3",
            "assignee": "Saraswati",
            "description": "Terminal artifact lacks explicit Archived Date."
        })
        
    return missions, open_loops, metrics

def generate_ceo_briefing(missions, open_loops, metrics):
    print("Generating CEO Briefing via LLM...")
    
    state_summary = f"""
    Metrics: {json.dumps(metrics)}
    Missions: {json.dumps(missions)}
    Open Loops: {json.dumps(open_loops)}
    """
    
    prompt = f"""
    You are ECO (Lakshmi), the Executive Coordination Officer of Y-OS.
    Your job is to provide executive visibility to the CEO.
    
    Based on the following Artifact Registry state, generate a CEO Briefing.
    Use the exact template structure defined in Lakshmi_CEO_Briefing_Template_v1.
    Keep it dense, actionable, and under 60 seconds to read.
    
    State:
    {state_summary}
    """
    
    try:
        base_url = os.environ.get('OPENAI_BASE_URL', 'https://api.manus.im/api/llm-proxy/v1')
        api_key = os.environ.get('OPENAI_API_KEY') or 'sk-placeholder'
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        models = client.models.list()
        model_id = models.data[0].id if models.data else 'gpt-4o'
        print(f"Using model: {model_id}")
        
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are Lakshmi, the Executive Coordination Officer of Y-OS."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        if response and response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        return "LLM returned empty response."
    except Exception as e:
        print(f"LLM Error: {e}")
        return "# Error generating briefing\n" + str(e)

def main():
    print("Starting Lakshmi Runtime MVP v2...")
    
    raw_artifacts = fetch_registry_data()
    print(f"Fetched {len(raw_artifacts)} artifacts.")
    
    missions, open_loops, metrics = process_artifacts(raw_artifacts)
    
    dashboard_state = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "metrics": metrics,
        "missions": list(missions.values()),
        "open_loops": open_loops,
        "ceo_action_queue": []
    }
    
    with open("/home/ubuntu/yreg/lakshmi_dashboard_state.json", "w") as f:
        json.dump(dashboard_state, f, indent=2)
    print("Wrote lakshmi_dashboard_state.json")
    
    briefing = generate_ceo_briefing(missions, open_loops, metrics)
    
    with open("/home/ubuntu/yreg/lakshmi_ceo_briefing.md", "w") as f:
        f.write(briefing)
    print("Wrote lakshmi_ceo_briefing.md")
    
    with open("/home/ubuntu/yreg/lakshmi_open_loops.md", "w") as f:
        f.write("# Open Loops Report\n\n")
        for ol in open_loops:
            f.write(f"- **{ol['id']}** [{ol['severity']}] Mission: {ol['mission_id']} - {ol['description']} (Assignee: {ol['assignee']})\n")
    print("Wrote lakshmi_open_loops.md")
    
    print("Lakshmi Runtime execution complete.")

if __name__ == "__main__":
    main()
