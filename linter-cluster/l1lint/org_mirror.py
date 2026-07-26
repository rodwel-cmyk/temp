# -*- coding: utf-8 -*-
"""l1lint.org_mirror - ORGANISATIONAL-layer definitions isolated per the 869drd6uy structuring guideline: the 869dx7xpc coverage map + org-mirror structural conventions. The forthcoming org-instructions/Layer-1 governance split localises here. The X04/X05 orchestration that consumes these stays verbatim inside xdoc.run_xdoc_checks (pure refactor: extracting it would alter call-frame shape); flagged as the follow-on cut line

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 777-797.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import re


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
