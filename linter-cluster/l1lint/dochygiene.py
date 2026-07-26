# -*- coding: utf-8 -*-
"""l1lint.dochygiene - 869dtn4e2 static-doc hygiene family (H01-H04, supplied-doc offline checks)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 1042-1251.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import re

from .loader import LONGID_RE
from .parsing import load_data, split_doc


# ============================================================================
# STATIC-DOC HYGIENE FAMILY — 869dtn4e2 (tier 1: deterministic, offline, on-demand). Runs on
# the SAME --doc copies as the XDOC family; pure text/structure checks, no live state. The
# editable docs can drift internally without tripping the pointer-only linter — these close that.
# Findings cite line numbers + detector labels; doc text is never echoed beyond version strings.
# ============================================================================
DOCHYG_VERSION_DOCS = ("rules", "tag_use", "charter")            # H01 scope (spec a)
DOCHYG_CLAIM_DOCS = ("rules", "tag_use", "gate_v")               # H02 scope (spec b)
DOCHYG_CEILING_DOCS = ("rules", "tag_use")                       # H03 scope (spec c)
DOCHYG_AUTHORITY_DOCS = ("charter", "project_pointer")           # H04 scope (spec d)
DOCHYG_ALL_DOCS = ("rules", "tag_use", "charter", "gate_v", "project_pointer")

_V_RE = re.compile(r'\bv(\d+)\.(\d+)\b')
_CHANGELOG_SEC_RE = re.compile(r'^#{2,}[^\n]*change[- ]?log[^\n]*$', re.IGNORECASE | re.MULTILINE)
_EDITABLE_CLAIM_RE = re.compile(r'cowork[-\s]editable', re.IGNORECASE)
_IMMUTABLE_CLAIM_RE = re.compile(r'immutable core|sovereign-paste only|jr sovereign-paste|never edit',
                                 re.IGNORECASE)
# canonical precedence anchors (same vocabulary as C04's prose check)
DOC_PREC_ANCHORS = ("safety", "failsafe", "gate-v", "never-write", "organisation", "ceiling", "rules")
# authority-bearing DEFINITION detectors: keyword mentions alone are references (legal);
# a definition needs an ID / a value bound to the keyword on the same line.
_AUTH_GRANT_RE = re.compile(r'full_rw|writable|rw_operational|consent[-_\s]gated|write[-\s]access',
                            re.IGNORECASE)
_THRESHOLD_DEF_RE = re.compile(r'\b(single_file_kb|cumulative_session_kb|large_docs)\s*[:=]\s*\S',
                               re.IGNORECASE)
_NEVERWRITE_WORD_RE = re.compile(r'never[-_\s]write', re.IGNORECASE)

DOCHYG_CHECKS = {
    "H01": "header version matches the latest change-log entry (no silent bump / unlogged edit)",
    "H02": "the doc's editable-vs-immutable self-claim agrees with the pointer's mutability lists",
    "H03": "no ceiling-shaped allow-list re-introduced; precedence restatements in canonical order",
    "H04": "charter / project pointer carry no authority-bearing definitions (ceiling/never-write/threshold)",
}
DOCHYG_CLAUSES = {
    "HL1": ("Editable docs may not bump their header version without a matching change-log entry (and vice versa)", ["H01"]),
    "HL2": ("A doc floored immutable may not claim Cowork-editable, nor the reverse (pointer mutability lists govern)", ["H02"]),
    "HL3": ("Rules/Tag Use may never re-introduce a ceiling allow-list or reorder precedence (Rules S0 bar)", ["H03"]),
    "HL4": ("Charter + project pointer are locators only — authority definitions live in the sovereign pointer", ["H04"]),
}


def _doc_text(docs, name):
    t = docs.get(name)
    if t is None:
        return None
    return t.decode("utf-8", "replace") if isinstance(t, bytes) else str(t)


def _header_version(text):
    """The vN.N on the doc's first H1 line, as an int tuple — or None."""
    for line in text.splitlines():
        if line.startswith("# "):
            m = _V_RE.search(line)
            return (int(m.group(1)), int(m.group(2))) if m else None
    return None


def _changelog_versions(text):
    """All vN.N tuples inside the change-log section (## ...change log... to the next heading),
    or None if the doc has no change-log section."""
    m = _CHANGELOG_SEC_RE.search(text)
    if not m:
        return None
    tail = text[m.end():]
    nxt = re.search(r'^#{1,6}\s', tail, re.MULTILINE)
    sect = tail[:nxt.start()] if nxt else tail
    return [(int(a), int(b)) for a, b in _V_RE.findall(sect)]


def _authority_definition_lines(text, detectors):
    """(line_no, [detector labels]) for every line tripping any detector. Labels only — the
    line text itself is not echoed."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        labs = []
        if "grant" in detectors and _AUTH_GRANT_RE.search(line) and LONGID_RE.search(line):
            labs.append("auth-grant+id")
        if "threshold" in detectors and _THRESHOLD_DEF_RE.search(line):
            labs.append("threshold-def")
        if "neverwrite" in detectors and _NEVERWRITE_WORD_RE.search(line) and LONGID_RE.search(line):
            labs.append("neverwrite-enum")
        if labs:
            hits.append((n, labs))
    return hits


def _precedence_restatement_errs(text):
    """Anchor-keyword sequence across the doc's NUMBERED lines must respect canonical order
    (subsequence test). No/one anchor found = no restatement = clean."""
    seq = []
    for m in re.finditer(r'^\s*\d+[.)]\s*(.+)$', text, re.MULTILINE):
        low = m.group(1).lower()
        for i, a in enumerate(DOC_PREC_ANCHORS):
            if a in low:
                seq.append((i, a))
    errs = []
    for (i1, a1), (i2, a2) in zip(seq, seq[1:]):
        if i2 < i1:
            errs.append(f"precedence restatement out of canonical order: '{a2}' after '{a1}'")
    return errs


def run_dochygiene_checks(pointer_text, docs=None):
    """869dtn4e2 orchestrator -> (results {hid: (ok, label, detail)}, skipped [info lines]).
    Uses the same supplied-doc dict as the XDOC family. Per-check scopes; checks whose docs are
    absent skip with a note. Never raises on malformed content."""
    docs = docs or {}
    results, skipped = {}, []

    # ---- H01: version <-> change-log (per supplied doc; max change-log version must equal
    # the header version — order-independent, so entry ordering conventions don't matter).
    sup = [n for n in DOCHYG_VERSION_DOCS if n in docs]
    if sup:
        errs, notes = [], []
        for name in sup:
            text = _doc_text(docs, name)
            hv = _header_version(text)
            cv = _changelog_versions(text)
            if hv is None:
                errs.append(f"{name}: no vN.N on the H1 header line (unversioned doc)")
                continue
            if cv is None:
                errs.append(f"{name}: no change-log section found (unlogged history)")
                continue
            if not cv:
                errs.append(f"{name}: change-log section has no vN.N entries")
                continue
            top = max(cv)
            if top != hv:
                errs.append(f"{name}: header v{hv[0]}.{hv[1]} != latest change-log v{top[0]}.{top[1]} "
                            f"(silent bump or unlogged edit)")
            else:
                notes.append(f"{name}=v{hv[0]}.{hv[1]}")
        results["H01"] = (not errs, DOCHYG_CHECKS["H01"],
                          "; ".join(errs) if errs else f"header == latest change-log [{'; '.join(notes)}]")
    else:
        skipped.append("H01 not run: no rules/tag_use/charter copy supplied")

    # ---- H02: editable/immutable self-claim vs the pointer's mutability lists.
    sup = [n for n in DOCHYG_CLAIM_DOCS if n in docs]
    if sup:
        try:
            yaml_text, _p = split_doc(pointer_text)
            data = load_data(yaml_text)
            mut = data.get("mutability", {}) if isinstance(data.get("mutability"), dict) else {}
            imm = set(mut.get("immutable_jr_paste_only", []) or [])
            edt = set(mut.get("cowork_editable_howto_only", []) or [])
            errs, notes = [], []
            for name in sup:
                text = _doc_text(docs, name)
                claims_e = bool(_EDITABLE_CLAIM_RE.search(text))
                claims_i = bool(_IMMUTABLE_CLAIM_RE.search(text))
                if claims_e and claims_i:
                    errs.append(f"{name}: claims BOTH Cowork-editable and immutable (ambiguous)")
                elif not claims_e and not claims_i:
                    notes.append(f"{name}: no self-claim found (nothing to cross-check)")
                elif claims_e and name in imm:
                    errs.append(f"{name}: claims Cowork-editable but the pointer floors it immutable")
                elif claims_i and name in edt:
                    errs.append(f"{name}: claims immutable but the pointer lists it Cowork-editable")
                elif claims_e and name not in edt:
                    errs.append(f"{name}: claims Cowork-editable but is not on the pointer's editable list")
                else:
                    notes.append(f"{name}: claim consistent")
            for n_ in notes:
                if "no self-claim" in n_:
                    skipped.append(f"H02 note: {n_}")
            results["H02"] = (not errs, DOCHYG_CHECKS["H02"],
                              "; ".join(errs) if errs
                              else "; ".join(n_ for n_ in notes if "consistent" in n_) or
                                   "no cross-checkable self-claims")
        except Exception as e:
            results["H02"] = (False, DOCHYG_CHECKS["H02"],
                              f"cannot verify: pointer parse failed ({type(e).__name__}: {e})")
    else:
        skipped.append("H02 not run: no rules/tag_use/gate_v copy supplied")

    # ---- H03: ceiling re-introduction + precedence restatement order (Rules/Tag Use).
    sup = [n for n in DOCHYG_CEILING_DOCS if n in docs]
    if sup:
        errs = []
        for name in sup:
            text = _doc_text(docs, name)
            for n_, labs in _authority_definition_lines(text, ("grant",)):
                errs.append(f"{name} line {n_}: ceiling-shaped allow-list content {labs} "
                            f"(Rules S0 forbids re-introducing one)")
            for e_ in _precedence_restatement_errs(text):
                errs.append(f"{name}: {e_}")
        results["H03"] = (not errs, DOCHYG_CHECKS["H03"],
                          "; ".join(errs) if errs
                          else f"no ceiling re-introduction; precedence restatements canonical "
                               f"[{', '.join(sup)}]")
    else:
        skipped.append("H03 not run: no rules/tag_use copy supplied")

    # ---- H04: authority-bearing DEFINITIONS in charter / project pointer.
    sup = [n for n in DOCHYG_AUTHORITY_DOCS if n in docs]
    if sup:
        errs = []
        for name in sup:
            text = _doc_text(docs, name)
            for n_, labs in _authority_definition_lines(text, ("grant", "threshold", "neverwrite")):
                errs.append(f"{name} line {n_}: authority-bearing definition {labs} "
                            f"(authority lives in the sovereign pointer only)")
        results["H04"] = (not errs, DOCHYG_CHECKS["H04"],
                          "; ".join(errs) if errs
                          else f"no authority-bearing definitions [{', '.join(sup)}]")
    else:
        skipped.append("H04 not run: no charter/project_pointer copy supplied")
    return results, skipped
