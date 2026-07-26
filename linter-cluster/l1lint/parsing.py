# -*- coding: utf-8 -*-
"""l1lint.parsing - pointer document parsing + tree-walk helpers shared by every check family

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 218-305.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import re

from .loader import LONGID_RE, UUID_FIND_RE, bounded_safe_load


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

