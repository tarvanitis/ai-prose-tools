# Style & Consistency Guide

The source files were authored separately, so they disagree on voice, self-labeling, and numbering.
A book needs one editorial voice. These rules resolve the conflicts. Where this guide is silent,
`CLAUDE.md` governs.

## Editorial voice

The target voice usually already exists in the strongest source chapters (the fundamentals and
training). It is **warm, precise, and pedagogical**: plain English first, formalism second, concrete
worked numbers throughout. Bring the other chapters up to this register:

- Prefer the direct second person ("you'll see", "notice that") and the inclusive first person plural
  for shared reasoning ("we can now…"). Pick one and keep it consistent within a chapter.

- Explain before you formalize: a plain-English sentence or analogy, then the definition, then the
  formula, then a worked example. This is the source's own order, enforce it everywhere.

- Drop self-labels ("Student Guide", "Complete Terminology Guide"). The book has one title.
- Fix source-quality issues carried over from the HTML originals: typos ("architecures",
  "geneally"), any emoji sign-off, and informal register drift in the weaker source files.

## Recurring devices (define once in the preface, use consistently)

- **Recurring analytical lenses.** If the book examines each idea from a fixed set of angles, name
  them once in the preface and keep the names and their meanings uniform throughout. Do not add a
  lens or rename one mid-book. (One worked example: Geometric, "the shape of the computation";
  Representation, "the meaning"; Mechanistic, "the machinery".)

- **Typed callouts (no raw emoji).** Callouts are pandoc fenced divs from a controlled vocabulary,
  each rendered with a small (12pt), vertically-centred monochrome icon (accent red), no enclosing
  badge, see
  `assets/classic-book.css` and `assets/icons/`. Emoji are *not* used in the manuscript. They clash with the classic serif theme.

  - `::: {.callout .idea}`: **Key idea / insight** (light bulb).
  - `::: {.callout .plain}`: **Plain English** intuition (speech bubble).
  - `::: {.callout .lens}`, an analytical lens; the bold label says which.
  - `::: {.callout .deepdive}`: **technical deep-dive** (magnifier).
  - `::: {.callout .note}`, neutral aside / info (info "i").
  - `::: {.callout .caution}`, pitfall / gotcha (warning triangle).
  **Labels:** drop the redundant lead-in where the icon + preface legend already convey it, `.idea`
  and `.plain` carry **no** label. `.lens` keeps a one-word qualifier (**Geometric.** /
  **Representation.** / **Mechanistic.**), since one icon can't distinguish the three. `.note`,
  `.caution`, and `.deepdive` keep their short descriptive lead (informative, not redundant). Keep the
  set small. Incidental one-off asides may stay plain blockquotes (cream box, no icon). The chapter
  bridge ("Coming up:") stays a plain blockquote. The **icon legend lives in the preface**.

## Notation (inherits CLAUDE.md, restated because it's the top consistency risk)

- **Hybrid notation.** Recommended for a Markdown manuscript rendered through Pandoc, where LaTeX
  becomes native OMML equations in Word and SVG in PDF.

  - *Inline* notation is plain Unicode: `√d_k`, `Σᵢ`, `π_θ`, `‖x‖`, `∝`, `≈`. Keeps prose readable
    and diffs clean.

  - *Display* equations use LaTeX in `$$…$$` **only where Unicode is genuinely worse**: stacked
    fractions (softmax), bracketed matrices, multi-line/aligned derivations. Don't LaTeX-ify things
    Unicode already renders cleanly.

  - *Worked numeric examples* stay in fenced code blocks, never convert step-by-step arithmetic to
    LaTeX. Monospace alignment is the point.

  - In LaTeX, prefer `\mathrm{}` for operator names (`\mathrm{softmax}`), `\top` for transpose,
    `\lVert x\rVert` for norms, `\begin{bmatrix}…\end{bmatrix}` for matrices.

- Keep symbol usage identical across chapters: one symbol per concept (e.g. `d_model` vs
  `d_k` used consistently. Don't let one chapter write `h` for what another calls `d_model`).

- Real worked numbers should stay internally consistent, the source often uses Llama 3 8B shapes
  (`E ∈ ℝ^{128000×4096}`); keep one running reference model per Part where possible.

## Numbering & captioning

- **Headings:** one H1 per chapter file (the chapter title). Sections H2 (`N.M`), sub-sections H3.
  Avoid H4+ (CLAUDE.md). Parts are inserted at assembly, not as chapter H1s.

- **Figures:** number `Figure N.k` per chapter. Every Mermaid diagram and ASCII diagram that a
  reader would refer to gets a caption. Collect into a List of Figures if the edition warrants it.

- **Tables:** `Table N.k` with a caption. Collect into a List of Tables if used.
- **Equations:** number displayed equations `(N.k)` only if they're referenced later. Don't number
  every formula.

- **Cross-references** use these labels ("as shown in Figure 5.2", "see Chapter 2"), never file
  names or `§`-from-the-old-numbering.

## Model-version callouts

Use the dated blockquote form from CLAUDE.md:

```
> **Current model families (as of YYYY-MM-DD):** …
```

Verify every version number from vendor release pages before publishing, never from memory or
training data. Update the date when refreshed. Keep the "durable shape vs. dated snapshot" framing
the source uses, so the book ages gracefully.

## Consistency passes (run across the whole manuscript, not per chapter)

1. **Terminology:** every term defined once (in the glossary); first chapter mention links to it; no
   term redefined in a chapter.

2. **Voice:** one person/tense per chapter. Self-labels gone.
3. **Notation:** one symbol per concept book-wide. Hybrid math per the Notation section above
   (Unicode inline, `$$...$$` display only where Unicode is genuinely worse).

4. **Numbering:** figures/tables/equations sequential and captioned. All cross-refs resolve.
5. **Dedup:** no foundation taught twice (see `book-architecture.md` dedup plan).
6. **Prose:** run the `prose-linter` skill, or its scanner directly:
   `python3 ~/.claude/skills/prose-linter/scripts/scan.py FILE.md --min-count 2`.
   ~36 content tells across 10,600 lines was deemed acceptable for the reference; hold roughly that
   density, don't over-sand the prose.

## Style choices to preserve (do not "fix")

- En-dashes (–) in numeric ranges (`2–3`, `10–20`) are deliberate (CLAUDE.md). Em-dashes (—) are
  **not** exempt: CLAUDE.md asks for them sparingly (at most one pair per paragraph, not in every
  paragraph), and the Stage 4 humanization pass reduces them. Do not treat em-dash density as
  protected style.

- ASCII diagrams and hand-worked arithmetic, they're a feature, keep them.
- The analogies ("keyhole vs. whole page", "GPS coordinates for words", "matrix as a recipe"): keep
  and, where helpful, reuse consistently rather than inventing new ones for the same idea.
