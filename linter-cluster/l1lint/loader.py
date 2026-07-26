# -*- coding: utf-8 -*-
"""l1lint.loader - pins, floors, bounded YAML loader, sha1-pinned artifact loads (engine core: the YAML load path + init-failure contract F2)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 40-216.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
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
_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
