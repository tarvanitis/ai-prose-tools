# Maintenance & Freshness

Any technical book makes two kinds of claim. The mechanics are durable. The **named products,
versions, sizes, prices, dates and tooling are perishable**, and they rot silently: nothing in the
manuscript warns you that a number stopped being true.

This file is the playbook for finding those spots and verifying them. Build a freshness catalog
for your own book from the categories below, then run the refresh procedure on demand, or when a
durable trigger (see the end of this file) reminds you.

A skill file is inert. It does not watch vendor pages or run on its own. It tells whoever invokes
it exactly what to check and how.

## Freshness catalog (what goes stale, and how fast)

Catalog your own manuscript against these categories. The rows are the kinds of claim that rot.
Fill in where each one lives in your book.

| Category | What churns | Cadence | How to verify |
|---|---|---|---|
| Dated snapshot callouts (`as of YYYY-MM-DD`) | Product and version names, who currently leads | **High** (weeks) | Fetch the vendor's own page. Confirm current names and tiers, then re-date the block |
| Specification tables and appendices | Sizes, counts, limits, prices | **High** | Primary docs and spec sheets. Cross-check every number, never from memory |
| Timelines and "evolution" sections | The last few rows only | **Yearly** | Add the year's notable shifts. Keep older rows as history |
| Tooling, versions and install instructions | Package versions, flags, names, sample hardware | **High** | Project release pages and changelogs. Record a tested-on date |
| "Current trends" framing | What is now standard, versus emerging, versus superseded | **Medium** (quarters) | Recent surveys and primary sources. Adjust the framing, not only the names |
| Bibliography and further reading | Link rot, new landmark work | **Medium** | Check every link resolves. Add what has since become essential |
| Weasel phrasing: `as of`, `latest`, `current`, `state-of-the-art`, `today`, `recently` | Silent staleness | Continuous | Grep for these. Each is a claim carrying an implicit expiry date |
| Worked examples pinned to a named product | Numbers drift if the example is re-pegged | **Low** | If you re-peg to a newer product, re-verify the arithmetic |

Fast grep to locate hotspots across the manuscript:

```bash
grep -rniE 'as of|current model families|guide version|latest|state-of-the-art|\b20[0-9]{2}\b' .
```

## Refresh procedure

1. Grep the canonical tree for the hotspots above. Build a worklist of every dated/volatile claim.
2. For each, **web-verify from the vendor's own page** (WebFetch/WebSearch): never from training
   data or memory (`CLAUDE.md`). Record source + date checked.

3. Update names, versions, sizes, and the `as of YYYY-MM-DD` dates. Preserve the "durable shape vs.
   dated snapshot" framing so the book keeps ageing gracefully, don't turn it into a changelog.

4. Re-verify (in Python) any worked example whose numbers you changed.
5. Re-validate any diagram or equation you touched, and rebuild to confirm it still renders.
6. **Report a diff of proposed changes for the author to approve, do not silent-edit.** Only after
   approval, apply and re-run the production build (`references/production.md`).

7. Run the `prose-linter` scan on changed chapters.

Output of a refresh run is a short report: what was checked, what's current, what changed, and the
proposed edits, plus anything genuinely new worth a paragraph (a new model class, a new technique).

## Durable trigger (the part CronCreate can't do)

The in-session scheduler (`CronCreate` / `/loop`) is **session-only and expires in 7 days**, so it
cannot deliver a persistent monthly check across sessions. For a trigger that survives, use one of:

- **A `SessionStart` hook** (in `.claude/settings.json`, set up via the `update-config` skill): on
  opening a session in this project, a small script reads the newest `as of YYYY-MM-DD` date in the
  canonical tree and, if it's older than a threshold (e.g. 30 days), prints a reminder to run this
  refresh. Durable, no external dependencies; it *nudges*, the skill does the actual web-verified
  work. Recommended default.

- **An OS `crontab` entry** running `claude -p "<refresh prompt>"` on a real monthly schedule. Truly
  unattended, but requires the machine to be on at fire time, working non-interactive auth, and
  per-run cost. Use if you want the check to happen without you opening a session.

Either way, the refresh itself is this procedure; the trigger only decides *when* it runs.
