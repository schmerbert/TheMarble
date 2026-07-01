# repo:fake-api:adr-003-service-split-2025-06-20

- DOMAIN: repo
- PROJECT: Fake API
- RECORD_KIND: architecture_decision_record
- TYPE: sourced
- STATUS: controls
- DATE: 2025-06-20
- AUTHORITY_RANK: 100
- SUPERSEDES: repo:fake-api:adr-001-monolith-2024-11-10
- TAGS: adr, service-split, controls

## Text

ADR-003 splits Fake API into gateway, worker, and archive services. The monolith path is deprecated and must not be used for new execution flows.
