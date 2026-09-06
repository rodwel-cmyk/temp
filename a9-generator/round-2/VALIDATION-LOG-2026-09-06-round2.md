# VALIDATION LOG — A9 generator, ROUND 2 (post-review fixes) — 2026-09-06

**Seat** Max drafting seat (Fable, model `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **AUTHORITY: NONE.** Evidence only. Every line below the header is verbatim machine output,
captured by redirection from a single scripted run; nothing was retyped.

**What changed before this run** (see CHANGE-RECORD.md): the two verbatim swaps from Gemini Review 1
(`oracle_gen.py` boxlive root-folder check; `oracle_lint.py` coverage-count guard), the cleared L9
`boxlive` adapter adopted into `oracle_lint.py`, and `rules_version` bumped v0.2 → v0.3-PROTOTYPE.
The seeds (inventory, setpin, staged boxlive snapshot) are the unchanged IN files, sha1-verified.

**What this log contains.** Manifest regeneration at v0.3 with the byte delta against round 1; the full
re-validation with explicit flags; an S5 control showing the round-1 (v0.2) manifests are now refused;
NC1 (root-check) and NC2 (coverage-count) negative controls with positive controls and a round-1 baseline;
one observation outside the required controls (a corpus with no `_source_folders` key).

**Claim status.** These results are this seat's CLAIM; the deterministic gate is re-run independently by
the Code-CLI applier. `nc2_driver.py` is a test harness for NC2 only and is not a deliverable.

---

```
### RUN CONTEXT (ROUND 2)
date_utc=2026-09-06T22:30:33Z
python=Python 3.11.15
pyyaml=6.0.1
cwd=flat round-2 working copy (revised generator set + staged seeds; no 'Level 1 - Dev' parent tree)

### INPUT IDENTITIES (local sha1 / bytes)
e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8  rules_as_data.yaml
3bfa706e264ddd630795685d88449c42798749a9  oracle_gen.py
4a6e37d34095a2eecde84b13a65403c3f12d2ecd  oracle_lint.py
9c1997090fe403476554168a2aaee3abf8e28b87  corpus-boxlive-2026-09-06.json
9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982  oracle-model-SETPIN-2026-07-28.json
94cb9b1a4efbf96ac10a8a60e9c77c096721e447  inventory-390802629329-2026-09-04-1650Z.json
 4920 rules_as_data.yaml
18861 oracle_gen.py
10963 oracle_lint.py

### STEP 4: regenerate the three manifests at v0.3
### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source live --out manifest-live.json
wrote manifest-live.json
exit=0
### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source sealed --out manifest-sealed.json
wrote manifest-sealed.json
exit=0
### CMD: python3 oracle_gen.py --boxlive $BL gen --source boxlive --out manifest-boxlive-2026-09-06.json
wrote manifest-boxlive-2026-09-06.json
exit=0
### regenerated manifest identities
4782d015a1838bc13988173debd7aea98cf16952  manifest-live.json
4f9f57b5263ff804dd95e350d8fb061270cf432b  manifest-sealed.json
4dbc9787678610c10a26cf8c9312247c4b602b24  manifest-boxlive-2026-09-06.json
2425 manifest-live.json
2419 manifest-sealed.json
2449 manifest-boxlive-2026-09-06.json
### version stamps in the regenerated manifests
manifest-live.json:  "oracle_version": "v0.3-PROTOTYPE",
manifest-live.json:  "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
manifest-sealed.json:  "oracle_version": "v0.3-PROTOTYPE",
manifest-sealed.json:  "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
manifest-boxlive-2026-09-06.json:  "oracle_version": "v0.3-PROTOTYPE",
manifest-boxlive-2026-09-06.json:  "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
### delta vs the round-1 manifests (expect exactly the two stamp lines to differ)
--- diff ../OUT/manifest-live.json (round 1) vs manifest-live.json (round 2)
9,10c9,10
<   "oracle_version": "v0.2-PROTOTYPE",
<   "rules_digest": "314c5174c1b5dbce14560e2c4d9838068859dbee",
---
>   "oracle_version": "v0.3-PROTOTYPE",
>   "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
--- diff ../OUT/manifest-sealed.json (round 1) vs manifest-sealed.json (round 2)
9,10c9,10
<   "oracle_version": "v0.2-PROTOTYPE",
<   "rules_digest": "314c5174c1b5dbce14560e2c4d9838068859dbee",
---
>   "oracle_version": "v0.3-PROTOTYPE",
>   "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",
--- diff ../OUT/manifest-boxlive-2026-09-06.json (round 1) vs manifest-boxlive-2026-09-06.json (round 2)
12,13c12,13
<   "oracle_version": "v0.2-PROTOTYPE",
<   "rules_digest": "314c5174c1b5dbce14560e2c4d9838068859dbee",
---
>   "oracle_version": "v0.3-PROTOTYPE",
>   "rules_digest": "e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8",

### STEP 5: full re-validation (explicit flags)
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

### CMD: python3 oracle_gen.py --boxlive $BL repin-dryrun   (staged snapshot; positive control for NC1 - root 396978339615 accepted)
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

### S5 BUMP CONTROL: the ROUND-1 (v0.2) manifests must now be REFUSED by version-lock against the v0.3 rules
### CMD: python3 oracle_gen.py version-lock ../OUT/manifest-live.json   (round-1 file)
==============================================================================
VERSION LOCK (S5) - manifest-live.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.2-PROTOTYPE rules_digest=314c5174c1b5
------------------------------------------------------------------------------
REFUSE: oracle_version v0.2-PROTOTYPE != rules_version v0.3-PROTOTYPE
REFUSE: rules_digest 314c5174c1b5 != current rules e7fbe6ff49a4 (rules edited without a version bump)
VERDICT: REFUSED (fail-closed) - regenerate before trusting this manifest
exit=1
### CMD: python3 oracle_gen.py version-lock ../OUT/manifest-sealed.json   (round-1 file)
==============================================================================
VERSION LOCK (S5) - manifest-sealed.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.2-PROTOTYPE rules_digest=314c5174c1b5
------------------------------------------------------------------------------
REFUSE: oracle_version v0.2-PROTOTYPE != rules_version v0.3-PROTOTYPE
REFUSE: rules_digest 314c5174c1b5 != current rules e7fbe6ff49a4 (rules edited without a version bump)
VERDICT: REFUSED (fail-closed) - regenerate before trusting this manifest
exit=1
### CMD: python3 oracle_gen.py version-lock ../OUT/manifest-boxlive-2026-09-06.json   (round-1 file)
==============================================================================
VERSION LOCK (S5) - manifest-boxlive-2026-09-06.json
==============================================================================
rules_version : v0.3-PROTOTYPE
rules_digest  : e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8
manifest      : oracle_version=v0.2-PROTOTYPE rules_digest=314c5174c1b5
------------------------------------------------------------------------------
REFUSE: oracle_version v0.2-PROTOTYPE != rules_version v0.3-PROTOTYPE
REFUSE: rules_digest 314c5174c1b5 != current rules e7fbe6ff49a4 (rules edited without a version bump)
VERDICT: REFUSED (fail-closed) - regenerate before trusting this manifest
exit=1

### NC1 (root-check): boxlive corpus whose _source_folders.root != 396978339615 must be refused
4:    "root": "000000000000",
### CMD: python3 oracle_gen.py --boxlive ../work/nc1-corpus-wrong-root.json repin-dryrun
boxlive corpus root folder id mismatch
exit=1
### CMD: python3 oracle_gen.py --boxlive ../work/nc1-corpus-wrong-root.json gen --source boxlive
boxlive corpus root folder id mismatch
exit=1
### NC1 observation (not a required control): corpus with NO _source_folders key at all
### CMD: python3 oracle_gen.py --boxlive ../work/nc1-corpus-no-source-folders.json repin-dryrun
    if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
exit=1

### NC2 (coverage-count): --enforce with fewer than 9 recorded rows must be refused (driver: nc2_driver.py, stubs one check to record nothing)
### CMD: python3 nc2_driver.py silent manifest-live.json --enforce --inventory $INV --setpin $SP
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
PASS     L9 determinism               regeneration is byte-identical
------------------------------------------------------------------------------
COVERAGE: 8 checks - 8 PASS, 0 FAIL, 0 SKIP
VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass
exit=1
### NC2 positive control: same driver, no modification, must PASS 9/0/0
### CMD: python3 nc2_driver.py none manifest-live.json --enforce --inventory $INV --setpin $SP
COVERAGE: 9 checks - 9 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0
### NC2b (two-sided): --enforce with MORE than 9 recorded rows must also be refused
### CMD: python3 nc2_driver.py dup manifest-live.json --enforce --inventory $INV --setpin $SP
PASS     L3 no_duplicate_relpaths     16 distinct relpaths
PASS     L8 harness_cross_section (duplicate) extra row injected by NC2b
COVERAGE: 10 checks - 10 PASS, 0 FAIL, 0 SKIP
VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass
exit=1
### NC2 baseline: the same silent-stub scenario against the ROUND-1 linter (staged oracle_lint.py) - shows the guard is new
COVERAGE: 8 checks - 8 PASS, 0 FAIL, 0 SKIP
VERDICT: PASS - all checks ran and passed
exit=0
```
