# Module 3 labs — Prompt and context engineering

**Day 1** · Labs 3.1, 3.2 (+ stretch) · about 105 minutes · Repository: `global-bank-account` ·
Start from: your Module 2 branch (catch-up: `m3-start`)

In Module 2 you wrote down what is true about the repository. These labs are about how you ask.
In Lab 3.1 you write one clear request for a ticket. Then you save the reusable half as a **skill
file** and a **prompt file**. In Lab 3.2 you test that skill file on six tickets and get a **pass
rate**. A pass rate is the number of tickets that passed, out of six.

Two words you need:

- **Skill file:** a file of steps for one kind of task. Copilot loads it by itself when your task
  matches the skill's description. It lives in `.github/skills/<name>/SKILL.md`.
- **Prompt file:** a saved prompt that you run by typing `/` and its name in the chat. It lives in
  `.github/prompts/`. It can take inputs, such as a ticket key.

## Before you start

**1. Load the Module 3 tickets.** Open a terminal in the `course` folder (right-click the folder in
the Explorer, then **Open in Integrated Terminal**). Run:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 3
```

This creates six tickets, GB-201 to GB-206, in your Jira project. Open `labs/lab-keys.md`. It
should now list GB-201 to GB-206, each with your own key. GB-151 is already there from Module 2.

**2. Check the Jira connection.** Run **MCP: List Servers** from the Command Palette. **atlassian**
must say **Running**.

**3. Branch from your Module 2 work.** Open a terminal in the `global-bank-account` folder. You
continue from the branch you finished Lab 2.2 on, `GB-151-lab-2.2`. It holds the knowledge files
you wrote in Module 2. Your skill file points at them.

```bash
cd ~/global-bank/global-bank-account
git status --short
# must print nothing. If it lists files, commit them first:
#   git add -A && git commit -m "Lab 2.2 work"
git switch -c GB-151-lab-3.1
mvn test
# expect: Failures: 0, Errors: 0
# Tests run: 4, or more if your Lab 2.2 work added tests
```

If `mvn test` fails on your Module 2 branch, do not fix it now. Use the catch-up tag instead:

```bash
git switch -C GB-151-lab-3.1 m3-start
# -C (capital) starts the branch again from the tag, even if it exists
mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0
```

You write some notes in `course/labs/my-work/`. That folder is for you. You do not commit it.

---

## Lab 3.1 — The skill file

**Goal:** write one clear request for GB-151, then save its reusable half as a skill file and a
prompt file · **Ticket:** GB-151 · **Timebox:** 45 min · **Output:** `SKILL.md` and
`gb-change.prompt.md`, committed on your branch

Slides 4 and 5 showed six parts of a good request: **goal, constraints, inputs, output contract, done
criteria and stop conditions**. A **stop condition** names a situation where the agent must stop
and ask you, instead of guessing. Keep slide 5 open while you work.

### Step 1 — Write the six-part request (10 min)

**Prompt 3.1-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-151. Use the atlassian MCP tools to read
that Jira issue.
Do not implement the ticket. Instead, write a request that I could give to an agent to implement it.
Use these six parts as headings, in this order: GOAL, CONSTRAINTS, INPUTS, OUTPUT CONTRACT, DONE, STOP.
- GOAL: one sentence that describes the result, not the code.
- CONSTRAINTS: point at the files in global-bank-account/docs and global-bank-account/.github that
  hold the rules. Do not copy their text.
- INPUTS: the two or three source files that matter, the ticket, and one existing file in the
  posting package whose style the agent should copy.
- OUTPUT CONTRACT: which kinds of files change, which tests are expected, the error format, and
  no new dependencies.
- DONE: checks that someone else could run without asking me, such as "mvn test passes".
- STOP: named situations where the agent must stop and ask me. Do not write "if unsure".
Check that every file you name exists.
Write the request to course/labs/my-work/gb-151-request.md. Do not change any file in
global-bank-account. Stop when the file is written, and show it to me.
```

**What you should see:** Copilot reads `lab-keys.md`, then the Jira issue, then some files under
`docs/` and `posting/`. It writes one short file with six headings. It changes nothing in
`global-bank-account`.

**Check:** read the file yourself, part by part. Edit it by hand where a check fails.

| Part | Check before you go on |
|---|---|
| GOAL | Does it describe a result, or a piece of code you already pictured? |
| CONSTRAINTS | Does it point at files, or copy text that is already in `docs/`? |
| INPUTS | Could you explain why each file you left out is not needed? |
| OUTPUT CONTRACT | Could a reviewer read the resulting change in one sitting? |
| DONE | Could a teammate run each check without asking you? |
| STOP | Does any line say only "if unsure" or "if unclear"? Rewrite it as a situation the agent can check, such as "if the ticket can be read two ways" or "if no ADR covers this design choice". |

"Ask if you are unsure" changes nothing. The model does not feel unsure the way a person does. A
stop condition must name something the agent can check.

### Step 2 — Split the reusable half from this ticket (8 min)

**Prompt 3.1-B** · Agent mode · base model · **same chat**

```text
Read course/labs/my-work/gb-151-request.md.
Split its lines into two groups, and write them to course/labs/my-work/gb-151-split.md:
- "This ticket only": lines that change with every ticket, such as the goal, the ticket key and
  the input files.
- "Every change of this kind": lines that hold for any change to posting or balance behaviour in
  global-bank-account.
Put each line in exactly one group. Do not add new rules, and do not delete any line.
If a line mixes both, split it into two lines and tell me which ones you split.
Stop when the file is written, and show me the second group.
```

**What you should see:** two lists. The goal and the input files are in the first. Most
constraints, the output contract, the done checks and the stop conditions are in the second.

**Check:** read the second group. It must not name GB-151, and it must not mention reversals. A
teammate should be able to use it on next sprint's ticket without editing it. Move any line that
fails this test into the first group, by hand.

### Step 3 — Write the skill file (12 min)

**Prompt 3.1-C** · Agent mode · base model · **same chat**

```text
Read course/labs/my-work/gb-151-split.md. Use only the group "Every change of this kind".
Create the skill file global-bank-account/.github/skills/account-change/SKILL.md from it.
Start with a YAML header between two "---" lines. It holds:
- name: account-change (this must match the folder name)
- description: one specific sentence that says which changes this skill is for
- metadata, with version: "1" and owner: payments-platform
Then use these sections, in this order:
# Before you write anything
# Rules that always apply
# Output contract
# Done criteria
# Stop and ask — do not choose
Under "Before you write anything", tell the agent to list docs/adr/ and open any ADR the ticket
touches.
Put the four grounding rules in the file: cite the file each rule came from, show the current
code before you change it, say so and stop when you cannot find something in the repository, and
never invent IDs, status values, codes or limits.
Keep every stop condition from the split file. Point at files in docs/ instead of copying their
text. Do not name any ticket in this file.
Create only this one file. Stop when it is written, and show it to me.
```

**What you should see:** one new file, about 30 to 45 lines, with the header and five sections.

**Check:** in the `global-bank-account` terminal:

```bash
head -8 .github/skills/account-change/SKILL.md
# the header must say: name: account-change
grep -n "GB-" .github/skills/account-change/SKILL.md
# must print nothing: the skill file names no ticket
```

### Step 4 — Write the prompt file (5 min)

**Prompt 3.1-D** · Agent mode · base model · **same chat**

```text
Create the prompt file global-bank-account/.github/prompts/gb-change.prompt.md.
Start with a YAML header between two "---" lines. It holds:
- description: Start a Global Bank change from a ticket
- agent: agent
- argument-hint: ticket=GB-nnn goal=...
Then write a short body, as slide 11 shows. It must:
- tell the agent to follow the account-change skill
- take two inputs, written as ${input:ticket} and ${input:goal}
- tell the agent to read course/labs/lab-keys.md to find my Jira key for the ticket, and to read
  that Jira issue with the atlassian MCP tools
- say that if the agent cannot name the input files, it searches #codebase once, lists what it
  found, and waits for my OK
Put no steps or rules in this file. They belong in the skill file.
Create only this one file. Stop when it is written, and show it to me.
```

**What you should see:** a file of about 12 lines. It holds the two input slots, a pointer to the
skill and the key lookup. It holds no rules.

**Check:** commit both files now. Lab 3.2 resets the working tree many times, and only committed
files are safe.

```bash
git add .github/skills .github/prompts
git commit -m "Add the account-change skill and the gb-change prompt file"
git status --short
# must print nothing
```

### Step 5 — Check that Copilot loads them (7 min)

**Prompt 3.1-E** · Agent mode · base model · **new chat**

In the chat box, type `/gb-` and check that **gb-change** appears in the list. Then send:

```text
/gb-change ticket=GB-151 goal="Let Operations reverse a posting booked in error"
```

**What you should see:** Copilot reads your `SKILL.md`. It also reads `lab-keys.md` and the Jira
issue. Its first answer follows your "Before you write anything" section. For example, it lists
`docs/adr/` and quotes a rule with the file it came from.

This step checks that the files load. It does not implement GB-151. When you see Copilot follow
your skill file, select **Stop**. Then clear anything it changed:

```bash
git stash push -u -m "lab 3.1 load check"
git status --short
# must print nothing
```

If `git stash` says "No local changes to save", that is fine.

**If it does not load:**

- **gb-change** is not in the `/` list: check the file name ends in `.prompt.md` and sits in
  `global-bank-account/.github/prompts/`.
- Copilot never opens `SKILL.md`: check that `name:` in the header is exactly `account-change`,
  the same as the folder name. Make the `description` more specific. Then tell your trainer.

### Record

Nothing goes on the tally for Lab 3.1. Keep `gb-151-request.md` open. In the debrief, you may be
asked to read out your stop conditions.

### If you are behind

Start Lab 3.1 from the catch-up tag, and do Steps 1 to 5:

```bash
git switch -C GB-151-lab-3.1 m3-start
# -C (capital) starts the branch again from the tag, even if it exists
```

If you run out of time before Step 4, go to Lab 3.2 anyway. Its "If you are behind" section shows
how to start from the reference skill file.

---

## Lab 3.2 — The prompt A/B

**Goal:** run six tickets twice and compare two ways of asking, by pass rate · **Tickets:** GB-201
to GB-206 · **Timebox:** 60 min (10 to set up, about 20 per column including scoring, 10 to record) · **Output:** two pass rates out of
6, on your tally

You run the six tickets twice. **Column A** uses an ordinary prompt, the way most people type it.
**Column B** uses `/gb-change`, which brings in your skill file. That makes twelve runs. You score
each run **pass** or **fail**. The six tickets are an **eval set**, short for evaluation set: a
small, fixed set of tickets for testing a prompt.

### Step 1 — Fill in the pass criteria first (8 min)

This step has no prompt. You write it yourself.

Copy this table into a new file, `course/labs/my-work/eval-sheet.md`. Read the six tickets in your
Jira. For each ticket, write what a pass means in the second column. Base it on the ticket's
acceptance criteria.

| Ticket | Pass means (write this before any run) | A | B | Changed? |
|---|---|---|---|---|
| GB-201 | | | | |
| GB-202 | | | | |
| GB-203 | | | | |
| GB-204 | | | | |
| GB-205 | | | | |
| GB-206 | | | | |
| **Pass rate** | | **/6** | **/6** | |

Use the rules from slide 19 for every ticket, cut down to fit a four-minute run:

- The acceptance criteria are met, and `mvn test` passes. (Slide 19 also asks that the new test
  fails on the old code. There is no time to check that here, so leave it out for both columns.)
- No file changed that the ticket did not need. (Column A has no INPUTS list, so this replaces
  slide 19's "no files changed outside INPUTS" for both columns.)
- A ticket you judge unclear passes only if the agent stopped and asked. Guessing is a fail.

**Do not change this column after your first run.** If you decide what a pass means after you see
the output, you will favour the prompt you wrote yourself.

### Step 2 — Set up a branch for the runs (2 min)

In the `global-bank-account` terminal:

```bash
git status --short
# must print nothing. Your skill file and prompt file must be committed
git switch -c eval-lab-3.2
git tag -f eval-base
```

`eval-base` marks the clean starting point. After every run, you go back to it.

### How every run works

1. Start a **new chat**. Set **Agent** mode and the **base model**.
2. Paste the run's prompt exactly.
3. Read each tool request before you select **Allow**. **If Copilot asks to add a comment to a Jira
   issue, select Skip.** A comment stays on the ticket, and your next run on that ticket would read it.
4. If Copilot lists the files it found and waits for your OK, send **Prompt 3.2-OK**:

   ```text
   Go ahead with those files.
   ```

5. Allow about 3 minutes per run. At 4 minutes, select **Stop** and score what is there.
6. **Score it.** Look at what changed, and run the tests:

   ```bash
   git status --short
   git diff
   mvn -q test
   # quiet mode: no "FAILURE" and no "Tests run" line with failures means all tests passed.
   # Ignore jacoco warnings
   ```

   `git diff` does not show new files. `git status --short` marks them with `??`. Open them in the
   editor.

   Also read the agent's last message. Did it stop and ask a question? Write **P** or **F** in the
   sheet, with a few words on why.
7. **Reset** before the next run. This keeps the run's changes in the git stash and cleans the tree:

   ```bash
   git stash push -u -m "lab 3.2 run"
   git reset --hard eval-base
   git status --short
   # must print nothing
   ```

   "No local changes to save" is fine. It means the run changed nothing.

Do not use `git clean` or `git stash pop` in this lab. Your runs stay in `git stash list`, newest
first, if you want to look at one again.

### Step 3 — Column A: the ordinary prompt (about 20 min)

Run all six, in order. Score and reset after each one.

**Prompt 3.2-A1** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-201. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2-A2** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-202. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2-A3** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-203. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2-A4** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-204. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2-A5** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-205. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2-A6** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-206. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

### Step 4 — Column B: the prompt file and your skill (about 20 min)

Same six tickets, same order, a new chat each time. Score and reset after each one.

**Prompt 3.2-B1** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-201 goal="List the postings for a client reference"
```

**Prompt 3.2-B2** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-202 goal="Reject postings dated more than 30 days ahead"
```

**Prompt 3.2-B3** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-203 goal="Add an account statement with a readable total"
```

**Prompt 3.2-B4** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-204 goal="Prove the posting limit with tests"
```

**Prompt 3.2-B5** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-205 goal="Handle the same reference and value date with a different amount"
```

**Prompt 3.2-B6** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-206 goal="Let Operations correct the narrative on a posting"
```

### Step 5 — Total, and read which rows changed (10 min)

Add up each column: two pass rates out of 6. Then fill in the **Changed?** column. Look at which
tickets changed, not only the total.

| What you see | What it means |
|---|---|
| Unclear tickets changed from fail to pass | Your stop conditions work. This part transfers to your own repository unchanged. |
| Tickets that failed in A pass in B | Your rules and output contract work. They work because Module 2 put the rules in files they can point at. |
| A ticket that passed in A fails in B | Your skill file is too strict. You would not see this without the tickets that A already passes. |
| Nothing changed | Module 2's files may already do the job for this repository. That is a real result, not a failed lab. |

Six tickets show a trend, not proof. Say so when you report it. It is still far better than an
opinion.

### Record

On your tally, fill in the **Lab 3.2** section:

- **A:** your column A pass rate, for example `3/6`
- **B:** your column B pass rate
- **Changed:** the tickets whose result changed between A and B

Update the table in the issue body, and post the same row as a comment. Report what you measured,
even if B scored lower than A.

### Then, and only then: compare with the reference

After your row is on the board, look at the team's reference skill file:

```bash
git show m4-start:.github/skills/account-change/SKILL.md
```

Do not score yourself against it. Look for stop conditions it has that yours does not. Write them
at the end of `eval-sheet.md`, under the heading "Stop conditions I did not think of". That list is
the real output of this module.

### If you are behind

If you have no working skill file and prompt file, start from the reference ones at `m4-start`:

```bash
git switch -c eval-lab-3.2-ref m4-start
git tag -f eval-base
```

Then do Steps 1 and 3 to 5 as written. On your tally, write **(reference)** after your B pass
rate. You measured the team's skill file, not your own.

If you are short of time, your trainer may ask you to run four tickets instead of six.

---

## Stretch lab 3.1+ (optional) — Reuse the skill on another ticket

**Goal:** make the skill file fully general, so that only the prompt file's inputs change per
ticket. Then use it on GB-142 without editing it. Do it if you finish Lab 3.1 early, before you start Lab
3.2. It sits at the end of this guide only because it is optional.

**Prompt 3.1+-A** · Ask mode · base model · **new chat**

```text
Read global-bank-account/.github/skills/account-change/SKILL.md and
global-bank-account/.github/prompts/gb-change.prompt.md.
List every line in the skill file that only makes sense for one ticket or one kind of feature,
such as reversals. For each line, say whether it should move to the prompt file as an input, or be
deleted. Do not change any file.
```

**Prompt 3.1+-B** · Agent mode · base model · **same chat**

```text
Make the changes you listed. Move each ticket-specific value out of the skill file. If a value
changes per ticket, add it to the prompt file as a new ${input:...} slot, and add it to the
argument-hint. Touch only these two files. Stop when both are saved, and show me the changes.
```

Commit the change:

```bash
git add .github/skills .github/prompts
git commit -m "Make the account-change skill ticket-independent"
```

**Prompt 3.1+-C** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-142 goal="Stop a retried payment from being booked twice"
```

**Check:** Copilot follows your skill file on a ticket it was not written for. The skill file did
not change during the run:

```bash
git diff --stat HEAD -- .github
# must print nothing
```

Did Copilot find the decision already written down in `docs/adr/`? Did it quote it? Then reset:

```bash
git stash push -u -m "lab 3.1+ GB-142"
git status --short
```

## Stretch lab 3.2+ (optional) — A seventh ticket

**Goal:** add a seventh eval ticket that tempts the agent to use a method that may not exist. Does
your pass rate hold?

**1. Create the ticket.** This ticket is not loaded by the script. Create it by hand in your Jira
project, from the browser. Type: **Story**. Summary: `[GB-208] Block postings to suspended accounts`, the same format the script uses.
Description:

```text
Compliance can suspend a ledger account. A suspended account must not receive or send any new
postings.

Use the existing LedgerAccount.isSuspended() check, and reject the posting with the standard
account-suspended reason from the error catalogue.

Acceptance criteria
1. A posting to or from a suspended account is rejected with a client error (4xx).
2. Postings between active accounts behave exactly as they do today.
3. Covered by tests.
```

Open `course/labs/lab-keys.md`. Add a row at the end of the table, with the key that Jira gave
the new ticket, in the same format as the other rows: `| GB-208 | ADLC-31 |` (use your own key).

**2. Add a row to your sheet.** Add GB-208 to `eval-sheet.md`, and write its pass criteria
**before** you run it.

**3. Run it twice.** Use the same run steps as Lab 3.2, including the reset after each run.

**Prompt 3.2+-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-208. Use the atlassian MCP tools to read
that Jira issue.
Implement it in the global-bank-account folder. Run "mvn test" there until it passes.
```

**Prompt 3.2+-B** · Agent mode · base model · **new chat**

```text
/gb-change ticket=GB-208 goal="Block postings to suspended accounts"
```

**Record:** your pass rates out of 7. Did B's rate hold? Which stop condition in your skill file
made the difference, if any? You can add this to the comment on your tally.
