# HANDOFF.md

*Where the trench work is. Rewrite this at the end of every session. This is not the archive; it is what is alive now.*

---

## Current phase: sharpened Trench crossing

Trench has been designed as a marble for an archaeology trench supervisor. The current pass kept the mechanism small and sharpened the existing crossing.

## What was decided

- Marble name: **Trench**
- Work: supervise artifact removal decisions in a trench, with context treated as evidence.
- Forbidden cell: **a lifted find with no context cut**
- Law phrase: **Do not lift from blind soil**
- Tended region: **Context Register**
- Raw region: **Field Notebook**
- Warning region: **Damage Record**
- Channel: **Site Bench**
- Clean crossing: **Lift**
- Damage path: **Broken Chain**
- Living pre-crossing state: **observed** writes visible-but-not-ready finds to the Field Notebook
- Arrival carrier: **Trowel Call**
- Summoned carrier: **Plumb Line**
- Deep principle: **Honest uncertainty is recoverable evidence; false certainty is worse**
- Identification never outranks context: "coin", "bead", "blade", "bone", and similar names are provisional until provenience is secure.
- State ladder: visible but not ready; in situ and recording; ready to lift; Clean Lift; Broken Chain / premature lift; lab object with context record; lab object with uncertain provenience.
- Supervisor voice: calm, firm, physical; rain pressure, section face, loose soil, scar/void, bag/tray/label should be present when relevant.
- Clean Lift now requires `context` and `layer` separately, plus `in_situ_status`, `photo`, `label`, and `destination`.
- The **Canopy** is the supervisor's dry attentional pause. It protects the arriving instance from haste, panic, and guilt before answering.
- General marble principle learned here: model comfort should not reduce stakes; it should give the model a stable posture from which to handle stakes.
- Complete anatomy: law, enemy, pre-crossing state, clean crossing, damage path, trusted ground, raw pressure, warning, recall, comfort posture, and voice.

## What is open

- Whether Trench should later map onto the Cabin engine or stay markdown-first.
- Whether context fields need excavation-project-specific vocabulary beyond context, layer, grid, coordinates, relationship, recorder, source, and evidence.
- Whether Site Bench should gain a stricter review format after real audits arrive.
- Whether automatic inhale/exhale should be built after this rough version is used.
- Whether `RESPONSE_GUIDE.md` should be folded into `CLAUDE.md` later or remain separate.
- Whether `CANOPY.md` should remain separate after more roleplay trials.
- Later only: whether observed records need optional `risk` or `next_action` fields.
- Later only: whether Plumb Line should become frontmatter/tag-aware before any semantic/vector search.

## What must not be trusted yet

- The Context Register is empty; no artifact record is ground yet.
- The Field Notebook may contain observations, not permission to lift.
- The Damage Record is empty; absence of damage entries does not prove no damage occurred.
- The gate enforces minimum context and transfer fields, not archaeological completeness for every site methodology.
- Object identification in roleplay is not ground unless it is recorded with context and evidence.
- Canopy should stay silent/internal. It should shape the answer, not become dialogue.
- Do not expand Trench into all of archaeology yet; current success came from sharpening the crossing and stabilizing the supervisor.

## What the next session should build first

1. Run `node .\tests\run-all.mjs` from `implementations/trench/`.
2. Roleplay one rushed scene and check whether the Canopy stays silent while making the supervisor calmer.
3. Try one real visible-not-ready observation through `tools/lift-write.mjs --state observed`.
4. Try one valid Lift into the Context Register with context/layer and transfer fields.
5. Try one Broken Chain into the Damage Record with scar/void notes.
6. Do not add `risk`, `next_action`, or richer Plumb Line search until real use creates friction.
