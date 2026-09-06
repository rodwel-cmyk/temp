# A9 GENERATOR — HANDOFF-BACK — Max seat → Teams/CCG promotion — 2026-09-06

**Written by** the Max drafting seat (Fable, `claude-fable-5-1`) · **Box identity** rodwel@me.com (`183820787`)
· **Instrument** the Box MCP connector — the only Box credential this seat holds (no raw-API instrument, no
`~/.box/box_rw.py`, no token this seat can re-mint) · **AUTHORITY: NONE.** This file directs nothing and
authorises nothing. It records what was verified, what was written to `A9 Generator - OUT` (`415603610278`),
and what the promotion step still has to do itself.

Every figure below was **measured in this session** — server-side sha1/size read by folder or file id, local
`sha1sum`, or generator output. Document values appear only as the thing a measurement was compared against.
A value from this file must not be carried into a write: **BARRED-13 — re-derive at write time.**

---

## 0 · Verdict

1. The generator set validates **full-strength from the staged seeds**, in a flat directory, with explicit
   `--inventory` / `--setpin` / `--boxlive` flags exactly as SEEDS-RUNBOOK §1 prescribes:
   **validate ALL MATCH (6/6, incl. sealed `ccda6511`) · anchor-demo [1] PASS [2] FAIL [3] FAIL ·
   version-lock LOCKED (both manifests) · `oracle_lint.py --enforce` 9 PASS / 0 FAIL / 0 SKIP on both
   manifests · both manifests regenerate byte-identical to the staged ones.** Verbatim log: §6.
2. The commit-ready set is in OUT (§3). **Every file was read back: server sha1 == local, `version_number` 1,
   created by `183820787`.** No file in IN was modified (all 17 server sha1s re-listed after the writes, unchanged).
3. **The live re-pin at write time was NOT done here and cannot be done from this seat.** The engine folders
   `396978339615` and `403356419210` return *Item not found* to `183820787` — by design: this identity holds the
   A9 exchange only (JR, 2026-09-06). The pins in §2 are re-derivations from the **staged** corpora.
   **The Teams/CCG seat must re-derive against the live engine at the moment of the org-tier commit** — §5.

## 1 · Inputs verified — IN `415602830059`, 17 items

All 17 server-side sha1s were read by folder id (hash-not-ingest: no corpus bytes were fetched — the 16 engine
members were never opened, and their copies visible elsewhere in this account's Box were **not** used as a
corpus). The nine runtime files were pulled to disk and compared: **9/9 MATCH**.

| IN file | Box id | bytes | sha1 (server == local) |
|---|---|---|---|
| `rules_as_data.yaml` | 2449859682122 | 4,920 | `314c5174c1b5dbce14560e2c4d9838068859dbee` |
| `oracle_gen.py` | 2449860666966 | 18,690 | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` |
| `oracle_lint.py` | 2449860388492 | 10,753 | `7137aab2c1da72f017f317c06d1985eb8bd49f22` |
| `manifest-live.json` | 2449861430379 | 2,425 | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` |
| `manifest-sealed.json` | 2449863955142 | 2,419 | `6049beb18899cb06379a9bd34b8a382cfd3c4905` |
| `corpus-boxlive-2026-09-06.json` | 2449860815455 | 1,600 | `9c1997090fe403476554168a2aaee3abf8e28b87` |
| `oracle-model-SETPIN-2026-07-28.json` | 2450238904095 | 1,513 | `9f4fc6c7d28e0bc27d1288ae04aee10f35cc4982` |
| `inventory-390802629329-2026-09-04-1650Z.json` | 2450234898780 | 350,581 | `94cb9b1a4efbf96ac10a8a60e9c77c096721e447` |
| `CHECKPOINT-oracle-codecli-2026-09-04.md` | 2449861192168 | 77,165 | `b765d4ee82740c71819204f64abcd9a795093039` |

The other eight documents (HANDOFF, SEEDS-RUNBOOK, SET-IDENTITY, GENERATOR-INPUTS, README-PROTOTYPE,
OPEN-ITEMS-DISPOSITION, OPEN-DECISIONS, APPENDIX-C slice) were read in full; their server sha1s agree with
HANDOFF §6 and SEEDS-RUNBOOK §4 wherever those give full values. Inventory shape checked without printing
content: 722 records; folder `396978339615` present once; 21 file records under `/Cowork-Layer1-Tooling/`.

**HANDOFF §5 defects honoured.** Checkpoint used at `b765d4ee…` / 77,165 B — and the §5.2 finding was reproduced,
not carried: the sha1 of its first 74,181 bytes is `b2e2db48ea2bd581b3ed3ef0956d29a813e0dc5e`, so OPEN-DECISIONS
§5's `74,181 / b2e2db48…` is the stale pre-append identity. Aggregation: `oracle_gen.py::set_sha1` only; the
Appendix C prose was not used. Sections: `engine_set` + `harness` only; none invented.

## 2 · Pins — re-derived from the STAGED corpora · all MATCH · not a write-time derivation

| pin | re-derived here | corpus | vs recorded |
|---|---|---|---|
| `engine_set.engine15` | `9520867753d0d26ec76e959d1a98a450d24255fa` | inventory 2026-09-04 16:50Z **and** staged boxlive snapshot 2026-09-06 | **MATCH** |
| `engine_set.set16` | `df59d6f66748ba6e45e897ca724dc1126a3a536e` | same | **MATCH** |
| `harness.file` | `a3e678f22dd1b4a8e89005e4c1f5d668e4c92b85` | same | **MATCH** |
| `engine_set.set16` (sealed) | `ccda65118beb01d742c60f86cea140828de2ad9d` | setpin 2026-07-28 only | MATCH — **NEGATIVE GUARD, never assert as live** |
| `harness.file` (sealed) | `3574c2d13a7f34f7cd8d1bac3543b05556e18ef9` | setpin only | MATCH — NEGATIVE GUARD |

`repin-dryrun` on the staged snapshot: **NO DRIFT, guard not tripped** — this re-runs the Teams seat's
2026-09-06 read; it is not a new observation of the engine. **No drift of any kind was observed in this run.**

## 3 · What is in OUT `415603610278` — 11 files; each read back, server sha1 == local, version 1

| OUT file | Box id | bytes | sha1 | provenance |
|---|---|---|---|---|
| `oracle_gen.py` | 2450306185463 | 18,690 | `d9485e36989b859dc6423bec52b4c09a0aa26a1a` | bytes unchanged from IN |
| `oracle_lint.py` | 2450307280287 | 10,753 | `7137aab2c1da72f017f317c06d1985eb8bd49f22` | bytes unchanged from IN |
| `rules_as_data.txt` ⚠ | 2450303541471 | 4,920 | `314c5174c1b5dbce14560e2c4d9838068859dbee` | bytes unchanged from IN `rules_as_data.yaml`; **name changed by the connector** — see below |
| `manifest-live.json` | 2450301277807 | 2,425 | `e5993c1de7d888e308f5b5a09a2f89810e74ae8d` | regenerated here (`gen --source live`); byte-identical to IN |
| `manifest-sealed.json` | 2450305456260 | 2,419 | `6049beb18899cb06379a9bd34b8a382cfd3c4905` | regenerated here (`gen --source sealed`); byte-identical to IN |
| `corpus-boxlive-2026-09-06.json` | 2450298608696 | 1,600 | `9c1997090fe403476554168a2aaee3abf8e28b87` | unchanged from IN — the Teams seat's dated snapshot, evidence only |
| `manifest-boxlive-2026-09-06.json` | 2450304675825 | 2,449 | `54a545534922360cc7c35e595e25f92e234ede3b` | **new** — `gen --source boxlive` from that snapshot; evidence only, not the write-time manifest |
| `VALIDATION-LOG-2026-09-06.md` | 2450306787923 | 13,768 | `5f79e66f5be093cdf44b35e187182796e8af9eaa` | **new** — verbatim run log |
| `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt` | see session report | 1,498 | `95bf61c494cd82c12e3382bdf81181d61f383fde` | **new** — proposed, **NOT applied** (§7 item 3) |
| `REVIEW-FEED.md` | see session report | — | — | **new** — the independent reviewer's evidence pack |
| `HANDOFF-BACK.md` | see session report | — | — | this file (cannot carry its own hash) |

**Connector rename.** The connector's text-upload path accepts a fixed extension list; `.yaml` is not on it, so
`rules_as_data.yaml` was stored as **`rules_as_data.txt`** — identical bytes (sha1 `314c5174…`). **On apply, restore
the name `rules_as_data.yaml`:** `oracle_gen.py` resolves `RULES` by that basename and the S5 lock digests those bytes.

**Recommended commit object set — five files:** `rules_as_data.yaml`, `oracle_gen.py`, `oracle_lint.py`,
`manifest-live.json`, `manifest-sealed.json`, **plus the write-time pair the promotion step generates itself**
(`corpus-boxlive-<UTC>.json` + `manifest-boxlive-<UTC>.json`, §5). The 2026-09-06 snapshot pair in OUT is dated
evidence of this run, not that pair. The `.md`/`.txt` files are evidence for the review and the apply, not commit objects.

## 4 · Recommended canonical target and mode — a RECOMMENDATION; JR's per-action yes is required (HANDOFF §3 item 2)

- **Mode: NEW-FILE creates, not version-replace.** No governed object holds the oracle or the generator today, so a
  version-replace would edit an unrelated record. GATE-V's bifurcated version check therefore expects
  **`version_number == 1`** on every read-back.
- **Container: a new subfolder under Cowork-Layer1-Tooling `396978339615`** — the governed home of the engine set the
  oracle pins — for example `oracle-generator/`. Not the folder root: its four governed root files plus `l1lint/` are the
  pinned corpus and the root already carries non-member files. Not the Routines catalog `2328644291918`: CHECKPOINT §19.2
  shows it has no schema slot for a path set or a hash. Not the harness `2296699168749`: that is a corpus member, not a home.
- Rule honoured: CHECKPOINT §17.4 — a document cites an artefact's **home** copy; a staged copy is never an object of
  record. Everything in IN and OUT is a staging copy; the commit creates the home copies.
- **Caveat:** this seat cannot see `396978339615`, so this is grounded in the documents, not in a PRE-READ of the target.
  GATE-V PRE-READ + metadata baseline, the container-guard confirmation for the Tooling folder (HANDOFF §2), the Box
  principal ruling (HANDOFF §5.1) and the Rules §3.x concurrent-writer check with its recorded result are the promotion
  step's to perform.

## 5 · What the promotion step must do itself — Teams/CCG, with engine access — the live re-pin at write time

1. Principal ruling (HANDOFF §5.1); token re-mint immediately pre-write; §3.x concurrent-writer check, result recorded.
2. Read the **current** server-side sha1 of all 16 members **by folder id** — `396978339615` (4 root files) and
   `403356419210` (`l1lint/`, 12 files) — metadata only, never bytes. Write `corpus-boxlive-<UTC>.json` in the staged
   file's shape: `{"files": {relpath: sha1}}`, `l1lint/`-prefixed relpaths, `_read_at`, `_source_folders`.
3. `python3 oracle_gen.py --boxlive corpus-boxlive-<UTC>.json repin-dryrun` → require **NO DRIFT** and
   **negative guard tripped: no**. Any DRIFT, or a tripped guard → **STOP; JR.** Never commit on the recorded value.
4. `python3 oracle_gen.py --boxlive corpus-boxlive-<UTC>.json gen --source boxlive --out manifest-boxlive-<UTC>.json`
   → the write-time manifest. Keep the corpus file beside it (check L7 declares it by name).
5. Re-run the whole gate of §6 on the commit set — the applier's deterministic gate is the proof; this file is a claim.
6. GATE-V in full: PRE-READ + baseline → compose-without-loss → clobber-guard → create with `on_conflict=error` →
   read back persisted bytes **with a different instrument** → sha1/size → `version_number == 1` →
   VERIFIED / UNVERIFIED-SEMANTIC-FALLBACK / FAIL.

## 6 · Validation results — this seat's claim; verbatim in `VALIDATION-LOG-2026-09-06.md` (Box 2450306787923)

| command (flags explicit; flat dir) | result | exit |
|---|---|---|
| `oracle_gen.py … validate` | ALL MATCH — engine15/set16/harness live, engine15/set16/harness sealed; KEY TEST `ccda6511` MATCH | 0 |
| `oracle_gen.py … anchor-demo` | [1] PASS · [2] FAIL (perturbed `l1lint/engine.py`) · [3] FAIL (stale harness → guard tripped) | 0 |
| `oracle_gen.py version-lock manifest-live.json` | LOCKED | 0 |
| `oracle_gen.py version-lock manifest-sealed.json` | LOCKED | 0 |
| `oracle_lint.py … manifest-live.json --enforce` | 9 PASS / 0 FAIL / 0 SKIP — PASS | 0 |
| `oracle_lint.py … manifest-sealed.json --enforce` | 9 PASS / 0 FAIL / 0 SKIP — PASS | 0 |
| `oracle_gen.py … gen --source live` | byte-identical to staged `manifest-live.json` (`e5993c1d…`) | 0 |
| `oracle_gen.py … gen --source sealed` | byte-identical to staged `manifest-sealed.json` (`6049beb1…`) | 0 |
| `oracle_gen.py --boxlive <staged snapshot> repin-dryrun` | NO DRIFT; guard not tripped (dated snapshot, see §2) | 0 |
| `oracle_gen.py --boxlive <staged snapshot> gen --source boxlive` | `manifest-boxlive-2026-09-06.json`, `54a54553…` | 0 |
| `oracle_lint.py … manifest-boxlive-2026-09-06.json` (shadow) | 8 PASS / 0 FAIL / 1 SKIP — L9 `unrecognised corpus_source.kind='boxlive'` | 0 |
| `oracle_lint.py … manifest-boxlive-2026-09-06.json --enforce` | REFUSED — incomplete coverage (the L9 gap, §7 item 3) | 1 |
| negative control: bare defaults, no flags | `FileNotFoundError` on the parent-relative inventory path — SEEDS-RUNBOOK §2 defect reproduced | 1 |

Environment: Python 3.11.15, PyYAML 6.0.1; run at 2026-09-06T20:49:34Z.

## 7 · Anomalies, gaps and open facts — recorded, not resolved

1. **Engine folders invisible to this identity.** `396978339615` and `403356419210` return *Item not found* to
   `183820787`; a name search finds only archive/exchange copies of the engine files, none under `390802629329`.
   By design (JR 2026-09-06). Consequence: no fresh corpus, no write-time re-pin from this seat — §5.
2. **Connector rename** `rules_as_data.yaml` → `rules_as_data.txt` (bytes identical). Restore the name on apply.
3. **`oracle_lint.py` L9 has no `boxlive` adapter.** `c_determinism` maps only `inventory`→live and `setpin`→sealed,
   so a manifest generated from a live read (`corpus_source.kind = boxlive`) can never pass `--enforce` as the linter
   stands — it SKIPs L9 and `--enforce` refuses on coverage. That is exactly the manifest §5 produces at write time.
   A three-line adapter was **tested on a scratch copy only** and is staged as `PROPOSED-PATCH-oracle_lint-boxlive-L9.txt`
   (`patch -p0` applies it cleanly to the staged file; result sha1 `69b11a31d42cf248567d100786e9d4d64d7b5932`):
   with it, the boxlive manifest passes `--enforce` 9/0/0, the live and sealed manifests still pass 9/0/0, and a
   perturbed corpus makes L9 FAIL. **It is NOT applied** — per SEEDS-RUNBOOK §2 a generator edit must be version-bumped
   (`rules_version` / S5) and re-validated, never slipped in. Options for the promotion step: (a) commit the set as
   staged and treat the write-time boxlive manifest as shadow-linted (8 PASS + L9 SKIP) alongside `manifest-live.json`,
   which passes `--enforce` and carries the same pins when the dry run reports NO DRIFT; or (b) adopt the patch with a
   bump and re-validate, then `--enforce` the write-time manifest. **Recommendation: (a) for this commit, (b) as the
   next generator revision.** JR's call.
4. **OPEN-DECISIONS §5 stale value confirmed** by prefix hash (§1). Use `b765d4ee…` / 77,165 for any path-or-hash job.
5. **Two Teams-side principals in the staged record.** The staged snapshot's `_note` says it was read by
   `mail@rodwell.biz` (10546707); HANDOFF says the folder was staged by CCG `52284892504`. Consistent with HANDOFF
   §5.1's open principal question; recorded, not ruled.
6. **Appendix C parent unverifiable here.** The slice cites parent sha1 `59965a22c38bdfbba5795773f5739a06b8d0ffdf`;
   the parent is not in IN. The slice's inline defect warning was honoured (§1).
7. **Instrument facts.** All Box access was the MCP connector under `183820787`: reads by direct folder/file id, writes
   create-only (version 1). Read-back used the **same** connector — GATE-V's different-instrument read-back applies
   to the org-tier step, not to this staging. No 401/403 occurred. No token could be re-minted from this seat.
8. **Search-visible engine copies were not used.** Box search returns engine-file copies in `z Archive` exchange folders
   with matching sha1s; the corpus is defined by folder id, so none was consulted.
9. **Versioned backup outside Box.** The OUT set (with `rules_as_data.yaml` under its proper name) was also committed to
   branch `claude/oracle-gen-a9-delivery-i5xmkb` of the `rodwel-cmyk/temp` GitHub repository — a recoverable copy, not
   a governed substrate; commit hash in the session report.

## 8 · Not done here, by scope

- Live corpus rebuild and write-time re-pin — the promotion step's (§5). · S9 org-tier commit — not attempted.
- No section beyond `engine_set` and `harness` (HANDOFF §3 item 4: boundaries must be ruled, not invented).
- No staged file modified; no write outside `415603610278`; no corpus bytes loaded.

*END — staged for the Teams/CCG promotion. Authority: NONE.*
