# Production: Assembly & Rendering

How to assemble chapter files into one manuscript and render publishable deliverables, and what to
check in the output. The specifics below describe one working pipeline. Substitute your own tools.
The failure modes are the same.

## Prerequisites (toolchain)

A known-good combination: **pandoc 3.1.3**, **WeasyPrint 69.0**, **Node 18** + **mathjax-full**,
**PyMuPDF 1.28**, **TeX Gyre** fonts, **Noto Color Emoji**. Record the versions you verified and
the date, and re-verify after any upgrade. A silent toolchain bump is a common cause of a build
that worked last month and does not today.

Two rendering paths, two math strategies:

- **PDF (professional review copy):** `build-pdf.py` renders ` ```mermaid ` fences to **PNG via
  mermaid-cli (Chromium, with a custom theme)**, runs `pandoc --mathjax --wrap=none`, pre-renders LaTeX
  `$$…$$` equations to **SVG via MathJax (Node)**, then **WeasyPrint** + `assets/classic-book.css`.
  Two things WeasyPrint can't do itself, both pre-rendered here: its native MathML doesn't stack
  fractions/radicals/matrices (and leaks raw LaTeX), and it can't run Mermaid's JS. Mermaid is
  rendered to **PNG, not SVG**. Chromium rasterizes its HTML labels correctly, whereas SVG-text mode
  mangles multi-word labels. (`--wrap=none` matters: otherwise pandoc inserts newlines inside tags and
  the equation-extraction regex misses spans.)

- **Word (handoff deliverable):** `pandoc … -o out.docx` converts `$$…$$` straight to native OMML
  Word equations. MathJax is not needed there.

**Required**

- **pandoc** ≥ 3.
- **WeasyPrint** ≥ 66 (`pip install weasyprint`): HTML+CSS → PDF.
- **Node** ≥ 18 + **mathjax-full** (`cd tools/math && npm install mathjax-full`): LaTeX → SVG
  for the PDF path, via `tools/math/tex2svg.js`.

- **mermaid-cli** (`@mermaid-js/mermaid-cli`, gives `mmdc`) + a headless **Chromium** (auto-fetched by
  its puppeteer dependency): renders ` ```mermaid ` fences to PNG using a theme config
  (`assets/mermaid-config.json`, which sets `flowchart.curve` and similar; keep mermaid's default
  `htmlLabels: true` since PNG rendering handles them). Installed in `tools/math`. Needs
  `tools/math/puppeteer-config.json` =
  `{"args":["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"]}` for Chromium to launch headless.

- A **serif book font**, `sudo apt-get install fonts-texgyre` (TeX Gyre Termes ≈ Times, Pagella ≈
  Palatino, plus the Courier-like *Cursor* mono); auto-selected by `classic-book.css`. DejaVu Serif
  is the fallback.

**Recommended**

- **PyMuPDF** (`pip install pymupdf`): rasterize the PDF to PNG to eyeball/verify renders.
- **PyTorch** (`pip install torch`, CPU build is fine): to *run* code-chapter listings (Parts III–IV),
  not just syntax-check them: extract the ` ```python ` fences, build the model on a tiny config, and
  smoke-test forward pass → one AdamW step (loss drops) → `generate()`. Code must execute, not just parse.

- **Noto Color Emoji** (`sudo apt-get install fonts-noto-color-emoji`) if the 🔑 / 🔬 markers stay.
  otherwise swap them for styled text labels (see `style-guide.md`).

PDF build: `python3 build-pdf.py OUT.pdf FILE1.md [FILE2.md …]`.

## The roles a build pipeline needs

Whatever tools you pick, these jobs have to be done by something. Audit that each one is covered,
and that no two tools are doing the same job differently.

| Role | What it does | Failure if missing |
|---|---|---|
| **Assembler** | Concatenates chapters in order, inserts Part dividers, generates the table of contents | Chapter order drifts from the intended structure |
| **Converter** | Markdown to the output format |, |
| **Math renderer** | Display equations to SVG or native equation objects | Raw LaTeX leaks into the output, or fractions fail to stack |
| **Diagram renderer** | Diagram source to images, before conversion | Diagram fences appear as code blocks |
| **Typesetter** | HTML and CSS to paginated PDF |, |
| **Verifier** | Rasterizes pages so you can look at them | Silent layout breakage: overflow, bad page breaks, missing glyphs |

Two rules worth holding. **Pre-render anything the typesetter cannot do itself** rather than hoping
it copes. And **check the rendered output, not the Markdown**: overflow, page breaks and missing
glyphs are invisible in the source.
## Assembly

A merge script written for a single-document collection typically demotes every H1 to H2 so the
whole thing nests under one document H1. A book wants a different hierarchy: **Parts** as the top
grouping and **chapter H1s preserved**. Two options:

- **Preferred:** add a small book-assembly step (or a `--book` mode / a sibling script) that:
  1. emits front matter (title page, edition note, preface) first.
  2. inserts a Part divider before each Part's first chapter.
  3. concatenates chapter files **without** demoting their H1s.
  4. appends back matter (appendices, bibliography, index).
  5. generates a TOC from Parts → Chapters → sections.
    If an existing merge script serves another purpose, leave it alone and add alongside rather
    than repurposing it.

- **Quick path:** keep the file order in one place, a Makefile or a manifest, and concatenate in
  that order, then let the renderer build the TOC. Acceptable for early drafts.

**Keep the order explicit and never glob it.** Alphabetical order is rarely the reading order: a
front-matter directory will sort a cover file after the numbered ones. A list you maintain by hand
makes adding a chapter a visible edit, and makes a forgotten file obvious.

Recommended manuscript tree (from `book-architecture.md`):

```
book/
  frontmatter/00-title.md, 01-copyright.md, 02-preface.md
  part-1/ch-01-*.md, ch-02-*.md
  part-2/ … part-5/ …
  backmatter/appendix-a-glossary.md, appendix-b-specs.md, bibliography.md, index.md
  book.md            # generated manuscript
```

## Document metadata

A PDF carries a document-information dictionary that readers show in their Properties pane, and that
ebook managers, reference managers and library catalogs index. It is easy to ship a book with all of it blank, because
nothing in the build fails when it is missing and nothing in the Markdown hints at it.

Populate at least `/Title`, `/Author`, `/Subject` and `/Keywords`. With WeasyPrint these come from
the HTML head that the build assembles:

```
<title>…</title>                        ->  /Title
<meta name="author" content="…">        ->  /Author
<meta name="description" content="…">   ->  /Subject
<meta name="keywords" content="…">      ->  /Keywords
```

Verify the result rather than assuming it worked:

```bash
python3 -c "from pypdf import PdfReader; print(PdfReader('out.pdf').metadata)"
```

**State the edition inside the book**, on the copyright page ("First edition, 2026"). A PDF travels
detached from the repository and from the release page that names its version, so the file has to be
able to identify itself. A filename cannot do this: the first person to save it renames it.

## Rendering deliverables

Draft everything in Markdown (the source of truth), then render:

- **HTML** (screen reading, review): render the assembled Markdown with your HTML converter (use a
  wide layout for
  the glossary/spec tables).

- **PDF** (the review copy): `python3 build-pdf.py OUT.pdf CH…md`, a classic book theme
  (`classic-book.css`) with MathJax-SVG equations. Check that display equations
  render, page breaks fall sensibly at chapter boundaries, worked-example blocks don't overflow the
  page width, and (if kept) the 🔑/🔬 emoji render. Rasterize with PyMuPDF to verify visually.

- **Word** (.docx): **the primary deliverable.** Use **Pandoc**, because the book's hybrid notation
  puts LaTeX in `$$…$$` display equations and only Pandoc turns those into native, editable Word
  equations (OMML). Baseline command:

  ```bash
  # File list in reading order, not a glob. See the assembly note above.
  pandoc frontmatter/... chapters/... backmatter/... \
         -o book.docx --toc --number-sections   # add: --reference-doc=styles.docx
  ```

  Two things to handle for a chapter that contains a Mermaid diagram (Part I chapters 1–2 have none,
  so this isn't blocking the sample): Pandoc doesn't render Mermaid, so **pre-render diagrams to
  PNG/SVG first** (a standalone `mmdc` call does it) and swap the
  ` ```mermaid ` fences for image links before running Pandoc. Then verify figure/table captions and
  numbering survive. Build a `--reference-doc` template once to lock fonts, heading styles, and
  equation styling for the whole book.

## Pre-publication checks

- All worked examples arithmetically verified in Python (CLAUDE.md quality bar).
- No LaTeX artifacts. All math is plain Unicode.
- Every Mermaid diagram validated with Mermaid CLI v11 before it goes in.
- Model-version callouts re-verified against vendor pages and re-dated.
- Cross-reference audit: no dangling `§`, no "this guide", every "see Chapter N"/"Figure N.k"
  resolves.

- TOC, List of Figures, List of Tables, and the index regenerated against the final chapter set.
- Front and back matter present. Per-file footers and the bookmark dump gone.
- **Final whole-book humanize consistency pass**: per-chapter humanizing already happened during
  drafting (see `chapter-workflow.md`); this last pass catches cross-chapter repetition and voice
  drift. Run the scanner over the assembled manuscript at `--min-count 2`. Don't over-sand.

## Note

Do not hand-edit derived build artifacts. Combined Markdown, rendered HTML, PDF and .docx are
outputs, not sources. Edit the canonical chapter files and rebuild. An edit made in an artifact is
lost at the next build, and until then the two disagree.
