# -*- coding: utf-8 -*-
"""l1lint.pins - 869e5m1nd/869dxa4gy pin / baseline-currency family (P01-P02, recommend-only) incl. the item7-REV1 gate_v double-isinstance guard (engine core: pin-check family)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 950-1039.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
from .loader import BASELINE_SHA1, SHA1_RE
from .parsing import load_data, split_doc


# ============================================================================
# PIN / BASELINE-CURRENCY FAMILY — 869e5m1nd + 869dxa4gy (recommend-only; one mechanism,
# cross-linked tasks). The linter's own baseline (BASELINE_SHA1) and the pointer's sha1 pins
# can silently drift from the LIVE docs; these checks compare RECORDED values against live
# server-side sha1s supplied by a connected seat (--live-sha NAME=HEX — the fetch is the
# downstream step; deterministic compares are ~0 tokens as code vs the LLM-seat eyeball pass).
#   P01 (869e5m1nd) baseline-currency: BASELINE_SHA1 vs the live DEPLOYED pointer copy
#       (Box 2289600889999). Divergence = the selftest baseline has gone stale (the v3.7->v4.3
#       incident class: C07 went vacuous unnoticed because nothing flagged the drift).
#   P02 (869dxa4gy) pin-tamper sweep: every pin RECORDED IN THE POINTER's data block —
#       gate_v.sha1_pin / scope_registry.sha1_pin / airlock_writer.sha1_pin — vs its supplied
#       live sha1. (gate_v also has the X03 deep-check; cross-linked, not merged — P02 is the
#       one-shot sweep the pre-edit chokepoint runs.) airlock_writer's "live" sha1 comes from
#       the M1 host file, not Box — same parameter, different fetch, noted at skip time.
# ============================================================================
DEPLOYED_POINTER_ID = "2289600889999"    # DEPLOYED-LIVE pointer copy (BASELINE_SHA1's referent)

PIN_CHECKS = {
    "P01": "baseline-currency: BASELINE_SHA1 == live deployed-pointer sha1 (selftest baseline not stale)",
    "P02": "pin-tamper sweep: pointer-recorded sha1 pins == live doc sha1s (gate_v/scope_registry/airlock_writer)",
}
PIN_CLAUSES = {
    "PL1": ("The frozen selftest baseline must track the live deployed pointer (stale baseline = vacuous checks)", ["P01"]),
    "PL2": ("Every sha1 pin recorded in the pointer must match its live artifact (deterministic tamper check, retires the LLM eyeball compare)", ["P02"]),
}


def run_pin_checks(pointer_text, live_shas=None):
    """869e5m1nd/869dxa4gy orchestrator -> (results {pid: (ok, label, detail)}, skipped).
    live_shas: {name: 40-hex}. Recommend-only; never raises on malformed content."""
    live_shas = live_shas or {}
    results, skipped = {}, []

    # ---- P01: baseline currency (recorded value = the ENGINE's own BASELINE_SHA1 constant).
    live = live_shas.get("deployed_pointer")
    if live is None:
        skipped.append(f"P01 not run: no live deployed-pointer sha1 supplied "
                       f"(--live-sha deployed_pointer=HEX; Box {DEPLOYED_POINTER_ID} — "
                       f"connected-seat fetch)")
    elif not SHA1_RE.fullmatch(str(live)):
        results["P01"] = (False, PIN_CHECKS["P01"], f"supplied deployed-pointer sha1 malformed: {live!r}")
    else:
        ok = str(live).lower() == BASELINE_SHA1.lower()
        results["P01"] = (ok, PIN_CHECKS["P01"],
                          f"live ...{str(live)[-8:]} == BASELINE_SHA1 (baseline current)" if ok
                          else f"live {live} != BASELINE_SHA1 {BASELINE_SHA1} — selftest baseline "
                               f"STALE vs Box {DEPLOYED_POINTER_ID}; refresh baseline.md + re-pin "
                               f"(recommend-only)")

    # ---- P02: pin-tamper sweep over the pointer-recorded pins with a supplied live sha1.
    sweep_names = [n for n in ("gate_v", "scope_registry", "airlock_writer") if n in live_shas]
    if not sweep_names:
        skipped.append("P02 not run: no live sha1 supplied for gate_v/scope_registry/"
                       "airlock_writer (airlock_writer's comes from the M1 host file, not Box)")
    else:
        try:
            yaml_text, _p = split_doc(pointer_text)
            data = load_data(yaml_text)
        except Exception as e:
            results["P02"] = (False, PIN_CHECKS["P02"],
                              f"cannot verify: pointer parse failed ({type(e).__name__}: {e})")
            return results, skipped
        recorded = {
            "gate_v": data["pointed_to_docs"]["gate_v"].get("sha1_pin")
                      if isinstance(data.get("pointed_to_docs"), dict)
                      and isinstance(data["pointed_to_docs"].get("gate_v"), dict) else None,
            "scope_registry": (data.get("scope_registry") or {}).get("sha1_pin")
                              if isinstance(data.get("scope_registry"), dict) else None,
            "airlock_writer": (data.get("airlock_writer") or {}).get("sha1_pin")
                              if isinstance(data.get("airlock_writer"), dict) else None,
        }
        errs, notes = [], []
        for name in sweep_names:
            live, rec = str(live_shas[name]), recorded.get(name)
            if not (isinstance(rec, str) and SHA1_RE.fullmatch(rec)):
                errs.append(f"{name}: recorded pin malformed/absent in the pointer: {rec!r}")
            elif not SHA1_RE.fullmatch(live):
                errs.append(f"{name}: supplied live sha1 malformed: {live!r}")
            elif live.lower() != rec.lower():
                errs.append(f"{name}: live {live} != recorded pin {rec} (TAMPER/DRIFT — "
                            f"surface to JR before any governance edit)")
            else:
                notes.append(f"{name} ok (...{live[-8:]})")
        unchecked = [n for n in ("gate_v", "scope_registry", "airlock_writer")
                     if n not in sweep_names]
        if unchecked:
            skipped.append(f"P02 partial: pins not checked this run (no live sha1): {unchecked}")
        results["P02"] = (not errs, PIN_CHECKS["P02"],
                          "; ".join(errs) if errs else f"pins match [{'; '.join(notes)}]")
    return results, skipped
