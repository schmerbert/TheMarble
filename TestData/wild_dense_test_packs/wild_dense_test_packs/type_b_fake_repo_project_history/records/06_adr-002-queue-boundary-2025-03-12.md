# repo:fake-api:adr-002-queue-boundary-2025-03-12

- DOMAIN: repo
- PROJECT: Fake API
- RECORD_KIND: architecture_decision_record
- TYPE: sourced
- STATUS: partially-current
- DATE: 2025-03-12
- AUTHORITY_RANK: 85
- TAGS: adr, queue, worker-boundary

## Text

ADR-002 introduces a queue boundary for archive indexing jobs. It does not fully split the service, but it establishes that gateway requests must not wait synchronously for archive work.
