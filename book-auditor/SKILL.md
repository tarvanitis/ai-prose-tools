---
name: book-auditor
description: >
  Audit a book-length technical manuscript for the defects that appear once content moves:
  broken cross-references, figure and table numbers that no longer match their captions,
  uncaptioned figures, missing chapter openers or closing bridges, inconsistent notation and
  terminology, absent front or back matter, and dated claims that have gone stale. Use when
  asked to "audit the manuscript", "review the book", "check the chapter numbering", "check
  cross-references", "find what is stale", "is the book consistent", or before a release or a
  review pass. Includes a mechanical CLI checker (scripts/check-structure.py) that can gate a
  build, and reference rubrics for architecture, chapter structure, editorial style, and
  production.
---

# Book Auditor

Check a book-length technical manuscript against the conventions a finished book has to hold,
and report what is broken. This skill inspects. It does not rewrite.

It pairs with **prose-linter**, which audits the words. This one audits everything around them:
the numbering, the references, the scaffolding, and the arc.

## The two halves

**Mechanical.** `scripts/check-structure.py` catches what a human reliably misses. Figure and
table numbers are hard-coded literals in Markdown. Nothing renumbers them automatically, so
inserting a table into Chapter 12 silently leaves the rest of that chapter mis-numbered and every
reference to it stale. The checker makes that loud.

```bash
python3 scripts/check-structure.py chapters/*.md          # report
python3 scripts/check-structure.py chapters/*.md && make  # gate a build
```

It checks figure and table numbering sequence, captions present on every figure, cross-references
that resolve to a chapter that exists, dated claims older than a threshold, and bibliography
entries whose line breaks will collapse on render. Exit code is non-zero when something fails, so
it drops straight into a Makefile or CI.

Conventions it assumes, which you can change in the script: chapter files are named `ch-NN-*.md`,
appendices `appendix-a-*.md` and `appendix-b-*.md`, and a dated claim is stale after 90 days.

**Editorial.** The rest needs judgment. Work through the rubrics below and report findings rather
than silently fixing them. An audit that edits as it goes is not an audit.

## What to audit

Run these in order. Stop and report after each pass rather than accumulating a single verdict.

1. **Structure.** Run the mechanical checker first. Everything it reports is a defect, not an
   opinion. Fix those before spending judgment on anything else.

2. **Architecture.** Does the manuscript have what a book needs and a draft usually lacks: a
   preface, a "how to read this book", clean front matter, a glossary, a bibliography, an index?
   Are the Parts balanced, or does one carry three chapters while another carries nine? See
   `references/book-architecture.md`.

3. **Chapter integrity.** Does every chapter open by saying what it will cover and close by
   handing off to the next? Are there leftover tells from an earlier life as standalone
   documents: per-file footers, duplicated H1s, version blocks, `§`-style internal links that
   should now be chapter references? See `references/chapter-workflow.md`.

4. **Consistency.** One editorial voice, or several? Is the same concept named the same way in
   Chapter 3 and Chapter 17? Is notation uniform? Are foundations taught once and referenced
   after, or re-derived in four places? See `references/style-guide.md`.

5. **Forward promises.** Does every "we will see in Chapter 9" actually pay off in Chapter 9?
   Unkept forward references are the most common defect in a restructured manuscript and the
   mechanical checker cannot see them.

6. **Freshness.** Every dated or volatile claim, verified against a primary source rather than
   from memory. See `references/maintenance.md`.

7. **Production.** Does it build? Do figures, math, code blocks and callouts render correctly in
   the output format? Two things are invisible in the Markdown and easy to ship blank: the PDF's
   document metadata (`/Title`, `/Author`, `/Subject`, `/Keywords`) and a statement of the edition
   on the copyright page. Check both by opening the output, not the source. See
   `references/production.md`.

## Reporting

Report findings as a list, most severe first, each with a file and line. Separate the mechanical
failures (objectively wrong) from the editorial findings (judgment). Say plainly which is which.

Do not fix as you go unless asked. The author decides what is a defect and what is a choice.

## Reference files

- `references/book-architecture.md`: Parts and Chapters, front and back matter templates,
  deduplication of repeated foundations.
- `references/chapter-workflow.md`: per-chapter structure, opener and closer templates,
  cross-reference conventions, a per-chapter checklist.
- `references/style-guide.md`: editorial voice, notation, figure/table/equation numbering,
  footer stripping.
- `references/production.md`: manuscript assembly and rendering.
- `references/maintenance.md`: the freshness catalog and a verified refresh procedure.

## Guardrails

- **Verify dated claims against primary sources**, never from memory. Version numbers, model
  names, benchmark results and prices all drift. Surface a proposed diff for the author to
  approve rather than silent-editing.
- **Arithmetic in worked examples is checkable.** Recompute it rather than trusting it.
- **Do not invent content to fill a thin chapter.** Report the imbalance and let the author
  decide whether to group, cut, or expand.
- **Preserve the author's terminology.** A term is a finding only when it is factually wrong in
  context, not when you would have chosen a different word.
- **Run prose-linter separately** for wording, punctuation and dialect. This skill does not
  duplicate those checks.
