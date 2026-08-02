# STEP3-PACKAGE-AUDIT — independent audit of the fix-run step-3 review package — v1.1 2026-08-01

**Authority: NONE.** An audit record. It changes nothing, clears nothing, and authorises nothing.
Output returns to the Level 1 project for review; nothing acts on it until then.

**Auditing seat.** Claude Code remote session (isolated Linux container), git branch
`claude/step3-audit-step4-governing-u98v48` on `rodwel-cmyk/temp`. Box access via MCP as user id
`183820787`, display name `Uploading_MRI`, login `rodwel@me.com` — per
`CODECLI-JOB-adopt-transport-and-retention-rules-2026-07-30.md` this is **the Max seat's Box
account**, the "third actor" of the 2026-07-30 exchange incident. It is NOT the Teams Code-CLI
seat and NOT the Cowork chat seat.

**Model.** `claude-fable-5` (Anthropic Claude 5 family; Mythos-class tier, positioned above
Opus-class). **Processing Model Standard: the Opus-class-or-higher requirement is SATISFIED.**

**Writes made by this session: ZERO to Box, ZERO to ClickUp** (no ClickUp tooling was even
attached). Every Box call was a read (list, search, metadata, content). The only writes are this
file and its companion draft, committed to the git branch above and emitted as hash-verifiable
text back to the Level 1 session.

---

## 0. DISCLOSURE FIRST — THE TASKING BRIEF WAS NOT READABLE FROM THIS SEAT

The session was instructed to read
`/Users/jonathanrodwell/Claude/Projects/Level 1 - Dev/MAX-SESSION-BRIEF-audit-and-step4-governing-doc-2026-08-01.md`
in full and follow it. **That file could not be read from this environment:** the path is on JR's
Mac; the remote container's filesystem does not contain it; the git repo does not contain it; and
a Box keyword search for `MAX-SESSION-BRIEF` returned zero results from this seat's visibility.

Everything this audit knows about the tasking therefore comes from the task message's own
restatement (marked `U-RELAY` below): two tasks in order (this audit, then the step-4 governing
draft); AUTHORITY NONE — read and draft only, no Box or ClickUp writes of any kind; a parallel
Teams Code job writing to both today; the Opus-class-or-higher confirmation; and the rule that no
hash, size, version or content is stated as fact unless read this session. **A follow-up relay
later the same session supplied three further brief requirements absent from the first relay**
[U-RELAY]: emission of both deliverables as hash-verifiable text (a git branch this project
cannot reach is a document nobody downstream can read); the verdict in the fixed form
SEND / SEND WITH NAMED CHANGES / DO NOT SEND (§9); and two named findings, ruled on here as F8
and F9. **If the brief carries requirements beyond these two relays, this session has not seen
them and cannot claim compliance with them.**

---

## 1. PROVENANCE KEYS — every value in this audit carries one

```
V-BOXMETA   Verified this session from Box server-side metadata (sha1 / size / timestamps
            returned by the Box API for the object itself).
V-LOCAL     Verified this session by local computation on the git clone: shasum -a 1, wc -c,
            or actually executing the artefact.
V-READ      Read this session, in full, from the named Box file's text representation. NOTE:
            the MCP content pipe is text-based (the repo README records this; the 75,066 B
            brief arrived as 74,833 characters), so V-READ vouches for CONTENT, while byte
            identity rests on V-BOXMETA.
U-DOC       Carried from a named document that was read this session. The DOCUMENT's claim,
            not this session's verification. Repeated here as an unverified claim.
U-RELAY     Carried from the task message / mid-turn user message. Not independently
            verifiable from this seat. Repeated here as an unverified claim.
```

---

## 2. WHAT THE STEP-3 PACKAGE IS, AND WHERE THIS AUDIT FOUND IT

The durable step-3 package is the three v2.0 instruments for the fresh-session Gemini review of
the fix diff. Their recorded home is `New outbox`, Box folder `404675989749`
(AI - Claude - Teams / Max-Drafting-Exchange) [U-DOC: FIX-RUN-REPORT §6; STEP1-LAUNCH OVERRIDE 1;
transport JOB "FINAL STATE" — three independent documents, agreeing]. This seat audited the
**copies staged into `New Inbox` (Box folder `404921689756`)** on 2026-07-31, plus the local git
mirror, because those are what this seat can see (section 6 explains the visibility boundary).

### The folder, enumerated by this session [V-BOXMETA]

`New Inbox` (404921689756) holds **12 files**. All created by `mail@rodwell.biz` (Jonathan
Rodwell). Eleven created 2026-07-31 10:04–10:24 UTC; one placed 2026-08-01 20:47:43 UTC.

```
FILE                                                          BOX ID          BYTES    SHA1 (server-side)                          CREATED (UTC)
03-GEMINI-REVIEW-PROMPT-fixrun-step3-v2.0.txt                 2380174300794   21,724   d3cf5a3ab72c43b9e92ef5f8706637485f1afc3d    2026-07-31 10:05:14
03b-PASTE-integrity-declaration-adapted-v1.0.txt              2380180813975    5,934   097d42fbafe064898c7b24c8807ea3f043f12aea    2026-07-31 10:05:27
CODECLI-FIXRUN-BRIEF-v2.1-2026-07-28.md                       2383211778276   75,066   7a59e1b21165e8901e9811cd7e4a3cccf2f27cdc    2026-08-01 20:47:43
CODECLI-FIXRUN-STEP1-LAUNCH-2026-07-30.md                     2380212453161   10,234   e454d532d2b6edb74ab5429b942978dd0009cadc    2026-07-31 10:22:09
CODECLI-JOB-adopt-transport-and-retention-rules-2026-07-30.md 2380233051644   14,838   58168130ab3e9963a68428513f9a2ef34464f3c8    2026-07-31 10:23:18
CODECLI-JOB-survey-durability-and-stale-clearance-2026-07-30  2380215403035   17,772   d65b8299930adc7cd35060cefaf48bf0595b75f5    2026-07-31 10:22:59
CODECLI-STALE-LOCAL-SWEEP-BRIEF-2026-07-30.md                 2380232865158    9,661   2e88995025b70c56f8d53ed9807864573c73f926    2026-07-31 10:23:48
Cowork-State-Cache.md                                         2380192278530   68,150   f66a77a356fcbdb9e19a1cf4e6948060e7361919    2026-07-31 10:04:21
DECISIONS-RULINGS-2026-07-17.md                               2380198895449   10,323   c6fea5756e9c53b94a8911dabedb290be8b56537    2026-07-31 10:04:38
FIX-RUN-REPORT-v1.0-2026-07-30.md                             2380233525303   38,340   fbbd5baef401d49797e5cab367792dd5268176cb    2026-07-31 10:24:16
RUN-CARD-fixrun-step3-review-v2.0.md                          2380182961206    6,302   5ed8de23b62d3c528aef07f2f21fed7cdb3137ae    2026-07-31 10:05:20
STALE-LOCAL-SWEEP-REPORT-v1.0-2026-07-30.md                   2380198643136   67,706   9a2d310b8d0689c2b4d21b9bc4d2bdee4b75d070    2026-07-31 10:04:30
```

Read in full this session [V-READ]: the RUN-CARD, 03 prompt, 03b declaration, FIX-RUN-REPORT,
FIXRUN-BRIEF v2.1, STEP1-LAUNCH, transport/retention JOB, DECISIONS-RULINGS, and the load-bearing
sections of Cowork-State-Cache (§§1–2, 0a–0d4, 0c0–0c3, §§5–7). Not read (out of audit scope, in
folder): the two stale-sweep files and the survey-durability job.
`CONSOLE-DRAFTING-POLICY-DECISION-RECORD-v0.3-2026-07-18.md` (2356338165045) sits at this seat's
Box root, outside the folder; not load-bearing here.

---

## 3. IDENTITY VERIFICATION — the three instruments match every recorded identity

The three package copies' server-side sha1s and sizes [V-BOXMETA] were compared against the
identities recorded for the `New outbox` originals in three documents read this session
[V-READ of the documents; the recorded values themselves are those documents' claims]:

```
INSTRUMENT      NEW-INBOX COPY [V-BOXMETA]                      RECORDED ORIGINAL (id per U-DOC)   AGREE?
03 prompt       d3cf5a3a… / 21,724 B                            2378613515653, same sha1/size      YES ×3 records
RUN-CARD        5ed8de23… /  6,302 B                            2378612293434, same sha1/size      YES ×3 records
03b declaration 097d42fb… /  5,934 B                            2378650309961, same sha1/size      YES ×3 records
```

The three records are FIX-RUN-REPORT §6, STEP1-LAUNCH OVERRIDE 1, and the transport JOB's "FINAL
STATE" paragraph — the last of which adds that the originals were verified three ways on
2026-07-30 (producer's declared value, Box's computed value, independent read-back) after the
one-byte-corrupt 03b was deleted and replaced by hand [U-DOC].

**Conclusion: the copies this seat can see are byte-identical (by Box's own hash) to the
recorded identities of the durable package.** The originals at their recorded IDs are not
resolvable from this seat (section 6) — equality of copy-to-original therefore rests on Box's
server-side hashing plus three agreeing documents, not on a this-session read of the originals.

### The governing brief's copy, placed mid-session

`CODECLI-FIXRUN-BRIEF-v2.1-2026-07-28.md` (2383211778276): **75,066 B, sha1 `7a59e1b2…`,
version 1, created 2026-08-01T20:47:43Z, content-created 2026-07-29T15:18:24Z** [V-BOXMETA].
That sha1 and size match the identity pinned by three independent records read this session:
FIX-RUN-REPORT §2 ("the brief itself … resolved, agreed (75,066 B, 1,148 lines)"), STEP1-LAUNCH
("75,066 bytes, 1,148 lines, sha1 7a59e1b2… CLEAR-TO-APPLY after four independent passes"), and
state-cache §5 [all U-DOC as to what they pin; the match to the live object is V-BOXMETA].
The full text was read this session [V-READ], 1,148 lines.

---

## 4. LOCAL VERIFICATION — the git mirror and the gate, re-run by this session

All [V-LOCAL], computed/executed 2026-08-01 in this container on git HEAD `340258b`:

```
linter-cluster/layer1_lint.py       a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7   107,222 B   matches README claim
linter-cluster/test_layer1_lint.py  31d74400b7a9f9064a49f0ea52ff8df3f485e39a    54,983 B   matches README claim
linter-cluster/manifest.yaml        0397bfd11cfe8023aa7eb4808681d0bd598ddad3     3,748 B   matches README claim
linter-cluster/baseline.md          dd5da45a1f93963c6f1c381e9dcd292f6f79333d    48,992 B   matches README claim
diffs/item1.diff … item7.diff       all seven present
SELFTEST (re-run this session):     python3 linter-cluster/layer1_lint.py --selftest
                                    -> "SELF-TEST RESULT: 89/89 fixtures correct (exact
                                    failing-set match); baseline clean -> PASS", exit 0
```

### Three convergences this produces

1. **The frozen-oracle ratification value now has a second independent leg.** FIX-RUN-REPORT §7
   asks JR to ratify `a87ce5101fe82ff10af67e4dc0b24c9771c0e6f7` / 107,222 B as the frozen
   oracle's pin, computed by the Teams seat from Box `2367835811909` on 2026-07-30 [U-DOC]. This
   session independently computed **the same sha1 and byte count** from the git mirror's
   `layer1_lint.py` [V-LOCAL]. Two computations, two routes (Box bytes vs git bytes), one value.
2. **`manifest.yaml` and `baseline.md` local bytes equal the staged/governed values** recorded in
   brief §4 and state-cache §5 (`0397bfd1…`/3,748 and `dd5da45a…`/48,992) [V-LOCAL vs U-DOC].
3. **The 89/89 gate claim of the git mirror README reproduces exactly** on this host [V-LOCAL].
   (Note precisely: this is the monolith's own `--selftest`. It is NOT a re-run of the fix run's
   harness gate, whose 89/89 [U-DOC] ran on the executor's host against the fixed harness.)

### Absence checks, with positive controls (discipline: no absence claim without one)

Positive controls fired: `grep -c 'selftest'` = 15, `grep -c 'ENGINE'` = 2 on the same file with
the same method [V-LOCAL]. Against that working method: the git-mirror corpus contains zero
occurrences of `l1lint`, `__init__.py`, `ENGINE_SET_RELPATHS`, or `Per-side identity for the run
header` — consistent with the mirror being the pre-refactor linter-cluster lineage (2026-07-24/25),
which predates the shim+package split. Consequences: (a) the §4 underscore transport control is
**N/A on this corpus** — there is no package filename in it to corrupt — and is NOT claimed as
passed; (b) D1(b)'s expectation that its two distinctive strings are absent from older-lineage
harnesses holds for this (even older) harness [V-LOCAL], which is weak corroboration, not proof
about the actual staged pre-fix harness.

---

## 5. CROSS-CONSISTENCY OF THE INSTRUMENTS — the D4-style sweep, done with a shell

Checked this session across the three instruments [V-READ] and the run-time values in
FIX-RUN-REPORT §5 [U-DOC]:

1. **Slot inventory.** The 03 prompt's §2 carries exactly EIGHT `<<<FILL…>>>` run-time slots
   (3 fix-diff, 2 fixed-harness, 3 demo-evidence) — matching the "eight run-time slots" the
   report and launch prompt describe. The staged copies are the UNFILLED masters, which is
   correct for a durable package; the RUN-CARD step 1 fills them at run time. AGREE.
2. **Slot ↔ deliverable mapping is complete.** Every slot has a value waiting in FIX-RUN-REPORT
   §5: fix diff `AUTHORITATIVE-DIFF-harness-3574c2d1-to-63804b9c-2026-07-30.diff`
   `8f648d73…`/16,600 B; fixed harness `63804b9c…`/104,070 B; rationale
   `DEMO-ASSERTION-RATIONALE-v1.0-2026-07-30.md` `422db33c…`/18,755 B; driver UNCHANGED
   `2651b859…`/18,586 B; driver-diff slot satisfied by the UNCHANGED statement +
   `DEMO-DRIVER-DIFF-STATEMENT-v1.0-2026-07-30.md` `e5fee309…`/5,855 B [all U-DOC — these
   artefacts are local to the executor's host and NOT visible from this seat]. The two driver
   entries agree (both UNCHANGED), satisfying the card's step 4 and the declaration's D4(5).
   AGREE, contingent on the artefacts. **See F9 for the seam in how the UNCHANGED statement
   physically travels.**
3. **Known-value agreement across instruments.** Pre-fix harness `3574c2d1…`/92,385 B: identical
   in RUN-CARD "FILES" and steps 2, 03 §2 KNOWN NOW, and 03 §3 names table. Template identity
   `22b0422e…`/4,094 B / header v1.4 (2026-07-27) / Box `2368457077961` / Box version counter 5:
   identical across RUN-CARD, 03 §2, 03b D2(b)'s duality note, and state-cache §5. Frozen oracle
   `a87ce510…`/107,222 B / Box `2367835811909`: identical across 03 §2 and FIX-RUN-REPORT — and
   confirmed against local bytes (section 4). Demo driver prefix `2651b859`/18,586 B: identical
   across 03 §2, brief §8, report §5 (see F8). AGREE throughout; no value collision found.
4. **The declaration's no-expected-values design holds.** 03b repeats none of §2's identities
   (checked by reading both); expected values live only in the 03 file's §2, as both documents
   claim. AGREE.
5. **The fresh-session inversion is carried coherently.** Brief §12.1's original route (existing
   gate (ii) session; correction 3 "send ONLY the fix diff") is dead per STEP1-LAUNCH OVERRIDEs
   1–2 and state-cache entry 0/0a; the RUN-CARD is a fresh-session Run Card B design; 03 §1 X4
   supplies the baseline as message 3; 03 §4 C3 states the inversion explicitly; the report §6
   quotes original and inverted forms side by side. AGREE — the package implements the inversion;
   no instrument still carries the dead route.
6. **RUN-CARD P3 (only live instruments in the working folder).** The audited folder contains no
   v1.0 prompt/card and no `gemini-review-template-CODE-CHANGE.md` [V-BOXMETA enumeration]. The
   stale 3,029-byte template (`87e6876a…`, header v1, 2026-07-25) recorded as sitting in "the
   project ROOT" [U-DOC state-cache] is not visible from this seat — its removal CANNOT be
   confirmed from here and remains an operator precondition at run time.
7. **F1 / fifth-correction closure.** C5 in the 03 prompt requires an F1 ruling; the report's
   measurement CONFIRMED F1 (17/17 byte-identical pre/post) and generated no fifth correction,
   explicitly recorded [U-DOC]. The prompt's four binding corrections C1–C4 match the four the
   brief mandates, with C3 in its inverted form. AGREE.

---

## 6. THE VISIBILITY BOUNDARY — what this seat could not check, and why (the D6 section)

**Every by-ID Box lookup outside `New Inbox` failed "Item not found" — 9 of 9:** GATE-V
`2289594143154`, Scope Registry `2327535678598`, SETPIN `2373446865036`, CODE-CHANGE template
`2368457077961`, outbox originals `2378613515653`/`2378612293434`/`2378650309961`, governed
harness `2296699168749`, frozen oracle `2367835811909` [all attempted this session].

**Classification under the §0 table, honestly: UNDECIDED from this seat — with a strong
mundane explanation.** Box returns the same "Item not found" for a nonexistent item and for an
item the caller cannot see. This seat is the Max Box account (`rodwel@me.com`), whose visible
world is essentially the shared `New Inbox` plus a near-empty root (owned space ~37 KB). Two of
the nine unresolvable IDs are files **this very account created** on 2026-07-30 [U-DOC transport
JOB], so the dominant explanation is that collaboration on the exchange folder was withdrawn
after the exchange completed (or the items moved) — **not** that nine governed objects vanished.
Per JR's 2026-07-28 ruling this is reported as a classification, and this read-only session
STOPS at reporting: **no lockdown is declared and none is warranted on this evidence.** The
practical consequence stands regardless: **step 3 cannot be assembled from this seat.** The
operator must hold main-account visibility (the Teams Code-CLI seat or JR), and the RUN-CARD's
step-2 local `shasum` checks then cover the identity risk this seat could not.

**Also not checkable from this seat:** the fix run's eight deliverables (local to the executor's
host at `~/l1-fixrun-2026-07-30/` and `~/Claude/Projects/Level 1 - Dev/` [U-DOC]); the
`New outbox` originals themselves; the live governed-substrate state (whether the parallel Teams
job has already begun step 4 today); every sha1 comparison involving those objects; and the
MAX-SESSION-BRIEF (section 0).

---

## 7. VERIFICATION OF THE MID-SESSION MESSAGE'S CLAIMS — checked, not echoed

The mid-turn message asserted five things about the folder. Outcome of this session's own checks:

```
CLAIM                                                        THIS SESSION FOUND
12 files, not 11                                             12 files. VERIFIED [V-BOXMETA].
2383211778276 is 75,066 B                                    75,066 B. VERIFIED [V-BOXMETA].
sha1 7a59e1b21165e8901e9811cd7e4a3cccf2f27cdc                Same. VERIFIED [V-BOXMETA].
placed 20:47 on 2026-08-01                                   createdAt 2026-08-01T20:47:43Z. VERIFIED [V-BOXMETA].
placed by server-side Box copy                               CONSISTENT, NOT PROVEN: version 1, created-at today,
                                                             content-created 2026-07-29 — copy-like, but metadata
                                                             cannot distinguish server-side copy from re-upload.
placed after the MAX-SESSION-BRIEF was written               NOT VERIFIABLE — that brief was never readable here.
three near-identical decoys elsewhere in Box, two within     NOT TESTABLE FROM THIS SEAT. A name search returned
4 KB; 75,066 B is the discriminator                          exactly ONE file named CODECLI-FIXRUN-BRIEF-* in this
                                                             seat's entire visibility. Zero decoys VISIBLE ≠ zero
                                                             decoys EXISTING: this seat cannot see the main account.
                                                             [U-RELAY, unverified]
```

Note on the discriminator: byte size is a weaker discriminator than the sha1. The placed copy
matches the pinned sha1 `7a59e1b2…` recorded by three pre-existing documents — that, not the
size, is the load-bearing identity check, and it passes [V-BOXMETA vs U-DOC].

---

## 8. FINDINGS

**F1 (MEDIUM, blocker-class for step 3, expected).** The step-3 feed cannot be assembled from
the audited folder alone, and not at all from this seat. Missing from the folder by design
(sourced "from the fix run" / "from masters/"): the pre-fix harness, the fix diff, the rationale
file, the demo outputs, the driver-diff statement, `04-GEMINI-SYSTEM-INSTRUCTIONS.txt`, and the
4,094-byte CODE-CHANGE template. All exist per three agreeing documents [U-DOC], none is
verifiable from this seat (section 6). ACTION: the step-3 operator confirms reachability of all
seven before opening the Gemini session; the RUN-CARD's own step 2 then hash-gates them.

**F2 (LOW, hygiene).** Version-label duality on the declaration: filename says `…adapted-v1.0.txt`,
internal header says "v2.0 (2026-07-30)", and the RUN-CARD itself uses both labels (P3: "the v2.0
declaration"; FILES list: the v1.0 filename) [V-READ]. This is the exact divergence-point pattern
D2(b) warns about on the template ("v1.4" vs Box counter "v5"). No identity risk while the sha1
`097d42fb…` is the reference — but a future reissue could mispair labels. ACTION: reference
step-3 instruments by sha1 in the step-4 documents (house rule: "name the hash, not just the
path"); consider renaming at the next legitimate reissue, not before.

**F3 (LOW, known/self-disclosed — confirmed still present).** The brief v2.1's READING COST
section still says 69,899 B against its actual 75,066 B [V-READ vs V-BOXMETA]; already recorded
as stale by the report (finding 4) and state-cache 0b(i). No action beyond not trusting that
sentence.

**F4 (LOW, observation).** The brief file is named `…v2.1-2026-07-28.md` and its change log says
v2.1 landed "same day" as v2.0 (2026-07-28), but the Box object's content-created stamp is
2026-07-29T15:18:24Z [V-BOXMETA]. Most plausibly the file's on-disk mtime at upload post-dates
its authorship date; not an integrity event; recorded so nobody rediscovers it as one.

**F5 (MEDIUM, context hazard).** The packaged `Cowork-State-Cache.md` copy (f66a77a3…, 68,150 B,
2026-07-31) matches NONE of the three cache states named in the launch prompt and report (v6
0256a571…/30,276; v9 eb26201c…/54,735; local 141d825e…/61,394) [V-BOXMETA vs U-DOC]. It is
plausibly the post-run 2026-07-31 sync — it DOES contain entries 0c0–0c3 and the 0d* corrections
[V-READ] — but its §2 still carries two superseded instructions ("the Gemini pass is step 4 of
5"; "USE THE EXISTING GATE (ii) SESSION") that its own entry 0c/0a and the launch OVERRIDEs
correct. A reader who stops at §2 inherits both dead instructions. ACTION: the step-4 governing
draft names the six-step count and the fresh-session route explicitly and does not delegate
either to the cache.

**F6 (INFO, positive).** The package correctly implements every correction the fix run handed
forward: fresh-session design, supplied-and-labelled baseline (inverted C3), C1/C2/C4 verbatim in
substance, F1 ruling required as H4/C5, instrument-change posture declared, and a D6
"could-not-check" section that forbids hash-verification theatre. The audit found **no internal
contradiction among the three instruments and no value collision across the nine documents
read.** The one-byte 03b corruption incident of 2026-07-30 was already caught, deleted, and
re-placed upstream [U-DOC], and the surviving copy's hash agrees with all records [V-BOXMETA].

**F7 (INFO).** The frozen-oracle full-hash ratification value now carries two independent
computations (section 4). JR's ratification remains outstanding — this audit adds evidence, not
authority.

**F8 (LOW — ruled on relay from the brief; the driver identity is a prefix where exact was
available).** The 03 prompt's §2 declares itself "the SINGLE home of every expected identity in
this run", yet its KNOWN NOW block records the demo driver as "sha1 prefix 2651b859, 18,586
bytes" — and the declaration's D4(3) cross-checks the rationale's stated pre-edit driver hash
against that entry, so a check that could be exact is approximate. RULING: real, LOW, and NOT an
authoring defect — §2's KNOWN NOW block is expressly "(recorded before the fix run)", and at
package-authoring time only the prefix existed in any record [U-DOC state-cache §5 "Still only a
prefix"]. The full value `2651b8598cfb3af87c8ec0d9bbc7c783a1987f9b` / 18,586 B was first
established at the fix run's staging gate [U-DOC report §5; the follow-up relay quotes the same
value — U-RELAY, agreeing; this seat cannot see the driver file itself]. The exposure is bounded
three ways: the run-time driver slot itself demands "UNCHANGED followed by its unchanged full
sha1", so the COMPLETED §2 puts the full 40-hex before the reviewer and D4(5) ties the two
driver entries together; prefix-AND-byte-count is the brief's own two-factor placeholder
discipline (§4: "Both must match; one alone is not sufficient"); and byte-level verification is
the OPERATOR's shell duty (RUN-CARD step 2, against the fix-run report's full values), not the
reviewer's — the reviewer cannot compute hashes at all. RESIDUAL: D4(3) as written compares
against an 8-hex (32-bit) entry where 160 bits were available — a document-consistency check
narrower than it needed to be, sitting downstream of the operator's full-hash gate. TREATED by
named change NC2 (§9), without touching either pinned instrument.

**F9 (MEDIUM — ruled on relay from the brief; the X5 dependency is real, and it has no slot).**
Disapplication X5 halts the review (standing rule 7) unless message 5 physically carries a
driver diff OR "the explicit statement that the driver is UNCHANGED **(with its hash)**". Two
seams found on inspection [V-READ of card and prompt]:
(i) the RUN-CARD's own step 4 prepares a TYPED LINE — "DRIVER UNCHANGED — no driver diff exists
for this run" — which carries NO hash. An assembly following the card literally therefore sends
a statement missing the one attribute X5 parenthesises, inviting a halt on a strict reading (and
a halt costs a full round; the reviewer is REQUIRED to stop rather than proceed).
(ii) the durable with-hash form EXISTS — `DEMO-DRIVER-DIFF-STATEMENT-v1.0-2026-07-30.md`,
`e5fee309314ae767fb77c38df686cf240241ee02`, 5,855 B, created by launch OVERRIDE 3 for exactly
this purpose ("an explicit UNCHANGED statement, WITH its sha1") [U-DOC; the follow-up relay
quotes the same identity — U-RELAY, agreeing] — but NO §2 slot, no RUN-CARD FILES row, and no
send-step names that document, so nothing in the package itself ensures it travels.
RULING: the dependency must be carried EXPLICITLY, and by RELAY CARD rather than by editing the
package. Editing the card or prompt would change pinned identities that three records already
carry (report §6, launch OVERRIDE 1, transport JOB), would reopen the review clock on cleared
instruments, and would re-run the exact text-parameter upload route that corrupted the
declaration once already — all to add one sentence. The house mechanism for corrections to
cleared instruments is the override/relay card (precedent: STEP1-LAUNCH overriding the cleared
brief). A relay note is sufficient ONLY as a durable, hash-recorded artefact handed WITH the
package — a chat-transcript note is not; instructions that live only in transcripts are the
failure class the brief's §0 records a Tier-2 audit catching. IMPLEMENTED as named change NC1
(§9).

---

## 9. VERDICT — in the form the brief requires

**VERDICT: SEND WITH NAMED CHANGES.**

The package as staged — the three pinned instruments plus the RUN-CARD assembly procedure — is
internally consistent, identity-verified as far as this seat can reach, and correctly implements
every correction handed forward from the fix run. **No finding requires editing any pinned
instrument; instrument identities (`d3cf5a3a…`, `5ed8de23…`, `097d42fb…`) are unchanged by all
three named changes.** The changes attach to the SEND — a small step-3 relay card (authority
NONE, ≤2 KB, its own sha1 recorded in the send report), the same mechanism the step-1 launch
prompt used on the cleared brief:

```
NC1  (from F9, MEDIUM)  Message 5's driver element is the eighth deliverable
     DEMO-DRIVER-DIFF-STATEMENT-v1.0-2026-07-30.md (e5fee309…, 5,855 B [U-DOC]), pasted under
     the message-5 heading in the position the RUN-CARD's step 4 gives the typed line, which it
     SUPERSEDES. Fallback if JR prefers the typed line: the line gains the driver's full sha1,
     so X5's "(with its hash)" is satisfied either way. The relay card also confirms, per D5,
     that message 5's items are listed individually.
NC2  (from F8, LOW)     When filling the driver slot, fill the FULL 40-hex
     (2651b8598cfb3af87c8ec0d9bbc7c783a1987f9b — as the slot text already demands), and at
     RUN-CARD step 2 verify the rationale's stated pre-edit driver hash against that full value
     from the fix-run report, closing D4(3)'s prefix-width residual outside the reviewer.
NC3  (from F1)          Before opening the session: confirm reachability of the seven
     externally-sourced inputs, and confirm the stale 3,029-byte template's removal from the
     working folder (RUN-CARD P3) — neither is checkable from this seat.
```

If the named changes cannot accompany the send as a durable artefact, the verdict degrades to
**DO NOT SEND** until they can: the failure they prevent — a rule-7 halt or an
unverifiable-driver round at step 3 — costs a full review round against a reviewer that is
required to stop.

Nothing found here blocks step 3 beyond the above. The gates that DO sit downstream are the ones
the records already name: JR's read of the brief (still NOT CONFIRMED per the report [U-DOC]),
the ratifications, and the ≥64 KB transport ruling — all ahead of step 4, per the companion
`STEP4-GOVERNING-DOC-DRAFT-v0.2-2026-08-01.md` (same branch, same session).

*Change log: v1.0 2026-08-01 — first issue, produced read-only. v1.1 same day — added §9 verdict*
*in the required SEND / SEND WITH NAMED CHANGES / DO NOT SEND form, and findings F8/F9 with*
*rulings; all three requirements arrived by follow-up relay from the (still unreadable) brief.*
*Supersedes v1.0 whole; v1.0 remains at git commit 0a2b0d0. Not adversarially reviewed; returns*
*to Level 1 for review.*
