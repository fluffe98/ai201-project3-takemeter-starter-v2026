# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

Accuracy on the held-out test set is at least 0.60 on all three seeds.

**Why this target:** With three labels, guessing gets about 33%, so 0.60 is
nearly double that. My test split will be about 22 posts, so one wrong post
moves accuracy by about 4.5 points, and the target has to hold on every seed.
That is why I did not pick a higher number.


---

## 2. Per-label performance

Every label has an F1 of at least 0.50 on the held-out test set, on all
three seeds.

**Why this target:** My smallest label will have only about 6 to 8 test
posts, so its F1 will swing a lot between seeds. I set this below the
accuracy target because of that.


---

## 3. Balance

No label is more than 55% of the rows in labels.csv, and each label has at
least 30 rows.

**Why this target:** The project cap is 70%, but at that level a model can
score well by guessing the biggest label. With 150 rows, 30 per label gives
about 4 to 5 test posts, which is the least I can measure anything on.


---

## 4. Agreement with staff

On the 30-post staff set in unit 6, my labels agree with staff on at least
21 of 30 (70%).

**Why this target:** I am labelling under the staff taxonomy, not my own,
and some of the 30 were picked because they are ambiguous. 70% would show
that I applied written rules consistently without expecting perfection.


---

## 5. Better than the baseline

The trained model's macro F1 is at least 0.05 higher than the baseline's on
the same test posts.

**Why this target:** The point of fine-tuning on my data is to beat a model
that has seen none of it. Five points is a small margin that still shows the
training added something. With a test set this small it could easily miss.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
