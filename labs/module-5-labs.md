# Module 5 labs — Spec-driven development

**Day 2** · Labs 5.1, 5.2 (+ stretch) · about 75 minutes · Repository: `global-bank-account` · Start from: `m5-start`

On Day 1 every agent worked from the ticket as it was written. Today you improve the ticket first.
In Lab 5.1 you turn a vague ticket into a **spec**: a short file that says what "done" means, so
that a test can check it. In Lab 5.2 you plan the change, challenge the plan and split it into
tasks, all before any code exists.

These two labs are not measured in `metrics.md`. What you count here is different: **how many
decisions you stopped the agent from inventing.**

## Words used in these labs

| Word | Meaning here |
|---|---|
| **Spec** | A short file that says what "done" means for one ticket. It says *what*, never *how*. |
| **Acceptance criterion** | One numbered line in the spec that a test can check. We label them AC1, AC2 … |
| **Out of scope** | Things a reader might think the change includes, but it does not. |
| **Assumption** | A question you answered for yourself. You mark it **CONFIRMED** or **UNCONFIRMED**. |
| **Blocking** | An unconfirmed assumption that would change what the code does. It stops the spec check. |
| **Technical plan** | How the code will meet the spec: the approach and the files. |
| **Gate** | A check by a person between two steps. The answer can be "no". |
| **Pre-mortem** | You imagine the plan has already failed, and you ask why. |

## Before you start

**1. Load the Module 5 ticket.** In a terminal at the root of the course repository:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 5
```

Open `labs/lab-keys.md`. It now has a line for **GB-147**.

**2. Open the workspace.** In VS Code, select **File**, then **Open Workspace from File**, then
`adlc-labs.code-workspace`. Check that the **atlassian** MCP server is **Running** (Command Palette,
then **MCP: List Servers**).

**3. Make your branch.** In a terminal in `global-bank-account`:

```bash
cd ~/global-bank/global-bank-account
git fetch --tags --force
git switch -c GB-147-lab-5.1 m5-start && mvn test
# "already exists"? The branch is from an earlier run: see "Running a lab again" in README.md
```

Expect: `Tests run: 4, Failures: 0, Errors: 0`.

Check that the four agents from Module 4 are there:

```bash
ls .github/agents
```

Expect: `coding.agent.md  design.agent.md  review.agent.md  test.agent.md`.

You do not need your Day 1 branches. `m5-start` holds everything this module needs.

---

## Lab 5.1 — Write the spec for GB-147

**Goal:** turn a vague ticket into a spec an agent can follow and a test can check · **Ticket:**
GB-147 · **Timebox:** 45 min · **Output:** `specs/GB-147.md`, committed and reviewed by a partner

GB-147 asks for "reporting for the ops team". Its only acceptance criterion is: *"Ops can see the
postings."*

> **Do not ask Copilot to build it first, "just to see".** It will not refuse. It will build a
> report that looks finished, and every choice in it will be a guess. Once you have seen that
> report, it is much harder to write a spec that disagrees with it.

In this lab Copilot is your **interviewer and drafter**. It asks the questions and writes the file.
**You** decide what goes in it.

### Step 1 — Let Copilot interview you (10 min)

**Prompt 5.1-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-147. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Do not design or build anything. Your job is to interview me, so that I can write a spec.
First read these files in global-bank-account: docs/glossary.md, docs/architecture.md, every ADR
in docs/adr/, and src/main/java/in/brainupgrade/accountservice/posting/domain/Posting.java.
Then list every decision someone must make to build this ticket that the ticket does not answer.
For each decision, name the file that answers it, or write "not answered".
Then ask me about the "not answered" decisions, one question at a time, most important first.
Wait for my answer before you ask the next question. Stop after six questions.
```

**How to answer:** reply in one line. If the ticket, the files and you do not know the answer,
type `unknown`. Do not guess just to keep going. A guess you type here becomes a requirement.

**What you should see:** Copilot asks to run `jira_get_issue`. Read the request, then select
**Allow**. It then lists the open decisions, and asks its first question.

**Check:** count the decisions marked "not answered". Write the number down.

### Step 2 — Draft the acceptance criteria (8 min)

**Prompt 5.1-B** · Agent mode · base model · **same chat**

```text
Create the file global-bank-account/specs/GB-147.md. Start it with a title line that names
GB-147. Then write one section, headed "## Acceptance criteria".
Label the criteria AC1, AC2, AC3 and so on. Rules for each criterion:
- It covers one behaviour only. If it needs the word "and", split it into two criteria.
- It names a concrete input and a result that someone can observe.
- Someone who reads only that sentence could write a failing test from it, without asking anyone.
- It says what must be true for the ops team.
Use only what the ticket says, what the repository files say, and my answers. Where I answered
"unknown", do not write a criterion that depends on a guess.
Write only this one section. Then, in the chat, give the name of one test for each criterion that
would fail today. Do not create any test.
```

**What you should see:** a new file with numbered criteria, and a list of test names in the chat.

**Check:** read each criterion yourself. Ask: *could I write a failing test from this sentence
alone?* Mark each one yes or no. Look for the word "and" — it usually hides two criteria.

### Step 3 — Add out of scope, assumptions and open questions (8 min)

**Prompt 5.1-C** · Agent mode · base model · **same chat**

```text
Add three sections to global-bank-account/specs/GB-147.md, after the acceptance criteria.
"## Out of scope": at least four things a reasonable reader might think this change includes,
but it does not. One line each.
"## Assumptions": every question that you or I answered without the ticket saying so. End each
line with CONFIRMED and the file that confirms it, or with UNCONFIRMED. If an unconfirmed
assumption would change what the code does, also mark it BLOCKING.
"## Open questions": the questions nobody here could answer. Each one must be a question that a
person from Client Money Ops could answer in one conversation. Aim for three.
Every answer I gave as "unknown" must appear as an UNCONFIRMED assumption or as an open question.
Do not change the acceptance criteria. Stop when the file is saved, and show it to me.
```

**What you should see:** the file now has four sections.

**Check:** open `specs/GB-147.md` and count:

- at least four out-of-scope items
- every assumption ends with CONFIRMED or UNCONFIRMED
- at least one assumption is marked BLOCKING
- about three open questions

For each open question, ask yourself: *what would the agent have guessed here?* That guess is a
decision you just stopped it from inventing.

### Step 4 — Look for a hidden plan (6 min)

A spec says **what** must be true. A plan says **how** the code makes it true. When a spec names
classes or methods, the design is already decided, and the plan check has nothing left to decide.

**Prompt 5.1-D** · Agent mode · base model · **new chat**

```text
Read only global-bank-account/specs/GB-147.md. Do not open any other file.
A spec says what must be true. A plan says how the code will make it true.
List every sentence in the spec that names a class, a method, a repository query, a table, a
code file, an endpoint path or a query parameter. For each one, say whether the sentence states
a result that someone can observe, or a way to build it.
Then answer this: could two good engineers read this spec and write two different plans? If a
sentence forces one plan, quote it.
Do not edit the file.
```

**What you should see:** a list of sentences, each marked "result" or "way to build it".

If any sentence is "a way to build it", fix it:

**Prompt 5.1-E** · Agent mode · base model · **same chat**

```text
Rewrite each sentence you marked "a way to build it", so that it states only what must be true.
Keep the AC numbers the same. Change nothing else in global-bank-account/specs/GB-147.md.
Show me the lines you changed.
```

**Check:** read the changed lines. A sentence such as *"Add
`LedgerEntryRepository.findByAccountIdAndValueDateLessThanEqual`"* is a plan. A sentence that
names what the ops team sees is a spec.

### Step 5 — Commit the spec (1 min)

In the `global-bank-account` terminal:

```bash
git add specs/GB-147.md
git commit -m "GB-147: spec"
```

### Step 6 — The pair review: the gate (7 min)

This is the most useful part of the lab. **Do not skip it.**

Your trainer puts you in pairs. Share your spec with your partner (share your screen, or paste the
file in the meeting chat). Read your partner's spec and find two things:

1. **One criterion you could not write a failing test from.** Say why.
2. **One decision the author made that should have been an open question.**

Both are almost always there in a first draft. Tell your partner. Then fix your own spec in the
editor, and commit again:

```bash
git commit -am "GB-147: spec after pair review"
```

**No partner?** Use this prompt instead. It is weaker than a person, but it is better than no review.

**Prompt 5.1-F** · Agent mode · premium reasoning model · **new chat**

```text
Read only global-bank-account/specs/GB-147.md. Do not open any other file.
You are reviewing this spec before any code is written. Find two things:
1. The acceptance criterion that is hardest to write a failing test from. Quote it, and say why.
2. One criterion or assumption where the writer decided something that should have been an open
   question for the business. Quote it, and say what the question is.
Do not edit the file.
```

### Record

Fill in this worksheet in your notes. Post the last line in the meeting chat.

| Check | Your count |
|---|---|
| Numbered criteria | |
| … of which you could write a failing test from the sentence alone | |
| Out-of-scope items | |
| Assumptions (how many UNCONFIRMED, how many BLOCKING) | |
| Open questions | |
| From the pair review: the criterion they could not test | |
| From the pair review: the decision that should have been a question | |
| **Decisions the agent did not get to invent** (open questions + UNCONFIRMED assumptions) | |

### If you are behind

At 38 minutes, commit whatever you have and go to step 6. Lab 5.2 works with any spec that has
numbered criteria, even a short one. No checkpoint tag holds a GB-147 spec, so keep your own.

---

## Lab 5.2 — Plan, challenge, gate

**Goal:** plan the change from your spec, challenge the plan, and split it into tasks you can
check · **Ticket:** GB-147 · **Timebox:** 30 min · **Output:** `specs/GB-147-plan.md`, with a
task list and your gate decision, committed

Stay on the branch `GB-147-lab-5.1`. You need the spec you just wrote.

You will not finish GB-147 in this lab, and you are not meant to. Nobody writes code in the core
lab. Implementing the first task is stretch lab 5.2+.

### Step 1 — The design agent writes the plan, from the spec (8 min)

In the Chat view, open the agent list and pick **design**. Then paste the prompt.

**Prompt 5.2-A** · **design** agent · premium reasoning model · **new chat**

```text
The agreed spec for this change is global-bank-account/specs/GB-147.md. Work from the spec
only. Do not read the Jira ticket.
Also read these files in global-bank-account: docs/architecture.md, docs/conventions.md,
docs/glossary.md and every ADR in docs/adr/.
Write a technical plan: how the code will meet each acceptance criterion (AC1, AC2 and so on).
For this lab, your hand-off is a plan, not spec.md. Give the plan these sections:
"## Approach": the approach. Give two options only if there is a real choice, and recommend one.
"## Criteria": one line for each AC, saying how the plan meets it.
"## Files": each file to change or add.
"## ADRs": each ADR that applies, and what it requires here.
"## Not touched": the spec's out-of-scope items, as the files or areas the change leaves alone.
If an UNCONFIRMED assumption in the spec would change the design, say how.
Write no code and edit no files. Show the plan here in the chat.
```

**What you should see:** a plan in the chat. The design agent writes no files, by design.

**Save it:** create the file `global-bank-account/specs/GB-147-plan.md`. Select **Copy** on the
agent's answer, and paste it into the file.

**Check:** does every AC have a line under "## Criteria"? Does the plan name at least one ADR?

### Step 2 — Challenge the plan (8 min)

Question 4 below is a **pre-mortem**: imagine the plan has already failed, and ask why. Most
people skip this question. It is the one that finds new assumptions.

**Prompt 5.2-B** · **design** agent · premium reasoning model · **new chat**

```text
Read global-bank-account/specs/GB-147.md, global-bank-account/specs/GB-147-plan.md and every ADR
in global-bank-account/docs/adr/. Challenge the plan by answering four questions.
1. Which acceptance criterion does each plan step serve? Name any step that serves none, and any
   criterion that no step serves.
2. What does the plan conflict with? Name the ADR, the convention or the existing behaviour, and
   the file. If you say "nothing", show what you checked.
3. What is the smallest change that meets the spec? Name anything in the plan that is bigger.
4. Imagine it is three months from now, and this plan has failed. Give the three most likely
   reasons. For each reason, say whether I can check it now, and how. If I cannot, say that it
   is a new assumption the spec must record.
Do not edit any file.
```

**What you should see:** four answers. Question 4 usually gives at least one new assumption.

Now record what the challenge found. In the **same chat**, open the agent list and pick **Agent**.
Then paste:

**Prompt 5.2-C** · Agent mode · base model · **same chat**

```text
Add each new assumption from your answer to question 4 to the "## Assumptions" section of
global-bank-account/specs/GB-147.md, marked UNCONFIRMED. If your answers to questions 1 to 3 show
a change the plan needs, make it in global-bank-account/specs/GB-147-plan.md. Change nothing
else. List the lines you added or changed.
```

**Check:** read the new lines. You decide if they stay. Delete any you disagree with.

### Step 3 — Split the plan into tasks you can check (6 min)

The size of a task decides how often you can check the work. The rule: **if you cannot check a
task without doing the next one, it is only half a task.**

**Prompt 5.2-D** · Agent mode · base model · **same chat**

```text
Add a "## Tasks" section at the end of global-bank-account/specs/GB-147-plan.md. Split the plan
into tasks. The rule: I must be able to check each task's result on its own, without doing the
next task. Size the tasks by what can be checked, not by how long they take.
For each task, give: a number, one line saying what it does, the acceptance criteria it serves,
and how I check it (a test name, a command, or what to look at).
No task may end with "then continue". Write no code. Show me the tasks.
```

**What you should see:** a numbered task list, often five to eight tasks.

**Check:** does any task end with "then continue", or depend on the next task to be checked?

### Step 4 — Gate the task list (6 min)

A fresh chat reads the files without the planner's reasoning.

**Prompt 5.2-E** · Agent mode · base model · **new chat**

```text
Read only global-bank-account/specs/GB-147.md and global-bank-account/specs/GB-147-plan.md.
Check the "## Tasks" section against the spec. Report in one table:
- each acceptance criterion and the tasks that serve it; mark a criterion with no task as GAP
- each task and the criterion it serves; mark a task with no criterion as EXTRA SCOPE
- any task that cannot be checked without doing the next one; mark it HALF A TASK
- any task that touches something the spec lists as out of scope
- any BLOCKING assumption that is still UNCONFIRMED
End with one line: "Gate: pass" or "Gate: fail", and the reason. Do not edit any file.
```

**You make the gate decision, not Copilot.** Read the table. Then add one line at the end of
`specs/GB-147-plan.md`, in the editor:

```text
Gate (my decision): pass or fail, and one sentence saying why.
```

A BLOCKING assumption that nobody has confirmed means **fail**. That is a correct result. A gate
that can say "no" is working.

Commit both files:

```bash
git add specs
git commit -m "GB-147: plan, challenged and gated"
```

### Record

Add these lines to your worksheet from Lab 5.1:

| Check | Your answer |
|---|---|
| What the plan conflicted with (an ADR, a convention, nothing) | |
| Pre-mortem: the new assumptions it found | |
| Criteria with no task (GAP) | |
| Tasks with no criterion (EXTRA SCOPE) | |
| Your gate decision, and why | |
| **Decisions the agent did not get to invent** — update the Lab 5.1 count | |

### If you are behind

Commit what you have. Module 6 starts from the tag `m6-start` and a different ticket, so you lose
nothing that the next lab needs:

```bash
git add specs && git commit -m "GB-147: work in progress"
```

---

## Stretch lab 5.1+ (optional) — The thirty-second spec

**Goal:** most tickets do not need a full spec. Write the short form for a small ticket, and save it
next to the code.

At work, these three lines go at the top of the ticket. In this module nothing is written
back to Jira yet. Module 6 teaches that. So here you save them at the top of a spec file instead.

This uses **GB-202**, loaded in Module 3. If `labs/lab-keys.md` has no line for GB-202, run
`python labs/scripts/setup-lab-tickets.py --module 3` first.

**Prompt 5.1+-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-202. Use the atlassian MCP tools to read
that Jira issue, including its comments.
First decide if this ticket needs a full spec. Answer three questions, yes or no, one line each:
Could "done" mean more than one thing? Is being wrong expensive? Will more than one person or
repository touch it?
Then write the thirty-second spec, in three lines only:
"Done when:" the results a test can check.
"Not doing:" what this change leaves out.
"Assuming:" what you assumed, each marked CONFIRMED or UNCONFIRMED.
Show me the three lines. Do not create any file yet.
```

**Check:** edit the three lines in the chat until you agree with them. Then save them:

**Prompt 5.1+-B** · Agent mode · base model · **same chat**

```text
Create the file global-bank-account/specs/GB-202.md. Start it with a title line that names GB-202
and says "Light spec (Lab 5.1+)". Under the title, write the three lines, exactly as we agreed
them. Write nothing else in the file. Do not write anything to Jira.
```

**What you should see:** a new file with a title and three lines. Copilot makes no Jira tool call.
If it asks to run `jira_add_comment`, select **Skip**.

**Check:** open `specs/GB-202.md`. Could a teammate read it in thirty seconds and know what "done"
means? Commit it:

```bash
git add specs/GB-202.md
git commit -m "GB-202: light spec"
```

---

## Stretch lab 5.2+ (optional) — Implement task 1, and make the build check the criteria

### Part A — Implement task 1 only, then stop

This is the step the core lab leaves out for time.

First, the gate. If your gate said **fail** because of a BLOCKING assumption, ask your trainer. Your
trainer plays the person from Client Money Ops for this lab. Post your question in the meeting
chat. Mark the answer in the spec as `CONFIRMED (Client Money Ops, in the meeting chat)`.

In the agent list, pick **coding**. Then paste:

**Prompt 5.2+-A** · **coding** agent · base model · **new chat**

```text
The agreed spec is global-bank-account/specs/GB-147.md. The agreed plan is
global-bank-account/specs/GB-147-plan.md. Implement Task 1 from the "## Tasks" section only.
Show me the current contents of any method before you change it.
Run "mvn test" in global-bank-account when you finish.
Then stop. Do not start Task 2. List the files you changed, and tell me how I can check Task 1
on its own.
```

**Check:**

```bash
git diff --stat
mvn test
```

The coding agent writes no tests, so expect `Tests run: 4` to still pass. Now answer honestly: *could
you check task 1 on its own?* If not, the task boundary was wrong. That is the finding.

### Part B — Fail the build when a criterion has no test

A test proves a criterion when it names it, for example with a comment such as
`/** Spec GB-147 AC1: ... */`. A short script can then fail the build when a numbered criterion
has no test.

**Prompt 5.2+-B** · Agent mode · base model · **new chat**

```text
In global-bank-account, create the script ci/check-criteria-covered.sh.
It takes one argument: the path to a spec file, for example specs/GB-147.md.
It reads the ticket key from the file name, for example GB-147.
It finds every criterion label (AC1, AC2 and so on) in the spec's "## Acceptance criteria"
section.
For each criterion, it searches src/test for the text "Spec GB-147 AC1", using that criterion's
number. Match whole labels, so that AC1 does not match AC10.
It prints each criterion that no test mentions. It exits with 1 if any criterion has no test, and
with 0 if every criterion has one.
Use only bash, grep and sed, so that it runs in Git Bash and on Linux.
Do not change any other file. Run it once on specs/GB-147.md and show me the output.
```

**Check:** in the `global-bank-account` terminal:

```bash
bash ci/check-criteria-covered.sh specs/GB-147.md; echo "exit code: $?"
```

No test mentions your criteria yet. So the script should list every criterion and print
`exit code: 1`. That is the correct result.

Now make it part of the build:

**Prompt 5.2+-C** · Agent mode · base model · **same chat**

```text
Add a step named "Every acceptance criterion has a test" to .github/workflows/build.yml in
global-bank-account, before the Build step. It runs ci/check-criteria-covered.sh on every file in
specs/ whose name matches GB-*.md, except files ending in -plan.md. Change nothing else.
Show me the new step.
```

Commit your work:

```bash
git add ci .github/workflows/build.yml
git commit -m "GB-147: fail the build when a criterion has no test"
```

In a team, the build runs this step on every pull request. You do not push in this course, so it does
not run here. Until the test agent writes tagged tests, it would fail, and that is the point.
