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

VERSION = "0.2.8"
INIT_EXIT = 3   # F2: dedicated init-failure exit code, distinct from argparse's CLI-usage exit 2

# ---- contract constants kept inline (not security floors; not partition-scoped) -------------
# C06 immutable-core floor: these doc-components must be JR-paste-only (never Cowork-editable).
IMMUTABLE_DOCS = {"pointer", "gate_v"}
# C13 numeric-threshold allow-list: exactly the context_thresholds keys that MUST carry a
# resolved int (bool rejected).
NUMERIC_THRESHOLD_KEYS = {"single_file_kb", "cumulative_session_kb", "large_docs"}
# C02 contextual-prose-ID allow-list: long-IDs legitimately appearing in pointer PROSE as context,
# not as enumerable targets mirrored in the YAML. 20433935 = the ClickUp WORKSPACE id (v4.3
# determination 2026-07-16: contextual — a C02 parser-gap closure, not a pointer defect).
CONTEXTUAL_PROSE_IDS = frozenset({"20433935"})

UUID_RE = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-'
                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
LONGID_RE = re.compile(r'(?<!\d)\d{8,}(?!\d)')       # Box/ClickUp IDs: long digit runs
UUID_FIND_RE = re.compile(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-'
                          r'[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b')

# ============================================================================
# External-artifact loaders (sha1-pinned; init-failure -> exit 3, never a traceback)
# ============================================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE_PATH = os.path.join(_HERE, "baseline.md")
MANIFEST_PATH = os.path.join(_HERE, "manifest.yaml")
BASELINE_SHA1 = "dd5da45a1f93963c6f1c381e9dcd292f6f79333d"   # == live v4.4 pointer (Box 2289600889999, DEPLOYED-LIVE copy)
MANIFEST_SHA1 = "0397bfd11cfe8023aa7eb4808681d0bd598ddad3"   # re-pinned for manifest v1.1 (869drd6uy: + top-level tier: declaration; floors unchanged)

# 869drd6uy: the manifest declares WHICH governance tier it floors (org -> personal -> project);
# validated fail-closed at load, exposed as MANIFEST_TIER, never enters the C00-C13 set-math.
MANIFEST_TIERS = ("org", "personal", "project")


class InitError(Exception):
    """A baseline/manifest initialisation failure (missing / unreadable / sha1-mismatch).
    Surfaced as a dedicated INIT-FAILURE message + exit code 3 — never a traceback, never a
    C00-C13 verdict (F2)."""


# ============================================================================
# 869dthz60 BOUNDED LOADER — alias-bomb ("billion-laughs") guard on the SHARED parse path.
# PyYAML safe_load has no alias-expansion budget: a ~7-level anchored alias bomb makes the load
# (and the engine's subsequent tree traversal) exceed the wall-time bound on both the oracle and
# split engine (pre-existing shared exposure; availability/DoS, likelihood LOW). Guard, applied
# BEFORE construction on every linter yaml.safe_load (pointer block + manifest):
#   (a) INPUT-SIZE CAP  — the yaml text may not exceed YAML_MAX_BYTES;
#   (b) ALIAS BUDGET    — alias events are counted via PyYAML's event parser (parsing emits
#       events WITHOUT constructing/expanding, so the scan is O(input) and cannot blow up);
#       budget 0: Layer 1 governance YAML is alias-free by construction, so ANY alias/anchor
#       use is rejected (deterministic — no wall-clock timeout, which would break determinism).
# A breach raises BoundedLoadError -> the pointer path reports it as a clean C00 FAIL and the
# manifest path as INIT-FAILURE exit 3. A malformed (non-bomb) input is deliberately re-parsed
# by yaml.safe_load so the canonical error message is byte-identical to the pre-guard engine.
# ============================================================================
YAML_MAX_BYTES = 2_000_000
YAML_ALIAS_BUDGET = 0


class BoundedLoadError(ValueError):
    """A bounded-loader cap breach (size / alias budget) — never a crash, never a hang."""


def bounded_safe_load(text, what="yaml block"):
    """yaml.safe_load with the 869dthz60 size + alias-budget guard. `text` may be str or bytes."""
    nbytes = len(text.encode("utf-8")) if isinstance(text, str) else len(text)
    if nbytes > YAML_MAX_BYTES:
        raise BoundedLoadError(f"{what} exceeds the bounded-loader size cap "
                               f"({nbytes} > {YAML_MAX_BYTES} bytes)")
    aliases = 0
    try:
        for ev in yaml.parse(text, Loader=yaml.SafeLoader):
            if isinstance(ev, yaml.events.AliasEvent):
                aliases += 1
                if aliases > YAML_ALIAS_BUDGET:
                    raise BoundedLoadError(
                        f"{what} exceeds the alias budget (> {YAML_ALIAS_BUDGET} alias/anchor "
                        f"references — alias-expansion bomb guard; governance YAML is alias-free)")
    except BoundedLoadError:
        raise
    except yaml.YAMLError:
        pass          # malformed input: fall through so safe_load raises the CANONICAL error
    return yaml.safe_load(text)


def _read_pinned(path, want_sha1, label):
    """Read `path` as raw bytes and assert sha1 == want_sha1. A read error or a sha1 mismatch
    (corruption, a Git core.autocrlf CRLF rewrite, or a wrong-version file) raises InitError."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as e:
        raise InitError(f"{label} unreadable ({path}): {type(e).__name__}: {e}")
    got = hashlib.sha1(raw).hexdigest()
    if got != want_sha1:
        raise InitError(f"{label} sha1 mismatch ({path}): got {got}, expected {want_sha1} "
                        f"(corruption / CRLF rewrite / wrong version)")
    return raw


def _validate_tier(tier):
    """869drd6uy: `tier` must be a MANIFEST_TIERS member; else InitError. Fail-closed for FUTURE
    re-pins (the pinned manifest carries a valid tier; a missing/unknown one is never defaulted)."""
    if tier not in MANIFEST_TIERS:
        raise InitError(f"manifest tier {tier!r} invalid (expected one of {list(MANIFEST_TIERS)})")
    return tier


def _validate_org_mirror_record(rec):
    """869dx7xpc: the manifest's OPTIONAL org_mirror record — {id: <digits>, sha1_recorded:
    <40-hex>} — validated when present (None = mirror not yet ratified, machinery dormant).
    Raises InitError on a malformed record (fail-closed at re-pin, like the tier field)."""
    if rec is None:
        return None
    if not isinstance(rec, dict):
        raise InitError(f"manifest org_mirror is {type(rec).__name__}, not a mapping")
    mid, sha = rec.get("id"), rec.get("sha1_recorded")
    if not (isinstance(mid, str) and mid.isdigit()):
        raise InitError(f"manifest org_mirror.id {mid!r} is not a digit-string Box id")
    if not (isinstance(sha, str) and SHA1_RE.fullmatch(sha)):
        raise InitError(f"manifest org_mirror.sha1_recorded {sha!r} is not 40-hex")
    return rec


def _load_manifest():
    """Load + sha1-verify manifest.yaml and PROJECT it (F5) into the exact native primitives
    C00-C13 expect: REQUIRED_NEVERWRITE_IDS / REQUIRED_DROPZONE_IDS as flat sets of id-STRINGS,
    CANONICAL_PRECEDENCE as a list of name-STRINGS in tier order. scope/tier metadata is dropped
    here and NEVER reaches the set-math (a dict in a set would raise unhashable-type).
    v1.1 (869drd6uy): also validates + returns the manifest's top-level `tier:` declaration."""
    raw = _read_pinned(MANIFEST_PATH, MANIFEST_SHA1, "manifest")
    try:
        m = bounded_safe_load(raw, what="manifest")   # 869dthz60: shared bounded parse path
    except (yaml.YAMLError, BoundedLoadError) as e:
        raise InitError(f"manifest YAML parse failed: {e}")
    if not isinstance(m, dict):
        raise InitError(f"manifest is {type(m).__name__}, not a mapping")
    try:
        nw = frozenset(e["id"] for e in m["never_write_ids"])
        dz = frozenset(e["id"] for e in m["drop_zone_ids"])
        prec = [e["name"] for e in sorted(m["precedence"], key=lambda e: e["tier"])]
        pin = m["gate_v_pin"]["sha1"]
        pin_ver = m["gate_v_pin"]["version_expected"]   # 869dtn48p: consumed by X02 pin coherence
    except (KeyError, TypeError) as e:
        raise InitError(f"manifest shape invalid: {type(e).__name__}: {e}")
    for name, coll in (("never_write_ids", nw), ("drop_zone_ids", dz), ("precedence", prec)):
        if not all(isinstance(x, str) for x in coll):
            raise InitError(f"manifest {name} did not project to id/name-strings "
                            f"(non-str element would corrupt set-math)")
    tier = _validate_tier(m.get("tier"))
    mirror = _validate_org_mirror_record(m.get("org_mirror"))   # 869dx7xpc: optional, None today
    return nw, dz, prec, pin, pin_ver, tier, mirror


def _load_baseline():
    """The frozen v3.1 pointer snapshot (sha1-pinned). Used ONLY by --selftest / --emit-fixtures."""
    return _read_pinned(BASELINE_PATH, BASELINE_SHA1, "baseline.md").decode("utf-8")


# Load the floors at import. A manifest failure here is fatal for EVERY mode (the checks need the
# floors), so it aborts cleanly with exit 3 before argparse runs. The baseline is loaded lazily
# (only the selftest/emit paths need it), so a baseline fault does not block a normal lint run.
try:
    (REQUIRED_NEVERWRITE_IDS, REQUIRED_DROPZONE_IDS, CANONICAL_PRECEDENCE, GATE_V_PIN,
     GATE_V_VERSION_EXPECTED, MANIFEST_TIER, ORG_MIRROR_RECORD) = _load_manifest()
except InitError as _e:
    sys.stderr.write(f"INIT-FAILURE: {_e}\n")
    sys.exit(INIT_EXIT)

# ============================================================================
# Parsing
# ============================================================================
def split_doc(text):
    """Return (yaml_block_text, prose_text). prose = doc minus the fenced yaml block."""
    m = re.search(r'```yaml\s*\n(.*?)\n```', text, re.DOTALL)
    if not m:
        raise ValueError("no fenced ```yaml ... ``` data block found")
    yaml_text = m.group(1)
    prose = text[:m.start()] + text[m.end():]
    return yaml_text, prose


def load_data(yaml_text):
    doc = bounded_safe_load(yaml_text)   # 869dthz60: bounded (size + alias budget) parse path
    if not isinstance(doc, dict) or "layer1_data" not in doc:
        raise ValueError("YAML block missing top-level 'layer1_data'")
    ld = doc["layer1_data"]
    # Phase B defect fix (2): layer1_data PRESENT but not a Mapping (one delta class — incl.
    # null/None, list, scalar) -> a clean single C00 FAIL. run_checks turns this raise into a
    # C00 short-circuit, instead of the oracle's downstream per-check `.get()`-on-None crashes.
    # isinstance(dict) is correct for PyYAML safe_load's plain-dict return (F4); switch to
    # collections.abc.Mapping only if the parser is changed to one returning a Mapping subclass.
    if not isinstance(ld, dict):
        raise ValueError(f"'layer1_data' is present but not a mapping/dict ({type(ld).__name__})")
    return ld


def walk_ids(obj):
    """Yield (key, value) for every dict key named 'id'."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "id":
                yield k, v
            else:
                yield from walk_ids(v)
    elif isinstance(obj, list):
        for it in obj:
            yield from walk_ids(it)


def parsed_id_pool(data):
    """Every long-ID / UUID appearing anywhere in the PARSED tree — as a scalar value
    OR a key, at any depth. Comments are gone (the parser dropped them), which is the
    point: an ID surviving only in a `# comment` is NOT in this pool."""
    pool = set()

    def add(s):
        s = str(s)
        pool.update(LONGID_RE.findall(s))
        pool.update(UUID_FIND_RE.findall(s))

    def visit(o):
        if isinstance(o, dict):
            for k, v in o.items():
                add(k)
                visit(v)
        elif isinstance(o, list):
            for it in o:
                visit(it)
        else:
            add(o)

    visit(data)
    return pool


def _box_zone(box, key):
    """The raw list for a box zone, or [] if box/zone is malformed. NEVER raises — a
    malformed shape is reported separately by C12; this just keeps the other checks safe."""
    if not isinstance(box, dict):
        return []
    v = box.get(key)
    return v if isinstance(v, list) else []


def _box_id_set(box, key):
    """The set of string ids in a box zone. Non-dict elements and non-string (e.g. unhashable
    list) ids are skipped so this can never raise; C12 separately FAILS on such shapes."""
    return {e["id"] for e in _box_zone(box, key)
            if isinstance(e, dict) and isinstance(e.get("id"), str)}


def _auth_values(entry):
    """The auth value(s) of a zone entry as a list, whether declared scalar or list."""
    a = entry.get("auth")
    return a if isinstance(a, list) else [a]


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

# 869dx7xpc COVERAGE MAP (re-scoped; 869dtn4e2 added the H-family slots): the linted doc
# universe and which family covers each slot.
COVERAGE_MAP = (
    ("pointer",         "always-on core C00-C13"),
    ("gate_v",          "supplied-input X02/X03 (pin coherence) + H02 (mutability claim)"),
    ("rules",           "supplied-input X01 (ID coherence) + H01-H03 (static hygiene)"),
    ("tag_use",         "supplied-input X01 (ID coherence) + H01-H03 (static hygiene)"),
    ("charter",         "supplied-input X01 (ID coherence) + H01/H04 (static hygiene)"),
    ("org_mirror",      "supplied-input X04 (structure) + X05 (baseline-currency)"),
    ("project_pointer", "supplied-input H04 (no authority-bearing definitions)"),
)

# 869dx7xpc org-mirror STRUCTURAL conventions (X04) — presence-anchors only, matched case-
# insensitively; details report anchor LABELS + byte counts, NEVER mirror content
# (confidentiality: the linter validates STRUCTURE + sha1 only). Conservative default set —
# ratify/tighten when the real mirror lands (flagged in the item deliverable).
ORG_MIRROR_STRUCTURE = (
    ("h1-title",        re.compile(r'^#\s+\S', re.MULTILINE)),
    ("org-tier-marker", re.compile(r'org[-\s]instruction|org[-\s]tier|organisation-level', re.IGNORECASE)),
    ("version-marker",  re.compile(r'\bv\d+\.\d+\b', re.IGNORECASE)),
)

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


# ============================================================================
# CLICKUP HYGIENE CHECK FAMILY — 869dwncba (recommend-only: surfaces, never auto-mutates).
# These checks read LIVE ClickUp in production; this venue has no connector, so they are engine
# functions taking the relevant data as INPUT — a tasks-with-comments dump (R01) and an
# audit-list dump (R02), as JSON. A connected seat feeds real dumps at run time (downstream
# wiring: the weekly hygiene battery; bump precondition = neither red for a linked candidate).
# Offender details cite task/comment IDs + matched MARKER LABELS only — comment text is never
# echoed into findings (same no-echo posture as the org-mirror checks).
# ============================================================================
HYGIENE_MARKERS = (               # (label, regex) — tunable recommend-only heuristics (869dwncba)
    ("add-to",    re.compile(r'\badd to\b', re.IGNORECASE)),
    ("arrow",     re.compile(re.escape("→"))),
    ("NEW",       re.compile(r'\bNEW\b')),                    # case-SENSITIVE by design
    ("should",    re.compile(r'\bshould\b', re.IGNORECASE)),
    ("open-item", re.compile(r'\bopen item\b', re.IGNORECASE)),
    ("decision",  re.compile(r'\bdecision', re.IGNORECASE)),  # prefix: catches decision(s)/decisional
)
CR_SEQ_RE = re.compile(r'\bTEAMS-CR-\d{4}-\d{2}-\d{2}-\d+\b')   # pointer cr_namespace shape

HYGIENE_CHECKS = {
    "R01": "comment-hygiene: no task comment carries scope/decision/open-item markers (candidate mis-files)",
    "R02": "duplicate-CR-seq: no two audit-list tasks share a TEAMS-CR-<date>-<seq> number",
}
HYGIENE_CLAUSES = {
    "RL1": ("Scope/decision content belongs in task body/subtasks, not comments — marker-bearing comments are flagged for extraction (recommend-only)", ["R01"]),
    "RL2": ("TEAMS-CR numbers are unique across the audit list — collisions are flagged (recommend-only)", ["R02"]),
}


def _parse_dump(raw, what):
    """Accept a JSON str/bytes (CLI path) or an already-parsed list (fixture path). Returns
    (list, None) or (None, error-detail). Top level must be a list; anything else is a clean
    check FAIL upstream (fail-closed on garbage — a skipped record is a silent coverage hole)."""
    if isinstance(raw, (bytes, str)):
        try:
            obj = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return None, f"{what} dump is not valid JSON: {e}"
    else:
        obj = raw
    if not isinstance(obj, list):
        return None, f"{what} dump top level is {type(obj).__name__}, not a list"
    return obj, None


def run_hygiene_checks(comments_dump=None, audit_dump=None):
    """869dwncba orchestrator -> (results {rid: (ok, label, detail)}, skipped [info lines]).
    comments_dump: JSON (or list) of {task_id, comments: [{id?, text} | str]};
    audit_dump: JSON (or list) of {task_id, name}. None = that check skips with a note.
    Recommend-only: output surfaces offenders for human extraction; nothing is mutated."""
    results, skipped = {}, []

    if comments_dump is not None:
        obj, err = _parse_dump(comments_dump, "comments")
        if err:
            results["R01"] = (False, HYGIENE_CHECKS["R01"], err)
        else:
            offenders, shape_errs, ncomments = [], [], 0
            for i, t in enumerate(obj):
                if not (isinstance(t, dict) and isinstance(t.get("task_id"), str)):
                    shape_errs.append(f"[{i}]: not a {{task_id, comments}} mapping")
                    continue
                cs = t.get("comments", [])
                if not isinstance(cs, list):
                    shape_errs.append(f"{t['task_id']}: comments is {type(cs).__name__}, not a list")
                    continue
                for j, c in enumerate(cs):
                    if isinstance(c, dict):
                        text, cid = c.get("text"), str(c.get("id", f"#{j}"))
                    elif isinstance(c, str):
                        text, cid = c, f"#{j}"
                    else:
                        text, cid = None, f"#{j}"
                    if not isinstance(text, str):
                        shape_errs.append(f"{t['task_id']} comment {cid}: no text field")
                        continue
                    ncomments += 1
                    hits = [lab for lab, rx in HYGIENE_MARKERS if rx.search(text)]
                    if hits:
                        offenders.append(f"{t['task_id']} comment {cid}: markers {hits} "
                                         f"-> extract to body/subtask")
            ok = not offenders and not shape_errs
            results["R01"] = (ok, HYGIENE_CHECKS["R01"],
                              f"{ncomments} comments across {len(obj)} tasks carry no markers"
                              if ok else "; ".join(shape_errs + offenders))
    else:
        skipped.append("R01 not run: no comments dump supplied (--comments-dump PATH; connected "
                       "seat exports in-scope tasks' comments as JSON — downstream wiring)")

    if audit_dump is not None:
        obj, err = _parse_dump(audit_dump, "audit-list")
        if err:
            results["R02"] = (False, HYGIENE_CHECKS["R02"], err)
        else:
            crs, shape_errs = {}, []
            for i, t in enumerate(obj):
                if not (isinstance(t, dict) and isinstance(t.get("task_id"), str)
                        and isinstance(t.get("name"), str)):
                    shape_errs.append(f"[{i}]: not a {{task_id, name}} mapping")
                    continue
                for cr in CR_SEQ_RE.findall(t["name"]):
                    crs.setdefault(cr, set()).add(t["task_id"])
            collisions = {cr: ids for cr, ids in crs.items() if len(ids) > 1}
            ok = not collisions and not shape_errs
            results["R02"] = (ok, HYGIENE_CHECKS["R02"],
                              f"{len(crs)} CR numbers across {len(obj)} tasks, all unique"
                              if ok else "; ".join(shape_errs +
                                                   [f"{cr} shared by tasks {sorted(ids)}"
                                                    for cr, ids in sorted(collisions.items())]))
    else:
        skipped.append("R02 not run: no audit-list dump supplied (--audit-dump PATH; connected "
                       "seat exports audit list 901218891519 task names as JSON — downstream wiring)")
    return results, skipped


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


# ============================================================================
if __name__ == "__main__":
    sys.exit(main())
