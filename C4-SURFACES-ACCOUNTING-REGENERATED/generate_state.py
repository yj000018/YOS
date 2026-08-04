import json
import datetime

state = {
  "schema_version": "1.0",
  "report_id": "C4-SURFACES-ACCOUNTING",
  "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
  "source_snapshot_at": "2026-07-31T05:09:43Z",
  "overall_status": "VERIFIED_PARTIAL",
  "surfaces": {
    "projects": {
      "semantic_project_taxonomy": {
        "labels_count": 62,
        "tagged_conversations": 239,
        "source": "enriched_239",
        "status": "CAPTURED_DERIVED",
        "evidence_refs": [
          {
            "path": "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_projects.json",
            "sha256": "1cd77cecd57e4894327e9fdf42be256feec49b7a5b56585e5a4eaed9e79cd66a",
            "source_type": "legacy_surface_report",
            "observed_at": "2026-07-31T05:00:00Z",
            "observation": "Reports 62 projects derived from enriched-239 conversations",
            "supports": "semantic_project_taxonomy"
          }
        ]
      },
      "native_chatgpt_projects": {
        "count": None,
        "native_ids_available": False,
        "files_captured": False,
        "instructions_captured": False,
        "status": "UNVERIFIED",
        "evidence_refs": []
      }
    },
    "tasks": {
      "native_chatgpt_scheduled_tasks": {
        "count": None,
        "status": "UNVERIFIED",
        "evidence_refs": []
      },
      "manus_tasks": {
        "count": 564,
        "status": "VERIFIED_COMPLETE",
        "evidence_refs": [
          {
            "path": "08_LOGS/session-ledger/api_task_list_full.json",
            "sha256": "be150cb5dc8f4bbecfd35f78e9cc1cd0e9ee417c566e5d490a8927e8b77222af",
            "source_type": "api_task_list",
            "observed_at": "2026-07-31T00:23:00Z",
            "observation": "Contains 2521 tasks in total, of which 564 were incorrectly attributed to ChatGPT Tasks in previous C4 report",
            "supports": "manus_tasks"
          },
          {
            "path": "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_tasks.json",
            "sha256": "08f8552e5d53b4fdbdc85888f9616ae6e05fcc3709a4e19ae7879e5293c3ed80",
            "source_type": "legacy_surface_report",
            "observed_at": "2026-07-31T05:00:00Z",
            "observation": "Acknowledges 564 tasks belong to Manus, not ChatGPT",
            "supports": "manus_tasks"
          }
        ]
      }
    },
    "custom_instructions": {
      "yos_artifacts": {
        "present": True,
        "files": [
          "01_BACKBONE/GOVERNANCE/Policies/custom_instructions_v2.md"
        ],
        "status": "VERIFIED_COMPLETE",
        "evidence_refs": [
          {
            "path": "01_BACKBONE/GOVERNANCE/Policies/custom_instructions_v2.md",
            "sha256": "unknown",
            "source_type": "yos_policy_file",
            "observed_at": "2026-08-04T00:00:00Z",
            "observation": "File exists with 1961 chars",
            "supports": "yos_artifacts"
          }
        ]
      },
      "native_chatgpt_settings": {
        "captured": False,
        "status": "MISSING",
        "evidence_refs": []
      }
    },
    "file_library": {
      "external_collection_folder": {
        "path": "01_Y_OS_CORE/02_Infrastructure/Chat GPT FILES",
        "observed_file_count": 0,
        "status": "VERIFIED_COMPLETE",
        "evidence_refs": [
          {
            "path": "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_file_library.json",
            "sha256": "3445ea87085949060125ebe5cd61f8e0b089ac1ecdac0cc11b051408498cd64f",
            "source_type": "legacy_surface_report",
            "observed_at": "2026-07-31T05:09:43Z",
            "observation": "Reports 0 files in GDrive folder",
            "supports": "external_collection_folder"
          }
        ]
      },
      "native_chatgpt_files": {
        "conversation_attachments_count": None,
        "project_files_count": None,
        "custom_gpt_files_count": None,
        "export_embedded_files_count": None,
        "status": "UNVERIFIED",
        "evidence_refs": []
      }
    }
  },
  "contradictions_resolved": [
    {
      "contradiction": "Tasks",
      "old_claim_a": "564 ChatGPT Tasks",
      "old_claim_b": "0 ChatGPT tasks, 564 Manus tasks",
      "resolution": "564 = Manus tasks",
      "evidence": "08_LOGS/session-ledger/api_task_list_full.json and c4_surface_tasks.json confirm these are Manus tasks"
    },
    {
      "contradiction": "Projects",
      "old_claim_a": "62 native Projects",
      "old_claim_b": "62 labels derived from enriched-239",
      "resolution": "derived taxonomy only",
      "evidence": "c4_surface_projects.json shows semantic project tags applied to 239 sessions, no native project objects captured"
    },
    {
      "contradiction": "Instructions",
      "old_claim_a": "native instructions missing",
      "old_claim_b": "instructions closed via YOS file",
      "resolution": "native settings unverified",
      "evidence": "custom_instructions_v2.md is a YOS artifact, native settings not independently captured"
    },
    {
      "contradiction": "File Library",
      "old_claim_a": "native library empty",
      "old_claim_b": "external GDrive folder empty",
      "resolution": "native census incomplete",
      "evidence": "Empty external GDrive folder does not prove absence of native attachments in ChatGPT"
    }
  ],
  "open_gaps": [
    "Native ChatGPT projects unverified (IDs, files, instructions)",
    "Native ChatGPT scheduled tasks unverified",
    "Native ChatGPT custom instructions not captured from settings",
    "Native ChatGPT file library attachments and project files not fully censused"
  ],
  "evidence_manifest": [
    "08_LOGS/session-ledger/api_task_list_full.json",
    "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_tasks.json",
    "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_projects.json",
    "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_custom_instructions.json",
    "07_SOURCE_CORPUS/chatgpt/surfaces/c4_surface_file_library.json",
    "01_BACKBONE/GOVERNANCE/Policies/custom_instructions_v2.md"
  ]
}

with open("c4_surfaces_state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Generated c4_surfaces_state.json")
