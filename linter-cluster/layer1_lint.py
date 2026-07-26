#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer 1 ADAPTIVE doc-linter — v0.2.8 (split engine, 2026-06-19)
==============================================================
Deterministic, READ-ONLY, OFFLINE consistency gate for the Cowork/Teams Layer 1 pointer.

This is the SPLIT engine: the audited v0.2.8 logic, byte-for-byte unchanged, with three
artifacts externalised so the engine source drops below the 50 KB inline threshold and the
floors become partition-ready (scope-tagged, org-default):
  * baseline.md          — the frozen v3.1 pointer snapshot (was the embedded FROZEN_BASELINE);
                           sha1-pinned + verified at load. Used ONLY by --selftest / --emit-fixtures.
  * manifest.yaml        — the C04 precedence + C10 never-write floor + C11 drop-zone floor +
                           GATE-V pin, lifted into a declarative file; sha1-pinned + verified at
                           load and PROJECTED to the exact native primitives C00-C13 expect
                           (flat sets/list of id-STRINGS; scope/tier metadata never enters set-math).
  * test_layer1_lint.py  — the 34 known-bad fixtures + the differential harness.

869drd6uy: manifest v1.1 adds a top-level `tier:` declaration (org|personal|project) — the
forward-compat hook for the tier-aware ENGINE/POLICY/SCOPE split. Validated fail-closed at load,
exposed as MANIFEST_TIER; C00-C13 semantics UNCHANGED (full cross-tier engine = flagged follow-on).

Init-failure contract (F2): a missing / unreadable / sha1-mismatched (incl. a CRLF rewrite)
baseline or manifest aborts with a dedicated INIT-FAILURE message and exit code 3 — never a
traceback, never a C00-C13 verdict, and distinct from argparse's native exit 2 for CLI-usage errors.

The check semantics, registry, clause manifest, coverage tripwire and runner are the v0.2.8
oracle's, unchanged. VERSION stays "0.2.8" on purpose: the self-reported version prints into the
report header, so a bump would be an output delta — behaviour preservation includes output.

READ-ONLY / OFFLINE / DETERMINISTIC / never-crashes-on-a-malformed-pointer, as before.
exit 0 = clean, 1 = lint FAIL, 2 = CLI-usage error (argparse), 3 = init-failure (F2).

Usage:
  layer1_lint.py POINTER.md                 # lint the pointer (default)
  layer1_lint.py POINTER.md --json          # emit the ClickUp action-items feed (STEP 4)
  layer1_lint.py --selftest                 # run the hermetic known-bad fixtures (loads baseline.md)
  layer1_lint.py --emit-fixtures DIR        # write the known-bad variants (from baseline.md) to DIR
"""
import sys, os, re, json, argparse, hashlib

try:
    import yaml
except ImportError:
    sys.stderr.write("FATAL: PyYAML required (pip install pyyaml)\n")
    sys.exit(2)

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
try:
    from l1lint.loader import (VERSION, INIT_EXIT, IMMUTABLE_DOCS, NUMERIC_THRESHOLD_KEYS,
        CONTEXTUAL_PROSE_IDS, UUID_RE, SHA1_RE, LONGID_RE, UUID_FIND_RE, _HERE, BASELINE_PATH,
        MANIFEST_PATH, BASELINE_SHA1, MANIFEST_SHA1, MANIFEST_TIERS, InitError, YAML_MAX_BYTES,
        YAML_ALIAS_BUDGET, BoundedLoadError, bounded_safe_load, _read_pinned, _validate_tier,
        _validate_org_mirror_record, _load_manifest, _load_baseline, REQUIRED_NEVERWRITE_IDS,
        REQUIRED_DROPZONE_IDS, CANONICAL_PRECEDENCE, GATE_V_PIN, GATE_V_VERSION_EXPECTED,
        MANIFEST_TIER, ORG_MIRROR_RECORD)
    from l1lint.parsing import (split_doc, load_data, walk_ids, parsed_id_pool, _box_zone,
        _box_id_set, _auth_values)
    from l1lint.checks import (_coerced_long_ids, c01_ids_quoted, c02_prose_ids_in_yaml,
        c03_writable_neverwrite_disjoint, c04_precedence_order, c05_failsafe_overrides,
        c06_mutability_partition, c07_jr_pattern, _classify_id, _classify_sha,
        c08_pointed_docs_resolve, c10_neverwrite_category, c11_dropzone_integrity,
        c12_zone_shapes, c13_schema_limits_guard, _c00_sentinel, CHECKS, CLAUSE_MANIFEST,
        coverage_tripwire)
    from l1lint.org_mirror import (COVERAGE_MAP, ORG_MIRROR_STRUCTURE)
    from l1lint.xdoc import (XDOC_DOC_NAMES, XDOC_ID_DOCS, XDOC_SHA_CONSUMERS, PIN_SHA_NAMES,
        LIVE_SHA_NAMES, XDOC_CHECKS, XDOC_CLAUSES, run_xdoc_checks)
    from l1lint.pins import (DEPLOYED_POINTER_ID, PIN_CHECKS, PIN_CLAUSES, run_pin_checks)
    from l1lint.dochygiene import (DOCHYG_VERSION_DOCS, DOCHYG_CLAIM_DOCS, DOCHYG_CEILING_DOCS,
        DOCHYG_AUTHORITY_DOCS, DOCHYG_ALL_DOCS, _V_RE, _CHANGELOG_SEC_RE, _EDITABLE_CLAIM_RE,
        _IMMUTABLE_CLAIM_RE, DOC_PREC_ANCHORS, _AUTH_GRANT_RE, _THRESHOLD_DEF_RE,
        _NEVERWRITE_WORD_RE, DOCHYG_CHECKS, DOCHYG_CLAUSES, _doc_text, _header_version,
        _changelog_versions, _authority_definition_lines, _precedence_restatement_errs,
        run_dochygiene_checks)
    from l1lint.hygiene import (HYGIENE_MARKERS, CR_SEQ_RE, HYGIENE_CHECKS, HYGIENE_CLAUSES,
        _parse_dump, run_hygiene_checks)
    from l1lint.engine import (run_checks, action_items, report)
    from l1lint.selftest import (_emit_fixture, _failed_set, selftest)
    from l1lint.cli import (_parse_named_values, main)
except ImportError as _imp_e:
    sys.stderr.write(f"INIT-FAILURE: engine package 'l1lint' not importable beside "
                     f"layer1_lint.py ({type(_imp_e).__name__}: {_imp_e}) - incomplete "
                     f"installation; the modular engine ships as layer1_lint.py + "
                     f"l1lint/ + manifest.yaml + baseline.md + test_layer1_lint.py\n")
    sys.exit(3)   # INIT_EXIT: package-missing is an init failure (F2 contract, fail-closed)


# ============================================================================
if __name__ == "__main__":
    sys.exit(main())
