# -*- coding: utf-8 -*-
"""l1lint.cli - argument parsing, mode dispatch and exit codes (thin CLI layer)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 1823-1948.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import argparse
import json
import os
import sys

from .checks import CHECKS
from .dochygiene import DOCHYG_ALL_DOCS, run_dochygiene_checks
from .engine import action_items, report
from .hygiene import run_hygiene_checks
from .loader import INIT_EXIT, InitError, _load_baseline
from .pins import run_pin_checks
from .selftest import _emit_fixture, selftest
from .xdoc import (LIVE_SHA_NAMES, PIN_SHA_NAMES, XDOC_CHECKS, XDOC_DOC_NAMES,
                   run_xdoc_checks)


def _parse_named_values(pairs, what, allowed):
    """869dtn48p CLI plumbing: parse repeatable NAME=VALUE args into a dict, strictly —
    malformed / unknown-name / duplicate entries raise ValueError (surfaced as a CLI-usage
    error, argparse exit 2)."""
    out = {}
    for spec in pairs or []:
        name, sep, val = spec.partition("=")
        if not sep or not name or not val:
            raise ValueError(f"{what} expects NAME=VALUE, got {spec!r}")
        if name not in allowed:
            raise ValueError(f"{what} name {name!r} not one of {sorted(allowed)}")
        if name in out:
            raise ValueError(f"duplicate {what} for {name!r}")
        out[name] = val
    return out


# ============================================================================
def main(argv=None):
    p = argparse.ArgumentParser(description="Layer 1 adaptive doc-linter (offline/deterministic)")
    p.add_argument("pointer", nargs="?", help="path to the pointer .md")
    p.add_argument("--selftest", action="store_true", help="run the hermetic known-bad fixtures")
    p.add_argument("--emit-fixtures", metavar="DIR", help="write known-bad variants (from baseline.md) to DIR")
    p.add_argument("--json", action="store_true", help="emit the ClickUp action-items feed (STEP 4)")
    p.add_argument("--doc", action="append", metavar="NAME=PATH",
                   help="869dtn48p: sovereign-doc copy to cross-check (NAME: gate_v|rules|tag_use|charter; repeatable)")
    p.add_argument("--live-sha", action="append", metavar="NAME=SHA1", dest="live_sha",
                   help="869dtn48p: live server-side sha1 for NAME (connected-seat input; repeatable)")
    p.add_argument("--comments-dump", metavar="PATH", dest="comments_dump",
                   help="869dwncba: JSON [{task_id, comments:[{id?,text}|str]}] for the recommend-only comment-hygiene scan")
    p.add_argument("--audit-dump", metavar="PATH", dest="audit_dump",
                   help="869dwncba: JSON [{task_id, name}] audit-list dump for the duplicate-CR-seq check")
    args = p.parse_args(argv)

    # 869dtn48p: strict parse of the cross-doc inputs; doc files are read as RAW BYTES (sha1-exact
    # for gate_v; X01 decodes utf-8/replace for ID harvest). Unreadable file = CLI-usage error.
    try:
        doc_paths = _parse_named_values(args.doc, "--doc", XDOC_DOC_NAMES)
        live_shas = _parse_named_values(args.live_sha, "--live-sha", LIVE_SHA_NAMES)
    except ValueError as e:
        p.error(str(e))
    docs = {}
    for name, path in doc_paths.items():
        try:
            with open(path, "rb") as fh:
                docs[name] = fh.read()
        except OSError as e:
            p.error(f"--doc {name}: cannot read {path!r}: {type(e).__name__}: {e}")
    xdoc_active = bool(docs) or bool(live_shas)

    # 869dwncba: hygiene dumps read as raw bytes; JSON validity is a CHECK concern (clean R01/R02
    # FAIL on malformed JSON), only unreadability is a CLI-usage error.
    dumps = {}
    for label, path in (("comments", args.comments_dump), ("audit", args.audit_dump)):
        if path is None:
            dumps[label] = None
            continue
        try:
            with open(path, "rb") as fh:
                dumps[label] = fh.read()
        except OSError as e:
            p.error(f"--{label}-dump: cannot read {path!r}: {type(e).__name__}: {e}")
    hyg_active = dumps["comments"] is not None or dumps["audit"] is not None
    dochyg_active = any(n in docs for n in DOCHYG_ALL_DOCS)   # 869dtn4e2: same --doc inputs
    pin_active = any(n in live_shas for n in PIN_SHA_NAMES)   # 869e5m1nd/869dxa4gy

    # baseline-dependent modes may hit a lazy init-failure -> clean exit 3 (F2), never a traceback.
    try:
        if args.selftest:
            return selftest(emit_dir=args.emit_fixtures)

        if args.emit_fixtures:
            from test_layer1_lint import FIXTURES
            base = _load_baseline()
            for fid, desc, mutate, expected in FIXTURES:
                _emit_fixture(args.emit_fixtures, fid, mutate(base))
            print(f"emitted {len(FIXTURES)} fixtures (from baseline.md) to {args.emit_fixtures}")
            if not args.pointer:
                return 0
    except InitError as e:
        sys.stderr.write(f"INIT-FAILURE: {e}\n")
        return INIT_EXIT

    if not args.pointer:
        p.error("a pointer .md path is required (or use --selftest)")
    try:
        with open(args.pointer, encoding="utf-8") as fh:
            text = fh.read()
    except UnicodeDecodeError as e:
        # Phase B defect fix (1): a non-UTF-8 pointer is a clean C00 FAIL, never an uncaught
        # traceback. STRICTLY UnicodeDecodeError (F3): IsADirectoryError / PermissionError (both
        # OSError subclasses, NOT UnicodeDecodeError) are NOT caught here, so they keep the
        # oracle's exact uncaught-crash behaviour. Routed through report()/action_items() with a
        # precomputed C00 result so the output format is identical to any other C00 FAIL.
        c00 = {"C00": (False, CHECKS["C00"][0],
                       f"structural parse failed: {type(e).__name__}: {e}")}
        xdoc = (({"X00": (False, XDOC_CHECKS["X00"],
                          f"pointer parse failed: {type(e).__name__}: {e}")}, [])
                if xdoc_active else None)
        hyg = (run_hygiene_checks(dumps["comments"], dumps["audit"])
               if hyg_active else None)             # hygiene needs no pointer text — still runs
        dochyg = (run_dochygiene_checks(None, docs)
                  if dochyg_active else None)       # doc-local checks run; H02 fails closed
        pin = run_pin_checks(None, live_shas) if pin_active else None   # P02 fails closed
        if args.json:
            feed = action_items(None, results=c00, xdoc=xdoc, hyg=hyg, dochyg=dochyg, pin=pin)
            print(json.dumps(feed, indent=2))
            return feed["exit"]
        rpt, code = report(None, target=args.pointer, results=c00,
                           nbytes=os.path.getsize(args.pointer), xdoc=xdoc, hyg=hyg,
                           dochyg=dochyg, pin=pin)
        print(rpt)
        return code

    xdoc = run_xdoc_checks(text, docs, live_shas) if xdoc_active else None
    hyg = run_hygiene_checks(dumps["comments"], dumps["audit"]) if hyg_active else None
    dochyg = run_dochygiene_checks(text, docs) if dochyg_active else None
    pin = run_pin_checks(text, live_shas) if pin_active else None
    if args.json:
        feed = action_items(text, xdoc=xdoc, hyg=hyg, dochyg=dochyg, pin=pin)
        print(json.dumps(feed, indent=2))
        return feed["exit"]

    rpt, code = report(text, target=args.pointer, xdoc=xdoc, hyg=hyg, dochyg=dochyg, pin=pin)
    print(rpt)
    return code
