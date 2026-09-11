# BL-1546 — An @handle in a bio is not an address: 66 of 1,870 removed

He was right, and he named the mechanism before I found it. **Of the 1,870 addresses on the
workbook's `Emails` sheet, 66 (3.53%, 95% Wilson 2.78–4.47) are not addresses at all — they are
references to somebody's other social account. 1,804 survive.** Every one of the 66 was
hand-checked against the bio it came from; none was removed on a count alone. Of the examples he
gave, the "new account @…" one and the "brothers@…" one are both in the workbook and both are now
caught; the "main @…" one is **not** in this workbook, but its shape is the single most common
failure here, **accounting for 60 of the 66**. The two he looked at and approved are likewise not
in this workbook — but both are pinned as fixtures that the test fails on if they ever stop
surviving, so the rule can never quietly start eating them. The rebuilt workbook is at
`%USERPROFILE%\OneDrive\Desktop\clipper_emails_ALL.xlsx` with a new **Removed** sheet carrying the
bio and the exact reason for all 66, so he can argue with every one.

---

## The mechanism, named

`word` + `@` + `word.tld` matches a social handle exactly as well as it matches an address, and **the domain
suffix cannot separate them** — `.cc`, `.ae`, `.tv`, `.me`, `.io` and `.co` are all real TLDs and
TikTok handles legitimately contain dots.

What actually fuses them is one line in `bio_parser._deobfuscate_email`:

```python
s = re.sub(r"\s*@\s*", "@", s)      # n @ d  ->  n@d
```

That rule exists to rescue a person who writes their address as `name @ gmail.com`. It also turns
`main @somehandle.cc` into a single `main` + `@` + `somehandle.cc` token. **So on a mis-extraction the lead-in word becomes
the local part** — which makes the census far sharper than scanning prose, because the evidence is
sitting in the address itself.

## The lead-in census, derived rather than guessed

Every address was sorted into a **match tier** by replaying the extractor's own rewrite rules one
at a time, rather than by matching a list of phrases I invented:

| tier | meaning | rows | share |
|---|---|---:|---:|
| `exact` | a character-for-character substring of the bio | 1,806 | 96.6% |
| `space_at` | matches only after whitespace around `@` is collapsed | 59 | 3.2% |
| `obfuscated` | needed `(at)`/`(dot)`/` at `/` dot ` rewriting | 5 | 0.3% |
| `unmatched` | not reproducible from its bio at all | 0 | 0.0% |

The local parts of the `space_at` tier **are** the lead-in words, and they came out of the data in
this order: `account` (7), `and` (4), `acc` (4), `alt` (3), `at` (2), `edits` (2), `main` (2), `ig`
(2), then a long tail of one each — `bro`, `instagram`, `insta`, `follows`, `dm`, `shop`, `on`,
`of`, `as`, `by`, `duo`, `promo`, `mobile`, `teacher`, `maker`, `lost`, `unknown`. For contrast the
top local parts in the `exact` tier are `contact`, `hello`, `info`, `promos`, `team`, `bookings` —
the vocabulary of somebody publishing a real inbox.

## The discriminator, and it is the spacing

The census produced a cleaner rule than a word list. Two bios, same shape after de-obfuscation:

```
"backup acc @<handle>.cc"        space BEFORE the '@', none AFTER   -> handle syntax
"Easy Booking @ <domain>.ca"     space on BOTH sides                -> an obfuscated address
```

Measured on the 59 `space_at` rows: **57 have the `@` glued to the following token, 2 do not.**
Both of the two are real businesses with working mail exchangers — a cleaning company and a
jeweller — and both are **kept**. The rule ships as four signatures:

| signature | rows | what it means |
|---|---:|---|
| `handle_syntax_at_is_glued` | 60 | space before the `@`, none after |
| `chained_at` | 7 | the local part is itself preceded by `@`, **and** the domain has no MX |
| `lead_in_word_no_mx` | 3 | a glued lead-in word **and** no mail exchanger |
| `prose_at_or_dot` | 2 | ordinary English rewritten into an address |
| **total (rows, not reasons)** | **66** | |

## Both directions, which is the point

A rule that catches 40 rows of which 8 are real is a bad rule. So for every signature: what does it
catch, and how much of the catch is genuine?

- **12 of the 66 removed rows have a working mail exchanger.** All twelve are listed individually
  in the `Removed` sheet and all twelve were hand-read: each is a bio naming somebody's other
  account on a live ccTLD. None is a mailbox.
- **The other direction is the one that nearly bit.** Three addresses that the rule does **not**
  touch have no MX route — and all three are genuine business inboxes with a 📩 in front of them.
  **MX as a lone executioner would have destroyed 3 real addresses out of 9.** It never fires alone
  here; it only corroborates.
- The second, unrelated bug — ` at ` and sentence-boundary `. ` de-obfuscation — caught 5 rows, all
  5 of which are ordinary English sentences. One is a creator writing that they hope to get *very
  good at \<something\>. My dream is…*, which the extractor turned into an address.

## The third signal does not separate, and I am saying so

The brief asked whether a string also appearing as a known account name is evidence. Checked
against the 73,008 handles this round's own bios carry: in the `exact` tier **27 rows** have a
domain whose first label is a known handle, and on reading them **essentially all are genuine** —
real businesses, a talent agency, a martial-arts coach, several creators who simply own the domain
that matches their handle. **A creator owning `<theirname>.com` is the normal case, not a
suspicious one.** The signal is not usable as a drop rule and is not shipped as one.

## What was never scored — and the prior was wrong

BL-1541's rows predate `address_check.py` entirely. The brief's instruction was to start there on
the grounds that they were the most likely place for bad rows. **They were not.**

| round | rows | removed | rate | 95% Wilson |
|---|---:|---:|---:|---|
| BL-1541 | 102 | 2 | 1.96% | 0.54 – 6.87% |
| BL-1542 | 1,001 | 49 | 4.90% | 3.72 – 6.41% |
| BL-1544 | 767 | 15 | 1.96% | 1.19 – 3.20% |
| **all** | **1,870** | **66** | **3.53%** | 2.78 – 4.47% |

BL-1541's interval is wide at n=102 and **overlaps BL-1542's, so it cannot be called significantly
cleaner** — but it is certainly not disproportionately dirty. BL-1542 versus BL-1544 **do not
overlap**, so that separation is real: the round that swept 512 tags picked up handle references at
2.5x the rate of the deep re-walk.

One correction to the brief's own framing: **BL-1541 contributed 102 addresses, not 103.** It found
103 address *mentions*, two of which are the same address published in two different bios.

## The creator question — flagged, never deleted

His first formulation ("if it's not Gmail, I don't want it") would delete addresses he himself kept
— he approved two custom domains in the same message. **The custom domain is not the tell; the
words are.** So this ships as a column and not a filter:

| flag | rows | share of 1,804 survivors |
|---|---:|---:|
| likely creator / label / agency | 106 | 5.67% (4.71 – 6.81) |
| role inbox (`info@`, `booking@`, …) | 34 | 1.82% (1.30 – 2.53) |
| very short local part | 13 | 0.70% (0.41 – 1.19) |

Role inboxes and short local parts are **kept**, as they were before — a merge once refused 69 of
72 shared-address rows because they are inboxes two people genuinely share, and that refusal was
right. He can filter a column; he cannot un-delete a row.

---

## What I got wrong

1. **My own rule destroyed 11 genuine addresses, and only the both-directions measurement caught
   it.** The first version of `chained_at` rejected any address whose local part was preceded by
   `@`. It matched 20 rows — and **11 were real Gmail addresses** belonging to people who write
   a decorative leading `@` immediately before their real address (`📧` `@` `name` `@` `gmail` `.com`). Every one of the 11 had a working mail
   exchanger and the one true handle chain did not, so the signature now requires a dead domain
   before it may speak. This is exactly the failure the brief warned about, committed by the very
   round sent to prevent it, and it survived only because I listed the catch instead of counting
   it.
2. **I wrote the committed test with eleven real addresses in it.** The fixtures were lifted
   straight from the corpus — real Gmail addresses, a real cleaning company, a real jeweller, a
   real talent agency. They would have entered a tracked file. Every fixture is now synthetic
   except the three he named himself, all three of which are absent from both stores; the test
   re-proves that at run time against the lead store rather than trusting a comment.
3. **I believed the brief's prior about BL-1541 before measuring it.** I started there as
   instructed, which was right, but I expected to find the worst rows and found the opposite.
4. **My first file-discovery script hid the largest source file from itself** — it filtered
   candidates by extension and the run checkpoints end in `.done`.

## Counts, plainly

```
in                    1,870
removed                  66   (3.53%)
survive               1,804   (96.47%)   <- re-derived a second way, agrees exactly

removed, by reason (rows may carry more than one)
  handle syntax, '@' glued        60
  chained '@' + no MX              7
  lead-in word + no MX             3
  English prose rewritten          2
```

## Where the file is

```
%USERPROFILE%\OneDrive\Desktop\clipper_emails_ALL.xlsx
```

Three sheets: **Emails** (1,804 survivors, with the role / short-local / likely-creator flag
columns and the reason each flag fired), **Removed** (all 66, each with the bio it came from, the
rule, a plain-English reason and the MX status), and **No email** (22,830, unchanged). Row counts
are parser-counted, never line-counted — bios contain newlines. The workbook is his and is not
committed.

## The suite — what I can and cannot quote

**I have no full-suite verdict line, so I am quoting none.** The 475-suite run was started four
times in this session and reached a verdict none of them: three were **killed by system memory
pressure** (a concurrent round was harvesting at the same time) and the fourth stopped after about
30 suites without printing a summary. Subtracting or estimating a total from a partial log is
exactly the mistake this project has already published once, so there is no number here.

What I did run, quoted verbatim from each runner:

```
tests/test_bl1542_address_check.py        Ran 19 tests   OK
tests/test_bl1546_handle_not_address.py   Ran 12 tests   OK
tests/test_bl1544_dedup_guard.py          Ran 18 tests   OK
```

That is the **blast radius**: `address_check.py` is the only shipping file this round changes, and
grep across `tests/` finds exactly two suites that reference it, both above. The one red observed
in the partial logs — `tests/test_atomic_io.py`, an unguarded `os.replace` at `proxy_pool.py:290` —
is **pre-existing and not this round's**: that file is untouched here, the line is present at HEAD,
and it was last modified by BL-1514 on 2026-09-06. **A full run still needs to happen on a quieter
machine, and until it does this round's green is a subset green.**

## Safety

Read-only on the funnel: `tiktok_finder.py`, `meme_finder.py` and every seen store are untouched
and nothing latched. **Zero vendor calls, $0.00 spent** — MX lookups are DNS and free. MX results
were written to this round's own scratch table rather than `suppress_mx.json`, which a concurrent
round holds. His workbook was backed up before it was rewritten, zero C0 control bytes were
asserted before the write rather than after, and the rebuilt file was read back and re-counted
from disk.
