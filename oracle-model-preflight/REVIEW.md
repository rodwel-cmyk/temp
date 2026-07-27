# Pre-execution review — Layer 1 linter PACKAGE-CAPABLE ORACLE MODEL brief

Reviewed artifact: `63e2171a-oraclebuildbriefDRAFT20260727.md` — DRAFT, NOT staged
(build 869e9ygnm; direction endorsed 869e9x8mt; Job C2, 2026-07-27).
Review seat: Fable pre-execution seat, 2026-07-27. Read-only throughout — nothing
written to Box or any governed substrate; the brief was not staged and not acted on.
All verification results below are CLAIMS from this seat's own runs; the Code-CLI
applier's independent re-run remains the correctness proof, per house rule.

Method: (1) eight-point coverage check against the requester's checklist;
(2) executing-seat analysis (ambiguity / missing inputs / testability /
contradictions / likely first-attempt errors); (3) evidence pass — full enumeration
of the seat-visible exchange, all 12 `l1lint/` modules + shim + reconciled harness
read in full, the brief's staged-input set reassembled byte-exact in scratch
(17/17 sha1 match, see `STAGED-INPUTS-full.sha1`), the gates executed, and three
failure-mode demos executed. Raw transcripts: `EVIDENCE.md`.

---

## 1. Coverage check (quote-or-ABSENT, per the requester's checklist)

1. **Objective** — PRESENT. "Build a PACKAGE-CAPABLE oracle model … PRESERVATION —
   snapshot each verified engine as a DIRECTORY plus a pinned SET-sha1 … EXECUTION —
   per-engine import ISOLATION … keep a subprocess batch-runner per engine directory
   as the FALLBACK."
2. **Live gap** — PRESENT (split across two lines): "the engine is now a shim +
   l1lint/ module SET, so a single-file oracle can no longer preserve it" +
   "That equivalence is the ONLY thing keeping the frozen single-file oracle valid,
   and it is unsatisfiable for the NEXT behaviour-changing engine edit — the gap
   this build closes." The standing preserve-each-verified-engine rule is carried
   implicitly ("snapshot each verified engine"), not cited as the rule.
3. **Adopted constraint + deferred lint** — PRESENT, both halves ("a lazy / deferred
   import executing inside a function AFTER isolation is torn down would silently
   bind to the WRONG engine's code rather than crashing"; "it does NOT ship in this
   run — it becomes the FIRST engine change verified UNDER the new oracle model").
4. **Sequencing rule** — PRESENT, verbatim coverage in SEQUENCING (HARD).
5. **Known residual** — PRESENT (PART 3c, citing TEAMS-CR-2026-07-26-004 §5).
6. **Instrument caution** — PRESENT (same SEQUENCING block: scratch-verify against
   the frozen oracle, previous harness recoverable via Box versioning, never both
   instrument and measured thing in one run).
7. **Bundled scope** — **SPLIT VERDICT — the one checklist failure.** The
   deployment-unit BUNDLING is present ("the oracle-model item of 869e9ekb3 and the
   module-SET deployment-unit 869e9h7ym close together"), but the audit clause
   ("any copy path assuming otherwise must be audited") is ABSENT from every PART.
   Manifest re-pin PAIRING appears only as an exclusion ("Manifest re-pin PAIRING
   stays OUT"); the mechanism (one directory, one manifest, one engine always fails
   init across a re-pin) is ABSENT. Lineage confirmed in the predecessor brief:
   pairing is "the second item on 869e9ekb3", deliberately left open by both briefs.
   If the checklist intends the pairing mechanism in-bundle, the draft contradicts
   the checklist; requester's call.
8. **Structure** — PRESENT, all ten elements (sha1 header + STOP gate, objective,
   precondition, numbered parts, OUT OF SCOPE, claims-not-proof acceptance,
   factual-only REVIEW-FEED, Gemini CODE-CHANGE relay line, hard rules, downstream).

---

## 2. Executed evidence — headline results

Environment: Python 3.11.15, PyYAML 6.0.1, container runs as uid 0 (root),
`sudo -u nobody` available.

| Gate (byte-exact stage, 17/17 sha1-verified) | Result |
|---|---|
| `python3 layer1_lint.py --selftest` | **89/89 PASS, exit 0** |
| `test_layer1_lint.py --phase A` as **root** | **FAIL** — `file/infra_fail=1` (`infra:manifest-chmod000`: root reads through chmod 000, engine inits normally, `BAD rc=0`) |
| `--phase A` as **nobody** | **PASS** — determinism=True, all zeros |
| `--phase B` as **nobody** | **PASS** — determinism=True, all zeros, zero declared deltas |

Demos (full transcripts in `EVIDENCE.md`):

- **Demo 1** — the brief's literal PART-1 set ("shim + l1lint/") copied to a fresh
  directory: `INIT-FAILURE: manifest unreadable … exit 3`. Dead on arrival.
- **Demo 2** — full closure minus `test_layer1_lint.py`: `--selftest` dies in a raw
  `ModuleNotFoundError` traceback, exit 1 — outside the F2 "never a traceback"
  taxonomy.
- **Demo 3** — in-process `exec_module` of the incomplete engine: `SystemExit(3)`
  propagates through the harness's unguarded `_import`; from a different working
  directory the SAME snapshot fails via the package-missing fallback instead of the
  manifest path — the brief's "resolves l1lint only BY COINCIDENCE" claim, enacted.

---

## 3. Findings that change the brief (ranked by run impact)

**F1 — The unprivileged-runner requirement is missing from VERIFICATION.**
"differential A/B → still GREEN" is unsatisfiable as written in this seat class:
as root, `infra:manifest-chmod000` cannot fail closed. The requirement is already
on record — reconcile REVIEW-FEED (harness-fix-outputs/REVIEW-FEED.md, Box
2370091760939): "differential phases run as an UNPRIVILEGED user (uid 65534
`nobody`) — required for the chmod-000 cases; as root they fail loudly (`BAD rc=0`,
observed)". One sentence in the brief prevents a guaranteed first-hour stall.
Corollary: the word "still" presumes a pre-change BASELINE run the brief never
orders; without one, a seat would misattribute the root-environment failure to its
own changes.

**F2 — The PART-1 snapshot set is insufficient as written (demonstrated).**
`l1lint/loader.py` resolves `manifest.yaml` and `baseline.md` relative to the
engine directory (`_HERE = dirname(dirname(__file__))`) — deliberate: the split
ledger records this `_HERE` re-base as the split's ONLY non-verbatim substitution.
The manifest loads AT IMPORT with `sys.exit(3)` on failure. The engine's own
fallback message defines the ship set: "the modular engine ships as layer1_lint.py
+ l1lint/ + manifest.yaml + baseline.md + test_layer1_lint.py" — five components.
Selftest capability additionally requires the harness (fixtures) beside the engine.
Because a snapshot must therefore carry its paired manifest, PART 1 unavoidably
makes a pairing-adjacent decision even though pairing is scoped OUT — needs an
explicit directive.

**F3 — The PART-3 constraint is already violated, twice, by both engines.**
`selftest()` and `main()`'s `--emit-fixtures` branch both lazily import the harness
(`from test_layer1_lint import …`) at call time — verbatim in the frozen monolith
(lines 1622 and 1895) and in the package. The 3a lint as specified lands RED on the
current engine the day it ships; the "first engine change under the new model" must
fix or explicitly exempt these two. Salvage, verified: every l1lint-INTERNAL import
across all 12 modules is top-level, and the differential's in-process path
(`run_checks`) does no call-time importing — scoped to the l1lint namespace, the
isolation precondition holds today. Selftest/emit already run via subprocess in the
harness and should stay there. Additional constraint the lazy imports impose: the
harness module top level must remain side-effect-free (the harness documents this
itself), which binds the NEW tooling code added to it.

**F4 — The per-engine importer must survive `SystemExit`, not just
`ModuleNotFoundError`.** `_import` (spec_from_file_location + exec_module) has no
guard; a bad snapshot raises SystemExit(3) inside exec_module and kills the whole
differential. Demo 3 also shows the failure PATH is cwd-dependent. The lint spec
(3a) must also distinguish fail-closed top-level try/except imports (loader.py's
`import yaml` → loud exit 2) from the banned silent-degradation pattern.

**F5 — Cross-binding cannot be proven by output this run.** Oracle and package
engine are behaviorally identical (precondition), so a cross-bound differential
still returns GREEN. The 2c demo needs a structural discriminator (module identity
/ `__file__` / sentinel). The Gemini focus line adds a scenario the task never
specifies ("no cross-binding when an engine directory is MOVED") — align 2c or the
reviewer will test something the seat never built.

**F6 — Set-sha1 completeness needs a named ground truth.** Re-verification catches
tamper-after-snapshot trivially; the §5 residual is a shallow copy AT CREATION,
which only an independent completeness source catches (source-dir re-walk vs
snapshot, or an expected-module list). No set-sha1 construct exists anywhere yet
(the split ledger is a line-slice provenance record, not a content-hash manifest);
prior art for set-copying is the harness's `_infra` loop (lines 846–848), which
already encodes the `__pycache__`/.pyc exclusion lesson.

Secondary (unchanged from the pre-evidence review): where the 2c demo lives
(retained test vs scratch evidence); whether a harness-side lazy-import scan is
prudent tooling or PART 3b by the back door — needs a ruling; the Gemini REVISE
handback mechanism is the one input the run prompt must still name; the relay
limit for `.partN` splitting is unnamed anywhere (observed precedent: parts of
5–23 KB relay safely); "previous harness recoverable (Box versioning)" is not
testable by the drafting seat — it is a property of the applier's landing step;
HARD RULES' ban on "saved to Box" claims is letter-vs-intent friction with
deliverables that are, in fact, Box uploads — followable, but a phrasing tripwire.

---

## 4. Review items closed by evidence

- **Header sha1s**: all 17 full 40-hex values recovered from Box file metadata and
  verified (`STAGED-INPUTS-full.sha1`). Truncated 8-hex headers are house
  convention (predecessor brief identical); Box metadata carries the authoritative
  full values, so run-time verification never depends on download fidelity.
- **Relay fidelity**: the Box MCP download path proved byte-exact (the fetched
  64,501 B harness hashed to `a3e678f2…` exactly). One manual-transcription hazard
  observed and caught by the sha1 gate: trailing blank lines invisible in fetched
  displays.
- **Staging mechanics**: staging is a server-side byte-exact Box copy; the
  tier-split → harness-fix `l1lint/` copies are 12/12 sha1-identical — the live,
  discipline-only precedent PART 1 formalizes. The staged brief names the exact
  per-run folder pair in its STAGED-INTO line at staging time (the predecessor's
  did, including a do-not-touch list); the draft's placeholder is normal draft
  state, refreshed by JR at staging — which also answers the stale-header risk.
- **Exchange topology**: this seat's Box root IS the exchange view; per-run
  input/output sibling pairs beside `inbox/`, `method/`, `outbox/`; the parent
  Max-Drafting-Exchange folder (402946233341) is intentionally unreachable from
  the seat (Box cannot nest new folders inside an already-shared folder — only the
  children are shared).
- **Gemini materials**: the standing 04 instructions and CODE-CHANGE template are
  not seat-visible anywhere in the exchange (every folder enumerated) — the relay
  is JR-side.
- **§5 residual source**: "§5" is the harness's own differential section number;
  the residual discussion lives in the reconcile REVIEW-FEED (Box 2370091760939).
- **Known open questions already on record** (do not rediscover in-run): the
  fixture-count observation (docstring "34" vs 35 FIXTURES ids, FX01–FX37 with
  gaps); the infra-sabotage copy-list review flag in the shim header.

## 5. Confirmations vs the pre-evidence review

The pre-evidence review's two top predicted first-attempt failures (literal
snapshot set → exit 3; missing runner privilege requirement) are both confirmed
and hereby pre-empted. Remaining likely first-attempt errors, in order: vacuous
cross-binding proof by output equality; sys.modules save/restore leaks between
engine loads; treating set-sha1 re-verification alone as the 1c completeness
check; running gates in the wrong directory (the stale repo monolith also reports
89/89 — a path mixup is invisible in the headline number).
