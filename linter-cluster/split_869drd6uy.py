#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""869drd6uy splitter — deterministic generator of the l1lint modular package from the
frozen layer1_lint.py monolith (sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7).

Method: every module body is a VERBATIM line-slice of the monolith (byte-exact by
construction); only generated docstring headers and import lines are new text. Exactly ONE
in-slice substitution is applied (the _HERE path anchor, re-based from the module file to the
entrypoint directory) — asserted to occur exactly once and recorded in the ledger.

Outputs: the package files + shim, plus split_ledger.json (the MODULE-MAP source of truth).
Line accounting: every line 1..1953 of the monolith must land in >=1 slice or be an
explicitly whitelisted blank separator — anything else aborts.
"""
import hashlib
import json
import os
import sys

SRC = "/home/user/temp/linter-cluster/layer1_lint.py"
OUT = "/home/user/temp/linter-cluster"
PKG = os.path.join(OUT, "l1lint")
EXPECT_SHA1 = "a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7"

raw = open(SRC, "rb").read()
got = hashlib.sha1(raw).hexdigest()
assert got == EXPECT_SHA1, f"monolith sha1 {got} != pinned {EXPECT_SHA1} — refusing to split"
text = raw.decode("utf-8")
lines = text.split("\n")            # monolith ends with trailing newline -> last element ""
assert lines[-1] == "" and len(lines) == 1954, f"unexpected line structure: {len(lines)}"
L = lines[:-1]                       # L[0] is line 1 ... L[1952] is line 1953


def sl(a, b):
    """Verbatim slice of monolith lines a..b inclusive (1-indexed)."""
    return "\n".join(L[a - 1:b])


HDR = '# -*- coding: utf-8 -*-\n"""{doc}\n\nVerbatim relocation from the frozen v0.2.8 monolith layer1_lint.py\n(sha1 {sha}), lines {ranges}.\nNo check logic altered - see MODULE-MAP.md for the exact move ledger.\n"""\n'

MODULES = [
    # (relpath, one-line role, [import lines], [(start, end), ...], [(old, new, why)])
    ("l1lint/loader.py",
     "l1lint.loader - pins, floors, bounded YAML loader, sha1-pinned artifact loads "
     "(engine core: the YAML load path + init-failure contract F2)",
     [],                                    # slice already begins with the monolith's own imports
     [(40, 216)],
     [("_HERE = os.path.dirname(os.path.abspath(__file__))",
       "_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
       "path anchor re-based: module now lives in l1lint/, one level below the entrypoint; "
       "baseline.md/manifest.yaml stay resolved beside layer1_lint.py exactly as before")]),
    ("l1lint/parsing.py",
     "l1lint.parsing - pointer document parsing + tree-walk helpers shared by every check family",
     ["import re",
      "",
      "from .loader import LONGID_RE, UUID_FIND_RE, bounded_safe_load"],
     [(218, 305)], []),
    ("l1lint/checks.py",
     "l1lint.checks - the C00-C13 core check family, the check registry (CHECKS), the clause "
     "manifest (CLAUSE_MANIFEST) and the coverage tripwire (engine core)",
     ["import re",
      "",
      "from .loader import (CANONICAL_PRECEDENCE, CONTEXTUAL_PROSE_IDS, IMMUTABLE_DOCS,",
      "                     LONGID_RE, NUMERIC_THRESHOLD_KEYS, REQUIRED_DROPZONE_IDS,",
      "                     REQUIRED_NEVERWRITE_IDS, SHA1_RE, UUID_FIND_RE, UUID_RE)",
      "from .parsing import _auth_values, _box_id_set, _box_zone, parsed_id_pool, walk_ids"],
     [(307, 761)], []),
    ("l1lint/org_mirror.py",
     "l1lint.org_mirror - ORGANISATIONAL-layer definitions isolated per the 869drd6uy "
     "structuring guideline: the 869dx7xpc coverage map + org-mirror structural conventions. "
     "The forthcoming org-instructions/Layer-1 governance split localises here. The X04/X05 "
     "orchestration that consumes these stays verbatim inside xdoc.run_xdoc_checks (pure "
     "refactor: extracting it would alter call-frame shape); flagged as the follow-on cut line",
     ["import re"],
     [(777, 797)], []),
    ("l1lint/xdoc.py",
     "l1lint.xdoc - 869dtn48p cross-doc coherence family (X00-X05) incl. the 869dx7xpc "
     "org-mirror checks X04/X05 (constants isolated in l1lint.org_mirror)",
     ["import hashlib",
      "",
      "from .loader import (CONTEXTUAL_PROSE_IDS, GATE_V_PIN, GATE_V_VERSION_EXPECTED,",
      "                     InitError, LONGID_RE, ORG_MIRROR_RECORD, SHA1_RE, UUID_FIND_RE,",
      "                     _validate_org_mirror_record)",
      "from .org_mirror import ORG_MIRROR_STRUCTURE",
      "from .parsing import load_data, parsed_id_pool, split_doc"],
     [(763, 775), (799, 947)], []),
    ("l1lint/pins.py",
     "l1lint.pins - 869e5m1nd/869dxa4gy pin / baseline-currency family (P01-P02, recommend-only) "
     "incl. the item7-REV1 gate_v double-isinstance guard (engine core: pin-check family)",
     ["from .loader import BASELINE_SHA1, SHA1_RE",
      "from .parsing import load_data, split_doc"],
     [(950, 1039)], []),
    ("l1lint/dochygiene.py",
     "l1lint.dochygiene - 869dtn4e2 static-doc hygiene family (H01-H04, supplied-doc offline checks)",
     ["import re",
      "",
      "from .loader import LONGID_RE",
      "from .parsing import load_data, split_doc"],
     [(1042, 1251)], []),
    ("l1lint/hygiene.py",
     "l1lint.hygiene - 869dwncba ClickUp hygiene family (R01-R02, recommend-only, dump-fed)",
     ["import json",
      "import re"],
     [(1254, 1366)], []),
    ("l1lint/engine.py",
     "l1lint.engine - the runner: run_checks orchestration, the STEP-4 action-items feed and "
     "the human-readable report (engine core)",
     ["from .checks import CHECKS, CLAUSE_MANIFEST, coverage_tripwire",
      "from .dochygiene import DOCHYG_CHECKS, DOCHYG_CLAUSES",
      "from .hygiene import HYGIENE_CHECKS, HYGIENE_CLAUSES",
      "from .loader import VERSION",
      "from .org_mirror import COVERAGE_MAP",
      "from .parsing import load_data, split_doc",
      "from .pins import PIN_CHECKS, PIN_CLAUSES",
      "from .xdoc import XDOC_CHECKS, XDOC_CLAUSES"],
     [(1369, 1599)], []),
    ("l1lint/selftest.py",
     "l1lint.selftest - the hermetic --selftest driver (external fixtures from "
     "test_layer1_lint.py, sha1-pinned baseline)",
     ["import os",
      "",
      "from .checks import CLAUSE_MANIFEST, coverage_tripwire",
      "from .dochygiene import DOCHYG_CHECKS, DOCHYG_CLAUSES, run_dochygiene_checks",
      "from .engine import run_checks",
      "from .hygiene import HYGIENE_CHECKS, HYGIENE_CLAUSES, run_hygiene_checks",
      "from .loader import (InitError, MANIFEST_TIER, MANIFEST_TIERS, _load_baseline,",
      "                     _validate_tier)",
      "from .pins import PIN_CHECKS, PIN_CLAUSES, run_pin_checks",
      "from .xdoc import XDOC_CHECKS, XDOC_CLAUSES, run_xdoc_checks"],
     [(1602, 1820)], []),
    ("l1lint/cli.py",
     "l1lint.cli - argument parsing, mode dispatch and exit codes (thin CLI layer)",
     ["import argparse",
      "import json",
      "import os",
      "import sys",
      "",
      "from .checks import CHECKS",
      "from .dochygiene import DOCHYG_ALL_DOCS, run_dochygiene_checks",
      "from .engine import action_items, report",
      "from .hygiene import run_hygiene_checks",
      "from .loader import INIT_EXIT, InitError, _load_baseline",
      "from .pins import run_pin_checks",
      "from .selftest import _emit_fixture, selftest",
      "from .xdoc import (LIVE_SHA_NAMES, PIN_SHA_NAMES, XDOC_CHECKS, XDOC_DOC_NAMES,",
      "                   run_xdoc_checks)"],
     [(1823, 1948)], []),
]

# blank separator lines deliberately not carried into any module (all must be whitespace-only)
DROPPED = [217, 306, 762, 776, 798, 948, 949, 1040, 1041, 1252, 1253,
           1367, 1368, 1600, 1601, 1821, 1822, 1949, 1950]

# ---- re-export groups for the shim: every top-level monolith binding, by owning module ----
REEXPORTS = [
    ("l1lint.loader",
     "VERSION, INIT_EXIT, IMMUTABLE_DOCS, NUMERIC_THRESHOLD_KEYS, CONTEXTUAL_PROSE_IDS, "
     "UUID_RE, SHA1_RE, LONGID_RE, UUID_FIND_RE, _HERE, BASELINE_PATH, MANIFEST_PATH, "
     "BASELINE_SHA1, MANIFEST_SHA1, MANIFEST_TIERS, InitError, YAML_MAX_BYTES, "
     "YAML_ALIAS_BUDGET, BoundedLoadError, bounded_safe_load, _read_pinned, _validate_tier, "
     "_validate_org_mirror_record, _load_manifest, _load_baseline, REQUIRED_NEVERWRITE_IDS, "
     "REQUIRED_DROPZONE_IDS, CANONICAL_PRECEDENCE, GATE_V_PIN, GATE_V_VERSION_EXPECTED, "
     "MANIFEST_TIER, ORG_MIRROR_RECORD"),
    ("l1lint.parsing",
     "split_doc, load_data, walk_ids, parsed_id_pool, _box_zone, _box_id_set, _auth_values"),
    ("l1lint.checks",
     "_coerced_long_ids, c01_ids_quoted, c02_prose_ids_in_yaml, "
     "c03_writable_neverwrite_disjoint, c04_precedence_order, c05_failsafe_overrides, "
     "c06_mutability_partition, c07_jr_pattern, _classify_id, _classify_sha, "
     "c08_pointed_docs_resolve, c10_neverwrite_category, c11_dropzone_integrity, "
     "c12_zone_shapes, c13_schema_limits_guard, _c00_sentinel, CHECKS, CLAUSE_MANIFEST, "
     "coverage_tripwire"),
    ("l1lint.org_mirror", "COVERAGE_MAP, ORG_MIRROR_STRUCTURE"),
    ("l1lint.xdoc",
     "XDOC_DOC_NAMES, XDOC_ID_DOCS, XDOC_SHA_CONSUMERS, PIN_SHA_NAMES, LIVE_SHA_NAMES, "
     "XDOC_CHECKS, XDOC_CLAUSES, run_xdoc_checks"),
    ("l1lint.pins", "DEPLOYED_POINTER_ID, PIN_CHECKS, PIN_CLAUSES, run_pin_checks"),
    ("l1lint.dochygiene",
     "DOCHYG_VERSION_DOCS, DOCHYG_CLAIM_DOCS, DOCHYG_CEILING_DOCS, DOCHYG_AUTHORITY_DOCS, "
     "DOCHYG_ALL_DOCS, _V_RE, _CHANGELOG_SEC_RE, _EDITABLE_CLAIM_RE, _IMMUTABLE_CLAIM_RE, "
     "DOC_PREC_ANCHORS, _AUTH_GRANT_RE, _THRESHOLD_DEF_RE, _NEVERWRITE_WORD_RE, "
     "DOCHYG_CHECKS, DOCHYG_CLAUSES, _doc_text, _header_version, _changelog_versions, "
     "_authority_definition_lines, _precedence_restatement_errs, run_dochygiene_checks"),
    ("l1lint.hygiene",
     "HYGIENE_MARKERS, CR_SEQ_RE, HYGIENE_CHECKS, HYGIENE_CLAUSES, _parse_dump, "
     "run_hygiene_checks"),
    ("l1lint.engine", "run_checks, action_items, report"),
    ("l1lint.selftest", "_emit_fixture, _failed_set, selftest"),
    ("l1lint.cli", "_parse_named_values, main"),
]

SHIM_NOTE = """\
# ============================================================================
# 869drd6uy TIER-ENGINE MODULAR SPLIT (2026-07-26) - ENTRYPOINT SHIM
# The v0.2.8 engine logic now lives, verbatim, in the l1lint/ package beside this
# file (see MODULE-MAP.md). This shim preserves the exact public surface and the
# exact invocation (`python3 layer1_lint.py ...`): it re-exports every top-level
# name the monolith defined and delegates execution to l1lint.cli.main.
# Import of l1lint.loader below runs the manifest floor-load at import time,
# exactly as the monolith did (INIT-FAILURE + exit 3 on a bad/missing manifest,
# before argparse - contract F2 unchanged).
# FAIL-CLOSED FALLBACK: if the l1lint package itself is missing/unreadable beside
# this file (an incomplete installation - e.g. the entrypoint copied without the
# package), this is treated as an init failure: INIT-FAILURE + exit 3, never a
# traceback. NOTE (review flag): the differential harness's infra-sabotage cases
# copy only layer1_lint.py + manifest.yaml + baseline.md (+ test module) into an
# isolated dir; under the split they exit 3 via THIS fallback rather than via the
# manifest/baseline sha1 checks those cases originally exercised. The sha1-pin
# init checks themselves are unchanged (loader.py) and are exercised by every
# in-place run; see REVIEW-FEED.md OPEN QUESTIONS.
# ============================================================================
"""


def build_shim():
    parts = [sl(1, 46), "", SHIM_NOTE.rstrip("\n"), "try:"]
    for mod, names in REEXPORTS:
        nl = [n.strip() for n in names.split(",")]
        line = f"    from {mod} import ("
        out, cur = [], line
        for i, n in enumerate(nl):
            tok = n + (", " if i < len(nl) - 1 else ")")
            if len(cur) + len(tok) > 99:
                out.append(cur.rstrip())
                cur = "        " + tok
            else:
                cur += tok
        out.append(cur)
        parts.extend(out)
    parts.extend([
        "except ImportError as _imp_e:",
        "    sys.stderr.write(f\"INIT-FAILURE: engine package 'l1lint' not importable beside \"",
        "                     f\"layer1_lint.py ({type(_imp_e).__name__}: {_imp_e}) - incomplete \"",
        "                     f\"installation; the modular engine ships as layer1_lint.py + \"",
        "                     f\"l1lint/ + manifest.yaml + baseline.md + test_layer1_lint.py\\n\")",
        "    sys.exit(3)   # INIT_EXIT: package-missing is an init failure (F2 contract, fail-closed)",
        "",
        "",
        sl(1951, 1953),
    ])
    return "\n".join(parts) + "\n"


def build_module(doc, imports, slices, subs):
    ranges = ", ".join(f"{a}-{b}" for a, b in slices)
    body_parts = [sl(a, b) for a, b in slices]
    body = "\n\n\n".join(body_parts)
    for old, new, _why in subs:
        assert body.count(old) == 1, f"substitution anchor not unique: {old!r}"
        body = body.replace(old, new)
    head = HDR.format(doc=doc, sha=EXPECT_SHA1, ranges=ranges)
    imp = ("\n".join(imports) + "\n\n\n") if imports else ""
    return head + imp + body + "\n"


# ---- line accounting ----
covered = set()
for _p, _d, _i, slices, _s in MODULES:
    for a, b in slices:
        covered.update(range(a, b + 1))
covered.update(range(1, 47))          # shim head
covered.update(range(1951, 1954))     # shim tail
for n in DROPPED:
    assert L[n - 1].strip() == "", f"dropped line {n} is not blank: {L[n-1]!r}"
    covered.add(n)
missing = [n for n in range(1, 1954) if n not in covered]
assert not missing, f"unassigned monolith lines: {missing}"

# ---- emit ----
os.makedirs(PKG, exist_ok=True)
ledger = {"monolith_sha1": EXPECT_SHA1, "monolith_lines": 1953, "files": [],
          "dropped_blank_separators": DROPPED,
          "substitutions": []}

init_doc = ('# -*- coding: utf-8 -*-\n"""l1lint - the Layer 1 doc-linter engine as a modular '
            'package (869drd6uy split of the\nfrozen v0.2.8 monolith, sha1 '
            f'{EXPECT_SHA1}).\n\nEntrypoint and public surface: the layer1_lint.py shim beside '
            'this package (invocation\nunchanged). Import layering (DAG): loader -> parsing -> '
            '{checks, xdoc(+org_mirror), pins,\ndochygiene, hygiene} -> engine -> selftest -> '
            'cli. Importing any submodule triggers the\nmanifest floor-load in l1lint.loader, '
            'exactly as importing the monolith did (F2:\nINIT-FAILURE + exit 3 on a '
            'missing/tampered manifest).\n"""\n')
written = [("l1lint/__init__.py", init_doc)]

for relpath, doc, imports, slices, subs in MODULES:
    written.append((relpath, build_module(doc, imports, slices, subs)))
    for old, new, why in subs:
        ledger["substitutions"].append({"file": relpath, "old": old, "new": new, "why": why})

written.append(("layer1_lint.py", build_shim()))

for relpath, content in written:
    path = os.path.join(OUT, relpath)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)

for relpath, doc, imports, slices, subs in MODULES:
    ledger["files"].append({"file": relpath, "slices": [[a, b] for a, b in slices],
                            "generated": "docstring header + import block only"})
ledger["files"].append({"file": "layer1_lint.py",
                        "slices": [[1, 46], [1951, 1953]],
                        "generated": "split note + full re-export block + fail-closed package fallback"})
ledger["files"].append({"file": "l1lint/__init__.py", "slices": [],
                        "generated": "package docstring only"})

with open(os.path.join(OUT, "split_ledger.json"), "w", encoding="utf-8") as fh:
    json.dump(ledger, fh, indent=2)

print("generated files:")
for relpath, _c in written:
    p = os.path.join(OUT, relpath)
    b = open(p, "rb").read()
    print(f"  {relpath:24s} {len(b):7d} B  sha1 {hashlib.sha1(b).hexdigest()}")
print("ledger: split_ledger.json")
print("OK")
