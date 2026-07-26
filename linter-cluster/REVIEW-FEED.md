# REVIEW-FEED — 869drd6uy tier-engine modular split (2026-07-26)

Factual evidence only. The Gemini CODE-CHANGE review template + standing 04 instructions
govern the review itself; nothing here proposes review criteria or conclusions.

## (a) GROUND TRUTH
- Frozen engine (monolith): `layer1_lint.py` v0.2.8, sha1 `a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7`,
  107,222 B / 1,953 lines. Staged input Box id 2369300366102; byte-identical oracle Box id
  2369300584087; preserved in-repo as `linter-cluster/oracle_layer1_lint.py` (same sha1,
  verified before and after the split).
- Pinned companions (verified against the session-header pins AND Box server-side sha1s
  before work started): `test_layer1_lint.py` `31d74400b7a9f9064a49f0ea52ff8df3f485e39a`
  (54,983 B, FROZEN — not modified); `manifest.yaml`
  `0397bfd11cfe8023aa7eb4808681d0bd598ddad3` (3,748 B, unmodified);
  `baseline.md` `dd5da45a1f93963c6f1c381e9dcd292f6f79333d` (48,992 B, unmodified);
  `LINTER-CLUSTER-SPECS-full.md` `06f29ebf097903916edebc5016e0965c0c7c861a`.
- Interpreter: Python 3.11.15 (same for oracle and split in every comparison; the harness
  asserts interpreter parity).

## (b) OUTPUT
The modular file-set (bytes + sha1 per file — MODULE-MAP.md carries the same table with
the per-file monolith line-ranges as the unified move ledger):

| file | bytes | sha1 |
|---|---:|---|
| `layer1_lint.py` | 7,118 | `79db9696e92d6320bd909c1f621fc531caefed6a` |
| `l1lint/__init__.py` | 589 | `ffcc84384fbc969e7373d79eaf98705aec9ab2a7` |
| `l1lint/loader.py` | 10,088 | `e753dd158ecf840264f347a8fd701ea39b5d3810` |
| `l1lint/parsing.py` | 3,717 | `af3289953daaffb5b1ccc14d03714dfe0d8f648f` |
| `l1lint/checks.py` | 26,631 | `2b21e531ce1b97a49aaf08faa7836561dbd635a4` |
| `l1lint/org_mirror.py` | 2,018 | `da11d42f916e9275c8c564d836f96e4d3153ec6d` |
| `l1lint/xdoc.py` | 11,055 | `53c6d212873123f7b5d9d186c422e88ea6ac17a3` |
| `l1lint/pins.py` | 6,232 | `a658517293c218aa950f45b54ad81e9c1615186c` |
| `l1lint/dochygiene.py` | 11,350 | `6e82c80abd0e5ae0c8e9496ef107321a3967106b` |
| `l1lint/hygiene.py` | 6,825 | `4032a64b30d3df63c6acc06c676fbf6c23d46a5e` |
| `l1lint/engine.py` | 13,213 | `1a8e16fa7effb7d04ec9ef231bb8259c0560c202` |
| `l1lint/selftest.py` | 12,332 | `e65c0d558c5f7457aea3eafdc4415285a9396815` |
| `l1lint/cli.py` | 7,535 | `b1fc79f470ebbe88b7e29f5a1f9e2fdf3005f425` |

Companion artifacts: `MODULE-MAP.md` (move ledger), `split_ledger.json` (machine-readable),
`split_869drd6uy.py` (the deterministic generator — re-runnable against the pinned monolith
for byte-exact reproduction), `diff_phaseA.log.txt` (full differential transcript),
`selftest_split_transcript.txt` (89/89 run).

## (c) CHANGE-MANIFEST — structural only, zero behaviour change
- Every module body is a verbatim line-slice of the pinned monolith (ranges in MODULE-MAP).
- New text is confined to: module docstring headers, import blocks, the package
  `__init__.py` docstring, and the entrypoint shim (re-exports + fail-closed fallback).
- Exactly one in-slice substitution: the `_HERE` anchor in `l1lint/loader.py`
  (`dirname(abspath(__file__))` -> `dirname(dirname(abspath(__file__)))`) so
  manifest/baseline resolve beside the entrypoint as before.
- Zero edits to: check bodies, constants, floors, regexes, message strings, registry
  entries, clause manifests, report/feed formats, exit codes, `VERSION` ("0.2.8").
- `test_layer1_lint.py`, `manifest.yaml`, `baseline.md`: untouched (sha1s above).
- No new dependency; no new parse/loader surface (the 869dthz60 bounded loader is the same
  code, same module-load path); no network; no writes.

## (d) VERIFICATION — first-pass CLAIMS (the applier re-runs these independently; this is
## not the gate)
1. `python3 layer1_lint.py --selftest` -> **89/89 PASS, exit 0**; stdout AND stderr
   byte-identical to `oracle_layer1_lint.py --selftest`.
2. Oracle differential, **Phase A (100% equivalence), full corpus** — 34 fixtures +
   structured/fence/edge cases + 1,100 seeded fuzz mutations, each compared across
   non-json stdout (exact bytes), --json payload (parsed), per-check failing-sets,
   coverage tripwire, exit codes; K=3 determinism; subprocess file/crash cases; infra
   sabotage; property bounds:
   - STABLE (identical run-to-run)
   - CONTENT+FUZZ equivalence: 1151/1151 as-expected (51 structured + 1100 fuzz)
   - **OVERALL Phase A: PASS** (determinism=True, content_fail=0, file/infra_fail=0, slow=0, property_flags=0)
   - file/crash/infra case lines:
     [OK] file:nonutf8[text]: identical
     [OK] file:nonutf8[json]: identical
     [OK] file:isadir[text]: identical
     [OK] file:isadir[json]: identical
     [OK] file:perm[text]: identical
     [OK] file:perm[json]: identical
     [OK] infra:manifest-deleted: exit3+INIT-FAILURE  | INIT-FAILURE: engine package 'l1lint' not importable beside layer1_lint.py (ModuleNotFoundError: No module named 'l1lint') - incomplete installation; the modula
     [OK] infra:manifest-chmod000: exit3+INIT-FAILURE  | INIT-FAILURE: engine package 'l1lint' not importable beside layer1_lint.py (ModuleNotFoundError: No module named 'l1lint') - incomplete installation; the modula
     [OK] infra:baseline-sha1-corrupt: exit3+INIT-FAILURE  | INIT-FAILURE: engine package 'l1lint' not importable beside layer1_lint.py (ModuleNotFoundError: No module named 'l1lint') - incomplete installation; the modula
     [OK] infra:baseline-crlf-rewrite: exit3+INIT-FAILURE  | INIT-FAILURE: engine package 'l1lint' not importable beside layer1_lint.py (ModuleNotFoundError: No module named 'l1lint') - incomplete installation; the modula
   - property bounds (F6 wall_time < 2 s):
     5MB-garbage[oracle]: 9 ms  ok
     5MB-garbage[new]: 6 ms  ok
     alias-bomb[oracle]: 94 ms  ok
     alias-bomb[new]: 65 ms  ok
3. CLI parity battery (split vs oracle, byte-compared; stderr via the harness's own
   normaliser): lint text mode, --json mode, --doc/--live-sha battery (text + json),
   --emit-fixtures (35-file trees identical), nonexistent-pointer traceback path —
   all IDENTICAL. argparse usage-error stderr differs ONLY by continuation-line
   indentation, which argparse derives from the PROG NAME length
   (`oracle_layer1_lint.py` vs `layer1_lint.py`); control experiment (monolith bytes
   run under the name `layer1_lint.py`) reproduces the split's output byte-exactly ->
   filename artifact, not a split delta.
4. Init-failure contract (F2) demos, split layout WITH package co-located:
   manifest deleted -> exit 3 `INIT-FAILURE: manifest unreadable`; manifest byte-appended ->
   exit 3 sha1 mismatch; baseline byte-appended + --selftest -> exit 3 sha1 mismatch.
   All no-traceback. (Proves the pin machinery is intact and the re-based `_HERE` resolves
   in copied layouts.)
5. Zero declared deltas: no behavioural difference was found in any comparison above, and
   none is declared. Any output difference = failure of this refactor, per the session brief.

## OPEN QUESTIONS / RISKS
1. **Infra-sabotage cases exercise a different init path under the split.** The frozen
   harness copies only `layer1_lint.py + manifest.yaml + baseline.md (+ test module)` into
   an isolated dir — the l1lint package is not in its copy list — so those four cases now
   exit 3 via the shim's fail-closed package fallback (`INIT-FAILURE: engine package
   'l1lint' not importable...`) rather than via the manifest/baseline sha1 checks they
   originally exercised. The harness assertions (exit 3 + INIT-FAILURE + no traceback)
   pass either way, and item 4 above exercises the original pin paths directly. Follow-on
   suggestion for ratification: extend the harness's infra copy list with `l1lint/` so the
   sabotage cases exercise the pin paths again (harness change — outside this pure refactor).
2. **Org-isolation judgment call.** The structuring guideline asks for the org_mirror
   family isolated in its own module. Isolated into `l1lint/org_mirror.py`: the 869dx7xpc
   COVERAGE_MAP + ORG_MIRROR_STRUCTURE definitions (what the forthcoming governance split
   would edit). The X04/X05 orchestration REMAINS verbatim inside `run_xdoc_checks`
   (`l1lint/xdoc.py`): extracting it into a cross-module helper would change call-frame
   shape/source structure beyond a pure move, so it is flagged as the natural follow-on cut
   line instead. Anything keyed to `org_instructions` inside C04/C10 vocabulary is
   inseparable from those checks' verbatim bodies and moved with them (`l1lint/checks.py`).
3. **Deployment unit changed.** The entrypoint alone is no longer the whole engine: the
   module SET (layer1_lint.py + l1lint/ + manifest.yaml + baseline.md +
   test_layer1_lint.py, co-located) is the deployable artifact. Per-file sha1s above.
   Embedding note: `import l1lint` resolves via the entrypoint's directory on `sys.path`
   (script runs and the harness's importlib load both satisfy this); a foreign embedder
   must have the cluster directory on `sys.path`.
4. **argparse usage indentation** is prog-name-length-dependent (pre-existing argparse
   behaviour, demonstrated above; invisible to the harness, which never compares
   argparse-usage stderr).
5. Verified on Python 3.11.15 only (matching the venue + harness parity assertion).
