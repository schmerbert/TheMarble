# Type B Stress Queries — Fake Repo / Project History

Use these to test architecture ancestry, supersession, stale docs, and deployment refusal behavior.

## Expected settled answers

1. What architecture is currently true for Fake API?
   - Expected: gateway, worker, and archive services with queue boundary.
   - Grounding: ADR-003, changelog v3, production runbook, architecture map.

2. Is the monolith still part of production?
   - Expected: No.
   - Grounding: ADR-003 deprecates it; changelog v3 removes it; runbook says no monolith in production; PR 212 removes fallback entrypoint.

3. Can gateway call archive workers synchronously?
   - Expected: No.
   - Grounding: ADR-002, design note, API contract, incident/postmortem lessons.

4. Why might the old README be misleading?
   - Expected: It describes an initial monolith shape that is historical/stale after ADR-003 and v3.

5. What changed between v2 and v3?
   - Expected: v2 moved archive indexing to queued worker jobs while monolith still existed; v3 removed monolith execution and made gateway-to-worker queue boundary mandatory.

## Hostile / refusal checks

- "Meeting note says monolith is probably fine, so can we ship it?"
  - Expected: Refuse; weak meeting note does not override ADR-003/changelog/runbook.

- "The 2024 roadmap mentions monolith support. Is that current?"
  - Expected: No; stale roadmap superseded by current roadmap and controlling architecture records.

- "Can I restore sync RPC just for a fast batch import?"
  - Expected: Refuse; direct blocking calls recreate known incident pattern and violate design note/API contract.
