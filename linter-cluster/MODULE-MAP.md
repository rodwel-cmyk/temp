# MODULE-MAP — 869drd6uy tier-engine modular split (2026-07-26)

## Ground truth
The frozen v0.2.8 monolith `layer1_lint.py`, sha1 `a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7`,
107,222 B / 1,953 lines — staged as `inbox/tier-split-inputs/layer1_lint.py` (Box id
2369300366102) and byte-identical `oracle_layer1_lint.py` (Box id 2369300584087); the
same bytes are preserved in-repo as `linter-cluster/oracle_layer1_lint.py`.

## Method
The split is **generated, not retyped**: `split_869drd6uy.py` slices the pinned monolith
into verbatim line-ranges (byte-exact module bodies by construction), prepends a generated
docstring header + import block per module, and applies exactly ONE in-slice substitution
(the `_HERE` path anchor, below). The generator asserts the monolith's sha1 before cutting,
asserts every dropped separator line is blank, and accounts for all 1,953 lines. Re-running
the generator against the pinned monolith reproduces this module set byte-for-byte
(`split_ledger.json` is its machine-readable output).

## What moved where

| new file | monolith lines (verbatim) | bytes | sha1 |
|---|---|---:|---|
| `layer1_lint.py` | 1-46, 1951-1953 | 7,118 | `79db9696e92d6320bd909c1f621fc531caefed6a` |
| `l1lint/__init__.py` | (generated) | 589 | `ffcc84384fbc969e7373d79eaf98705aec9ab2a7` |
| `l1lint/loader.py` | 40-216 | 10,088 | `e753dd158ecf840264f347a8fd701ea39b5d3810` |
| `l1lint/parsing.py` | 218-305 | 3,717 | `af3289953daaffb5b1ccc14d03714dfe0d8f648f` |
| `l1lint/checks.py` | 307-761 | 26,631 | `2b21e531ce1b97a49aaf08faa7836561dbd635a4` |
| `l1lint/org_mirror.py` | 777-797 | 2,018 | `da11d42f916e9275c8c564d836f96e4d3153ec6d` |
| `l1lint/xdoc.py` | 763-775, 799-947 | 11,055 | `53c6d212873123f7b5d9d186c422e88ea6ac17a3` |
| `l1lint/pins.py` | 950-1039 | 6,232 | `a658517293c218aa950f45b54ad81e9c1615186c` |
| `l1lint/dochygiene.py` | 1042-1251 | 11,350 | `6e82c80abd0e5ae0c8e9496ef107321a3967106b` |
| `l1lint/hygiene.py` | 1254-1366 | 6,825 | `4032a64b30d3df63c6acc06c676fbf6c23d46a5e` |
| `l1lint/engine.py` | 1369-1599 | 13,213 | `1a8e16fa7effb7d04ec9ef231bb8259c0560c202` |
| `l1lint/selftest.py` | 1602-1820 | 12,332 | `e65c0d558c5f7457aea3eafdc4415285a9396815` |
| `l1lint/cli.py` | 1823-1948 | 7,535 | `b1fc79f470ebbe88b7e29f5a1f9e2fdf3005f425` |

Module set total: 118,703 B across 13 files; largest module
l1lint/checks.py at 26,631 B (bound: no module over ~40 KB — met).
Entrypoint `layer1_lint.py`: 107,222 B -> 7,118 B.

Roles:
- `layer1_lint.py` — entrypoint shim: monolith docstring + stdlib/yaml guard (verbatim), full re-export of all 114 top-level names, fail-closed package fallback, `__main__` guard (verbatim)
- `l1lint/__init__.py` — package docstring only (no imports, no side effects of its own)
- `l1lint/loader.py` — engine core — pins, floors, contract constants, regexes, InitError, 869dthz60 bounded YAML loader, sha1-pinned manifest/baseline loads, import-time floor load (F2)
- `l1lint/parsing.py` — pointer parsing + tree-walk helpers (split_doc, load_data, id pools, zone helpers)
- `l1lint/checks.py` — engine core — C01-C13 check family, C00 sentinel, CHECKS registry, CLAUSE_MANIFEST, coverage_tripwire
- `l1lint/org_mirror.py` — ORGANISATIONAL layer (isolated per the structuring guideline): 869dx7xpc COVERAGE_MAP + ORG_MIRROR_STRUCTURE anchors
- `l1lint/xdoc.py` — 869dtn48p cross-doc family X00-X05 (incl. 869dx7xpc X04/X05 orchestration, verbatim)
- `l1lint/pins.py` — engine core — 869e5m1nd/869dxa4gy pin/baseline-currency family P01-P02 (incl. the item7-REV1 gate_v double-isinstance guard)
- `l1lint/dochygiene.py` — 869dtn4e2 static-doc hygiene family H01-H04
- `l1lint/hygiene.py` — 869dwncba ClickUp hygiene family R01-R02 (recommend-only, dump-fed)
- `l1lint/engine.py` — engine core — runner: run_checks, action_items (STEP-4 feed), report
- `l1lint/selftest.py` — hermetic --selftest driver (external fixtures, sha1-pinned baseline)
- `l1lint/cli.py` — thin CLI: _parse_named_values + main (argparse, mode dispatch, exit codes)

## Line accounting
- Monolith lines 1-46 (shebang, coding, module docstring, stdlib imports + PyYAML guard) and
  1951-1953 (`__main__` guard incl. its banner) are carried **verbatim in the shim**; lines
  40-46 also open `l1lint/loader.py` verbatim (the package must be import-safe standalone).
- Every other line lands in exactly one module per the table above.
- Dropped lines (all verified blank inter-section separators):
  [217, 306, 762, 776, 798, 948, 949, 1040, 1041, 1252, 1253, 1367, 1368, 1600, 1601, 1821, 1822, 1949, 1950].

## The single in-slice substitution
`l1lint/loader.py`:
- old: `_HERE = os.path.dirname(os.path.abspath(__file__))`
- new: `_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`
- why: path anchor re-based: module now lives in l1lint/, one level below the entrypoint; baseline.md/manifest.yaml stay resolved beside layer1_lint.py exactly as before

Effect: `BASELINE_PATH`/`MANIFEST_PATH` resolve beside the entrypoint exactly as the
monolith resolved them — verified by the copied-layout init-failure demos in REVIEW-FEED.

## Generated (new) text — exhaustive list
1. Per-module docstring headers + import blocks (imports only re-bind names the monolith
   already had in scope at those lines; no new dependencies, stdlib + PyYAML only, unchanged).
2. `l1lint/__init__.py` (docstring only).
3. The shim's split-note comment block, full re-export block (all 114 monolith top-level
   bindings, incl. underscore names, so any attribute-level consumer sees the identical
   surface), and the fail-closed package fallback (`INIT-FAILURE` + exit 3 if `l1lint/` is
   not importable beside the entrypoint — F2-consistent, never a traceback).
No check body, constant value, message string, registry entry, clause text, or output line
was edited. `VERSION` remains "0.2.8" (self-reported version prints into the report header;
a bump would be an output delta).

## Import graph (DAG, no cycles)
loader -> parsing -> {checks, xdoc (+ org_mirror), pins, dochygiene, hygiene} -> engine
-> selftest -> cli -> (shim re-exports everything; `__main__` guard calls `main`).
Importing any submodule triggers the manifest floor-load in `loader` at import time,
exactly as importing the monolith did (INIT-FAILURE + exit 3 before argparse on a
missing/tampered manifest).

## Invocation
Unchanged: `python3 layer1_lint.py [POINTER.md] [--json | --selftest | --emit-fixtures DIR |
--doc NAME=PATH | --live-sha NAME=HEX | --comments-dump PATH | --audit-dump PATH]`.
Exit codes unchanged (0/1/2/3). The engine now ships as the module SET
(layer1_lint.py + l1lint/ + manifest.yaml + baseline.md + test_layer1_lint.py co-located).
