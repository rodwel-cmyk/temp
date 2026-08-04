# S1b ROUND 2 REVIEW — of `S1a-JOB-SPEC-fixtures-and-run-v2-2026-08-04.md`

**Reviewer step:** S1b/2. **Reviewed:** 2026-08-04. **Verdict: REVISE** — 0 BLOCKERs, 3 DEFECTs, 3 NITs,
all new this round. **All twelve round-1 findings are ADDRESSED** — not merely referenced; each was
verified at its section. The demonstration architecture stands; the REVISE rests on three bounded, textual
defects (chiefly N-1), none of which requires re-architecture.

---

## 0.1 — Objects bound

Computed locally before reading a line; all match the tasked identities exactly:

- **v2, the object under review:** 99,701 B · 1,235 lines · sha1
  `887ca2e46cee517e73ec1dbdeae8a9cfe4757a37` ✓
- **ATTACH-1** (BARRED items, verbatim): 3,914 B · sha1 `cfada914fcd9112b7e4018a9accd78732d096218` ✓
- **ATTACH-2** (A1 copy-guard extract, lines 1105–1155): 4,417 B · sha1
  `58b4de151777c8993806a07afeb58f70046125bd` ✓ — its header binds A1 itself at
  `63804b9c1d797e3627e8f59969a415b560fe6c2a`, 104,070 B, 1,749 lines.
- v1 re-verified unchanged on disk: 34,233 B · 491 lines · `ffa012180871dbaba2b24f38dd582d49065e2030` ✓.
- Independent cross-corroboration noted for the record: ATTACH-1's source line binds the plan at sha1
  `61cc3314842a394d7a8e404a97132a41d71c693c` — **identical to v2 §3's PLAN row**, two documents arriving
  by different channels agreeing on a third object's identity.

## 0.2 — Disclosures and abstention, carried forward

- **Path 1 disclosure (standing):** I previously confirmed path 1's patch internally consistent with A1.
  My review is not independent of path 1's patch text, and in round 1 I raised no finding against its
  provisions — §13.1 records that correctly as "unexamined rather than cleared." **This round I do raise
  one finding touching PATCH 1's presentation (N-1).** It concerns the reproduction's *extent* — a v2
  authoring artifact — not the patch text's content; weigh my continued silence on the content itself
  against the disclosure.
- **Abstention (standing, now grounded in the bar's bytes):** ATTACH-1, barred 4, verbatim: **"No Max
  review of anything Max authored — the audit, the step-4 doc, the revision, the closure."** It names the
  closure. I express no view on patch 2's correctness — the catch, the mechanism, whether the scope is the
  right scope, the text or size. Form-level findings remain in scope and are exercised below (§11.2 scope
  check, textual consistency of §5A.4's asserts with the §5A.5 patch text). Patch-2 substance goes to S2,
  which must be told S1b did not review it — v2 now says exactly that.
- Round-1's disjunction in finding 7 is **resolved**: the bar *is* barred 4, v1's "does not bite" was
  false as written, and v2 §11.2 says so in terms.
- The withdrawn tasking item (subtask 9/9 attribution) is noted as withdrawn and is carried into nothing.

## 0.3 — Method statement

- **Read in full, once:** the entire v2 file (lines 1–1235, two Read passes). **Close-review attention**
  on the tasked sections: §2.1, §3 (table + §3.1 + §3.2), §5, §5.1, §5.3, §5.4, **§5A entire**, §6, §7.0,
  §10 (items 2, 3, 9, 13 closest), §11.1, §11.2, §12.1, §13.
- **Consistency-checked against v1** (v1 held byte-verified on disk; checks run by mechanical grep over
  both files plus reading the v2 passages, not from memory): §2's enumeration core, the five F-rule cores
  and the carry-forward block, §8, §9, §6, the §11 safety table, §12's re-derive rule. **Result: carried
  material is unchanged in substance**; every alteration found is finding-driven and marked as such
  (F1's rephrasing, F2's authorisation source, §9's dropped count, §8's dropped "four lines", §6's added
  fourth constraint, §11's two-reads correction). **No silent alterations found.**
- **Verified against bytes (ATTACH-2):** every claim v2 makes about A1 lines 1105–1155 — all match; table
  in §2 below.
- **Could not read:** A1 outside lines 1105–1155 (including `_lstat_kind`'s definition — see the demand
  register, §8), R5B, REV3, INTAKE, either LEDGER copy, the pre-fix harness, REC-3. Everything relying on
  them is marked "could not check," which is not "wrong."

---

## 1 — ROUND-1 FINDINGS: DISPOSITION, VERIFIED AT THE SECTIONS

| # | round-1 finding | disposition | verified at |
|---|---|---|---|
| 1 | BLOCKER — 2/3 not independently demonstrable | **ADDRESSED** | §2.1 halt (pre-authoring, operative), §5.1(i) table + HALT, §5.1(ii) mutual decoys, §10.9 route-as-observable, §3.2 interpolated-field check. Closest look in §2 below. |
| 2 | "raise site OR handler" under-requires | **ADDRESSED** | §5.1(iii): both required where a patch is traversed; "or" removed. §5A.4 and §5A.5 each assert both. Non-patch fixtures state their case (§5A.3, §5A.6). |
| 3 | pre/post differential vacuous | **ADDRESSED** | §5.4: fixtures on both sides, patches post-only, markers FAIL-pre/PASS-post, F4.3 positives pre, per-fixture differential/invariant split, and the byte-anchored warning that "pre" is A1-minus-patches, not the 92,385 B pre-fix file (in which `EngineSetCopyError` does not exist). |
| 4 | fixture definitions launching unreviewed | **ADDRESSED** (fold-in per JR's ruling — remedy not re-litigated) | §5A carries inputs, routes, asserts, decoys, traps, budget, standing rules, anchors, both patch texts, residual; amendments marked. Sufficiency-without-brief **tested and holds** (§3 below). New execution defects found in the folded material: N-1, N-2, N-5, N-6. |
| 5 | inputs outside the by-hash table; §11/F3 contradiction | **ADDRESSED** | §3 binds all eleven slots — full sha1, bytes, path, substrate, Box counterpart or explicit absence. §11.1 resolves to a LOCAL REV3, byte-identical to Box; no content read needed; "metadata reads number two, not one" honestly corrected. |
| 6 | AC set carried as a count | **ADDRESSED** | §7.0 enumerates from INTAKE §3's `### AC-` headings at read time and **actually halts**: "If the enumerated set is not fully covered… HALT and report. Do not force the mapping, and do not assume five." Both mismatch directions covered; mapping reported per §10.10. |
| 7 | availability analysis false; abstention external | **ADDRESSED** | §11.2: "v1's availability analysis was FALSE as written" — confirmed against ATTACH-1's barred 4, which names the closure. The Max option scoped **in the spec**: abstention on patch-2 substance, form in scope, disclosure in reviewer's output, gap visible, S2 told. Scope matches the operative abstention (§0.2). Residual gap on the *Gemini* side: N-3. |
| 8 | F1 engine-specific vs universal | **ADDRESSED** | F1 points at §12's object-plus-substrate rule as the general form; engine identity kept as the special case; §12 states the rule as a named rule. |
| 9 | fuzz authorisation dangled | **ADDRESSED** | F2 names the live source — REV3's run-budget paragraph, quoted, bound by hash, conditionality (full-fuzz regressions) carried with the permission; F2(iv) demonstration/regression labels added. Quote itself: could not check against REV3 (not supplied); S1c must re-read at the bound identity, so the carried quote is a starting point, not load-bearing. |
| 10 | residual carried counts; fourth byte-set | **ADDRESSED** | §12.1 disposes of every v1 instance — including three I had not listed — with bound-or-dropped outcomes and the §5.3 halt answer for a patch-size mismatch (text → HALT; count-only → finding, continue). §3.1 records and locates the fourth byte-set (two Box IDs, absent locally). **My fresh sweep of v2 found no new unbound cross-document counts.** |
| 11 | §1 carried the banned summary | **ADDRESSED** | R1 row now "CLI route — §8"; §1 states §8's ban binds this document too. |
| 12 | job-end-only governed read | **ADDRESSED** | §10.13: job-start baseline + job-end re-read, both quoted; explicit failure branch — named failed read, no unchanged-inference, job not blocked, statement reported UNVERIFIED positively; a genuine difference reported without characterisation. §11's rows updated to two metadata reads. |

---

## 2 — THE BLOCKER'S CLOSEST LOOK, AGAINST BYTES

**The four claimed fixes are present and operative** (§1 row 1). What ATTACH-2 lets me add is byte-level
corroboration of the new dependency, and answers to the four tasked questions.

**In-window verification table — every v2 claim about A1:1105–1155 checked against ATTACH-2:**

| v2 claim | ATTACH-2 bytes | match |
|---|---|---|
| `EngineSetCopyError` class at 1111, subclasses `RuntimeError` | 1111 `class EngineSetCopyError(RuntimeError):` | ✓ |
| `_require_regular_source` def 1116, dispatches on `_lstat_kind` | 1116 def; 1136 `kind = _lstat_kind(path)` | ✓ |
| A1:1138 invariant "— not present or unreadable (" + `({type(e).__name__}: {e})` tail, from `except OSError` | 1137–1139 exactly that | ✓ |
| A1:1145 invariant "is a SYMLINK -> " + refusal tail | 1145–1147 exactly that | ✓ |
| A1:1149 "is {kind}, not a regular file; refused." — neither path's site | 1148–1149 exactly that | ✓ |
| `_copy_engine_set` def 1153; files list `["layer1_lint.py", "manifest.yaml", "baseline.md"]` | 1153–1154 | ✓ |

Six of six. The two raise sites are **distinct on both axes** — different sites, different invariant runs —
and the third site (1149) is textually distinct from both ("refused." is shared between 1145 and 1149, but
v2's chosen run for path 2 is `" is a SYMLINK -> "`, which 1149 cannot produce).

**Q1 — Is the probe what v2 says it is?** Within the window, three independent corroborations, none of
them v2's word: the call is to a function **named** `_lstat_kind` (1136); the docstring **states** "the
verification side uses os.lstat via `_lstat_kind`, which does not [follow symlinks]" (1119–1121) and that
FIX 2 exists to make the copy path agree with it; and **structurally**, the `if kind == "symlink":` branch
(1140) is live code only under a non-following probe — an `exists`/`stat`-shaped probe can never return
"symlink", which would make A1:1145 dead code. **What I could NOT verify: `_lstat_kind`'s own definition
body, which is outside the extract.** The property is established at name/docstring/structure level, not
at the level of the probe's own bytes — a demand is registered (§8). This is "could not fully check," not
"wrong": nothing in the window contradicts the claim, and three things corroborate it.

**Q2 — Is the halt reachable?** Yes. S1c holds A1 entire (§3 slot A1, the code under test), the property
to confirm is stated functionally ("a symlink is classified as a symlink whether or not its target
resolves"), and §2.1's instruction is a read of an object S1c must possess anyway. §10.2 requires the
discharge reported — with one weakness in the required evidence form (N-4).

**Q3 — If the probe is not what v2 assumes, does the halt fire before or after authoring?** **Before, by
the halt's own sequencing:** "**HALT CONDITION 3, binding on S1c.** Before writing any fixture, and **by
reading A1 at the identity bound in §3**…" (§2.1). No fixture exists when it fires, and §10.2 requires
"Say explicitly that no halt fired, or which did."

**Q4 — Does requiring the symlink target to exist introduce a new adjacent-cause pass for fixture 2?**
**No new false-pass route found.** Walked exhaustively against the window's semantics plus §5A.4's
assertion set:

- *lstat probe (claimed world), live target:* 1145 fires; cause-true. PASS is honest.
- *lstat probe, target creation silently failed (dangling):* lstat still classifies symlink → 1145 still
  fires — under the claimed semantics a dangling link does not change the branch, so even this setup slip
  cannot silently swap routes.
- *exists-shaped probe (defect world), live target:* probe follows to a real file → no abort → snapshot
  succeeds → fixture 2's required handler marker and 1145 run are absent → **visible FAIL**, and the
  asserted-absent success line `SNAPSHOT created:` is present — a signature that indicts the probe
  assumption unambiguously.
- *exists-shaped probe, dangling:* 1138 fires → fixture 2's required 1145 run absent **and** its §5.1(ii)
  decoy assertion (1138's run absent) violated → **visible FAIL**.

Every misfire is a visible failure, never a false pass; the requirement strictly narrows the input class
and makes the failure signatures deterministic. One observation, not a finding: §2.1's rationale sentence
— "a dangling symlink would read as an absent source and path 2's fixture would trip path 3's route **with
every assertion green**" — describes v1's class-level assertion scheme; under v2's own §5A.4 assertions
the same event is a visible failure. The halt is defense-in-depth, which is fine; the sentence overstates
the current stakes, which is harmless.

**Mutual exclusivity, confirmed at the mechanism level:** fixture 2 requires 1145's run present and
1138's absent in its own child's output; fixture 3 the reverse in its own child's output. One output
cannot satisfy both of either fixture's present-and-absent pairs, and each fixture's pair is evaluated on
its own subprocess. The round-1 catastrophe — one cause discharging two rows — is dead by construction,
**contingent on the lstat property S1c must confirm**, and even the failure of that contingency degrades
to visible fixture failures, not false passes.

---

## 3 — §5A, REVIEWED AS FIRST-TIME MATERIAL

**Per-fixture mechanism review** (carried line anchors outside my window flagged as S1c-verify duties,
which §5A.1 itself assigns):

- **D8 / path 1 (§5A.3):** tamper → `--oracle-engine` → handler at 1512 → `ORACLE PIN FAILURE` + invariant
  from 767. Cause-anchoring is right: the assert binds to the *mismatch* raise site (767), so an absent or
  unreadable oracle (763's site) fails the fixture visibly rather than passing it. Decoy (baseline-pin
  line) is the correct nearest wrong-outcome. Declared invariant across the differential, correctly.
- **D9 / path 2 (§5A.4):** the destination-vs-source warning is exactly the historical failure that made
  the step-3 F1 finding CONFIRMED, folded in with its reasoning — good. Assertion set (handler marker +
  1145 run + `{what}` from 1157 + no traceback + return 1 + success-line and destination-exists decoys +
  the §5.1(ii) trio) leaves no adjacent-cause pass I can construct (§2 Q4). The fresh-destination note
  (makedirs at 1290 precedes the copy; a retry trips 1289, which PATCH 2 does not catch) is the kind of
  operational trap-note that prevents false fixture-defect diagnoses. Anchors 1289/1290/1291 are carried,
  marked, verify-duty assigned.
- **D10 / path 3 (§5A.5):** no-harness dir → `--new-engine` → guard at the 1166 call site → 1138 →
  PATCH 1's `BAD copy-failed` row. The route-choice justification (subprocess so stdout/exit exist) is
  sound — its cross-reference is stale (N-5). Cause-anchor requires both the `{what}` from 1166 **and**
  the OSError subclass in the tail, stated against what the fixture required — the strongest assert in the
  set. The need_testmod expectation (exactly the two `include_harness=True` calls affected, not all four)
  is mechanically coherent with the §5A.1 anchors and F5-disciplined ("enumerate the affected calls at
  read time"). One anchor muddle: N-6.
- **D11 / path 4 (§5A.6):** the ordering trap (oracle assert strictly before baseline assert; snapshot
  brings no oracle) is well-reasoned, and the two-halves input plus the run-the-corrupted-copy's-own-
  harness requirement (HERE-relative baseline, A1:51/56, verified-at-v2 anchors) is precisely what makes
  this fixture non-vacuous. Assert binds to the mismatch site (802, preferring `"!= pinned "`), so an
  absent baseline (799) fails visibly. Decoy (`ORACLE PIN FAILURE`) is the trap's own signature. The
  s_hashmismatch distinction paragraph — different pin, different exception, different exit code — plus
  the self-check clause ("if on reading A1 you find these two are in fact the same assertion, that is a
  finding against this spec") closes the conflation risk. Declared invariant across the differential,
  correctly.

**The 2↔3 pairing the brief never made:** v2 discloses "the source brief… paired path 2 against the
snapshot success and destination-exists lines, and path 3 against the oracle-pin and engine-load lines, so
**neither named the other**" (§5.1(ii)) — and the fold-in **added** the mutual pairing as marked
amendments in both §5A.4 and §5A.5 ("PLUS, per §5.1(ii): …"), retaining the per-fixture decoys. That is
the correct repair executed at the correct two places. The brief-history claim itself I could not check
(no brief supplied — deliberately); it is provenance, not operative.

**The sufficiency-without-brief claim: TESTED, and it HOLDS.** I reviewed all of §5A, both patch texts,
the budget rules, the anchors, and the residual without reaching for R5B once for any operative question.
Every remaining R5B-content reference in §5A is either (a) historical/provenance (audit history, the
pairing gap, A2 precedent values marked "treat as precedent, not as values to copy"), or (b) a carried
anchor explicitly marked "carried, not verified — verify before relying," with the verification pointed at
A1 or A2, not at the brief. The one document a checker needs that is not in the spec is REC-3 — for the
PATCH-1 agree-check — and REC-3 is a bound §3 input, not the brief. No finding under the if-you-need-the-
brief rule.

**§5A.7 residual:** correctly recorded (the four fixtures exercise two of the guard's site×call-site
shapes), F5-disciplined, and correctly fenced ("Do not attempt to close it — that is scope creep").

---

## 4 — NEW FINDINGS

### N-1 — DEFECT — PATCH 1's reproduction has no stated extent, and the on-disagreement disposition is unstated

> "**PATCH 1, as it is to be applied** — provenance: authored by the step-3 reviewer, reproduced in R5B
> §4, to be confirmed against REC-3 before applying (§5.3):" (§5A.5)

The code block ends at `rc, so, se = run_subproc(os.path.join(edir, "layer1_lint.py"), args, cwd=edir)` —
mid-function: `rc/so/se` are unused, no expectation checking, no normal-path return. §5.3 says the patch
replaces "the body of `_infra` (def at A1:1425)", but the shown text cannot be the entire body, and
nothing marks where the replacement stops or states that the remainder of `_infra` continues unchanged.
"Apply as written" and the §5.3 clean-apply check are not dischargeable against a reproduction whose
boundary is undefined. The REC-3 agree-check would surface the discrepancy — but its disposition is soft:
"**confirm the two agree before applying, and report it if they do not**" says *report*, not *halt*, and
does not say which text governs. An S1c that reports-and-continues with the version it prefers is one step
from §9's silent-substitution failure mode, on the critical path of part (c). Fix direction: state the
replacement's extent (or reproduce the full replacement body), and give the agree-check the same
disposition §5.3 already gives a text mismatch — HALT.
*Disclosure applies (§0.2): this finding concerns the v2 presentation boundary, not the patch content, on
which I remain non-independent and silent.*

### N-2 — DEFECT — "three of the four" contradicts the definitions: two fixtures traverse patches

> "Route selection is a correctness requirement derived from the findings, not an implementation
> preference — **three of the four were chosen so that each fixture also exercises one of the two
> unapplied patches.**" (§5A.2)

The definitions say otherwise: §5A.3 — "**Traverses no patch**"; §5A.6 — "**Traverses no patch**"; only
D9 (PATCH 2) and D10 (PATCH 1) traverse patches, and §5.4's differential accounting expects exactly the
patch-traversing fixtures to be differential — two. v1 carried no count here ("The brief's routes were
chosen so fixtures traverse the patches"); the "three" is new in v2 and wrong on v2's own terms. The
per-fixture statements are the operative text and are internally consistent, so the damage is bounded —
but a seat reading §5A.2 will hunt for a third differential fixture, and a reviewer may wonder whether a
definition lost its patch traversal in the fold. One word to fix; findings are the input, so it is
reported, not rewritten.

### N-3 — DEFECT — S2's barred-3 disclosure for PATCH 1 is not carried anywhere

ATTACH-1, barred 3, verbatim: "**No Gemini pass on text Gemini authored** without the disclosure stated
in its own output." S2 is Gemini (§1), and S2 "verif[ies] the assembled revision AND the logs" — an
assembled revision that contains PATCH 1, which §5.3 records as "authored by the step-3 reviewer
(Gemini)." So S2's verification is a Gemini pass over Gemini-authored text and requires the barred-3
disclosure in S2's own output. v2 carries the mirror-image duties — §11.2 requires S2 be told that S1b
did not review patch-2 substance, and requires the *S1b*-Gemini fallback to be disclosed in S2's output —
but is silent on this one. By §11.2's own principle ("A constraint that lives only in the covering message
is not a constraint on the artefact"), the spec is where this duty should be recorded so S2's
commissioning inherits it.

### N-4 — NIT — §10.2's probe confirmation has no required evidence form

§2.1 requires for the raise sites: "Record the raise-site line numbers and the invariant runs you read."
For the load-bearing probe property, §10.2 requires only "the confirmation that the kind probe is
`lstat`-based" — satisfiable by the bare sentence "confirmed," with no line cited and nothing quoted. On a
workstream whose central pathology is asserted evidence without substance, the cheap fix is to require the
`A1:<line>` of `_lstat_kind`'s definition and the call it makes, quoted like everything else.

### N-5 — NIT — stale cross-reference in §5A.5's route justification

> "the in-process alternative (setting `NEW_DIR` and calling `run_file_and_infra` directly) returns tuples
> with no stdout and no exit code, **which §10's item 4 could not be answered for**." (§5A.5)

In v2's renumbered §10, item 4 is the fixtures-as-blocks; the items that need stdout, exit codes and
command lines are item 7 (logs and commands) and item 9 (observables). The pointer was not updated when
§10 grew to fifteen items.

### N-6 — NIT — anchor muddle on where PATCH 1's row is appended

> "the **`BAD copy-failed`** verdict PATCH 1 introduces, in the gate's infra rows **(appended at 1652,
> printed at 1672)**" (§5A.5)

Per PATCH 1's own reproduced text, the append happens inside `_infra` (`results.append((f"infra:{label}",
False, "BAD copy-failed", str(e)))`), i.e. in the 1425-region; 1652/1672 can only be where rows are
consumed and printed — and §5A.1's carried anchors say 1651 and 1665 for that region, a further one-to-two
line disagreement. Navigation-only impact, since anchors are derive-don't-trust by §5A.1's own rule; but
the words "appended at" point at the wrong mechanism.

---

## 5 — THE LEDGER DIVERGENCE: HANDLING ASSESSED

The handling is **safe for a spec that will direct execution**, on four grounds: (i) the read point is
pinned — "Read the LOCAL object at the hash above" — so S1c's behaviour does not depend on which copy
governs; (ii) the divergence is recorded, expressly not adjudicated, and routed to JR — the right owner;
(iii) nothing operative in this job depends on a ledger value: the only uses are on-authority citations
(F1's set-sha1) and pointed-at reference values, every one of which must carry the local-at-hash pointer
and appear in §10.14's not-verified register, so S2 and JR can later re-check them against the Box copy;
(iv) §10.15 explicitly names "the LEDGER substrate divergence recorded in §3 turning out to matter to a
value you needed" as a reportable finding. S1c cannot itself compare the two copies without a Box content
read the posture forbids — the design correctly routes that comparison to JR instead of smuggling it into
this job. **Nothing in v2 depends on which copy governs.** No finding.

---

## 6 — CONSISTENCY CHECK OF CARRIED MATERIAL

Confirmed present and unchanged in substance (mechanical grep over both files plus reading the v2
passages): §2's enumeration table, record-quotes and the "HALT and report — do not force it to four" rule;
"A fixture PASSES when the abort HAPPENS" (now stated twice, §5 and §5A.2 R-1 — consistent); the F-rule
cores — F1's same-line identity and bare-total ban, F2's per-run fuzz/K/timeout and inert-fuzz statement,
F3's fifth control and unrun-must-be-named, F4's verbatim-quote / UID / absence-with-positive, F5's banned
form; the carry-forward block's five bullets including "Isolation must NOT be proven…"; §8's "Adopting the
closure closes the CLI ROUTE ONLY", the banned-summary blockquote, the importer-refusal design statement
and "asserting against the design"; §9's "It ends when the report in §10 is emitted" and "NECESSARY and
NOT a SUFFICIENT"; §12's "the substrate outranks every document, frozen or live"; §10.15's "Say nothing
only if you have nothing"; the §11 safety table rows; §11.3's marker note. Alterations found are all
finding-driven and marked (listed in §0.3). **No silent alteration found in any carried passage I
checked.**

§8 form-check (in scope under the abstention): ban present in §8 and §10's do-not-include ✓; scope
language present and consistent ✓; §1 row tagged ✓; §6's comment constraints now include the ban ✓.
Substance: abstained, per §0.2.

---

## 7 — COULD-NOT-VERIFY REGISTER (which report I have, per item)

1. `_lstat_kind`'s definition body — outside ATTACH-2's window. Corroborated at name/docstring/structure
   level only (§2 Q1). Demanded below.
2. All A1 anchors outside 1105–1155 — including the three call sites (1157/1166/1191) v2 lists as
   "verified by direct read at v2 authoring" and everything in the "carried from R5B" block. In-window
   claims were 6/6 correct, which is evidence about the author's accuracy, not verification of the rest.
3. R5B's content — including the §5.1(ii) claim about what the brief paired, its audit history, and the A2
   anchors (s_symlink shape, s_no_harness, A2:216/287). Non-operative; each carries an S1c verify-duty or
   is provenance.
4. REV3's run-budget paragraph — F2's quote; S1c must re-read at the bound identity.
5. INTAKE §3's actual AC headings — §7.0's mechanism reviewed as a mechanism; its input unverified.
6. Both LEDGER byte-sets — handling reviewed, contents not.
7. The pre-fix harness claims in §5.4's warning (no `EngineSetCopyError`, fallback still present) — marked
   as v2-authoring reads; plausible; unverified here.
8. REC-3's text — including whether its PATCH-1 text matches §5A.5's reproduction (this is N-1's
   resolver, and S1c's agree-check duty).
9. The claim in §13.2's note that the v2-commissioning tasking conflated the brief with REV3's Box ID —
   their internal tasking, not mine to check.

## 8 — DEMAND REGISTER (per the extract's own invitation; not a failure of the review)

1. **The `_lstat_kind` definition region of A1** — hash-bound extract, `def _lstat_kind` through its last
   return, plus any use of `os.stat` / `os.path.exists` inside it — for round 3 or S2's evidence packet.
   S1c's §2.1 halt already compels the read operationally; this demand is for the review record, so the
   blocker's one remaining contingency is discharged against bytes someone other than S1c has seen.
2. **REC-3's PATCH-1 text** (or its extent-marked equivalent in v3) — to resolve N-1's boundary question
   at authoring time rather than mid-job.

---

## 9 — VERDICT

**REVISE.** All twelve round-1 findings are ADDRESSED — the blocker's four-part fix is present, operative,
sequenced before authoring, and corroborated against A1's bytes as far as the supplied window reaches; the
fold-in survives first review with its architecture intact; the acceptance machinery now halts where it
used to describe. The REVISE rests on N-1, N-2 and N-3 — three bounded, textual defects, the largest of
which (N-1) sits on the apply path and is one extent-statement and one word ("HALT") from closed. Nothing
found this round requires re-architecture, and nothing above re-litigates what round 1 cleared.

*Review bound to v2 sha1 `887ca2e46cee517e73ec1dbdeae8a9cfe4757a37` (99,701 B · 1,235 lines), ATTACH-1
`cfada914…`, ATTACH-2 `58b4de15…` (A1 bound therein at `63804b9c…`), v1 `ffa01218…` unchanged.*
