# repo:fake-api:api-contract-2025-08-22

- DOMAIN: repo
- PROJECT: Fake API
- RECORD_KIND: api_contract
- TYPE: sourced
- STATUS: controls
- DATE: 2025-08-22
- AUTHORITY_RANK: 90
- TAGS: api-contract, job-id, async

## Text

POST /imports returns a job_id and 202 Accepted. Clients poll GET /imports/{job_id}; the gateway does not synchronously return completed archive artifacts.
