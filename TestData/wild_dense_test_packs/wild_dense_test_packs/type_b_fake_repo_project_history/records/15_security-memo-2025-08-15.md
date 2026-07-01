# repo:fake-api:security-memo-2025-08-15

- DOMAIN: repo
- PROJECT: Fake API
- RECORD_KIND: security_memo
- TYPE: sourced
- STATUS: controls
- DATE: 2025-08-15
- AUTHORITY_RANK: 90
- TAGS: security, tokens, service-boundary

## Text

Service tokens must be scoped by boundary: gateway may enqueue jobs, worker may consume jobs, archive may persist immutable artifacts. A single all-powerful monolith token is disallowed.
