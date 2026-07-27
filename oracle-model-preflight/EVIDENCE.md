# Preflight evidence — raw transcripts (2026-07-27, Fable pre-execution seat)

All runs executed against a scratch stage reassembled from the exchange and
verified byte-exact BEFORE any gate ran: every file matched the full 40-hex sha1
recorded in Box file metadata (see `STAGED-INPUTS-full.sha1`; `shasum -c` → 17/17
OK). The engine, oracle, manifest and baseline are byte-identical to the governed
copies in `harness-fix-inputs/` (Box); the harness is the reconciled a3e678f2.
Stated as CLAIMS from this seat; the applier's independent re-run is the proof.

## Environment

    uid                  0 (root)
    python3              3.11.15
    PyYAML               6.0.1
    privilege drop       sudo -u nobody   (available, used for the green runs)

Root reads through chmod 000 (probe: os.chmod(f,0) then open(f).read() succeeds).

## Gate 1 — engine selftest (in stage dir)

    $ python3 layer1_lint.py --selftest
    ...
    SELF-TEST RESULT: 89/89 fixtures correct (exact failing-set match); baseline clean -> PASS
    exit=0

## Gate 2 — differential Phase A as ROOT (fails by environment, not by change)

    $ python3 test_layer1_lint.py --phase A
    ...
    OVERALL Phase A: FAIL  (determinism=True, registry_config_errors=0,
      content_fail=0, file/infra_fail=1, slow=0, property_flags=0)

The single failure is `infra:manifest-chmod000` (expects exit 3 +
"PermissionError"; as root the chmod-000 manifest stays readable, sha1 verifies,
the engine inits normally → `BAD rc=0`). Matches the reconcile REVIEW-FEED's
RUNTIME NOTE verbatim: "differential phases run as an UNPRIVILEGED user
(uid 65534 `nobody`) — required for the chmod-000 cases; as root they fail
loudly (`BAD rc=0`, observed)". Note: a `phaseA_exit=0` line in this seat's first
transcript was the tail-pipe's exit status, not the harness verdict — the OVERALL
line is authoritative.

## Gate 3 — both phases as NOBODY (the documented runner) — GREEN

    runner: sudo -u nobody

    OVERALL Phase A: PASS  (determinism=True, registry_config_errors=0,
      content_fail=0, file/infra_fail=0, slow=0, property_flags=0)
    phaseA_nobody_exit=0

    OVERALL Phase B: PASS  (determinism=True, registry_config_errors=0,
      content_fail=0, file/infra_fail=0, slow=0, property_flags=0)
    phaseB_nobody_exit=0

Zero declared deltas in both phases (PHASEB registries empty), fuzz corpus at the
default N=1100. This reproduces the brief's PRECONDITION in full — selftest 89/89
plus differential A/B green, zero deltas — under the unprivileged runner only.

## Demo 1 — the brief's literal PART-1 set ("shim + l1lint/") as a snapshot

    $ cp stage/layer1_lint.py snap_literal/ && cp -r stage/l1lint snap_literal/l1lint
    $ cd snap_literal && python3 layer1_lint.py --selftest
    INIT-FAILURE: manifest unreadable (<snap_literal>/manifest.yaml):
      FileNotFoundError: [Errno 2] No such file or directory: '<snap_literal>/manifest.yaml'
    exit=3

The named set cannot init from its own directory: loader.py resolves
manifest.yaml/baseline.md engine-dir-relative and loads the manifest at import
(sys.exit(3) on failure).

## Demo 2 — full closure minus test_layer1_lint.py

    $ cd snap_noharness && python3 layer1_lint.py --selftest
    ...
      File ".../l1lint/selftest.py", line 40, in selftest
        from test_layer1_lint import (FIXTURES, XDOC_FIXTURES, XDOC_FIXTURES2, HYG_FIXTURES,
    ModuleNotFoundError: No module named 'test_layer1_lint'
    exit=1  (raw traceback — outside the F2 no-traceback taxonomy)

## Demo 3 — in-process import of the incomplete engine (what the differential sees)

    $ python3 -c "spec_from_file_location + exec_module on snap_literal/layer1_lint.py"
    INIT-FAILURE: engine package 'l1lint' not importable beside layer1_lint.py
      (ModuleNotFoundError: No module named 'l1lint') - incomplete installation;
      the modular engine ships as layer1_lint.py + l1lint/ + manifest.yaml +
      baseline.md + test_layer1_lint.py
    -> exec_module raised SystemExit(code=3)

Same snapshot as Demo 1, different failure PATH (package-missing fallback, not the
manifest pin) purely because the working directory differed — and the SystemExit
propagates through the harness's unguarded `_import`.

## Source-verified facts (file:line, package = harness-fix-inputs/l1lint/)

- loader.py: `_HERE = dirname(dirname(abspath(__file__)))`; MANIFEST_PATH/BASELINE_PATH
  joined to `_HERE`; module-level `_load_manifest()` in try/except → `sys.exit(3)`.
  Top-level fail-closed `try: import yaml / except ImportError: exit(2)`.
- Lazy imports of the harness (the only function-level imports in the engine):
  selftest.py::selftest() (`from test_layer1_lint import (FIXTURES, …)`) and
  cli.py::main() emit-fixtures branch (`from test_layer1_lint import FIXTURES`).
  Verbatim in the frozen monolith a87ce510 at lines 1622 and 1895 (grep-verified
  against the byte-verified repo mirror copy).
- All l1lint-internal imports in all 12 modules are module-top-level (full read).
- Reconciled harness a3e678f2: ORACLE_PATH fixed at HERE (line 28); only
  L1_NEW_ENGINE overridable (line 31); `_import` = spec_from_file_location +
  exec_module with no SystemExit/ImportError guard (lines 488–494); engines
  imported lazily with the documented reason — the engine's selftest import of
  the harness must stay side-effect-free (lines 497–498); no sys.path writes
  anywhere; in-process comparison is the content corpus only (run_checks — pure,
  no call-time imports); subprocess runner `run_subproc` (lines 572–577) covers
  file/crash/infra corpora; `_infra` copies the module set excluding
  `__pycache__`/.pyc/.pyo (lines 846–852); PHASEB delta registries empty
  (lines 732–733); "Only after Phase B is green is the outgoing engine preserved
  as the new oracle" (line 720).
- split_ledger.json (tier-split-outputs): line-slice provenance ledger; records
  exactly one non-verbatim substitution — the loader `_HERE` re-base, "baseline.md/
  manifest.yaml stay resolved beside layer1_lint.py exactly as before". No
  content-hash set manifest exists anywhere in the exchange.
- Copy-fidelity precedent: tier-split-outputs/l1lint/ and harness-fix-inputs/
  l1lint/ are sha1-identical 12/12 (server-side Box copy staging).

## Box locations referenced (seat-visible exchange)

    harness-fix-inputs/            403377656532   (engine set + oracle + brief)
    harness-fix-inputs/l1lint/     403378035625   (12 modules, sha1s in manifest file)
    harness-fix-outputs/           403378041254   (reconciled harness a3e678f2,
                                                   HARNESS-CHANGE-MAP.md,
                                                   REVIEW-FEED.md 2370091760939 —
                                                   §5 residual + nobody RUNTIME NOTE)
    outbox/tier-split-outputs/     403285566973   (split ledger, MODULE-MAP, shim)
    method/                        402947258288   (Drafting Engine v3, Adversarial
                                                   Chamber v1.3 — no Gemini docs
                                                   anywhere seat-visible)
