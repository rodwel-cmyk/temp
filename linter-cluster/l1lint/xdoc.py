# -*- coding: utf-8 -*-
"""l1lint.xdoc - 869dtn48p cross-doc coherence family (X00-X05) incl. the 869dx7xpc org-mirror checks X04/X05 (constants isolated in l1lint.org_mirror)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 763-775, 799-947.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import hashlib

from .loader import (CONTEXTUAL_PROSE_IDS, GATE_V_PIN, GATE_V_VERSION_EXPECTED,
                     InitError, LONGID_RE, ORG_MIRROR_RECORD, SHA1_RE, UUID_FIND_RE,
                     _validate_org_mirror_record)
from .org_mirror import ORG_MIRROR_STRUCTURE
from .parsing import load_data, parsed_id_pool, split_doc


# ============================================================================
# CROSS-DOC (XDOC) CHECK FAMILY — 869dtn48p. Parameterised: runs ONLY when doc copies /
# live sha1s are supplied (--doc NAME=PATH / --live-sha NAME=HEX, or the selftest fixtures),
# so default pointer-lint output stays byte-identical. The pointer YAML data block is the
# single-source-of-truth; supplied sovereign-doc copies are checked AGAINST it. The live
# server-side sha1 fetch is the connected seat's downstream step — this venue takes it as input.
# ============================================================================
XDOC_DOC_NAMES = ("gate_v", "rules", "tag_use", "charter", "org_mirror", "project_pointer")
XDOC_ID_DOCS = ("rules", "tag_use", "charter")       # X01 scope: docs that RESTATE pointer IDs
XDOC_SHA_CONSUMERS = ("gate_v", "org_mirror")        # names whose --live-sha an X-check consumes
# 869e5m1nd/869dxa4gy P-family sha names (+gate_v, which P02 also sweeps when supplied)
PIN_SHA_NAMES = ("deployed_pointer", "scope_registry", "airlock_writer")
LIVE_SHA_NAMES = XDOC_DOC_NAMES + PIN_SHA_NAMES      # full --live-sha vocabulary


XDOC_CHECKS = {                                       # xid -> label (fns are orchestrated below)
    "X00": "pointer parses for cross-doc comparison (structural gate)",
    "X01": "every Box/ClickUp ID + field UUID quoted in supplied docs resolves to the pointer YAML data block",
    "X02": "GATE-V pin mutually consistent: pointer sha1_pin + version_expected == manifest record",
    "X03": "GATE-V pin matches the supplied live server-side sha1 (or supplied doc-copy sha1)",
    "X04": "org-mirror structural/presence conventions hold (structure only — content never echoed)",
    "X05": "org-mirror baseline-currency: supplied sha1 == manifest-recorded sha1",
}
XDOC_CLAUSES = {
    "XL1": ("Rules/Tag Use/charter restate ONLY IDs the pointer data block holds (no cross-doc drift)", ["X01"]),
    "XL2": ("GATE-V sha1_pin + declared version stay consistent AND match the live doc sha1 (mechanises the load-time assertion)", ["X02", "X03"]),
    "XL0": ("Cross-doc comparison requires a parseable pointer (malformed = clean FAIL)", ["X00"]),
    "XL3": ("The org-instruction mirror keeps its ratified structural conventions (presence-anchors; no content echo)", ["X04"]),
    "XL4": ("The org-mirror copy in circulation matches the manifest-recorded sha1 (org-tier baseline-currency)", ["X05"]),
}


def run_xdoc_checks(pointer_text, docs=None, live_shas=None, org_mirror_record=None):
    """869dtn48p/869dx7xpc orchestrator -> (results {xid: (ok, label, detail)}, skipped [info]).
    docs: {name: str|bytes doc copy}; live_shas: {name: 40-hex server-side sha1};
    org_mirror_record: fixture override for the manifest's optional org_mirror record
    (default None -> the pinned manifest's ORG_MIRROR_RECORD). Checks whose inputs are absent
    are SKIPPED with an info line (parameterised activation — never a vacuous PASS, never a
    block on missing optional input). Never raises on malformed content."""
    docs, live_shas = docs or {}, live_shas or {}
    skipped = []
    try:
        yaml_text, _prose = split_doc(pointer_text)
        data = load_data(yaml_text)
    except Exception as e:
        return ({"X00": (False, XDOC_CHECKS["X00"],
                         f"pointer parse failed: {type(e).__name__}: {e}")}, skipped)
    results = {"X00": (True, XDOC_CHECKS["X00"], "pointer parses into a layer1_data mapping")}

    # ---- X01: cross-doc ID coherence (spec (a)) — supplied docs' IDs must be a SUBSET of the
    # pointer's parsed-YAML pool (single-source-of-truth; CONTEXTUAL_PROSE_IDS exempt).
    pool = parsed_id_pool(data)
    supplied = [n for n in XDOC_ID_DOCS if n in docs]
    if supplied:
        errs, notes = [], []
        for name in supplied:
            t = docs[name]
            t = t.decode("utf-8", "replace") if isinstance(t, bytes) else str(t)
            ids = set(LONGID_RE.findall(t)) | set(UUID_FIND_RE.findall(t))
            orphan = sorted(i for i in ids if i not in pool and i not in CONTEXTUAL_PROSE_IDS)
            notes.append(f"{name}:{len(ids)} ids")
            if orphan:
                errs.append(f"{name}: IDs absent from pointer YAML data: {orphan}")
        absent = [n for n in XDOC_ID_DOCS if n not in docs]
        if absent:
            skipped.append(f"X01 partial: no copy supplied for {absent} (--doc NAME=PATH)")
        results["X01"] = (not errs, XDOC_CHECKS["X01"],
                          "; ".join(errs) if errs
                          else f"single-source-of-truth holds [{'; '.join(notes)}]")
    else:
        skipped.append("X01 not run: no rules/tag_use/charter copy supplied (--doc NAME=PATH)")

    # ---- X02: pin mutual consistency (spec (b), offline half) — pointer pointed_to_docs.gate_v
    # {sha1_pin, version_expected} vs the manifest's recorded gate_v_pin. Always runnable.
    ptd = data.get("pointed_to_docs")
    gv = (ptd.get("gate_v") if isinstance(ptd, dict) else None)
    gv = gv if isinstance(gv, dict) else {}
    pin, ver = gv.get("sha1_pin"), gv.get("version_expected")
    errs = []
    pin_ok = isinstance(pin, str) and bool(SHA1_RE.fullmatch(pin))
    if not pin_ok:
        errs.append(f"pointer gate_v.sha1_pin malformed/absent: {pin!r}")
    elif pin.lower() != GATE_V_PIN.lower():
        errs.append(f"pointer gate_v.sha1_pin {pin} != manifest recorded pin {GATE_V_PIN}")
    if ver != GATE_V_VERSION_EXPECTED:
        errs.append(f"pointer gate_v.version_expected {ver!r} != manifest {GATE_V_VERSION_EXPECTED!r}")
    results["X02"] = (not errs, XDOC_CHECKS["X02"],
                      "; ".join(errs) if errs
                      else f"pin + version consistent (...{GATE_V_PIN[-8:]}, {GATE_V_VERSION_EXPECTED})")

    # ---- X03: pin vs live sha1 (spec (b), connected half) — compares the POINTER's pin (the
    # operative load-time assertion) against a supplied live sha1, or the sha1 of a supplied
    # byte-exact gate_v doc copy. Fail-closed: an unusable pointer pin fails X03 too.
    live, src = live_shas.get("gate_v"), "supplied live sha1"
    if live is None and "gate_v" in docs:
        raw = docs["gate_v"]
        raw = raw.encode("utf-8") if isinstance(raw, str) else raw
        live, src = hashlib.sha1(raw).hexdigest(), "sha1(supplied gate_v doc copy)"
    if live is not None:
        live = str(live)
        if not SHA1_RE.fullmatch(live):
            results["X03"] = (False, XDOC_CHECKS["X03"], f"supplied gate_v sha1 malformed: {live!r}")
        elif not pin_ok:
            results["X03"] = (False, XDOC_CHECKS["X03"],
                              "cannot verify: pointer gate_v.sha1_pin malformed/absent (see X02)")
        else:
            ok = live.lower() == pin.lower()
            results["X03"] = (ok, XDOC_CHECKS["X03"],
                              f"{src} ...{live[-8:]} == pointer pin" if ok
                              else f"{src} {live} != pointer pin {pin} "
                                   f"(GATE-V drift/tamper — the load-time assertion would lock down)")
    else:
        skipped.append("X03 not run: no live GATE-V sha1 (--live-sha gate_v=HEX) or gate_v doc copy "
                       "supplied — the live fetch is the connected seat's downstream step")

    # ---- X04/X05: org-mirror coverage (869dx7xpc) — CONFIDENTIALITY: structure + sha1 only,
    # mirror content is NEVER echoed into any detail/finding (anchor labels + byte counts only).
    rec = ORG_MIRROR_RECORD if org_mirror_record is None else org_mirror_record
    m_copy = docs.get("org_mirror")
    m_live = live_shas.get("org_mirror")
    if m_copy is None and m_live is None:
        skipped.append("X04/X05 not run: org-mirror not supplied (--doc/--live-sha org_mirror=...) — "
                       "machinery dormant; FLAG: the org-instruction mirror does not exist yet "
                       "(sibling-item dependency)")
    else:
        if m_copy is not None:
            raw = m_copy.encode("utf-8") if isinstance(m_copy, str) else m_copy
            text = raw.decode("utf-8", "replace")
            missing = [label for label, rx in ORG_MIRROR_STRUCTURE if not rx.search(text)]
            results["X04"] = (not missing, XDOC_CHECKS["X04"],
                              f"missing structural anchors: {missing} [{len(raw)} bytes]" if missing
                              else f"all {len(ORG_MIRROR_STRUCTURE)} structural anchors present "
                                   f"[{len(raw)} bytes]")
        else:
            skipped.append("X04 not run: structure needs the mirror doc copy (--doc org_mirror=PATH); "
                           "only a live sha1 was supplied")
        got = m_live if m_live is not None else hashlib.sha1(
            m_copy.encode("utf-8") if isinstance(m_copy, str) else m_copy).hexdigest()
        gsrc = "supplied live sha1" if m_live is not None else "sha1(supplied mirror copy)"
        try:
            rec = _validate_org_mirror_record(rec)
        except InitError as e:
            rec, rec_err = None, str(e)
        else:
            rec_err = None
        if rec_err is not None:
            results["X05"] = (False, XDOC_CHECKS["X05"], f"org_mirror record malformed: {rec_err}")
        elif rec is None:
            skipped.append("X05 not run: manifest carries no org_mirror record — record "
                           "{id, sha1_recorded} at mirror ratification (org-tier baseline-currency "
                           "activates then)")
        elif not SHA1_RE.fullmatch(str(got)):
            results["X05"] = (False, XDOC_CHECKS["X05"], f"supplied org_mirror sha1 malformed: {got!r}")
        else:
            ok = str(got).lower() == rec["sha1_recorded"].lower()
            results["X05"] = (ok, XDOC_CHECKS["X05"],
                              f"{gsrc} ...{str(got)[-8:]} == recorded (mirror id {rec['id']})" if ok
                              else f"{gsrc} {got} != recorded {rec['sha1_recorded']} "
                                   f"(mirror id {rec['id']} — org-tier baseline drift)")

    for name in live_shas:
        if name not in XDOC_SHA_CONSUMERS and name not in PIN_SHA_NAMES:
            skipped.append(f"live sha1 for {name!r} supplied but not yet consumed (later cluster items)")
    return results, skipped
