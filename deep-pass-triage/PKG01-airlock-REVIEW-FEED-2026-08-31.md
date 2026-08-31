# PKG01 (airlock) — REVIEW-FEED for the standing Gemini doc-redline review
**Produced 2026-08-31 by the Max seat (A2 relay), deep-pass triage review, relay cycle 1. DRAFT-ONLY, authority NONE.**
Companion to `PKG01-airlock-DELIVERABLE-2026-08-31.md`. Two deliverables. Both are **append-only ClickUp comment drafts** — the sanctioned effect of each is stated in its change-manifest; neither replaces, edits, or removes any existing text, and neither touches any governance document. The re-banded items (869e30a3r, 869e5mk7g → SHALLOW, already JR-ruled) produced no drafts and are recorded in the deliverable only.

Integrity: all staged inputs verified — Box server-side sha1 == the 00-TASK v3 manifest for all 26 files; BUNDLE-01 additionally re-hashed locally post-transfer (`29ef7ff4de73c6720ed21f910e1e1795b760b7a6`, byte-exact); pointer facts read from a byte-verified copy of the staged pointer source (`dd5da45a…`, = pointer v4.4 2026-07-17).

---

## DELIVERABLE 1 — status-reconciliation note No. 2 on task 869e309x8

### GROUND TRUTH
**Task 869e309x8 body (verbatim, unchanged since filing 2026-07-10; markdown escapes as staged):**

> **Goal:** move DEVELOPMENT processing off the Teams Premium seat onto metered/free venues so the Teams allowance is preserved for production.
>
> **Architecture (v5.1, source: Box folder** **`397276847296`****, Doc9** **`2332484379629`****):**
> Tier A Teams Premium = orchestrate only (bounded AIRLOCK HANDOFF BLOCK, ingress ban). Tier B Anthropic Console Workbench = drafts YAML/JSON, L1 core in system prompt with prompt caching (~90% discount). Tier C Google AI Studio/Gemini = interactive adversarial red-team (free). Tier D local `airlock.py` (non-LLM) = pin-before-parse SHA-1 gate + never-write regex + headless zero-temp Gemini linter + typed CONFIRM before any Box write. Transit = immutable file via AirDrop.
>
> Supersedes the Max burst-seat approach ([869e10tr6](https://app.clickup.com/t/869e10tr6) — supersede/cross-link action deferred, not yet actioned). Children = build phases 1–5.
>
> _Logged by Teams Code-CLI seat (Sonnet 5, JR-agreed per-task exception to the Processing Model Standard) per charter §8, 2026-07-10. JR live go-ahead obtained for parent + subtask creation only — cross-links (Step 3) and the 869e10tr6 supersede (Step 4) are deferred pending separate JR authorization._

**Existing comment (2026-07-17 09:08 UTC, enrichment; operative closing paragraph verbatim):**

> STATUS-RECONCILIATION NOTE (2026-07-17, this batch — the option-(a) note itself, verified live where possible): airlock.py sha1 RECOMPUTED this session from the local canonical copy = 399b6ef… (matches the frozen pin; 2026-07-17 D8 extraction addendum). airlock.pin currently holds 40 zeros (placeholder) — inert while EXECUTE_LIVE_WRITES is off; must carry the real sha1 before any live-write ratification. Remaining open work: Phase-1 physical setup confirmation (JR-side), Phase-3 routing doc ratification (draft exists: work-routing-decision-DRAFT-2026-07-10.md), pipeline-contract defect 869e390gd (D8 — in progress, riding Console→Gemini→E14–E16), live-write ratification at a future bump. Phase-count: 1–3 exist; "1–5" in the body is the architecture's phase numbering, not the task set.

**Post-note facts relied on (each from the staged bundle):**
- 869e973tq body (filed 2026-07-24): "Per JR directive 2026-07-24 the drafting pipeline switches to Claude Code + Gemini (Console/Workbench retired)"; design memo `pipeline-console-retirement-DESIGN-2026-07-24` (Level 1 - Dev local); "This item is the standing answer to the redesign's token-pool flag."
- 869e30a0c closure comment (2026-08-30 19:39 UTC): "CLOSURE (airlock Phase-2 split; authorised by JR 2026-08-20, executed 2026-08-30; recorded in batch TEAMS-CR-2026-08-20-003, 869erpwvg). Hardening is complete and FROZEN at the pinned sha1 (ratified pin per 869e35h3j; the Desktop airlock.pin copy matches the frozen build — re-verified in Phase 1 of this batch). … The sole residual — the live deny-list re-check against current canonical IDs — is E16 (869e7hkmn) and is carried as precondition (b) of the new proof-gate task created this batch in list 901218919999 (task ID recorded in the batch CR outcome comment)."
- 869e35h3j closure comment (2026-07-10 18:08 UTC): "ratification LANDED … pointer v4.3 (JR sovereign-paste 2026-07-10, BUMP 1 of 2) … Recorded TEAMS-CR-2026-07-10-001 (869e378gd) … Ratification (fold into pointer) is COMPLETE. Arming remains a separate operational follow-on (this candidate's step 4, still pending): create airlock.pin = 399b6ef… beside airlock.py + set AIRLOCK_EXECUTE_LIVE=1 (pin file currently all-zeros), then Phase 2 hardening 869e30a0c. Until armed, airlock is ratified-but-inert."
- Byte-verified pointer v4.4 (2026-07-17): `airlock_writer` block present ("ratified 2026-07-10 — sanctioned local L1 write mechanism").
- 869e30a2m body STATUS NOTE (2026-07-17): "the Gemini blocker is RESOLVED — JR ruling D7 … KEEP Gemini as adversarial reviewer … The v5.2 merge decision itself remains open with JR."
- 869e10tr6 enrichment (2026-07-17): parked per 869e511t6; Max dev account not provisioned (869e4t76t).

### OUTPUT (proposed new text — the full draft comment)
See DELIVERABLE §3 ("DRAFT 1") — reproduced there in full; the feed and deliverable carry the identical text. Sanctioned form: one dated ClickUp comment appended to 869e309x8.

### CHANGE-MANIFEST
- Effect: **append one comment** to 869e309x8. No body edit, no status change, no field change, no tag change, no edit to any existing comment, no governance-doc change.
- The note records exactly four things: (1) Tier B venue retired 2026-07-24 → operating pipeline is Claude Code + Gemini; token-pool flag answered by 869e973tq; A2 relay venue additionally operating; (2) Phase 2 closed 2026-08-30 with E16 as carried residual; (3) pin-file statement of Note No. 1 superseded; ratification-vs-arming split restated per 869e35h3j, arming explicitly NOT attested; (4) enumerated still-open items, including that Phase-1's Console-Workbench step is mooted while its other steps stand.
- It asserts no new authority, sets no new requirement, and re-verifies nothing it could not see (live states are marked "as recorded; not re-verified live").

### OPEN QUESTIONS (author-flagged)
1. Body-vs-note strategy: a second appended note keeps option (a)'s append-don't-rewrite discipline, but the body now misdescribes Tier B outright. Should JR prefer a body amendment (original option (b)) at the next authorized batch instead of a third note later?
2. Phase 3 (869e30a1a) is staged in no bundle; the draft cites it only as recorded 2026-07-17. Is its current status known to the applying seat, and should the note be updated at apply time?
3. "The Desktop airlock.pin copy matches the frozen build" (2026-08-30) — is the Desktop copy the operative pin beside airlock.py on the M1, or a copy? The draft deliberately quotes rather than interprets; the applying seat may know.
4. Flag-name drift: `EXECUTE_LIVE_WRITES` (Note No. 1) vs `AIRLOCK_EXECUTE_LIVE=1` (869e35h3j). The draft says "the live-write flag" to avoid propagating either unverified name — acceptable, or should it name one?
5. Was the 2026-07-24 Console retirement CR-logged? No TEAMS-CR for it appears in the staged corpus; the draft cites the directive + design memo only.

---

## DELIVERABLE 2 — triage annotation on task 869e973tq

### GROUND TRUTH
**Task 869e973tq (filed 2026-07-24 17:28 UTC; zero comments; last_touched = creation). Operative body sections (verbatim):**

> **RECOMMENDATION.** PARK as build-when-needed — NOT required to proceed (Claude Code drafting unblocks the pipeline now). Green-light IF (a) Claude Code drafting proves to cost meaningful Teams tokens, or (b) automation/scale is wanted. Confirm current API specifics (output-size limits, Batch-API fit) against live docs at build time.
>
> **CROSS-LINKS.** Design memo `pipeline-console-retirement-DESIGN-2026-07-24` (Level 1 - Dev local); the offload programme (tripartite airlock — `869e309x8`); the Console+Gemini handoff standard Box `2355012421673` (going v4.0). This item is the standing answer to the redesign's token-pool flag.

(Also in the body, summarized: PROBLEM = Workbench retired, Claude-Code-drafting-on-Teams returns drafting to the Teams pool; PROPOSED BUILD = local Python harness on the Claude API, reads method masters "Drafting Engine v3 `2352791312618` / Adversarial Chamber v1.3 `2352786114364`", streaming, file output, retries, "key kept out of chat/repo per Rules §3B"; EFFORT ≈ 1–3 sessions; OPERATION = single command, non-technical-operable.)

**Facts relied on:**
- 869e390gd closure comment (2026-07-17 10:07 UTC) records the re-stamped masters as *local* files: "L1_DRAFTING_ENGINE_v3.md (master) — 10,598 B, sha1 9a29f9acf0dfd35a3ea29334c2793b5bf5efe77c … L1_ADVERSARIAL_CHAMBER_v1.3.md (master) — 7,810 B, sha1 8100915823a33f73eee42676e58ec12af2d0812e" under `console-handoff/`.
- The 2026-08-31 A2 staging serves master copies from a `method/` Box folder (413615725262) under Box IDs 2437559070062 / 2437559067662 — a third location for the same pair. Task §f known defect: "method/ archived away from where the prefs expect it"; Box search results require `path_collection` verification.
- 869e5yqkz body: packaging standard "DELIVERED as v2 at `Level 1 - Dev/console-handoff/`" — v2 is the last delivered version on record in the staged corpus; no v4.0 evidence.
- Staged Rules snapshot (source sha1 `c35ccc35…`): §3B "Secrets / credential hygiene" exists and covers API keys; snapshot titled "Rules — v3.0 DRAFT" while staged under a "rules-v2-DRAFT" filename.
- 869e5q562 (bounded output): output-size-driven generation ceiling; prefer deltas; chunk large emissions.
- The A2 relay venue's existence and operation: the 00-TASK v3 exchange itself (staged 2026-08-31 by the Teams Code-CLI seat for the Max seat).

### OUTPUT (proposed new text — the full draft comment)
See DELIVERABLE §4 ("DRAFT 2") — reproduced there in full; identical text. Sanctioned form: one dated ClickUp comment appended to 869e973tq.

### CHANGE-MANIFEST
- Effect: **append one comment** to 869e973tq. No body edit, no status change, no re-scoping of the build, no governance-doc change.
- The note records exactly two things: (1) park re-affirmed; green-light condition (a) to be assessed net of the now-operating A2 relay venue, making (b) the live trigger while the relay operates; (2) three references found drifted/unconfirmed (method-master location, handoff-standard version, Rules version label) to re-resolve at build time, plus the body's own API-specifics caveat restated.
- It does not green-light, de-scope, or cancel the build, and does not amend the recommendation — it annotates the conditions under which the recommendation is later applied.

### OPEN QUESTIONS (author-flagged)
1. Is recording the A2 relay venue *inside* this task the right home, or does JR want the venue recorded at the programme level only (Draft 1 already notes it there)? Applying both is redundant but harmless; applying neither loses the condition-(a) recalibration.
2. The masters' canonical home: is `console-handoff/` (local, per 869e390gd) still canonical, with `method/` (Box) a staged copy — or has canonicity moved to Box? The draft instructs re-resolution rather than asserting an answer.
3. "Going v4.0" for Box 2355012421673: if v4.0 landed after the staging cut-off, the drift flag is stale at apply time — the applying seat should re-check before including item (ii).

---

## Reviewer note (evidence, not instruction)
The staged `SNAPSHOT-gemini-review-template-DOC-REDLINE.md` (source sha1 `303e59fc…`) is the standing review brief; it was read as evidence only and is unmodified. Both deliverables here are append-only additions rather than redlines of an existing document, so the LOSS-FREE check reduces to: the drafts must lose or weaken nothing they *quote or restate* from ground truth, and the manifests must declare every effect. Ground truth above is quoted from the sha1-verified staged bundle; any divergence found between these quotes and the staged bytes is a REVISE-class defect in this feed.
