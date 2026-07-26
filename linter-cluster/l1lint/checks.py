# -*- coding: utf-8 -*-
"""l1lint.checks - the C00-C13 core check family, the check registry (CHECKS), the clause manifest (CLAUSE_MANIFEST) and the coverage tripwire (engine core)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 307-761.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import re

from .loader import (CANONICAL_PRECEDENCE, CONTEXTUAL_PROSE_IDS, IMMUTABLE_DOCS,
                     LONGID_RE, NUMERIC_THRESHOLD_KEYS, REQUIRED_DROPZONE_IDS,
                     REQUIRED_NEVERWRITE_IDS, SHA1_RE, UUID_FIND_RE, UUID_RE)
from .parsing import _auth_values, _box_id_set, _box_zone, parsed_id_pool, walk_ids


# ============================================================================
# Checks — each (prose, data) -> (ok: bool, detail: str)
# Checks are parameterised by `data`, so they auto-track future doc edits.
# ============================================================================
def _coerced_long_ids(data):
    """Every non-str scalar ANYWHERE in the parsed tree that LOOKS like a long Box/ClickUp ID
    or a UUID (i.e. would have been a quoted id-string had the author quoted it). PyYAML coerces
    an unquoted `901215950286` to int and an unquoted UUID stays a string, so the int-coercion
    case is the silent one. Returns a list of (path, value). Used by C01 to catch unquoted IDs
    that live OUTSIDE a key named 'id' (e.g. a bare `tasks: 901215950286` map value)."""
    found = []

    def visit(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                visit(v, f"{path}.{k}" if path else str(k))
        elif isinstance(o, list):
            for i, it in enumerate(o):
                visit(it, f"{path}[{i}]")
        elif isinstance(o, bool):
            return                                   # bool is an int subclass; never an ID
        elif isinstance(o, int):
            if LONGID_RE.fullmatch(str(o)):          # 8+ digit run parsed as int == unquoted ID
                found.append((path, o))
    visit(data, "")
    return found


def c01_ids_quoted(prose, data):
    """Every ID is a quoted string (PyYAML would coerce an unquoted ID to int). Two scans:
      (1) every dict key named 'id' must be a well-formed id-STRING;
      (2) NO long-ID-shaped scalar anywhere in the tree was coerced to a non-str (int) — this
          catches an unquoted ID that lives outside an 'id' key (e.g. `lists.tasks: 9012...`)."""
    bad = []
    for k, v in walk_ids(data):
        if not isinstance(v, str):
            bad.append(f"id={v!r} parsed as {type(v).__name__} (unquoted)")
        elif not (LONGID_RE.fullmatch(v) or UUID_RE.fullmatch(v)):
            bad.append(f"id={v!r} is not a numeric/UUID id-string")
    # 'ids' / 'bases' lists must be lists of strings
    for path, lst in (("production_spaces.ids",
                       data.get("clickup", {}).get("production_spaces", {}).get("ids")),
                      ("airtable.bases", data.get("airtable", {}).get("bases"))):
        if lst is not None:
            for e in lst:
                if not isinstance(e, str):
                    bad.append(f"{path} element {e!r} not a quoted string")
    # int-coerced unquoted long-IDs anywhere in the tree (outside an explicit 'id' key)
    for path, val in _coerced_long_ids(data):
        if not path.endswith(".id") and path != "id":   # 'id'-key cases already reported above
            bad.append(f"{path} = {val!r} parsed as int (unquoted long-ID — must be a quoted string)")
    return (not bad, "all IDs are quoted strings" if not bad else "; ".join(bad))


def c02_prose_ids_in_yaml(prose, data):
    """Every long-ID / UUID named in the prose appears in the PARSED YAML data tree.
    Parsed-pool (not raw text) so an ID left only in a YAML `# comment` is correctly
    flagged (comment-spoof). Broader than a key=='id'-only walk, so IDs that live in
    `desc`/non-id keys (e.g. the sub-doc IDs inside never_write desc) do NOT false-flag.
    CONTEXTUAL_PROSE_IDS (e.g. the ClickUp workspace id 20433935) are exempt: they appear in
    prose as context, not as an enumerable Box/ClickUp target mirrored in the data block."""
    pool = parsed_id_pool(data)
    prose_ids = set(LONGID_RE.findall(prose)) | set(UUID_FIND_RE.findall(prose))
    orphan = sorted(i for i in prose_ids if i not in pool and i not in CONTEXTUAL_PROSE_IDS)
    return (not orphan,
            "every prose ID resolves to a parsed YAML value"
            if not orphan else f"prose IDs absent from parsed YAML data: {orphan}")


def c03_writable_neverwrite_disjoint(prose, data):
    """writable (and create-only drop-zones) must not intersect never_write."""
    box = data.get("box", {})
    writable = _box_id_set(box, "writable_baseline")
    drops = _box_id_set(box, "drop_zones_create_only")
    never = _box_id_set(box, "never_write")
    clash = sorted((writable | drops) & never)
    return (not clash,
            "writable / drop-zones disjoint from never_write"
            if not clash else f"writable & never_write overlap: {clash}")


def c04_precedence_order(prose, data):
    """YAML precedence == canonical 7 tiers in order; prose lists them in same order."""
    prec = data.get("precedence", [])
    if prec != CANONICAL_PRECEDENCE:
        return False, f"YAML precedence != canonical: {prec}"
    # prose: scope to the '## PRECEDENCE' section only, then check its 1..7 list
    msec = re.search(r'##\s*PRECEDENCE.*?(?=\n##\s|\Z)', prose, re.DOTALL | re.IGNORECASE)
    if not msec:
        return False, "no '## PRECEDENCE' prose section found"
    sect = msec.group(0)
    # v4.3 (2026-07-16): 7-tier precedence — never-write/never-grant extracted to its own tier 4
    # (structurally supreme), org-instructions tier 5, ceilings/mandate/registry tier 6, rules+tag-use
    # tier 7. Anchors are distinctive lowercase substrings of each tier, in canonical order 1..7
    # (verified vs the live v4.3 pointer). Same-class parser update as C10/C02/C12 — it tracks the
    # already-sovereign 7-tier order; it does NOT redefine precedence (the pointer governs that).
    expected_anchors = ["safety", "failsafe", "gate-v", "never-write", "organisation", "ceiling", "rules"]
    items = re.findall(r'^\s*([1-7])\.\s*(.+)$', sect, re.MULTILINE)
    if len(items) < 7:
        return False, f"prose PRECEDENCE has {len(items)} numbered tiers, expected 7"
    items = [ln for _, ln in sorted(items, key=lambda x: x[0])][:7]
    for ln, anchor in zip(items, expected_anchors):
        if anchor not in ln.lower():
            return False, f"prose tier missing expected anchor '{anchor}': {ln[:50]!r}"
    return True, "precedence = 7 canonical tiers, prose order matches"


def c05_failsafe_overrides(prose, data):
    v = data.get("failsafe", {}).get("overrides_ceilings", None)
    return (v is True, "failsafe.overrides_ceilings == true"
            if v is True else f"failsafe.overrides_ceilings == {v!r}")


def c06_mutability_partition(prose, data):
    """Immutable & editable lists are disjoint, and the immutable-core floor holds.
    Two load-bearing invariants (v0.2.6 — over-specified DOC_COMPONENTS/EDITABLE_DOCS
    partitioning + misfiled branch dropped; they never tripped on a real edit and only
    added surface):
      (a) DISJOINTNESS — no doc-component is BOTH immutable_jr_paste_only and cowork_editable
          (a self-contradictory mutability claim; the C10-class category-bypass for docs);
      (b) IMMUTABLE-CORE FLOOR — {pointer, gate_v} MUST be in the immutable list (hardcoded,
          NOT derived from the editable doc-under-test, so a hijacked YAML cannot demote the
          two sovereign-paste-only docs to editable)."""
    mut = data.get("mutability", {})
    imm = set(mut.get("immutable_jr_paste_only", []))
    edt = set(mut.get("cowork_editable_howto_only", []))
    errs = []
    overlap = imm & edt
    if overlap:
        errs.append(f"in both lists: {sorted(overlap)}")
    if not IMMUTABLE_DOCS <= imm:
        errs.append(f"immutable-core docs missing: {sorted(IMMUTABLE_DOCS - imm)}")
    return (not errs, "mutability lists disjoint + immutable core floored"
            if not errs else "; ".join(errs))


def c07_jr_pattern(prose, data):
    """(JR)-field rule integrity over jr_field_rule.{allow_list, consent_gated, never_write}
    (the v4.1 FIELD-ID-based restructure; pre-v4.1 key vacuity closed 2026-07-16). ID-centric by
    design — display names are non-authoritative labels ("match by FIELD-ID, never display name"),
    so no (JR)-suffix audit. Two invariants:
      (a) UUID VALIDITY — every enumerated field id, across ALL THREE classes, is a well-formed UUID;
      (b) CLASS DISJOINTNESS — no field-id appears in more than one class (a field cannot be e.g. both
          allow-list-writable AND never-write; the C06-class self-contradiction applied to JR fields)."""
    ps = data.get("clickup", {}).get("production_spaces", {})
    jfr = ps.get("jr_field_rule", {})
    if not isinstance(jfr, dict):
        return False, f"jr_field_rule is {type(jfr).__name__}, not a mapping"
    errs = []
    seen = {}                                        # field-id -> first class seen in (disjointness)
    for cls in ("allow_list", "consent_gated", "never_write"):
        entries = jfr.get(cls, []) or []
        if not isinstance(entries, list):
            errs.append(f"jr_field_rule.{cls} is {type(entries).__name__}, not a list")
            continue
        for f in entries:
            if not isinstance(f, dict):
                errs.append(f"jr_field_rule.{cls} entry is {type(f).__name__}, not a dict")
                continue
            fid = f.get("id")
            if not (isinstance(fid, str) and UUID_RE.fullmatch(fid)):
                errs.append(f"jr_field_rule.{cls} field id {fid!r} not a UUID")
                continue
            if fid in seen and seen[fid] != cls:
                errs.append(f"field id {fid!r} in both {seen[fid]} and {cls} (class contradiction)")
            seen[fid] = cls
    return (not errs, "(JR) field ids are UUIDs across all classes + classes disjoint"
            if not errs else "; ".join(errs))


def _classify_id(v):
    if v is None:
        return "MISSING"
    s = v.strip()
    if "fill" in s.lower() or (s.startswith("<") and s.endswith(">")):
        return "PENDING"
    if s.isdigit():
        return "RESOLVED"
    return "INVALID"


def _classify_sha(v):
    if v is None:
        return "MISSING"
    s = v.strip()
    if "fill" in s.lower() or (s.startswith("<") and s.endswith(">")):
        return "PENDING"
    if SHA1_RE.fullmatch(s):
        return "RESOLVED"
    return "INVALID"


def c08_pointed_docs_resolve(prose, data):
    """The three 'Pointed-to docs' prose Box refs + the GATE-V sha1 line are each
    PENDING (placeholder; OK in a draft) / RESOLVED (well-formed) / INVALID (FAIL =
    a lost pointer). RESOLVED values are cross-checked EQUAL to the YAML
    pointed_to_docs block (single-source-of-truth)."""
    errs, classes = [], []
    msec = re.search(r'\*\*Pointed-to docs.*?(?=\*\*Load)', prose, re.DOTALL | re.IGNORECASE)
    sect = msec.group(0) if msec else ""
    yaml_ptd = data.get("pointed_to_docs", {}) or {}

    prose_refs = {}
    for key, anchor in (("gate_v", "GATE-V"), ("rules", "Rules"), ("tag_use", "Tag Use")):
        m = re.search(re.escape(anchor) + r'.*?Box\s*`([^`]+)`', sect, re.IGNORECASE)
        prose_refs[key] = m.group(1) if m else None

    for key in ("gate_v", "rules", "tag_use"):
        v = prose_refs[key]
        cls = _classify_id(v)
        classes.append(f"{key}={(v or '').strip()!r}:{cls}")
        if cls == "MISSING":
            errs.append(f"{key}: prose Box ref not found in 'Pointed-to docs' section")
        elif cls == "INVALID":
            errs.append(f"{key}: prose Box ref malformed (lost pointer): {v!r}")
        elif cls == "RESOLVED" and key in yaml_ptd:
            yv = (yaml_ptd.get(key) or {}).get("id")
            if yv is not None and yv != v.strip():
                errs.append(f"{key}: prose id {v.strip()!r} != YAML pointed_to_docs id {yv!r}")

    # v4.4: pins are YAML-ONLY. The de-bloat (E8c) removed the prose GATE-V tamper-awareness sha
    # line, so the authoritative GATE-V pin is the YAML data block pointed_to_docs.gate_v.sha1_pin.
    # c08 validates that pin directly; NO prose literal hash is required or consulted.
    yaml_pin = (yaml_ptd.get("gate_v") or {}).get("sha1_pin")
    scls = _classify_sha(yaml_pin)
    classes.append(f"gate_v_sha1(YAML)={(str(yaml_pin) if yaml_pin is not None else '').strip()!r}:{scls}")
    if scls == "MISSING":
        errs.append("YAML pointed_to_docs.gate_v.sha1_pin absent (GATE-V pin lost)")
    elif scls == "INVALID":
        errs.append(f"YAML gate_v.sha1_pin malformed (not 40-hex): {yaml_pin!r}")

    return (not errs, "pointed-to refs resolve + match YAML [" + "; ".join(classes) + "]"
            if not errs else "; ".join(errs))


def c10_neverwrite_category(prose, data):
    """ROOT-OF-TRUST GUARD (hardcoded — security beats auto-track, per the C06 precedent
    and Gemini STEP-5). Every id in REQUIRED_NEVERWRITE_IDS MUST be classified never_write
    in the YAML AND MUST NOT appear in any writable / create-only drop zone. Hardcoded (NOT
    parsed from editable prose) so it cannot be defeated by prose deletion/obfuscation,
    section truncation, or a coordinated prose+YAML edit. The set is a FLOOR — extended only
    by ratified change, never auto-shrunk.
    NOTE: a NON-floored never-write container is NOT relocation-protected — moving it to
    writable passes C02 (id still in the pool) and C03 (no never_write overlap). Relocation
    protection requires being on this floor (added by ratified change)."""
    box = data.get("box", {})
    nw = _box_id_set(box, "never_write")
    writ = _box_id_set(box, "writable_baseline")
    drops = _box_id_set(box, "drop_zones_create_only")
    ng = _box_id_set(box, "never_grant")     # v4.3: never-GRANT is a DISTINCT class from never-write
    errs = []
    missing = sorted(REQUIRED_NEVERWRITE_IDS - nw)
    if missing:
        errs.append(f"root-of-trust IDs not classified never_write (category bypass): {missing}")
    escalated = sorted(REQUIRED_NEVERWRITE_IDS & (writ | drops))
    if escalated:
        errs.append(f"root-of-trust IDs escalated into writable/drop zones: {escalated}")
    # v0.2.6 ADDITIVE prose-consistency augment (the hardcoded floor above is UNCHANGED):
    # every long-ID enumerated in the prose '## ABSOLUTE NEVER-WRITE' section must (a) be
    # classified never_write in the YAML and (b) NOT appear in writable/drops. This catches a
    # prose-vs-YAML drift where a doc author lists a never-write folder in the prose but forgot
    # (or was tricked into omitting) it from the YAML never_write zone. SCOPE: only the IDs the
    # prose section itself enumerates — inherited sub-doc IDs (e.g. 2253140343860) live in YAML
    # `desc` text and are NOT enumerated in this prose section, so this does not parent-inherit.
    msec = re.search(r'##\s*ABSOLUTE NEVER-WRITE.*?(?=\n##\s|\Z)', prose, re.DOTALL | re.IGNORECASE)
    if msec:
        sect = msec.group(0)
        # v4.3 (2026-07-16): the section also carries NEVER-GRANT / AUTOMATION-FIREWALL /
        # disambiguation text citing contrast IDs (367146590337, 390802629329) that are NOT
        # never-write claims — harvest only the enumeration (text before the first sub-heading),
        # and subtract the YAML never_grant set (distinct class) as defence-in-depth.
        cut = re.search(r'\*\*NEVER-GRANT guard|\*\*AUTOMATION FIREWALL|Disambiguation warning', sect, re.IGNORECASE)
        enum = sect[:cut.start()] if cut else sect
        prose_nw_ids = set(LONGID_RE.findall(enum))
        nw_gap = sorted(prose_nw_ids - nw - ng)
        if nw_gap:
            errs.append(f"prose ABSOLUTE NEVER-WRITE IDs absent from YAML never_write: {nw_gap}")
        nw_escalated = sorted((prose_nw_ids - ng) & (writ | drops))
        if nw_escalated:
            errs.append(f"prose ABSOLUTE NEVER-WRITE IDs found in writable/drop zones: {nw_escalated}")
    return (not errs, "root-of-trust IDs classified never_write + not escalated; prose never-write consistent"
            if not errs else "; ".join(errs))


def c11_dropzone_integrity(prose, data):
    """DROP-ZONE INTEGRITY (Gemini STEP-5, L11). Four guarantees:
      (a) writable and create-only drop-zones are MUTUALLY disjoint;
      (b) the known create-only drop-zones (REQUIRED_DROPZONE_IDS) STAY classified as
          drop-zones and never appear in writable — closes the relocation/move attack;
      (c) no create-only drop-zone entry carries full_rw auth — checked LIST-AWARE, so
          `auth: full_rw` AND `auth: [full_rw]` are both caught (C09 accepts list auth, so a
          scalar-only check let the list form silently escalate)."""
    box = data.get("box", {})
    writ = _box_id_set(box, "writable_baseline")
    drops = _box_id_set(box, "drop_zones_create_only")
    errs = []
    clash = sorted(writ & drops)
    if clash:
        errs.append(f"writable & drop-zones overlap (privilege escalation): {clash}")
    missing = sorted(REQUIRED_DROPZONE_IDS - drops)
    if missing:
        errs.append(f"known create-only drop-zones not classified drop-zone (relocation): {missing}")
    escalated = sorted(REQUIRED_DROPZONE_IDS & writ)
    if escalated:
        errs.append(f"create-only drop-zones escalated into writable: {escalated}")
    rogue = sorted(e.get("id") for e in _box_zone(box, "drop_zones_create_only")
                   if isinstance(e, dict) and isinstance(e.get("id"), str)
                   and "full_rw" in _auth_values(e))
    if rogue:
        errs.append(f"create-only drop-zone entries carrying full_rw auth: {rogue}")
    return (not errs, "drop-zones disjoint from writable + floored + not full_rw"
            if not errs else "; ".join(errs))


def c12_zone_shapes(prose, data):
    """SCHEMA-SHAPE (Gemini STEP-5, L12). `box` must be a mapping, and the three Box zone
    arrays must each be a LIST whose every element is a dict with a string `id`. A non-dict
    element / non-string id / null zone / non-mapping box is a clean FAIL — this is what lets
    the gate report a malformed pointer deterministically instead of crashing (the zone
    helpers above also tolerate these shapes so no earlier check raises)."""
    box = data.get("box")
    if not isinstance(box, dict):
        return False, f"box is {type(box).__name__}, not a mapping"
    errs = []
    for key in ("writable_baseline", "drop_zones_create_only", "never_write"):
        if key not in box:
            errs.append(f"box.{key} is absent (expected a list of {{id:...}} dicts)")
            continue
        v = box.get(key)
        if v is None:
            errs.append(f"box.{key} is null/empty (must be a list of {{id:...}} dicts)")
            continue
        if not isinstance(v, list):
            errs.append(f"box.{key} is {type(v).__name__}, not a list")
            continue
        for i, e in enumerate(v):
            if not isinstance(e, dict):
                errs.append(f"box.{key}[{i}] is {type(e).__name__} ({e!r}), not a dict")
            elif not isinstance(e.get("id"), str):
                errs.append(f"box.{key}[{i}] missing a string 'id'")
    return (not errs, "zone arrays are lists of {id:...} dicts"
            if not errs else "; ".join(errs))


def c13_schema_limits_guard(prose, data):
    """TOP-LEVEL SCHEMA & LIMITS GUARD (senior fitness review, L13). Two real operational
    misses nothing else catches, because every other loop uses safe `.get()`:
      (a) a canonical top-level subsystem block silently dropped/un-indented (e.g. the whole
          `context_thresholds:` or `clickup:` block deleted) — the data still parses, every
          downstream `.get()` quietly returns {} / [], and the gate passes blind;
      (b) an operational context threshold left as an UNRESOLVED placeholder
          (e.g. `single_file_kb: "[JR-CONFIRM]"` or `<fill>`) — a string survives where an int
          is required and is never range-checked.
    Ratified invariant: the canonical subsystems `clickup`, `box`, `context_thresholds` must each
    be present AND be a mapping/dict; and every numeric context threshold (the explicit
    NUMERIC_THRESHOLD_KEYS allow-list), WHEN PRESENT, must carry a real `int` (bool rejected;
    v0.2.6 replaced the false-positive-prone substring heuristic with the allow-list).
    Exception-safe: any malformed shape is a clean FAIL. Scope is deliberately the three named
    subsystems only (not the optional pointers)."""
    errs = []
    if not isinstance(data, dict):
        return False, f"data block is {type(data).__name__}, not a mapping"
    for k in ("clickup", "box", "context_thresholds"):
        v = data.get(k)
        if v is None:
            errs.append(f"top-level '{k}' is missing (subsystem block dropped)")
        elif not isinstance(v, dict):
            errs.append(f"top-level '{k}' is {type(v).__name__}, not a mapping/dict")
    ct = data.get("context_thresholds")
    if isinstance(ct, dict):
        for k in NUMERIC_THRESHOLD_KEYS:
            if k in ct:
                v = ct[k]
                if isinstance(v, bool) or not isinstance(v, int):
                    errs.append(f"context_thresholds.{k} = {v!r} is not a resolved int "
                                f"(unconfirmed placeholder / wrong type)")
    return (not errs, "canonical subsystems present as dicts + thresholds are resolved ints"
            if not errs else "; ".join(errs))


# C00 is the structural-parse gate. It is NOT a (prose, data) check like the others — it runs
# BEFORE the YAML is parsed (it IS the parse), so run_checks() produces its result directly and
# this entry's fn is a never-called sentinel kept only so C00 is registered for the coverage
# tripwire + orphan guard. See run_checks().
def _c00_sentinel(prose, data):                      # pragma: no cover  (never invoked)
    return True, "structural parse handled by run_checks"


# Check registry: id -> (label, fn)
CHECKS = {
    "C00": ("pointer parses into a layer1_data mapping (structural parse)", _c00_sentinel),
    "C01": ("every ID is a quoted string", c01_ids_quoted),
    "C02": ("prose IDs exist in the parsed YAML data", c02_prose_ids_in_yaml),
    "C03": ("writable n never_write = empty", c03_writable_neverwrite_disjoint),
    "C04": ("precedence = 7 canonical tiers in order", c04_precedence_order),
    "C05": ("failsafe.overrides_ceilings == true", c05_failsafe_overrides),
    "C06": ("mutability lists disjoint + immutable core floored", c06_mutability_partition),
    "C07": ("jr_field_rule ids are UUIDs across all classes + classes disjoint", c07_jr_pattern),
    "C08": ("pointed-to docs prose refs + sha1 pin resolve + match YAML", c08_pointed_docs_resolve),
    "C10": ("root-of-trust IDs classified never_write + not escalated (hardcoded floor + prose consistency)", c10_neverwrite_category),
    "C11": ("drop-zone integrity: disjoint + floored + not full_rw (list-aware)", c11_dropzone_integrity),
    "C12": ("box zone arrays are lists of {id:...} dicts (schema-shape)", c12_zone_shapes),
    "C13": ("canonical top-level subsystems present + context thresholds resolved ints", c13_schema_limits_guard),
}

# ----------------------------------------------------------------------------
# COVERAGE TRIPWIRE — clause manifest: every normative clause must map to >=1
# check. Adding normative prose without a covering check => FAIL ("uncovered rule").
#
# MANIFEST-DRIFT LIMITATION (Gemini STEP-5, documented, NOT auto-fixed): this manifest is
# hardcoded, so a NEW normative prose clause that nobody adds here is invisible to the
# tripwire. Auto-extracting clauses would make the gate non-deterministic, so we do not.
# Mitigation: (a) the STEP-3 advisory proposer (designed, not built) surfaces candidate
# clauses for JR to ratify into this manifest; (b) the tripwire fails any ratified clause
# whose covering-check list is empty. clause_id -> (prose summary, [covering check ids])
# ----------------------------------------------------------------------------
CLAUSE_MANIFEST = {
    "L0": ("Pointer must parse into a layer1_data mapping (malformed = clean FAIL, never a crash)", ["C00"]),
    "L1": ("Data-block IDs are quoted strings", ["C01"]),
    "L2": ("Prose IDs must exist in the parsed YAML data (YAML governs; comment-spoof-proof)", ["C02"]),
    "L3": ("Writable zone disjoint from the never-write tree (sibling-name trap)", ["C03"]),
    "L4": ("Precedence is 7 tiers, earlier always wins", ["C04"]),
    "L5": ("Failsafe lockdown overrides the write ceilings", ["C05"]),
    "L6": ("Immutable core vs Cowork-editable partition", ["C06"]),
    "L7": ("jr_field_rule fields (allow_list/consent_gated/never_write) have UUID ids and are class-disjoint (a field-id lives in exactly one class)", ["C07"]),
    "L8": ("Pointed-to docs refs + GATE-V sha1 pin resolve + match YAML at sovereign-paste", ["C08"]),
    "L10": ("Root-of-trust IDs must stay classified never_write and never appear in writable/drop zones; prose never-write IDs consistent with YAML", ["C10"]),
    "L11": ("Drop-zones disjoint from writable, floored, none full_rw (scalar or list auth)", ["C11"]),
    "L12": ("Box zone arrays must be lists of {id:...} dicts; box a mapping (no coercion/null)", ["C12"]),
    "L13": ("Canonical top-level subsystems (clickup/box/context_thresholds) exist as dicts; context thresholds are fully resolved ints (no unconfirmed placeholders)", ["C13"]),
}


def coverage_tripwire(manifest=CLAUSE_MANIFEST, checks=CHECKS):
    """Every clause -> >=1 existing check; flag orphan checks. Returns (ok, lines)."""
    lines, ok = [], True
    covered_checks = set()
    for cid, (summary, covers) in sorted(manifest.items()):
        if not covers:
            ok = False
            lines.append(f"  [UNCOVERED] {cid}: '{summary}' has NO mapped check")
            continue
        missing = [c for c in covers if c not in checks]
        if missing:
            ok = False
            lines.append(f"  [UNCOVERED] {cid}: references missing check(s) {missing}")
        else:
            covered_checks.update(covers)
            lines.append(f"  [ok] {cid} -> {covers}: {summary}")
    orphans = sorted(set(checks) - covered_checks)
    if orphans:
        ok = False
        lines.append(f"  [ORPHAN] checks with no clause: {orphans}")
    return ok, lines

