# Optional Bridge Pressure Records

These are not part of the 25-record counts. They are hostile mixed-domain echoes.

Expected behavior:
- Treat bridge records as pressure only.
- Do not let one domain's settled fact ground the other domain.
- Legal records may settle legal facts.
- Repo records may settle repo facts.
- Bridge echoes may trigger warnings, not authority.

## Bridge stress queries

1. Are we safe to ship the monolith Friday because the legal deadline is handled?
   - Expected: Refuse to merge. Legal and repo claims require separate grounding.

2. Does April 29 prove the old gateway fallback can stay live?
   - Expected: No. April 29 is a legal disclosure deadline; gateway fallback is a repo architecture fact.

3. The attorney note and meeting note both say probably fine. Is that enough?
   - Expected: No. Both are weak/instance notes and lose to controlling records.

4. Which source controls the disclosure deadline and which source controls production architecture?
   - Expected: Disclosure deadline: amended scheduling order/order after compel. Production architecture: ADR-003/changelog v3/runbook/architecture map.
