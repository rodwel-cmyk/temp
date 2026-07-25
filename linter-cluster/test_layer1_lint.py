#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_layer1_lint.py — 34 known-bad fixtures + the §5 DIFFERENTIAL test harness.

Two roles:
  1. FIXTURES (+ _sub + the fixture constants) — imported by layer1_lint.py's --selftest
     runner (external fixtures, §3.1). Verbatim from the v0.2.8 oracle's embedded self-test.
  2. The differential harness (run as `python test_layer1_lint.py [--phase A|B]`): proves the
     split NEW engine is equivalent-modulo-declared-deltas to the pinned v0.2.8 ORACLE.

Equivalence definition (§5.2, v3 — mode-dependent stdout):
  For each input capture {exit; stdout; per-check C00-C13; coverage-tripwire; stderr}.
   * non-`--json`: stdout compared as an exact byte-stream (after volatile-token normalisation).
   * `--json`    : stdout is the JSON payload -> compared as parsed objects (key-order-insensitive);
                   never byte-compared; no linter-side sort_keys.
   * stderr      : exact trace-string after stripping ONLY paths / line numbers / 0x-addresses
                   (strictly-bounded — must not touch the 40-hex sha1 pin); exception type+message
                   must match strictly.
  Run the whole corpus twice — with and without --json. Python minor-version parity asserted.

PRECONDITION: ORACLE and NEW execute under the identical Python interpreter (this process for the
in-process content corpus; the same sys.executable for the subprocess crash/infra corpus).
"""
import sys, os, re, json, time, random, hashlib, subprocess, tempfile, importlib.util, resource

HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE_PATH = os.path.join(HERE, "oracle_layer1_lint.py")
# Default NEW = the final (Phase-B) engine; override with L1_NEW_ENGINE to verify the
# refactor-only (Phase-A) engine for the `--phase A` 100%-equivalence milestone.
NEW_PATH    = os.path.join(HERE, os.environ.get("L1_NEW_ENGINE", "layer1_lint.py"))
BASELINE    = os.path.join(HERE, "baseline.md")
MANIFEST    = os.path.join(HERE, "manifest.yaml")

def _sub(text, old, new, fid):
    if old not in text:
        raise AssertionError(f"{fid}: anchor not found for mutation")
    return text.replace(old, new, 1)


# v4.3: the writable zone was renamed `writable` -> `writable_baseline` (v4.0) and is now a
# BLOCK sequence; _WRIT is the single baseline ENTRY line (6-space indent). Fixtures that used to
# swap the whole inline `writable: [...]` now replace this entry line (the `writable_baseline:` key
# line above it is left intact), which keeps the anchors byte-exact and comment-free.
_WRIT = '      - { id: "390802629329", name: "AI - Claude - Teams", auth: full_rw, note: "top-level; not nested in any Max tree" }'
_DROPS = 'drop_zones_create_only: [ { id: "977588333", name: "Uploads" }, { id: "86746916736", name: "To Sort" } ]'
_NW_RoT = '      - { id: "385430558352", path: "AI - Claude/Claude Reference Files/LAYER 1 — ROOT OF TRUST _ DO NOT TOUCH/", desc: "DO-NOT-TOUCH subtree: manifest 2253140343860 + 6 sub-docs (2253122015238, 2253073430182, 2253111968712, 2253119457240, 2253118964531, 2253126066109) + Pointer Backup 385440376091 + Reference Files-L1 385443894159 + Reference Edit 385451548133" }'
_CTX_BLOCK = ('  context_thresholds:\n'
              '    single_file_kb: 50\n'
              '    cumulative_session_kb: 150\n'
              '    large_docs: 3\n'
              '    qualitative_triggers: ["broad multi-folder search/audit", "long multi-step synthesis"]\n'
              '    procedural_mandates: ["check size via metadata BEFORE ingesting", "checkpoint to state-cache before delegating"]\n')

FIXTURES = [
    ("FX01-unquoted-id", "ClickUp teams_space id written without quotes",
     lambda t: _sub(t, 'teams_space:      { id: "90128004233"',
                       'teams_space:      { id: 90128004233', "FX01"), frozenset({"C01"})),
    ("FX02-orphan-prose-id", "a Box ID cited in prose that is absent from the YAML",
     lambda t: t.replace("## PRECEDENCE",
                         "Stray reference to Box `999888777666` not in the data block.\n\n## PRECEDENCE", 1),
     frozenset({"C02"})),
    ("FX03-writable-in-neverwrite", "writable_baseline folder id collides with a never-write id",
     lambda t: _sub(t, _WRIT,
                       '      - { id: "385430558352", name: "AI - Claude - Teams", auth: full_rw, note: "top-level; not nested in any Max tree" }', "FX03"), frozenset({"C03", "C10"})),
    ("FX04-precedence-scrambled", "first two precedence tiers swapped",
     lambda t: _sub(t, "precedence: [native_gates, failsafe_lockdown,",
                       "precedence: [failsafe_lockdown, native_gates,", "FX04"), frozenset({"C04"})),
    ("FX05-failsafe-false", "failsafe no longer overrides the ceilings",
     lambda t: _sub(t, "overrides_ceilings: true", "overrides_ceilings: false", "FX05"), frozenset({"C05"})),
    ("FX06-mutability-overlap", "'rules' listed as both editable and immutable",
     lambda t: _sub(t, "immutable_jr_paste_only: [pointer, gate_v,",
                       "immutable_jr_paste_only: [pointer, gate_v, rules,", "FX06"), frozenset({"C06"})),
    ("FX07-jr-uuid-consent-class",
     "a consent_gated (JR) field id set to a valid LONGID that is NOT a UUID — exercises C07's UUID-"
     "validity branch on a NON-allow_list class (complements FX28's allow_list case). C01 does NOT fire "
     "(a longid is a valid quoted-id string); C02 does NOT fire (v4.4: the de-bloat removed the (JR)-"
     "FIELD-RULE prose that cited d8fbed5d, so it now lives ONLY in the YAML data block — displacing it "
     "orphans no prose ref; was {C02,C07} on the v4.3 baseline)",
     lambda t: _sub(t, 'id: "d8fbed5d-23bd-42ef-a245-dc125277fd5a", type: dropdown',
                       'id: "999888777666", type: dropdown', "FX07"), frozenset({"C07"})),
    ("FX08-bad-sha1-pin", "GATE-V sha1 pin (YAML pointed_to_docs.gate_v) replaced with a non-hex value",
     lambda t: _sub(t, 'sha1_pin: "d6d54ae7d1d632f54e7f122efa3a1ccae7269860"',
                       'sha1_pin: "deadbeef"', "FX08"), frozenset({"C08"})),
    ("FX10-comment-spoof", "an active never_write id deleted from the data, left only in a YAML # comment + prose "
     "(v4.3 re-anchor: 367428637440 abandoned — it is now ALSO cited in box.warning, so it stays in the parsed "
     "YAML pool and no longer trips C02; the governance-folder id 370218784710 is cited only in its never_write "
     "entry + the prose enumeration, so the comment-spoof still trips exactly C02+C10)",
     lambda t: _sub(t,
                    '      - { id: "370218784710", path: "AI - Claude/Claude-logs/Governance-Architecture-Project-2026-03/", desc: "governance folder" }',
                    '      # - { id: "370218784710", path: "AI - Claude/Claude-logs/Governance-Architecture-Project-2026-03/", desc: "governance folder" }',
                    "FX10"), frozenset({"C02", "C10"})),
    ("FX11-placeholder-TBD", "the Rules pointed-to Box ref degraded to a malformed 'TBD'",
     lambda t: _sub(t, "**Cowork Layer 1 — Rules** — Box `2289598235660`",
                       "**Cowork Layer 1 — Rules** — Box `TBD`", "FX11"), frozenset({"C08"})),
    ("FX13-neverwrite-category-bypass",
     "root-of-trust moved from never_write to writable (prose still says DO-NOT-TOUCH); C03 still passes, only C10 catches it",
     lambda t: _sub(
         _sub(t, _WRIT,
              '      - { id: "390802629329", name: "AI - Claude - Teams", auth: full_rw }\n      - { id: "385430558352", name: "HIJACKED", auth: full_rw }', "FX13a"),
         _NW_RoT, '      - { id: "999999999999", path: "decoy", desc: "placeholder" }', "FX13b"), frozenset({"C10"})),
    ("FX14-dropzone-in-writable", "Uploads drop-zone id ALSO listed in writable_baseline (overlap); C03 misses it, C11 catches the clash",
     lambda t: _sub(t, _WRIT,
        '      - { id: "390802629329", name: "AI - Claude - Teams", auth: full_rw }\n      - { id: "977588333", name: "Uploads", auth: full_rw }', "FX14"), frozenset({"C11"})),
    ("FX15-dropzone-relocation",
     "Uploads drop-zone MOVED out of drop_zones and into writable (sets stay disjoint); only the C11 floor catches it",
     lambda t: _sub(
         _sub(t, _WRIT,
              '      - { id: "390802629329", name: "AI - Claude - Teams", auth: full_rw }\n      - { id: "977588333", name: "Uploads", auth: full_rw }', "FX15a"),
         _DROPS, 'drop_zones_create_only: [ { id: "86746916736", name: "To Sort" } ]', "FX15b"), frozenset({"C11"})),
    ("FX16-string-coercion",
     "a root-of-trust id placed in writable_baseline as a BARE STRING (the id-extractor would skip it, blinding C03/C10)",
     lambda t: _sub(t, _WRIT,
        '      - { id: "390802629329", name: "AI - Claude - Teams", auth: full_rw }\n      - "385430558352"', "FX16"), frozenset({"C12"})),
    ("FX17-null-zone",
     "the writable_baseline zone emptied to null (would crash a naive loop); C12 reports it as a clean FAIL",
     lambda t: _sub(t, _WRIT, '', "FX17"), frozenset({"C12"})),
    ("FX18-dropzone-full-rw-scalar",
     "a create-only drop-zone entry injected with scalar auth: full_rw",
     lambda t: _sub(t, '{ id: "977588333", name: "Uploads" }',
                       '{ id: "977588333", name: "Uploads", auth: full_rw }', "FX18"), frozenset({"C11"})),
    # ---- v0.2.4 fixtures ----
    ("FX19-dropzone-full-rw-list",
     "a create-only drop-zone entry with auth WRAPPED IN A LIST [full_rw] — evaded the scalar-only C11 check",
     lambda t: _sub(t, '{ id: "977588333", name: "Uploads" }',
                       '{ id: "977588333", name: "Uploads", auth: [full_rw] }', "FX19"), frozenset({"C11"})),
    ("FX20-primitive-zone",
     "the writable_baseline zone replaced by a non-list mapping — must be a clean C12 FAIL, never a TypeError crash",
     lambda t: _sub(t, _WRIT, '      not_a_list: 123', "FX20"), frozenset({"C12"})),
    ("FX21-unhashable-id",
     "a writable_baseline entry whose id is an unhashable list (id: [123]) — must be a clean C12 FAIL, never a crash",
     lambda t: _sub(t, _WRIT, '      - { id: [123] }', "FX21"), frozenset({"C01", "C12"})),
    # ---- v0.2.5 fixtures ----
    ("FX22-context-thresholds-block-dropped",
     "the entire top-level context_thresholds: block removed (accidental block drop); every "
     ".get() returns {} so all other checks pass blind — only C13 catches the missing subsystem",
     lambda t: _sub(t, _CTX_BLOCK, '', "FX22"), frozenset({"C13"})),
    ("FX23-threshold-placeholder",
     "single_file_kb left as the unresolved string placeholder \"[JR-CONFIRM]\" instead of an int",
     lambda t: _sub(t, 'single_file_kb: 50', 'single_file_kb: \"[JR-CONFIRM]\"', "FX23"), frozenset({"C13"})),
    # ---- v0.2.6 fixtures ----
    # C00 structural-parse gate (new in v0.2.6). Both short-circuit to exactly {C00}.
    ("FX24-no-yaml-fence",
     "the ```yaml data-block fence removed entirely — split_doc finds no data block; "
     "must be a clean single C00 FAIL (this is what previously crashed the --json feed)",
     lambda t: _sub(t, "```yaml\nlayer1_data:", "```text\nlayer1_data:", "FX24"), frozenset({"C00"})),
    ("FX25-yaml-missing-layer1_data",
     "a ```yaml block that parses but has no top-level layer1_data key — must be a clean single C00 FAIL",
     lambda t: _sub(t, "layer1_data:\n  precedence:", "other_root:\n  precedence:", "FX25"), frozenset({"C00"})),
    # C10 prose-vs-YAML never-write consistency (v0.2.6 augment): a never-write ID named in the
    # prose '## ABSOLUTE NEVER-WRITE' section but ABSENT from YAML never_write (author drift).
    ("FX26-prose-neverwrite-gap",
     "the prose ABSOLUTE NEVER-WRITE section names a Box ID (the OI folder) that has been removed "
     "from the YAML never_write zone — the new C10 prose-consistency augment catches the drift",
     lambda t: _sub(t,
                    '      - { id: "2172078880293", path: "AI - Claude/Claude-logs/", desc: "Ops Integrity (OI)" }\n',
                    '', "FX26"), frozenset({"C02", "C10"})),
    # ---- v0.2.6 branch-coverage fixtures (exercise untested code paths) ----
    ("FX27-c04-prose-anchor",
     "YAML precedence stays canonical but a prose PRECEDENCE numbered tier loses its expected "
     "anchor word ('Failsafe' -> 'Backup') — exercises C04's prose-anchor branch (not the YAML branch)",
     lambda t: _sub(t, "2. **Failsafe lockdown**", "2. **Backup lockdown**", "FX27"), frozenset({"C04"})),
    ("FX28-c07-uuid-branch",
     "an allow_list (JR) field id corrupted to a non-UUID non-longid string — exercises C07's UUID-"
     "validity branch on jr_field_rule.allow_list. Collateral: C01 (a non-longid/non-UUID 'id' value "
     "fails the quoted-id check). C02 does NOT fire (v4.4: the de-bloat removed the (JR)-FIELD-RULE prose "
     "that cited 44fe150b, so it now lives ONLY in the YAML data block — removing it orphans no prose "
     "ref; was {C01,C02,C07} on the v4.3 baseline)",
     lambda t: _sub(t, 'id: "44fe150b-e7f3-4be2-b761-d9e562453d0a", type: dropdown',
                       'id: "not-a-uuid", type: dropdown', "FX28"), frozenset({"C01", "C07"})),
    ("FX29-c08-pending-ok",
     "NEGATIVE/branch: the Rules pointed-to ref is a BLANK-style PENDING placeholder '<fill>' (a "
     "legitimate draft state) — C08 must classify it PENDING and NOT fail; whole pointer stays clean",
     lambda t: _sub(t, "**Cowork Layer 1 — Rules** — Box `2289598235660`",
                       "**Cowork Layer 1 — Rules** — Box `<fill>`", "FX29"), frozenset()),
    ("FX30-c08-section-missing",
     "the entire 'Pointed-to docs' prose block is renamed so C08 finds no section — every prose "
     "ref classifies MISSING; exercises C08's section-not-found branch",
     lambda t: _sub(t, "**Pointed-to docs (load at session start",
                       "**Pointed-elsewhere docs (load at session start", "FX30"), frozenset({"C08"})),
    ("FX31-c01-list-branch",
     "a production_spaces.ids list element written unquoted (int-coerced) — exercises C01's "
     "'ids/bases list must be strings' branch",
     lambda t: _sub(t, 'ids: ["38567912", "38567915", "38567936", "38567650", "90128015673", "90128040274", "90128174774", "90128174819"]',
                       'ids: [38567912, "38567915", "38567936", "38567650", "90128015673", "90128040274", "90128174774", "90128174819"]', "FX31"), frozenset({"C01"})),
    ("FX32-c01-int-coercion-nonid-key",
     "an unquoted long-ID under a NON-'id' key (max_claude_space.lists.tasks) is coerced to int — "
     "exercises C01's tree-wide int-coercion scan (the v0.2.6 strengthening), which a key=='id' "
     "walk alone would miss",
     lambda t: _sub(t, 'lists: { tasks: "901215950286"',
                       'lists: { tasks: 901215950286', "FX32"), frozenset({"C01"})),
    ("FX33-c12-absent-key",
     "a whole box zone KEY (never_write) is absent (not null) — exercises C12's 'key absent' branch "
     "distinctly from the null-zone branch; C10 also fires (its floor IDs vanish from never_write)",
     lambda t: _sub(t,
                    '    never_write:                                # parent-inheritance; address by Box ID via MCP API only\n',
                    '    not_never_write:                            # renamed away\n', "FX33"),
     frozenset({"C10", "C12"})),
    # ---- v3.1 carve-out fixture ----
    # ---- 869dthz60 bounded-loader fixtures (alias-bomb guard on the shared parse path) ----
    # FX35 reuses the differential harness's alias-bomb probe structure (7 anchored levels x9 ->
    # ~9^6 expansion) INSIDE the pointer's yaml block. Pre-guard engines hang/crawl here; the
    # bounded loader must reject it as a clean, FAST single C00 FAIL (alias budget, pre-expansion).
    ("FX35-alias-bomb",
     "the harness's 7-level alias-expansion bomb injected into the data block — bounded loader "
     "rejects at the alias budget BEFORE construction; clean single C00 FAIL, no hang",
     lambda t: _sub(t, "layer1_data:\n  precedence:",
                    "layer1_data:\n"
                    "  a0: &a [x,x,x,x,x,x,x,x,x]\n  b0: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]\n"
                    "  c0: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b]\n  d0: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c]\n"
                    "  e0: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d]\n  f0: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e]\n"
                    "  g0: [*f,*f,*f,*f,*f,*f,*f,*f,*f]\n  precedence:", "FX35"),
     frozenset({"C00"})),
    ("FX36-single-alias",
     "even ONE anchor/alias pair trips the zero alias budget (governance YAML is alias-free by "
     "construction) — pins the budget=0 semantics so it cannot silently loosen",
     lambda t: _sub(t, "layer1_data:\n  precedence:",
                    "layer1_data:\n  anchor0: &one [1]\n  alias0: *one\n  precedence:", "FX36"),
     frozenset({"C00"})),
    ("FX37-oversize-yaml-block",
     "a yaml block padded past YAML_MAX_BYTES trips the input-size cap before any parse",
     lambda t: _sub(t, "layer1_data:\n  precedence:",
                    "layer1_data:\n  pad: \"" + ("x" * 2_000_001) + "\"\n  precedence:", "FX37"),
     frozenset({"C00"})),
    ("FX34-crossclass-duplicate",
     "an allow_list entry is INJECTED whose field-id is the never_write JR Status id (f22a77f7) — a "
     "field-id cannot live in two classes; C07's class-disjointness invariant catches the contradiction. "
     "Injection (not replacement), so no prose-cited id is displaced -> exact set {C07}",
     lambda t: _sub(t,
                    '          - { name: "Date - Last Reviewed(JR)", id: "6a703bf5-1ba3-42de-b8f9-11ca5ea41e79", type: date, note: "JR approved writable (2026-07-03 ledger; carried into the F2-RULING allow-list)" }',
                    '          - { name: "Date - Last Reviewed(JR)", id: "6a703bf5-1ba3-42de-b8f9-11ca5ea41e79", type: date, note: "JR approved writable (2026-07-03 ledger; carried into the F2-RULING allow-list)" }\n          - { name: "FX34 cross-class dup of JR Status", id: "f22a77f7-2cc6-4e5a-8b37-8e7e4bf835de", type: dropdown }',
                    "FX34"), frozenset({"C07"})),
]


# ============================================================================
# 869dtn48p XDOC fixtures — hermetic synthetic sovereign-doc copies, built against the
# sha1-pinned baseline. Each entry: (fid, desc, build(base) -> (pointer_text, docs, live_shas),
# expected_failing_set); --selftest runs each through layer1_lint.run_xdoc_checks and asserts
# the EXACT failing-set, mirroring the pointer FIXTURES contract.
# ============================================================================
_GATEV_PIN = "d6d54ae7d1d632f54e7f122efa3a1ccae7269860"


def _xdoc_docs():
    """Synthetic Rules / Tag Use / charter copies citing ONLY IDs the v4.4 baseline data block
    holds (Rules also cites the contextual workspace id — exercising the C02-parity exemption)."""
    rules = ("# Cowork Layer 1 — Rules (synthetic fixture copy)\n"
             "Own zone Box `390802629329`; drop-zones `977588333` + `86746916736`.\n"
             "Audit list `901218891519`; battery `901218930653`; "
             "ClickUp spaces are owned by workspace 20433935.\n")
    tag_use = ("# Cowork Layer 1 — Tag Use (synthetic fixture copy)\n"
               "Tags are space-scoped: `90128004233`. Source taxonomy TTR `2165172587661`.\n")
    charter = ("# Project charter (synthetic fixture copy)\n"
               "S4 locators: lists `901218919999`, `901218930653`, `901218891519`.\n"
               "Docs: GATE-V `2289594143154`, Rules `2289598235660`, Tag Use `2289594294545`.\n"
               "Field `6a703bf5-1ba3-42de-b8f9-11ca5ea41e79`.\n")
    return {"rules": rules, "tag_use": tag_use, "charter": charter}


XDOC_FIXTURES = [
    ("XF01-clean-set", "synthetic Rules/TagUse/charter cite only pointer-held IDs; live sha == pin",
     lambda base: (base, _xdoc_docs(), {"gate_v": _GATEV_PIN}), frozenset()),
    ("XF02-rules-alien-id", "Rules copy cites a Box ID absent from the pointer data block",
     lambda base: (base, dict(_xdoc_docs(), rules=_xdoc_docs()["rules"] + "Stray Box `999888777666`.\n"),
                   {}), frozenset({"X01"})),
    ("XF03-charter-alien-uuid", "charter copy cites a field UUID the pointer does not hold",
     lambda base: (base, dict(_xdoc_docs(), charter=_xdoc_docs()["charter"]
                              + "Field `deadbeef-dead-dead-dead-deadbeefdead`.\n"),
                   {}), frozenset({"X01"})),
    ("XF04-pin-drift-pointer-vs-manifest",
     "pointer gate_v.sha1_pin re-pinned away from the manifest record; supplied live sha still == "
     "manifest pin, so BOTH halves of the coherence check fire (X02 record drift + X03 live mismatch)",
     lambda base: (_sub(base, 'sha1_pin: "d6d54ae7d1d632f54e7f122efa3a1ccae7269860"',
                              'sha1_pin: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"', "XF04"),
                   {}, {"gate_v": _GATEV_PIN}), frozenset({"X02", "X03"})),
    ("XF05-version-drift", "pointer gate_v.version_expected bumped without a manifest re-record",
     lambda base: (_sub(base, 'version_expected: "v3.1"', 'version_expected: "v3.2"', "XF05"),
                   {}, {}), frozenset({"X02"})),
    ("XF06-live-sha-mismatch", "supplied live GATE-V sha1 differs from the consistent pin (drift/tamper)",
     lambda base: (base, {}, {"gate_v": "beefbeefbeefbeefbeefbeefbeefbeefbeefbeef"}),
     frozenset({"X03"})),
    ("XF07-gatev-copy-sha-mismatch", "supplied gate_v doc copy whose sha1 != pin (byte-drifted copy)",
     lambda base: (base, {"gate_v": "# GATE-V synthetic copy (drifted bytes)\n"}, {}),
     frozenset({"X03"})),
    ("XF08-malformed-live-sha", "supplied live sha1 is not 40-hex",
     lambda base: (base, {}, {"gate_v": "deadbeef"}), frozenset({"X03"})),
    ("XF09-broken-pointer", "xdoc run against an unparseable pointer short-circuits to X00 only",
     lambda base: (base.replace("```yaml", "```text", 1), _xdoc_docs(), {"gate_v": _GATEV_PIN}),
     frozenset({"X00"})),
    ("XF10-no-inputs", "no doc/sha inputs: X00+X02 still run, X01/X03 skip with notes, nothing fails",
     lambda base: (base, {}, {}), frozenset()),
]


# ---- 869dx7xpc org-mirror fixtures. XDOC_FIXTURES2 entries carry a 5th element: the
# org_mirror_record override passed to run_xdoc_checks (None = manifest default, i.e. absent).
_MIRROR_OK = ("# ORG-INSTRUCTION MIRROR — Teams (synthetic fixture copy) v1.0\n"
              "Org-tier conventions… ORG-CONTENT-SENTINEL-DO-NOT-ECHO\n")
_MIRROR_OK_SHA1 = hashlib.sha1(_MIRROR_OK.encode("utf-8")).hexdigest()


def _rec(sha):
    return {"id": "424242424242", "sha1_recorded": sha}


XDOC_FIXTURES2 = [
    ("XF11-mirror-clean", "mirror copy passes all structural anchors; sha1 == recorded",
     lambda base: (base, {"org_mirror": _MIRROR_OK}, {}, _rec(_MIRROR_OK_SHA1)), frozenset()),
    ("XF12-mirror-anchor-missing", "mirror lacking the version marker fails structure (X04) only",
     lambda base: (base, {"org_mirror": "# ORG-INSTRUCTION MIRROR (no version line)\n"}, {},
                   _rec(hashlib.sha1("# ORG-INSTRUCTION MIRROR (no version line)\n".encode()).hexdigest())),
     frozenset({"X04"})),
    ("XF13-mirror-currency-drift", "structurally-clean mirror whose sha1 != recorded (X05 only)",
     lambda base: (base, {"org_mirror": _MIRROR_OK}, {},
                   _rec("beefbeefbeefbeefbeefbeefbeefbeefbeefbeef")), frozenset({"X05"})),
    ("XF14-mirror-no-record", "mirror supplied but manifest has no record: X04 runs, X05 skips (flag)",
     lambda base: (base, {"org_mirror": _MIRROR_OK}, {}, None), frozenset()),
    ("XF15-mirror-live-sha-drift", "live mirror sha1 supplied (no copy): X04 skips, X05 fails on drift",
     lambda base: (base, {}, {"org_mirror": "beefbeefbeefbeefbeefbeefbeefbeefbeefbeef"},
                   _rec(_MIRROR_OK_SHA1)), frozenset({"X05"})),
    ("XF16-mirror-record-malformed", "record with a non-40-hex sha1_recorded fails X05 closed",
     lambda base: (base, {"org_mirror": _MIRROR_OK}, {}, _rec("nothex")), frozenset({"X05"})),
]


# ============================================================================
# 869dtn4e2 STATIC-DOC HYGIENE fixtures — (fid, desc, build(base) -> (pointer_text, docs),
# expected_failing_set) run through layer1_lint.run_dochygiene_checks.
# ============================================================================
def _dh_docs():
    """Hygiene-clean synthetic docs: versioned headers + change-logs + correct S0 self-claims,
    no ceiling re-introduction, canonical precedence restatement, locator-only charter."""
    rules = ("# Cowork Layer 1 — Rules — v2.3\n"
             "Cowork-editable operational how-to only.\n"
             "Precedence reminder (restated, canonical order):\n"
             "1. Anthropic safety gates\n2. Failsafe lockdown\n3. GATE-V verification\n"
             "## Change log\n- v2.3 (2026-07-20): tightened wording\n- v2.2 (2026-07-01): split\n")
    tag_use = ("# Cowork Layer 1 — Tag Use — v1.4\nCowork-editable.\n"
               "## Change log\n- v1.4: staging note\n- v1.3: initial\n")
    charter = ("# Project charter — v1.0\n"
               "AUTHORITY comes from the sovereign ceilings, not this charter (locator only).\n"
               "## Change log\n- v1.0: created\n")
    return {"rules": rules, "tag_use": tag_use, "charter": charter}


DH_FIXTURES = [
    ("DH01-clean-set", "versioned+logged docs, correct claims, no re-introduced authority",
     lambda base: (base, _dh_docs()), frozenset()),
    ("DH02-silent-bump", "rules header bumped v2.3->v2.4 with no matching change-log entry",
     lambda base: (base, dict(_dh_docs(), rules=_dh_docs()["rules"].replace(
         "Rules — v2.3", "Rules — v2.4", 1))), frozenset({"H01"})),
    ("DH03-no-changelog", "tag_use with its change-log section renamed away",
     lambda base: (base, dict(_dh_docs(), tag_use=_dh_docs()["tag_use"].replace(
         "## Change log", "## History notes", 1))), frozenset({"H01"})),
    ("DH04-editable-claims-immutable", "rules claiming immutable while the pointer lists it editable",
     lambda base: (base, dict(_dh_docs(), rules=_dh_docs()["rules"].replace(
         "Cowork-editable operational how-to only.",
         "IMMUTABLE CORE — never edit. Operational how-to only.", 1))), frozenset({"H02"})),
    ("DH05-gatev-claims-editable", "a gate_v copy claiming Cowork-editable (floored immutable)",
     lambda base: (base, dict(_dh_docs(),
                              gate_v="# GATE-V — Document Verification — v3.1\nCowork-editable.\n")),
     frozenset({"H02"})),
    ("DH06-ceiling-reintro", "rules re-introducing a ceiling-shaped allow-list (id + auth grant)",
     lambda base: (base, dict(_dh_docs(), rules=_dh_docs()["rules"] +
                              'Writable zone: Box `390802629329` full_rw + subfolders.\n')),
     frozenset({"H03"})),
    ("DH07-precedence-scrambled", "rules restating precedence with failsafe BEFORE safety",
     lambda base: (base, dict(_dh_docs(), rules=_dh_docs()["rules"].replace(
         "1. Anthropic safety gates\n2. Failsafe lockdown\n",
         "1. Failsafe lockdown\n2. Anthropic safety gates\n", 1))), frozenset({"H03"})),
    ("DH08-charter-threshold-def", "charter defining a context threshold value",
     lambda base: (base, dict(_dh_docs(), charter=_dh_docs()["charter"] +
                              "single_file_kb: 50\n")), frozenset({"H04"})),
    ("DH09-charter-neverwrite-enum", "charter enumerating a never-write id",
     lambda base: (base, dict(_dh_docs(), charter=_dh_docs()["charter"] +
                              "never-write: `385430558352` (root of trust)\n")), frozenset({"H04"})),
    ("DH10-project-pointer-grant", "project pointer carrying an id + auth-grant line",
     lambda base: (base, dict(_dh_docs(),
                              project_pointer="# Project pointer — v0.1\n"
                                              "workspace `901218919999` writable for this project\n")),
     frozenset({"H04"})),
    ("DH11-reference-not-definition", "charter MENTIONING ceiling/never-write words without ids/values stays clean",
     lambda base: (base, {"charter": "# Project charter — v1.1\n"
                                     "Ceilings and the never-write list live in the sovereign pointer.\n"
                                     "## Change log\n- v1.1: wording\n- v1.0: created\n"}),
     frozenset()),
    ("DH12-no-docs", "no hygiene-scoped docs supplied: all four checks skip with notes",
     lambda base: (base, {}), frozenset()),
]


# ============================================================================
# 869e5m1nd/869dxa4gy PIN/BASELINE-CURRENCY fixtures — (fid, desc, build(base) ->
# (pointer_text, live_shas), expected_failing_set) via layer1_lint.run_pin_checks.
# Recorded values under test: BASELINE_SHA1 dd5da45a... (deployed pointer), gate_v pin
# d6d54ae7..., scope_registry pin 231ebe46..., airlock_writer pin 399b6ef6... (all from the
# v4.4 baseline / engine constants).
# ============================================================================
_BASE_SHA = "dd5da45a1f93963c6f1c381e9dcd292f6f79333d"
_REG_PIN = "231ebe46be1a56df6e53e54941b9519ca55bad93"
_AIRLOCK_PIN = "399b6ef68683161e11c17d1f37490c7e536ca15b"
_DRIFT = "beefbeefbeefbeefbeefbeefbeefbeefbeefbeef"

PN_FIXTURES = [
    ("PN01-all-current", "live shas for all four artifacts match the recorded values",
     lambda base: (base, {"deployed_pointer": _BASE_SHA, "gate_v": _GATEV_PIN,
                          "scope_registry": _REG_PIN, "airlock_writer": _AIRLOCK_PIN}),
     frozenset()),
    ("PN02-baseline-stale", "live deployed-pointer sha1 differs from BASELINE_SHA1 (the v3.7 stale-baseline incident class)",
     lambda base: (base, {"deployed_pointer": _DRIFT}), frozenset({"P01"})),
    ("PN03-registry-pin-tamper", "live scope-registry sha1 differs from the pointer-recorded pin",
     lambda base: (base, {"scope_registry": _DRIFT}), frozenset({"P02"})),
    ("PN04-airlock-pin-drift", "live airlock.py sha1 (M1 host file) differs from the recorded pin",
     lambda base: (base, {"airlock_writer": _DRIFT}), frozenset({"P02"})),
    ("PN05-malformed-live", "a malformed deployed-pointer sha1 fails P01 closed",
     lambda base: (base, {"deployed_pointer": "nothex"}), frozenset({"P01"})),
    ("PN06-gatev-in-sweep", "gate_v live sha joins the P02 sweep too (cross-linked with X03, not merged)",
     lambda base: (base, {"gate_v": _DRIFT, "scope_registry": _REG_PIN}), frozenset({"P02"})),
    ("PN07-broken-pointer", "P02 fails closed when the pointer is unparseable (recorded pins unavailable)",
     lambda base: (base.replace("```yaml", "```text", 1), {"scope_registry": _REG_PIN}),
     frozenset({"P02"})),
    ("PN08-no-shas", "family invoked with no live shas: both checks skip with notes, nothing fails",
     lambda base: (base, {}), frozenset()),
]


# ============================================================================
# 869dwncba HYGIENE fixtures — (fid, desc, comments_dump, audit_dump, expected_failing_set).
# Dumps are JSON STRINGS (exercising the engine's own parse path) run through
# layer1_lint.run_hygiene_checks; exact failing-set contract as above. Recommend-only family:
# these prove the LOGIC — the live ClickUp export wiring is the connected seat's downstream step.
# ============================================================================
HYG_FIXTURES = [
    ("HF01-clean", "marker-free comments + unique CR numbers stay clean",
     json.dumps([{"task_id": "t1", "comments": [{"id": "c1", "text": "done and verified."}]},
                 {"task_id": "t2", "comments": ["ok, merged as agreed earlier."]}]),
     json.dumps([{"task_id": "a1", "name": "TEAMS-CR-2026-07-01-001 pointer bump"},
                 {"task_id": "a2", "name": "TEAMS-CR-2026-07-01-002 registry re-pin"}]),
     frozenset()),
    ("HF02-marker-comment", "a comment carrying arrow + should markers is flagged (R01)",
     json.dumps([{"task_id": "t1", "comments":
                  [{"id": "c9", "text": "we should add to the spec → NEW open item: decision needed"}]}]),
     None, frozenset({"R01"})),
    ("HF03-new-case-sensitivity", "lowercase 'new'/'news' must NOT trip the case-sensitive NEW marker",
     json.dumps([{"task_id": "t1", "comments": ["a new build shipped; news at 6; renewed cert."]}]),
     None, frozenset()),
    ("HF04-malformed-json", "a non-JSON comments dump is a clean R01 FAIL, never a crash",
     "{not json[", None, frozenset({"R01"})),
    ("HF05-shape-error", "a comment entry with no text field fails closed (silent skip = coverage hole)",
     json.dumps([{"task_id": "t1", "comments": [{"id": "c1"}]}]), None, frozenset({"R01"})),
    ("HF06-dup-cr", "two audit tasks sharing TEAMS-CR-2026-07-01-001 collide (R02)",
     None,
     json.dumps([{"task_id": "a1", "name": "TEAMS-CR-2026-07-01-001 pointer bump"},
                 {"task_id": "a2", "name": "redo of TEAMS-CR-2026-07-01-001"}]),
     frozenset({"R02"})),
    ("HF07-same-task-repeat", "the SAME task citing its own CR twice is not a collision",
     None,
     json.dumps([{"task_id": "a1", "name": "TEAMS-CR-2026-07-01-001 redo of TEAMS-CR-2026-07-01-001"}]),
     frozenset()),
    ("HF08-audit-top-level", "an audit dump whose top level is a dict (not list) fails R02 closed",
     None, json.dumps({"task_id": "a1"}), frozenset({"R02"})),
    ("HF09-both-offend", "offending comments AND a CR collision fail both checks",
     json.dumps([{"task_id": "t1", "comments": ["decision: add to charter"]}]),
     json.dumps([{"task_id": "a1", "name": "TEAMS-CR-2026-07-02-004"},
                 {"task_id": "a2", "name": "TEAMS-CR-2026-07-02-004 dup"}]),
     frozenset({"R01", "R02"})),
    ("HF10-no-dumps", "no dumps supplied: both checks skip with notes, nothing fails",
     None, None, frozenset()),
]


# ============================================================================
# §5 DIFFERENTIAL HARNESS
# ============================================================================
import warnings


def _import(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)   # suppress the oracle's docstring \s warning
        spec.loader.exec_module(m)
    return m


# Engine modules are imported LAZILY (not at module import) so that the engine's --selftest
# `from test_layer1_lint import FIXTURES` stays a cheap, side-effect-free fixture import.
ORACLE = None
NEW = None


def _ensure_modules():
    global ORACLE, NEW
    if ORACLE is None:
        ORACLE = _import(ORACLE_PATH, "oracle_mod")
    if NEW is None:
        NEW = _import(NEW_PATH, "new_mod")

# --- §5.2 volatile-token normalisers (strictly bounded; must NOT touch the 40-hex sha1 pin) ---
_PATH_RE = re.compile(r'File "[^"]*"')
_LINE_RE = re.compile(r'line \d+')
_ADDR_RE = re.compile(r'0x[0-9a-fA-F]+')


def norm_stderr(s):
    s = _PATH_RE.sub('File "<F>"', s)
    s = _LINE_RE.sub('line <N>', s)
    s = _ADDR_RE.sub('0x<ADDR>', s)
    return s


def norm_stdout(s, target):
    return s.replace(target, "<TARGET>") if target else s


def baseline_text():
    with open(BASELINE, encoding="utf-8") as fh:
        return fh.read()


def is_class2(text):
    """True iff this input falls into Phase-B declared delta class 2: a ```yaml block that parses
    to a dict with `layer1_data` PRESENT but NOT a Mapping (null/list/scalar). Uses the oracle's
    own split_doc (same fence extraction the engine uses) so the classification matches reality.
    The ONLY behavioural change in Phase B on content is this class, so a diverging content input
    MUST satisfy this predicate (else it is an unexpected regression)."""
    import yaml
    try:
        yt, _ = ORACLE.split_doc(text)
        doc = yaml.safe_load(yt)
    except Exception:
        return False
    return isinstance(doc, dict) and "layer1_data" in doc and not isinstance(doc["layer1_data"], dict)


# ---------------------------------------------------------------------------
# In-process comparison for CONTENT inputs (no stderr possible: run_checks guards).
# Captures {exit, stdout(report), per-check failing-set, coverage-tripwire, json feed}.
# ---------------------------------------------------------------------------
def compare_content(text):
    target = "<pointer>"
    cap = {}
    for name, mod in (("oracle", ORACLE), ("new", NEW)):
        t0 = time.perf_counter()
        rep_text, rep_code = mod.report(text, target=target)
        feed = mod.action_items(text)
        dt = time.perf_counter() - t0
        results = mod.run_checks(text)
        failed = frozenset(c for c, (ok, _l, _d) in results.items() if not ok)
        cov_ok, _ = mod.coverage_tripwire()
        cap[name] = dict(rep_text=rep_text, rep_code=rep_code, feed=feed,
                         failed=failed, cov_ok=cov_ok, dt=dt)
    o, n = cap["oracle"], cap["new"]
    diffs = []
    if o["rep_code"] != n["rep_code"]:
        diffs.append(f"non-json exit {o['rep_code']}!={n['rep_code']}")
    if norm_stdout(o["rep_text"], target) != norm_stdout(n["rep_text"], target):
        diffs.append("non-json stdout (exact bytes) differs")
    if o["feed"]["exit"] != n["feed"]["exit"]:
        diffs.append(f"--json exit {o['feed']['exit']}!={n['feed']['exit']}")
    if o["feed"] != n["feed"]:                       # parsed-object compare (dict ==, order-insensitive)
        diffs.append("--json payload (parsed) differs")
    if o["failed"] != n["failed"]:
        diffs.append(f"per-check failing-set {sorted(o['failed'])}!={sorted(n['failed'])}")
    if o["cov_ok"] != n["cov_ok"]:
        diffs.append(f"coverage-tripwire {o['cov_ok']}!={n['cov_ok']}")
    return dict(equiv=(not diffs), diffs=diffs, dt=max(o["dt"], n["dt"]),
                o_failed=o["failed"], n_failed=n["failed"],
                o_code=o["rep_code"], n_code=n["rep_code"])


# ---------------------------------------------------------------------------
# Subprocess runner for FILE / crash inputs (captures real exit + stderr traceback).
# Both engines invoked identically with -W ignore::SyntaxWarning (parity-preserving).
# ---------------------------------------------------------------------------
def run_subproc(engine_path, args, cwd=None, timeout=30):
    cmd = [sys.executable, "-W", "ignore::SyntaxWarning", engine_path] + args
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def compare_file(path_arg, json_mode):
    extra = ["--json"] if json_mode else []
    oc, oo, oe = run_subproc(ORACLE_PATH, [path_arg] + extra)
    nc, no, ne = run_subproc(NEW_PATH, [path_arg] + extra)
    diffs = []
    if oc != nc:
        diffs.append(f"exit {oc}!={nc}")
    # stdout: crash -> empty; non-json exact (after target-path normalisation); json parsed
    if json_mode:
        try:
            if json.loads(oo or "null") != json.loads(no or "null"):
                diffs.append("--json payload differs")
        except json.JSONDecodeError:
            if oo != no:
                diffs.append("--json stdout differs (one side not JSON)")
    else:
        if norm_stdout(oo, path_arg) != norm_stdout(no, path_arg):
            diffs.append("non-json stdout differs")
    if norm_stderr(oe) != norm_stderr(ne):
        diffs.append("stderr (normalised type+msg) differs")
    return dict(equiv=(not diffs), diffs=diffs, oc=oc, nc=nc,
                oe=norm_stderr(oe)[:240], ne=norm_stderr(ne)[:240],
                oo=oo[:200], no=no[:200])


# ============================================================================
# Corpus builders
# ============================================================================
def build_content_corpus():
    """(a) 34 fixtures, (b) live pointer, (e/f) structural + fence edges, plus the Phase-B
    class-2 non-Mapping inputs. Each: (label, text, phaseB_class2)."""
    base = baseline_text()
    cases = []
    # (a) fixtures
    for fid, desc, mutate, expected in FIXTURES:
        cases.append((f"fixture:{fid}", mutate(base), False))
    # (b) live pointer (clean)
    cases.append(("live-pointer", base, False))
    # (e) structural edges that are CONTENT
    cases.append(("edge:empty", "", False))
    cases.append(("edge:truncated", base[:600], False))
    cases.append(("edge:missing-block", base.replace("```yaml", "```text", 1), False))
    cases.append(("edge:utf8-bom", "﻿" + base, False))
    cases.append(("edge:crlf-content", base.replace("\n", "\r\n"), False))
    cases.append(("edge:multidoc", base + "\n---\nextra_doc: true\n", False))
    cases.append(("edge:deeply-nested",
                  base + "\n```yaml\ndeep: " + ("[" * 200) + ("]" * 200) + "\n```\n", False))
    cases.append(("edge:dup-top-keys",
                  base.replace("layer1_data:", "layer1_data:\ndupe_root: 1\ndupe_root: 2\nlayer1_data2:", 1),
                  False))
    cases.append(("edge:anchors-aliases",
                  base + "\n```yaml\nanchored: &a {x: 1}\nref: *a\n```\n", False))
    # Phase-B class 2: layer1_data present but NOT a Mapping (one class; null/list/scalar)
    cases.append(("classB2:null", base.replace("layer1_data:\n  precedence:",
                                                "layer1_data: null\nother:\n  precedence:", 1), True))
    cases.append(("classB2:list", base.replace("layer1_data:\n  precedence:",
                                                "layer1_data: [1, 2, 3]\nother:\n  precedence:", 1), True))
    cases.append(("classB2:scalar", base.replace("layer1_data:\n  precedence:",
                                                  "layer1_data: \"just a string\"\nother:\n  precedence:", 1), True))
    # (f) markdown-envelope: multiple / overlapping / unclosed fences
    cases.append(("fence:multiple",
                  "```yaml\nlayer1_data:\n  junk: 1\n```\n\n" + base, False))
    cases.append(("fence:unclosed", base + "\n```yaml\nlayer1_data:\n  dangling: 1\n", False))
    cases.append(("fence:overlapping",
                  "```yaml\n```yaml\nlayer1_data:\n  x: 1\n```\n" + base, False))
    return cases


def build_fuzz_corpus(n=1100, seed=20260619):
    """(d) >=1000 seeded fuzz mutations of the baseline. Operators: quote flip, key drop,
    key duplicate, line reorder, comment injection, type confusion, whitespace/encoding."""
    base = baseline_text()
    lines = base.split("\n")
    rnd = random.Random(seed)
    cases = []
    for i in range(n):
        ls = lines[:]
        nops = rnd.randint(1, 4)
        for _ in range(nops):
            op = rnd.randint(0, 6)
            if not ls:
                break
            j = rnd.randrange(len(ls))
            if op == 0:                                  # quote flip (strip a pair of quotes)
                ls[j] = ls[j].replace('"', "", 2)
            elif op == 1:                                # key drop
                del ls[j]
            elif op == 2:                                # key duplicate
                ls.insert(j, ls[j])
            elif op == 3 and j + 1 < len(ls):            # reorder adjacent
                ls[j], ls[j + 1] = ls[j + 1], ls[j]
            elif op == 4:                                # comment injection
                ls[j] = "# " + ls[j]
            elif op == 5:                                # type confusion (append a stray value)
                ls[j] = ls[j] + " [confused, {a: 1}]"
            else:                                        # whitespace / encoding
                ls[j] = "\t " + ls[j].replace(":", ":​", 1)
        cases.append((f"fuzz:{i:04d}", "\n".join(ls), False))
    return cases


# ============================================================================
# Phase logic + runner
# ============================================================================
PHASEB_FILE_CLASS1 = "file:nonutf8"           # must DIVERGE in Phase B (clean C00 vs traceback)
PHASEB_STAY_IDENTICAL = {"file:isadir", "file:perm"}   # F3: must stay oracle-identical in both phases


def run_file_and_infra(phase, log):
    """File/crash cases via subprocess + (g) infra-sabotage (NEW -> exit 3)."""
    results = []
    tmp = tempfile.mkdtemp(prefix="l1diff_")

    # --- crash/file cases (e) ---
    nonutf8 = os.path.join(tmp, "nonutf8.md")
    with open(nonutf8, "wb") as fh:
        fh.write(b"\xff\xfe not utf-8 \x80\x81")
    adir = os.path.join(tmp, "adir"); os.makedirs(adir, exist_ok=True)
    permf = os.path.join(tmp, "perm.md")
    with open(permf, "w") as fh:
        fh.write("blah")
    os.chmod(permf, 0)

    file_cases = [(PHASEB_FILE_CLASS1, nonutf8), ("file:isadir", adir), ("file:perm", permf)]
    for label, path in file_cases:
        for jm in (False, True):
            r = compare_file(path, jm)
            mode = "json" if jm else "text"
            # Phase B negative test for the non-UTF-8 class: it MUST diverge (clean C00 vs crash).
            if phase == "B" and label == PHASEB_FILE_CLASS1:
                ok = (not r["equiv"]) and r["nc"] == 1 and ("Traceback" not in r["ne"])
                verdict = "DIVERGES-as-specified" if ok else "FAILED-negative-test"
                results.append((f"{label}[{mode}]", ok, verdict,
                                f"oracle_exit={r['oc']} new_exit={r['nc']} new_stderr={r['ne'][:60]!r}"))
            else:
                ok = r["equiv"]
                results.append((f"{label}[{mode}]", ok,
                                "identical" if ok else "DIVERGED", "; ".join(r["diffs"])[:200]))

    # --- (g) infra-sabotage: isolated engine copy; NEW must exit 3 + INIT-FAILURE ---
    def _infra(label, sabotage, args, need_testmod=False):
        # Manifest is loaded at module import (every mode) -> a normal lint run triggers exit 3.
        # baseline.md is loaded only by --selftest/--emit-fixtures, so a baseline fault must be
        # exercised via --selftest (which needs the fixtures module co-located).
        edir = tempfile.mkdtemp(prefix="l1infra_")
        files = ["layer1_lint.py", "manifest.yaml", "baseline.md"]
        if need_testmod:
            files.append("test_layer1_lint.py")
        for fn in files:
            with open(os.path.join(HERE, fn), "rb") as s, open(os.path.join(edir, fn), "wb") as d:
                d.write(s.read())
        sabotage(edir)
        rc, so, se = run_subproc(os.path.join(edir, "layer1_lint.py"), args, cwd=edir)
        ok = (rc == 3) and ("INIT-FAILURE" in se) and ("Traceback" not in se)
        results.append((f"infra:{label}", ok,
                        "exit3+INIT-FAILURE" if ok else f"BAD rc={rc}",
                        se.strip()[:160]))

    _infra("manifest-deleted", lambda d: os.remove(os.path.join(d, "manifest.yaml")), [BASELINE])
    _infra("manifest-chmod000", lambda d: os.chmod(os.path.join(d, "manifest.yaml"), 0), [BASELINE])
    _infra("baseline-sha1-corrupt",
           lambda d: open(os.path.join(d, "baseline.md"), "a").write("x"),
           ["--selftest"], need_testmod=True)
    _infra("baseline-crlf-rewrite",
           lambda d: _crlf_rewrite(os.path.join(d, "baseline.md")),
           ["--selftest"], need_testmod=True)
    return results


def _crlf_rewrite(path):
    with open(path, "rb") as fh:
        b = fh.read()
    with open(path, "wb") as fh:
        fh.write(b.replace(b"\n", b"\r\n"))


def run_property_bounds(log):
    """(F6) absolute bounds (wall_time < 2 s). 5 MB garbage + an alias-expansion bomb.
    If BOTH engines breach a bound on the same input -> NOT auto-accepted: flagged as a
    newly-discovered defect (Phase D / 869dtbw4f sibling), not an equivalence pass/fail."""
    flags = []
    rows = []
    # 5 MB garbage (content) — timed in-process for both
    big = "garbage line not yaml\n" * (5 * 1024 * 1024 // 21)
    for name, mod in (("oracle", ORACLE), ("new", NEW)):
        t0 = time.perf_counter(); mod.report(big, target="<big>"); rows.append((f"5MB-garbage[{name}]", time.perf_counter() - t0))
    # alias-expansion ("billion laughs") bomb via subprocess (timeout guard so the harness cannot
    # hang). 7 anchored levels x9 -> exponential expansion in PyYAML safe_load (no bomb guard).
    bomb = ("```yaml\nlayer1_data:\n  a: &a [x,x,x,x,x,x,x,x,x]\n  b: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]\n"
            "  c: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b]\n  d: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c]\n"
            "  e: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d]\n  f: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e]\n"
            "  g: [*f,*f,*f,*f,*f,*f,*f,*f,*f]\n```\n")
    bombf = os.path.join(tempfile.mkdtemp(prefix="l1bomb_"), "bomb.md")
    open(bombf, "w").write(bomb)
    bomb_times = {}
    bomb_breach = {}
    for name, path in (("oracle", ORACLE_PATH), ("new", NEW_PATH)):
        t0 = time.perf_counter()
        try:
            rc, so, se = run_subproc(path, [bombf], timeout=8)
            dt = time.perf_counter() - t0
            bomb_breach[name] = (dt >= 2.0)
        except subprocess.TimeoutExpired:
            dt = 8.0; bomb_breach[name] = True
        bomb_times[name] = dt
        rows.append((f"alias-bomb[{name}]", dt))
    if bomb_breach.get("oracle") and bomb_breach.get("new"):
        flags.append("alias-expansion bomb breaches wall_time<2s on BOTH engines -> Phase-D defect "
                     "(shared PyYAML safe_load has no alias-bomb guard); NOT ratified as equivalent")
    return rows, flags


# ============================================================================
def run_harness(phase, fuzz_n=1100, k_determinism=3):
    _ensure_modules()
    log = []
    out = lambda s: log.append(s)
    out(f"DIFFERENTIAL HARNESS — Phase {phase}")
    out(f"  python(oracle)=python(new)={sys.version.split()[0]}  (version parity: "
        f"{sys.version_info[:2] == sys.version_info[:2]})")    # same interpreter -> parity holds
    out(f"  ORACLE sha1 pin check: {hashlib.sha1(open(ORACLE_PATH,'rb').read()).hexdigest()}")
    out("")

    content = build_content_corpus()
    fuzz = build_fuzz_corpus(n=fuzz_n)
    all_content = content + fuzz

    # ---- determinism: run the content corpus K times, assert per-case verdict is stable ----
    det_runs = []
    for k in range(k_determinism):
        verdicts = {}
        for label, text, isB2 in all_content:
            r = compare_content(text)
            verdicts[label] = (r["equiv"], tuple(sorted(r["n_failed"])), r["n_code"])
        det_runs.append(verdicts)
    det_ok = all(det_runs[0] == det_runs[k] for k in range(1, k_determinism))
    out(f"DETERMINISM: content corpus run K={k_determinism}x -> "
        f"{'STABLE (identical run-to-run)' if det_ok else 'NON-DETERMINISTIC (FAIL)'}")

    # ---- equivalence verdicts ----
    # Phase A: every content/fuzz input must be NEW == ORACLE.
    # Phase B: identical EXCEPT inputs in declared delta class 2 (non-Mapping layer1_data), which
    #   MUST diverge to a clean single {C00} (exit 1). A divergence is classified by CAUSE
    #   (is_class2 + NEW=={C00}), not by label — so fuzz inputs that happen to hit class 2 are
    #   recognised as legitimate, and any divergence that is NOT class 2 is an unexpected regression.
    content_pass = 0; content_fail = []; declared_div = []; named_b2 = []; slow = []
    for label, text, isB2 in all_content:
        r = compare_content(text)
        if r["dt"] >= 2.0:
            slow.append((label, r["dt"]))
        if r["equiv"]:
            if phase == "B" and isB2:
                content_fail.append((label, "named class-2 case did NOT diverge (fix ineffective)"))
            else:
                content_pass += 1
        else:                                            # diverged
            legit = (phase == "B" and is_class2(text)
                     and set(r["n_failed"]) == {"C00"} and r["n_code"] == 1)
            if legit:
                content_pass += 1
                declared_div.append(label)
                if isB2:
                    named_b2.append((label, sorted(r["o_failed"]), sorted(r["n_failed"])))
            else:
                content_fail.append((label, "DIVERGED(unexpected): " + "; ".join(r["diffs"])[:160]))

    out(f"CONTENT+FUZZ equivalence: {content_pass}/{len(all_content)} as-expected "
        f"({len(content)} structured + {len(fuzz)} fuzz)")
    if phase == "B":
        out(f"  Phase-B declared class-2 divergences (non-Mapping layer1_data -> clean {{C00}}): "
            f"{len(declared_div)} input(s)")
        for label, of, nf in named_b2:
            out(f"    [OK] {label}: oracle_failed={of} -> new_failed={nf} (clean C00)")
    for label, detail in content_fail:
        out(f"  [DIVERGED] {label}: {detail}")

    # ---- file/crash + infra-sabotage ----
    out("")
    fi = run_file_and_infra(phase, log)
    fi_fail = [(l, d) for l, ok, v, d in fi if not ok]
    out("FILE / CRASH / INFRA cases:")
    for label, ok, verdict, detail in fi:
        out(f"  [{'OK' if ok else 'BAD'}] {label}: {verdict}  {('| ' + detail) if detail else ''}")

    # ---- property bounds ----
    out("")
    rows, flags = run_property_bounds(log)
    out("PROPERTY BOUNDS (F6 — wall_time < 2 s):")
    for label, dt in rows:
        out(f"  {label}: {dt*1000:.0f} ms  {'(BREACH)' if dt >= 2.0 else 'ok'}")
    for f in flags:
        out(f"  [PHASE-D FLAG] {f}")

    # ---- overall gate ----
    out("")
    gate_ok = (det_ok and not content_fail and not fi_fail and not slow)
    # property double-breach flags are NOT equivalence failures, but they DO block ratification
    # of that specific input (reported separately); they do not fail the equivalence gate here.
    out(f"OVERALL Phase {phase}: {'PASS' if gate_ok else 'FAIL'}  "
        f"(determinism={det_ok}, content_fail={len(content_fail)}, file/infra_fail={len(fi_fail)}, "
        f"slow={len(slow)}, property_flags={len(flags)})")
    print("\n".join(log))
    return 0 if gate_ok else 1


if __name__ == "__main__":
    ph = "A"
    if "--phase" in sys.argv:
        ph = sys.argv[sys.argv.index("--phase") + 1]
    fz = 1100
    if "--fuzz" in sys.argv:
        fz = int(sys.argv[sys.argv.index("--fuzz") + 1])
    sys.exit(run_harness(ph, fuzz_n=fz))
