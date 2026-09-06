# VALIDATION LOG — A9 generator, standalone full-strength run — 2026-09-06

**Seat** Max drafting seat (Fable, model `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **AUTHORITY: NONE.** Evidence only. Every line below the header is verbatim machine output,
captured with `tee`-style redirection from a single scripted run; nothing was retyped.

**Method.** All 17 items of `A9 Generator -IN` (`415602830059`) were listed by direct folder id with
server-side `sha1`/`size`. The nine files needed at runtime were pulled to one flat working directory
and each local sha1 was compared to the server value before use (all MATCH — see INPUT IDENTITIES).
No `Level 1 - Dev` parent tree exists on this machine, so `--inventory`, `--setpin` and `--boxlive`
were passed explicitly, exactly as SEEDS-RUNBOOK.md section 1 prescribes. The governed engine folders
(`396978339615`, `403356419210`) are not visible to this identity by design; the `--boxlive` corpus is
therefore the STAGED snapshot read 2026-09-06 by the Teams seat, not a fresh read.

**Claim status.** These results are this seat's CLAIM. The deterministic gate is re-run independently by
the Code-CLI applier; nothing here is the final gate.

---

```
### RUN CONTEXT
date_utc=2026-09-06T20:49:34Z
python=Python 3.11.15
pyyaml=6.0.1
cwd=flat working copy of A9 Generator -IN (no 'Level 1 - Dev' parent tree)

### INPUT IDENTITIES (local sha1 / bytes of the working copy)
314c5174c1b5dbce14560e2c4d9838068859dbee  rules_as_data.yaml
d9485e36989b859dc6423bec52b4c09a0aa26a1a  oracle_gen.py
7137aab2c1da72f017f317c06d1985eb8bd49f22  oracle_lint.py
e5993c1de7d888e308f5b5a09a2f89810e74ae8d  manifest-live.json
6049beb18899cb06379a9bd34b8a382cfd3c4905  manifest-sealed.json
9c1997090fe403476554168a2aaee3abf8e28b87  corpus-boxlive-2026-09-06.json
9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982  oracle-model-SETPIN-2026-07-28.json
94cb9b1a4efbf96ac10a8a60e9c77c096721e447  inventory-390802629329-2026-09-04-1650Z.json
b765d4ee82740c71819204f64abcd9a795093039  CHECKPOINT-oracle-codecli-2026-09-04.md
  4920 rules_as_data.yaml
 18690 oracle_gen.py
 10753 oracle_lint.py
  2425 manifest-live.json
  2419 manifest-sealed.json
  1600 corpus-boxlive-2026-09-06.json
  1513 oracle-model-SETPIN-2026-07-28.json
350581 inventory-390802629329-2026-09-04-1650Z.json
 77165 CHECKPOINT-oracle-codecli-2026-09-04.md

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
rules_version : v0.2-PROTOTYPE
rules_digest  : 314c5174c1b5dbce14560e2c4d9838068859dbee
manifest      : oracle_version=v0.2-PROTOTYPE rules_digest=314c5174c1b5
------------------------------------------------------------------------------
VERDICT: LOCKED - oracle_version == rules_version and rules unedited
exit=0

### CMD: python3 oracle_gen.py version-lock manifest-sealed.json
==============================================================================
VERSION LOCK (S5) - manifest-sealed.json
==============================================================================
rules_version : v0.2-PROTOTYPE
rules_digest  : 314c5174c1b5dbce14560e2c4d9838068859dbee
manifest      : oracle_version=v0.2-PROTOTYPE rules_digest=314c5174c1b5
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

### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source live --out $W/regen-live.json  (then cmp against staged manifest-live.json)
wrote ../work/regen-live.json
exit=0
cmp: BYTE-IDENTICAL to staged manifest-live.json
e5993c1de7d888e308f5b5a09a2f89810e74ae8d  ../work/regen-live.json

### CMD: python3 oracle_gen.py --inventory $INV --setpin $SP gen --source sealed --out $W/regen-sealed.json  (then cmp against staged manifest-sealed.json)
wrote ../work/regen-sealed.json
exit=0
cmp: BYTE-IDENTICAL to staged manifest-sealed.json
6049beb18899cb06379a9bd34b8a382cfd3c4905  ../work/regen-sealed.json

### CMD: python3 oracle_gen.py --boxlive $BL repin-dryrun   [NOTE: $BL is the STAGED snapshot read 2026-09-06 by the Teams seat; NOT a fresh read by this seat - folders 396978339615/403356419210 return 'Item not found' to user 183820787]
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

### CMD: python3 oracle_gen.py --boxlive $BL gen --source boxlive --out $W/manifest-boxlive-2026-09-06.json
wrote ../work/manifest-boxlive-2026-09-06.json
exit=0
54a545534922360cc7c35e595e25f92e234ede3b  ../work/manifest-boxlive-2026-09-06.json
2449 ../work/manifest-boxlive-2026-09-06.json

### CMD: python3 oracle_lint.py --inventory $INV --setpin $SP $W/manifest-boxlive-2026-09-06.json   (SHADOW mode)
==============================================================================
SHADOW-LINT (S7) - manifest-boxlive-2026-09-06.json
mode: SHADOW (recommend-only)
==============================================================================
PASS     L1 version_lock              stamp matches current rules
PASS     L2 member_completeness       all 16 declared members present, no extras
PASS     L3 no_duplicate_relpaths     16 distinct relpaths
PASS     L4 sha1_wellformed           all sha1s are 40-char lowercase hex
PASS     L5 set_pin_self_consistent   all 2 pin(s) follow from the recorded members
PASS     L6 negative_guard_not_live   set16 is not the dead sealed value
PASS     L7 corpus_source_declared    kind=boxlive path=corpus-boxlive-2026-09-06.json
PASS     L8 harness_cross_section     FILE pin and SET member agree on test_layer1_lint.py
SKIP     L9 determinism               unrecognised corpus_source.kind='boxlive'
------------------------------------------------------------------------------
COVERAGE: 9 checks - 8 PASS, 0 FAIL, 1 SKIP
          NOT a clean result: 1 check(s) could not run -
            L9 determinism: unrecognised corpus_source.kind='boxlive'
VERDICT: SHADOW - 0 finding(s) reported, nothing blocked. Exit 0 by design.
         Promote with --enforce only after S8 extends this to every section.
exit=0

### CMD: python3 oracle_lint.py --inventory $INV --setpin $SP $W/manifest-boxlive-2026-09-06.json --enforce   (expected REFUSE: L9 has no boxlive adapter)
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
SKIP     L9 determinism               unrecognised corpus_source.kind='boxlive'
------------------------------------------------------------------------------
COVERAGE: 9 checks - 8 PASS, 0 FAIL, 1 SKIP
          NOT a clean result: 1 check(s) could not run -
            L9 determinism: unrecognised corpus_source.kind='boxlive'
VERDICT: REFUSED - incomplete coverage under --enforce; a gap is not a pass
exit=1

### NEGATIVE CONTROL: bare defaults in the flat folder (runbook section 2 defect)
                      ^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-0/-home-user-temp/582c4b4d-a3ee-59f0-9ca4-b05e861bb0e9/scratchpad/inventory-390802629329-2026-09-04-1650Z.json'
exit=1
```
