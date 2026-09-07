# VALIDATION LOG — A9 generator, ROUND 2 + JR-DIRECTED HARDENING ADDENDUM — 2026-09-07

**Seat** Max drafting seat (Fable, model `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **AUTHORITY: NONE.** Evidence only. Every line below the header is verbatim machine output,
captured by redirection from a single scripted run; nothing was retyped.

**What changed before this run.** One token in `oracle_gen.py::load_corpus` (boxlive branch), directed by JR
after round 2: `m.get("source_folders", {})` → `(m.get("source_folders") or {})`, so a boxlive corpus whose
`_source_folders` is missing or `null` reaches the clean `SystemExit("boxlive corpus root folder id mismatch")`
instead of raising `AttributeError`. No other file changed. No rules bump: `rules_as_data.yaml` is unchanged,
so the S5 digest (`e7fbe6ff…`) and `v0.3-PROTOTYPE` stand.

**What this log contains.** The diff; manifest regeneration proving the three manifests are byte-identical to
the delivered round-2 set; the full re-validation; the valid-corpus pass; NC1a (wrong root) and NC1b (missing
key, the new proof); NC1c (`null`, an extra observation); and the round-2 baseline reproducing the defect.

**Claim status.** These results are this seat's CLAIM; the deterministic gate is re-run independently by the
Code-CLI applier. The hardening itself is JR-directed, not reviewer-authored, and is to be reviewed adversarially.

---

```
### RUN CONTEXT (ROUND 2 - JR-DIRECTED HARDENING ADDENDUM)
date_utc=2026-09-07T08:51:38Z
python=Python 3.11.15
pyyaml=6.0.1
cwd=flat working copy: round-2 set with the one-token hardening in oracle_gen.py; all other files byte-identical to round 2

### INPUT IDENTITIES (local sha1 / bytes)
520f83042f3ad1f063064e6f1995b30ec021d74c  oracle_gen.py
4a6e37d34095a2eecde84b13a65403c3f12d2ecd  oracle_lint.py
e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8  rules_as_data.yaml
9c1997090fe403476554168a2aaee3abf8e28b87  corpus-boxlive-2026-09-06.json
9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982  oracle-model-SETPIN-2026-07-28.json
94cb9b1a4efbf96ac10a8a60e9c77c096721e447  inventory-390802629329-2026-09-04-1650Z.json
18865 oracle_gen.py
10963 oracle_lint.py
 4920 rules_as_data.yaml

### THE CHANGE (diff round-2 oracle_gen.py -> hardened)
--- round-2/oracle_gen.py (sha1 3bfa706e264ddd630795685d88449c42798749a9)
+++ round-2-hardened/oracle_gen.py (JR-directed one-token hardening)
@@ -84,7 +84,7 @@
         if not boxlive_path:
             raise SystemExit("source=boxlive needs --boxlive <corpus.json>")
         c, m = corpus_from_json(boxlive_path)
-        if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):
+        if str((m.get("source_folders") or {}).get("root")) != str(root_folder_id):
             raise SystemExit("boxlive corpus root folder id mismatch")
         return c, m
     raise SystemExit("unknown source: %s" % source)

### STEP 2: regenerate the three manifests (no bump; rules unchanged) and compare to the delivered round-2 set
### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source live --out manifest-live.json
wrote manifest-live.json
exit=0
### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source sealed --out manifest-sealed.json
wrote manifest-sealed.json
exit=0
### CMD: python3 oracle_gen.py --boxlive $BL gen --source boxlive --out manifest-boxlive-2026-09-06.json
wrote manifest-boxlive-2026-09-06.json
exit=0
### regenerated identities
4782d015a1838bc13988173debd7aea98cf16952  manifest-live.json
4f9f57b5263ff804dd95e350d8fb061270cf432b  manifest-sealed.json
4dbc9787678610c10a26cf8c9312247c4b602b24  manifest-boxlive-2026-09-06.json
cmp: manifest-live.json BYTE-IDENTICAL to the delivered round-2 file
cmp: manifest-sealed.json BYTE-IDENTICAL to the delivered round-2 file
cmp: manifest-boxlive-2026-09-06.json BYTE-IDENTICAL to the delivered round-2 file

### STEP 3: full re-validation (explicit flags)
### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP --boxlive $BL validate
==============================================================================
PARALLEL VALIDATION (PROTOTYPE)  - generator vs hand-computed pins
live   corpus: inventory-390802629329-2026-09-04-1650Z.json
sealed corpus: oracle-model-SETPIN-2026-07-28.json
==============================================================================
engine15  (live)           MATCH     computed=9520867753d0d26ec76e959d1a98a450d24255fa  expected=9520867753d0d26ec76e959d1a98a450d24255fa  [LIVE-POSITIVE]
set16     (live)           MATCH     computed=df59d6f66748ba6e45e897ca724dc1126a3a536e  expected=df59d6f66748ba6e45e897ca724dc1126a3a536e  [LIVE-POSITIVE]
harness   (live)           MATCH     computed=a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85  expected=a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85  [LIVE-POSITIVE]
engine15  (sealed)         MATCH     computed=9520867753d0d26ec76e959d1a98a450d24255fa  expected=9520867753d0d26ec76e959d1a98a450d24255fa  [LIVE-POSITIVE]
set16     (sealed)         MATCH     computed=ccda65118beb01d742c60f86cea140828de2ad9d  expected=ccda65118beb01d742c60f86cea140828de2ad9d  [NEGATIVE-GUARD]
harness   (sealed)         MATCH     computed=3574c2d13a7f34f7cd8d1bac3543b05556e18ef9  expected=3574c2d13a7f34f7cd8d1bac3543b05556e18ef9  [NEGATIVE-GUARD]
------------------------------------------------------------------------------
KEY TEST - sealed set-sha1 reproduces ccda6511: MATCH
OVERALL: ALL MATCH - generator is faithful
exit=0

### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP --boxlive $BL anchor-demo
==============================================================================
ANCHOR FAIL-CLOSED DEMO (PROTOTYPE)
pinned (live SET pin) : df59d6f66748ba6e45e897ca724dc1126a3a536e
negative guard (dead) : ccda65118beb01d742c60f86cea140828de2ad9d
==============================================================================
[1] clean live corpus         -> PASS  (computed == pinned)  computed=df59d6f66748ba6e45e897ca724dc1126a3a536e
[2] perturbed l1lint/engine.py-> FAIL  (computed != pinned)  computed=079afd153fdb94dee6154d8150654f5e9854db06
[3] stale harness (3574c2d1)  -> FAIL  (computed == NEGATIVE-GUARD (dead sealed value) - refuse)  computed=ccda65118beb01d742c60f86cea140828de2ad9d
------------------------------------------------------------------------------
Expected: [1] PASS, [2] FAIL, [3] FAIL (trips the negative guard).
exit=0

### CMD: python3 oracle_gen.py version-lock manifest-live.json
==============================================================================
VERSION LOCK (S5) - manifest-live.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.3-PROTOTYPE rules_digest=e7fbe6ff49a4
------------------------------------------------------------------------------
VERDICT: LOCKED - oracle_version == rules_version and rules unedited
exit=0

### CMD: python3 oracle_gen.py version-lock manifest-sealed.json
==============================================================================
VERSION LOCK (S5) - manifest-sealed.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.3-PROTOTYPE rules_digest=e7fbe6ff49a4
------------------------------------------------------------------------------
VERDICT: LOCKED - oracle_version == rules_version and rules unedited
exit=0

### CMD: python3 oracle_gen.py version-lock manifest-boxlive-2026-09-06.json
==============================================================================
VERSION LOCK (S5) - manifest-boxlive-2026-09-06.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.3-PROTOTYPE rules_digest=e7fbe6ff49a4
------------------------------------------------------------------------------
VERDICT: LOCKED - oracle_version == rules_version and rules unedited
exit=0

### CMD: python3 oracle_lint.py --inventory $INV --setpin $SP manifest-live.json --enforce
==============================================================================
SHADOW-LINT (S7) - manifest-live.json
mode: ENFORCE (fail-closed)
==============================================================================
PASS     L1 version_lock              stamp matches current rules
PASS     L2 member_completeness       all 16 declared members present, no extras
PASS     L3 no_duplicate_relpaths     16 distinct relpaths
PASS     L4 sha1_wellformed           all sha1s are 40-char lowercase hex
PASS     L5 set_pin_self_consistent   all 2 pin(s) follow from the recorded members
PASS     L6 negative_guard_not_live   set16 is not the dead sealed value
PASS     L7 corpus_source_declared    kind=inventory path=inventory-390802629329-2026-09-04-1650Z.json
PASS     L8 harness_cross_section     FILE pin and SET member agree on test_layer1_lint.py
PASS     L9 determinism               regeneration is byte-identical
------------------------------------------------------------------------------
COVERAGE: 9 checks - 9 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0

### CMD: python3 oracle_lint.py --inventory $INV --setpin $SP manifest-sealed.json --enforce
==============================================================================
SHADOW-LINT (S7) - manifest-sealed.json
mode: ENFORCE (fail-closed)
==============================================================================
PASS     L1 version_lock              stamp matches current rules
PASS     L2 member_completeness       all 16 declared members present, no extras
PASS     L3 no_duplicate_relpaths     16 distinct relpaths
PASS     L4 sha1_wellformed           all sha1s are 40-char lowercase hex
PASS     L5 set_pin_self_consistent   all 2 pin(s) follow from the recorded members
PASS     L6 negative_guard_not_live   equals the guard, but corpus_source is the sealed snapshot (fidelity proof)
PASS     L7 corpus_source_declared    kind=setpin path=oracle-model-SETPIN-2026-07-28.json
PASS     L8 harness_cross_section     FILE pin and SET member agree on test_layer1_lint.py
PASS     L9 determinism               regeneration is byte-identical
------------------------------------------------------------------------------
COVERAGE: 9 checks - 9 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0

### CMD: python3 oracle_lint.py --inventory $INV --setpin $SP --boxlive $BL manifest-boxlive-2026-09-06.json --enforce
==============================================================================
SHADOW-LINT (S7) - manifest-boxlive-2026-09-06.json
mode: ENFORCE (fail-closed)
==============================================================================
PASS     L1 version_lock              stamp matches current rules
PASS     L2 member_completeness       all 16 declared members present, no extras
PASS     L3 no_duplicate_relpaths     16 distinct relpaths
PASS     L4 sha1_wellformed           all sha1s are 40-char lowercase hex
PASS     L5 set_pin_self_consistent   all 2 pin(s) follow from the recorded members
PASS     L6 negative_guard_not_live   set16 is not the dead sealed value
PASS     L7 corpus_source_declared    kind=boxlive path=corpus-boxlive-2026-09-06.json
PASS     L8 harness_cross_section     FILE pin and SET member agree on test_layer1_lint.py
PASS     L9 determinism               regeneration is byte-identical
------------------------------------------------------------------------------
COVERAGE: 9 checks - 9 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0

### STEP 4: NEGATIVE CONTROLS
### valid corpus (staged snapshot, root 396978339615) must still pass
### CMD: python3 oracle_gen.py --boxlive $BL repin-dryrun
==============================================================================
S10 RE-PIN DRY RUN - re-derived from LIVE Box, nothing written
corpus : corpus-boxlive-2026-09-06.json (read 2026-09-06)
folders: {'root': '396978339615', 'l1lint': '403356419210'}
==============================================================================
engine_set.engine15    MATCH     re-derived=9520867753d0d26ec76e959d1a98a450d24255fa  recorded=9520867753d0d26ec76e959d1a98a450d24255fa
engine_set.set16       MATCH     re-derived=df59d6f66748ba6e45e897ca724dc1126a3a536e  recorded=df59d6f66748ba6e45e897ca724dc1126a3a536e
harness.file           MATCH     re-derived=a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85  recorded=a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85
------------------------------------------------------------------------------
negative guard tripped: no
VERDICT: NO DRIFT - live corpus still yields the recorded pins.
         Still not authorisation to write: S9 re-derives at write time (BARRED-13).
exit=0

### NC1a (wrong root): _source_folders.root = 000000000000
4:    "root": "000000000000",
### CMD: python3 oracle_gen.py --boxlive ../work/nc1a-corpus-wrong-root.json repin-dryrun
boxlive corpus root folder id mismatch
exit=1
### CMD: python3 oracle_gen.py --boxlive ../work/nc1a-corpus-wrong-root.json gen --source boxlive
boxlive corpus root folder id mismatch
exit=1

### NC1b (NEW - missing key): corpus with NO _source_folders key; must refuse CLEANLY with the same message, no traceback
0
^ occurrences of _source_folders in the NC1b corpus (want 0)
### CMD: python3 oracle_gen.py --boxlive ../work/nc1b-corpus-no-source-folders.json repin-dryrun
boxlive corpus root folder id mismatch
exit=1
### CMD: python3 oracle_gen.py --boxlive ../work/nc1b-corpus-no-source-folders.json gen --source boxlive
boxlive corpus root folder id mismatch
exit=1
### NC1b combined stdout+stderr line count and traceback check (want: 1 line, no Traceback, no AttributeError)
lines=1 traceback_lines=0 attributeerror_lines=0

### NC1c (extra observation): _source_folders present but null
### CMD: python3 oracle_gen.py --boxlive ../work/nc1c-corpus-null-source-folders.json repin-dryrun
boxlive corpus root folder id mismatch
exit=1

### BASELINE: the ROUND-2 oracle_gen.py (pre-hardening, sha1 3bfa706e...) on the NC1b corpus - the defect being closed
### CMD: python3 ../work/baseline-gen/oracle_gen.py --boxlive ../work/nc1b-corpus-no-source-folders.json repin-dryrun
    if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
exit=1
```
