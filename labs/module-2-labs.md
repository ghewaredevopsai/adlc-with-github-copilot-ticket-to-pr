# Module 2 labs — Knowledge harnessing

**Day 1** · Labs 2.1, 2.2 (+ stretch) · about 90 minutes · Repository: `global-bank-account` · Start
from: `m1-start`

In Lab 1.1 the agent spent many turns working out facts your team already knows. In Lab 2.1 you write
those facts into the repository, in three files: two for the whole repository and one for a single
folder. In Lab 2.2 you run **the same
ticket again**, with the same prompt and the same 35 minutes, in a new chat on a branch without your
Lab 1.1 code. The only thing that changes between the two runs is what is written down.

**Words used in these labs.** An **instruction file** is a Markdown file that Copilot loads by
itself. A **path-scoped** instruction file loads only when the agent works on files in one folder.
An **ADR** (Architecture Decision Record) records one decision, why it was made, and what was
rejected. The deck explains all three.

## Before you start

1. Your Lab 1.1 work and its metrics file are committed on their own branch (`GB-142-lab-1.1`). Lab 2.1 does not change that branch.

2. Both labs use GB-142, which is already in your Jira from Module 1. There is nothing to load.

3. Open the lab workspace: **File**, then **Open Workspace from File**, then
   `adlc-labs.code-workspace`. Check that the **atlassian** MCP server is running
   (**MCP: List Servers**).

4. Make a fresh branch from the starting code. Do **not** branch from your Lab 1.1 work: the code you
   give the agent in Lab 2.2 must be the same code you gave it in Lab 1.1.

   ```bash
   cd ~/adlc-copilot-training/global-bank-account
   git switch -c lab-2.1-knowledge m1-start && mvn test
   # expect: Tests run: 4, Failures: 0, Errors: 0
   ```

   **"already exists"?** You ran Lab 2.1 before. The tests do not run when the branch is not
   created. Delete the old branch, or rename it to keep it, then run the block again:

   ```bash
   git switch main
   git branch -D lab-2.1-knowledge GB-142-lab-2.2      # both, so Lab 2.2 starts clean too
   ```

   **Any number other than 4** means the branch did not come from `m1-start`.

---

## Lab 2.1 — Write the knowledge in three layers

**Goal:** turn what the agent had to re-discover in Lab 1.1 into three files it reads by itself ·
**Ticket:** GB-142 (for the ADR) · **Timebox:** 45 min · **Output:** three files, committed on
`lab-2.1-knowledge`

| File | Layer | What goes in it |
|---|---|---|
| `.github/copilot-instructions.md` | Repository | What is needed on every request. 30 lines or fewer |
| `.github/instructions/domain.instructions.md` | Path-scoped | Rules for the `posting/domain` folder only |
| `docs/adr/ADR-001-duplicate-suppression.md` | Repository | The GB-142 decision, and what you rejected |

All paths are inside `global-bank-account`. Use the three tests from the deck ("Which layer does a
fact belong in?") and the write-it-down test ("Should you write it down?").

### Step 1 — List what the agent had to re-discover

Open your Lab 1.1 chat again. At the top of the Chat view, open the chat history (the clock icon),
and pick the Lab 1.1 chat. Switch the mode to **Ask**.

**Prompt 2.1-A** · Ask mode · base model · **same chat as Lab 1.1**

```text
Look back over this whole chat. List every fact about the global-bank-account repository or
our team that you had to work out by opening or searching files, or that you asked me about.
For each fact, give one line: the fact, and how many files you opened to find it.
Then ask me which of these facts matter for future tickets. Wait for my answer.
Do not open any files. Do not change anything.
```

**What you should see:** a numbered list of facts, then a question to you.

Answer the question in your own words. Keep the facts that cost many file opens, and anything the
agent guessed wrongly. Add any fact you know that the agent never found.

**Then send this, in the same chat:**

**Prompt 2.1-B** · Agent mode · base model · **same chat**

```text
Write the facts I agreed to keep into a new file, course/labs/lab-2.1-facts.md.
One fact per line, in plain words. After each fact, say which file or class proves it.
Do not write the facts anywhere else. Stop when the file is written.
```

**Check:** open `course/labs/lab-2.1-facts.md`. Every line is a fact you agreed to. This file is your
notes. It is not part of the knowledge you commit.

> **No Lab 1.1 chat any more?** Run this instead, in a new chat, in **Agent** mode:
>
> ```text
> In the global-bank-account folder, compare the branch GB-142-lab-1.1 with the tag m1-start.
> Use "git diff m1-start GB-142-lab-1.1". From the change, list the facts about this
> repository that a new engineer would need to know to make it. One line per fact.
> Then ask me which of these facts matter for future tickets. Wait for my answer.
> Do not change anything.
> ```
>
> Then send Prompt 2.1-B in the same chat.

### Step 2 — Draft the repository instruction file

**Prompt 2.1-C** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-2.1-facts.md. Draft global-bank-account/.github/copilot-instructions.md
from those facts only.
Use three parts, in this order: "Read these before proposing a change" (pointers to other
files), "Non-negotiables" (rules that are a bug to break), and "When you are unsure" (tell the
agent to ask, and to quote the file it relies on).
Keep only facts needed on every request. For a fact that changes often, write where to find
it, not the value. Keep the file to 30 lines or fewer.
Check each rule against the code before you write it. Do not add any rule that is not in my
facts file.
Write the file. Then list each line you wrote and say why it belongs in this file.
Do not create any other file.
```

**What you should see:** the new file, and a short reason for each line.

**Check:** `wc -l .github/copilot-instructions.md` shows 30 or fewer. Read every line. Is each one
true in the code? Delete any line you cannot confirm.

### Step 3 — Cut it down

**Prompt 2.1-D** · Agent mode · base model · **same chat**

```text
Sort every line of global-bank-account/.github/copilot-instructions.md into these four boxes:
1. hard to work out from the code, and needed on every request - keep
2. hard to work out, but needed only sometimes - write an index: move it to a file, and point to it
3. easy to see in one or two files, but needed on every request - replace with a pointer
4. easy to see in one or two files, and rarely needed - delete
Show me the table first. Then make the changes, and list every line you deleted.
Do not change any other file.
```

**What you should see:** a table of lines and boxes, then a shorter file.

**Check:** at least one line was deleted. If nothing was deleted, look again at box 4. Most first
drafts lose about a third.

### Step 4 — Draft the path-scoped file for the domain folder

**Prompt 2.1-E** · Agent mode · base model · **new chat**

```text
Read global-bank-account/.github/copilot-instructions.md and course/labs/lab-2.1-facts.md.
Draft global-bank-account/.github/instructions/domain.instructions.md.
Start the file with this header, exactly:
---
applyTo: "src/main/java/in/brainupgrade/accountservice/posting/domain/**"
---
Write only the rules that are true in the posting/domain folder and different from the
repository instructions. Do not repeat any rule from copilot-instructions.md.
Check each rule against the classes in that folder before you write it. Keep it to 12 lines
or fewer after the header.
Write the file. Then list each rule and name the domain class that shows it is true.
Do not create any other file.
```

**What you should see:** a short file with the `applyTo` header, and a class named for each rule.

**Check:**

```bash
head -3 .github/instructions/domain.instructions.md
ls src/main/java/in/brainupgrade/accountservice/posting/domain/
```

The header is there, and the folder in `applyTo` exists. Then compare the two instruction files. No
rule appears in both.

### Step 5 — Write the ADR for the GB-142 decision

The ADR records **your** decision from Lab 1.1, and what you decided **not** to do. The agent does
not know your reasons, so you supply them. If you do not know why an option was rejected, say
"unknown — ask the team". Do not let the agent invent a reason.

**Prompt 2.1-F** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-142. Use the atlassian MCP tools to
read that Jira issue, including its comments. Read Jira only. Do not add a comment to the
issue, and do not change it.
I will write an ADR for how we suppress duplicate postings. You write it down; I supply the
decision. Ask me these questions here in the chat, one at a time. Ask the first question,
then stop and end your turn. Do not run any tool while you are asking. Wait for my answer
before you ask the next one.
1. Which options did we consider?
2. Which option did we choose, and why?
3. Which options did we reject, and why was each one rejected?
4. What does the choice cost us, or what must we do next?
Do not suggest answers. Do not add any reason I did not give you. If I say a reason is
unknown, write "Unknown - ask the team".
When I have answered all four, write
global-bank-account/docs/adr/ADR-001-duplicate-suppression.md with these sections:
Status, Context, Options considered, Decision, Rejected options, Consequences.
Then add one line under "Read these before proposing a change" in
global-bank-account/.github/copilot-instructions.md that points to docs/adr/.
Do not change any other file.
```

**What you should see:** four questions, one at a time. Then the ADR file, and one new pointer line
in the instruction file.

If you see **Add Comment** run instead, the agent is posting your questions to the Jira issue. It
has no way to ask you, so it reached for the nearest tool it did have. Stop it, delete the comments
it added to the issue, and start a new chat with the prompt above.

**Answer from your own run first.** The ADR records what **you** decided in Lab 1.1. Read the example
below only after you have answered all four questions. Your answers will differ from it, because your
Lab 1.1 differed. That is correct.

<details>
<summary><b>An example of the four answers</b> — open after you have answered</summary>

**1. Which options did we consider?**

> Three. (a) A posting is a duplicate when the `clientReference` matches. (b) A posting is a duplicate
> when `clientReference` **and** `valueDate` both match. (c) An `Idempotency-Key` request header, with
> a store of keys we have already seen.

If your agent weighed only one option, say so. A short list is an honest list.

**2. Which option did we choose, and why?**

> `clientReference` + `valueDate`. Criteria 1 and 3 need both fields. The same reference on the same
> value date is the retry. The same reference on a later value date is a real standing-order payment,
> and it must go through. `findByClientReferenceAndValueDate` was already in the repository, unused.
> On a match we return the first posting with HTTP 200 and its posting id, so criterion 2 holds.
> Amount and narrative are not part of the key.

**3. Which options did we reject, and why was each one rejected?**

> - `clientReference` alone — breaks criterion 3. The April payment has the same reference, and we
>   would suppress it.
> - Answer the retry with an error — breaks criterion 2. The caller needs the posting id back.
> - `Idempotency-Key` header — **Unknown, ask the team.**

The last line is the honest one. Nothing in the ticket or the code says why a header would not work
here. You meet that reason in Module 4. Do not let the agent write a reason for you.

**4. What does the choice cost us, or what must we do next?**

> - Two retries at the same moment can both pass the check. Closing that needs a unique index on
>   `(client_reference, value_date)`. We have not added one, and no test covers it.
> - `clientReference` is now part of our API contract. Callers must keep it the same across their own
>   retries, and we must tell them.
> - A caller that sends the same reference with a different amount on the same date now gets the first
>   posting back. We accepted that. It is a caller mistake, so we may want to log it.

</details>

**Check:** open the ADR. It has a **Rejected options** section with at least one option and a reason
(or "Unknown - ask the team"). Check that every reason in it is one you gave.

### Step 6 — Commit

```bash
git add .github docs
git commit -m "GB-142 knowledge: repository instructions, domain rules, ADR-001"
git show --stat HEAD
# expect: 3 files changed
```

Do not add `course/labs/lab-2.1-facts.md` to this commit. It is in the other repository, and it is
your notes.

### Done means

- Three files are committed on `lab-2.1-knowledge`.
- The instruction file has 30 lines or fewer, and you deleted at least one line from the first draft.
- The path-scoped file has an `applyTo` that matches a real folder, and repeats no repository rule.
- The ADR names at least one rejected option, with a reason or "Unknown - ask the team".

### Record

Lab 2.1 is not a measured run, so there is no metrics file. Write two lines in your notes:
- the line you deleted in Step 3, and why
- the rejected option in your ADR, and where the reason came from

### If you are behind

Commit what you have, even if you have only two files. Lab 2.2 runs on your own files. If your
trainer tells you to skip Step 4, keep the instruction file and the ADR.

If you have no files at all, use the catch-up tag in Lab 2.2 (see below).

---

## Lab 2.2 — The same ticket, re-measured

**Goal:** run GB-142 again on the repository you just wrote, and compare the numbers ·
**Ticket:** GB-142 · **Timebox:** 45 min (35 working, 10 recording) · **Output:** `metrics-2.2-*.md`

The same ticket, the same prompt and the same 35 minutes. Only the repository changed. That is what
makes the two rows comparable: a different ticket would measure its size as much as your files.

The agent starts in a **new chat**, so it remembers nothing from Lab 1.1. Your branch starts from
`lab-2.1-knowledge`, which has your three files and none of your Lab 1.1 code.

### Step 1 — Branch from your own Lab 2.1 work

```bash
cd ~/adlc-copilot-training/global-bank-account
git status --short
# must print nothing. If it lists your three files, Lab 2.1 Step 6 did not commit them:
# go back and commit them on lab-2.1-knowledge first
git switch -c GB-142-lab-2.2 lab-2.1-knowledge
# "already exists"? git switch main && git branch -D GB-142-lab-2.2, then run this block again
git show --stat lab-2.1-knowledge | tail -5
# expect: your three knowledge files
mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0
```

### Step 2 — Check that Copilot sees your files

Do this before the clock starts. It does not count in your numbers.

Close every editor tab. Then open
`global-bank-account/src/main/java/in/brainupgrade/accountservice/posting/domain/Posting.java`, so
it is the only open file.

**Prompt 2.2-check** · Ask mode · base model · **new chat**

```text
Answer from the instructions you were given for this chat. Do not open or search any file.
1. Quote one rule, word for word, from global-bank-account/.github/copilot-instructions.md.
2. The open file is Posting.java. Which path-scoped instruction file applies to it?
   Quote one rule from that file, word for word.
Do not change anything.
```

**What you should see:** one quoted rule from each of your two files.

**Check:** expand the **references** list under the answer (it says "Used n references"). Both
`copilot-instructions.md` and `domain.instructions.md` should be listed.

**On Copilot CLI, check it this way instead.** The CLI reads instruction files from **the folder it
was started in**, so it must be started inside `global-bank-account`:

```bash
cd ~/adlc-copilot-training/global-bank-account
copilot instruction list
```

It must list `.github/copilot-instructions.md` and your path-scoped file. If it says **"No
instruction sources found"**, you started the CLI in the wrong folder — close it, `cd` into
`global-bank-account`, and start it again. Starting one folder up finds nothing, with no warning.

If a file is missing from the list, stop and tell your trainer. Written is not the same as
reachable, and a run with files Copilot cannot see measures nothing.

Now close `Posting.java`, so no editor tab is open. Lab 1.1 started with no open file too.

### Step 3 — The measured run

Your 35 minutes start with this prompt. You do not count anything: the record prompt does that.

**Prompt 2.2-A** · Agent mode · base model · **new chat**

**This run is one chat again,** the way Lab 1.1 was. On **Copilot CLI**, start the CLI fresh before
you send it, **inside `global-bank-account`**: `/usage` counts the whole session, and this session
already holds Lab 2.1 and Prompt 2.2-check, which would land in your row and make the prepared run
look more expensive than it was. The folder matters as much as the fresh start — from anywhere else
the CLI loads none of your instruction files, and the run measures an unprepared repository.

```text
Read course/labs/lab-keys.md to find my Jira key for GB-142. Use the atlassian MCP tools to read
that Jira issue, including its comments. Read no other issue, and do not search Confluence.
Implement the ticket in the global-bank-account folder. Meet every acceptance criterion.
Work only from the files on the current branch. Do not read any other git branch.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say which acceptance criteria are met and how.
```

Copy it exactly. It is Prompt 1.1-A, word for word.

**Two things not to do.** Do not tell Copilot what your Lab 1.1 run did, and do not open your
`GB-142-lab-1.1` branch. The comparison only holds while the chat and the branch are clean. What you
remember is not a problem: you send one scripted prompt, so your memory has no way into the run.

### Step 4 — The same five checks as Lab 1.1

Run them yourself. Do not trust Copilot's report alone. The steps are in
[module-1-labs.md](module-1-labs.md): `mvn test` for Check 1, then `mvn spring-boot:run` in a second
terminal, then the `post` and `balance` helpers for Checks 2 to 5.

| Check | Passes when |
|---|---|
| **1** — tests | `Tests run` is more than 4, `Failures: 0`, `Errors: 0` |
| **2** — the same instruction twice | Both calls return HTTP 200 or 201 with the **same** `postingId`. Balance `2500000` |
| **3** — same reference, new value date | HTTP 201, a **new** `postingId`, `"valueDate":"2026-04-30"`. Balance `5000000` |
| **4** — a new instruction | HTTP 201 with a `postingId`. Balance `750000` |
| **5** — the March payment again, worded differently | The **same** `postingId` as your first `MARCH` call. Balance still `5000000` |

### Step 5 — Repair, only when a check fails

**Prompt 2.2-R** · Agent mode · **same chat as Prompt 2.2-A**

```text
A check failed. This is what I saw:
<paste the failing output here>
Fix only this. Run "mvn test" in global-bank-account again, and tell me which acceptance
criteria are now met.
```

Replace the one line in `<>` with the output of the failing check. Each repair counts as one turn
**and** one rework.

After a repair, stop the service (`Ctrl+C`), start it again, and run all the checks again from the
top.

**Stop** when all five checks pass, after three repairs, or at 35 minutes. Whichever comes first.

### Step 6 — Commit

Stop the service. Then:

```bash
git add -A
git commit -m "GB-142 with the knowledge files (Lab 2.2 run)"
```

Commit even if some checks still fail. The metrics file records what happened.

### Record

Read the model and the usage numbers for this chat first, the same way as in Lab 1.1: `/usage` in
Copilot CLI, or the **context window control** in the VS Code chat input box. Read them before you
record, so the record prompt's own cost stays out of the run. The agent cannot run `/usage` for you.
On CLI, the number is this run only if you started the CLI fresh at Step 3.

Then send this in the **same chat as Prompt 2.2-A**, as soon as the checks pass. Your 35 minutes run
until you send it. It is Prompt 1.1-M with the run and the commit
message changed. Prompt 2.2-check was a different chat, so it is not counted.

**Prompt 2.2-M** · Agent mode · **same chat**

```text
The run is over. Do not ask me anything. Anything below still written inside angle brackets is
missing: write "-" in its place, never the bracket text itself, and carry on.
Count these numbers from this chat only, and do not guess beyond it:
- Turns: prompts I sent, from the opener to the last repair. Not this prompt.
- Tool calls: files you read and searches you ran. Not the Jira fetch, edits or terminal commands.
- Asked: questions you asked me that a file in the repository could have answered.
- Rework: repair prompts I sent that start with "A check failed".
- Churn: lines you wrote earlier in this run and later replaced or deleted, to the nearest ten.
- Assumptions: decisions you made that no file in the repository answered, for example a design
  choice, a rule or a name. List them in one line each.
The model and usage numbers below come from my Copilot client, read just before I sent this
prompt. Copy them exactly. Do not calculate, estimate, round or replace them.
- Model: <paste the model name>
- Model ID: <paste the model id, if it is shown>
- Input tokens: <paste input tokens>
- Output tokens: <paste output tokens>
- Total tokens: <paste total tokens>
- AIC: <paste AI credits>
If more than one model ran during the work, list each one in Model and Model ID, separated by
semicolons.
Run "date +%Y%m%d-%H%M%S" in a terminal and use its output as the timestamp. At the root of
global-bank-account create metrics-2.2-<timestamp>.md, with this table and one row:
| Run | Ticket | Model | Model ID | Turns | Tool calls | Asked | Rework | Churn | Input tokens | Output tokens | Total tokens | AIC |
Use "2.2" as the run and "GB-142" as the ticket.
Add the Lab 1.1 row below it, copied from the newest Lab 1.1 metrics file, which you get with
"git show GB-142-lab-1.1:$(git ls-tree --name-only GB-142-lab-1.1 | grep '^metrics-1.1-' | sort | tail -1)".
Under the table, add "Assumptions (N):" with N the number you counted and the list below it, then a
line "Lab 1.1 assumptions:" with the count from that same Lab 1.1 file, then one line "Notes:" with
my notes below, and one line "How counted:" that says anything you could not count exactly, and says
that the model, token and AIC values were read from my client just before this prompt, so they leave
this prompt out.
Then run: git add -A && git commit -m "GB-142 lab 2.2 metrics". Show me the file name and the
table.
My notes: <anything unusual, or leave empty>
```

**A `-` in any usage column?** You sent the prompt with those lines unchanged. Type the values into
your `metrics-2.2-…md` yourself and commit again, as in Lab 1.1.

Report what you measured, even if a number got worse. **AIC is the real bill**, so read that column in
both rows first: it is what the three files cost or saved on this one ticket. Then write one line under
the row: which of your three files helped most in this run, and how you know. The references list
under each answer shows which files Copilot used.

**Read the two assumption lists, not the two counts.** The count often does not move, and it does not
have to. What changes is **what** the agent had to assume. Put the lists side by side and mark each
line: is it a **business rule** (what counts as a duplicate, what the caller gets back) or an
**implementation detail** (a class name, an exception name, an edge case)? A run that guesses only
names, on a repository that settled the rule for it, is the result Module 2 is after — even with the
same number of lines.

**Tool calls may go up, and that is not a failure.** Your files do not stop the agent reading code;
they point it at more of the code, and it often writes more tests and more classes as a result. Say
what you see.

**Then compare the two fixes.** The numbers are not the only result. Both runs solved the same
ticket, so you can read the code side by side:

```bash
git diff GB-142-lab-1.1 GB-142-lab-2.2 -- src/main/java
```

Ask two questions. Does the Lab 1.1 fix match the decision in your ADR, or did the agent invent its
own rule? Does the Lab 2.2 fix follow the ADR? A run with the same numbers but the agreed design
is still a better run, and that difference is what your files bought.

Finally, compare your instruction file with the reference version:

```bash
git diff GB-142-lab-2.2 m2.2-start -- .github/copilot-instructions.md
```

Note one fact the reference file has and yours does not. Then read the reference ADR the same way,
and compare it with your ADR-001:

```bash
git show m2.2-start:docs/adr/ADR-007-duplicate-suppression.md
```

Look for the rejected option and the reason it gives. The debrief after lunch goes through it.

### If you are behind

Did not finish Lab 2.1? Start Lab 2.2 from the reference knowledge instead of your own:

```bash
git switch -c GB-142-lab-2.2 m2.2-start
```

Then do Steps 2 to 6 as written. Write "m2.2-start" in the notes line of Prompt 2.2-M, because this row then
measures the reference files, not yours.

---

## Stretch lab 2.1+ (optional) — A check for paths that no longer exist

**Goal:** a test that fails when an instruction file names a file or folder that is not in the
repository. It runs with `mvn test`, so in a team the CI build would run it on every pull request.

Do it on its own branch, so Lab 2.2 still starts from your three files only:

```bash
git switch -c lab-2.1-plus lab-2.1-knowledge
```

**Prompt 2.1+A** · Agent mode · base model · **new chat**

```text
In global-bank-account, plan a JUnit test named InstructionFilePathsTest in src/test/java.
It reads every Markdown file under .github/ and docs/. It finds every text in backticks that
looks like a repository path: it contains a "/" or ends in .md, .java, .xml, .sql or .properties.
It checks that each path exists, relative to the repository root.
It fails with a message that names the Markdown file and the missing path.
Show me the plan and the path rule. Do not write any code yet.
```

**Prompt 2.1+B** · Agent mode · base model · **same chat**

```text
Write the test from the plan. Use AssertJ and no Spring context. Run "mvn test" in
global-bank-account. If the test finds a path that does not exist, show it to me and stop.
Do not change any Markdown file.
```

**Check:** break one path on purpose, then undo it.

First check that your `copilot-instructions.md` names `docs/adr/` in backticks. The test reads only
paths in backticks, so without them this check passes and proves nothing. Add the backticks if they
are missing, then:

```bash
sed -i 's#docs/adr/#docs/decisions/#' .github/copilot-instructions.md
mvn test          # expect: InstructionFilePathsTest fails and names docs/decisions/
git restore .github/copilot-instructions.md
mvn test          # expect: passes
```

(On a Mac, use `sed -i ''`.) Commit on `lab-2.1-plus`. Switch back with
`git switch GB-142-lab-2.2` before you go on.

## Stretch lab 2.2+ (optional) — Plant a fake secret

**Goal:** see whether Copilot, or a review, notices a secret in an instruction file. The value below
is fake. **Never use a real key, token or password in this lab.**

Do it on a throwaway branch, and never push it:

```bash
git switch -c lab-2.2-plus GB-142-lab-2.2
echo "- Test posting API: API_KEY=test-not-real-0000" >> .github/copilot-instructions.md
git commit -am "Add API note"
```

**Prompt 2.2+A** · Agent mode · base model · **new chat**

```text
Write a pull request description for the last commit on the current branch in
global-bank-account. Use "git show HEAD" to see it. Keep it to five lines.
Do not change any file.
```

**What to look at:** does the description repeat the key? Does Copilot warn you about it?

**Prompt 2.2+B** · Ask mode · base model · **new chat**

```text
Review global-bank-account/.github/copilot-instructions.md as a security reviewer.
List any line that should not be in a file that is sent with every Copilot request, and say why.
Do not change anything.
```

**What to look at:** does the review find the line? What does it tell you to do about it?

Now delete the line in a new commit, and look at the history:

```bash
sed -i '/test-not-real-0000/d' .github/copilot-instructions.md
git commit -am "Remove API note"
git log -p -S test-not-real-0000 --oneline
```

The value is still in the history. For a real key, deleting it is not enough: you must replace it
with a new key (rotate it). Then delete the branch:

```bash
git switch GB-142-lab-2.2
git branch -D lab-2.2-plus
```
