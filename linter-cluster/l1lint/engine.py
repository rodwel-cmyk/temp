# -*- coding: utf-8 -*-
"""l1lint.engine - the runner: run_checks orchestration, the STEP-4 action-items feed and the human-readable report (engine core)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 1369-1599.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
from .checks import CHECKS, CLAUSE_MANIFEST, coverage_tripwire
from .dochygiene import DOCHYG_CHECKS, DOCHYG_CLAUSES
from .hygiene import HYGIENE_CHECKS, HYGIENE_CLAUSES
from .loader import VERSION
from .org_mirror import COVERAGE_MAP
from .parsing import load_data, split_doc
from .pins import PIN_CHECKS, PIN_CLAUSES
from .xdoc import XDOC_CHECKS, XDOC_CLAUSES


# ============================================================================
# Runner
# ============================================================================
def run_checks(text):
    """Run every registered check and return {cid: (ok, label, detail)}.
    C00 (structural parse) is run FIRST and INSIDE this function's guard: split_doc + load_data
    (which calls yaml.safe_load) can raise on a malformed pointer. Previously they ran outside the
    per-check try/except, so a bad pointer threw an uncaught traceback (worst case: it crashed the
    --json STEP-4 feed instead of emitting a clean FAIL). Now a parse failure is a single clean C00
    FAIL and short-circuits (data is unavailable, so the data-dependent checks cannot run); a good
    parse records C00:(True, ...) so C00 is ALWAYS present in the results."""
    c00_label = CHECKS["C00"][0]
    try:
        yaml_text, prose = split_doc(text)
        data = load_data(yaml_text)
    except Exception as e:                           # malformed pointer -> clean single FAIL
        return {"C00": (False, c00_label,
                        f"structural parse failed: {type(e).__name__}: {e}")}
    results = {"C00": (True, c00_label, "pointer parses into a layer1_data mapping")}
    for cid, (label, fn) in CHECKS.items():
        if cid == "C00":
            continue                                 # already produced above (parse gate)
        try:
            ok, detail = fn(prose, data)
        except Exception as e:                       # a malformed pointer is a clean FAIL,
            ok, detail = False, f"check crashed: {type(e).__name__}: {e}"   # never a traceback
        results[cid] = (ok, label, detail)
    return results


def action_items(text, results=None, xdoc=None, hyg=None, dochyg=None, pin=None):
    """STEP 4 feed (issue-tracker pattern). Returns the list of human-action items
    keyed by a STABLE finding-id, for an idempotent ClickUp upsert by the seat.
    Clean run -> [] (no tasks for clean runs). The linter does NOT write ClickUp
    itself here; it emits the feed and the seat upserts read-before-update.
    `results` may be a precomputed run_checks() map (used by main()'s Phase-B read-error path to
    render a C00 FAIL without text); default None preserves the exact normal behaviour.
    `xdoc` (869dtn48p) is an optional (xdoc_results, skipped) pair — its FAILs join the feed
    with the same item shape; default None keeps the feed byte-identical to v0.2.8.
    `hyg` (869dwncba) is the same for the recommend-only hygiene family — its items carry
    kind "recommendation" so the STEP-4 consumer can route them as extraction candidates."""
    results = run_checks(text) if results is None else results
    cov_ok, cov_lines = coverage_tripwire()
    items = []
    for cid in sorted(results):
        ok, label, detail = results[cid]
        if not ok:
            items.append({"finding_id": f"L1LINT-{cid}", "kind": "inconsistency",
                          "check": cid, "summary": label, "detail": detail})
    if not cov_ok:
        for ln in cov_lines:
            if "UNCOVERED" in ln or "ORPHAN" in ln:
                items.append({"finding_id": "L1LINT-COVERAGE", "kind": "uncovered_rule",
                              "summary": "coverage tripwire fired", "detail": ln.strip()})
    xdoc_ok = True
    if xdoc is not None:
        xresults, _xskipped = xdoc
        xcov_ok, xcov_lines = coverage_tripwire(manifest=XDOC_CLAUSES, checks=XDOC_CHECKS)
        for xid in sorted(xresults):
            ok, label, detail = xresults[xid]
            if not ok:
                items.append({"finding_id": f"L1LINT-{xid}", "kind": "inconsistency",
                              "check": xid, "summary": label, "detail": detail})
        if not xcov_ok:
            for ln in xcov_lines:
                if "UNCOVERED" in ln or "ORPHAN" in ln:
                    items.append({"finding_id": "L1LINT-XDOC-COVERAGE", "kind": "uncovered_rule",
                                  "summary": "xdoc coverage tripwire fired", "detail": ln.strip()})
        xdoc_ok = all(r[0] for r in xresults.values()) and xcov_ok
    hyg_ok = True
    if hyg is not None:
        hresults, _hskipped = hyg
        hcov_ok, hcov_lines = coverage_tripwire(manifest=HYGIENE_CLAUSES, checks=HYGIENE_CHECKS)
        for rid in sorted(hresults):
            ok, label, detail = hresults[rid]
            if not ok:
                items.append({"finding_id": f"L1LINT-{rid}", "kind": "recommendation",
                              "check": rid, "summary": label, "detail": detail})
        if not hcov_ok:
            for ln in hcov_lines:
                if "UNCOVERED" in ln or "ORPHAN" in ln:
                    items.append({"finding_id": "L1LINT-HYG-COVERAGE", "kind": "uncovered_rule",
                                  "summary": "hygiene coverage tripwire fired", "detail": ln.strip()})
        hyg_ok = all(r[0] for r in hresults.values()) and hcov_ok
    dochyg_ok = True
    if dochyg is not None:
        dresults, _dskipped = dochyg
        dcov_ok, dcov_lines = coverage_tripwire(manifest=DOCHYG_CLAUSES, checks=DOCHYG_CHECKS)
        for hid in sorted(dresults):
            ok, label, detail = dresults[hid]
            if not ok:
                items.append({"finding_id": f"L1LINT-{hid}", "kind": "inconsistency",
                              "check": hid, "summary": label, "detail": detail})
        if not dcov_ok:
            for ln in dcov_lines:
                if "UNCOVERED" in ln or "ORPHAN" in ln:
                    items.append({"finding_id": "L1LINT-DOCHYG-COVERAGE", "kind": "uncovered_rule",
                                  "summary": "doc-hygiene coverage tripwire fired", "detail": ln.strip()})
        dochyg_ok = all(r[0] for r in dresults.values()) and dcov_ok
    pin_ok = True
    if pin is not None:
        presults, _pskipped = pin
        pcov_ok, pcov_lines = coverage_tripwire(manifest=PIN_CLAUSES, checks=PIN_CHECKS)
        for pid in sorted(presults):
            ok, label, detail = presults[pid]
            if not ok:
                items.append({"finding_id": f"L1LINT-{pid}", "kind": "recommendation",
                              "check": pid, "summary": label, "detail": detail})
        if not pcov_ok:
            for ln in pcov_lines:
                if "UNCOVERED" in ln or "ORPHAN" in ln:
                    items.append({"finding_id": "L1LINT-PIN-COVERAGE", "kind": "uncovered_rule",
                                  "summary": "pin coverage tripwire fired", "detail": ln.strip()})
        pin_ok = all(r[0] for r in presults.values()) and pcov_ok
    overall = (all(r[0] for r in results.values()) and cov_ok and xdoc_ok and hyg_ok
               and dochyg_ok and pin_ok)
    return {"result": "PASS" if overall else "FAIL",
            "exit": 0 if overall else 1,
            "action_items": items,          # -> ClickUp tasks (idempotent by finding_id)
            # RESERVED FOR STEP-3: the (designed, not-yet-built) advisory proposer will populate
            # this with candidate normative clauses for JR to ratify into CLAUSE_MANIFEST. Kept as
            # an empty list so the feed schema is stable for the seat's STEP-4 consumer today.
            "proposed_checks": []}


def report(text, target="<pointer>", results=None, nbytes=None, xdoc=None, hyg=None, dochyg=None, pin=None):
    # `results`/`nbytes` default None -> identical to the normal path; the Phase-B read-error
    # path passes a precomputed C00 result + the raw byte count (text is unavailable then).
    # `xdoc` (869dtn48p) default None -> byte-identical default report; when supplied it is the
    # (xdoc_results, skipped) pair and a CROSS-DOC section is appended before RESULT.
    # `hyg` (869dwncba) same pattern: the recommend-only CLICKUP HYGIENE section.
    # `dochyg` (869dtn4e2) same pattern: the STATIC-DOC HYGIENE section.
    # `pin` (869e5m1nd/869dxa4gy) same pattern: the PIN / BASELINE-CURRENCY section.
    results = run_checks(text) if results is None else results
    cov_ok, cov_lines = coverage_tripwire()
    out = []
    out.append(f"LAYER 1 ADAPTIVE DOC-LINTER v{VERSION} — RUN REPORT  (offline/deterministic)")
    out.append(f"  target : {target}")
    out.append(f"  bytes  : {len(text.encode('utf-8')) if nbytes is None else nbytes}")
    out.append("")
    out.append("CHECKS (derived from the pointer YAML data block):")
    checks_ok = True
    for cid in sorted(results):
        ok, label, detail = results[cid]
        tag = "PASS" if ok else "FAIL"
        if not ok:
            checks_ok = False
        out.append(f"  [{tag}] {cid} {label}")
        out.append(f"         -> {detail}")
    out.append("")
    out.append("COVERAGE TRIPWIRE (every normative clause must map to >=1 check):")
    out.extend(cov_lines)
    out.append(f"  => {'PASS' if cov_ok else 'FAIL'}")
    out.append("")
    xdoc_ok = True
    if xdoc is not None:
        xresults, xskipped = xdoc
        xcov_ok, xcov_lines = coverage_tripwire(manifest=XDOC_CLAUSES, checks=XDOC_CHECKS)
        out.append("CROSS-DOC CHECKS (869dtn48p — supplied-input family):")
        out.append("  coverage map (869dx7xpc): "
                   + "; ".join(f"{n} -> {c}" for n, c in COVERAGE_MAP))
        for xid in sorted(xresults):
            ok, label, detail = xresults[xid]
            if not ok:
                xdoc_ok = False
            out.append(f"  [{'PASS' if ok else 'FAIL'}] {xid} {label}")
            out.append(f"         -> {detail}")
        for note in xskipped:
            out.append(f"  [note] {note}")
        out.append("XDOC COVERAGE (family clauses):")
        out.extend(xcov_lines)
        out.append(f"  => {'PASS' if xcov_ok else 'FAIL'}")
        out.append("")
        xdoc_ok = xdoc_ok and xcov_ok
    hyg_ok = True
    if hyg is not None:
        hresults, hskipped = hyg
        hcov_ok, hcov_lines = coverage_tripwire(manifest=HYGIENE_CLAUSES, checks=HYGIENE_CHECKS)
        out.append("CLICKUP HYGIENE CHECKS (869dwncba — recommend-only; reads supplied dumps, never live):")
        for rid in sorted(hresults):
            ok, label, detail = hresults[rid]
            if not ok:
                hyg_ok = False
            out.append(f"  [{'PASS' if ok else 'FAIL'}] {rid} {label}")
            out.append(f"         -> {detail}")
        for note in hskipped:
            out.append(f"  [note] {note}")
        out.append("HYGIENE COVERAGE (family clauses):")
        out.extend(hcov_lines)
        out.append(f"  => {'PASS' if hcov_ok else 'FAIL'}")
        out.append("")
        hyg_ok = hyg_ok and hcov_ok
    dochyg_ok = True
    if dochyg is not None:
        dresults, dskipped = dochyg
        dcov_ok, dcov_lines = coverage_tripwire(manifest=DOCHYG_CLAUSES, checks=DOCHYG_CHECKS)
        out.append("STATIC-DOC HYGIENE CHECKS (869dtn4e2 — tier-1 offline, supplied docs):")
        for hid in sorted(dresults):
            ok, label, detail = dresults[hid]
            if not ok:
                dochyg_ok = False
            out.append(f"  [{'PASS' if ok else 'FAIL'}] {hid} {label}")
            out.append(f"         -> {detail}")
        for note in dskipped:
            out.append(f"  [note] {note}")
        out.append("DOC-HYGIENE COVERAGE (family clauses):")
        out.extend(dcov_lines)
        out.append(f"  => {'PASS' if dcov_ok else 'FAIL'}")
        out.append("")
        dochyg_ok = dochyg_ok and dcov_ok
    pin_ok = True
    if pin is not None:
        presults, pskipped = pin
        pcov_ok, pcov_lines = coverage_tripwire(manifest=PIN_CLAUSES, checks=PIN_CHECKS)
        out.append("PIN / BASELINE-CURRENCY CHECKS (869e5m1nd + 869dxa4gy — recommend-only; live sha1s are connected-seat inputs):")
        for pid in sorted(presults):
            ok, label, detail = presults[pid]
            if not ok:
                pin_ok = False
            out.append(f"  [{'PASS' if ok else 'FAIL'}] {pid} {label}")
            out.append(f"         -> {detail}")
        for note in pskipped:
            out.append(f"  [note] {note}")
        out.append("PIN COVERAGE (family clauses):")
        out.extend(pcov_lines)
        out.append(f"  => {'PASS' if pcov_ok else 'FAIL'}")
        out.append("")
        pin_ok = pin_ok and pcov_ok
    overall = checks_ok and cov_ok and xdoc_ok and hyg_ok and dochyg_ok and pin_ok
    out.append(f"RESULT: {'PASS (exit 0)' if overall else 'FAIL (exit 1)'}")
    return "\n".join(out), (0 if overall else 1)
