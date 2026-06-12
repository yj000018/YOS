#!/usr/bin/env python3
"""
Y-REG Scanner v1.0
Scans all SKILL.md files and extracts metadata for Y-REG expansion.
Uses Claude/Gemini to extract capabilities from unstructured SKILL.md content.
"""

import os, json, re, subprocess, glob
from pathlib import Path

SKILLS_DIR = "/home/ubuntu/skills"
OUTPUT_FILE = "/home/ubuntu/yreg/scan_results.json"

# ─────────────────────────────────────────────────────────────────────────────
# SKILL METADATA EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def read_skill_md(skill_name):
    """Read SKILL.md for a given skill."""
    path = f"{SKILLS_DIR}/{skill_name}/SKILL.md"
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()

def extract_metadata_from_skill(skill_name, content):
    """
    Extract structured metadata from a SKILL.md file.
    Returns a dict with: name, description, capabilities[], tags[], dependencies[], use_when
    """
    meta = {
        "slug": f"skill-{skill_name}",
        "name": skill_name,
        "type": "skill",
        "status": "active",
        "visibility": "advanced",
        "description": "",
        "use_when": "",
        "capabilities": [],
        "tags": [],
        "dependencies": [],
        "git_path": f"skills/{skill_name}/SKILL.md",
        "module_owner": "Y-DEV",
    }

    # Extract description from first paragraph after title
    lines = content.split("\n")
    title_found = False
    desc_lines = []
    for line in lines[:30]:
        if line.startswith("#"):
            title_found = True
            # Try to extract name from title
            title_text = re.sub(r'^#+\s*', '', line).strip()
            if title_text:
                meta["name"] = title_text[:80]
            continue
        if title_found and line.strip() and not line.startswith("#"):
            desc_lines.append(line.strip())
            if len(desc_lines) >= 2:
                break

    if desc_lines:
        meta["description"] = " ".join(desc_lines)[:300]

    # Extract "use_when" section
    use_when_match = re.search(r'[Uu]se\s+[Ww]hen[:\s]+([^\n]+(?:\n(?!#)[^\n]+)*)', content)
    if use_when_match:
        meta["use_when"] = use_when_match.group(1).strip()[:300]

    # Extract capabilities from content patterns
    caps = []

    # Pattern: "Use when user asks to X, Y, Z"
    use_when_caps = re.findall(r'(?:Use when|use when|when user)[^.]*?(?:to|for)\s+([a-z][^.,\n]{5,60})', content, re.IGNORECASE)
    for cap in use_when_caps[:5]:
        cap = cap.strip().rstrip('.')
        if len(cap) > 10:
            caps.append(cap)

    # Pattern: "Supports X", "Provides X", "Enables X"
    support_caps = re.findall(r'(?:Supports?|Provides?|Enables?|Allows?|Handles?)\s+([a-z][^.,\n]{5,60})', content, re.IGNORECASE)
    for cap in support_caps[:5]:
        cap = cap.strip().rstrip('.')
        if len(cap) > 10:
            caps.append(cap)

    # Pattern: numbered or bulleted lists of features
    list_items = re.findall(r'^\s*[-*•]\s+([A-Z][^.\n]{10,80})', content, re.MULTILINE)
    for item in list_items[:8]:
        item = item.strip()
        if len(item) > 10 and not item.startswith("MUST") and not item.startswith("DO NOT"):
            caps.append(item)

    # Deduplicate and clean
    seen = set()
    clean_caps = []
    for cap in caps:
        cap_lower = cap.lower()[:50]
        if cap_lower not in seen and len(cap) > 8:
            seen.add(cap_lower)
            clean_caps.append(cap[:100])
    meta["capabilities"] = clean_caps[:8]

    # Extract tags from content
    tags = []
    tag_patterns = [
        r'\b(memory|notion|github|slack|supabase|n8n|obsidian|git|python|mcp|api|web|browser|audio|video|image|pdf|excel|slides|email|calendar|search|llm|ai|automation|workflow|agent|skill|protocol)\b'
    ]
    for pattern in tag_patterns:
        found = re.findall(pattern, content, re.IGNORECASE)
        tags.extend([t.lower() for t in found])
    meta["tags"] = list(set(tags))[:10]

    # Detect dependencies (mentions of other skills or tools)
    skill_names = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(f"{SKILLS_DIR}/{d}")]
    for other_skill in skill_names:
        if other_skill != skill_name and other_skill in content:
            meta["dependencies"].append(f"skill-{other_skill}")

    return meta

# ─────────────────────────────────────────────────────────────────────────────
# CAPABILITY NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

# Canonical capability taxonomy — maps raw extracted text to normalized slugs
CAPABILITY_MAP = {
    # Memory & Knowledge
    "memory": ("memory-store-retrieve", "Memory Store & Retrieve", "Y-MEM"),
    "store": ("memory-store-retrieve", "Memory Store & Retrieve", "Y-MEM"),
    "retrieve": ("memory-store-retrieve", "Memory Store & Retrieve", "Y-MEM"),
    "archive": ("session-archiving", "Session Archiving", "Y-MEM"),
    "session": ("session-management", "Session Management", "Y-MEM"),
    "notion": ("notion-integration", "Notion Integration", "Y-MEM"),
    "knowledge": ("knowledge-management", "Knowledge Management", "Y-MEM"),

    # Context & Analysis
    "context": ("context-assembly", "Context Assembly", "Y-CTX"),
    "analysis": ("data-analysis", "Data Analysis", "Y-CTX"),
    "research": ("web-research", "Web Research", "Y-CTX"),
    "search": ("web-search", "Web Search", "Y-CTX"),
    "synthesis": ("content-synthesis", "Content Synthesis", "Y-CTX"),
    "summarize": ("content-synthesis", "Content Synthesis", "Y-CTX"),

    # Generation & Creation
    "text": ("text-generation", "Text Generation", "Y-ORC"),
    "writing": ("text-generation", "Text Generation", "Y-ORC"),
    "image": ("image-generation", "Image Generation", "Y-ORC"),
    "video": ("video-generation", "Video Generation", "Y-ORC"),
    "audio": ("audio-generation", "Audio Generation", "Y-ORC"),
    "music": ("music-generation", "Music Generation", "Y-ORC"),
    "speech": ("speech-synthesis", "Speech Synthesis", "Y-ORC"),
    "slides": ("slides-generation", "Slides Generation", "Y-ORC"),
    "excel": ("spreadsheet-creation", "Spreadsheet Creation", "Y-ORC"),
    "pdf": ("pdf-processing", "PDF Processing", "Y-ORC"),

    # Code & Development
    "code": ("code-execution", "Code Execution", "Y-DEV"),
    "python": ("code-execution", "Code Execution", "Y-DEV"),
    "web": ("web-development", "Web Development", "Y-DEV"),
    "github": ("github-integration", "GitHub Integration", "Y-DEV"),
    "api": ("api-integration", "API Integration", "Y-DEV"),

    # Automation & Orchestration
    "automation": ("workflow-automation", "Workflow Automation", "Y-ORC"),
    "workflow": ("workflow-execution", "Workflow Execution", "Y-ORC"),
    "n8n": ("n8n-automation", "n8n Automation", "Y-ORC"),
    "zapier": ("zapier-automation", "Zapier Automation", "Y-ORC"),
    "browser": ("browser-automation", "Browser Automation", "Y-ORC"),
    "playwright": ("browser-automation", "Browser Automation", "Y-ORC"),

    # Registry & Identity
    "registry": ("registry-lookup", "Registry Lookup", "Y-REG"),
    "slug": ("identifier-resolution", "Identifier Resolution", "Y-ID"),
    "naming": ("identifier-resolution", "Identifier Resolution", "Y-ID"),

    # Logging & Audit
    "audit": ("audit-logging", "Audit Logging", "Y-LOG"),
    "log": ("audit-logging", "Audit Logging", "Y-LOG"),
    "track": ("task-tracking", "Task Tracking", "Y-LOG"),

    # Capabilities
    "capability": ("capability-acquisition", "Capability Acquisition", "Y-CAP"),
    "skill": ("skill-management", "Skill Management", "Y-CAP"),

    # Communication
    "email": ("email-integration", "Email Integration", "Y-ORC"),
    "slack": ("slack-integration", "Slack Integration", "Y-ORC"),
    "calendar": ("calendar-management", "Calendar Management", "Y-ORC"),
    "telegram": ("messaging-integration", "Messaging Integration", "Y-ORC"),

    # Design
    "canva": ("design-creation", "Design Creation", "Y-ORC"),
    "design": ("design-creation", "Design Creation", "Y-ORC"),

    # Data
    "supabase": ("database-operations", "Database Operations", "Y-ORC"),
    "airtable": ("database-operations", "Database Operations", "Y-ORC"),
    "data": ("data-analysis", "Data Analysis", "Y-CTX"),

    # LLM
    "llm": ("llm-routing", "LLM Routing", "Y-ORC"),
    "ai": ("ai-model-invocation", "AI Model Invocation", "Y-ORC"),
    "mcp": ("mcp-tool-invocation", "MCP Tool Invocation", "Y-ORC"),
    "prompt": ("prompt-engineering", "Prompt Engineering", "Y-ORC"),
    "optimize": ("prompt-engineering", "Prompt Engineering", "Y-ORC"),
}

def normalize_capabilities(raw_caps, tags, skill_name):
    """Map raw capabilities and tags to canonical capability slugs."""
    found = {}  # slug -> (slug, name, module)

    # Check tags first (more reliable)
    for tag in tags:
        if tag in CAPABILITY_MAP:
            slug, name, module = CAPABILITY_MAP[tag]
            found[slug] = (slug, name, module)

    # Check raw capabilities text
    for cap_text in raw_caps:
        cap_lower = cap_text.lower()
        for keyword, mapping in CAPABILITY_MAP.items():
            if keyword in cap_lower:
                slug, name, module = mapping
                found[slug] = (slug, name, module)

    # Always add skill-management for skills
    found["skill-management"] = ("skill-management", "Skill Management", "Y-CAP")

    return list(found.values())

# ─────────────────────────────────────────────────────────────────────────────
# MAIN SCAN
# ─────────────────────────────────────────────────────────────────────────────

def scan_all_skills():
    """Scan all skills and return structured data."""
    skills = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(f"{SKILLS_DIR}/{d}")]
    results = []

    print(f"Scanning {len(skills)} skills...")
    for skill_name in sorted(skills):
        content = read_skill_md(skill_name)
        if not content:
            print(f"  SKIP {skill_name} (no SKILL.md)")
            continue

        meta = extract_metadata_from_skill(skill_name, content)
        normalized_caps = normalize_capabilities(meta["capabilities"], meta["tags"], skill_name)
        meta["normalized_capabilities"] = normalized_caps
        results.append(meta)
        print(f"  ✓ {skill_name}: {len(normalized_caps)} caps, {len(meta['tags'])} tags")

    return results

if __name__ == "__main__":
    results = scan_all_skills()

    # Save raw scan results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nScan complete: {len(results)} skills")

    # Summary
    all_caps = {}
    for skill in results:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            all_caps[cap_slug] = (cap_name, cap_module)

    print(f"Unique capabilities discovered: {len(all_caps)}")
    for slug, (name, module) in sorted(all_caps.items()):
        print(f"  [{module}] {name} ({slug})")
