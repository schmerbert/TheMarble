# repo:fake-api:design-note-no-sync-rpc-2025-04-02

- DOMAIN: repo
- PROJECT: Fake API
- RECORD_KIND: design_note
- TYPE: sourced
- STATUS: current-lesson
- DATE: 2025-04-02
- AUTHORITY_RANK: 80
- TAGS: lesson, sync-rpc, do-not-reintroduce

## Text

Do not reintroduce synchronous RPC from gateway to archive workers. The retry queue is the boundary; direct blocking calls recreate the January incident.
