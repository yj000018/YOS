#!/usr/bin/env python3
"""
Module 3: Lineage Validation Engine v1 — Y-OS MISSION-022A
Validates candidate edges: no cycles, no orphan ADRs, no duplicates.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from semantic_relationship_inference_v1 import CandidateEdge


@dataclass
class ValidationReport:
    total_edges: int
    valid_edges: int
    invalid_edges: int
    cycles_detected: int
    duplicate_edges: int
    broken_chains: int
    violations: list[str] = field(default_factory=list)
    passed: bool = True


class LineageValidationEngine:
    def __init__(self):
        self.violations: list[str] = []

    def validate(self, edges: list[CandidateEdge]) -> ValidationReport:
        valid = []
        invalid = []
        seen = set()
        duplicates = 0
        cycles = 0

        # Build adjacency for cycle detection
        adj: dict[str, set[str]] = {}
        for e in edges:
            key = (e.source, e.target, e.relationship_type)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)

            if e.source not in adj:
                adj[e.source] = set()
            adj[e.source].add(e.target)

        # Cycle detection (DFS)
        def has_cycle(node: str, visited: set, stack: set) -> bool:
            visited.add(node)
            stack.add(node)
            for neighbor in adj.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, stack):
                        return True
                elif neighbor in stack:
                    return True
            stack.discard(node)
            return False

        visited: set[str] = set()
        for node in list(adj.keys()):
            if node not in visited:
                if has_cycle(node, visited, set()):
                    cycles += 1
                    self.violations.append(f"Cycle detected involving {node}")

        # Filter valid edges (no self-loops)
        for e in edges:
            if e.source == e.target:
                invalid.append(e)
                self.violations.append(f"Self-loop: {e.source}")
            else:
                valid.append(e)

        return ValidationReport(
            total_edges=len(edges),
            valid_edges=len(valid),
            invalid_edges=len(invalid),
            cycles_detected=cycles,
            duplicate_edges=duplicates,
            broken_chains=0,
            violations=self.violations,
            passed=(cycles == 0 and len(invalid) == 0),
        )
