# STEP4-GOVERNING-DOC — DRAFT — apply the fix run under GATE-V — v0.2 2026-08-01

**STATUS: DRAFT v0.2 — NOT REVIEWED, NOT CLEARED, NOT LAUNCHABLE.** Under the standing rule of
2026-07-27 this document requires independent adversarial review before staging, sharing or
launch — it has had none. Its criteria were authored by the seat that wrote it (the
seat-authored-criteria weakness that rule exists to catch). It also requires **JR's confirmed
read** before the apply it governs, because the apply is the irreversible step and that read has
been skipped once already (brief §12.3). **Do not launch on the strength of this document.**

**Authority: NONE.** This draft cannot widen any write ceiling, waive any verification, create
any never-write exception, alter any threshold, or authorise anything — including its own
launch. The live records and the Layer 1 documents win over every sentence in it. Every carried
value below is a prior record's claim unless marked verified; section 12 keys every one.

**Drafting seat.** Claude Code remote session on model `claude-fable-5` (Claude 5 family,
Mythos-class tier above Opus-class; Processing Model Standard satisfied), Box-visible only as
the Max account (`rodwel@me.com`) — see the companion
`STEP3-PACKAGE-AUDIT-v1.1-2026-08-01.md` for that seat's visibility limits. The drafting seat
could NOT read the tasking brief `MAX-SESSION-BRIEF-audit-and-step4-governing-doc-2026-08-01.md`
(Mac-local; not visible from the container) and worked from the task message's relay of its
constraints. **NOT the executor.** The executor of step 4 is the **Teams Code-CLI seat**.

**REQUIRED MODEL for execution: Opus-class or higher.** If the executing seat is running below
Opus-class it HALTS and tells JR before reading inputs, staging anything, or writing anything.

---

## PLAIN ENGLISH, FIVE LINES — for JR

1. Step 4 takes the four safety fixes that were built and proven in a throwaway copy, and — only
   after the Gemini review clears them — installs them into the real, governed harness in Box.
2. Exactly ONE governed file changes: the test harness. Everything else stays byte-identical,
   and the write is a Box version-replace, so it is reversible.
3. The proof it worked is NOT the review and NOT the earlier scratch run: it is a fresh download
   of what actually landed, re-tested green by a non-root run on that downloaded copy.
4. The old sealed snapshot pin dies the moment the fix lands — that is EXPECTED, and this
   document says exactly which one mismatch is expected so every other mismatch still screams.
5. Steps 5 (retake the snapshot) and 6 (re-record the pin) are separate steps and stay separate;
   this document hands them forward and forbids folding them into "done".

---

## 1. WHAT STEP 4 IS, AND WHAT IT IS NOT

From the six-step sequence of `CODECLI-FIXRUN-BRIEF-v2.1-2026-07-28.md` §3 [U-DOC], restated:

```
STEP 1  Build the four fixes on the revised harness.          DONE 2026-07-30 (FIX-RUN-REPORT)
STEP 2  Gate green in scratch, non-root, full fuzz.           DONE 2026-07-30 (FIX-RUN-REPORT)
STEP 3  Gemini CODE-CHANGE review of the fix diff,            NOT DONE at drafting time.
        fresh session, v2.0 package.                          PRECONDITION P1 of this document.
STEP 4  APPLY under GATE-V, with an independent non-root      <-- THIS DOCUMENT
        re-run as the correctness proof.
STEP 5  RETAKE the snapshot.                                  NOT this document. DISTINCT step.
STEP 6  RE-RECORD the pin.                                    NOT this document. DISTINCT step.
THEN    One governance-doc Box write closes the workstream    NOT this document. Named in §10.
        (869e9h7ym action 1, catalog 2328644291918).
```

**Scope of the write, stated exactly.** Step 4 writes **ONE governed object**: a new version of
`test_layer1_lint.py`, Box `2296699168749`, in Cowork-Layer1-Tooling folder `396978339615`,
replacing its current bytes with the FIXED harness. **Nothing else in the governed folder
changes**: not the engine shim, not the 12 `l1lint` modules, not `manifest.yaml`, not
`baseline.md`, not the frozen oracle. The demo driver was NOT edited by the fix run (UNCHANGED,
`2651b859…` [U-DOC]) and is not governed tooling. Any need to write a second object is a scope
change: **HALT and ask JR.**

### THE APPLY MODE — WHOLE-FILE VERSION-REPLACE. THE SUBSTRATE IS NOT AT THE FIX DIFF'S BASE.

This block sits ahead of the preconditions deliberately: it defines what the apply IS. The
preconditions (§2) gate whether it may run.

**The fact, stated plainly: the copy in the governed folder is the STAGED harness, not the
PRE-FIX harness.** The governed object `2296699168749` is expected to hold `a3e678f2…` /
64,501 B — brief §4's own row calls it "staged harness v6 … reference only; NOT the base", the
state cache (§5) records the same identity, and the fix run wrote nothing to governed
[all U-DOC; this seat cannot see the object]. The fix diff's base — the PRE-FIX / revised
harness `3574c2d1…` / 92,385 B — exists only in build-outputs (Box `2373463499360`) and in
staging trees. **It has never been in the governed folder.**

Four consequences, spelled out so no operator has to derive them at apply time:

```
1  THE FIX DIFF CANNOT BE PATCH-APPLIED TO THE GOVERNED OBJECT. The governed bytes are not at
   the diff's base and never were. Any patch-mode tool that pins a base of 3574c2d1… will
   (correctly) refuse against the governed object. That refusal is fail-closed behaviour
   WORKING — and the WRONG remedy is "fixing" it by first uploading the base (see 3).
2  STEP 4 IS THEREFORE A WHOLE-FILE VERSION-REPLACE of the fixed bytes (63804b9c…), and the
   diff-base relationship is proven OFF-substrate, before any write: S5(a) requires that
   applying the fix diff to a staged copy of the pre-fix harness (3574c2d1…) reproduces the
   fixed harness byte-exactly. The substrate never needs to be at the diff's base, because the
   diff is never applied to the substrate.
3  NO INTERVENING APPLY of the revised harness (3574c2d1…) — not as its own step, not as a
   repair. That intermediate is precisely the state gate (ii) REFUSED to clear standing alone
   (verdict REVISE, four gated fixes: "leaving the identity unasserted fundamentally breaks
   the differential's anchoring"). The total governed delta a3e678f2… → 63804b9c… is the
   COMPOSITION of two reviewed deltas — the authoritative build diff (gate (ii)'s subject) and
   the fix diff (step 3's subject) — and lineage is preserved by Box version history and the
   two diffs' annotated headers, not by materialising an un-cleared state on the substrate.
   One write also means one read-back and one transport exposure instead of two.
4  S5(d)'s pre-write assert on a3e678f2… is a QUIET-SUBSTRATE check — proof that nobody else
   has written — NOT a patch-base check. If it fails, someone's write has landed: INTEGRITY,
   fail-closed lockdown, JR. Never "upload the base and continue".
```

**Six-step discipline.** Before staging anything, the executor restates all six steps in its own
words and states that this run performs step 4 only. A restatement that reads "apply → done" or
folds 5/6 into 4 means the trap is lost: stop and re-read brief §3. Proof: report item R1.

---

## 2. PRECONDITIONS — ALL must be YES before any staging. Any NO → HALT and report to JR.

```
P1  STEP-3 VERDICT. The fresh-session Gemini review (v2.0 package) has run and its FINAL
    verdict on the fix diff is CLEAR-TO-APPLY — either first pass, or after REVISE rounds
    applied mechanically per Run Card C, capped at 2–3 substantive rounds. The full review
    output, INCLUDING its completed D1–D6 declaration with a non-empty D6, is on file and was
    brought back to JR / Level 1 unchanged. A reviewer halt, a STOP in any D-item, or an empty
    D6 means step 3 is NOT satisfied. CLEAR means "design-sound, no gaps found" — it is not the
    correctness proof and does not weaken S8–S10.
P2  JR'S CONFIRMED READS, in writing: (a) of the fix-run brief v2.1 (sha1 7a59e1b2…) — recorded
    NOT CONFIRMED as of 2026-07-30 and gating exactly this step; (b) of THIS document in its
    reviewed, cleared revision. Neither read is inferable; each is a stated confirmation.
P3  ADVERSARIAL REVIEW OF THIS DOCUMENT is complete and its verdict recorded, per the standing
    rule of 2026-07-27. This v0.2 draft fails P3 by construction.
P4  JR'S RATIFICATIONS, each recorded: (a) the frozen oracle's full pin
    a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7 / 107,222 B (two independent computations exist —
    Teams seat 2026-07-30 from Box 2367835811909; audit session 2026-08-01 from the git mirror —
    but computation is not ratification); (b) the six reversible decisions of FIX-RUN-REPORT
    ("DECISIONS TAKEN IN THIS RUN THAT JR CAN REVERSE"), explicitly including FIX 1's engine15
    choice, the pin's location in ORACLE_IDENTITY_PINS inside the harness, and the two-value
    pin set. A reversal here changes the artefact: it sends the work BACK to step 1, not onward.
P5  THE TRANSPORT RULING. JR has ruled the ≥64 KB transport SCOPE question for this apply. The
    fixed harness is 104,070 B [U-DOC]. Default expectation pending that ruling: BYTE-TRANSFER
    ONLY (Box Drive sync tree, file upload, or git) — a text-parameter route is unverified by
    construction (clause 3, 2026-07-30) and is PROHIBITED for the apply payload regardless of
    the ruling's shape.
P6  CREDENTIAL PLAN. The Box developer token expires ~60 minutes after JR applies it. The token
    is refreshed immediately before S6 (the write phase), not at session start. JR's 2026-07-28
    credential-vs-integrity ruling and its decision table (brief §0) are in force verbatim for
    every assertion in this run.
P7  SUBSTRATE QUIET. No other job is writing to the governed folder or the pins during this
    run. On 2026-08-01 a parallel Teams Code job held Box/ClickUp write authority — step 4 must
    not run concurrently with any such job. JR confirms quiet before launch.
P8  ARTEFACT IDENTITIES IN HAND. The executor holds, from the fix run and step 3: the fix diff
    (8f648d73… / 16,600 B), the fixed harness (63804b9c… / 104,070 B), the pre-fix harness
    (3574c2d1… / 92,385 B), the SETPIN file (9f4fc6c7… / 1,513 B, Box 2373446865036), and the
    step-3 output. All are [U-DOC] here and MUST be re-verified by local shasum at S4 — this
    document's copies of these values are reference, never authority.
P9  EXECUTION SEAT. Teams Code-CLI seat, Opus-class or higher, main-account Box visibility,
    non-root shell available. (The Max-account seat that drafted this cannot execute: it cannot
    see the governed folder at all.)
```

---

## 3. SESSION START — in this order, before anything else

```
S1  Load Box 2291166678888 (Governance-Dev charter); state "Layer 1 Governance-Dev charter
    loaded". Load GATE-V 2289594143154, Rules 2289598235660, Tag Use 2289594294545 from LIVE
    Box; state "Cowork Layer 1 loaded (GATE-V + Rules + Tag Use)". Assert GATE-V's live
    server-side sha1 against the CURRENT JR-confirmed pin carried by the launch prompt (the
    2026-07-28 recorded value was d6d54ae7… / 19,365 B [U-DOC]; a GATE-V de-bloat is queued, so
    the launch prompt, not this draft, carries the pin current at launch). Apply the §0 table.
S2  Fetch Scope Registry 2327535678598; assert live sha1 against the launch prompt's current
    pin (2026-07-28 recorded value 231ebe46… / 5,975 B [U-DOC]). Same table.
S3  Read the state cache (Box 2373971080457) — ADVISORY, authority NONE. Two known hazards:
    its §2 still says "step 4 of 5" and "use the existing gate (ii) session"; both are dead.
    The six-step count in §1 of THIS document and the fresh-session record govern. Then restate
    the six steps (report R1).
```

---

## 4. STAGE AND VERIFY — nothing is written until S6, and only after S4+S5 pass

```
S4  STAGE BYTE-EXACT, outside the Box-sync tree, as non-root (record `id -u`; must not be 0).
    Stage: the fixed harness; the fix diff; the pre-fix harness; the SETPIN file; and the live
    governed engine set (shim, 12 modules, manifest.yaml, baseline.md) fetched byte-exact from
    folder 396978339615. Compute sha1 -a 1 and byte count for EVERY staged input; report
    expected-versus-computed in full 40-hex. Expected values come from the fix-run report and
    step-3 output, re-quoted in the launch prompt. ANY mismatch → HALT, quote both values,
    classify per the §0 table.
S5  FOUR PRE-WRITE PROOFS, each its own line in the report:
    (a) DIFF INTEGRITY: applying the fix diff to the staged pre-fix harness (3574c2d1…)
        reproduces the fixed harness byte-exactly (sha1 63804b9c…, 104,070 B). This re-derives
        the fix from its reviewed delivery form rather than trusting a carried file. It is the
        ONLY place the fix diff is ever applied — off-substrate (§1 apply-mode block).
    (b) UNDERSCORE CONTROL: in the RAW fix diff and the staged path lists, every occurrence of
        the l1lint init filename reads as four underscore characters (two + init + two) + .py.
        Any init.py → transport corruption → HALT and re-export; never repair by hand.
    (c) SETPIN ENUMERATION: enumerate the pinned paths from the SETPIN file's own `files`
        object; the count MUST be 16. Anything else → STOP, ask JR.
    (d) GOVERNED PRE-STATE: the live governed harness 2296699168749 still carries the OLD v6
        bytes — server-side sha1 a3e678f2… / 64,501 B (see §1's apply-mode block: this is a
        quiet-substrate check, not a patch-base check). Any other value RESOLVES-AND-DISAGREES
        → INTEGRITY → fail-closed lockdown per GATE-V: someone or something has already written
        to the substrate, and step 4 must not stack on it.
```

---

## 5. THE APPLY — one governed write, then verification that follows the write

```
S6  Refresh the token (P6). Then perform the ONE write: upload the fixed harness as a NEW
    VERSION of Box 2296699168749 (version-replace — Box-versioned, therefore reversible). No
    other write. A refused or failed write → HALT and report; ANTI-AUTO-RECOVERY applies — no
    retry against a different target, no substitute route, no parent/child traversal.
S7  READ-BACK (GATE-V discipline; clause 2's rule — verification follows the WRITE, not the
    writer): fetch the destination's NEW server-side sha1 and size; they MUST equal the fixed
    harness's declared identity (63804b9c… / 104,070 B). A size match alone is NOT
    verification. Mismatch → INTEGRITY → restore the prior version (S11) and lockdown.
```

---

## 6. THE CORRECTNESS PROOF — an independent non-root re-run ON WHAT LANDED

**This re-run — not the step-3 review, not the 2026-07-30 scratch gate — is the correctness
proof** [U-DOC brief §3, restated as binding here].

```
S8  FETCH-BACK: into a FRESH scratch directory (outside the sync tree, non-root), download the
    full 16-path set FROM THE GOVERNED FOLDER as it now stands, byte-exact. Verify: the fetched
    harness is 63804b9c…; the other 15 paths match the SETPIN's recorded per-file hashes (the
    engine did not change in step 4). Any mismatch → INTEGRITY → S11.
S9  RUN THE GATE on that fetched tree, non-root (`id -u` recorded again):
      --selftest                      criterion: the recorded baseline count, 89/89, under the
                                      brief §9 table VERBATIM — any other count, any failure,
                                      any lost case → STOP, quote output, attribution table if
                                      risen, JR rules. No self-clearing.
      differential Phase A and B      full fuzz 1100 / K=3; report ACTUAL counts and rc; the
                                      2026-07-30 reference wall-clock was 25–45 min/phase —
                                      silence is not a hang.
      demonstrations                  expected 17/17 with verdict lines byte-identical to the
                                      fix run's post-edit capture [U-DOC]; any movement → STOP
                                      and report (an assertion moved between scratch and apply
                                      — that is evidence, not noise).
S10 ORACLE AND PIN STATE, declared with exactly one expected death:
      frozen oracle file sha1         MUST still equal the ratified pin (P4a).
      engine15 set-sha1               MUST equal 9520867753d0… [U-DOC report decision 1] — the
                                      engine did not change.
      16-path set-sha1                EXPECTED to differ from ccda6511… — the sealed pin is
                                      DEAD BY DESIGN the moment the fix lands (brief §3). This
                                      one predicted mismatch is NOT an integrity event and MUST
                                      be reported as "moved as predicted". EVERY OTHER mismatch
                                      in this run keeps its full INTEGRITY meaning.
S11 ROLLBACK PATH (only on S7/S8/S9/S10 failure): restore Box 2296699168749 to its prior
    version via Box version history; read-back the restore (expect a3e678f2… again); report to
    JR as INTEGRITY with all values quoted. A rollback is a JR event, never a silent retry.
```

---

## 7. HAND FORWARD — steps 5 and 6, and the closing write. DISTINCT. NOT THIS RUN.

```
S12 The report hands forward, explicitly and by name:
    · STEP 5 — RETAKE the snapshot of the post-apply 16-path set. Its own step, its own gate.
    · STEP 6 — RE-RECORD the pin (the new 16-path set-sha1 replaces ccda6511… in the SETPIN
      record). Its own step. The value written is computed from the retaken snapshot and
      ratified by JR — never copied from this run's prediction.
    · THE CLOSING WRITE — 869e9h7ym action 1: record the module-SET deployment unit in the
      Cowork-Run L1 Routines catalog, Box 2328644291918. THE ORACLE IS NOT COMPLETE UNTIL THIS
      LANDS. Not part of step 4.
    Steps 5 and 6 MAY be scheduled in the same session as step 4 if JR so directs (open
    question Q2), but each keeps its own checklist, its own verification, and its own report
    line — a report that says "applied and re-pinned" in one breath has folded the fold this
    document exists to prevent.
```

---

## 8. NEVER — for the executing seat, in force throughout

```
N1  Never write anything but the ONE object in S6. No snapshot write, no pin write, no
    governance-doc write, no state-cache write, no ClickUp write in this run. The two standing
    ClickUp proposals and the 869e9h7ym write remain PENDING JR, outside this run.
N2  Never proceed past a failed assert by choosing a classification. The §0 table decides;
    UNDECIDED means stop and ask.
N3  Never treat the predicted death of ccda6511… as cover for any other mismatch, and never
    "re-verify" the old 16-path pin after the apply expecting it to hold.
N4  Never move the payload by a text-parameter route (paste, retype, model re-emission) — a
    retyped file is unverified by construction.
N5  Never run the gate as root, and never report "green" / "as expected" in place of actual
    counts and the literal `id -u`.
N6  Never repair a transport corruption (init.py, lost markers, dropped newline) by hand;
    re-export from the artefact.
N7  Never stack step 4 on a substrate whose pre-state assert failed (S5d) — that is someone
    else's write, and it needs JR before anything else.
N8  Never fill a value this document marks [U-DOC] into the substrate without live
    re-verification at run time; this draft is reference, not authority.
N9  Anti-auto-recovery, verbatim scope: a refused or failed read/write means HALT and report.
    No guessing, no context-search for an alternative, no substitute target, no nearest match.
N10 Never patch the governed object in place, and never write the intermediate revised harness
    (3574c2d1…) to the governed folder — not as its own step, not as a repair for a patch-base
    refusal. The only bytes step 4 writes are the S5(a)-proven fixed bytes, as one whole-file
    version-replace (§1 apply-mode block).
```

---

## 9. REPORT BACK — every MUST above maps to one item

```
R1   The six-step restatement, and "this run performed step 4 only".
R2   Every pin assertion with its §0 classification named (CREDENTIAL / INTEGRITY / UNDECIDED
     / agreed), including S1, S2, S5d, S7, S8, S10.
R3   The staging table: expected-vs-computed, full 40-hex + exact bytes, for every S4 input.
R4   The four pre-write proofs S5a–S5d, each with its evidence line.
R5   The write and read-back identities (S6/S7), with the destination's new Box version number.
R6   The fetch-back verification result (S8), all 16 paths.
R7   Gate output with ACTUAL counts and both literal `id -u` values (S4, S9); attribution table
     and JR ask if the selftest count moved.
R8   The S10 three-line pin-state declaration, with the 16-path movement reported as predicted.
R9   What was handed forward (S12), by name and ID, including the 869e9h7ym/2328644291918 line
     and the statement that the oracle is not complete until it lands.
R10  Whether JR's reads (P2a, P2b) were confirmed before launch — "not confirmed" written out
     if not (in which case the run should never have started; say so plainly).
R11  Any rollback, as its own section, with both read-backs.
R12  WHAT IN THIS DOCUMENT TURNED OUT TO BE WRONG. Every value it carries is a prior record's
     claim; on 2026-07-28/30 this question was never answered "nothing" by any seat. Say what
     you checked. Expected candidates: the GATE-V pin (de-bloat queued), the governed pre-state
     (parallel jobs), the reference wall-clocks.
R13  Anything you could not do, and every point where you stopped and asked JR rather than
     choosing. A stop is a valid outcome. A guess is not.
```

---

## 10. OPEN QUESTIONS FOR JR — marked, not guessed (this draft answers none of them)

```
Q1  TRANSPORT SCOPE (P5): which byte-transfer route is ruled in for the 104,070 B payload —
    Box Drive sync tree, direct API upload, or git-mediated? (4-SYNC names governance-doc
    writes; the harness is tooling.)
Q2  SESSION SHAPE: may steps 5 and 6 ride the same session as step 4 under their own
    checklists, or does JR want separate sessions/launches?
Q3  RATIFICATION VEHICLE: does JR's P4 ratification land as a ClickUp comment, a decisions
    record, or both — and who files it (not this run)?
Q4  Should the step-4 launch prompt re-pin GATE-V/Scope-Registry values itself (they may
    legitimately move before launch), and who confirms them current at launch?
Q5  Does the near-miss filename gate (869eb7dre) join the workstream BEFORE the apply (state
    cache 0d2 notes the cheapest moment has passed once step 3's package is sent), or wait?
Q6  Where does this document live once cleared — local only (the ≥64 KB rule does not bind it:
    it is ~17 KB), Box References, or the exchange folder?
```

---

## 11. WHAT COMPLETION OF STEP 4 UNBLOCKS — carried so it is not rediscovered

Steps 5 and 6, then the 869e9h7ym action-1 closing write; then, per brief §17: the
no-lazy-imports lint as the first engine change verified under the new model; `869dx7xpc`;
`869dwncba` battery wiring; and the GATE-V de-bloat `869e9hwky`, which is a bump-queue
precondition. [U-DOC brief §17 — re-verify liveness at the time.]

---

## 12. IDENTITY REFERENCE — every value above, with provenance. RE-VERIFY LIVE AT RUN TIME.

Provenance keys as defined in `STEP3-PACKAGE-AUDIT-v1.1-2026-08-01.md` §1 (V-BOXMETA / V-LOCAL /
V-READ = verified by the drafting session on 2026-08-01; U-DOC = carried claim, unverified).

```
OBJECT                          IDENTITY CARRIED HERE                            PROVENANCE
fix-run brief v2.1              7a59e1b21165e8901e9811cd7e4a3cccf2f27cdc 75,066B V-BOXMETA (New Inbox copy) + 3 agreeing records
fixed harness                   63804b9c1d797e3627e8f59969a415b560fe6c2a 104,070B U-DOC (FIX-RUN-REPORT §5) — local to executor
fix diff                        8f648d73c2274d1108ebe7b922a87b5da27147e3 16,600B  U-DOC (FIX-RUN-REPORT §5)
pre-fix (revised) harness       3574c2d13a7f34f7cd8d1bac3543b05556e18ef9 92,385B  U-DOC (brief §4; RUN-CARD; 03 §2 — agreeing)
governed harness pre-state      a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85 64,501B  U-DOC (state-cache §5; brief §4 staged v6)
frozen oracle pin (to ratify)   a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7 107,222B V-LOCAL (git mirror) + U-DOC (report, from Box)
engine15 post-fix expectation   9520867753d0d26ec76e959d1a98a450d24255fa          U-DOC (FIX-RUN-REPORT decision 1)
sealed 16-path pin (dies)       ccda65118beb01d742c60f86cea140828de2ad9d          U-DOC (brief §3; report §1)
SETPIN file                     9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982 1,513B   U-DOC (report finding 5; Box 2373446865036)
demo driver (unchanged)         2651b8598cfb3af87c8ec0d9bbc7c783a1987f9b 18,586B  U-DOC (report §5)
GATE-V pin as of 2026-07-28     d6d54ae7d1d632f54e7f122efa3a1ccae7269860 19,365B  U-DOC (brief §1) — refresh at launch (Q4)
Scope Registry as of 2026-07-28 231ebe46be1a56df6e53e54941b9519ca55bad93  5,975B  U-DOC (brief §1) — refresh at launch (Q4)
step-3 instruments              d3cf5a3a… 21,724B / 5ed8de23… 6,302B /            V-BOXMETA (New Inbox copies = recorded
                                097d42fb… 5,934B                                  originals; see audit §3)
governed folder / harness ID    396978339615 / 2296699168749                      U-DOC (report §12; state-cache §5)
closing-write task / catalog    869e9h7ym action 1 / Box 2328644291918            U-DOC (brief §12.2; report §7)
```

---

*Change log: v0.1 2026-08-01 — first draft, written read-only by the Level 1 audit session*
*alongside the step-3 package audit. Sources: fix-run brief v2.1 §§0–17, RUN-CARD v2.0, 03/03b*
*v2.0 instruments, FIX-RUN-REPORT v1.0, STEP1-LAUNCH overrides, transport/retention JOB (three*
*clauses), state cache (2026-07-31 New-Inbox copy), DECISIONS-RULINGS 2026-07-17 — all read*
*2026-08-01. v0.2 same day — §1 gains the named APPLY MODE block (the governed copy is the*
*STAGED harness a3e678f2…, so the fix diff's base is not in Box: whole-file version-replace,*
*never a substrate patch, no intervening 3574c2d1… apply) and N10 pins the same rule; prompted*
*by a follow-up relay from the (still unreadable) brief. Supersedes v0.1 whole; v0.1 remains at*
*git commit 0a2b0d0. NOT adversarially reviewed. NOT read-confirmed by JR. Not launchable.*
