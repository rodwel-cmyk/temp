# A9 GENERATOR — MAX SEAT CLOSE-OUT / HANDOFF RECORD — 2026-09-07

**Written by** the Max drafting seat (Fable, `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **Instrument** Box MCP connector (reads by direct folder id; text uploads; no raw API) · **AUTHORITY: NONE.**
This is the single close-out record for the A9 generator build sessions of 2026-09-06/07. It authorises nothing,
retires nothing, re-points nothing. **A fresh Stage-3b builder re-grounds from this file plus the Box/disk objects
it names — not from the session that wrote it.** Every figure below was measured by this seat unless marked
*relayed*; relayed figures are JR's statements and were not verifiable from this identity.

---

## 0 · Status at close

**Build consumed** (*relayed by JR, 2026-09-07*): the `round-2-hardened` set — nine files, generator
`oracle_gen.py` `520f83042f3ad1f063064e6f1995b30ec021d74c` — was promoted to the org tier by the Teams seat and
byte-verified on read-back: all nine VERIFIED, `version_number == 1`, landed in Box **`oracle-manifest/`
`415887502885`** under Cowork-Layer1-Tooling `396978339615`. Nothing retired, nothing re-pointed; the live oracle
`a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7` is untouched. That zone is outside this identity's visibility by design,
so this seat records the promotion as relayed and did not read it.

**Exchange state, measured 2026-09-07 by folder listing** (the last act of this session, no write in between):

| folder | id | state |
|---|---|---|
| `A9 Generator -IN` | 415602830059 | 17 items, every server sha1 equal to the first listing of 2026-09-06 — never modified by this seat |
| `A9 Generator - OUT` root | 415603610278 | the 11 round-1 files (v0.2 set + round-1 records) + 2 subfolders; unchanged since 2026-09-06 |
| `OUT/round-2` | 415677707437 | 9 files, unchanged since 2026-09-06 (v0.3 set, pre-hardening generator) |
| `OUT/round-2-hardened` | 415820305904 | 9 files, unchanged since 2026-09-07 — **the consumed set (§2)** |

## 1 · Clean-desk check

- **No un-delivered or in-progress artefact exists in the exchange.** Every artefact this seat produced is in OUT,
  in one of the three generations above, and the current one is `round-2-hardened`. Nothing was deleted, and
  nothing needs deleting: the older generations are superseded evidence (the root set is refused by the v0.3
  lock; `round-2/oracle_gen.py` `3bfa706e…` is the pre-hardening generator).
- **Local-only, by design, not deliverables** — all described in the delivered records, none needed to re-ground:
  `nc2_driver.py` (the NC2 silent-stub harness; its behaviour is verbatim in the round-2 log); the negative-control
  corpora (one-line edits of the staged snapshot: wrong root, key removed, `null`, plus today's string/list/`{}`/
  `0`/`false`/integer variants); the machine diffs (embedded verbatim in `CHANGE-RECORD.md`); the raw run logs
  (embedded verbatim in the three VALIDATION-LOGs); scratch working directories.
- **GitHub mirror.** The three OUT generations are committed to `rodwel-cmyk/temp`, branch
  `claude/oracle-gen-a9-delivery-i5xmkb`, under `a9-generator/OUT/`, `a9-generator/round-2/`,
  `a9-generator/round-2-hardened/` (commits `8f7433f`, `976dd2f`, `d12633c`), with `rules_as_data.yaml` under its
  proper name. A recoverable copy, not a governed substrate. This record is committed there too.
- No ClickUp access was used at any point. No write outside `415603610278` was made in any session.

## 2 · Final delivered state — the consumed set, `OUT/round-2-hardened` (415820305904)

| file | Box id | bytes | sha1 (server read-back == local) |
|---|---|---|---|
| `oracle_gen.py` | 2451284224000 | 18,865 | `520f83042f3ad1f063064e6f1995b30ec021d74c` |
| `oracle_lint.py` | 2451282227434 | 10,963 | `4a6e37d34095a2eecde84b13a65403c3f12d2ecd` |
| `rules_as_data.txt` — bytes of `rules_as_data.yaml` v0.3 | 2451297102737 | 4,920 | `e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8` |
| `manifest-live.json` | 2451293312585 | 2,425 | `4782d015a1838bc13988173debd7aea98cf16952` |
| `manifest-sealed.json` | 2451293039647 | 2,419 | `4f9f57b5263ff804dd95e350d8fb061270cf432b` |
| `manifest-boxlive-2026-09-06.json` | 2451291909301 | 2,449 | `4dbc9787678610c10a26cf8c9312247c4b602b24` |
| `VALIDATION-LOG-2026-09-07-round2-hardened.md` | 2451292876086 | 14,592 | `d20ff22aac76fcfbf6b6e54ff5a6767792992be0` |
| `CHANGE-RECORD.md` | 2451302094558 | 21,903 | `bc82a11bf63944b412291fb1ccaa4098b167d0c2` |
| `ROUND-2-REVIEW-FEED.md` | 2451303932736 | 16,202 | `2715f1a106727faf5ebeb9905df64a26e0515bcd` |

The connector stores the rules file as `.txt`; the bytes are `rules_as_data.yaml` and must carry that name wherever
the generator runs (`oracle_gen.py` resolves `RULES` by basename; the S5 digest is over these bytes). The three
manifests are the oracle's assembled identity (Appendix C); their pins are in §4.4. The two `.md` records carry the
full change history, verbatim diffs, the round-2 validation, and every negative control.

## 3 · Known residuals — owed, not done here

1. **boxlive `_source_folders` hardening covers 2 of the 4 cases.** Measured 2026-09-07 on `520f8304…`:

   | `_source_folders` value | behaviour of `repin-dryrun` |
   |---|---|
   | key missing | `boxlive corpus root folder id mismatch`, one line, exit 1 |
   | `null` | same clean refusal, exit 1 |
   | `{}` · `0` · `false` | same clean refusal, exit 1 |
   | **truthy string** (`"x"`) | `AttributeError: 'str' object has no attribute 'get'` — traceback, exit 1 |
   | **truthy list** (`["x"]`) | `AttributeError: 'list' object has no attribute 'get'` — traceback, exit 1 |
   | valid dict, `root` as JSON number `396978339615` | accepted (comparison is by `str()`); NO DRIFT, exit 0 |

   Every case fails closed (non-zero exit), but two are crashes, not refusals. **A full 4-case fix is owed** — for
   example an `isinstance(…, dict)` guard before `.get` — and it is a generator edit, so it takes a
   `rules_version` bump (v0.4) plus the full gate and NC1a–d, and Gemini review. Not started.
2. **Linter re-point + the deploy/execution half — DEFERRED to Stage-3b.** As relayed, nothing was re-pointed: the
   deployed linter's target is still the frozen oracle `a87ce510…`; the promoted set in `oracle-manifest/` is not
   yet what the linter executes against. Stage-3b's brief, not this record's, defines that work.
3. **Hardcoded check count.** `oracle_lint.py` refuses under `--enforce` unless exactly nine rows are recorded
   (`len(rep.rows) != 9`). Any check added or removed must bump that literal in the same edit, or every manifest is
   refused with `incomplete coverage` (fail-closed).
4. **Changelog comment** on `rules_as_data.yaml` line 14 still describes v0.2; only the version value was bumped.
5. **`--boxlive` default** in `oracle_lint.py` names the dated snapshot beside the script; always pass `--boxlive`
   explicitly.
6. **NC2 is a simulation**: the stock linter always records nine rows, so the coverage guard was proven with a
   silent-stub driver, not by an input to the unmodified program.
7. **Write-time re-pin (BARRED-13).** This seat never read the engine folders; every pin it reports was re-derived
   from the staged, dated seeds. Whether a write-time `repin-dryrun` against the live engine was run at promotion
   is not known to this seat — Stage-3b should confirm it from the Teams promotion record before any re-point.
8. **Review status of the hardening.** Section (e) of `ROUND-2-REVIEW-FEED.md` flags the one-token hardening as
   JR-directed and unreviewed; the round-2 review outcome was not relayed to this seat. The set was promoted on
   JR's decision as relayed.
9. **Three generations sit in OUT** under canonical filenames. A consumer must take `round-2-hardened`; nothing in
   Box marks the older folders as superseded except the records.

## 4 · Build context for a FRESH Stage-3b builder — re-ground from Box and disk, not from this session

### 4.1 Where things are (Box ids; access is by direct id — the exchange parent `402946233341` is not visible)

- **Consumed set:** `OUT/round-2-hardened` (§2). Mirror: GitHub path `a9-generator/round-2-hardened/` at `d12633c`.
- **Seeds, in IN `415602830059`** (dated observations — re-derive at use): `inventory-390802629329-2026-09-04-1650Z.json`
  2450234898780 (350,581 B, `94cb9b1a4efbf96ac10a8a60e9c77c096721e447`; 722 records, 16:50Z 2026-09-04);
  `oracle-model-SETPIN-2026-07-28.json` 2450238904095 (1,513 B, `9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982`; the
  sealed snapshot); `corpus-boxlive-2026-09-06.json` 2449860815455 (1,600 B, `9c1997090fe403476554168a2aaee3abf8e28b87`;
  the Teams seat's 2026-09-06 live read, shape `{"files": {relpath: sha1}}` with `_source_folders` and `_read_at`).
- **Method documents, in IN:** `HANDOFF.md` 2449864551821 · `SEEDS-RUNBOOK.md` 2450241224989 (the explicit-flag
  invocation and the flat-folder defect) · `SET-IDENTITY-live-computation-2026-09-04.md` 2450238882415 (the algorithm's
  source) · `CHECKPOINT-oracle-codecli-2026-09-04.md` 2449861192168 (77,165 B, `b765d4ee82740c71819204f64abcd9a795093039`
  — use this identity, not the stale 74,181/`b2e2db48…` in OPEN-DECISIONS §5) · `README-PROTOTYPE.md` 2449862905859 ·
  `GENERATOR-INPUTS.md` 2449860347356 · `OPEN-ITEMS-DISPOSITION-2026-09-06.md` 2449859195133 ·
  `OPEN-DECISIONS-oracle-2026-09-06.md` 2449865068792 · `APPENDIX-C-SLICE-sectioned-oracle-2026-09-06.md` 2449866507942
  (its prose aggregation is wrong; use the code).
- **Round-1 handoff:** `OUT/HANDOFF-BACK.md` 2450316795901 — target recommendation and the write-time steps.
- **Org-tier landing** (*relayed*): `oracle-manifest/` 415887502885 under `396978339615`. Not visible to `183820787`.
- **Engine folders:** `396978339615` (4 governed root files) and `403356419210` (`l1lint/`, 12 files). **Not visible to
  identity `183820787`**; a Max builder cannot read them unless newly granted. Hash-not-ingest applies: never open the
  members' bytes; read server-side sha1s only.

### 4.2 The member set — 16 relpaths in `members_ordered` order, with the sha1s as recorded in the staged 2026-09-06 snapshot (DATED; BARRED-13 — re-derive at use)

| # | relpath | sha1 in the 2026-09-06 snapshot |
|---|---|---|
| 1 | `layer1_lint.py` | `79db9696e92d6320bd909c1f621fc531caefed6a` |
| 2 | `l1lint/__init__.py` | `ffcc84384fbc969e7373d79eaf98705aec9ab2a7` |
| 3 | `l1lint/checks.py` | `2b21e531ce1b97a49aaf08faa7836561dbd635a4` |
| 4 | `l1lint/cli.py` | `b1fc79f470ebbe88b7e29f5a1f9e2fdf3005f425` |
| 5 | `l1lint/dochygiene.py` | `6e82c80abd0e5ae0c8e9496ef107321a3967106b` |
| 6 | `l1lint/engine.py` | `1a8e16fa7effb7d04ec9ef231bb8259c0560c202` |
| 7 | `l1lint/hygiene.py` | `4032a64b30d3df63c6acc06c676fbf6c23d46a5e` |
| 8 | `l1lint/loader.py` | `e753dd158ecf840264f347a8fd701ea39b5d3810` |
| 9 | `l1lint/org_mirror.py` | `da11d42f916e9275c8c564d836f96e4d3153ec6d` |
| 10 | `l1lint/parsing.py` | `af3289953daaffb5b1ccc14d03714dfe0d8f648f` |
| 11 | `l1lint/pins.py` | `a658517293c218aa950f45b54ad81e9c1615186c` |
| 12 | `l1lint/selftest.py` | `e65c0d558c5f7457aea3eafdc4415285a9396815` |
| 13 | `l1lint/xdoc.py` | `53c6d212873123f7b5d9d186c422e88ea6ac17a3` |
| 14 | `manifest.yaml` | `0397bfd11cfe8023aa7eb4808681d0bd598ddad3` |
| 15 | `baseline.md` | `dd5da45a1f93963c6f1c381e9dcd292f6f79333d` — also the Layer 1 pointer bytes; a pointer paste moves the set (CHECKPOINT §4) |
| 16 | `test_layer1_lint.py` | `a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85` — the governed harness (64,501 B); the sealed snapshot has `3574c2d13a7f34f7cd8d1bac3543b05556e18ef9` here instead |

`engine15` is the same set minus `test_layer1_lint.py`. The set is defined by these declared relpaths, never by
enumerating a folder; non-member files in the root folder (e.g. `oracle_layer1_lint.py`) do not enter the pin.

### 4.3 `rules_as_data.yaml` v0.3-PROTOTYPE — identity and structure

`e7fbe6ff49a435e5a2c6cb3aa3c2dad0391b81d8`, 4,920 B. `schema: oracle-generator-rules-v0-PROTOTYPE`;
`rules_version: v0.3-PROTOTYPE`. Two sections, and only two — boundaries beyond them must be ruled, not invented:

- `engine_set` — `kind: set`, `layer: SET`, `aggregation: _set_sha1`, `corpus_root_folder_id: "396978339615"`,
  `members_ordered` = §4.2, `pin_keys: {full: set16_set_sha1, subsets: {engine15_set_sha1: [test_layer1_lint.py]}}`,
  `expected_pins`: `engine15_set_sha1` `9520867753d0d26ec76e959d1a98a450d24255fa` (LIVE-POSITIVE);
  `set16_set_sha1_live` `df59d6f66748ba6e45e897ca724dc1126a3a536e` (LIVE-POSITIVE; re-derive at write time);
  `set16_set_sha1_sealed` `ccda65118beb01d742c60f86cea140828de2ad9d` (NEGATIVE-GUARD; never assert as live).
- `harness` — `kind: file`, `layer: FILE`, `relpath: test_layer1_lint.py`, `expected_pins`: `file_sha1_live`
  `a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85` (LIVE-POSITIVE); `file_sha1_sealed` `3574c2d13a7f34f7cd8d1bac3543b05556e18ef9`
  (NEGATIVE-GUARD).

**S5 lock:** every manifest is stamped with `oracle_version` (= `rules_version`) and `rules_digest` (= sha1 of the
rules bytes); `version-lock` refuses on either mismatch, and absence is a refuse. Any edit to the rules — and, by the
runbook's convention, any edit to the generator or linter code — takes a bump and a full re-validation. The v0.3 bump
was made for the round-2 code changes; the 2026-09-07 one-token hardening was applied without a bump on JR's direction.

### 4.4 The set-sha1 derivation — the aggregation of record, verbatim from `oracle_gen.py::set_sha1`

```python
def set_sha1(entries):
    """sha1 over the SORTED (relpath, per-file sha1) manifest,
    serialised as 'relpath\\x00sha1\\n' per entry."""
    h = hashlib.sha1()
    for rel, sha in sorted(entries):
        h.update(rel.encode("utf-8")); h.update(b"\x00")
        h.update(sha.encode("ascii")); h.update(b"\n")
    return h.hexdigest()
```

One running sha1 over the sorted `(relpath, sha1hex)` pairs, each serialised as `relpath + 0x00 + sha1hex + 0x0A`.
The Moving-Plan Appendix C paraphrase ("per-entry hash → concatenate → sha1") does **not** reproduce the pins. Proof
by computation: over §4.2 this yields `set16 = df59d6f6…` and `engine15 = 9520…`; with the harness swapped to
`3574c2d1…` it yields the sealed guard `ccda6511…` — `validate` shows all six. **Two-level pin:** the SET layer
(set16, engine15) and the FILE layer (the harness sha1) are pinned separately in the manifest; the FILE pin and the
SET member for the harness must agree (lint L8).

### 4.5 Invocation discipline and the gate (expected results on the consumed set)

Flat directory; Python 3 + PyYAML; the defaults resolve one level up and break in a flat folder, so always pass the
seeds explicitly (`--inventory`, `--setpin`, `--boxlive` before the subcommand on `oracle_gen.py`):

```
python3 oracle_gen.py --inventory $INV --setpin $SP --boxlive $BL validate        # ALL MATCH, six pins, exit 0
python3 oracle_gen.py --inventory $INV --setpin $SP --boxlive $BL anchor-demo     # [1] PASS [2] FAIL [3] FAIL, exit 0
python3 oracle_gen.py version-lock <manifest>                                     # LOCKED, exit 0 (each of the three)
python3 oracle_lint.py --inventory $INV --setpin $SP [--boxlive $BL] <manifest> --enforce   # 9 PASS / 0 FAIL / 0 SKIP
python3 oracle_gen.py --boxlive $BL repin-dryrun                                  # NO DRIFT; guard not tripped
python3 oracle_gen.py --boxlive $BL gen --source boxlive --out <manifest>         # the write-time manifest
```

Negative controls that must hold: wrong `root` or missing/`null` `_source_folders` → `boxlive corpus root folder id
mismatch`, exit 1; a linter run recording other than nine rows under `--enforce` → `incomplete coverage`, exit 1;
bare defaults in a flat folder → `FileNotFoundError`, exit 1; the round-1 v0.2 manifests against the v0.3 rules →
`version-lock` REFUSED. `manifest-live.json` and `manifest-sealed.json` regenerate byte-identical from the seeds; the
boxlive manifest regenerates byte-identical from the same corpus file.

### 4.6 What Stage-3b is understood to own, and the seat rules that still bind a Max builder

- Owns (as relayed): the linter re-point and the deploy/execution half; the 4-case `_source_folders` fix under a v0.4
  bump; anything that changes the check count with the matching literal bump; each with negative controls, a
  REVIEW-FEED for Gemini, and delivery through the exchange for the Teams/CCG seat to apply under GATE-V.
- Still binding: authority NONE; no S9 or org-tier write from the Max seat; no ClickUp; no deletes; output only to
  the exchange OUT folder; no engine read without access (and hash-not-ingest even with it); no invented sections;
  no silent generator edit — bump and re-validate; state `--selftest`/gate results as claims for the applier to re-run.

## 5 · Instrument facts a fresh Max will hit immediately

- The Box MCP connector authenticates as `183820787`; IN and OUT are reachable by id only; the exchange parent is not.
- Uploads are text-only and extension-filtered: `.yaml` becomes `.txt`; `.diff` becomes `.txt`. Duplicate filenames
  in a folder are refused — use a new subfolder for a re-delivery and `copy_file` for unchanged files (server-side,
  byte-exact). Read-back is by `get_file_details` with the `sha1` field, through the same connector.
- Large text reads are saved by the harness to a local file when they exceed the inline limit; verify the saved
  file's sha1 against the server value before use (this is how the 350 KB inventory was transferred, sha1-verified).
- No raw-API instrument, no token re-mint, no 401/403 was encountered in any session.

## 6 · Session record

| date | round | outcome |
|---|---|---|
| 2026-09-06 | round 1 | staged set validated full-strength from the seeds; 11 files to OUT root; HANDOFF-BACK; L9 gap found, patch proposed |
| 2026-09-06 | round 2 | Gemini Review-1 REVISE applied verbatim (root-check; coverage guard); L9 patch adopted; bump to v0.3; NC1/NC2 proven; 9 files to `round-2` |
| 2026-09-07 | hardening | JR-directed one-token change; manifests byte-identical; NC1b proven; 9 files to `round-2-hardened`; consumed (relayed) |
| 2026-09-07 | close-out | clean desk verified; this record; session closed |

*END — Max seat closed. Authority: NONE. No governed write, no ClickUp, no delete, IN untouched throughout.*
