# -*- coding: utf-8 -*-
"""l1lint.selftest - the hermetic --selftest driver (external fixtures from test_layer1_lint.py, sha1-pinned baseline)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 1602-1820.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import os

from .checks import CLAUSE_MANIFEST, coverage_tripwire
from .dochygiene import DOCHYG_CHECKS, DOCHYG_CLAUSES, run_dochygiene_checks
from .engine import run_checks
from .hygiene import HYGIENE_CHECKS, HYGIENE_CLAUSES, run_hygiene_checks
from .loader import (InitError, MANIFEST_TIER, MANIFEST_TIERS, _load_baseline,
                     _validate_tier)
from .pins import PIN_CHECKS, PIN_CLAUSES, run_pin_checks
from .xdoc import XDOC_CHECKS, XDOC_CLAUSES, run_xdoc_checks


# ============================================================================
# Self-test driver (fixtures live in test_layer1_lint.py — loaded externally, §3.1).
# Runs the 34 known-bad mutations against the sha1-pinned baseline.md and asserts the
# EXACT failing-set per fixture, exactly as the v0.2.8 oracle's embedded self-test did.
# ============================================================================
def _emit_fixture(emit_dir, fid, text):
    """The single fixture-file emitter, shared by --selftest --emit-fixtures and the
    standalone --emit-fixtures path so the two cannot drift."""
    os.makedirs(emit_dir, exist_ok=True)
    with open(os.path.join(emit_dir, fid + ".md"), "w", encoding="utf-8") as fh:
        fh.write(text)


def _failed_set(results):
    """The set of check-ids that FAILED in a run_checks() result map."""
    return frozenset(cid for cid, (ok, _l, _d) in results.items() if not ok)


def selftest(emit_dir=None):
    # external fixtures (§3.1 + 869dtn48p + 869dx7xpc + 869dwncba + 869dtn4e2)
    from test_layer1_lint import (FIXTURES, XDOC_FIXTURES, XDOC_FIXTURES2, HYG_FIXTURES,
                                  DH_FIXTURES, PN_FIXTURES)
    clean_text = _load_baseline()                # sha1-pinned frozen baseline (was FROZEN_BASELINE)
    print(f"SELF-TEST (HERMETIC — sha1-pinned baseline.md, v3.7 / etag-16 snapshot)")
    print(f"  baseline bytes: {len(clean_text.encode('utf-8'))}")
    print(f"  manifest tier : {MANIFEST_TIER} (v1.1 schema hook, 869drd6uy)\n")

    base_results = run_checks(clean_text)
    base_cov_ok, _ = coverage_tripwire()
    base_clean = all(r[0] for r in base_results.values()) and base_cov_ok
    print(f"  [{'OK' if base_clean else 'BROKEN'}] frozen baseline lints clean "
          f"({sum(1 for r in base_results.values() if r[0])}/{len(base_results)} checks + tripwire)")
    if not base_clean:
        for cid, (ok, label, detail) in sorted(base_results.items()):
            if not ok:
                print(f"           BASELINE FAIL {cid}: {detail}")

    passed = 0
    # pointer fixtures + tripwire + tier-schema + xdoc fixtures (both tables) + xdoc tripwire
    # + the org-mirror confidentiality fixture + hygiene fixtures + hygiene tripwire
    # + doc-hygiene fixtures + doc-hygiene tripwire
    total = (len(FIXTURES) + 2 + len(XDOC_FIXTURES) + len(XDOC_FIXTURES2) + 1 + 1
             + len(HYG_FIXTURES) + 1 + len(DH_FIXTURES) + 1 + len(PN_FIXTURES) + 1)
    print()
    for fid, desc, mutate, expected in FIXTURES:
        try:
            bad_text = mutate(clean_text)
            if emit_dir:
                _emit_fixture(emit_dir, fid, bad_text)
            results = run_checks(bad_text)
            failed = _failed_set(results)
            ok = (failed == expected)
            detail = (f"failed={sorted(failed)} == expected"
                      if ok else f"failed={sorted(failed)} != expected={sorted(expected)}")
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        status = "OK" if ok else "BAD"
        if ok:
            passed += 1
        verb = "stay clean" if not expected else f"FAIL exactly {sorted(expected)}"
        print(f"  [{status}] {fid}: {desc}")
        print(f"           expected to {verb} -> {detail}")

    inj = dict(CLAUSE_MANIFEST)
    inj["L99"] = ("DELIBERATELY UNCOVERED normative rule", [])
    cov_ok, _ = coverage_tripwire(manifest=inj)
    trip_caught = not cov_ok
    if trip_caught:
        passed += 1
    print(f"  [{'OK' if trip_caught else 'BAD'}] FXCOV-uncovered-rule: a clause with no mapped check")
    print(f"           expected coverage tripwire to FAIL -> {'fired' if trip_caught else 'did NOT fire'}")

    # 869drd6uy tier-schema self-check: exercise _validate_tier's accept AND reject paths so a
    # future manifest re-pin cannot silently regress the fail-closed tier contract.
    tier_accept = all(_validate_tier(t) == t for t in MANIFEST_TIERS)
    tier_reject = 0
    for _bad in (None, "global", "ORG", 7):
        try:
            _validate_tier(_bad)
        except InitError:
            tier_reject += 1
    tier_ok = tier_accept and tier_reject == 4
    if tier_ok:
        passed += 1
    print(f"  [{'OK' if tier_ok else 'BAD'}] FXTIER-manifest-tier-enum: tier declaration accepts "
          f"{list(MANIFEST_TIERS)} only (fail-closed InitError otherwise)")
    print(f"           expected accept 3/3 + reject 4/4 -> "
          f"accepted={'3/3' if tier_accept else 'BAD'}, rejected={tier_reject}/4")

    # 869dtn48p/869dx7xpc XDOC family fixtures (synthetic doc copies; exact failing-set match,
    # same contract as the pointer fixtures above). XDOC_FIXTURES2 carries a 5th element: the
    # org_mirror_record override.
    print()
    for entry in XDOC_FIXTURES + XDOC_FIXTURES2:
        fid, desc, build, expected = entry
        try:
            built = build(clean_text)
            ptr, docs, shas = built[0], built[1], built[2]
            rec = built[3] if len(built) > 3 else None
            xres, _skip = run_xdoc_checks(ptr, docs, shas, org_mirror_record=rec)
            failed = _failed_set(xres)
            ok = (failed == expected)
            detail = (f"failed={sorted(failed)} == expected" if ok
                      else f"failed={sorted(failed)} != expected={sorted(expected)}")
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        if ok:
            passed += 1
        verb = "stay clean" if not expected else f"FAIL exactly {sorted(expected)}"
        print(f"  [{'OK' if ok else 'BAD'}] {fid}: {desc}")
        print(f"           expected to {verb} -> {detail}")

    # 869dx7xpc confidentiality fixture: mirror CONTENT must never be echoed into any xdoc
    # label / detail / skip-note — only structure labels, byte counts and sha1s may appear.
    sentinel = "ORG-CONTENT-SENTINEL-DO-NOT-ECHO"
    bad_mirror = f"# wrong shape {sentinel}\n"       # fails X04 + X05 -> worst-case output paths
    xres, xskip = run_xdoc_checks(clean_text, {"org_mirror": bad_mirror}, {},
                                  org_mirror_record={"id": "424242424242",
                                                     "sha1_recorded": "beefbeefbeefbeefbeefbeefbeefbeefbeefbeef"})
    blob = " ".join(f"{l} {d}" for _ok, l, d in xres.values()) + " " + " ".join(xskip)
    conf_ok = sentinel not in blob
    if conf_ok:
        passed += 1
    print(f"  [{'OK' if conf_ok else 'BAD'}] FXCONF-mirror-no-echo: org-mirror content never appears "
          f"in xdoc output (structure/sha1 only)")
    print(f"           expected sentinel absent from all labels/details/notes -> "
          f"{'absent' if conf_ok else 'LEAKED'}")
    xinj = dict(XDOC_CLAUSES)
    xinj["XL99"] = ("DELIBERATELY UNCOVERED xdoc rule", [])
    xcov_ok, _ = coverage_tripwire(manifest=xinj, checks=XDOC_CHECKS)
    xtrip_caught = not xcov_ok
    if xtrip_caught:
        passed += 1
    print(f"  [{'OK' if xtrip_caught else 'BAD'}] FXXCOV-uncovered-xdoc-rule: an xdoc clause with no mapped check")
    print(f"           expected xdoc coverage tripwire to FAIL -> {'fired' if xtrip_caught else 'did NOT fire'}")

    # 869dwncba hygiene family fixtures (JSON-string dumps through run_hygiene_checks; exact
    # failing-set contract). Recommend-only family — the fixtures prove the flagging LOGIC.
    print()
    for fid, desc, cdump, adump, expected in HYG_FIXTURES:
        try:
            hres, _skip = run_hygiene_checks(cdump, adump)
            failed = _failed_set(hres)
            ok = (failed == expected)
            detail = (f"failed={sorted(failed)} == expected" if ok
                      else f"failed={sorted(failed)} != expected={sorted(expected)}")
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        if ok:
            passed += 1
        verb = "stay clean" if not expected else f"FAIL exactly {sorted(expected)}"
        print(f"  [{'OK' if ok else 'BAD'}] {fid}: {desc}")
        print(f"           expected to {verb} -> {detail}")
    hinj = dict(HYGIENE_CLAUSES)
    hinj["RL99"] = ("DELIBERATELY UNCOVERED hygiene rule", [])
    hcov_ok, _ = coverage_tripwire(manifest=hinj, checks=HYGIENE_CHECKS)
    htrip_caught = not hcov_ok
    if htrip_caught:
        passed += 1
    print(f"  [{'OK' if htrip_caught else 'BAD'}] FXHCOV-uncovered-hygiene-rule: a hygiene clause with no mapped check")
    print(f"           expected hygiene coverage tripwire to FAIL -> {'fired' if htrip_caught else 'did NOT fire'}")

    # 869dtn4e2 static-doc hygiene fixtures (synthetic doc copies through run_dochygiene_checks;
    # exact failing-set contract).
    print()
    for fid, desc, build, expected in DH_FIXTURES:
        try:
            ptr, docs = build(clean_text)
            dres, _skip = run_dochygiene_checks(ptr, docs)
            failed = _failed_set(dres)
            ok = (failed == expected)
            detail = (f"failed={sorted(failed)} == expected" if ok
                      else f"failed={sorted(failed)} != expected={sorted(expected)}")
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        if ok:
            passed += 1
        verb = "stay clean" if not expected else f"FAIL exactly {sorted(expected)}"
        print(f"  [{'OK' if ok else 'BAD'}] {fid}: {desc}")
        print(f"           expected to {verb} -> {detail}")
    dinj = dict(DOCHYG_CLAUSES)
    dinj["HL99"] = ("DELIBERATELY UNCOVERED doc-hygiene rule", [])
    dcov_ok, _ = coverage_tripwire(manifest=dinj, checks=DOCHYG_CHECKS)
    dtrip_caught = not dcov_ok
    if dtrip_caught:
        passed += 1
    print(f"  [{'OK' if dtrip_caught else 'BAD'}] FXDCOV-uncovered-dochygiene-rule: a doc-hygiene clause with no mapped check")
    print(f"           expected doc-hygiene coverage tripwire to FAIL -> {'fired' if dtrip_caught else 'did NOT fire'}")

    # 869e5m1nd/869dxa4gy pin/baseline-currency fixtures (exact failing-set contract).
    print()
    for fid, desc, build, expected in PN_FIXTURES:
        try:
            ptr, shas = build(clean_text)
            pres, _skip = run_pin_checks(ptr, shas)
            failed = _failed_set(pres)
            ok = (failed == expected)
            detail = (f"failed={sorted(failed)} == expected" if ok
                      else f"failed={sorted(failed)} != expected={sorted(expected)}")
        except Exception as e:
            ok, detail = False, f"raised {type(e).__name__}: {e}"
        if ok:
            passed += 1
        verb = "stay clean" if not expected else f"FAIL exactly {sorted(expected)}"
        print(f"  [{'OK' if ok else 'BAD'}] {fid}: {desc}")
        print(f"           expected to {verb} -> {detail}")
    pinj = dict(PIN_CLAUSES)
    pinj["PL99"] = ("DELIBERATELY UNCOVERED pin rule", [])
    pcov_ok, _ = coverage_tripwire(manifest=pinj, checks=PIN_CHECKS)
    ptrip_caught = not pcov_ok
    if ptrip_caught:
        passed += 1
    print(f"  [{'OK' if ptrip_caught else 'BAD'}] FXPCOV-uncovered-pin-rule: a pin clause with no mapped check")
    print(f"           expected pin coverage tripwire to FAIL -> {'fired' if ptrip_caught else 'did NOT fire'}")

    all_ok = base_clean and (passed == total)
    print(f"\nSELF-TEST RESULT: {passed}/{total} fixtures correct (exact failing-set match); "
          f"baseline {'clean' if base_clean else 'BROKEN'} -> {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1
