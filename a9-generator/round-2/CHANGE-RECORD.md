# CHANGE-RECORD — A9 generator, ROUND 2 (after Gemini Review 1) — 2026-09-06

**Written by** the Max drafting seat (Fable, `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **Instrument** Box MCP connector · **AUTHORITY: NONE.** This file records what was changed, why, and what was
measured. It authorises nothing. No S9, no org-tier write, no live-engine read was performed.

**Review-1 outcome (as relayed by JR):** REVISE on `oracle_gen.py` and `oracle_lint.py`; everything else CLEAR,
including `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt`. This round applies exactly the listed swaps, adopts the
cleared patch, bumps the rules version, regenerates the manifests, re-validates, and proves each fix bites.

---

## 0 · Summary

| item | result |
|---|---|
| Swap 1 — `oracle_gen.py` boxlive root-folder check | applied verbatim (1 occurrence asserted) |
| Swap 2 — `oracle_lint.py` coverage-count guard | applied verbatim (1 occurrence asserted) |
| L9 `boxlive` adapter (cleared patch) | adopted into `oracle_lint.py` with `patch -p0`; composes with swap 2 |
| Rules bump | `rules_version: v0.2-PROTOTYPE` → `v0.3-PROTOTYPE`; `rules_digest` → `e7fbe6ff…` |
| Manifests | all three regenerated at v0.3; delta vs round 1 is exactly the two stamp lines; pins unchanged |
| Re-validation | validate ALL MATCH · anchor-demo PASS/FAIL/FAIL · version-lock LOCKED ×3 · lint `--enforce` 9/0/0 ×3 |
| NC1 (root-check) | refuses `boxlive corpus root folder id mismatch`, exit 1, on both code paths |
| NC2 (coverage-count) | refuses `incomplete coverage under --enforce`, exit 1, at 8 rows (and at 10) |
| Delivered | `A9 Generator - OUT` → subfolder `round-2` (`415677707437`); every file read back, server sha1 == local |

## 1 · Changes applied

### 1.1 Swap 1 — `oracle_gen.py::load_corpus`, boxlive root-folder check (verbatim)

Quote → Replacement exactly as instructed. The review text shows the block with four extra leading spaces; it was
applied at the file's own indentation (the `if source == "boxlive":` line sits at 4 spaces inside `load_corpus`),
with the relative structure identical. Exactly one occurrence of the quoted block existed; the swap was asserted
against that count before writing. `root_folder_id` is the existing parameter of `load_corpus`.

```
--- ../IN/oracle_gen.py	2026-09-06 20:42:40.018507257 +0000
+++ oracle_gen.py	2026-09-06 22:29:23.809566648 +0000
@@ -83,7 +83,10 @@
     if source == "boxlive":
         if not boxlive_path:
             raise SystemExit("source=boxlive needs --boxlive <corpus.json>")
-        return corpus_from_json(boxlive_path)
+        c, m = corpus_from_json(boxlive_path)
+        if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):
+            raise SystemExit("boxlive corpus root folder id mismatch")
+        return c, m
     raise SystemExit("unknown source: %s" % source)
 
 
```

### 1.2 Swap 2 — `oracle_lint.py::run`, coverage-count guard (verbatim)

Same treatment: the quoted three lines sit at 8 spaces inside `if args.enforce:`; one occurrence asserted.

### 1.3 L9 `boxlive` adapter — the cleared patch, adopted

`PROPOSED-PATCH-oracle_lint-boxlive-L9.txt` (OUT root, Box `2450318277001`, sha1 `95bf61c4…`) was applied with
`patch -p0` to the staged `oracle_lint.py` **before** swap 2. The intermediate file hashed `69b11a31d42cf248567d100786e9d4d64d7b5932`,
the same value measured on the round-1 scratch copy, so the patch applied identically. It touches `c_determinism`
(lines 161–173) and the argument parser (line 233); swap 2 touches `run()` (line 214). All three edits are present:

```
164:    source = {"inventory": "live", "setpin": "sealed", "boxlive": "boxlive"}.get(kind)
170:                                     getattr(args, "boxlive", None))
214:        if rep.count(SKIP) or len(rep.rows) != 9:
233:    ap.add_argument("--boxlive", default=os.path.join(G.HERE, "corpus-boxlive-2026-09-06.json"))
```

Combined diff of `oracle_lint.py` against the staged file:

```
--- ../IN/oracle_lint.py	2026-09-06 20:43:18.944268123 +0000
+++ oracle_lint.py	2026-09-06 22:29:23.809870787 +0000
@@ -161,12 +161,13 @@
 def c_determinism(m, rules, rep, args):
     """Regenerate from the manifest's declared corpus and compare bytes."""
     kind = (m.get("corpus_source") or {}).get("kind")
-    source = {"inventory": "live", "setpin": "sealed"}.get(kind)
+    source = {"inventory": "live", "setpin": "sealed", "boxlive": "boxlive"}.get(kind)
     if not source:
         return rep.add("L9 determinism", SKIP, "unrecognised corpus_source.kind=%r" % kind)
     eng = G.section_by_id(rules, "engine_set")
     try:
-        corpus, meta = G.load_corpus(source, args.inventory, args.setpin, eng["corpus_root_folder_id"])
+        corpus, meta = G.load_corpus(source, args.inventory, args.setpin, eng["corpus_root_folder_id"],
+                                     getattr(args, "boxlive", None))
     except SystemExit as e:
         return rep.add("L9 determinism", SKIP, "corpus unavailable: %s" % e)
     again = G.emit_json(G.generate(rules, corpus, meta))
@@ -210,7 +211,7 @@
         if rep.failed():
             print("VERDICT: REFUSED - %d failing check(s), fail-closed" % len(rep.failed()))
             return 1
-        if rep.count(SKIP):
+        if rep.count(SKIP) or len(rep.rows) != 9:
             print("VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass")
             return 1
         print("VERDICT: PASS - all checks ran and passed")
@@ -229,6 +230,7 @@
                     help="promote findings to fail-closed (default is shadow / recommend-only)")
     ap.add_argument("--inventory", default=G.DEF_INVENTORY)
     ap.add_argument("--setpin", default=G.DEF_SETPIN)
+    ap.add_argument("--boxlive", default=os.path.join(G.HERE, "corpus-boxlive-2026-09-06.json"))
     sys.exit(run(ap.parse_args()))
 
 
```

### 1.4 Rules bump — `rules_as_data.yaml`

Only the value changed. The trailing changelog comment on that line (`# v0.2: S8 - pin keys moved into data`)
was left as it was, because the instruction was to set the version; see §5 item 3.

```
-rules_version: v0.2-PROTOTYPE   # v0.2: S8 - pin keys moved into data (pin_keys)
+rules_version: v0.3-PROTOTYPE   # v0.2: S8 - pin keys moved into data (pin_keys)
```

Both scripts compile (`python3 -m py_compile`). No other line of any file was touched.

## 2 · Identities — before and after

| file | round 1 (staged IN) | round 2 | Box id (round-2 folder) |
|---|---|---|---|
| `oracle_gen.py` | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` · 18,690 B | `3bfa706e264ddd630795685d88449c42798749a9` · 18,861 B | 2450403165211 |
| `oracle_lint.py` | `7137aab2c1da72f017f317c06d1985eb8bd49f22` · 10,753 B | `4a6e37d34095a2eecde84b13a65403c3f12d2ecd` · 10,963 B | 2450403366687 |
| `rules_as_data.yaml` | `314c5174c1b5dbce14560e2c4d9838068859dbee` · 4,920 B | `e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8` · 4,920 B | 2450404583942 (stored as `rules_as_data.txt`) |
| `manifest-live.json` | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` · 2,425 B | `4782d015a1838bc13988173debd7aea98cf16952` · 2,425 B | 2450410605150 |
| `manifest-sealed.json` | `6049beb18899cb06379a9bd34b8a382cfd3c4905` · 2,419 B | `4f9f57b5263ff804dd95e350d8fb061270cf432b` · 2,419 B | 2450408239004 |
| `manifest-boxlive-2026-09-06.json` | `54a545534922360cc7c35e595e25f92e234ede3b` · 2,449 B | `4dbc9787678610c10a26cf8c9312247c4b602b24` · 2,449 B | 2450403755460 |
| `VALIDATION-LOG-2026-09-06-round2.md` | — | `08fd9840413e5bd6c4ff3821bf7285553d157e1d` · 18,880 B | 2450411824536 |
| `CHANGE-RECORD.md` | — | this file | see session report |
| `ROUND-2-REVIEW-FEED.md` | — | see session report | see session report |

Every row with a Box id was read back: server sha1 == local, `version_number` 1, created by `183820787`.
The seeds are unchanged: inventory `94cb9b1a…` (350,581 B), setpin `9f4fc6c7…` (1,513 B), staged boxlive snapshot
`9c199709…` (1,600 B). Each regenerated manifest differs from its round-1 counterpart in exactly two lines:

```
<   "oracle_version": "v0.2-PROTOTYPE",
<   "rules_digest": "314c5174c1b5dbce14560e2c4d9838068859dbee",
>   "oracle_version": "v0.3-PROTOTYPE",
>   "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
```

The pins are unchanged: engine15 `9520867753d0d26ec76e959d1a98a450d24255fa`, set16 `df59d6f66748ba6e45e897ca724dc1126a3a536e`,
harness `a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85`; sealed set16 `ccda65118beb01d742c60f86cea140828de2ad9d` (negative guard).

## 3 · Re-validation — explicit flags, flat directory (verbatim: `VALIDATION-LOG-2026-09-06-round2.md`)

| command | result | exit |
|---|---|---|
| `oracle_gen.py … validate` | ALL MATCH — six pins, incl. sealed `ccda6511` (KEY TEST MATCH) | 0 |
| `oracle_gen.py … anchor-demo` | [1] PASS · [2] FAIL · [3] FAIL (guard tripped) | 0 |
| `oracle_gen.py version-lock manifest-live.json` | LOCKED at v0.3 | 0 |
| `oracle_gen.py version-lock manifest-sealed.json` | LOCKED at v0.3 | 0 |
| `oracle_gen.py version-lock manifest-boxlive-2026-09-06.json` | LOCKED at v0.3 | 0 |
| `oracle_lint.py … manifest-live.json --enforce` | 9 PASS / 0 FAIL / 0 SKIP — PASS | 0 |
| `oracle_lint.py … manifest-sealed.json --enforce` | 9 PASS / 0 FAIL / 0 SKIP — PASS | 0 |
| `oracle_lint.py … --boxlive … manifest-boxlive-2026-09-06.json --enforce` | 9 PASS / 0 FAIL / 0 SKIP — PASS (L9 now runs for `boxlive`) | 0 |
| `oracle_gen.py --boxlive <staged snapshot> repin-dryrun` | NO DRIFT; guard not tripped; root `396978339615` accepted | 0 |
| S5 control: `version-lock` on each ROUND-1 manifest against the v0.3 rules | REFUSED ×3 — `oracle_version v0.2 != v0.3` and `rules_digest 314c5174 != e7fbe6ff` | 1 |

Environment: Python 3.11.15, PyYAML 6.0.1; run at 2026-09-06T22:30:33Z.

## 4 · Negative controls — each fix bites (verbatim output)

**NC1 — root-check.** A copy of the staged corpus with `_source_folders.root` changed to `000000000000`:

```
### CMD: python3 oracle_gen.py --boxlive ../work/nc1-corpus-wrong-root.json repin-dryrun
boxlive corpus root folder id mismatch
exit=1
### CMD: python3 oracle_gen.py --boxlive ../work/nc1-corpus-wrong-root.json gen --source boxlive
boxlive corpus root folder id mismatch
exit=1
```

Positive control: the unmodified staged corpus (root `396978339615`) → `repin-dryrun` NO DRIFT, exit 0 (§3).

**NC2 — coverage-count.** The stock linter always records exactly nine rows (every check adds one row on every
path), so a sub-nine result was produced with a small driver, `nc2_driver.py`, which imports the revised
`oracle_lint` unchanged, mirrors its argument parser, and replaces one check with a stub that records nothing —
the silent-check failure mode the guard exists to catch. The driver is a test harness, not a deliverable.

```
### CMD: python3 nc2_driver.py silent manifest-live.json --enforce --inventory $INV --setpin $SP
[…eight PASS rows; L8 absent…]
COVERAGE: 8 checks - 8 PASS, 0 FAIL, 0 SKIP
VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass
exit=1
### NC2 positive control: same driver, no modification, must PASS 9/0/0
COVERAGE: 9 checks - 9 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0
### NC2b (two-sided): --enforce with MORE than 9 recorded rows must also be refused
COVERAGE: 10 checks - 10 PASS, 0 FAIL, 0 SKIP
VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass
exit=1
### NC2 baseline: the same silent-stub scenario against the ROUND-1 linter (staged oracle_lint.py)
COVERAGE: 8 checks - 8 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0
```

The baseline line is the proof that the guard is new: the round-1 linter passed the same eight-row scenario.

## 5 · FLAGS for JR — recorded, deliberately NOT changed

1. **Hardcoded check count.** `oracle_lint.py` now contains the literal `len(rep.rows) != 9`. It is correct for the
   nine checks that exist today. Any future change to the check set — a check added for a new section, or one
   removed — must bump that literal in the same edit, or `--enforce` will refuse every manifest with
   `incomplete coverage`. That failure is fail-closed (a refusal, never a silent pass), which is the safe direction,
   but it is a maintenance trap. The verbatim fix is left intact. A later revision could derive the expected count
   from the check tuple itself; not done here.
2. **Corpus with no `_source_folders` key.** Observed, outside the required controls: swap 1 raises
   `AttributeError: 'NoneType' object has no attribute 'get'` (exit 1, traceback) instead of the clean
   `SystemExit` message, because `corpus_from_json` stores `None` for a missing key and `dict.get(key, {})` does not
   substitute for a present-but-`None` value. It still fails closed. The verbatim fix is left intact; a later
   hardening could read `(m.get("source_folders") or {})`.
3. **Changelog comment not extended.** `rules_as_data.yaml` line 14 still ends with `# v0.2: S8 - pin keys moved
   into data (pin_keys)`. Only the version value was changed, as instructed. JR may want a `# v0.3: …` note added
   in a later revision, under its own bump.
4. **`--boxlive` default names the dated snapshot.** The adopted adapter gives `oracle_lint.py` a `--boxlive` default
   of `corpus-boxlive-2026-09-06.json` next to the script. At write time pass `--boxlive` explicitly (the runbook
   discipline), so a stale snapshot is never linted by accident.
5. **Connector rename.** As in round 1, `rules_as_data.yaml` is stored in Box as `rules_as_data.txt`; bytes are
   identical (sha1 `e7fbe6ff…`). Restore the `.yaml` name on apply — `oracle_gen.py` resolves `RULES` by that basename
   and the S5 digest is over those bytes.
6. **Round-1 files remain in the OUT root.** The connector cannot replace a same-named file, so round 2 lives in the
   `round-2` subfolder. The OUT-root copies of `oracle_gen.py`, `oracle_lint.py`, `rules_as_data.txt` and the three
   manifests are the v0.2 set and are now refused by the v0.3 lock (§3); they are superseded evidence, not the
   deliverable. A consumer must take the `round-2` folder.

## 6 · Not done, by scope

- No S9; no org-tier write; no write outside `415603610278`; no live-engine read (folders `396978339615` /
  `403356419210` remain out of this identity's scope by design).
- IN `415602830059` untouched — 17/17 server sha1s equal before and after this round.
- No section beyond `engine_set` and `harness`. The write-time re-pin remains the Teams/CCG promotion step
  (round-1 HANDOFF-BACK §5 still applies, with the v0.3 set).

*END — round 2. Authority: NONE.*
