# CONVENTION.md — how report IDs are allocated, and the check that stops them colliding

**Why this file exists.** IDs here are allocated by reading the highest existing report and adding
one. That is a read-then-write with no lock, so two agents working the same day read the same
ceiling and pick the same number. When the second one pushes, git accepts it as an ordinary
commit — **the path already existed, and the new content simply replaces it.** Nothing fails. No
warning is printed. The first report is gone from `main`, and every citation pointing at that ID
silently starts referring to a different document.

This has happened **three times** and was noticed only once:

| ID | first report (lost from `main`) | second report (kept) | noticed |
|---|---|---|---|
| `BL-649` | "Do already-installed iPhone PWAs get the new launch images? NO." (`321ceef`, 2026-07-24) | "Merge BL-648 to main" (`40ea3df`) | **no — found 5 days later by audit** |
| `BL-675` | "Instagram reels move to /v2/user/clips…" (`4c9b4f0`, 2026-07-29) | "merge BL-673 to main" (`c4b38ce`) | **no — found by audit** |
| `BL-677` | "beat-drop timestamp and mood for Instagram Reels" (`773dfe2`, 2026-07-29) | "Apify is supposed to be dead" (`54e19d6`) | yes |

Nothing was lost permanently — git keeps every version — but the *published* copy vanished, which
is the only copy an automated reader can fetch. That is the whole point of this repository.

---

## The rule

> **A push that would create a path which ALREADY EXISTS on `origin/main` is a COLLISION.
> Stop, take the next free ID, and push that instead. Never fast-forward over it, never
> overwrite, never `--force`.**

An existing path is only a legitimate write when you are **deliberately editing that same
report** — correcting a figure, fixing a citation. If you are publishing a *new* report, the
target path must not exist. Those two cases are easy to tell apart because you know which one
you are doing; the check below enforces the one you declared.

---

## The exact check

Run this immediately before `git push`, after `git fetch`. It costs one round trip.

```bash
# 1. Get the true remote state. NEVER trust a local listing — another agent may have
#    pushed since you cloned, and your working tree will not know.
git fetch origin

# 2. Refuse if the path you are about to create already exists on the remote.
for f in BL-684.md; do                       # <- every NEW report in this push
  if git ls-tree origin/main "reports/$f" --name-only | grep -q .; then
    echo "*** COLLISION: reports/$f already exists on origin/main — NOT pushing ***"
    exit 1
  fi
done

# 3. Only now commit and push.
git add reports/BL-684.md
git commit -m "BL-684: ..."
git push origin main
```

`git ls-tree origin/main <path>` prints the blob line if the path exists on the remote and
prints nothing if it does not, so `grep -q .` is the whole test. It reads the **remote** ref, not
the working tree, which is what makes it correct under concurrency.

### Picking the next ID — read the remote, not the disk

```bash
git fetch origin
git ls-tree origin/main reports/ --name-only \
  | grep -oE 'BL-[0-9]+' | sort -t- -k2 -n | tail -1
```

`sort -t- -k2 -n` is numeric on the part after the dash. A plain `sort` puts `BL-99` after
`BL-681`, which is how a ceiling gets misread in the first place.

### If the push is rejected

`! [rejected] main -> main (fetch first)` means someone pushed while you worked. **Do not
`git pull` and merge blindly** — re-run step 2 first. Your chosen ID may have been taken in the
interval. Rebase, re-check, rename if needed, then push.

---

## Two projects publish here, and their IDs are not globally unique

This repository carries reports from **more than one project** — `clipper-finder` (the Python
lead-generation pipeline) and `ClippersHQ` (the Next.js app). They number their own tickets
independently, so the same `BL-NNN` can legitimately exist in both, and "take the next free ID"
is the wrong answer when the number is not yours to take.

**The established fix is to suffix the filename, not to renumber someone else's ticket.** Real
precedent, handled correctly by another agent:

```
reports/BL-676.md                            <- clipper-finder's BL-676, untouched
reports/BL-676-clippershq-campaign-refusal.md  <- ClippersHQ's BL-676, published beside it
```

The collision check still applies unchanged: `reports/BL-676.md` already existed, so it was not
overwritten. The agent chose a new *path*, kept its own ticket number, and said so in the commit
message. Do the same. A suffix of `-<project>-<slug>` keeps both readable and keeps every
existing raw URL working.

## Editing an existing report on purpose

Allowed, and it does not trip the check above because the check only guards *new* paths. Two
requirements:

1. **Say so in the commit message** — `BL-678: relink BL-677 -> BL-679 (citation repair)`.
2. **Leave a note in the report itself** if the change alters meaning. A reader who fetched the
   old raw URL has no way to know it moved underneath them.

Never rewrite another agent's findings. Correcting a broken link or an ID reference is
repair; changing a conclusion is not, and belongs in a new report that cites the old one.

---

## Do not reserve an ID in prose before it exists

A third failure mode, found by the same audit. `BL-648` wrote:

> "Two pre-existing issues were reported, not fixed, and filed as **BL-649** (the viewport meta
> blocks pinch zoom) and **BL-650** (the recharts SVG has no text alternative)."

Neither report was ever written. Both IDs were later claimed by unrelated work — `BL-649` by a
merge report, `BL-650` by the analytics-screenshot reader. The citation in `BL-648` now points at
two documents that have nothing to do with what it describes, and no link-fix can repair it
because the referenced content never existed.

**Refer to future work by description, not by a number you have not published.** An ID becomes
real when the file lands on `main`, not when someone intends to write it.

---

## Checklist before publishing

- [ ] `git fetch origin` — remote state is current
- [ ] Next ID read from `origin/main`, sorted numerically
- [ ] Collision check passes for every **new** path in the push
- [ ] No credentials in the report (see `README.md` — this repo is public by design)
- [ ] Every `[BL-NNN](BL-NNN.md)` link resolves to the report you actually mean
- [ ] Any forward reference is described, not numbered
