#!/usr/bin/env python3
# ============================================================================
# PROTOTYPE - NOT COMMITTED / NOT GOVERNED
# Oracle generator (S7) - shadow-lint of a GENERATED section. Sandbox only.
# Authority: NONE. No Box write. No ClickUp write. No governed commit.
#
# SHADOW is the default and always exits 0: findings are recommendations, and
# the linter cannot block anything until it is explicitly promoted with
# --enforce. That ordering is the point of S7 - the linter runs against
# generated output long before it is allowed to fail-closed on live governance.
#
# Every run reports its own COVERAGE: checks passed, failed, and SKIPPED with
# the reason. A check that could not run is never silently counted as a pass.
# (A8 2026-09-04 lesson: a hash sweep that errored on 92 of 1,700 files would
# have read as a clean negative if it had not reported its own gaps.)
# ============================================================================
import argparse, json, os, re, sys

import oracle_gen as G

HEX40 = re.compile(r"^[0-9a-f]{40}$")

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


class Report(object):
    """Collects per-check verdicts and refuses to lose a SKIP."""

    def __init__(self):
        self.rows = []

    def add(self, cid, verdict, detail):
        self.rows.append((cid, verdict, detail))

    def count(self, verdict):
        return sum(1 for _, v, _ in self.rows if v == verdict)

    def failed(self):
        return [r for r in self.rows if r[1] == FAIL]


# ---- checks ---------------------------------------------------------------
# Each returns (verdict, detail). A check that cannot establish its own
# precondition returns SKIP with the reason - never PASS.

def c_version_lock(m, rules, rep):
    ok, reasons = G.check_version_lock(m, rules)
    rep.add("L1 version_lock", PASS if ok else FAIL,
            "stamp matches current rules" if ok else "; ".join(reasons))


def c_member_completeness(m, rules, rep):
    eng = G.section_by_id(rules, "engine_set")
    want = list(eng["members_ordered"])
    sec = m.get("sections", {}).get("engine_set")
    if not sec:
        return rep.add("L2 member_completeness", SKIP, "manifest has no engine_set section")
    got = [r for r, _ in sec.get("members", [])]
    missing = [x for x in want if x not in got]
    extra = [x for x in got if x not in want]
    if missing or extra:
        rep.add("L2 member_completeness", FAIL,
                "missing=%s extra=%s" % (missing or "none", extra or "none"))
    else:
        rep.add("L2 member_completeness", PASS, "all %d declared members present, no extras" % len(want))


def c_no_duplicates(m, rules, rep):
    sec = m.get("sections", {}).get("engine_set")
    if not sec:
        return rep.add("L3 no_duplicate_relpaths", SKIP, "manifest has no engine_set section")
    rels = [r for r, _ in sec.get("members", [])]
    dupes = sorted(set(x for x in rels if rels.count(x) > 1))
    rep.add("L3 no_duplicate_relpaths", FAIL if dupes else PASS,
            ("duplicated: %s" % ", ".join(dupes)) if dupes else "%d distinct relpaths" % len(rels))


def c_sha1_wellformed(m, rules, rep):
    bad = []
    sec = m.get("sections", {}).get("engine_set", {})
    for r, s in sec.get("members", []):
        if not (isinstance(s, str) and HEX40.match(s)):
            bad.append(r)
    h = m.get("sections", {}).get("harness", {}).get("file_sha1")
    if h is not None and not (isinstance(h, str) and HEX40.match(h)):
        bad.append("harness:file_sha1")
    if not sec.get("members") and h is None:
        return rep.add("L4 sha1_wellformed", SKIP, "no sha1 fields found to check")
    rep.add("L4 sha1_wellformed", FAIL if bad else PASS,
            ("malformed: %s" % ", ".join(bad)) if bad else "all sha1s are 40-char lowercase hex")


def c_set_pin_self_consistent(m, rules, rep):
    """Recompute both pins from the manifest's OWN recorded members. Catches a
    hand-edited manifest whose pin no longer follows from its member list."""
    # Section-generic (S8): every declared set section, every declared pin key.
    bad, checked = [], 0
    for rsec in [s for s in rules["sections"] if s["kind"] == "set"]:
        msec = m.get("sections", {}).get(rsec["id"])
        if not msec or not msec.get("members"):
            continue
        entries = [(r, s) for r, s in msec["members"]]
        keys = rsec["pin_keys"]
        want = {keys["full"]: G.set_sha1(entries)}
        for key, excluded in (keys.get("subsets") or {}).items():
            drop = set(excluded)
            want[key] = G.set_sha1([e for e in entries if e[0] not in drop])
        for key, recomputed in sorted(want.items()):
            checked += 1
            if recomputed != msec.get(key):
                bad.append("%s.%s recomputes to %s, manifest says %s"
                           % (rsec["id"], key, recomputed[:12], str(msec.get(key))[:12]))
    if not checked:
        return rep.add("L5 set_pin_self_consistent", SKIP, "no set section in the manifest records members")
    rep.add("L5 set_pin_self_consistent", FAIL if bad else PASS,
            "; ".join(bad) if bad else "all %d pin(s) follow from the recorded members" % checked)


def c_negative_guard(m, rules, rep):
    guard = G.exp(rules, "engine_set", "set16_set_sha1_sealed")
    sec = m.get("sections", {}).get("engine_set")
    if not sec:
        return rep.add("L6 negative_guard_not_live", SKIP, "manifest has no engine_set section")
    got = sec.get("set16_set_sha1")
    src = (m.get("corpus_source") or {}).get("kind")
    if got == guard["value"]:
        # Reproducing the guard from the SEALED corpus is the fidelity proof, not a defect.
        if src == "setpin":
            return rep.add("L6 negative_guard_not_live", PASS,
                           "equals the guard, but corpus_source is the sealed snapshot (fidelity proof)")
        return rep.add("L6 negative_guard_not_live", FAIL,
                       "set16 == NEGATIVE-GUARD %s from a live corpus - dead value, never assert" % guard["value"][:12])
    rep.add("L6 negative_guard_not_live", PASS, "set16 is not the dead sealed value")


def c_corpus_declared(m, rules, rep):
    cs = m.get("corpus_source") or {}
    missing = [k for k in ("kind", "path") if not cs.get(k)]
    rep.add("L7 corpus_source_declared", FAIL if missing else PASS,
            ("corpus_source lacks: %s" % ", ".join(missing)) if missing
            else "kind=%s path=%s" % (cs["kind"], cs["path"]))


def c_harness_cross_section(m, rules, rep):
    """The harness is pinned twice by design - as a FILE section and as a member
    of the SET. The two must agree, or the two-level pin is incoherent."""
    harn = m.get("sections", {}).get("harness")
    sec = m.get("sections", {}).get("engine_set")
    if not harn or not sec:
        return rep.add("L8 harness_cross_section", SKIP, "need both harness and engine_set sections")
    rel = harn.get("relpath")
    as_member = dict((r, s) for r, s in sec.get("members", [])).get(rel)
    if as_member is None:
        return rep.add("L8 harness_cross_section", FAIL, "harness %s is not a member of the set" % rel)
    if as_member != harn.get("file_sha1"):
        return rep.add("L8 harness_cross_section", FAIL,
                       "FILE layer says %s, SET member says %s" % (str(harn.get("file_sha1"))[:12], as_member[:12]))
    rep.add("L8 harness_cross_section", PASS, "FILE pin and SET member agree on %s" % rel)


def c_determinism(m, rules, rep, args):
    """Regenerate from the manifest's declared corpus and compare bytes."""
    kind = (m.get("corpus_source") or {}).get("kind")
    source = {"inventory": "live", "setpin": "sealed"}.get(kind)
    if not source:
        return rep.add("L9 determinism", SKIP, "unrecognised corpus_source.kind=%r" % kind)
    eng = G.section_by_id(rules, "engine_set")
    try:
        corpus, meta = G.load_corpus(source, args.inventory, args.setpin, eng["corpus_root_folder_id"])
    except SystemExit as e:
        return rep.add("L9 determinism", SKIP, "corpus unavailable: %s" % e)
    again = G.emit_json(G.generate(rules, corpus, meta))
    on_disk = open(args.manifest).read().rstrip("\n")
    rep.add("L9 determinism", PASS if again == on_disk else FAIL,
            "regeneration is byte-identical" if again == on_disk
            else "regeneration differs from the file on disk (%d vs %d bytes)" % (len(again), len(on_disk)))


# ---- driver ---------------------------------------------------------------
def run(args):
    rules = G.load_rules()
    m = json.load(open(args.manifest))
    rep = Report()

    for fn in (c_version_lock, c_member_completeness, c_no_duplicates, c_sha1_wellformed,
               c_set_pin_self_consistent, c_negative_guard, c_corpus_declared,
               c_harness_cross_section):
        fn(m, rules, rep)
    c_determinism(m, rules, rep, args)

    mode = "ENFORCE (fail-closed)" if args.enforce else "SHADOW (recommend-only)"
    print("=" * 78)
    print("SHADOW-LINT (S7) - %s" % os.path.basename(args.manifest))
    print("mode: %s" % mode)
    print("=" * 78)
    for cid, v, detail in rep.rows:
        print("%-8s %-28s %s" % (v, cid, detail))

    # Coverage, stated explicitly. A SKIP is a gap in the result, not a pass.
    print("-" * 78)
    print("COVERAGE: %d checks - %d PASS, %d FAIL, %d SKIP"
          % (len(rep.rows), rep.count(PASS), rep.count(FAIL), rep.count(SKIP)))
    if rep.count(SKIP):
        print("          NOT a clean result: %d check(s) could not run -" % rep.count(SKIP))
        for cid, v, detail in rep.rows:
            if v == SKIP:
                print("            %s: %s" % (cid, detail))

    if args.enforce:
        if rep.failed():
            print("VERDICT: REFUSED - %d failing check(s), fail-closed" % len(rep.failed()))
            return 1
        if rep.count(SKIP):
            print("VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass")
            return 1
        print("VERDICT: PASS - all checks ran and passed")
        return 0

    print("VERDICT: SHADOW - %d finding(s) reported, nothing blocked. Exit 0 by design."
          % len(rep.failed()))
    print("         Promote with --enforce only after S8 extends this to every section.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Shadow-lint a generated oracle section (PROTOTYPE)")
    ap.add_argument("manifest")
    ap.add_argument("--enforce", action="store_true",
                    help="promote findings to fail-closed (default is shadow / recommend-only)")
    ap.add_argument("--inventory", default=G.DEF_INVENTORY)
    ap.add_argument("--setpin", default=G.DEF_SETPIN)
    sys.exit(run(ap.parse_args()))


if __name__ == "__main__":
    main()
