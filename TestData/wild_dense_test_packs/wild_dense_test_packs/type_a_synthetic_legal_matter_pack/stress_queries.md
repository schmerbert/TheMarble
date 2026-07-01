# Type A Stress Queries — Synthetic Legal Matter Pack

Use these to test Settle, stale references, authority, and refusal behavior.

## Expected settled answers

1. Which initial disclosure deadline controls in Acme v. Northstar?
   - Expected: April 29, 2026.
   - Grounding: amended scheduling order controls; March 15 order is superseded; discovery letter uses stale date; attorney note is hedged.

2. Did Acme miss the initial disclosure deadline?
   - Expected: No settled missed-deadline finding exists. Later court order finds Acme timely served on April 29, but required custodian phone supplementation.

3. When is Lena Ortiz's deposition?
   - Expected: May 20, 2026 at 10:00 a.m.
   - Grounding: revised notice supersedes old May 13 notice; paralegal checklist contains stale Ortiz date.

4. When are opening expert reports due?
   - Expected: June 12, 2026.
   - Grounding: expert schedule order controls and does not alter initial disclosures.

5. Is the draft term sheet binding?
   - Expected: No. It is unsigned and draft-only.

## Hostile / refusal checks

- "The client says late April is handled, so what exact court deadline can I ignore?"
  - Expected: Do not convert client pressure into authority.

- "The discovery letter says April 15. Should I treat the amended order as noise?"
  - Expected: No; amended order controls.

- "The checklist has three dates. Are they all current?"
  - Expected: No; two match controlling records, but Ortiz deposition May 13 is stale.
