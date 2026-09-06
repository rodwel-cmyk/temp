#!/usr/bin/env python3
# ============================================================================
# PROTOTYPE - NOT COMMITTED / NOT GOVERNED
# Oracle generator (S2) - minimal deterministic generator + parallel-validation
# + fail-closed anchor demo. Sandbox only. Authority: NONE.
#
#   - Reads rules-as-data (rules_as_data.yaml, S1) as the single source of truth.
#   - Obtains each path's sha1 from a corpus source (live inventory OR a sealed
#     SETPIN manifest) - hash-not-ingest: it consumes recorded sha1s, it never
#     reads the corpus files' contents.
#   - Applies the documented _set_sha1 aggregation (verbatim from source).
#   - Emits the TWO-LEVEL pin: engine-set SECTION (SET layer) + harness SECTION
#     (FILE layer), each pinned separately, plus a manifest entry.
#   - Deterministic: sorted inputs, NO timestamps in the hashed body or manifest.
#
# NOT the governed build. The governed commit runs on the Code-CLI seat under
# GATE-V (see README-PROTOTYPE.md).
# ============================================================================
import argparse, hashlib, json, os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.normpath(os.path.join(HERE, ".."))          # Level 1 - Dev
DEF_INVENTORY = os.path.join(SEEDS, "inventory-390802629329-2026-09-04-1650Z.json")
DEF_SETPIN    = os.path.join(SEEDS, "l1-fixrun-2026-07-30", "build-inputs",
                             "oracle-model-SETPIN-2026-07-28.json")
RULES         = os.path.join(HERE, "rules_as_data.yaml")


# ---- the aggregation, verbatim from source --------------------------------
# SET-IDENTITY-live-computation-2026-09-04.md (read from harness Box 2384141567519
# lines 666-675). This single implementation is the aggregation of record.
def set_sha1(entries):
    """sha1 over the SORTED (relpath, per-file sha1) manifest,
    serialised as 'relpath\\x00sha1\\n' per entry."""
    h = hashlib.sha1()
    for rel, sha in sorted(entries):
        h.update(rel.encode("utf-8")); h.update(b"\x00")
        h.update(sha.encode("ascii")); h.update(b"\n")
    return h.hexdigest()


# ---- corpus adapters (obtain per-file sha1; never ingest file contents) ----
def corpus_from_inventory(inventory_path, root_folder_id):
    """Resolve {relpath: sha1} for files under the given Box folder id, using the
    inventory's recorded server-side sha1s. Scoping to the folder id disambiguates
    the many same-named copies elsewhere in the tree (e.g. baseline.md x6)."""
    items = json.load(open(inventory_path))
    root = next((x for x in items if str(x.get("id")) == str(root_folder_id)), None)
    if root is None:
        raise SystemExit("inventory: root folder id %s not found" % root_folder_id)
    prefix = root["_path"].rstrip("/") + "/"
    out = {}
    for x in items:
        if x.get("type") == "file" and x.get("_path", "").startswith(prefix):
            out[x["_path"][len(prefix):]] = x.get("sha1")
    return out, {"kind": "inventory", "path": os.path.basename(inventory_path),
                 "root_folder_id": str(root_folder_id), "root_path": root["_path"]}


def corpus_from_setpin(setpin_path):
    """Sealed SETPIN manifest: schema l1-oracle-model-setpin-v1 -> {"files": {relpath: sha1}}."""
    d = json.load(open(setpin_path))
    return dict(d["files"]), {"kind": "setpin", "path": os.path.basename(setpin_path),
                              "schema": d.get("schema"), "recorded_utc": d.get("recorded_utc")}


def corpus_from_json(path):
    """Flat {"files": {relpath: sha1}} read from live Box at a stated moment.
    Used by the S10 re-pin dry run: it re-derives the pin from CURRENT server-side
    sha1s rather than a dated inventory snapshot (BARRED-13 - never carry a pin)."""
    d = json.load(open(path))
    return dict(d["files"]), {"kind": "boxlive", "path": os.path.basename(path),
                              "read_at": d.get("_read_at"),
                              "source_folders": d.get("_source_folders")}


def load_corpus(source, inventory_path, setpin_path, root_folder_id, boxlive_path=None):
    if source == "live":
        return corpus_from_inventory(inventory_path, root_folder_id)
    if source == "sealed":
        return corpus_from_setpin(setpin_path)
    if source == "boxlive":
        if not boxlive_path:
            raise SystemExit("source=boxlive needs --boxlive <corpus.json>")
        c, m = corpus_from_json(boxlive_path)
        if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):
            raise SystemExit("boxlive corpus root folder id mismatch")
        return c, m
    raise SystemExit("unknown source: %s" % source)


# ---- generator ------------------------------------------------------------
def load_rules():
    return yaml.safe_load(open(RULES))


# ---- S5: version lock -----------------------------------------------------
# Two independent facts, both stamped into the manifest and both re-checked by
# the lock: the DECLARED rules_version, and a DIGEST of the rules bytes. Either
# alone is spoofable - a bumped version over unchanged rules, or edited rules
# under a stale version. Absence of either is a refuse, never a pass.
def rules_digest():
    """sha1 of rules_as_data.yaml as bytes. Content identity, not a timestamp."""
    return hashlib.sha1(open(RULES, "rb").read()).hexdigest()


def rules_version(rules):
    v = rules.get("rules_version")
    if not v:
        raise SystemExit("FAIL-CLOSED: rules_as_data.yaml declares no rules_version")
    return v


def version_block(rules):
    return {"oracle_version": rules_version(rules), "rules_digest": rules_digest()}


def check_version_lock(manifest, rules):
    """Fail-closed comparison. Returns (ok, [reasons]); absence counts against."""
    want = version_block(rules)
    got_v = manifest.get("oracle_version")
    got_d = manifest.get("rules_digest")
    reasons = []
    if not got_v:
        reasons.append("manifest declares no oracle_version")
    elif got_v != want["oracle_version"]:
        reasons.append("oracle_version %s != rules_version %s" % (got_v, want["oracle_version"]))
    if not got_d:
        reasons.append("manifest declares no rules_digest")
    elif got_d != want["rules_digest"]:
        reasons.append("rules_digest %s != current rules %s (rules edited without a version bump)"
                       % (got_d[:12], want["rules_digest"][:12]))
    return (not reasons), reasons


def section_by_id(rules, sid):
    return next(s for s in rules["sections"] if s["id"] == sid)


def resolve_members(members, corpus):
    missing = [m for m in members if not corpus.get(m)]
    if missing:
        raise SystemExit("corpus missing sha1 for: %s" % ", ".join(missing))
    return [(m, corpus[m]) for m in members]


# ---- S8: section-generic build --------------------------------------------
# One builder per SECTION KIND, dispatched from the rules-data. Adding section
# N+1 is a rules_as_data.yaml edit - a new entry under `sections:` - and needs
# NO change here. That is the whole point of "sectioned": the code knows about
# kinds, never about particular sections.
def build_set_section(sec, corpus):
    """kind: set - a set-sha1 over members_ordered, plus any declared subsets.
    `pin_keys.subsets` maps an output key -> the relpaths that key excludes."""
    entries = resolve_members(sec["members_ordered"], corpus)
    keys = sec["pin_keys"]
    out = {
        "layer": "SET",
        "members": [[r, s] for (r, s) in sorted(entries)],
        keys["full"]: set_sha1(entries),
    }
    for key, excluded in sorted((keys.get("subsets") or {}).items()):
        drop = set(excluded)
        out[key] = set_sha1([(r, s) for (r, s) in entries if r not in drop])
    return out


def build_file_section(sec, corpus):
    """kind: file - a single governed file, pinned in its own right."""
    sha = corpus.get(sec["relpath"])
    if not sha:
        raise SystemExit("corpus missing file %s (section %s)" % (sec["relpath"], sec["id"]))
    return {"layer": "FILE", "relpath": sec["relpath"], "file_sha1": sha}


BUILDERS = {"set": build_set_section, "file": build_file_section}


def generate(rules, corpus, corpus_meta):
    """Build every section declared in the rules-data. Deterministic, no timestamps."""
    sections = {}
    for sec in rules["sections"]:
        builder = BUILDERS.get(sec["kind"])
        if builder is None:
            raise SystemExit("FAIL-CLOSED: section %s has unknown kind %r"
                             % (sec["id"], sec["kind"]))
        sections[sec["id"]] = builder(sec, corpus)

    manifest = {
        "schema": "oracle-generator-manifest-v0-PROTOTYPE",
        "aggregation": rules["aggregation"]["id"],
        # S5: version-lock stamp. Deterministic - a version string and a content
        # digest, not a timestamp, so the manifest stays byte-stable across runs.
        "oracle_version": version_block(rules)["oracle_version"],
        "rules_digest": version_block(rules)["rules_digest"],
        "corpus_source": corpus_meta,
        "sections": sections,
    }
    return manifest


def emit_json(obj):
    # sort_keys keeps the file byte-deterministic across runs
    return json.dumps(obj, indent=2, sort_keys=True)


# ---- expected-pin helpers -------------------------------------------------
def exp(rules, sid, key):
    return section_by_id(rules, sid)["expected_pins"][key]


# ---- subcommands ----------------------------------------------------------
def cmd_gen(a):
    rules = load_rules()
    eng = section_by_id(rules, "engine_set")
    corpus, meta = load_corpus(a.source, a.inventory, a.setpin,
                               eng["corpus_root_folder_id"], a.boxlive)
    m = generate(rules, corpus, meta)
    txt = emit_json(m)
    if a.out:
        open(a.out, "w").write(txt + "\n")
        print("wrote", a.out, file=sys.stderr)
    print(txt)


def _row(label, computed, expected, status, positive_expected=True):
    ok = (computed == expected)
    verdict = "MATCH" if ok else "MISMATCH"
    return ok, "%-26s %s  computed=%s  expected=%s  [%s]" % (
        label, verdict.ljust(8), computed, expected, status)


def cmd_validate(a):
    rules = load_rules()
    eng = section_by_id(rules, "engine_set")
    root = eng["corpus_root_folder_id"]

    live_c, live_m = load_corpus("live", a.inventory, a.setpin, root)
    seal_c, seal_m = load_corpus("sealed", a.inventory, a.setpin, root)
    live = generate(rules, live_c, live_m)
    seal = generate(rules, seal_c, seal_m)

    print("=" * 78)
    print("PARALLEL VALIDATION (PROTOTYPE)  - generator vs hand-computed pins")
    print("live   corpus:", live_m["path"])
    print("sealed corpus:", seal_m["path"])
    print("=" * 78)
    all_ok = True
    rows = [
        ("engine15  (live)",  live["sections"]["engine_set"]["engine15_set_sha1"],
         exp(rules, "engine_set", "engine15_set_sha1")),
        ("set16     (live)",  live["sections"]["engine_set"]["set16_set_sha1"],
         exp(rules, "engine_set", "set16_set_sha1_live")),
        ("harness   (live)",  live["sections"]["harness"]["file_sha1"],
         exp(rules, "harness", "file_sha1_live")),
        ("engine15  (sealed)", seal["sections"]["engine_set"]["engine15_set_sha1"],
         exp(rules, "engine_set", "engine15_set_sha1")),
        ("set16     (sealed)", seal["sections"]["engine_set"]["set16_set_sha1"],
         exp(rules, "engine_set", "set16_set_sha1_sealed")),
        ("harness   (sealed)", seal["sections"]["harness"]["file_sha1"],
         exp(rules, "harness", "file_sha1_sealed")),
    ]
    for label, computed, e in rows:
        ok, line = _row(label, computed, e["value"], e["status"])
        all_ok = all_ok and ok
        print(line)
    print("-" * 78)
    key = seal["sections"]["engine_set"]["set16_set_sha1"]
    exp_seal = exp(rules, "engine_set", "set16_set_sha1_sealed")["value"]
    print("KEY TEST - sealed set-sha1 reproduces ccda6511: %s" %
          ("MATCH" if key == exp_seal else "MISMATCH -> %s" % key))
    print("OVERALL:", "ALL MATCH - generator is faithful" if all_ok else "MISMATCH present")
    return 0 if all_ok else 1


def _anchor(computed, pinned, negative_guard=None):
    """Fail-closed anchor: PASS iff computed == pinned. A computed value equal to
    the NEGATIVE-GUARD (dead/sealed) is an explicit FAIL even before the pin check."""
    if negative_guard and computed == negative_guard:
        return "FAIL", "computed == NEGATIVE-GUARD (dead sealed value) - refuse"
    if computed == pinned:
        return "PASS", "computed == pinned"
    return "FAIL", "computed != pinned"


def cmd_anchor_demo(a):
    rules = load_rules()
    eng = section_by_id(rules, "engine_set")
    root = eng["corpus_root_folder_id"]
    live_c, live_m = load_corpus("live", a.inventory, a.setpin, root)
    seal_c, _ = load_corpus("sealed", a.inventory, a.setpin, root)

    pin_live = exp(rules, "engine_set", "set16_set_sha1_live")["value"]
    neg_guard = exp(rules, "engine_set", "set16_set_sha1_sealed")["value"]

    print("=" * 78)
    print("ANCHOR FAIL-CLOSED DEMO (PROTOTYPE)")
    print("pinned (live SET pin) :", pin_live)
    print("negative guard (dead) :", neg_guard)
    print("=" * 78)

    # (1) PASS - clean live corpus
    live = generate(rules, live_c, live_m)
    c1 = live["sections"]["engine_set"]["set16_set_sha1"]
    v, why = _anchor(c1, pin_live, neg_guard)
    print("[1] clean live corpus         -> %-4s  (%s)  computed=%s" % (v, why, c1))

    # (2) FAIL - deliberate single-byte perturbation of one member's sha1
    perturbed = dict(live_c)
    victim = "l1lint/engine.py"
    perturbed[victim] = "0" * 40
    lm = dict(live_m); lm["note"] = "PERTURBED %s -> 000...0" % victim
    p = generate(rules, perturbed, lm)
    c2 = p["sections"]["engine_set"]["set16_set_sha1"]
    v, why = _anchor(c2, pin_live, neg_guard)
    print("[2] perturbed %-16s-> %-4s  (%s)  computed=%s" % (victim, v, why, c2))

    # (3) FAIL - stale-harness regression: swap the harness member back to the
    #     pre-fix file, which collapses the set-sha1 onto the dead sealed value.
    stale = dict(live_c)
    stale["test_layer1_lint.py"] = seal_c["test_layer1_lint.py"]
    sm = dict(live_m); sm["note"] = "STALE HARNESS (pre-fix 3574c2d1) swapped in"
    s = generate(rules, stale, sm)
    c3 = s["sections"]["engine_set"]["set16_set_sha1"]
    v, why = _anchor(c3, pin_live, neg_guard)
    print("[3] stale harness (3574c2d1)  -> %-4s  (%s)  computed=%s" % (v, why, c3))
    print("-" * 78)
    print("Expected: [1] PASS, [2] FAIL, [3] FAIL (trips the negative guard).")


def cmd_version_lock(a):
    """S5: refuse when a manifest's stamp disagrees with the current rules."""
    rules = load_rules()
    manifest = json.load(open(a.manifest))
    ok, reasons = check_version_lock(manifest, rules)
    print("=" * 78)
    print("VERSION LOCK (S5) -", os.path.basename(a.manifest))
    print("=" * 78)
    print("rules_version : %s" % rules_version(rules))
    print("rules_digest  : %s" % rules_digest())
    print("manifest      : oracle_version=%s rules_digest=%s"
          % (manifest.get("oracle_version"), (manifest.get("rules_digest") or "")[:12] or None))
    print("-" * 78)
    if ok:
        print("VERDICT: LOCKED - oracle_version == rules_version and rules unedited")
        return 0
    for r in reasons:
        print("REFUSE:", r)
    print("VERDICT: REFUSED (fail-closed) - regenerate before trusting this manifest")
    return 1


def cmd_repin_dryrun(a):
    """S10 re-pin DRY RUN. Re-derives every pin from CURRENT server-side sha1s and
    compares against the recorded expected pins. WRITES NOTHING - it reports drift
    so a human can decide, which is the only thing BARRED-13 permits without a
    fresh derivation at write time."""
    rules = load_rules()
    eng = section_by_id(rules, "engine_set")
    corpus, meta = load_corpus("boxlive", a.inventory, a.setpin,
                               eng["corpus_root_folder_id"], a.boxlive)
    m = generate(rules, corpus, meta)

    print("=" * 78)
    print("S10 RE-PIN DRY RUN - re-derived from LIVE Box, nothing written")
    print("corpus : %s (read %s)" % (meta["path"], meta.get("read_at")))
    print("folders: %s" % meta.get("source_folders"))
    print("=" * 78)

    rows = [
        ("engine_set.engine15", m["sections"]["engine_set"]["engine15_set_sha1"],
         exp(rules, "engine_set", "engine15_set_sha1")),
        ("engine_set.set16", m["sections"]["engine_set"]["set16_set_sha1"],
         exp(rules, "engine_set", "set16_set_sha1_live")),
        ("harness.file", m["sections"]["harness"]["file_sha1"],
         exp(rules, "harness", "file_sha1_live")),
    ]
    drift = []
    for label, got, e in rows:
        ok = (got == e["value"])
        if not ok:
            drift.append(label)
        print("%-22s %-9s re-derived=%s  recorded=%s" %
              (label, "MATCH" if ok else "DRIFT", got, e["value"]))

    guard = exp(rules, "engine_set", "set16_set_sha1_sealed")["value"]
    tripped = (m["sections"]["engine_set"]["set16_set_sha1"] == guard)
    print("-" * 78)
    print("negative guard tripped: %s" % ("YES - REFUSE" if tripped else "no"))
    if drift:
        print("VERDICT: DRIFT on %s - the live corpus no longer matches the recorded pin." % ", ".join(drift))
        print("         S9 must NOT proceed on the recorded value. Re-derive at write time.")
        return 1
    print("VERDICT: NO DRIFT - live corpus still yields the recorded pins.")
    print("         Still not authorisation to write: S9 re-derives at write time (BARRED-13).")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Oracle generator PROTOTYPE (not governed)")
    ap.add_argument("--inventory", default=DEF_INVENTORY)
    ap.add_argument("--setpin", default=DEF_SETPIN)
    ap.add_argument("--boxlive", default=os.path.join(HERE, "corpus-boxlive-2026-09-06.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="emit two-level pin + manifest for one corpus source")
    g.add_argument("--source", choices=["live", "sealed", "boxlive"], default="live")
    g.add_argument("--out")
    g.set_defaults(fn=cmd_gen)

    v = sub.add_parser("validate", help="reproduce published pins; MATCH/MISMATCH table")
    v.set_defaults(fn=cmd_validate)

    an = sub.add_parser("anchor-demo", help="fail-closed anchor: a pass and two fails")
    an.set_defaults(fn=cmd_anchor_demo)

    vl = sub.add_parser("version-lock", help="S5: refuse a manifest whose stamp != current rules")
    vl.add_argument("manifest")
    vl.set_defaults(fn=cmd_version_lock)

    rp = sub.add_parser("repin-dryrun", help="S10: re-derive pins from live Box; report drift, write nothing")
    rp.set_defaults(fn=cmd_repin_dryrun)

    a = ap.parse_args()
    rc = a.fn(a)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
