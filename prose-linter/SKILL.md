---
name: prose-linter
description: >
  Check prose for the mechanical tells of AI writing, and fix them. Use this
  whenever generating or editing prose meant for people (documents, reports,
  markdown, README/docs, emails, proposals, deliverables) and whenever asked to
  "de-AI" text, make writing sound human or natural, remove AI tells, or review a
  draft for AI-generated patterns. Covers the patterns catalogued in Wikipedia's
  "Signs of AI writing": inflated-importance claims, name-dropping, vague sources,
  formulaic sayings, fake alternatives, passive voice, nominalisation, symmetry,
  bullet overuse, missing opinions, filler openers, semicolon and em-dash overuse,
  and more. Includes voice matching, false-positive guidance, a mechanical CLI
  scanner (scripts/scan.py) that can gate a build, and a-priori guidance for
  writing human from scratch.
---

# Humanize Prose

Goal: text a reader cannot flag as AI-written.

---

## Step 0 — Voice matching (do this first)

If you have a writing sample from the author, read it before touching anything else. Note:

- Sentence length range (short punchy? long periodic?)
- Whether they use contractions
- How they start paragraphs (anecdote? claim? question?)
- Punctuation habits (serial comma? em-dash? parentheticals?)
- Register (formal? casual? blunt?)

Apply those habits throughout the rewrite. A text can be free of every pattern below and still feel wrong if it doesn't sound like the author.

---

## The 36 patterns

### Category A — Content

#### A1. Inflated-importance claims

Asserting that something is revolutionary, unprecedented, or game-changing without evidence.

**Before:** This framework represents a paradigm shift that will revolutionize how organizations think about data.
**After:** This framework changes how organisations structure their data pipelines.

Watch for: revolutionary, unprecedented, paradigm shift, game-changing, transformative, groundbreaking, landmark.

---

#### A2. Name-dropping without substance

Dropping famous names, companies, or concepts that add prestige but no insight.

**Before:** As Aristotle understood, and as Google has demonstrated, the key to success is iteration.
**After:** Rapid iteration shortens feedback loops and reduces the cost of mistakes.

Watch for: name + "understood", "recognized", "has shown", "has demonstrated" when the name adds nothing to the claim.

---

#### A3. Shallow -ing opener phrases

Opening a sentence or paragraph with a gerund phrase that claims impact without showing it.

**Before:** Revolutionizing the way teams collaborate, the platform enables real-time co-editing.
**After:** The platform lets teams edit the same document simultaneously.

Watch for: Revolutionizing…, Transforming…, Redefining…, Empowering…, Enabling… at sentence start.

---

#### A4. Vague attribution

Citing "experts", "studies", "research", or "many" without a source, date, or number.

**Before:** Studies show that remote workers are more productive. Experts agree the trend will continue.
**After:** A 2023 Stanford survey of 16,000 workers found remote employees completed 13% more tasks per shift.

Watch for: studies show, research suggests, experts agree, many believe, it is widely accepted.

---

#### A5. False balance

Presenting two sides as equally valid when one is better-supported, or hedging a clear conclusion.

**Before:** Some argue that caching improves performance; others contend it introduces complexity. Both views have merit.
**After:** Caching improves read performance significantly; the added complexity is worth it for read-heavy workloads.

Watch for: some argue…others contend, on one hand…on the other, both perspectives are valid.

---

#### A6. Hedged universals

Qualifying every claim to the point of saying nothing.

**Before:** In most cases, this approach generally tends to work relatively well for many common scenarios.
**After:** This approach works well for read-heavy workloads with stable schemas.

Watch for: in most cases, generally, typically, often, tends to, relatively, somewhat, for many.

---

#### A7. Overpromising scope

Claiming a piece of writing covers more than it does.

**Before:** This comprehensive guide covers everything you need to know about Kubernetes networking.
**After:** This guide covers pod-to-pod networking and NetworkPolicy basics.

Watch for: comprehensive guide, everything you need to know, complete overview, all aspects of, ultimate resource.

---

#### A8. Missing concrete details

Claims with no numbers, dates, names, places, or examples to anchor them.

**Before:** The system handles large volumes of data efficiently across multiple regions.
**After:** The system processes 4 million events per second across three AWS regions (eu-west-1, us-east-1, ap-southeast-1).

Fix: add at least one specific figure or named example per factual claim.

---

### Category B — Language and grammar

#### B9. Em-dash overuse

Using — for every parenthetical aside, turning a stylistic tool into a crutch.

**Before:** The approach — which was developed over several years — has proven — in most trials — to be effective.
**After:** The approach, developed over several years, has proven effective in most trials.

Rule: one em-dash pair per paragraph maximum. Bullet lists are not exempt — if more than one bullet in a list contains an em-dash pair, convert the extras to parentheses. Chapter-wide: if em-dash pairs appear in most paragraphs, the density is too high even when each individual use is grammatically valid. Use commas or parentheses for the rest.

---

#### B10. Passive voice overuse

Removing the agent from every sentence, producing a ghostly, agentless text.

**Before:** It was determined that the threshold should be lowered. Errors were logged and the report was generated.
**After:** The team lowered the threshold after reviewing error rates. The pipeline logs errors and generates a daily report.

Watch for: it was determined, it should be noted, it has been found, errors were, the report was.

---

#### B11. Nominalisation

Turning verbs into nouns, inflating sentence length and removing dynamism.

**Before:** We need to make a decision on the implementation of the new authentication method.
**After:** We need to decide how to implement the new authentication method.

Watch for: make a decision → decide; provide an explanation → explain; give consideration → consider; reach a conclusion → conclude; have a discussion → discuss.

---

#### B12. Stacked compound adjectives

Piling three or more hyphenated adjectives before a noun.

**Before:** A high-quality, cost-effective, enterprise-grade, cloud-native, scalable solution.
**After:** A scalable, enterprise-grade cloud solution — and cost-effective at volume.

Rule: two compound adjectives maximum before a noun. Restructure the rest.

---

#### B13. Doubled hedges

Combining two hedging words that mean the same thing.

**Before:** This may potentially cause issues. The system could possibly experience downtime.
**After:** This may cause issues. The system could experience downtime.

Watch for: may potentially, could possibly, might perhaps, seems to appear, tends to usually.

---

#### B14. Formulaic transitions

Opening every paragraph with the same set of linking words.

**Before:** Furthermore, the system is scalable. Moreover, it is secure. Additionally, it integrates with existing tools.
**After:** The system is scalable and secure. It integrates with existing tools through standard OAuth flows.

Watch for: Furthermore,; Moreover,; Additionally,; In addition,; It is worth noting that; It is important to highlight. Replace with a direct sentence or a real causal connector (because, so, which means).

---

#### B15. Subordinate clause padding

Adding clauses that restate what the main clause already says.

**Before:** The architecture is modular, which is to say that each component operates independently, meaning that changes to one do not affect the others.
**After:** The architecture is modular: each component is independent.

Watch for: which is to say, in the sense that, what this means is, by which I mean.

---

#### B16. Parallel list overuse

Forcing every sentence in a list into the exact same grammatical structure, making the text sound robotic.

**Before:**
- Ensures that data is processed correctly.
- Ensures that logs are stored securely.
- Ensures that errors are handled gracefully.

**After:**
- Processes data correctly.
- Stores logs securely in S3 with AES-256.
- Handles errors by retrying three times, then dead-lettering.

---

#### B17. Oxford-comma hyper-consistency

Applying punctuation rules with machine-like uniformity across an entire document, even where a human would make exceptions for rhythm.

Fix: vary sentence structure enough that punctuation decisions look editorial, not algorithmic.

---

#### B17b. Spelling dialect consistency

Mixing British and American spellings inside one document reads as text assembled from
several sources rather than written by one person. It is one of the easier tells to spot
and one of the easiest to fix.

**Default to American English** unless the project states otherwise: `-ize`/`-ization`,
`-or`, `-er`, single `l` before a suffix.

| Use | Not |
|---|---|
| normalization, optimizer, tokenizer, quantization | normalisation, optimiser, tokeniser, quantisation |
| behavior, color, favor, neighbor, labor | behaviour, colour, favour, neighbour, labour |
| center, meter, fiber | centre, metre, fibre |
| modeling, labeled, canceled | modelling, labelled, cancelled |
| analyze, paralyze, practice (verb) | analyse, paralyse, practise |
| license, defense, offense, toward, gray | licence, defence, offence, towards, grey |

**Never change:**

- **Published titles and proper nouns.** A paper called *Layer Normalization* keeps its
  spelling even in a British-English document, and vice versa. So do product names
  (Arize, Optimisely) and quoted material.
- **Code**: identifiers, APIs and string literals (`normalize()`, `chunk_size`,
  `tokenizer.json`). Only prose is in scope.
- **Words that merely look like the pattern**: *exercise, promise, surprise, precise,
  advertise, supervise, comprise, otherwise, pairwise, noise, raise, expertise* are
  spelled the same either way. A naive `-ise` → `-ize` substitution mangles these into
  *advertizing*, *surprizing*, *unsupervized*. Match on whole words, not prefixes.

**To override the default**, state the dialect in the project's `CLAUDE.md`. The rule is
consistency first; the direction is a project decision.

---

#### B18. Semicolon overuse

Joining independent clauses with a semicolon instead of ending the sentence. AI models favour semicolons to signal sophistication, but human writers usually just use a period.

**Before:** The deployment completed successfully; all services are now running.
**After:** The deployment completed successfully. All services are now running.

**Before:** The configuration is straightforward; you only need to set three environment variables.
**After:** The configuration is straightforward. Set three environment variables: HOST, PORT, and TOKEN.

Rule: replace semicolons that join independent statements with a period. Contrasting pairs use a comma, not a semicolon ("The API is fast, the UI is not"). The only legitimate use for a semicolon in prose is a list whose items themselves contain commas ("Paris, France; London, UK; Berlin, Germany").

**Code block comments:** `#` and `//` prose comment lines inside fenced code blocks are still prose. Fix B18 violations in comment lines. Only actual code syntax — operators, statements, language constructs — is exempt.

---

### Category C — Style

#### C19. Symmetrical section lengths

Every section is the same number of sentences or words, making the document feel templated.

Fix: let important sections breathe. A critical caveat can be one sentence. A complex procedure can be ten. Don't pad short sections or trim long ones to match.

---

#### C20. Three-item list lock

Every list has exactly three items — because three feels "balanced". Add a fourth or drop to two when the content calls for it.

**Before:** There are three key benefits: performance, reliability, and scalability.
**After:** There are four constraints: latency budget, throughput ceiling, error budget, and cost per GB.

---

#### C21. Sandwich structure

Every section opens with a statement, elaborates, and closes by restating the opening. The closing restatement adds nothing.

**Before:** Caching is critical for performance. [body] In summary, caching plays a critical role in system performance.
**After:** Remove the summary sentence. The body already said it.

---

#### C22. Over-formatting

Bolding or italicising every key term, producing emphasis inflation where nothing stands out.

Fix: reserve bold for terms the reader must not miss. One or two per section maximum. Remove italic from every word that isn't a title, foreign term, or deliberate stress.

---

#### C23. Bullet overuse

Converting flowing argument into disconnected bullet fragments, losing causality and reasoning.

**Before:**
- The system uses microservices.
- This improves scalability.
- Teams can deploy independently.

**After:** The system's microservice architecture lets teams deploy independently — a component's release cycle no longer blocks the rest.

Rule: if bullets are fewer than five items with no internal logic between them, consider whether a sentence would work better.

---

#### C24. Absence of opinion

Never taking a position. Presenting options without a recommendation. Ending analysis with "it depends".

**Before:** Both approaches have trade-offs. The right choice depends on your specific situation.
**After:** For read-heavy workloads with stable schemas, option A is faster and simpler. Option B is worth the overhead only if you expect frequent schema changes.

---

#### C25. Uniform sentence rhythm

Every sentence within a passage is the same length — medium-long. Readers stop noticing individual sentences.

Fix: vary length deliberately. Short sentences land hard. Use them for conclusions, warnings, and transitions. Save long sentences for explanation and qualification.

---

#### C26. No concrete anecdote or example

Abstract claims with no illustrative instance. The text could describe anything.

**Before:** Organisations that adopt this approach see significant improvements in team velocity.
**After:** After the payments team at Monzo adopted trunk-based development, their lead time dropped from 11 days to 2.

---

#### C27. Motivational sign-off

Ending with an encouraging statement about the future rather than a conclusion.

**Before:** By embracing these principles, your team can unlock new possibilities and achieve lasting success.
**After:** [Nothing. End after the last substantive point.]

---

#### C28. Header for everything

A new H2 or H3 every two or three sentences, turning prose into a slide deck.

Fix: use headers to mark genuine topic shifts, not to break up every paragraph. Three to five paragraphs under one header is normal. Running prose with no header is fine.

---

### Category D — Filler and hedging

#### D29. Filler openers

Starting a response, section, or paragraph with a phrase that says nothing.

**Before:** It's important to note that the system requires authentication. It goes without saying that security matters.
**After:** The system requires authentication. Configure OAuth 2.0 before deploying.

Watch for: It's important to note that; It's worth mentioning that; It goes without saying; Needless to say; First and foremost; Last but not least; It should be noted that.

---

#### D30. Redundant affirmations

Agreeing or reassuring before answering, adding no information.

**Before:** Absolutely! That's a great question. Certainly, I can help with that.
**After:** [Answer directly.]

Watch for: Absolutely!; Certainly!; Of course!; Great question!; Sure thing!; Happy to help!

---

#### D31. Formulaic sayings

Using idioms and clichés to sound relatable, when they sound lazy instead.

**Before:** At the end of the day, you need to think outside the box and leverage synergies.
**After:** The real constraint is deployment frequency, not tooling.

Watch for: at the end of the day; think outside the box; leverage synergies; move the needle; take it to the next level; circle back; low-hanging fruit; deep dive.

---

#### D32. Fake alternatives

Presenting a binary that covers everyone, thereby addressing no one.

**Before:** Whether you're a complete beginner or a seasoned expert, this guide has something for you.
**After:** This guide assumes familiarity with Docker and basic Kubernetes concepts.

Watch for: Whether you're a [X] or a [Y]...; No matter your [level/background/experience]...

---

#### D33. Scope disclaimers

Hedging a document's coverage rather than simply writing what it covers.

**Before:** While this is not an exhaustive list, and results may vary depending on your specific environment...
**After:** [Write what the document covers. If it's incomplete, say what's missing specifically.]

Watch for: while this is not exhaustive; results may vary; your mileage may vary; this is just one approach; there are many ways to.

---

#### D34. Emphasis inflation

Using intensifiers so frequently they cancel each other out.

**Before:** This is a very important, extremely critical, highly significant issue that is incredibly urgent.
**After:** Fix this before the next deployment — it corrupts records silently.

Watch for: very, extremely, incredibly, highly, truly, really, absolutely as adjective/adverb modifiers.

---

#### D35. Meta-commentary

Describing what the text is about to do rather than doing it.

**Before:** In this section, we will discuss the key considerations you need to be aware of when configuring the system.
**After:** Configure the system with three settings: [list].

Watch for: In this section we will; As mentioned above; As I explained earlier; This section covers; The purpose of this section is to.

---

#### D36. Soft landing

Ending with a social pleasantry instead of a conclusion.

**Before:** I hope this helps! Feel free to reach out if you have any questions. Don't hesitate to let me know!
**After:** [End after the last substantive sentence.]

Watch for: I hope this helps; feel free to reach out; don't hesitate to ask; let me know if you need anything; happy to clarify.

---

### Category E — Advanced structural tells

#### N37. Negation-antithesis

Stating what something is *not* before stating what it *is* — a hollow rhetorical frame.

**Before:** It's not just a tool — it's a movement. This isn't simply a fix; it's a philosophy.
**After:** It's a movement. It's a philosophy.

Watch for: "It's not X — it's Y", "This isn't just X, it's Y", "X isn't about Y; it's about Z", "Less X, more Y", "Where X used to Y, it now Z", "What began as X became Y." Delete the negated half; state the positive claim only.

---

#### N38. Participial opener

Opening a sentence with a participial phrase as a structural tic rather than a natural transition.

**Before:** Having established the baseline, we can now measure progress. Drawing on decades of research, the authors conclude...
**After:** We can now measure progress against the baseline. The authors conclude...

Watch for: sentences beginning with *Having [verb-ed]*, *Drawing on*, *Armed with*, *Built on*, *Designed to* when the pattern repeats across paragraphs. Convert to a main clause with a conjunction.

---

#### N39. From-to ranging

Spanning a range to signal comprehensiveness while saying nothing specific.

**Before:** From startups to enterprises, every organisation benefits. From onboarding to offboarding, the system handles it all.
**After:** Name one concrete instance. Cut the spanning frame.

Watch for: "From X to Y, ...", "Everything from A to B", "across the spectrum from X to Y."

---

#### N40. Rhetorical question + immediate answer

Asking a question then answering it in the next sentence — adding words without information.

**Before:** So what does this mean? It means the model can generalise.
**After:** The model can generalise.

Watch for: "So what does this mean?", "But what is X?", "Why does this matter?", "How does this work?" followed immediately by the answer. Delete the question; keep only the answer.

---

#### N41. Colon-then-reveal

Using a colon for dramatic effect in a short "setup: payoff" structure.

**Before:** The problem: nobody read it. One word: trust. The result: a 40% drop.
**After:** Nobody read it. The result was a 40% drop.

Watch for: short clause + colon + short dramatic payoff as a repeated sentence shape. Rewrite as a full clause.

---

#### N42. Synonym cycling

Referring to the same technical object by different names to avoid repeating a word, breaking terminology consistency.

**Before:** The attention mask controls visibility. The masking matrix... The visibility filter...
**After:** Pick one term — "attention mask" — and use it throughout.

Rule: pick the canonical term for each technical concept and use it consistently. Do not synonym-swap to avoid repetition. Applies to technical terms only; ordinary words can vary naturally.

---

#### N43. Explanatory chain

Chaining causal sentences with "This means / allows / enables / ensures / provides" where one sentence would do.

**Before:** X improves caching. This allows the service to reduce latency. This, in turn, helps improve response times.
**After:** X improves caching and reduces response latency.

Watch for: consecutive sentences using "This means that...", "This allows...", "This enables...", "This ensures...", "This, in turn, ...". Collapse to a single sentence with a direct causal verb.

---

#### N44. Over-explanation

A claim followed by a paraphrase, followed by an example that merely restates the claim — three sentences saying one thing.

**Before:** The model is non-deterministic — meaning its outputs vary across runs — so the same input can produce different results each time.
**After:** The model is non-deterministic: the same input can produce different outputs.

Rule: if a sentence and its "that is, ..." / "in other words, ..." / "meaning that..." rider say the same thing, drop the rider and keep the cleaner version.

---

## What not to flag

Apply these 17 guards before marking anything as an AI tell.

1. **Formal register legitimately uses formal words.** "Ensure", "robust", "comprehensive", "facilitate" are fine once per section in a technical spec. Flag repetition and combination, not presence.
2. **Subject-matter terminology is not jargon.** "Scalability", "fault tolerance", "idempotent" are precise terms, not inflation.
3. **Short lists are not always AI.** A three-item list is fine when there are exactly three items.
4. **Passive voice has legitimate uses.** Scientific and legal writing uses passive deliberately. Flag overuse, not any use.
5. **Transitions are sometimes needed.** "However" and "because" are causal connectors, not filler. Only flag the formulaic set (Furthermore, Moreover, Additionally, In addition).
6. **Uniform structure is sometimes appropriate.** API reference documentation, changelogs, and release notes are intentionally uniform.
7. **Hedging is appropriate in genuine uncertainty.** "This may cause issues under high load" is accurate, not evasive, if high-load behavior is genuinely uncertain.
8. **An absence of anecdotes is not a tell.** Technical reference documentation does not need anecdotes.
9. **Bold and italic serve accessibility.** Keyboard shortcuts, warnings, and first-use of defined terms warrant emphasis.
10. **Oxford comma or no Oxford comma — pick one.** Consistency in a document is correct usage, not an AI pattern.
11. **Nominalisation is sometimes preferred.** Legal and policy documents use nominalisations by convention.
12. **Numbered lists imply order.** Do not convert ordered steps to prose to avoid "bullet overuse".
13. **Em-dashes are editorial punctuation.** One pair per paragraph is the maximum, not the target. Flag when most paragraphs each contain a pair — that density is an AI tell even when each individual use is grammatically valid. Do not flag a single isolated pair.
14. **"Furthermore" once is fine.** Flag it when it opens three consecutive paragraphs.
15. **High-intensity words can be accurate.** "Critical" is accurate for a security vulnerability. "Extremely urgent" is not inflation if the deadline is real.
16. **Do not strip the author's voice.** If the writing sample uses a particular construction consistently, that is the author's style — preserve it.
17. **Semicolons in comma-lists are correct.** "Paris, France; London, UK; Berlin, Germany" uses semicolons as a higher-level list separator. Only flag semicolons that join independent clauses where a period would work.

---

## Human details to keep

When you encounter these in the source text, preserve them even if they pattern-match to something above:

- Specific numbers, dates, names, and places ("on 14 March", "in the Frankfurt cluster", "3.2 million rows")
- Actual quotes from real people with attribution
- Concrete anecdotes with enough detail to be verifiable
- Domain-specific idioms used accurately in context
- The author's signature constructions (identified from the writing sample)
- Deliberate rhetorical repetition used for emphasis (anaphora)
- Short sentences used for deliberate punch
- Incomplete sentences used as stylistic choice

---

## Vocabulary reference

Use this alongside the scanner. Three or more Tier A words in 200 words of prose is near-conclusive; single instances in technical registers may be accurate.

### Tier A — near-diagnostic in clusters

`delve`, `tapestry`, `realm`, `beacon`, `testament`, `crucible`, `embark`, `unlock`, `harness`, `illuminate` (figurative), `underscore`, `navigate` (figurative), `foster`, `cultivate`, `usher`, `resonate`, `elevate`, `empower`, `amplify`, `bolster`, `spearhead`, `odyssey`, `watershed`, `labyrinth`, `mosaic`

### Tier B — strong signal on density

`robust`, `seamless`, `intricate`, `nuanced`, `multifaceted`, `holistic`, `comprehensive` (unsupported), `meticulous`, `pivotal`, `crucial`, `vital`, `transformative`, `groundbreaking`, `cutting-edge`, `unprecedented`, `myriad`, `plethora`, `pertinent`, `compelling`, `invaluable`, `paramount`, `formidable`, `vibrant`, `stark`, `sobering`, `striking`

### Tier C — intensifiers (flag on repetition)

`truly`, `remarkably`, `seamlessly`, `incredibly`, `deeply`, `genuinely`, `fundamentally`, `undeniably`, `notably`, `significantly`, `substantially`, `particularly`, `essentially`, `ultimately`, `crucially`, `importantly`

### High-value substitutions

| AI phrasing | Plain equivalent |
|---|---|
| `utilize` | `use` |
| `leverage` (verb) | `use` |
| `individuals` | `people` |
| `ensure` (repeated) | `make sure` or restructure |
| `in order to` | `to` |
| `due to the fact that` | `because` |
| `provides the ability to` | `can` |
| `offers the capability to` | `can` |
| `is designed to` (describing actual behavior) | say what it does |
| `with regard to` | `about` |
| `at this point in time` | `now` |
| `in the event that` | `if` |

Only apply when semantically equivalent. Never replace technical identifiers.

---

## Quality gate

Before declaring any humanization pass complete:

1. Run `scan.py --min-count 2` **before** editing and note the total hit count.
2. Apply fixes.
3. Run `scan.py --min-count 2` again and compare.
4. Pass criteria:
   - **B18 (semicolons):** zero hits remaining.
   - **B9 (em-dash):** total `—` count in the file is under one per 500 words of prose.
   - **Overused words:** no Tier A or B word appears more than twice in the chapter.
5. If criteria are not met, continue editing before reporting completion.

Do not report a pass as complete based on edit count alone.

---

## Mechanical scanner (scripts/scan.py)

The `scan.py` script catches word- and phrase-level tells automatically. Run it before and after a manual rewrite pass to catch what pattern review alone misses.

```bash
# Full scan — all categories
python3 ~/.claude/skills/prose-linter/scripts/scan.py FILE.md

# Only words that repeat (reduces false positives in long docs)
python3 ~/.claude/skills/prose-linter/scripts/scan.py FILE.md --min-count 2

# Summary only (for CI gates)
python3 ~/.claude/skills/prose-linter/scripts/scan.py FILE.md --quiet
```

Output format: `file:line:col: [category] detail`. Exits non-zero when anything is flagged, so it works as a pre-publish gate in CI.

The scanner covers typographic tells (em-dash, curly quotes, ellipsis character), semicolons joining independent clauses (B18), and overused words/phrases not fully covered by the prose patterns above. It is a complement to the 36 patterns, not a replacement.

---

## Writing from scratch (a-priori)

Before and while drafting, apply the 36 patterns as construction rules, not just as an audit checklist. The condensed version for fast reference:

1. No filler opener. Start with the substance.
2. Plain `-`, straight quotes `"` `'`, `...` — not `—`, `"`, `'`, `…`.
3. Cut overused words and empty phrases ("It's important to note", "This ensures that"). State the point.
4. No "not just X, but Y" / "not only…but also" constructions.
5. Vary section and paragraph length. Let some be short.
6. Take positions. Prefer "X is better because Z" over "some say X, others Y".
7. Use transitions only when the logic needs one.
8. No motivational sign-off. Just end.
9. Contractions are fine and read as human.
10. Use periods to end independent statements — not semicolons.

Then run the mechanical scanner on your draft before delivering.

---

## Composing with document generation

For any document built from Markdown: write and clean the Markdown with this skill first, then convert to its final format. Conversion handles typography and layout in the output file. This skill handles the wording and structure in the source, which is where both are easiest to fix.

---

***This file is licensed CC BY-SA 4.0**, not MIT like the rest of this repository, because it
adapts the selection and arrangement of Wikipedia's catalog. See NOTICE.*

*Based on [Blader's Humanizer](https://github.com/blader/humanizer) (MIT). Patterns derived from Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). To update this skill, fetch the latest SKILL.md from the upstream repository and reconcile changes against the scanner section, a-priori section, and the document-generation pairing note above.*
