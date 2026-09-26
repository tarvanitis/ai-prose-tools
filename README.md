# ai-prose-tools

Writing tools for long-form work: lint prose for AI tells, audit structure for unnumbered figures
and broken cross-references. Runs standalone or as agent skills.

Both tools are plain Python with no third-party dependencies and no agent required. Python 3.8 or
later. The optional `book-audit.toml` config needs 3.11 or later for `tomllib`. On older
versions the config is skipped and the defaults apply. They are also packaged as
[Claude Code](https://claude.com/claude-code) skills, which is a convenience, not a requirement.

---

## prose-linter

Catches the mechanical tells of AI writing: em-dash overuse, semicolons joining independent
clauses, filler openers, nominalization, hedging, inflated-importance claims, and the rest of the
catalog documented in Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
It also carries guidance for writing human prose from the start, and for matching an author's
existing voice.

```bash
python3 prose-linter/scripts/scan.py FILE.md                 # report everything
python3 prose-linter/scripts/scan.py FILE.md --min-count 2   # only repeated tells
python3 prose-linter/scripts/scan.py FILE.md --quiet         # summary only
python3 prose-linter/scripts/scan.py *.md --gate --emdash-per 500   # fail a build
```

`--gate` enforces the hard rules and exits non-zero when they are broken: the em-dash budget,
clause-joining semicolons, spelling dialect, and defects that are invisible in Markdown but appear
in the rendered output. Word-choice findings stay advisory, because they need judgment.

Spelling dialect defaults to American English. Override with `PROSE_DIALECT=en-GB` or
`PROSE_DIALECT=off`. The word list lives in `prose-linter/references/dialect-wordlist.txt`, so a
word can be added without touching code.

## book-auditor

Audits a book-length manuscript for what breaks when content moves: figure and table numbers that
no longer match their captions, uncaptioned figures, cross-references to chapters that do not
exist, dated claims that have gone stale, and bibliography entries whose line breaks collapse on
render.

```bash
python3 book-auditor/scripts/check-structure.py chapters/*.md
python3 book-auditor/scripts/check-structure.py --strict chapters/*.md   # warnings fail too
```

**It calibrates itself against your manuscript rather than imposing conventions.** It infers your
chapter filename pattern, learns your dominant cross-reference and caption styles, and reports
what deviates from them. A book that writes "Chapter 5" everywhere and "Ch. 5" twice gets told
about the two, not about the two hundred.

Findings come in two classes. **FAIL** is objectively broken and exits non-zero, so it gates a
build. **WARN** is inconsistency with your own dominant convention, which is advisory because
sometimes the minority usage is deliberate.

Given part of a manuscript, it says so and does not treat references to the missing chapters as
errors. A reference to a chapter missing from *inside* the range you supplied is still a failure.

Configuration is optional. Drop a `book-audit.toml` beside the manuscript:

```toml
chapter_pattern = "ch-(\\d+)-"              # default: inferred from your filenames
stale_days      = 90                        # age at which an "as of" claim is flagged
allow           = "allow.txt"               # files exempt from caption-count checks
xref_styles     = ["Chapter N", "Ch N"]     # cross-reference forms you use on purpose
```

`xref_styles` is worth explaining, because it is the difference between silencing a check and
teaching it. By default the tool infers your dominant cross-reference form and warns about the rest.
Some books legitimately use two: the full form in running prose, an abbreviation in glossary entries
and narrow table cells. Declaring both replaces the guess with a fact. The declared forms are
accepted, and anything outside the set still warns, so genuine drift is still caught. Recognized
forms are `Chapter N`, `Ch. N`, `Ch N` and `§N`. A name that is not one of those is reported rather
than ignored, so a typo cannot quietly disable the check.

The config file is looked for beside the manuscript first, then in the working directory, and the
one that was used is printed.

The `book-auditor/references/` directory holds the editorial rubrics the mechanical checker cannot
cover: book architecture, per-chapter structure, editorial style, production, and a freshness
procedure for claims that rot.

---

## Using them as agent skills

Copy or symlink each directory into your skills directory:

```bash
ln -s "$PWD/prose-linter"  ~/.claude/skills/prose-linter
ln -s "$PWD/book-auditor"  ~/.claude/skills/book-auditor
```

## License

MIT, with one exception. `prose-linter/SKILL.md` adapts Wikipedia's catalog of AI-writing
patterns and therefore carries **CC BY-SA 4.0** forward. See [NOTICE](NOTICE) for the detail, and
for the attribution to [Blader's Humanizer](https://github.com/blader/humanizer), on which the
prose skill is based.

## In use

`prose-linter` gates the build of *Inside the Transformer: From Attention to Reasoning*, a free book
on how transformers and large language models work. That book's prose gate calls this scanner
directly, and refuses to produce a PDF when a hard rule is broken.

`book-auditor` grew out of the same book's structure checker, generalized here to work on any
manuscript. That book now runs this version, configured for its own conventions through
`book-audit.toml` rather than by editing the script. Its authoring skill stays with the book, since
it describes that manuscript rather than manuscripts in general.
