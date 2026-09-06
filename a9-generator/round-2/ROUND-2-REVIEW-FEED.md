# ROUND-2-REVIEW-FEED — A9 generator, delta pack for Gemini round 2 — 2026-09-06

**Purpose.** Evidence for the independent reviewer, scoped to the delta since Review 1: the two changed files, the
re-validation, and the negative controls. It states what was, what is, what changed, and what is unverified. It
contains no review criteria and no conclusion about the quality of the output.

**Producer.** Max drafting seat (Fable, `claude-fable-5-1`) · Box identity rodwel@me.com (`183820787`) · Box MCP
connector only · Authority: NONE. Output type: code-change set. Round-1 items reported CLEAR (rules content,
manifests' structure, documents, the L9 patch) are not re-argued here; they are listed only where their bytes
changed as a consequence of this round.

---

## (a) GROUND TRUTH — pre-state

### The two files under revision, as staged in IN and as delivered in round 1 (byte-identical)

| file | IN Box id | OUT-root Box id (round 1) | bytes | sha1 |
|---|---|---|---|---|
| `oracle_gen.py` | 2449860666966 | 2450306185463 | 18,690 | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` |
| `oracle_lint.py` | 2449860388492 | 2450307280287 | 10,753 | `7137aab2c1da72f017f317c06d1985eb8bd49f22` |

### Other inputs to this round

| item | Box id | bytes | sha1 |
|---|---|---|---|
| `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt` (reported CLEAR in Review 1) | 2450318277001 | 1,498 | `95bf61c494cd82c12e3382bdf81181d61f383fde` |
| `rules_as_data.yaml` (v0.2) | 2449859682122 | 4,920 | `314c5174c1b5dbce14560e2c4d9838068859dbee` |
| `manifest-live.json` (v0.2) | 2449861430379 | 2,425 | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` |
| `manifest-sealed.json` (v0.2) | 2449863955142 | 2,419 | `6049beb18899cb06379a9bd34b8a382cfd3c4905` |
| `manifest-boxlive-2026-09-06.json` (v0.2, round 1) | 2450304675825 | 2,449 | `54a545534922360cc7c35e595e25f92e234ede3b` |
| seeds: inventory / setpin / staged boxlive snapshot | 2450234898780 / 2450238904095 / 2449860815455 | 350,581 / 1,513 / 1,600 | `94cb9b1a…` / `9f4fc6c7…` / `9c199709…` |

### The Review-1 instructions, as relayed (the input this round executes)

1. `oracle_gen.py` — replace the four-line `if source == "boxlive": … return corpus_from_json(boxlive_path)` block
   with the seven-line block that binds `c, m`, compares `str(m.get("source_folders", {}).get("root"))` to
   `str(root_folder_id)`, raises `SystemExit("boxlive corpus root folder id mismatch")` on mismatch, and returns `c, m`.
2. `oracle_lint.py` — replace `if rep.count(SKIP):` (the coverage refusal in `run()`) with
   `if rep.count(SKIP) or len(rep.rows) != 9:`.
3. Adopt the cleared L9 patch into `oracle_lint.py`.
4. Bump `rules_version` v0.2-PROTOTYPE → v0.3-PROTOTYPE; regenerate all three manifests.
5. Re-validate; 6. negative controls NC1 and NC2; 7–9. records and delivery.

### Pre-state of the delivery folder

`A9 Generator - OUT` (`415603610278`) held the 11 round-1 files, all at their round-1 sha1s; no `round-2` folder existed.

## (b) OUTPUT — post-state (`round-2` subfolder `415677707437` in OUT)

| file | Box id | bytes | sha1 (server read-back) |
|---|---|---|---|
| `oracle_gen.py` | 2450403165211 | 18,861 | `3bfa706e264ddd630795685d88449c42798749a9` |
| `oracle_lint.py` | 2450403366687 | 10,963 | `4a6e37d34095a2eecde84b13a65403c3f12d2ecd` |
| `rules_as_data.txt` (bytes of `rules_as_data.yaml` v0.3) | 2450404583942 | 4,920 | `e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8` |
| `manifest-live.json` | 2450410605150 | 2,425 | `4782d015a1838bc13988173debd7aea98cf16952` |
| `manifest-sealed.json` | 2450408239004 | 2,419 | `4f9f57b5263ff804dd95e350d8fb061270cf432b` |
| `manifest-boxlive-2026-09-06.json` | 2450403755460 | 2,449 | `4dbc9787678610c10a26cf8c9312247c4b602b24` |
| `VALIDATION-LOG-2026-09-06-round2.md` | 2450411824536 | 18,880 | `08fd9840413e5bd6c4ff3821bf7285553d157e1d` |
| `CHANGE-RECORD.md` | assigned at upload — see session report | — | local sha1 in the session report |
| `ROUND-2-REVIEW-FEED.md` | assigned at upload — see session report | — | this file |

All rows with a Box id: `version_number` 1, `created_by` `183820787`, parent `415677707437`. The 11 round-1 files
in the OUT root were not modified. IN was not modified (17/17 sha1s equal before and after).

## (c) CHANGE-MANIFEST — factual, per item

| item | what happened |
|---|---|
| `oracle_gen.py` | One block replaced in `load_corpus` (lines 83–89 of the staged file): 4 lines → 7 lines, text as instructed. The block was applied at the file's indentation (4 spaces), the instruction having shown it with 4 extra leading spaces. Occurrence count before replacement: 1. Net +171 bytes. No other change. |
| `oracle_lint.py` | Three edits. (i) Patch `95bf61c4…` applied with `patch -p0` to the staged file: `c_determinism` kind map gains `"boxlive": "boxlive"`; `G.load_corpus` call gains a fifth argument `getattr(args, "boxlive", None)`; `main()` gains `ap.add_argument("--boxlive", default=os.path.join(G.HERE, "corpus-boxlive-2026-09-06.json"))`. Intermediate sha1 `69b11a31d42cf248567d100786e9d4d64d7b5932`. (ii) Then in `run()`: `if rep.count(SKIP):` → `if rep.count(SKIP) or len(rep.rows) != 9:` (8-space indentation; occurrence count 1). Net +210 bytes. No other change. |
| `rules_as_data.yaml` | Line 14: the value `v0.2-PROTOTYPE` → `v0.3-PROTOTYPE`. The comment on the same line unchanged. Same byte count (4,920). Stored in Box under the name `rules_as_data.txt` (connector extension rule), bytes identical. |
| `manifest-live.json`, `manifest-sealed.json`, `manifest-boxlive-2026-09-06.json` | Regenerated by the revised `oracle_gen.py` from the unchanged seeds. Each differs from its round-1 counterpart in exactly two lines: `oracle_version` (`v0.2-PROTOTYPE` → `v0.3-PROTOTYPE`) and `rules_digest` (`314c5174…` → `e7fbe6ff…`). Member lists and all pin values identical to round 1. |
| `VALIDATION-LOG-2026-09-06-round2.md` | New. Producer-written header + verbatim machine output of one scripted run. |
| `CHANGE-RECORD.md` | New, authored: the swaps with diffs, identities, re-validation table, negative-control outputs, flags for JR. |
| `nc2_driver.py` | Test harness, local only, NOT delivered: imports the revised `oracle_lint` unchanged, mirrors its argument parser, and in mode `silent` replaces `c_harness_cross_section` with a stub that records no row; mode `dup` wraps it to record an extra row; mode `none` is unmodified. Its full text is not in the delivery; its behaviour is in the log. |
| Box, other | `round-2` subfolder created in OUT. No other Box write. |
| Outside Box | Round-2 set committed to GitHub branch `claude/oracle-gen-a9-delivery-i5xmkb` of `rodwel-cmyk/temp` (commit hash in the session report). |

Verbatim diffs of both code files are in CHANGE-RECORD.md §1; the byte-level manifest delta is in the log.

### Measured behaviour after the change (from the log)

| check | before (round 1) | after (round 2) |
|---|---|---|
| `repin-dryrun` / `gen --source boxlive` with corpus root `000000000000` | not tested (no check existed) | `boxlive corpus root folder id mismatch`, exit 1 |
| `repin-dryrun` with the staged corpus (root `396978339615`) | NO DRIFT, exit 0 | NO DRIFT, exit 0 |
| `--enforce` with 8 recorded rows (silent-stub driver) | PASS, exit 0 | REFUSED `incomplete coverage under --enforce`, exit 1 |
| `--enforce` with 10 recorded rows (duplicate-row driver) | not tested | REFUSED, exit 1 |
| `--enforce` with 9 rows, unmodified driver | PASS | PASS, exit 0 |
| `--enforce` on the boxlive manifest | REFUSED (L9 SKIP) | 9 PASS / 0 FAIL / 0 SKIP, PASS |
| `version-lock` of the round-1 (v0.2) manifests | LOCKED | REFUSED (two reasons each) |
| `validate`, `anchor-demo` | ALL MATCH; PASS/FAIL/FAIL | unchanged |
| corpus with no `_source_folders` key (observation) | NO DRIFT, exit 0 (no check) | `AttributeError: 'NoneType' object has no attribute 'get'`, exit 1 |

## (d) OPEN QUESTIONS / RISKS — what is unverified or uncertain

1. **Hardcoded literal `9`.** The guard `len(rep.rows) != 9` is correct for the nine checks that exist; a future
   check added or removed without bumping the literal makes `--enforce` refuse every manifest. Recorded in
   CHANGE-RECORD §5.1; the verbatim text was not altered.
2. **NC2 is a simulation.** The stock linter always records nine rows, so the eight-row scenario was constructed by
   replacing one check with a silent stub in a driver. The guard's bite on a naturally occurring silent check is
   therefore demonstrated by simulation, not reached by any input to the unmodified program.
3. **AttributeError path.** A corpus lacking `_source_folders` crashes with a traceback rather than the clean
   refusal (exit 1 either way). The swap was applied exactly as given; not hardened.
4. **Indentation normalisation.** Both swaps were applied at the files' own indentation, the instruction having
   shown each block with four extra leading spaces. The relative structure is identical; whether "verbatim" was meant
   to include the outer indentation is a reading, recorded here.
5. **Changelog comment.** `rules_as_data.yaml` line 14's comment still describes the v0.2 change.
6. **`--boxlive` default** in `oracle_lint.py` points at the dated snapshot beside the script.
7. **Single-seat, single-machine claims;** the same connector performed write and read-back; files passed through
   the model as text at both hops, sha1-verified at each.
8. **Round-1 files remain in the OUT root** under their canonical names and now fail the v0.3 lock; the deliverable
   is the `round-2` folder. Nothing marks the root copies as superseded other than CHANGE-RECORD §5.6.
9. **Connector rename** of `rules_as_data.yaml` to `.txt`, as in round 1.
10. **Pins unchanged by construction.** The manifests' pin values are identical to round 1 because the seeds did
    not change; no live-engine read occurred in this round either.

*END of evidence. No verdict is offered here.*
