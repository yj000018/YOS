---
name: task-manager
description: Comprehensive task lifecycle management for Manus with cleanup, similarity detection, intelligent merging, and archival. Use for batch task operations, finding related tasks, consolidating similar tasks, archiving to Notion, and automated cleanup workflows.
---

# Task Manager

Comprehensive task lifecycle management for Manus: cleanup, similarity detection, intelligent merging, and archival.

## Capabilities

- **List & Filter** — Retrieve tasks with flexible filters
- **Similarity Detection** — Find related tasks using semantic embeddings
- **Intelligent Merge** — Consolidate similar tasks with AI-powered synthesis
- **Notion Archive** — Export tasks to Notion with structured formatting
- **Batch Operations** — Process multiple tasks efficiently

## Installation

System location: `/home/ubuntu/manus-task-manager/`

### Required Environment Variables

```bash
export MANUS_API_KEY="your_manus_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export NOTION_API_KEY="your_notion_api_key"  # Optional
export NOTION_DATABASE_ID="your_database_id"  # Optional
```

### Required Packages

```bash
sudo pip3 install openai requests scikit-learn numpy
```

## CLI Commands

### List Tasks

```bash
python3 /home/ubuntu/manus-task-manager/manus_tasks.py list \
  --limit 50 \
  --status completed
```

### Find Similar Tasks

```bash
python3 /home/ubuntu/manus-task-manager/manus_tasks.py similar \
  --limit 50 \
  --threshold 0.8 \
  --min-size 2 \
  --output similar_tasks.json
```

**Threshold guide:**
- `0.9+` — Near-duplicates
- `0.7-0.8` — Related topics (recommended)
- `0.5-0.6` — Broad themes

### Merge Tasks

```bash
# Preview
python3 /home/ubuntu/manus-task-manager/manus_tasks.py merge \
  task_id_1,task_id_2,task_id_3 \
  --dry-run

# Execute
python3 /home/ubuntu/manus-task-manager/manus_tasks.py merge \
  task_id_1,task_id_2,task_id_3 \
  --strategy synthesis
```

**Strategies:** `synthesis` (AI-powered), `chronological`, `thematic`

### Archive to Notion

```bash
python3 /home/ubuntu/manus-task-manager/manus_tasks.py archive \
  task_id_1,task_id_2 \
  --output archive_results.json
```

### Full Cleanup Workflow

```bash
# Preview
python3 /home/ubuntu/manus-task-manager/manus_tasks.py cleanup \
  --limit 50 \
  --threshold 0.8 \
  --min-size 3

# Execute with archiving
python3 /home/ubuntu/manus-task-manager/manus_tasks.py cleanup \
  --limit 50 \
  --auto \
  --archive
```

**Workflow:**
1. Fetch tasks
2. Generate embeddings
3. Cluster similar tasks
4. Suggest merge groups
5. Execute merges (if `--auto`)
6. Archive source tasks (if `--archive`)

## Programmatic Usage

```python
import sys
sys.path.insert(0, '/home/ubuntu/manus-task-manager/src')

from task_manager import ManusTaskManager
from similarity_detector import SimilarityDetector
from merge_engine import MergeEngine
from notion_archiver import NotionArchiver

# Initialize
tm = ManusTaskManager()
sd = SimilarityDetector()
me = MergeEngine(tm)
na = NotionArchiver()

# Workflow
tasks = tm.list_tasks(limit=50, status='completed')
embeddings = sd.batch_generate_embeddings(tasks, tm)
clusters = sd.cluster_tasks(embeddings, eps=0.2, min_samples=2)

# Merge cluster
task_ids = clusters[0]
result = me.merge_tasks(task_ids, strategy='synthesis')

# Archive
if result.get('success'):
    source_tasks = tm.batch_get_tasks(result['source_task_ids'])
    na.batch_archive(source_tasks, tm)
```

## Configuration

### Similarity Detection

Adjust in `similarity_detector.py`:
- `eps` — Max distance (lower = stricter)
- `min_samples` — Min cluster size

### Merge Strategies

- `synthesis` — GPT-4 synthesis with conflict detection
- `chronological` — Temporal order preservation
- `thematic` — Topic-based grouping

### Notion Export

Customize in `notion_archiver.py`:
- Markdown → Notion blocks conversion
- Metadata fields
- Page structure

## Best Practices

### Start with Preview

Always run `--dry-run` or omit `--auto` first.

### Adjust Threshold

- High (0.9+): Very strict
- Medium (0.7-0.8): Related topics
- Low (0.5-0.6): Broad themes

### Batch Processing

Process 50-100 tasks at a time for rate limits.

### Backup Before Merge

Source tasks updated with `merged_into` metadata but not deleted.

### Review Conflicts

Check `conflicts` field in merge results.

## Troubleshooting

### Rate Limiting

Increase delays in `similarity_detector.py`:
```python
delay = 1.0  # From 0.5 to 1.0 second
```

### Clear Cache

```bash
rm /home/ubuntu/manus-task-manager/cache/embeddings_cache.json
```

### Notion API Errors

Ensure:
- Read/write access to database
- Correct database ID (not page ID)
- Required properties exist

## Examples

### Weekly Cleanup

```bash
python3 /home/ubuntu/manus-task-manager/manus_tasks.py cleanup \
  --status completed \
  --threshold 0.8 \
  --min-size 3 \
  --auto \
  --archive
```

### Manual Merge

```bash
# Find similar
python3 /home/ubuntu/manus-task-manager/manus_tasks.py similar \
  --limit 50 \
  --output similar.json

# Merge specific cluster
python3 /home/ubuntu/manus-task-manager/manus_tasks.py merge \
  task_abc,task_def,task_ghi \
  --strategy synthesis
```

### Archive Only

```bash
python3 /home/ubuntu/manus-task-manager/manus_tasks.py archive \
  task_id_1,task_id_2,task_id_3
```

## Files

```
/home/ubuntu/manus-task-manager/
├── manus_tasks.py              # Main CLI
├── src/
│   ├── task_manager.py         # Core operations
│   ├── similarity_detector.py  # Embeddings & clustering
│   ├── merge_engine.py         # Intelligent merging
│   └── notion_archiver.py      # Notion export
├── cache/
│   └── embeddings_cache.json   # Cached embeddings
├── logs/
│   └── merge_*.json            # Merge logs
└── backups/
    └── task_*.json             # Task backups
```

## Notes

- **Costs**: ~$0.0001/task (embeddings), ~$0.01/merge (GPT-4)
- **Performance**: 50 tasks ~2-3 minutes
- **Safety**: All operations logged
- **Vector DB**: Embeddings cache ready for vector DB integration (already decided/partially implemented)
- **Session/Chat Manager**: Web UI for visual management (separate from task todo list)

## Support

- Architecture: `/home/ubuntu/task_mgmt_system/manus_task_management_architecture_v1.md`
- Source: `/home/ubuntu/manus-task-manager/src/`
- README: `/home/ubuntu/manus-task-manager/README.md`
