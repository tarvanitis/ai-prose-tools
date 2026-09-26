# Book Architecture

What a book's architecture record should contain, and what to check it against.

Audit the architecture before auditing anything smaller. A chapter written beautifully in the wrong
place is still in the wrong place, and renumbering late is expensive.

## What to check

- **Front matter exists and is reader-facing.** A repository README is not a preface. Look for a
  title page, a copyright and edition note, a preface saying who the book is for, and a "how to
  read this book".

- **Back matter exists.** Glossary, bibliography, index. Reference material belongs at the back,
  not interrupting the linear read.

- **Parts are balanced.** One Part carrying nine chapters while another carries two usually means
  the spine was split by source file rather than by idea.

- **There is an arc.** Chapters should progress, each depending on what came before. A sequence
  that could be read in any order is a reference collection, not a book.

- **Foundations are taught once.** Anything explained from scratch in three chapters should be
  explained in one and referenced twice.

- **Every source is accounted for.** If the book was assembled from existing material, track the
  mapping so nothing is silently dropped or duplicated.

The rest of this file shows each of those as a worked example, taken from a 20-chapter technical
book on transformers and large language models. **Read the examples for their shape, not their
content.** The subject is irrelevant. What transfers is how the Parts balance, how sources map to
chapters, and how repeated foundations get consolidated.

## Worked example: Parts and Chapters

**Front matter**

- Half-title / title page
- Copyright & edition note (carry the dated "as of" snapshot, versions churn)
- Preface: who this book is for; what you'll learn; the three lenses; how to read this book
- (Optional) Foreword

**Part I. Foundations**

- Ch 1. What Is a Transformer?: history, the sequential-processing problem, the "whole page vs.
  keyhole" insight  *(from 02: Introduction)*

- Ch 2. The Mathematics You'll Need: vectors, matrices, matmul, dot product, softmax, probability,
  gradients, entropy/KL. **This is the single canonical treatment**. Later chapters reference it
  instead of re-deriving.  *(from 03, absorbing the duplicated math in 01/02)*

**Part II. How Transformers Work**  *(the spine, splits the large 02 file into digestible chapters)*

- Ch 3. From Text to Numbers: Tokenization & Embeddings  *(02: Tokenization, Token Embeddings)*
- Ch 4. Position: How a Model Knows Word Order  *(02: Positional Encoding, RoPE)*
- Ch 5. Attention: The Core Mechanism  *(02: Self-Attention, Multi-Head, GQA/MQA/MLA)*
- Ch 6. The Transformer Block and Depth  *(02: block + FFN, stacking layers)*
- Ch 7. Inside a Trained Model: Mechanistic Interpretability  *(02: circuits)*
- Ch 8. Generating Text: Inference and the Next Token  *(02: inference, KV cache, making it fast)*
- Ch 9. The Full Architecture and Modern Trends  *(02: putting it together, MoE, hybrid SSM, current trends)*

**Part III. Building One**

- Ch 10. Building a GPT from Scratch in PyTorch  *(04 Part I)*
- Ch 11. Every Component, Annotated  *(04 Part II: reconcile the acknowledged overlap with Ch 10)*

**Part IV. Training and Alignment**

- Ch 12. The Training Pipeline at a Glance  *(05: overview)*
- Ch 13. Pre-training  *(05: ①)*
- Ch 14. Supervised Fine-Tuning  *(05: ②)*
- Ch 15. Learning from Human Preferences: Reward Models, RLHF/PPO, and DPO  *(05: ③④⑤)*
- Ch 16. Training Reasoning Models: GRPO and RLVR  *(05: ⑥)*
- Ch 17. Evaluating Language Models  *(05: ⑦)*

**Part V. Applications**

- Ch 18. Retrieval-Augmented Generation  *(06 Part 1)*
- Ch 19. Building AI Agents  *(06 Part 2)*
- Ch 20. Running Models Offline  *(06 Part 3)*

**Back matter**

- Appendix A: Glossary (163 terms)  *(from 01, kept by category or alphabetized)*
- Appendix B: Modern LLM Specifications & Evolution, 2017→2026  *(from 02 Appendices B & C)*
- Bibliography / Further Reading  *(from 99 "Curated Further Reading" only)*
- Index

This yields ~20 chapters in 5 Parts and evens out chapter weight: the 3,000-line fundamentals file
becomes seven chapters. The short 595-line training file becomes six brief chapters grouped into one
Part. The two oversized reference files (glossary, applications) are rebalanced (glossary → appendix).

## Worked example: source to chapter mapping

Where a book is assembled from existing material, keep a table like this and audit against it. Its
job is to make omission and duplication visible. Every source must appear exactly once in the
"Goes to" column, and every chapter must have a source or be marked as new writing.

| Source file | Goes to | Notes |
|---|---|---|
| `01-terminology.md` | Appendix A (Glossary) | Move out of the linear read; keep `*Related:*` as glossary see-alsos, but link the *first* mention of each term from its chapter to the glossary entry. |
| `02-fundamentals.md` | Ch 1, Ch 3–9 | The book's spine. Its own Appendix A glossary is dropped (superseded by book Appendix A); Appendices B/C → book Appendix B. |
| `03-mathematics.md` | Ch 2 | Becomes the canonical math chapter. |
| `04-implementation.md` | Ch 10–11 | Deduplicate Part I/Part II overlap; fix source typos ("architecures", "geneally"). |
| `05-training.md` | Ch 12–17 | Cleanest linear source already. |
| `06-applications.md` | Ch 18–20 | Strip the emoji sign-off and the version/hardware block → move dated specifics into a boxed "as of" note. |
| `99-references.md` | Bibliography | Keep only "Curated Further Reading"; drop the FEDORA/AI browser export, localhost logins, and duplicate tutorial links. |

## Worked example: deduplication plan

**The rule is the part that transfers:** the first full treatment stays, every later occurrence
becomes a one-line reminder plus a cross-reference. Build the equivalent list for your own book by
grepping for each foundational concept and seeing how many places define it.

In the example book these were each taught from scratch in several source files. They were
consolidated into Ch 2 and referenced from everywhere else:

- Vectors, matrices, matrix multiplication: 01, 02, 03 → **Ch 2**
- Dot product: 01, 02, 03 → **Ch 2** (attention chapter references it)
- Softmax: 01, 02, 03 → **Ch 2** (attention + training reference it)
- Cross-entropy, KL divergence: 01, 02, 03, 05 → **Ch 2** (training references it)
- Tokenization / BPE, 01, 02, 04 → **Ch 3** (implementation references it)
- Glossary duplication: 02's Appendix-A glossary overlaps all of 01 → keep only **Appendix A**

Rule: the first full treatment stays. Every other occurrence becomes a one-line reminder plus a
cross-reference ("Recall from Ch 2 that softmax turns a vector of scores into probabilities…").

## Front-matter templates

These transfer directly to any technical book.

**Preface**: cover, in order:

1. The problem the book solves and who it's for (states the no-prior-knowledge→expert-internals arc).
2. What the reader will be able to do by the end, stated as capabilities rather than topics.
3. Any recurring devices the book uses: analytical lenses, callout types, worked-example
   conventions. Explain them once, here, so chapters don't each re-introduce them.

4. How to read this book: linear vs. as-reference; which Parts a practitioner can skip to; the
   glossary and math chapter as anytime look-ups.

5. A dated edition note: "Model names and sizes are a snapshot as of YYYY-MM-DD. The durable
   material is the mechanics." (Verify current versions from vendor pages before publishing.)

**Chapter opener / closer templates** live in `chapter-workflow.md`.

## Manuscript layout on disk

One file per chapter, one H1 per file, Parts inserted at assembly time. Where the book is converted
from existing material, build alongside the source rather than in place, so the original stays
intact until the conversion is proven.

Example layout:

```
book/
  frontmatter/00-preface.md
  part-1/ch-01-what-is-a-transformer.md ... ch-02-mathematics.md
  part-2/ch-03-... .md
  ...
  backmatter/appendix-a-glossary.md
  backmatter/bibliography.md
  book.md            # assembled manuscript (generated)
```

One file per chapter (H1 = chapter title). Parts are grouping headers inserted at assembly time.
See `production.md` for assembly and rendering.
