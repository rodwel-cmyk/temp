# -*- coding: utf-8 -*-
"""l1lint.hygiene - 869dwncba ClickUp hygiene family (R01-R02, recommend-only, dump-fed)

Verbatim relocation from the frozen v0.2.8 monolith layer1_lint.py
(sha1 a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7), lines 1254-1366.
No check logic altered - see MODULE-MAP.md for the exact move ledger.
"""
import json
import re


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
