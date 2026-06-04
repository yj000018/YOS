import os, re, json

# Determine vault directory dynamically
if os.path.exists("/home/ubuntu/Y-WORLD"):
    VAULT = "/home/ubuntu/Y-WORLD"
elif os.path.exists("./Y-WORLD"):
    VAULT = "./Y-WORLD"
else:
    # Fallback to current directory if running in root of repo which contains folders like 00_System
    VAULT = "."

DOMAIN_MAP = {
    "00_System": {"domain": "System", "color": "#7c3aed", "icon": "⚙️"},
    "01_Cockpit": {"domain": "Cockpit", "color": "#4f46e5", "icon": "🎛️"},
    "02_Maps": {"domain": "Maps", "color": "#6366f1", "icon": "🗺️"},
    "03_Dashboards": {"domain": "Dashboards", "color": "#4338ca", "icon": "📊"},
    "04_Templates": {"domain": "Templates", "color": "#475569", "icon": "📋"},
    "10_Inbox": {"domain": "Inbox", "color": "#64748b", "icon": "📥"},
    "20_Life": {"domain": "Life", "color": "#ec4899", "icon": "❤️"},
    "30_Knowledge": {"domain": "Knowledge", "color": "#f59e0b", "icon": "📚"},
    "40_K-Cards": {"domain": "K-Cards", "color": "#10b981", "icon": "🃏"},
    "50_Projects": {"domain": "Projects", "color": "#f97316", "icon": "🚀"},
    "60_Y-OS": {"domain": "Y-OS", "color": "#4f46e5", "icon": "🧠"},
    "70_CasaTAO": {"domain": "CasaTAO", "color": "#f97316", "icon": "🏠"},
    "71_ARC_Anandaz": {"domain": "ARC Anandaz", "color": "#0d9488", "icon": "🏔️"},
    "80_Archetypes": {"domain": "Archetypes", "color": "#8b5cf6", "icon": "🎭"},
    "81_Y-Publishing": {"domain": "Y-Publishing", "color": "#ef4444", "icon": "📖"},
    "90_Reality_Interfaces": {"domain": "Reality Interfaces", "color": "#06b6d4", "icon": "🌐"},
}

# Define Explicit Meta-Nodes (the absolute top-level centers)
META_NODES = {
    "Y-WORLD ROOT MAP": "ROOT",
    "Y-OS Architecture": "Y-OS",
    "CasaTAO": "SANCTUARY",
    "ARC Anandaz": "SANCTUARY",
    "Sovereign Living": "PHILOSOPHY",
    "Archetypes System": "ARCHETYPES",
    "Y-Publishing Book 1": "PUBLISHING",
    "Health Protocol": "LIFE",
    "Notion Memory Hub": "MEMORY",
    "n8n Cognitive Automation": "AUTOMATION",
}

nodes = {}
edges = []
edge_set = set()

def get_domain_info(filepath):
    rel = os.path.relpath(filepath, VAULT)
    parts = rel.split(os.sep)
    folder = parts[0] if parts else ""
    for key, info in DOMAIN_MAP.items():
        if folder.startswith(key):
            return info
    return {"domain": "Other", "color": "#6b7280", "icon": "📄"}

def get_type_from_yaml(content):
    m = re.search(r'^type:\s*(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else "note"

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        node_id = fname[:-3]
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        domain_info = get_domain_info(fpath)
        node_type = get_type_from_yaml(content)
        links = re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]+)?\]\]', content)
        links = [l.strip() for l in links]
        
        # Determine node level / weight
        is_meta = node_id in META_NODES
        level = 1 if is_meta else (2 if node_type in ["map", "dashboard", "project"] else 3)
        
        nodes[node_id] = {
            "id": node_id,
            "label": node_id,
            "domain": domain_info["domain"],
            "color": domain_info["color"],
            "icon": domain_info["icon"],
            "type": node_type,
            "path": os.path.relpath(fpath, VAULT),
            "level": level,
            "isMeta": is_meta,
            "metaGroup": META_NODES.get(node_id, None)
        }
        for link in links:
            key = tuple(sorted([node_id, link]))
            if key not in edge_set:
                edge_set.add(key)
                edges.append({"source": node_id, "target": link})

# Inject all extra nodes
EXTRA_NODES = {
    # Y-OS
    "n8n Cognitive Automation": ("Y-OS","#4f46e5","🧠"),
    "Manus Operations": ("Y-OS","#4f46e5","🧠"),
    "CRT Model Routing": ("Y-OS","#4f46e5","🧠"),
    "Mem0 Sync": ("Y-OS","#4f46e5","🧠"),
    "Manus API": ("Y-OS","#4f46e5","🧠"),
    "Prompt Optimizer": ("Y-OS","#4f46e5","🧠"),
    "Tool Router": ("Y-OS","#4f46e5","🧠"),
    "GitHub Repo Y-WORLD": ("Y-OS","#4f46e5","🧠"),
    "Supabase DB": ("Y-OS","#4f46e5","🧠"),
    "Vercel Deploy": ("Y-OS","#4f46e5","🧠"),
    "Starlink Node": ("Y-OS","#4f46e5","🧠"),
    "Home Assistant CasaTAO": ("Y-OS","#4f46e5","🧠"),
    "Home Assistant ARC": ("Y-OS","#4f46e5","🧠"),
    "Session Synthesizer": ("Y-OS","#4f46e5","🧠"),
    "Memory Router": ("Y-OS","#4f46e5","🧠"),
    "Context Injector": ("Y-OS","#4f46e5","🧠"),
    "Wrike Integration": ("Y-OS","#4f46e5","🧠"),
    "Linear Integration": ("Y-OS","#4f46e5","🧠"),
    "Slack Integration": ("Y-OS","#4f46e5","🧠"),
    "Zapier Bridge": ("Y-OS","#4f46e5","🧠"),
    "pfSense Router": ("Y-OS","#4f46e5","🧠"),
    "Cloudflare Tunnel": ("Y-OS","#4f46e5","🧠"),
    "Upstash Redis": ("Y-OS","#4f46e5","🧠"),
    "Sentry Monitoring": ("Y-OS","#4f46e5","🧠"),
    "Backup Protocol": ("Y-OS","#4f46e5","🧠"),
    "Security Checklist": ("Y-OS","#4f46e5","🧠"),
    "Cost Optimizer": ("Y-OS","#4f46e5","🧠"),
    "Y-OS Roadmap": ("Y-OS","#4f46e5","🧠"),
    # AI Systems
    "Claude Sonnet": ("Reality Interfaces","#06b6d4","🌐"),
    "GPT-5": ("Reality Interfaces","#06b6d4","🌐"),
    "Gemini Flash": ("Reality Interfaces","#06b6d4","🌐"),
    "Flux Image Gen": ("Reality Interfaces","#06b6d4","🌐"),
    "ElevenLabs TTS": ("Reality Interfaces","#06b6d4","🌐"),
    "Perplexity Sonar": ("Reality Interfaces","#06b6d4","🌐"),
    "Grok xAI": ("Reality Interfaces","#06b6d4","🌐"),
    "Mistral 7B": ("Reality Interfaces","#06b6d4","🌐"),
    "Llama 3.1": ("Reality Interfaces","#06b6d4","🌐"),
    "Replicate API": ("Reality Interfaces","#06b6d4","🌐"),
    "HeyGen Avatars": ("Reality Interfaces","#06b6d4","🌐"),
    "Hume TTS": ("Reality Interfaces","#06b6d4","🌐"),
    "Firecrawl": ("Reality Interfaces","#06b6d4","🌐"),
    "Whisper STT": ("Reality Interfaces","#06b6d4","🌐"),
    "MiniMax Video": ("Reality Interfaces","#06b6d4","🌐"),
    "Canva AI": ("Reality Interfaces","#06b6d4","🌐"),
    # CasaTAO
    "CasaTAO Energy System": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Inverter": ("CasaTAO","#f97316","🏠"),
    "Pylontech Batteries": ("CasaTAO","#f97316","🏠"),
    "Victron Energy": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Network": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Studio": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Garden": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Terrace": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Cameras": ("CasaTAO","#f97316","🏠"),
    "CasaTAO Starlink Dish": ("CasaTAO","#f97316","🏠"),
    # ARC Anandaz
    "ARC Local Server": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Heating System": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Library": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Meditation Space": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Sauna": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Workshop": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Starlink Dish": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Cameras": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Terrace Alpine": ("ARC Anandaz","#0d9488","🏔️"),
    "ARC Reading Nook": ("ARC Anandaz","#0d9488","🏔️"),
    "Anandaz Philosophy": ("ARC Anandaz","#0d9488","🏔️"),
    # Knowledge / Library
    "Lao Tzu": ("Knowledge","#f59e0b","📚"),
    "Carl Jung": ("Knowledge","#f59e0b","📚"),
    "Nassim Taleb": ("Knowledge","#f59e0b","📚"),
    "Yuval Noah Harari": ("Knowledge","#f59e0b","📚"),
    "James Davidson": ("Knowledge","#f59e0b","📚"),
    "Frank Herbert": ("Knowledge","#f59e0b","📚"),
    "Daniel Kahneman": ("Knowledge","#f59e0b","📚"),
    "Tao Te Ching": ("Knowledge","#f59e0b","📚"),
    "Sapiens": ("Knowledge","#f59e0b","📚"),
    "The Sovereign Individual": ("Knowledge","#f59e0b","📚"),
    "Antifragile": ("Knowledge","#f59e0b","📚"),
    "Dune": ("Knowledge","#f59e0b","📚"),
    "Thinking Fast and Slow": ("Knowledge","#f59e0b","📚"),
    "ESP32-S3": ("Knowledge","#f59e0b","📚"),
    "MQTT Protocol": ("Knowledge","#f59e0b","📚"),
    "Shelly Devices": ("Knowledge","#f59e0b","📚"),
    "Ollama Local LLM": ("Knowledge","#f59e0b","📚"),
    "Docker": ("Knowledge","#f59e0b","📚"),
    "Proxmox": ("Knowledge","#f59e0b","📚"),
    "Raspberry Pi 5": ("Knowledge","#f59e0b","📚"),
    # Archetypes
    "The Architect Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Hermit Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Forge Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Oracle Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Scribe Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Wanderer Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Alchemist Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Guardian Archetype": ("Archetypes","#8b5cf6","🎭"),
    "The Trickster Archetype": ("Archetypes","#8b5cf6","🎭"),
    "Archetypes App": ("Archetypes","#8b5cf6","🎭"),
    "Norse Tradition": ("Archetypes","#8b5cf6","🎭"),
    "Taoist Tradition": ("Archetypes","#8b5cf6","🎭"),
    "Egyptian Tradition": ("Archetypes","#8b5cf6","🎭"),
    # Y-Publishing
    "Book 1 — Chapter 1 Notes": ("Y-Publishing","#ef4444","📖"),
    "Book 1 — Chapter 2 Notes": ("Y-Publishing","#ef4444","📖"),
    "Book 1 — Chapter 3 Notes": ("Y-Publishing","#ef4444","📖"),
    "Book 1 — Cover Design": ("Y-Publishing","#ef4444","📖"),
    "Research Database": ("Y-Publishing","#ef4444","📖"),
    "Y-Publishing Landing Page": ("Y-Publishing","#ef4444","📖"),
    "Newsletter YOS": ("Y-Publishing","#ef4444","📖"),
    "Podcast YOS": ("Y-Publishing","#ef4444","📖"),
    "Audiobook Production": ("Y-Publishing","#ef4444","📖"),
    # Life
    "Morning Ritual": ("Life","#ec4899","❤️"),
    "Cold Exposure Protocol": ("Life","#ec4899","❤️"),
    "Fasting Protocol": ("Life","#ec4899","❤️"),
    "Physical Training": ("Life","#ec4899","❤️"),
    "Sleep Protocol": ("Life","#ec4899","❤️"),
    "Financial Architecture": ("Life","#ec4899","❤️"),
    "Crypto Portfolio": ("Life","#ec4899","❤️"),
    "Real Estate Portfolio": ("Life","#ec4899","❤️"),
    "Reading Practice": ("Life","#ec4899","❤️"),
    "Annual Retreat Protocol": ("Life","#ec4899","❤️"),
    # Projects
    "Project - CasaTAO Solar Upgrade": ("Projects","#f97316","🚀"),
    "Project - ARC Smart Heating": ("Projects","#f97316","🚀"),
    "Project - Y-Publishing Book 1": ("Projects","#f97316","🚀"),
    "Project - Obsidian Git Setup": ("Projects","#f97316","🚀"),
    "Project - Archetypes App v1": ("Projects","#f97316","🚀"),
    "Project - Y-WORLD.net": ("Projects","#f97316","🚀"),
    # People
    "Yannick Jolliet": ("Life","#ec4899","👤"),
    # Reality Interfaces
    "Y-WORLD.net": ("Reality Interfaces","#06b6d4","🌐"),
    "Telegram Bot YOS": ("Reality Interfaces","#06b6d4","🌐"),
    "Obsidian Mobile": ("Reality Interfaces","#06b6d4","🌐"),
    "Voice Interface YOS": ("Reality Interfaces","#06b6d4","🌐"),
    "Y-WORLD iOS App": ("Reality Interfaces","#06b6d4","🌐"),
    "Dashboard TV Mode": ("Reality Interfaces","#06b6d4","🌐"),
    "Notion Public Pages": ("Reality Interfaces","#06b6d4","🌐"),
    "GitHub Public Profile": ("Reality Interfaces","#06b6d4","🌐"),
    # Life extra
    "Sicily Residency & Living": ("Life","#ec4899","❤️"),
    "Swiss Chalet Living": ("Life","#ec4899","❤️"),
}

# Add extra nodes if not already present
for nid, (domain, color, icon) in EXTRA_NODES.items():
    if nid not in nodes:
        is_meta = nid in META_NODES
        level = 1 if is_meta else (2 if nid.startswith("Project") or nid.endswith("Dashboard") else 3)
        nodes[nid] = {
            "id": nid, "label": nid,
            "domain": domain, "color": color, "icon": icon,
            "type": "node", "path": None,
            "level": level, "isMeta": is_meta,
            "metaGroup": META_NODES.get(nid, None)
        }

# Add extra edges (key relationships)
EXTRA_EDGES = [
    ("n8n Cognitive Automation","Notion Memory Hub"),
    ("n8n Cognitive Automation","CasaTAO"),
    ("n8n Cognitive Automation","ARC Anandaz"),
    ("n8n Cognitive Automation","Manus Operations"),
    ("n8n Cognitive Automation","Home Assistant CasaTAO"),
    ("n8n Cognitive Automation","Home Assistant ARC"),
    ("n8n Cognitive Automation","Telegram Bot YOS"),
    ("n8n Cognitive Automation","Slack Integration"),
    ("n8n Cognitive Automation","Zapier Bridge"),
    ("CRT Model Routing","Claude Sonnet"),
    ("CRT Model Routing","GPT-5"),
    ("CRT Model Routing","Gemini Flash"),
    ("CRT Model Routing","Mistral 7B"),
    ("CRT Model Routing","Perplexity Sonar"),
    ("CRT Model Routing","Y-OS Architecture"),
    ("Manus Operations","CRT Model Routing"),
    ("CasaTAO","CasaTAO Cameras"),
    ("CasaTAO","CasaTAO Starlink Dish"),
    ("CasaTAO","pfSense Router"),
    ("CasaTAO","Sovereign Living"),
    ("ARC Anandaz","Home Assistant ARC"),
    ("ARC Anandaz","ARC Local Server"),
    ("ARC Anandaz","ARC Heating System"),
    ("ARC Anandaz","ARC Library"),
    ("ARC Anandaz","ARC Meditation Space"),
    ("ARC Anandaz","ARC Sauna"),
    ("ARC Anandaz","ARC Workshop"),
    ("ARC Anandaz","ARC Starlink Dish"),
    ("ARC Anandaz","Anandaz Philosophy"),
    ("ARC Anandaz","Sovereign Living"),
    ("Frigate NVR","Coral Edge TPU"),
    ("Frigate NVR","CasaTAO Cameras"),
    ("Frigate NVR","ARC Cameras"),
    ("CasaTAO Energy System","CasaTAO Inverter"),
    ("CasaTAO Energy System","Pylontech Batteries"),
    ("CasaTAO Energy System","Victron Energy"),
    ("Home Assistant CasaTAO","MQTT Protocol"),
    ("Home Assistant CasaTAO","Shelly Devices"),
    ("Home Assistant ARC","MQTT Protocol"),
    ("Home Assistant ARC","Shelly Devices"),
    ("Home Assistant ARC","Ollama Local LLM"),
    ("ARC Local Server","Ollama Local LLM"),
    ("ARC Local Server","Docker"),
    ("ARC Local Server","Raspberry Pi 5"),
    ("Ollama Local LLM","Mistral 7B"),
    ("Ollama Local LLM","Llama 3.1"),
    ("Archetypes System","The Architect Archetype"),
    ("Archetypes System","The Hermit Archetype"),
    ("Archetypes System","The Forge Archetype"),
    ("Archetypes System","The Oracle Archetype"),
    ("Archetypes System","The Scribe Archetype"),
    ("Archetypes System","The Wanderer Archetype"),
    ("Archetypes System","The Alchemist Archetype"),
    ("Archetypes System","The Guardian Archetype"),
    ("Archetypes System","The Trickster Archetype"),
    ("Archetypes System","Archetypes App"),
    ("Norse Tradition","The Architect Archetype"),
    ("Norse Tradition","The Forge Archetype"),
    ("Norse Tradition","The Guardian Archetype"),
    ("Norse Tradition","The Trickster Archetype"),
    ("Taoist Tradition","The Hermit Archetype"),
    ("Taoist Tradition","The Wanderer Archetype"),
    ("Taoist Tradition","Tao Te Ching"),
    ("Taoist Tradition","Lao Tzu"),
    ("Egyptian Tradition","The Scribe Archetype"),
    ("Egyptian Tradition","The Oracle Archetype"),
    ("Egyptian Tradition","The Guardian Archetype"),
    ("Y-Publishing Book 1","Book 1 — Chapter 1 Notes"),
    ("Y-Publishing Book 1","Book 1 — Chapter 2 Notes"),
    ("Y-Publishing Book 1","Book 1 — Chapter 3 Notes"),
    ("Y-Publishing Book 1","Book 1 — Cover Design"),
    ("Y-Publishing Book 1","Archetypes System"),
    ("Y-Publishing Book 1","Research Database"),
    ("Y-Publishing Landing Page","Newsletter YOS"),
    ("Y-Publishing Landing Page","Podcast YOS"),
    ("Y-Publishing Landing Page","Audiobook Production"),
    ("Y-Publishing Landing Page","Vercel Deploy"),
    ("Health Protocol","Cold Exposure Protocol"),
    ("Health Protocol","Fasting Protocol"),
    ("Health Protocol","Physical Training"),
    ("Health Protocol","Sleep Protocol"),
    ("Health Protocol","ARC Sauna"),
    ("Morning Ritual","Health Protocol"),
    ("Morning Ritual","CasaTAO Terrace"),
    ("Morning Ritual","ARC Terrace Alpine"),
    ("Financial Architecture","Crypto Portfolio"),
    ("Financial Architecture","Real Estate Portfolio"),
    ("Financial Architecture","CasaTAO"),
    ("Financial Architecture","ARC Anandaz"),
    ("Sovereign Living","Financial Architecture"),
    ("Sovereign Living","Health Protocol"),
    ("Sovereign Living","Digital Detox Protocol"),
    ("Sovereign Living","CasaTAO"),
    ("Sovereign Living","ARC Anandaz"),
    ("Anandaz Philosophy","Sovereign Living"),
    ("Anandaz Philosophy","The Hermit Archetype"),
    ("Anandaz Philosophy","Tao Te Ching"),
    ("Anandaz Philosophy","ARC Meditation Space"),
    ("Yannick Jolliet","Y-OS Architecture"),
    ("Yannick Jolliet","CasaTAO"),
    ("Yannick Jolliet","ARC Anandaz"),
    ("Yannick Jolliet","Archetypes System"),
    ("Yannick Jolliet","Y-Publishing Book 1"),
    ("Tao Te Ching","Lao Tzu"),
    ("Sapiens","Yuval Noah Harari"),
    ("The Sovereign Individual","James Davidson"),
    ("Antifragile","Nassim Taleb"),
    ("Dune","Frank Herbert"),
    ("Thinking Fast and Slow","Daniel Kahneman"),
    ("Thinking Fast and Slow","CRT Model Routing"),
    ("Voice Interface YOS","ElevenLabs TTS"),
    ("Voice Interface YOS","Whisper STT"),
    ("Voice Interface YOS","n8n Cognitive Automation"),
    ("Voice Interface YOS","ESP32-S3"),
    ("Telegram Bot YOS","Whisper STT"),
    ("Telegram Bot YOS","Manus Operations"),
    ("Y-WORLD.net","Vercel Deploy"),
    ("Y-WORLD.net","Supabase DB"),
    ("Y-WORLD.net","React Framework"),
    ("Archetypes App","React Framework"),
    ("Archetypes App","Supabase DB"),
    ("Archetypes App","Vercel Deploy"),
    ("Cloudflare Tunnel","Home Assistant CasaTAO"),
    ("Cloudflare Tunnel","Frigate NVR"),
    ("pfSense Router","Home Assistant CasaTAO"),
    ("Reading Practice","ARC Reading Nook"),
    ("Reading Practice","Tao Te Ching"),
    ("Reading Practice","Antifragile"),
    ("Annual Retreat Protocol","ARC Anandaz"),
    ("Annual Retreat Protocol","ARC Meditation Space"),
    ("Annual Retreat Protocol","Y-OS Roadmap"),
]

for src, tgt in EXTRA_EDGES:
    key = tuple(sorted([src, tgt]))
    if key not in edge_set:
        edge_set.add(key)
        edges.append({"source": src, "target": tgt})

# Ensure all edge endpoints exist as nodes
for edge in edges:
    for side in ["source", "target"]:
        nid = edge[side]
        if nid not in nodes:
            is_meta = nid in META_NODES
            level = 1 if is_meta else 3
            nodes[nid] = {
                "id": nid, "label": nid,
                "domain": "Referenced", "color": "#475569", "icon": "🔗",
                "type": "reference", "path": None,
                "level": level, "isMeta": is_meta,
                "metaGroup": META_NODES.get(nid, None)
            }

# Compute connection counts
conn_count = {}
for e in edges:
    conn_count[e["source"]] = conn_count.get(e["source"], 0) + 1
    conn_count[e["target"]] = conn_count.get(e["target"], 0) + 1

for nid in nodes:
    nodes[nid]["connections"] = conn_count.get(nid, 0)

# Get unique domains with colors
domain_colors = {}
for n in nodes.values():
    if n["domain"] not in domain_colors:
        domain_colors[n["domain"]] = n["color"]

graph_data = {
    "nodes": list(nodes.values()),
    "edges": edges,
    "domain_colors": domain_colors,
    "stats": {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "domains": len(domain_colors)
    }
}

# Determine output path dynamically
output_dir = "client/public" if os.path.exists("client/public") else "."
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "graph_data.json")

with open(output_path, "w") as f:
    json.dump(graph_data, f, indent=2)

print(f"✓ {len(nodes)} nodes, {len(edges)} edges, {len(domain_colors)} domains")
top = sorted(nodes.values(), key=lambda x: x['connections'], reverse=True)[:15]
print("Top 15 hubs:")
for n in top:
    print(f"  {n['connections']:3d}  {n['domain']:20s}  {n['label']}")
