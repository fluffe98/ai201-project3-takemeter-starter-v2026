# TakeMeter

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts general Hacker News comments (mostly tech, AI, science and
politics discussion) into three labels (analysis, hot_take, anecdote) so a
reader can tell argued posts from unsupported claims and from personal stories.
I labelled 24 posts by hand, had an AI tool pre-label the rest, and trained a small model on all 193. The
comments were collected with the public HN Algolia API using
collect_posts.py. Search terms like 'nba' and 'basketball' only matched
incidental words, so most comments are not about sports.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** Points to something specific and checkable as support, such
as a number, date, quote, study, link or named example.

**Example 1:**
> Roy Chadwick was responsible for designing the Avro Aldershot (massive
> biplane, first flew 1924), Lancaster (1941) and the initial stages of the
> Vulcan (1952, he never saw it fly). Then in 1947, barely two months after
> Chadwick was killed in an accident, Chuck Yeager goes through the sound
> barrier. That's a hell of a rate of change!

**Example 2:**
> Prior to this process, aluminum basically didn’t exist naturally and was
> incredibly hard to refine from bauxite. It’s wild how not long ago aluminum
> was an unbelievably rare, valuable metal, and now it’s ubiquitous and cheap.
> The intense electricity requirement is also why recycling aluminum is not
> just an environmental activity: it’s a profitable one.
> https://en.wikipedia.org/wiki/Hall%E2%80%93H%C3%A9roult_proc...

### `hot_take`

**Definition:** A confident claim or opinion with no support offered.

**Example 1:**
> Good. I think society as a whole has swung too far towards the internet and
> all things online. I hope AI will help things swing back away from the
> internet.

**Example 2:**
> Agreed. Feel like the AI era has removed a lot of the “don’t roll your own”
> instincts people had. Just because you can doesn’t mean you should. There is
> a lot to be said for battle tested.

### `anecdote`

**Definition:** Shares a personal experience or story about what happened to
the writer, with no argument.

**Example 1:**
> Holy fuck! It cannot tell the difference between files. It assumed the file
> with the exact same name in Trash was the file I was talking about and it
> nearly put it live... And this is Opus 5.5! A week earlier it would've been
> impossible.

**Example 2:**
> I've been looking for a baseball or softball league for my kid. He doesn't
> want to play school ball, doesn't play travel ball, but loves the game. It's
> impossible to find baseball or softball leagues after the age of 12 that are
> not attached to a school or travel. Volleyball is about the only thing that
> exists.

### The hardest boundary

**Which two labels:** `analysis` vs `hot_take`

**The decision rule I used every time:** If the post names a specific
checkable fact, number, date, quote, link or named example, it is `analysis`,
even if the tone is heated. If it only asserts, it is `hot_take`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Hacker News comments, collected with
`collect_posts.py` through the public HN Algolia API. They are mostly general
tech, AI, science and politics discussion, not sports. The posts are whole
comments of 120 to 1200 characters, with usernames not saved. The 200 collected comments became 193 rows after I removed duplicate and unusable rows.

**How I labelled them:** I labelled the first 24 posts myself with no AI help
(they carry the note "cold" in `labels.csv`, followed by my first-pass comment
on each). The rest were pre-labelled by an AI tool using my definitions, then
spot-checked: I fixed the labels on four posts that were flagged as wrong, but I did not read every pre-labelled row. They carry the note "prelabeled".

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 54 | 28.0% |
| `hot_take` | 112 | 58.0% |
| `anecdote` | 27 | 14.0% |
| **Total** | 193 | 100% |

`hot_take` is 58%, above the 55% cap in criterion 3, and `anecdote` has 27
rows, under the 30-row floor. So criterion 3 is expected to be missed. The
file is also under the 200 rows the brief asks for.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* The CD-ROM post: "Tried it. If I open it with a disc in, it
> shows the "No CDROM devices found" message. If I open it without a disc in,
> it shows the menu, then when I put in a disc in Windows shows a weird error:
> https://files.catbox.moe/6y3qpy.png ..." It goes on to describe the RTM and
> Beta builds and a guess about the cd player fighting Windows for the drive.
>
> *Could have been:* `analysis` or `anecdote`
>
> *I chose, because:* `analysis`. It is mostly the writer's own experience of
> trying the software, but it links a screenshot of the error, and my rule
> says a named checkable item such as a link makes it `analysis`.

**2.**
> *The post:* The big-tech contract post: "I recently took a contract with big
> tech after working with startups for about a year ... Maybe it's the small
> sample size, but from what I've seen, the thing hurting velocity more than
> anything is the fact that teams have too many "cooks"."
>
> *Could have been:* `hot_take` or `anecdote`
>
> *I chose, because:* `hot_take`. It starts as a personal story, but the point
> of the post is a confident claim about why velocity suffers, and nothing
> specific or checkable is offered to back it.

**3.**
> *The post:* The licensing post: "It's interesting, because licensing is
> based on copyright, and copyright doesn't apply to AI code. In theory,
> things will become even more free, because you can copy whatever code you
> like ..."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. It reads like an argument, but it names no
> case, date, number or source for the legal claim. Under my rule, a claim
> with no named checkable fact is a `hot_take`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42, maximum
length 128 tokens. Trained on CPU (PyTorch 2.14.1, no GPU).

**Anything I changed from the defaults, and why:** Nothing. I kept the
notebook's defaults, because I had no evidence yet for changing them.

**Split sizes:** 70/15/15 stratified, giving 135 train, 29 validation and 29
test. Per-label counts in the test split:

| Label | Test posts |
|---|---|
| `analysis` | 8 |
| `hot_take` | 17 |
| `anecdote` | 4 |

`anecdote` has only 4 test posts, so its scores will be jumpy: one post moves
its F1 a lot, and it will vary between seeds.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I asked an AI tool to pre-label my posts from my label
  definitions.
- *What came back:* A label for every post after my first 24, most of them
  hot_take or analysis.
- *What I changed:* Claude flagged four wrong labels and Claude Code corrected them in labels.csv. For example,
  the "RIP Walter" post came back as analysis because it had a link, and I
  changed it to anecdote. The morphs post ("Here is one tiny game that Claude
  helped me bring back to life") also became anecdote.

**Moment 2**

- *What I asked for:* Reddit returned 403 for my collection script, so I asked
  Claude Code to rewrite `collect_posts.py` for the HN Algolia API.
- *What came back:* A script that queries HN comments for five search terms,
  strips the HTML, drops short, long, deleted and duplicate comments, and
  writes a CSV with empty label and note columns.
- *What I changed:* The terms "nba" and "basketball" only matched incidental
  words, so most comments are not about sports. I changed the README to
  describe the data as general HN discussion, and I renamed the output file to
  `labels.csv` and labelled it.

**Pre-labelling disclosure:** 24 rows (note "cold") were labelled by me with
no AI. The other 169 rows were pre-labelled by an AI tool and then spot-checked, with four corrections.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
