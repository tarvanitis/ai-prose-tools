#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan.py - flag the *mechanical* tells of AI-generated writing in a text or
Markdown file: typographic characters, filler openers and sign-offs, overused
words, formulaic phrases, synonym pairs, "not just X but Y" constructions, and
transition/hedge pile-ups. Each hit is reported with line:column.

What this does NOT do: judge the structural and voice tells (symmetry, sandwich
structure, false balance, missing opinions, over-hedging). Those need a human or
Claude reading the text - see SKILL.md.

Findings are candidates, not verdicts. Formal/technical registers legitimately
use some of these words ("comprehensive scope", "robust design"). Weigh
frequency and combination, not single hits.

Usage:
    scan.py FILE [FILE ...] [--quiet] [--min-count N]
Exit code is 1 when anything is flagged (usable as a pre-publish gate), else 0.
"""
import argparse
import os
import pathlib
import re
import sys

# --- typographic characters (checked in prose, outside code) ---
CHARS = {
    "—": "em dash",        "–": "en dash",
    "‒": "figure dash",    "―": "horizontal bar",
    "…": "ellipsis character",
    "“": "curly quote",    "”": "curly quote",
    "‘": "curly quote",    "’": "curly apostrophe",
    "•": "bullet symbol",
    ";": "semicolon (B18 - prefer period; only legitimate in comma-lists)",
}

# --- line-start affirmations / lead-ins ---
OPENERS = [
    "certainly", "absolutely", "of course", "sure", "definitely",
    "great question", "that's a great point", "that is a great point",
    "i'd be happy to help", "i would be happy to help", "i'm happy to help",
    "let's dive in", "let's explore", "let's unpack", "let's get started",
    "let's take a look", "dive in", "in this article", "in this document we will",
]

# --- sign-offs / closers (anywhere) ---
CLOSERS = [
    "i hope this helps", "hope this helps", "good luck",
    "feel free to reach out", "feel free to ask", "happy to help",
    "let me know if you have any questions", "if you have any questions",
    "don't hesitate to reach out",
]

# --- formulaic phrases (anywhere) ---
PHRASES = [
    "it's important to note", "it is important to note",
    "it's worth mentioning", "it is worth mentioning", "it's worth noting",
    "it is worth noting", "it should be noted that", "it can be observed that",
    "this ensures that", "this allows for", "this, in turn,", "this means that",
    "keep in mind that", "bear in mind that",
    "in today's world", "in today's fast-paced world", "in today's digital age",
    "in an era of", "in the ever-evolving", "in an ever-evolving",
    "as technology continues", "over the past decade",
    "at the end of the day", "when it comes to", "the fact of the matter is",
    "it goes without saying", "as previously mentioned", "needless to say",
    "moving forward", "going forward", "on a high level", "at its core",
    "that said", "with that in mind", "in the realm of", "in the world of",
    "plays a crucial role", "plays a key role", "plays a vital role",
    "a testament to", "aims to", "serves as",
    "when it comes down to it", "from start to finish",
    # verbosity phrases (N29-class substitutions)
    "due to the fact that", "provides the ability to", "offers the capability to",
    "at this point in time", "in the event that",
]

# --- "not just X but Y" family ---
NOT_JUST = [
    # Existing negation-antithesis family
    (re.compile(r"\bnot\s+just\b[^.\n]{0,60}?\bbut\b", re.I), "not-just-X-but-Y construction (N37)"),
    (re.compile(r"\bnot\s+only\b[^.\n]{0,60}?\bbut\s+also\b", re.I), "not-only-but-also construction (N37)"),
    (re.compile(r"\bisn't\s+just\b", re.I), "isn't-just construction (N37)"),
    (re.compile(r"\bit'?s\s+not\s+about\b[^.\n]{0,60}?\bit'?s\s+about\b", re.I), "it's-not-about-X-it's-about-Y (N37)"),
    (re.compile(r"\bless\s+about\b[^.\n]{0,40}?\bmore\s+about\b", re.I), "less-about-more-about parallelism (N37)"),
    (re.compile(r"\bfrom\b\s+[a-zA-Z]{4,}\s+\bto\b\s+[a-zA-Z]{4,},", re.I), "'from X to Y' framing (N39 - use a specific example)"),
    # N38 — participial openers
    (re.compile(r"^(Having\s+\w+ed|Drawing\s+on\b|Armed\s+with\b)", re.I), "participial opener (N38 - convert to main clause)"),
    # N40 — rhetorical question + immediate answer
    (re.compile(r"\b(so\s+what\s+does\s+this\s+mean|but\s+what\s+is|why\s+does\s+this\s+matter|how\s+does\s+this\s+work)\?", re.I), "rhetorical Q + answer (N40 - delete question, keep answer)"),
    # N43 — explanatory chain
    (re.compile(r"\bthis,?\s+(in\s+turn,?\s+)?(means\s+that|allows|enables|ensures|provides)\b", re.I), "explanatory chain (N43 - collapse to one sentence)"),
    # N37 extended
    (re.compile(r"\bit'?s\s+not\s+[a-zA-Z].*?—\s*it'?s\b", re.I), "it's-not-X-it's-Y (N37)"),
    (re.compile(r"\bwhat\s+began\s+as\b[^.\n]{0,40}?\bbecame\b", re.I), "what-began-as-X-became-Y (N37)"),
]

# --- transition adverbs (pile-up signal) ---
TRANSITIONS = ["furthermore", "moreover", "additionally", "in addition to this",
               "last but not least", "as such", "in essence"]

# --- hedges ---
HEDGES = ["it could be argued", "one might consider", "there is a possibility",
          "generally speaking", "for the most part", "it may or may not",
          "in some cases", "some experts believe", "studies show",
          "research suggests", "experts agree"]

# --- synonym pairs ---
PAIRS = ["clear and concise", "helpful and informative", "quick and easy",
         "safe and secure", "simple and straightforward", "fast and efficient",
         "new and innovative", "tried and true", "tips and tricks",
         "peace of mind"]

# --- overused single words ---
WORDS = [
    # Tier A — near-diagnostic in clusters
    "delve", "tapestry", "beacon", "testament", "crucible", "odyssey", "watershed",
    "labyrinth", "mosaic", "embark", "unlock", "harness", "underscore", "underscores",
    "foster", "cultivate", "usher", "resonate", "elevate", "empower", "amplify",
    "bolster", "spearhead", "garner", "navigate", "unveil",
    # Tier B — strong signal on density
    "nuanced", "robust", "leverage", "leveraging", "utilize", "utilizing",
    "comprehensive", "multifaceted", "holistic", "seamless", "seamlessly",
    "streamline", "crucial", "vital", "pivotal", "groundbreaking",
    "innovative", "cutting-edge", "actionable", "showcase", "showcases",
    "tapestry", "landscape", "boast", "boasts", "myriad", "plethora", "intricate",
    "intricacies", "bustling", "vibrant", "pertinent", "paramount",
    "meticulous", "meticulously", "commendable", "notably",
    # Tier C — intensifiers
    "truly", "incredibly", "remarkably", "significantly", "undoubtedly",
    "fundamentally", "inherently", "essentially", "crucially", "importantly",
]

WORD_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in WORDS) + r")(?![\w-])", re.I)

# B17b - spelling dialect. Word data lives in references/dialect-wordlist.txt so a
# word can be added without touching this regex. Default American. Override with
# PROSE_DIALECT=en-GB (or "off"). HUMANIZE_DIALECT is still honoured as the
# previous name of this variable.
_DIALECT = os.environ.get("PROSE_DIALECT",
                          os.environ.get("HUMANIZE_DIALECT", "en-US")).lower()
_WORDLIST = pathlib.Path(__file__).resolve().parent.parent / "references" / "dialect-wordlist.txt"


def _load_dialect(path=_WORDLIST):
    pairs, suffix, same = {}, [], []
    section = None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return pairs, suffix, same
    for raw in text.split("\n"):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if section == "pairs" and "=" in line:
            b, a = (x.strip() for x in line.split("=", 1))
            pairs[b.lower()] = a
        elif section == "suffix":
            suffix += line.split()
        elif section == "same-in-both":
            same += line.split()
    return pairs, suffix, same


DIALECT_PAIRS, _SUFFIX, _SAME = _load_dialect()

# Anchored at ^ this only caught words *starting* with the stem, so "overpromising"
# slipped through and the -ise rule mangled it to "overpromizing". Allow a prefix.
_SAME_RE = re.compile(r"^\w*?(?:" + "|".join(re.escape(w) for w in _SAME) + ")", re.I) if _SAME else None
_PAIR_RE = (re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in DIALECT_PAIRS) + r")(?![\w-])", re.I)
            if DIALECT_PAIRS else None)
_SUFFIX_RE = (re.compile(r"(?<![\w-])(\w{3,}?is(?:" + "|".join(x[2:] for x in _SUFFIX if x.startswith("is")) + r"))(?![\w-])", re.I)
              if _SUFFIX else None)
_AMER_RE = re.compile(r"(?<![\w-])(\w{3,}?iz(?:e|es|ed|ing|ation|ations|er|ers)"
                      r"|\w*(?:color|behavior|favor|neighbor)\w*"
                      r"|modeling|modeled|labeling|labeled|analyze\w*|license|defense|toward|gray)"
                      r"(?![\w-])", re.I)


def dialect_hits(text):
    """Yield (col, message) for spellings that fight the configured dialect.

    Callers exclude code and published titles; this only inspects the string given.
    """
    if _DIALECT in ("off", "none"):
        return
    if _DIALECT == "en-us":
        seen = set()
        for rx in (_PAIR_RE, _SUFFIX_RE):
            if not rx:
                continue
            for m in rx.finditer(text):
                w = m.group(0)
                if _SAME_RE and _SAME_RE.match(w):
                    continue
                if m.start() in seen:
                    continue
                seen.add(m.start())
                fix = DIALECT_PAIRS.get(w.lower()) or re.sub(r"is(\w+)$", r"iz\1", w.lower())
                yield m.start(), f"{w} -> {fix} (B17b - house dialect is American English)"
    else:
        for m in _AMER_RE.finditer(text):
            yield m.start(), f"{m.group(0)} (B17b - house dialect is British English)"


_LIST_PREFIX = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|>\s*|#{1,6}\s+|\[[ xX]\]\s*)*")


def _phrase_re(items):
    return re.compile(r"(?<!\w)(" + "|".join(re.escape(p) for p in items) + r")(?!\w)", re.I)


OPENER_RE = _phrase_re(OPENERS)
CLOSER_RE = _phrase_re(CLOSERS)
PHRASE_RE = _phrase_re(PHRASES)
TRANS_RE = _phrase_re(TRANSITIONS)
HEDGE_RE = _phrase_re(HEDGES)
PAIR_RE = _phrase_re(PAIRS)

INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_inline(s):
    """Remove inline code spans and link URLs (keep link text) for prose checks."""
    s = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), s)
    s = LINK.sub(lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), s)
    return s


def semicolon_joins(line):
    """B18: yield columns of semicolons that join independent clauses.

    Guard 17: a semicolon is correct as a higher-level separator in a list whose
    items carry internal punctuation. Signals that this is a list, not a join:
    a comma or bracket earlier in the clause, two or more semicolons on the line,
    the next item opening with a bracket, a bold span, a quote, or "and"/"or".
    A table row separates cells with ";" by construction, so it is never a join.
    """
    if ";" not in line or "\\" in line:
        return
    if line.lstrip().startswith("|"):
        return
    multi = line.count(";") >= 2
    for m in re.finditer(";", line):
        before = line[:m.start()].split(".")[-1]
        after = line[m.start() + 1:].lstrip()
        if re.search(r"[(),\[]", before):
            continue
        if multi:
            continue
        if after[:2] == "**" or after[:1] in ("(", '"', "'", "["):
            continue
        if after.startswith(("and ", "or ", "but ")):
            continue
        yield m.start()


def structural_findings(raw):
    """Render-only defects that are invisible in Markdown source.

    A list that does not have a blank line before it renders as a run-on paragraph;
    a line ending in a hyphen glues a spurious space into the word when Markdown
    joins the lines."""
    out = []
    lines = raw.split("\n")
    in_fence = False
    for i, ln in enumerate(lines):
        st = ln.lstrip()
        if st.startswith("```") or st.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if i and re.match(r"^(\d+\.|[-*+])\s+\S", ln):
            prev = lines[i - 1]
            if (prev.strip() and not prev.startswith((" ", "\t"))
                    and not re.match(r"^(\d+\.|[-*+])\s", prev)
                    and not prev.startswith(("#", "|", ">", ":::"))
                    and not prev.endswith("  ")):
                out.append((i + 1, 1, "list-spacing",
                            "list needs a blank line before it or it renders as a paragraph"))
        if i + 1 < len(lines) and re.search(r"[A-Za-z]-$", ln.rstrip()) and lines[i + 1].strip():
            out.append((i + 1, len(ln.rstrip()), "hyphen-split",
                        "hyphenated word split across lines renders with a spurious space"))
    return out


def emdash_budget(raw, per=500):
    """B9 as a number: em-dashes outside fenced code against one per `per` words."""
    total = 0
    in_fence = False
    for ln in raw.split("\n"):
        st = ln.lstrip()
        if st.startswith("```") or st.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            total += ln.count("\u2014")
    return total, max(len(raw.split()) // per, 1)


def scan_file(path, min_count=1):
    findings = []          # (line, col, category, detail)
    word_counts = {}
    try:
        raw = open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as e:
        return [(0, 0, "error", str(e))], {}
    findings.extend(structural_findings(raw))
    in_fence = False
    for lineno, line in enumerate(raw.split("\n"), 1):
        stripped_line = line.lstrip()
        if stripped_line.startswith("```") or stripped_line.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            # Prose comment lines inside fenced blocks are still prose for B18
            stripped_inner = line.lstrip()
            if stripped_inner.startswith("#") or stripped_inner.startswith("//"):
                for i, ch in enumerate(line):
                    if ch == ";":
                        findings.append((lineno, i + 1, "char",
                                         "semicolon in code comment (B18 - prefer period)"))
            continue
        prose = strip_inline(line)
        # Blank HTML entities so & amp ; etc. don't trigger false-positive semicolons
        prose = re.sub(r"&\w+;", lambda m: " " * len(m.group(0)), prose)

        # B17b - spelling dialect. Bibliography-style lines that are nothing but a
        # bold span are published titles and keep their printed spelling.
        if not re.match(r"^\*\*[^*]+\*\*\s*$", line.strip()):
            for col, msg in dialect_hits(prose):
                findings.append((lineno, col + 1, "spelling", msg))

        for col in semicolon_joins(prose):
            findings.append((lineno, col + 1, "semicolon-join",
                             "semicolon joining independent clauses (B18 - use a period)"))

        for ch, name in CHARS.items():
            start = 0
            while True:
                i = prose.find(ch, start)
                if i < 0:
                    break
                findings.append((lineno, i + 1, "char", name))
                start = i + 1

        body = _LIST_PREFIX.sub("", prose)
        offset = len(prose) - len(body)
        for m in OPENER_RE.finditer(body):
            if m.start() == 0:      # only when it actually opens the line
                findings.append((lineno, offset + m.start() + 1, "opener",
                                 f"filler opener '{m.group(0)}'"))

        for rx, cat in ((CLOSER_RE, "closer"), (PHRASE_RE, "phrase"),
                        (TRANS_RE, "transition"), (HEDGE_RE, "hedge"),
                        (PAIR_RE, "synonym-pair")):
            for m in rx.finditer(prose):
                label = {"closer": "sign-off", "phrase": "formulaic phrase",
                         "transition": "transition adverb", "hedge": "hedge",
                         "synonym-pair": "synonym pair"}[cat]
                findings.append((lineno, m.start() + 1, cat, f"{label} '{m.group(0)}'"))

        for rx, detail in NOT_JUST:
            for m in rx.finditer(prose):
                findings.append((lineno, m.start() + 1, "construction", detail))

        for m in WORD_RE.finditer(prose):
            w = m.group(0).lower()
            word_counts[w] = word_counts.get(w, 0) + 1
            findings.append((lineno, m.start() + 1, "overused-word", f"overused word '{m.group(0)}'"))

    # drop overused-word hits whose total count is below the threshold
    if min_count > 1:
        keep = {w for w, c in word_counts.items() if c >= min_count}
        findings = [f for f in findings
                    if f[2] != "overused-word" or f[3].split("'")[1].lower() in keep]
        word_counts = {w: c for w, c in word_counts.items() if c >= min_count}
    return findings, word_counts


def main(argv=None):
    ap = argparse.ArgumentParser(description="Flag mechanical AI-writing tells.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--quiet", action="store_true", help="print the summary only")
    ap.add_argument("--gate", action="store_true",
                    help="enforce thresholds and exit non-zero (pre-build use)")
    ap.add_argument("--emdash-per", type=int, default=500,
                    help="B9 budget: one em-dash per N words (default 500)")
    ap.add_argument("--allow", help="file of 'path:line  # reason' exemptions")
    ap.add_argument("--min-count", type=int, default=1,
                    help="only report overused words appearing at least N times (default 1)")
    args = ap.parse_args(argv)

    allowed = set()
    if args.allow:
        for ln in pathlib.Path(args.allow).read_text().split("\n"):
            ln = ln.split("#")[0].strip()
            if ln and ":" in ln:
                f, _, n = ln.rpartition(":")
                allowed.add((f.strip(), int(n)))

    # In gate mode only hard, mechanical rules fail a build. Word-choice and
    # opener findings are advisory: they need human judgment, not a red light.
    GATED = {"semicolon-join", "spelling", "list-spacing", "hyphen-split"}

    total = 0
    gate_fails = 0
    grand_words = {}
    for path in args.files:
        findings, words = scan_file(path, args.min_count)
        findings = [f for f in findings if (path, f[0]) not in allowed]
        findings.sort(key=lambda f: (f[0], f[1]))
        if not args.quiet:
            for line, col, cat, detail in findings:
                print(f"{path}:{line}:{col}: [{cat}] {detail}")
        total += len(findings)
        if args.gate:
            raw = pathlib.Path(path).read_text(encoding="utf-8")
            n, budget = emdash_budget(raw, args.emdash_per)
            if n > budget:
                print(f"{path}: [B9] {n} em-dashes over a budget of {budget}")
                gate_fails += 1
            hard = [f for f in findings if f[2] in GATED]
            if hard:
                gate_fails += 1
        for w, c in words.items():
            grand_words[w] = grand_words.get(w, 0) + c

    print()
    print(f"== summary ==  {total} mechanical tell(s) flagged in {len(args.files)} file(s)")
    if grand_words:
        top = sorted(grand_words.items(), key=lambda kv: (-kv[1], kv[0]))
        print("overused words:", ", ".join(f"{w} x{c}" for w, c in top))
    print("Note: candidates, not verdicts - apply judgment for formal registers.")
    print("Structural & voice tells (symmetry, sandwich, hedging balance, missing")
    print("opinions) are NOT scanned here; review those by reading the text.")
    if args.gate:
        if gate_fails:
            print(f"GATE FAIL: {gate_fails} file(s) violate a hard rule (B9, B18, B17b, structure)")
            return 1
        print("GATE OK")
        return 0
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
