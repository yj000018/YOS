"""
Unit tests for yos_memory package.
Phase 1 — MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR
"""
import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Set up test environment before imports
TEST_REPO = tempfile.mkdtemp()
os.environ["YOS_REPO_PATH"] = TEST_REPO
os.environ.pop("NOTION_API_KEY", None)  # Ensure Notion key is not set

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from yos_memory.ids import generate_global_uid, generate_content_hash, generate_memory_key
from yos_memory.frontmatter import read_markdown, write_markdown
from yos_memory.schemas import validate_frontmatter, create_base_frontmatter
from yos_memory.git_store import write_canonical_file
from yos_memory.dedup import DedupState
from yos_memory.ledger import SessionLedger

# ─────────────────────────────────────────────────────────────────────────────
# IDs
# ─────────────────────────────────────────────────────────────────────────────

def test_global_uid_stable():
    uid1 = generate_global_uid("Manus", "abc123")
    uid2 = generate_global_uid("Manus", "abc123")
    assert uid1 == uid2 == "manus_abc123"

def test_global_uid_different_sources():
    uid1 = generate_global_uid("Manus", "abc123")
    uid2 = generate_global_uid("ChatGPT", "abc123")
    assert uid1 != uid2

def test_content_hash_deterministic():
    h1 = generate_content_hash("Hello World")
    h2 = generate_content_hash("Hello World")
    assert h1 == h2
    assert h1.startswith("sha256:")

def test_content_hash_different_content():
    h1 = generate_content_hash("Hello World")
    h2 = generate_content_hash("Hello World!")
    assert h1 != h2

def test_content_hash_normalizes_line_endings():
    h1 = generate_content_hash("Hello\nWorld")
    h2 = generate_content_hash("Hello\r\nWorld")
    assert h1 == h2

def test_memory_key_format():
    key = generate_memory_key("session", "manus_abc123", "sha256:deadbeef")
    assert key == "session:manus_abc123:sha256:deadbeef"

def test_global_uid_invalid_raises():
    try:
        generate_global_uid("", "abc123")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# Frontmatter
# ─────────────────────────────────────────────────────────────────────────────

def test_frontmatter_round_trip():
    metadata = {"key": "value", "number": 42, "list": [1, 2, 3]}
    body = "# Test\n\nBody content here."
    content = write_markdown(metadata, body)
    parsed_meta, parsed_body = read_markdown(content)
    assert parsed_meta == metadata
    assert "Body content here." in parsed_body

def test_frontmatter_no_frontmatter():
    content = "# Just a title\n\nNo frontmatter here."
    meta, body = read_markdown(content)
    assert meta == {}
    assert "Just a title" in body

def test_frontmatter_empty_body():
    metadata = {"key": "value"}
    body = ""
    content = write_markdown(metadata, body)
    parsed_meta, parsed_body = read_markdown(content)
    assert parsed_meta == metadata

# ─────────────────────────────────────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────────────────────────────────────

def test_validate_frontmatter_valid():
    meta = create_base_frontmatter(
        memory_type="session",
        source="manus",
        source_id="abc123",
        memory_id="manus_abc123",
        content_hash="sha256:abc",
        canonical_path="08_LOGS/session-ledger/sessions/manus/2026/manus_abc123.md",
        created_at="2026-07-31T00:00:00Z",
        updated_at="2026-07-31T00:00:00Z"
    )
    assert validate_frontmatter(meta) is True

def test_validate_frontmatter_missing_field():
    meta = create_base_frontmatter(
        memory_type="session",
        source="manus",
        source_id="abc123",
        memory_id="manus_abc123",
        content_hash="sha256:abc",
        canonical_path="08_LOGS/session-ledger/sessions/manus/2026/manus_abc123.md",
        created_at="2026-07-31T00:00:00Z",
        updated_at="2026-07-31T00:00:00Z"
    )
    del meta["content_hash"]
    try:
        validate_frontmatter(meta)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_validate_frontmatter_invalid_type():
    meta = create_base_frontmatter(
        memory_type="invalid_type",
        source="manus",
        source_id="abc123",
        memory_id="manus_abc123",
        content_hash="sha256:abc",
        canonical_path="08_LOGS/session-ledger/sessions/manus/2026/manus_abc123.md",
        created_at="2026-07-31T00:00:00Z",
        updated_at="2026-07-31T00:00:00Z"
    )
    try:
        validate_frontmatter(meta)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# Git Store
# ─────────────────────────────────────────────────────────────────────────────

def test_atomic_write():
    target = Path(TEST_REPO) / "test_dir" / "test_file.md"
    content = "# Test\n\nContent here."
    path, hash_val = write_canonical_file(target, content)
    assert target.exists()
    assert target.read_text() == content
    assert hash_val.startswith("sha256:")

def test_atomic_write_creates_dirs():
    target = Path(TEST_REPO) / "deeply" / "nested" / "dir" / "file.md"
    content = "Test content"
    write_canonical_file(target, content)
    assert target.exists()

def test_atomic_write_no_temp_file_on_success():
    target = Path(TEST_REPO) / "no_temp_test.md"
    write_canonical_file(target, "content")
    temp = target.with_suffix('.tmp')
    assert not temp.exists()

# ─────────────────────────────────────────────────────────────────────────────
# Dedup
# ─────────────────────────────────────────────────────────────────────────────

def test_dedup_new_uid_not_processed():
    state_file = Path(TEST_REPO) / "state" / "test_dedup.json"
    dedup = DedupState(state_file)
    assert not dedup.is_processed("manus_new123")

def test_dedup_after_git_write():
    state_file = Path(TEST_REPO) / "state" / "test_dedup2.json"
    dedup = DedupState(state_file)
    dedup.update_git_state("manus_abc123", "sha256:abc", "08_LOGS/sessions/manus/2026/manus_abc123.md")
    assert dedup.is_processed("manus_abc123", "sha256:abc")

def test_dedup_same_uid_different_hash():
    state_file = Path(TEST_REPO) / "state" / "test_dedup3.json"
    dedup = DedupState(state_file)
    dedup.update_git_state("manus_abc123", "sha256:abc", "path/to/file.md")
    # Same UID but different content hash → not a duplicate
    assert not dedup.is_processed("manus_abc123", "sha256:xyz")

def test_dedup_persists_across_instances():
    state_file = Path(TEST_REPO) / "state" / "test_dedup4.json"
    dedup1 = DedupState(state_file)
    dedup1.update_git_state("manus_persist", "sha256:persist", "path/to/file.md")
    
    dedup2 = DedupState(state_file)
    assert dedup2.is_processed("manus_persist", "sha256:persist")

def test_dedup_mem0_state_update():
    state_file = Path(TEST_REPO) / "state" / "test_dedup5.json"
    dedup = DedupState(state_file)
    dedup.update_git_state("manus_m0", "sha256:m0", "path/to/file.md")
    dedup.update_mem0_state("manus_m0", "synced", ["mem0_id_1", "mem0_id_2"])
    
    record = dedup.get_record("manus_m0")
    assert record["mem0_status"] == "synced"
    assert "mem0_id_1" in record["mem0_memory_ids"]

# ─────────────────────────────────────────────────────────────────────────────
# Mem0 Security
# ─────────────────────────────────────────────────────────────────────────────

def test_mem0_rejects_jwt_in_projection():
    from yos_memory.mem0_store import Mem0Store
    store = Mem0Store()
    store.api_key = "test_key"
    
    jwt_content = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.signature"
    try:
        store.push_projection(jwt_content, {})
        assert False, "Should have raised ValueError for JWT in projection"
    except ValueError as e:
        assert "SECURITY VIOLATION" in str(e)

# ─────────────────────────────────────────────────────────────────────────────
# Notion Absence
# ─────────────────────────────────────────────────────────────────────────────

def test_runs_without_notion_api_key():
    """All core operations must work without NOTION_API_KEY."""
    assert "NOTION_API_KEY" not in os.environ
    
    # These should all work without Notion
    uid = generate_global_uid("manus", "test123")
    hash_val = generate_content_hash("test content")
    meta = create_base_frontmatter(
        memory_type="session",
        source="manus",
        source_id="test123",
        memory_id=uid,
        content_hash=hash_val,
        canonical_path="08_LOGS/sessions/manus/2026/manus_test123.md",
        created_at="2026-07-31T00:00:00Z",
        updated_at="2026-07-31T00:00:00Z"
    )
    assert validate_frontmatter(meta) is True

# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_global_uid_stable,
        test_global_uid_different_sources,
        test_content_hash_deterministic,
        test_content_hash_different_content,
        test_content_hash_normalizes_line_endings,
        test_memory_key_format,
        test_global_uid_invalid_raises,
        test_frontmatter_round_trip,
        test_frontmatter_no_frontmatter,
        test_frontmatter_empty_body,
        test_validate_frontmatter_valid,
        test_validate_frontmatter_missing_field,
        test_validate_frontmatter_invalid_type,
        test_atomic_write,
        test_atomic_write_creates_dirs,
        test_atomic_write_no_temp_file_on_success,
        test_dedup_new_uid_not_processed,
        test_dedup_after_git_write,
        test_dedup_same_uid_different_hash,
        test_dedup_persists_across_instances,
        test_dedup_mem0_state_update,
        test_mem0_rejects_jwt_in_projection,
        test_runs_without_notion_api_key,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {test.__name__}: {e}")
            failed += 1
            
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    
    # Cleanup
    shutil.rmtree(TEST_REPO, ignore_errors=True)
    
    sys.exit(0 if failed == 0 else 1)
