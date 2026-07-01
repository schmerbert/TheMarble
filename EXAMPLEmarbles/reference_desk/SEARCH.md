# SEARCH.md

Search at the Reference Desk is layered and provenance-aware.

Keyword search alone is not enough. Semantic search alone is not enough.

## Search modes

Catalog search:
  Filter by matter, type, source system, date, author, jurisdiction, court, docket, privilege, confidentiality, authority label, and verification status.

Text search:
  Exact phrases, names, dates, citations, defined terms, exhibit numbers, statute sections, docket entries.

Semantic search:
  Conceptual similarity. Returns leads, not Ground.

Citation search:
  Find a citation and all records that cite, quote, summarize, rely on, question, or draft from it.

Fact search:
  Find support for a proposition and return source trails: client says, document shows, pleading alleges, court found, model inferred.

Authority search:
  Find law by jurisdiction, binding force, court level, date, treatment, currentness, and issue.

Risk search:
  Find warnings: privilege, confidentiality, missing source, stale law, deadline uncertainty, wrong matter, failed Stamp.

## Search result packet

```text
Matter:
Query:
Search mode:
Result:
Why surfaced:
Source:
Authority label:
Verification:
Use limit:
Next check:
```

For fast surfacing, use the Quick Search Return in `DESK_SLIPS.md`.

## Surfacing order

Return results in this order unless the user asks for a narrower mode:

1. Warnings affecting safety, confidentiality, privilege, deadlines, matter isolation, vault silence, or source integrity.
2. Ground directly tied to the active matter and query.
3. Receipts or Vault Door packets relevant to the query.
4. Wild leads with close source proximity.
5. Drafts currently under review.
6. Older Pressure only when requested or clearly relevant.

Search quality is judged by fit and labeling, not by volume.

## Source checks

Record verification attempts in `SOURCE_CHECKS.md`.

A failed public lookup is Pressure or Warning, not Ground. It means the search did not find a match through that method. It does not prove the source does not exist.

## Search law

Search may surface from the Wild Stacks, but only Stamp can make a result authority.
