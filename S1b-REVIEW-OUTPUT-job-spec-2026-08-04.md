# S1b INDEPENDENT REVIEW — of `S1a-JOB-SPEC-fixtures-and-run-2026-08-03.md`

**Reviewer step:** S1b. **Reviewed:** 2026-08-04. **Verdict: REVISE** — 1 BLOCKER, 6 DEFECTs, 5 NITs.
This file is named `S1b-…` because S1b is the step that authored it. It reviews the S1a spec; it does not
execute it, does not verify S1c's output (S2 does), and does not rewrite the spec — findings below are the
input to the next S1a round.

---

## 0.1 — Reviewed object, bound

- Stated identity in tasking: `S1a-JOB-SPEC-fixtures-and-run-2026-08-03.md`, 34,233 B, 491 lines, Level 1 -
  Dev project folder. **No expected sha1 was supplied for the spec itself** — the one input to a review
  convened on resolve-by-hash discipline was identified by size, line count and location only. Recorded as
  an observation on the tasking, not a finding against the spec.
- What I read: a single uploaded candidate (session upload path,
  `…/e6f7f6e8-S1aJOBSPECfixturesandrun20260803.md`). Measured: **34,233 B, 491 lines — both match.**
  Exactly one candidate matched the name in my input set, so the stop-and-ask-which-hash condition did not
  arise.
- **Computed sha1 `ffa012180871dbaba2b24f38dd582d49065e2030`.** This review is bound to that byte-set. The
  next round should resolve this review against that hash, not against the filename.
- The Level 1 - Dev folder in Box was **not** consulted; this review made no Box call of any kind.

## 0.2 — Disclosure and abstention

- **Disclosure (required):** I previously confirmed that path 1's patch — the finding-2 replacement text,
  the differential gate — is internally consistent with A1. This review is therefore independent of the
  fixtures and of the acceptance criteria, but **NOT independent of path 1's patch text.** I raise no
  finding against §5(c)'s PATCH 1 provisions; that silence is the one place my prior contact could have
  dulled the review, and should be weighed accordingly.
- **Abstention (required):** I authored path 2's closure at the `--snapshot-create` branch of
  `_snapshot_cli`. Under the bar "no Max review of anything Max authored," I express no view anywhere in
  this review on whether that closure is correct, sufficient, or well-made — S2 (Gemini, fresh session)
  covers it. **The spec does not ask S1b to assess the closure** — §5(c) directs S1c to apply it as
  written, and §9 excludes merits review — so there is no defect to flag on that score. Finding 7 and the
  Q5 answer concern what the spec *says about* the closure's scope and who may review what, not the
  closure.

## 0.3 — Substrate available to this review

Checked (session git repo, `linter-cluster/`, a byte-exact mirror of the 2026-07-24/25 session outputs):

- `layer1_lint.py` — 107,222 B · `a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7` — **byte-exact match to §3's
  ORACLE pin.** Corroborates that row.
- `baseline.md` — `dd5da45a1f93963c6f1c381e9dcd292f6f79333d` — **byte-exact match to §3's BASELINE pin.**
  Corroborates that row.
- `test_layer1_lint.py` — 54,983 B · `31d74400b7a9f9064a49f0ea52ff8df3f485e39a` — matches **neither** A1
  (104,070 B / `63804b9c…`) **nor** the pre-fix file (92,385 B / `3574c2d1…`) **nor** the governed Box
  object (64,501 B / `a3e678f2…`). A fourth byte-set under the same name, on a fourth substrate —
  empirically corroborating §3's name-collision warning. It contains **zero occurrences** of
  `OraclePinError`, `EngineSetCopyError`, or `BaselinePinError` (it predates the abort machinery), so
  **nothing about A1's raise sites is checkable from it.**

Not available to me: A1, A2, the step-3 findings record, the R5 brief, `oracle-build-brief-REV3`, the
corrections intake, plan v1.2, `ORACLE-LEDGER.md`, the 2026-07-30 logs, and the bars/rulings texts. Every
"could not check" below refers to one of these, and is stated as *unverified*, not as *wrong*.

---

## FINDINGS

### Finding 1 — BLOCKER — paths 2 and 3 are ordered independent, but the spec's mechanism does not make them independently demonstrable

The spec states the requirement exactly right:

> "**Two of the four are the same exception class reached by different routes** — a fixture set that trips
> `EngineSetCopyError` twice by the same route has discharged one path, not two. Assert the route, not only
> the class." (§2)

but the mechanism it then mandates is:

> "Each fixture asserts (i) a literal substring unique to its own raise site or handler, and (ii) the
> **absence of the nearest decoy abort's marker**." (§5a)
> "Assert on the literal text between the placeholders, and prefer the run that is **unique** in the file —
> verify uniqueness by reading, not by assuming." (§3)

Three gaps, one consequence:

**(a) Nothing requires the four asserted discriminators to be pairwise distinct.** "Unique to its own raise
site" is uniqueness of the substring *within A1*, not distinctness *across fixtures*. If A1 raises
`EngineSetCopyError` for both causes from a single raise site (one invariant run), then fixtures 2 and 3
both satisfy every stated rule by asserting the same substring with the same `A1:<line>` citation — and
both pass whenever *either* cause fires. Whether A1 has one shared or two distinct raise sites for the two
causes is **UNVERIFIED** (A1 is not in my substrate; the same-named copy I hold predates the abort
machinery entirely). The defect is that the spec leaves the outcome to that unestablished property of A1
either way.

**(b) "The nearest decoy abort's marker" is never assigned per fixture.** The only assignment that makes
paths 2 and 3 mutually exclusive — each asserts the absence of the *other's* marker — is not required, and
"nearest" reads at least as naturally as the nearest *other class*. For every pair except 2/3 the decoy
choice is low-stakes; for 2/3 it is the entire question this spec was convened to close.

**(c) No halt rule covers the indistinguishable case.** §2 halts on enumeration mismatch; §3 halts on
underivable strings ("you invented it — say so"). Neither covers "derivable but identical for both
routes." A route that cannot be textually discriminated should be a HALT-and-report; the spec does not say
so.

**Consequence.** A fully compliant S1c can return four green rows demonstrating three causes. Concretely
(risk class, not a claim about A1 — A1 unverified): a dangling symlink presented to an `exists()`-style
check that follows links reads as an *absent source*; fixture 2 then trips route 3 while every required
assertion passes. §10.6's "the route traversed" then reports setup *intent*, not an observable. F4.1's
verbatim-quote rule would capture the interpolated tail of the message — the one place the wrong cause
could show — but §3 explicitly directs assertions *away* from placeholder content, and no condition directs
anyone to check the interpolation against the claimed cause. That is precisely "four fixtures proving
three things" with logs that look like success.

**Fix direction (not a rewrite):** require the four discriminators to be pairwise distinct and
cause-anchored; require fixtures 2 and 3 to each assert the absence of the *other's* discriminator; require
S1c to verify by reading A1 that the two causes produce distinct invariant runs, and HALT-and-report if
they do not.

### Finding 2 — DEFECT — "or handler" lets a route be proven at the wrong layer

> "(i) a literal substring unique to its own raise site **or handler**" (§5a)
> "**two primary discriminators exist only in the patches and appear nowhere in A1** — grepping A1 for them
> returns nothing" (§3)

The patch-only markers (PATCH 1's recorded row, PATCH 2's printed verdict) mark **which door the abort
exited** — the in-process differential gate or the CLI — not **which known-bad input caused it**, while
§2's table defines the four paths by input, "in the record's own words." A fixture satisfying (i) with the
handler marker alone has demonstrated the exit, not the cause. If the prescribed routes send fixtures 2 and
3 through different patches (**UNVERIFIED** — the routes live in the brief, which I do not hold), swapped or
duplicated causes stay green behind the correct handler markers. The complete assertion is the raise-site
(cause) discriminator **and** the handler marker where a patch is traversed; "or" under-requires.

### Finding 3 — DEFECT — the pre/post differential does not evidence what the spec says it evidences

> "**Pre = the scratch tree before the patches and fixtures; post = after.** The pre log is what makes the
> post log mean anything: it is the evidence that the abort was **absent** before and **present** after."
> (§5d)

With the fixtures absent from the pre tree, nothing *attempts* the four aborts pre; the pre log evidences
that the stock driver was green (useful for attribution), and nothing about the four paths. As defined,
"absent before" is vacuous. The differential that would carry evidence — fixtures present on both sides,
patches only in post; pre showing each discriminator FAILING (raw traceback text in child output), post
showing it PASSING — is required nowhere, even though §7's carry-forward states exactly that standard for
isolation:

> "with a **negative control** showing the discriminator FAILING when isolation is deliberately disabled."

Whether the 2026-07-30 run's "shape" actually had fixtures on both sides is **UNVERIFIED** (logs not in my
substrate); the defect is internal — the spec's gloss contradicts its own definition. Left unfixed, this
compounds Finding 1: the one structural control that could catch a non-firing or wrong-firing fixture is
defined so that it cannot.

### Finding 4 — DEFECT — the fixture mechanisms re-enter the critical path with no review anywhere

> "**TAKE from it:** the four fixture definitions and their prescribed routes … It is the only place the
> fixture-level detail exists." (§4)
> "**Nothing in it is pre-cleared**" (§4); "**R4 is dissolved, not waived.**" (§1)

The bar quoted in my tasking reads "no brief, spec or task file launched without its own independent
review." S1b reviews this spec; the spec incorporates the brief's fixture definitions by reference; the
brief's own review step (R4) no longer exists. Net effect: the operative fixture-level content launches
with **no review at any step** — S1b cannot reach it (the brief is not an S1b input; **UNVERIFIED, not
wrong**), and S2 sees it only after execution. The in-spec mitigations (§5a's route-objection duty, §3's
derivation rule, D7's author-is-runner) reduce the exposure but do not substitute for review. Either the
four definitions' operative content comes **into** the spec, making it reviewable at S1b, or the TAKEn
material gets its own review step.

### Finding 5 — DEFECT — must-read inputs sit outside §3's by-hash table: truncated hashes, unstated substrates, and one threat to the no-Box posture

> "Only the values this job **cannot function without** appear here." (§3)

The job cannot function without at least two objects that are not in §3's table:

- **The R5 brief** — sole carrier of the fixture definitions — identified in §4 as "31,825 B ·
  `c7211de83ee08…`": truncated hash, **no substrate or path stated anywhere**.
- **`oracle-build-brief-REV3`** — F3 requires "every completeness condition in the set, **enumerated at
  read time from `oracle-build-brief-REV3` PART 1(c)**", and §4 identifies that document as "(51,009 B ·
  `0270340debc5…`; Box `2373322144026`)" with **no local copy named** — while §11 states "the one Box
  interaction is a **metadata read** for §10.9." If no local REV3 exists, F3 forces a *second* Box
  interaction — a **content** read — contradicting §11; if a local copy exists, the spec must say where and
  bind it by full hash. Which arm holds is **UNVERIFIED** (I hold no tree inventory).

Same hygiene gap, lower stakes: `ORACLE-LEDGER.md` (§12 says "Read it there" — substrate unstated) and the
corrections intake (`90eae013ed0e…`, provenance only). The spec demonstrates the correct pattern on the
findings record in §2 (local sha1 + Box ID + "local and Box bytes AGREE") and simply does not apply it to
these. In a tree where "Name-resolution fails … demonstrably," truncated prefixes and unstated substrates
on must-read inputs are the §3 fault class, inside the spec that names it.

### Finding 6 — DEFECT — the acceptance surface itself rests on a carried cross-document count

> "The five defects and their fixes are recorded in
> **`CODECLI-CORRECTIONS-INTAKE-and-STAGED-FILINGS-2026-08-03.md`** (22,187 B · `90eae013ed0e…`) §3 as
> **AC-1 … AC-5**." (§4)

§7 then closes AC-1…AC-5, one per F-rule. That is the exact form F5 bans — "**Do not write 'the six X' or
'the eight Y' about another document's contents**" — applied to the one place a silent shortfall is worst:
if the intake's §3 records a sixth defect, §7 under-closes and nothing surfaces it. No read-time
re-derivation of the AC set is ordered on anyone (S1c or S2). I could not check the intake (not in my
substrate): this is **unverified completeness, not a wrong count**. Fix direction: bind §7 to the intake's
§3 *enumerated at read time*, mismatch → HALT — the same shape §2 already uses for the four paths.

### Finding 7 — DEFECT — §11's availability analysis for S1b omits the candidate reviewer's patch-2 authorship

> "**Max is available on the face of it** — under D7 Max authors neither this spec nor the fixtures, so
> barred 4 does not bite — **but availability is not allocation.**" (§11)

The spec itself records that patch 2 is "**Max's closure at the `--snapshot-create` branch of
`_snapshot_cli`**" (§5c) and quotes the brief assigning "Patch 2's text and the section-7 comment are
yours" to Max (§4.3). Under the bar quoted in my tasking — "no Max review of anything Max authored"; I hold
no bars text and cannot verify its number — either: that bar **is** barred 4, in which case "does not bite"
is false as written (it bites, scoped to patch-2 substance, and a Max S1b requires a declared abstention
plus disclosure); or it is a different bar, in which case §11's analysis never considers it at all. Either
way the availability claim is overbroad, and the abstention this review carries arrived via the external
tasking, not via the spec. The next revision should scope the Max option explicitly ("available with
abstention on §5(c)-PATCH-2/§8 substance, disclosed in S1b output") or rule it out.

### Finding 8 — NIT — F1's required phrasing is engine-specific while §10.8 universalizes it

> "Every reported count is phrased as **'the total recorded for the pinned engine at pin time'**" (F1)
> versus "**Every count paired with an identity on the same line** (F1)" (§10.8)

Non-engine counts the report must contain (fixture totals, set sizes, tree counts) have no defined identity
form under F1's wording. §12's object-plus-substrate rule is the evident intent — point F1 at it, or state
the identity form for non-engine counts.

### Finding 9 — NIT — F2's rationale grounds fuzz reduction in a block §7 has just voided

> "**reduced fuzz is authorised** for the AS-1 and AS-2 demonstration sets" (F2) — one page after "**§7
> below is binding; the AS block as written is not.**" (§4)

The F2 *requirement* stands on its own; the authorization pointer dangles. Name the live source of the
reduced-fuzz authorization (presumably the brief's "run-budget shape," §4 TAKE).

### Finding 10 — NIT — residual carried counts survive "hold this spec to it too" (§7/F5)

- "**Thirty-two files are named `test_layer1_lint.py`**: fifteen are the **pre-fix** harness and seventeen
  are the **fixed** harness" (§3) — substrate semi-named, no read-time binding;
- "five of JR's six remain open" (§9);
- "the nine-subtask ID↔name map" (§12);
- "the fixed harness and fifteen decoys sharing its filename" (§12);
- "four lines" as patch 2's size (§5c, §8, §6 rationale) — descriptive, but a mismatch against the patch as
  applied invites a halt-or-not question §5(c) does not answer.

None is operative for S1c's assertions; all are the banned form. Incidentally, my substrate corroborates
the collision phenomenon itself: the session repo carries a **fourth** byte-set under the same harness name
(54,983 B · `31d74400…`).

### Finding 11 — NIT — §1's table carries the summary §8 bans

> "R1 | path 2 — close it, **no ruling on intent**" (§1) versus "**'Path 2 is closed' is WRONG as a summary
> and must not be written that way anywhere**" (§8)

A reader of the table alone leaves with the banned reading. A two-word scope tag in the row ("CLI route —
§8") closes it.

### Finding 12 — NIT — §10.9's job-end metadata read has no failure branch and no job-start baseline

If the connector read fails at job end, only §9's generic say-which-report-you-have posture covers it; the
job's one external dependency merits an explicit line ("report the attempted read and its error; do not
substitute §3's value"). And an end-only read cannot attribute a between-times version move to or away from
this job; a start-plus-end pair would. Fail-closed as written — direction right, attribution weak.

---

## THE SIX REVIEW QUESTIONS, ANSWERED

**1. The four abort paths.** Enumeration discipline is solid: §2 quotes the findings record verbatim, binds
it by full hash with a substrate-agreement statement, and orders "**If a read at S1c time yields a
different set or a different number, HALT and report — do not force it to four.**" Independent
demonstrability of paths 2/3 is demanded in words but not secured by mechanism — Finding 1 (BLOCKER),
Finding 2. Precisely: one *run* cannot discharge two rows (§5a: "One per abort path in §2," "exactly one
`outcome(name, ok, detail)` call"), but one underlying *cause* can satisfy both fixtures' full assertion
sets, yielding four green rows proving three things. **As written: not independently demonstrable by
construction.**

**2. Does each fixture trip the path it claims?** Not determinable from this spec: the mechanisms live in
the R5 brief (not an S1b input — Finding 4), and A1 is not in my substrate. That is "**could not check**,"
not "wrong." What the spec itself fixes mechanically is sound: pass polarity ("**A fixture PASSES when the
abort HAPPENS**"), aborts as text in a child process, the ban on generic `except` in setup/teardown, the
can't-kill-`main()` constraint, and the reach-the-check precondition for path 4 (§3 ORACLE row: path 4
"needs one that **does**" match, so execution reaches the baseline check). The analogous preconditions for
paths 2/3 are unstated here and live in the brief with the rest of the mechanism (Finding 4). Findings 2
and 3 name the two places the spec's own text would let a false demonstration pass unnoticed.

**3. The acceptance criteria.** The five replacements hold as rules. **F1 ✓** — identity on the same line
required; the recomputable-versus-on-authority split (shim sha1 vs set-sha1, `ORACLE-LEDGER.md` pointer) is
honest (Nit 8). **F2 ✓** — effective fuzz and K per run, inert fuzz stated explicitly, no bare totals,
timeout per subprocess (Nit 9). **F3 ✓** — the fifth condition is resolved IN SCOPE with an existing named
control (`s_hashmismatch`) and an unrun-must-be-named rule; its enumeration source is under-bound as an
input (Finding 5). **F4 ✓** — the strongest of the five: verbatim observed verdicts so a reworded message
surfaces as a mismatch, UID as a computed fact, every absence paired with a positive. **F5 ✓ as a rule** —
and the spec breaks it itself in one operative place (Finding 6) and several decorative ones (Nit 10). So:
the replacements hold; the answer to "any counts of another document's contents left anywhere" is **yes**,
at the locations listed in Findings 6 and 10.

**4. Where Code-CLI's responsibility ends.** Sufficient and clear. "**It ends when the report in §10 is
emitted**"; "**A log meeting §7's conditions is a NECESSARY and NOT a SUFFICIENT finding**"; the
not-as-courtesy list; both guarded failure modes named with the correct remedy ("say which report you
have"); §10.10's mandatory populated not-verified section; §10's ISSUING-CHAT rule. The
asserting-evidence-it-cannot-have seat and the silently-omitting seat are both closed from the reporting
side. No finding beyond Nit 12.

**5. Path 2 scope.** **Confirmed present, correct, and complete as statements** — without any view on the
closure itself (see 0.2): CLI route only ("**Adopting the closure closes the CLI ROUTE ONLY**"); importer
raise-through "**unchanged and deliberate**" / "unchanged by design" (§8, §6.3); the summary "path 2 is
closed" banned in report, logs, code comment, and commit message (§8) and again in §10's do-not-include
list; per-route assertion semantics stated (a "no exception" assertion on the importer path "would be
**asserting against the design**"); the residual honestly recorded ("**A reviewer who reads finding 2 as
being about a public API function will find that part still open and may reasonably re-raise it**"). Nit 11
is the one blemish. The spec routes closure verification to S2 and does not ask S1b for it — correctly.

**6. Producible in scratch, no Box access, no token?** Yes, with one exception: F3's read of REV3 (Finding
5). The single §10.9 metadata read is explicitly accounted as connector-served and tokenless; "A 401 on the
raw API does not block this job" is consistent with that; the scratch-only table, zero-write posture, and
the capability-is-not-permission note are coherent. Nothing else in the spec requires Box content or a
token.

---

## VERDICT

**REVISE.** The blocker (Finding 1) sits on exactly the question this review was convened for. Findings
2–7 are defects for the next S1a round; the nits are recorded for the same round. Nothing here requires
re-architecture: §2's enumeration discipline, §7's F-rules, §9's boundary, and §8's scope language are the
right shape — the blocker is a missing mechanism (pairwise-distinct cause-anchored discriminators, the 2↔3
decoy pairing, a halt rule for the indistinguishable case), not a wrong design.

*Review bound to spec sha1 `ffa012180871dbaba2b24f38dd582d49065e2030` (34,233 B, 491 lines).*
