# ROUND-2-REVIEW-FEED — A9 generator, delta pack for Gemini round 2 — updated 2026-09-07 with a JR-DIRECTED hardening

**Purpose.** Evidence for the independent reviewer, scoped to the delta since Review 1: the two changed files, the
re-validation, the negative controls, and — added 2026-09-07 — a **JR-directed** one-token hardening of
`oracle_gen.py` (section (e)). It states what was, what is, what changed, and what is unverified. It contains no
review criteria and no conclusion about the quality of the output.

**Producer.** Max drafting seat (Fable, `claude-fable-5-1`) · Box identity rodwel@me.com (`183820787`) · Box MCP
connector only · Authority: NONE. Output type: code-change set. Round-1 items reported CLEAR (rules content,
manifests' structure, documents, the L9 patch) are not re-argued here; they are listed only where their bytes
changed as a consequence of this round.

> **FLAG — section (e) is JR-DIRECTED, not reviewer-authored.** The hardening was requested by JR after the
> round-2 delivery and applied by the producer. It has not been reviewed by anyone. It is presented here for
> adversarial review in round 2; nothing in this file asks the reviewer to assume it correct.

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

### The Review-1 instructions, as relayed (the input round 2 executes)

1. `oracle_gen.py` — replace the four-line `if source == "boxlive": … return corpus_from_json(boxlive_path)` block
   with the seven-line block that binds `c, m`, compares `str(m.get("source_folders", {}).get("root"))` to
   `str(root_folder_id)`, raises `SystemExit("boxlive corpus root folder id mismatch")` on mismatch, and returns `c, m`.
2. `oracle_lint.py` — replace `if rep.count(SKIP):` (the coverage refusal in `run()`) with
   `if rep.count(SKIP) or len(rep.rows) != 9:`.
3. Adopt the cleared L9 patch into `oracle_lint.py`.
4. Bump `rules_version` v0.2-PROTOTYPE → v0.3-PROTOTYPE; regenerate all three manifests.
5. Re-validate; 6. negative controls NC1 and NC2; 7–9. records and delivery.

### The JR direction of 2026-09-07, as relayed (the input section (e) executes)

In `oracle_gen.py`, `load_corpus` boxlive branch, change exactly
`if str(m.get("source_folders", {}).get("root")) != str(root_folder_id):` to
`if str((m.get("source_folders") or {}).get("root")) != str(root_folder_id):`; nothing else; no version bump;
regenerate and confirm byte-identical manifests; re-validate; NC1a, NC1b (missing key → clean refusal), valid corpus.

### Pre-state of the delivery folder

`A9 Generator - OUT` (`415603610278`) held the 11 round-1 files, all at their round-1 sha1s; no `round-2` folder
existed before round 2, and no `round-2-hardened` folder existed before 2026-09-07.

## (b) OUTPUT — post-state

### Round 2 (2026-09-06) — `round-2` subfolder `415677707437`

| file | Box id | bytes | sha1 (server read-back) |
|---|---|---|---|
| `oracle_gen.py` — *superseded by (e)* | 2450403165211 | 18,861 | `3bfa706e264ddd630795685d88449c42798749a9` |
| `oracle_lint.py` | 2450403366687 | 10,963 | `4a6e37d34095a2eecde84b13a65403c3f12d2ecd` |
| `rules_as_data.txt` (bytes of `rules_as_data.yaml` v0.3) | 2450404583942 | 4,920 | `e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8` |
| `manifest-live.json` | 2450410605150 | 2,425 | `4782d015a1838bc13988173debd7aea98cf16952` |
| `manifest-sealed.json` | 2450408239004 | 2,419 | `4f9f57b5263ff804dd95e350d8fb061270cf432b` |
| `manifest-boxlive-2026-09-06.json` | 2450403755460 | 2,449 | `4dbc9787678610c10a26cf8c9312247c4b602b24` |
| `VALIDATION-LOG-2026-09-06-round2.md` | 2450411824536 | 18,880 | `08fd9840413e5bd6c4ff3821bf7285553d157e1d` |
| `CHANGE-RECORD.md` (round-2 text) | 2450412940020 | 14,725 | `a4aaced19dfd07711bbdd07a4e65173f7e361ed5` |
| `ROUND-2-REVIEW-FEED.md` (round-2 text) | 2450410533530 | 9,958 | `539547a16d52ec253733d67e04290d147999c513` |

### Current delivery (2026-09-07) — `round-2-hardened` subfolder `415820305904`

| file | Box id | bytes | sha1 (server read-back) | origin |
|---|---|---|---|---|
| `oracle_gen.py` | 2451284224000 | 18,865 | `520f83042f3ad1f063064e6f1995b30ec021d74c` | uploaded — the hardened file |
| `oracle_lint.py` | 2451282227434 | 10,963 | `4a6e37d34095a2eecde84b13a65403c3f12d2ecd` | server-side copy of round-2 file |
| `rules_as_data.txt` | 2451297102737 | 4,920 | `e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8` | server-side copy |
| `manifest-live.json` | 2451293312585 | 2,425 | `4782d015a1838bc13988173debd7aea98cf16952` | server-side copy |
| `manifest-sealed.json` | 2451293039647 | 2,419 | `4f9f57b5263ff804dd95e350d8fb061270cf432b` | server-side copy |
| `manifest-boxlive-2026-09-06.json` | 2451291909301 | 2,449 | `4dbc9787678610c10a26cf8c9312247c4b602b24` | server-side copy |
| `VALIDATION-LOG-2026-09-07-round2-hardened.md` | 2451292876086 | 14,592 | `d20ff22aac76fcfbf6b6e54ff5a6767792992be0` (local; read-back in the session report) | uploaded |
| `CHANGE-RECORD.md` (updated) | assigned at upload — see session report | — | local sha1 in the session report | uploaded |
| `ROUND-2-REVIEW-FEED.md` (this file) | assigned at upload — see session report | — | — | uploaded |

All rows with a Box id: `version_number` 1, `created_by` `183820787`. The 11 round-1 files in the OUT root and the
9 round-2 files were not modified. IN was not modified (17/17 sha1s equal before and after both rounds).

## (c) CHANGE-MANIFEST — factual, per item

| item | what happened |
|---|---|
| `oracle_gen.py` (round 2) | One block replaced in `load_corpus` (lines 83–89 of the staged file): 4 lines → 7 lines, text as instructed. The block was applied at the file's indentation (4 spaces), the instruction having shown it with 4 extra leading spaces. Occurrence count before replacement: 1. Net +171 bytes. |
| `oracle_gen.py` (2026-09-07, JR-directed) | Line 87 only: `m.get("source_folders", {})` → `(m.get("source_folders") or {})`. Occurrence count before replacement: 1. Net +4 bytes. `3bfa706e…` → `520f8304…`. No other line touched. See (e). |
| `oracle_lint.py` | Three edits (round 2). (i) Patch `95bf61c4…` applied with `patch -p0` to the staged file: `c_determinism` kind map gains `"boxlive": "boxlive"`; `G.load_corpus` call gains a fifth argument `getattr(args, "boxlive", None)`; `main()` gains `ap.add_argument("--boxlive", default=os.path.join(G.HERE, "corpus-boxlive-2026-09-06.json"))`. Intermediate sha1 `69b11a31d42cf248567d100786e9d4d64d7b5932`. (ii) Then in `run()`: `if rep.count(SKIP):` → `if rep.count(SKIP) or len(rep.rows) != 9:` (8-space indentation; occurrence count 1). Net +210 bytes. Unchanged on 2026-09-07. |
| `rules_as_data.yaml` | Line 14: the value `v0.2-PROTOTYPE` → `v0.3-PROTOTYPE`. The comment on the same line unchanged. Same byte count (4,920). Stored in Box under the name `rules_as_data.txt` (connector extension rule), bytes identical. Unchanged on 2026-09-07. |
| `manifest-live.json`, `manifest-sealed.json`, `manifest-boxlive-2026-09-06.json` | Regenerated in round 2 by the revised `oracle_gen.py` from the unchanged seeds; each differs from its round-1 counterpart in exactly two lines (`oracle_version`, `rules_digest`). Regenerated again on 2026-09-07 with the hardened generator: `cmp` byte-identical to the round-2 files. Member lists and all pin values identical to round 1. |
| `VALIDATION-LOG-2026-09-06-round2.md` | New in round 2. Producer-written header + verbatim machine output of one scripted run. |
| `VALIDATION-LOG-2026-09-07-round2-hardened.md` | New on 2026-09-07. Same structure; covers the hardening run. |
| `CHANGE-RECORD.md` | Round-2 text plus a §0A addendum for the hardening; round-2 sections kept, with lines marked *superseded by §0A* where the generator changed. |
| `nc2_driver.py` | Test harness, local only, NOT delivered: imports the revised `oracle_lint` unchanged, mirrors its argument parser, and in mode `silent` replaces `c_harness_cross_section` with a stub that records no row; mode `dup` wraps it to record an extra row; mode `none` is unmodified. |
| NC corpora | Local only, NOT delivered: the staged snapshot with `root` set to `000000000000` (NC1a); with the `_source_folders` key removed (NC1b); with `_source_folders` set to `null` (NC1c). |
| Box, other | `round-2` and `round-2-hardened` subfolders created in OUT; five files copied server-side from `round-2` to `round-2-hardened`. No other Box write. |
| Outside Box | Both sets committed to GitHub branch `claude/oracle-gen-a9-delivery-i5xmkb` of `rodwel-cmyk/temp` (commit hashes in the session reports). |

### Measured behaviour after the round-2 changes (from the round-2 log)

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
| corpus with no `_source_folders` key (observation) | NO DRIFT, exit 0 (no check) | `AttributeError: 'NoneType' object has no attribute 'get'`, exit 1 — *changed again by (e)* |

## (d) OPEN QUESTIONS / RISKS — what is unverified or uncertain

1. **Hardcoded literal `9`.** The guard `len(rep.rows) != 9` is correct for the nine checks that exist; a future
   check added or removed without bumping the literal makes `--enforce` refuse every manifest. Recorded in
   CHANGE-RECORD §5.1; the verbatim text was not altered.
2. **NC2 is a simulation.** The stock linter always records nine rows, so the eight-row scenario was constructed by
   replacing one check with a silent stub in a driver. The guard's bite on a naturally occurring silent check is
   therefore demonstrated by simulation, not reached by any input to the unmodified program.
3. **AttributeError path — changed by a JR-directed edit, see (e).** In round 2 a corpus lacking `_source_folders`
   crashed with a traceback (exit 1). On 2026-09-07 JR directed a one-token change that routes that case to the clean
   refusal. Whether that change is correct, complete, and free of side effects is a question for the reviewer; the
   producer applied it as directed and measured it, nothing more.
4. **Indentation normalisation.** Both round-2 swaps were applied at the files' own indentation, the instruction
   having shown each block with four extra leading spaces. The relative structure is identical; whether "verbatim"
   was meant to include the outer indentation is a reading, recorded here.
5. **Changelog comment.** `rules_as_data.yaml` line 14's comment still describes the v0.2 change.
6. **`--boxlive` default** in `oracle_lint.py` points at the dated snapshot beside the script.
7. **Single-seat, single-machine claims;** the same connector performed write and read-back; uploaded files passed
   through the model as text at both hops, sha1-verified at each; the five server-side copies did not pass through
   the model.
8. **Three generations of files now sit in OUT** — root (v0.2), `round-2` (v0.3, pre-hardening generator),
   `round-2-hardened` (v0.3, hardened generator). Nothing in Box marks the older ones as superseded except the
   records; a consumer picking the wrong folder gets a refused or un-hardened set.
9. **Connector rename** of `rules_as_data.yaml` to `.txt`, as in round 1.
10. **Pins unchanged by construction.** The manifests' pin values are identical to round 1 because the seeds did
    not change; no live-engine read occurred in any round.

## (e) JR-DIRECTED HARDENING ADDENDUM — 2026-09-07 — FLAGGED FOR ADVERSARIAL REVIEW

**Status.** JR-directed; producer-applied; **unreviewed**. Not a Review-1 finding. To be attacked in round 2, not
assumed correct.

**Pre → post.** `oracle_gen.py` `3bfa706e264ddd630795685d88449c42798749a9` (18,861 B) →
`520f83042f3ad1f063064e6f1995b30ec021d74c` (18,865 B). Every other file in the set is byte-identical to round 2.
`rules_as_data.yaml` unchanged, so no bump: `v0.3-PROTOTYPE`, digest `e7fbe6ff…`.

**The diff, verbatim:**

```
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
```

**Measured behaviour (verbatim in `VALIDATION-LOG-2026-09-07-round2-hardened.md`):**

| check | round-2 generator (`3bfa706e…`) | hardened generator (`520f8304…`) |
|---|---|---|
| three manifests regenerated | — | `cmp` byte-identical to the round-2 files (`4782d015…`, `4f9f57b5…`, `4dbc9787…`) |
| `validate` / `anchor-demo` / `version-lock` ×3 / `--enforce` ×3 | ALL MATCH / PASS-FAIL-FAIL / LOCKED / 9-0-0 | unchanged, same verdicts, all exit 0 |
| valid staged corpus, `repin-dryrun` | NO DRIFT, exit 0 | NO DRIFT, exit 0 |
| NC1a: `root` = `000000000000` | `boxlive corpus root folder id mismatch`, exit 1 | same, exit 1, on `repin-dryrun` and `gen --source boxlive` |
| NC1b: `_source_folders` key absent | `AttributeError: 'NoneType' object has no attribute 'get'`, traceback, exit 1 | `boxlive corpus root folder id mismatch`, one line, exit 1 (stdout+stderr = 1 line; 0 `Traceback`, 0 `AttributeError`) |
| NC1c: `_source_folders` = `null` | not measured in round 2 | `boxlive corpus root folder id mismatch`, exit 1 |

**Facts the reviewer may want, stated without conclusion.** The expression `(m.get("source_folders") or {})`
substitutes `{}` for every falsy value of `source_folders` — absent, `None`, `{}`, and also `0`, `""`, `False` —
so each of those now yields `root = None` and the mismatch refusal. A non-dict truthy value (for example a string or
a list) would still raise `AttributeError` on `.get`. The `root` comparison is by string equality after `str()`.
Nothing else in the boxlive path was changed, and the `corpus_from_json` adapter that produces `source_folders` is
unchanged.

**Delivery.** `round-2-hardened` (`415820305904`) — ids and sha1s in (b).

*END of evidence. No verdict is offered here.*
