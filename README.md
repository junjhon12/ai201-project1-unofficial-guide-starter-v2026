# The Unofficial Guide

The project is built around the `advice_threads` corpus, where students answer practical campus-life questions in short, opinionated replies. The system retrieves the most relevant reply chunks and answers questions about commuting, roommate issues, laundry timing, office-hours norms, and textbook questions using only those documents.

---

# Unit 1

## What This Does

This project builds a small retrieval system over the `advice_threads` corpus. It loads the thread documents, splits them into reply-sized chunks, embeds them, retrieves the closest matches for a question, and then answers from those chunks while naming the source file. The point is to answer practical student questions from the corpus without inventing facts or guessing when the documents do not cover the topic.

## Chunking Strategy

**Chunk size:** 500 characters
**Overlap:** 80 characters

I chose these numbers because the corpus is made of short, self-contained replies rather than long sectioned guides. Most useful information sits inside one reply, and the reply header plus a few sentences are enough to stand alone. A fixed 800-character chunk was too blunt for this material and would cut across the logic of a reply; a smaller chunk size helps preserve each answer as a complete thought while still keeping a little continuity between adjacent replies.

## Sample Chunks

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.
```

**Chunk 2** — source: `thread_first_gen.txt#1` — produced by: `chunker.py::split_documents`

```
--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.
```

**Chunk 3** — source: `thread_laptop_specs.txt#2` — produced by: `chunker.py::split_documents`

```
--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_parking.txt#1` — produced by: `chunker.py::split_documents`

```
--- reply 2 (21 votes) ---
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.
```

**Chunk 5** — source: `thread_sleep_schedule.txt#1` — produced by: `chunker.py::split_documents`

```
--- reply 2 (37 votes) ---
The library being open until 2am is a trap. It's a resource, not a schedule.
```

## Sample Answer

**Question:** When is laundry actually free in the dorms?

**Answer:**

```
According to thread_laundry_timing.txt, Tuesday and Wednesday mornings are the free laundry times in every building, and Sunday evening is the worst option.
```

**My relevance cutoff:** 0.65

I measured the best distance for five in-corpus questions and five clearly out-of-scope questions. In-corpus results clustered between about 0.39 and 0.60, while out-of-scope questions stayed above 0.72. Putting the threshold at 0.65 sits in the middle of that gap and keeps related questions in while refusing unrelated ones.

| Question | In corpus? | Best distance |
|---|---|---|
| Is a bike worth it for a 20-minute walk commute? | Yes | 0.3948 |
| What should I do if my roommate situation is not working? | Yes | 0.5992 |
| When is laundry actually free in the dorms? | Yes | 0.5872 |
| Does the textbook edition matter for math or physics classes? | Yes | 0.5122 |
| Is it weird to go to office hours without a specific question? | Yes | 0.5168 |
| What is the capital of Mongolia? | No | 0.8967 |
| How do I change the oil in a diesel engine? | No | 0.7211 |
| Who won the 1994 World Cup? | No | 0.9110 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.7818 |
| How do I write a for loop in Rust? | No | 0.8917 |

## How I Used AI

**1.** I asked a model to help me identify a better chunking rule for the advice-thread corpus. It suggested a generic character-based heuristic, but it did not respect reply boundaries, so I changed the implementation to split on the `--- reply ... ---` blocks and kept a small overlap to preserve continuity between adjacent replies.

**2.** I asked for help tightening the relevance-gate logic and checking whether the threshold should be lower or higher. The response suggested a broad range based on intuition, but I compared the actual best distances from the in-corpus and out-of-corpus questions and set the threshold at 0.65 in the gap between those groups instead of guessing.

---

# Unit 2

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
