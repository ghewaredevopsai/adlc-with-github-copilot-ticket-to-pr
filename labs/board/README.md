# The board — remote delivery

In a room, this is a whiteboard that stays up for two days. Online, it is a **GitHub issue per
participant** in a public repository, and it works better than the whiteboard because nobody has to
read someone else's handwriting from a webcam.

Your trainer posts the link to the board repository on Day 1. It holds this file and the tally form,
`.github/ISSUE_TEMPLATE/tally.yml`, which you open once.

## Why an issue per participant, not a shared file

A shared file means merge conflicts — thirty people editing one table on a Tuesday morning is a
guaranteed twenty minutes lost to git, during the labs, which is exactly the time the course cannot
spare. One issue per person has none of that: no write access to the repo is needed, no branches, no
conflicts, and anyone with a GitHub account can open one.

It also matches what the board is *for*. The board is **public and unedited**, and it stays up until
the capstone, because the closing comparison is against those exact numbers **including the
embarrassing ones**. An issue thread is append-only by nature: the body holds
the current tally, and each row is also posted as a comment when it lands, so the history of what was
claimed and when is visible. Editing a number later leaves a visible edit mark. That is the point.

## How it runs

**Day 1, before Lab 1.1.** Each participant opens one issue from the **Workshop tally** template and
titles it with their name. That is the whole setup.

**After each measured run.** They update the table in the issue body, and post a comment with the row
they just filled. Four rows across two days:

| Run | When |
|---|---|
| **1.1** — unprepared repository (GB-142) | Module 1 |
| **2.2** — your knowledge in the repository (GB-151) | Module 2 |
| **3.2** — the prompt A/B | Module 3, a **pass rate**, not the six counters |
| **capstone** — the full pipeline (GB-186) | Module 8 |

**At the capstone debrief.** The trainer reads the board — every capstone row next to its 1.1 row,
by category rather than by headline.

## The rule that makes it worth anything

Report what you measured, either way. A run that got worse is a finding and goes on the board
unchanged. Module 1 slide 10 makes that promise to the room; the board is where it is kept.

## Reading rows 1.1 and 2.2 against each other

These two are the comparison the course rests on, and they are matched deliberately: same repository,
comparable ticket size, and the **same 35-minute working window**. The only thing that changed between
them is what was written down.

## Reading the capstone row

Do **not** compare its raw totals to row 1.1. GB-142 was one repository and five acceptance criteria;
GB-186 is two repositories, six criteria and eight process stages, so turns, tool calls and wall-clock
will be higher — that measures the size of the ticket, not the value of the method.

**Asked, rework and churn are the columns that compare, and they compare per acceptance criterion**
(five for GB-142, six for GB-186). A course that spends two days insisting you state what a number can
support does not get to hand you an unfair one at the end.
