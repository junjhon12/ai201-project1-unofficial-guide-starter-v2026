# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
The advice-thread corpus is messy: some questions are answered by a single reply,
while others require combining different viewpoints. I set the target at 4 of 5
so one harder question can still be realistic without making the criterion too
lenient.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This corpus is built from discussion threads, so an answer without a source would
be hard to verify. I set this to 5 of 5 because a source citation is part of the
basic trust check for every answer, not just most answers.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
A good cutoff should separate in-corpus questions from clearly unrelated ones. I
picked 4 of 5 because the gate can still fail on one borderline question, but it
needs to be reliable enough to refuse most unsupported topics.

---

## 4. Chunks are self-contained enough to answer from

For at least 4 of my 5 test questions, a single retrieved chunk can stand on its
own as a usable answer without needing the surrounding replies.

**Why this target:**
The advice-thread documents often have multiple replies in one thread, and some
replies are only meaningful when read as a complete thought. I want chunks that
carry a full idea instead of cutting through an argument mid-sentence.

---

## 5. Answers stay grounded in the corpus

For at least 4 of my 5 test questions, the answer contains only information
supported by the corpus and does not add unsupported facts.

**Why this target:**
This corpus includes disagreement and opinion, so unsupported details are a real
risk. I set the target at 4 of 5 because one question may be harder to answer
precisely, but the system should still avoid guessing on the majority of them.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
