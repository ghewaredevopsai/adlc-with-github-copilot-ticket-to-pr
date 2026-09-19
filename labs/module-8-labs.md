# Module 8 labs — Closing the loop

**Day 2** · Lab 8.1 and the capstone (+ stretch) · about 85 minutes · Repositories: `global-bank-account`
and `global-bank-transaction` · Start from: `capstone-start`

Lab 8.1 is short. You take one thing you learned in the last two days and save it where the next ticket
will find it. This is called **write-back**. Most of the words already exist in your spec, so you
copy and tidy, not write from nothing.

Then the **capstone**: one ticket, GB-186, through both repositories and all eight stages. You measure
it the same way as Lab 1.1. The result goes on the board next to your Lab 1.1 row, whatever it says.

Your trainer runs the Module 8 quiz (the last slide of the deck) before the capstone starts.

## Before you start

**1. Check the Confluence pages for Lab 8.1.** You created them before Day 1, with
[confluence-setup.md](confluence-setup.md). In a VS Code terminal, at the root of the course
repository:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 8
```

You should see `Confluence OK: space ...`, then `exists page ... 'Global Bank'` and `exists page ...
'Global Bank posting API - decisions'`. If it says `created` instead, that is fine: the script has just
made the pages you skipped. `labs/lab-keys.md` now has a `CONFLUENCE-PAGE` line. That line holds the id
of the decisions page. Your write-back pages go under it.

An error instead? See [If something goes wrong](confluence-setup.md#if-something-goes-wrong) in
`confluence-setup.md`.

Do **not** load the capstone ticket yet. Your trainer tells you when.

**2. Save your Day 2 work.** In each repository, commit anything that is still open on your GB-158
branches from Lab 7.1. Then run `git status`. It must say `nothing to commit`.

**3. Make the Lab 8.1 branches.** In a terminal:

```bash
cd ~/global-bank/global-bank-account && git switch -c GB-151-lab-8.1 capstone-start
cd ~/global-bank/global-bank-transaction && git switch -c GB-151-lab-8.1 capstone-start
```

**4. Open the workspace.** In VS Code, open `adlc-labs.code-workspace`. Check that the **atlassian**
MCP server is **Running** (**MCP: List Servers**).

---

## Lab 8.1 — Close the loop

**Goal:** save one decision and one correction where the next ticket will read them · **Ticket:**
GB-151 · **Timebox:** 15 min, steps 1–3 · **Output:** one ADR and one corrected document, in one commit

An **ADR** (Architecture Decision Record) is a short file in `docs/adr/`. It records a decision, the
option the team rejected, and why. The code shows *what* was built. Only an ADR shows what was
rejected.

The test for every candidate is the one from Module 2: **can an engineer work this out from the code,
easily?** If yes, do not write it. If no, write it, even if people need it only twice a year.

Steps 1 to 3 fit in the 15 minutes. The rest of the write-back, the ticket comment and the Confluence
page, is in stretch lab 8.1+, below.

### Step 1 — Find the candidates

**Prompt 8.1-A** · Agent mode · base model · **new chat**

```text
I want to write back what I learned in this course. Do not change any file in this step.
1. Search the global-bank-account and global-bank-transaction folders for spec files: files
   named spec.md, and files under a specs/, handoff/ or docs/contract-changes/ folder. Also look on
   my other local branches. Run
   "git branch" in each repository, and read files there with "git show", giving the branch
   and the path.
   Do not switch branch, and do not run git stash, git checkout or git reset.
2. Read course/labs/lab-keys.md to find my Jira keys for GB-151, GB-119, GB-158 and GB-163.
   Use the atlassian MCP tool jira_get_issue to read each of those four issues, with comments.
   Make no more than four Jira calls.
3. List up to six write-back candidates. A candidate is one of these:
   - a decision with a rejected option, from a spec
   - a rule that was hard to find, for example in a closed ticket or a comment
   - a document in either repository that the work made wrong
   For each candidate, give its source (file or ticket), and one line on what it says.
   Then apply this test: "Can an engineer work this out from the code, easily?"
   Mark each candidate WRITE or SKIP, with one line of reason.
Stop after the list.
```

**What you should see:** Copilot asks to run `git` commands and four `jira_get_issue` calls. Read each
request before you select **Allow**. Then it shows a list of candidates, each marked WRITE or SKIP.

**Check:** does every candidate name a source you can open? Now add one thing yourself: open your chat history (the clock icon at the top of the Chat view) and
look at your Day 2 chats. Did you find something there that is not on the list? Note it on paper.

### Step 2 — Write one ADR

In Module 4 you saw the design agent's spec for GB-151, the reversal ticket. It already holds the
decision, the rejected option and the rule that decided it. You promote that spec to an ADR. You do
not write it from nothing. The prompt holds that spec's text as slide 11 of the Module 8 deck shows it.

**Prompt 8.1-B** · Agent mode · base model · **same chat**

```text
Write one ADR from this text, which is the design agent's spec for GB-151:
## Recommendation
Reversal creates a second posting with debit and credit swapped, and marks the original REVERSED.
## Why not change it in place
docs/glossary.md: "Reversal - a status change on the original posting. We do not delete
postings." Changing it in place would lose the original instruction.
## Deciding rule
copilot-instructions.md: balances are derived from entries, never stored.

Create global-bank-account/docs/adr/ADR-011-reversal-as-a-second-posting.md with exactly this
shape:
- Title: "# ADR-011 — Reversal as a second posting"
- A status line: "Status: Accepted · YYYY-MM-DD · GB-151", with today's date. Get the date
  from the terminal.
- An owner line: "Owner: payments-platform"
- "## Decision": the recommendation, in one or two sentences.
- "## Rejected": the option that was rejected, and why. Name the rule that decided it, and the
  file that rule comes from.
- "## Consequences": what is now true because of this decision, for reports and for callers.
Copy the words above where you can. Add nothing they do not say. If you think something is
missing, tell me instead of adding it.
Add one line for the new ADR to docs/adr/README.md, in the same format as the lines already there.
Change no other file. Show me the ADR and the new README line when you finish.
```

**What you should see:** one new file, about 15 lines, in `global-bank-account/docs/adr/`, and one new
line in `docs/adr/README.md`. The "Rejected" section names a rule and a file.

**Check:** read the ADR once. Does it say what was **rejected**? An ADR with no rejected option only
describes the code. If it has none, ask Copilot to add it from the spec text.

### Step 3 — Fix one document the work made wrong

**Prompt 8.1-C** · Agent mode · base model · **same chat**

```text
Find the documents that are now wrong, because of the new ADR-011 or because of the candidates
marked WRITE in step 1. Look in docs/ and .github/ in both repository folders.
Show me each wrong line, the file it is in, and why it is wrong. Then pick the ONE that would
mislead the next person most, and fix only that document. Change the fewest lines you can.
Keep the author's own wording where it is still true.
Show me the diff when you finish.
```

**What you should see:** a short list of wrong lines, then one small change to one document.

**Check:** in the terminal, commit the ADR and the fix together. This is the same-PR rule: the
knowledge changes with the work that made it wrong.

```bash
cd ~/global-bank/global-bank-account
git status
git add docs .github
git commit -m "GB-151: ADR-011 reversal as a second posting, and fix the doc it made wrong"
```

If the fix is in `global-bank-transaction`, commit it there on its `GB-151-lab-8.1` branch, with the
same message.

### Record

Lab 8.1 is not a measured run. Nothing goes on the board. Keep one note for the debrief: which
candidate did you mark SKIP, and why?

### If you are behind

Stop at the end of step 2 and commit the ADR alone. The capstone starts from `capstone-start` in both
repositories. It needs nothing from Lab 8.1.

---

## Stretch lab 8.1+ (optional)

**Goal:** finish the write-back the clock dropped: the Confluence page, the ticket comment, and one
deletion. Do it only if you finish steps 1–3 early. Stay in the same chat.

All three steps only **add** something, or remove one line you choose. Copilot never edits a page
that someone else owns. This is the "safe alone" level from Module 6 and slide 10 of this module.

**Prompt 8.1-D** · Agent mode · base model · **same chat**

```text
Publish the ADR-011 decision to Confluence, as a pointer for people who do not read the
repository. Read course/labs/lab-keys.md. Find my Confluence space key, and the CONFLUENCE-PAGE
id. That id is the parent page.
Use the atlassian MCP tool confluence_create_page to create ONE new page in that space, under
that parent. Title: "ADR-011 — Reversal as a second posting". Body, short:
- the decision, in one sentence
- the rejected option, in one sentence
- where the full ADR lives: docs/adr/ADR-011-reversal-as-a-second-posting.md in
  global-bank-account, branch GB-151-lab-8.1
- the ticket: GB-151
Do not edit the parent page or any other page. Show me the new page's title and id.
```

**What you should see:** one `confluence_create_page` request. Read it before you select **Allow**. It
must name the parent id from `lab-keys.md`.

**Check:** open Confluence in the browser. The new page sits under "Global Bank posting API -
decisions". The parent page is unchanged.

**Prompt 8.1-E** · Agent mode · base model · **same chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-151. Use the atlassian MCP tool
jira_add_comment to add ONE comment to that issue. Say, in three short lines:
- the decision is recorded in docs/adr/ADR-011-reversal-as-a-second-posting.md, in
  global-bank-account, branch GB-151-lab-8.1
- the Confluence page "ADR-011 — Reversal as a second posting" points to it
- the document that was fixed in the same commit, and what was wrong with it
Start the comment with "Write-back from the ADLC course, Lab 8.1:".
Do not change the issue's status, fields or assignee. Show me the comment you added.
```

**Check:** open the issue in Jira. The comment is there, and nothing else on the issue changed.

**Prompt 8.1-F** · Agent mode · base model · **same chat**

```text
Now find something to delete. Read the instruction files and the skill file in
global-bank-account: .github/copilot-instructions.md, .github/instructions/*.instructions.md and
.github/skills/account-change/SKILL.md.
Find ONE line that did not help any lab in the last two days, or that repeats what another file
already says. Show me the line, its file, and why you think it can go.
Do not edit anything. Stop and wait for my decision.
```

**What you should see:** one line, and a reason. You decide. If you agree, delete the line yourself
and commit it with `git commit -am "Remove a line that no lab needed"`. If you disagree, keep it,
and say why at the debrief.

A knowledge base that only grows is one that nobody trusts a year later. This is the only step in
the course where you practise removing something.

---

## Capstone — GB-186, one ticket through every stage

**Goal:** take GB-186 through all eight stages, across both repositories, and measure it like Lab 1.1
· **Ticket:** GB-186 · **Timebox:** 50 min of work + 20 min to record and debrief · **Output:** two
branches ready for pull requests, the write-back, and the last row on the board

**GB-186 — A payroll batch must post all-or-nothing.** Today, global-bank-transaction posts a payroll
run one item at a time. If one item fails, the ledger holds part of the batch. The ticket has six
acceptance criteria and touches both repositories. Read it through the stages, not before.

**Atomic** means all or nothing: every posting in the batch is saved, or none is.

### Two rules — the second is the hard one

- **Measure it the same way as Lab 1.1.** The same six counters, counted by the same person (you), as
  you go. Use the **base model** for every stage, as in Lab 1.1.
- **Work at your normal pace.** Lab 1.1 was a normal working day. The capstone must be one too. A
  careful run compared with a careless one proves nothing.

**Start the clock** at your first prompt. **Stop it** when you finish stage 8, or at 50 minutes, the
earlier of the two. This is the same clock rule as every lab: stop when all the lab's checks pass, or at
the timebox. In the capstone, "all checks pass" means stage 8 is done. If the clock beats you, stop and write down which stage you reached. An honest
unfinished run is worth more than a rushed complete one.

**One counting note.** In stage 2 the spec may raise an open question that no file in either
repository can answer. When you ask the trainer, that is not an **Asked**. Asked counts only
questions that a file could have answered.

### Before you start the capstone

**1. Load the ticket** when your trainer says so:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module capstone
```

You should see `created GB-186 ...`, and `labs/lab-keys.md` now has a line for GB-186.

**2. Make the capstone branches** in both repositories. In a terminal:

```bash
cd ~/global-bank/global-bank-account && git switch -c GB-186-capstone capstone-start && mvn test | grep "Tests run:" | tail -1
cd ~/global-bank/global-bank-transaction && git switch -c GB-186-capstone capstone-start && mvn test | grep "Tests run:" | tail -1
```

Expect `Tests run: 4, Failures: 0` in `global-bank-account` and `Tests run: 2, Failures: 0` in
`global-bank-transaction`.

**3. Open your tally** (your issue on the board) at the capstone row.

### The custom agents

Five stages use the four custom agents from Module 4: **design**, **coding**, **test** and **review**.
To use one, open the agent list in the Chat view (next to the mode list) and pick the agent. Then
paste the prompt. Pick the agent **before** you paste.

The stages that say **default agent** use plain Agent mode, with no custom agent picked.

### Stage 1 — Pull the ticket, within a budget

**Prompt C1** · Agent mode · default agent · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira keys for GB-186 and GB-158.
Use the atlassian MCP tool jira_get_issue to read GB-186 with its comments, then GB-158, which
GB-186 names. Make no more than three Jira calls. Do not search for other tickets.
Write a short summary to global-bank-account/specs/GB-186-ticket.md: the description in three
lines, the six acceptance criteria word for word, the notes, and what GB-158 says about the
sequencing rule. Quote the tickets only. Do not look the rule up.
Change no other file. Stop when the file is written.
```

**What you should see:** two or three `jira_get_issue` calls, then one new file. Every later stage
reads this file, not Jira. You pull once.

**Check:** the file has six numbered criteria, copied word for word.

### Stage 2 — Write the spec

**Prompt C2** · Agent mode · agent: **design** · base model · **new chat**

```text
Write the spec for GB-186. The ticket is in global-bank-account/specs/GB-186-ticket.md.
GB-186 changes both repositories. Read:
- in global-bank-account: docs/adr/, docs/architecture.md, docs/glossary.md,
  .github/copilot-instructions.md
- in global-bank-transaction: .github/copilot-instructions.md and docs/contract.md
Your spec must have these sections:
1. The problem, in one paragraph.
2. Acceptance criteria, numbered AC1 to AC6, one behaviour each, each one testable.
3. Out of scope.
4. Assumptions.
5. Two or three options, with a recommendation and the rule that decides it. Name the file
   each rule comes from.
6. Open questions: anything neither repository can answer. Ask them. Do not guess.
Write no code and edit no files. Show the spec here in the chat.
```

**What you should see:** a spec in the chat, with six numbered criteria, options, a recommendation,
and at least one open question. The design agent writes no files, by design.

**Save it:** create the file `global-bank-account/specs/GB-186.md`. Select **Copy** on the agent's
answer, and paste it into the file. That file is the hand-off for every later stage.

**Then, you:** read the open questions. If a question needs a business answer, ask your trainer. In
this room, the trainer speaks for Client Money Ops, who reported the ticket. Type the answer under the
question in `specs/GB-186.md`, with "Answer from Client Money Ops (trainer):" in front. Do not let
Copilot choose the answer.

### Stage 3 — Plan it, then challenge the plan

**Prompt C3** · Agent mode · agent: **coding** · base model · **new chat**

```text
Plan the change for GB-186. Read the spec global-bank-account/specs/GB-186.md, including the
answers under the open questions. Do not edit any code yet.
Write the plan to global-bank-account/specs/GB-186-plan.md, as numbered small steps. For each
step give: the repository, the files, and the acceptance criterion it serves.
Order the steps like this: the contract between the two repositories first, then the producer
(global-bank-account), then the consumer (global-bank-transaction).
Stop and show me the plan. Do not edit any other file.
```

Now challenge the plan. The challenger must not be the agent that wrote it. The design agent has not
seen any code, and there is none yet.

**Prompt C4** · Agent mode · agent: **design** · base model · **new chat**

```text
Challenge this plan: global-bank-account/specs/GB-186-plan.md. The spec is
global-bank-account/specs/GB-186.md. Answer four questions about the plan:
1. Which acceptance criterion does each step serve? List steps with none, and criteria with none.
2. What does this conflict with? Name the ADR, convention, instruction file or existing test.
3. What is the smallest change that meets the spec? Say what in the plan is bigger than that.
4. What would make this the wrong approach? Imagine it failed in production, and say why.
Give each answer in at most four lines. Do not edit any file.
```

**Then, you:** decide what to change. If the plan needs a change, go back to the coding agent's chat
from C3 and ask for it in one sentence. That counts as a turn, not as rework.

### Stage 4 — Build across both repositories, contract first

Go back to the **coding agent's chat from C3** for all three prompts in this stage.

**Prompt C5** · Agent mode · agent: **coding** · base model · **same chat as C3**

```text
Do the contract step of the plan only. Write the batch request and response shapes, the
error cases, and the merge order into global-bank-transaction/docs/contract.md. Keep what is
still true, and change only what GB-186 changes. Follow ADR-009 in global-bank-account.
Do not change any code yet. Show me the diff of docs/contract.md, then stop.
```

**Prompt C6** · Agent mode · agent: **coding** · base model · **same chat**

```text
Now do the producer steps of the plan, in global-bank-account only. Existing single postings
must keep working unchanged. Follow the contract you just wrote.
Run "mvn test" in global-bank-account until it passes. Do not write the new tests for GB-186.
The test agent writes those in stage 5.
When you finish, list the files you changed, and which steps of the plan are done.
```

**Prompt C7** · Agent mode · agent: **coding** · base model · **same chat**

```text
Now do the consumer steps of the plan, in global-bank-transaction only. Keep the mirrored
client types in step with the producer, as docs/contract.md says.
Run "mvn test" in global-bank-transaction until it passes. If an existing test asserts
behaviour that GB-186 changes, stop and tell me which test and why, before you change it.
When you finish, list the files you changed, and which steps of the plan are done.
```

**What you should see:** after C6 and C7, both repositories build and their tests pass. You have not
yet checked the acceptance criteria. That is next.

### Stage 5 — Tests from the ticket, not from the code

The test agent works from the ticket and the spec's criteria. It must not see how the coder reasoned,
so it gets a new chat.

**Prompt C8** · Agent mode · agent: **test** · base model · **new chat**

```text
Write the tests for GB-186. Your source of truth is the ticket,
global-bank-account/specs/GB-186-ticket.md, and the numbered criteria AC1 to AC6 in
global-bank-account/specs/GB-186.md. Do not read specs/GB-186-plan.md.
Write tests in both repositories, under src/test/ only. Run "mvn test" in each.
Do not run git stash, git checkout or git reset. If you cannot run a new test against the old
code without them, say so in the report.
Show the test report in the chat: one line per criterion, AC1 to AC6, marked covered or not
covered, with the test that covers it. Then stop.
```

**What you should see:** new tests in both repositories, and a report with six lines in the chat. A
criterion marked "not covered" is a finding, not a failure. Leave it in the report.

**Save it:** the test agent edits only under `src/test/`, so you save the report. Create
`global-bank-account/specs/GB-186-test-report.md` and paste the report into it.

### Checks — do the acceptance criteria hold?

Run these after stage 5. **Paste the repair prompt only when a check fails.** Paste it in the
coding agent's chat (from C3). A run has at most three repairs.

**Check 1 — both builds (AC6).** In a terminal:

```bash
cd ~/global-bank/global-bank-account && mvn test | grep "Tests run:" | tail -1
cd ~/global-bank/global-bank-transaction && mvn test | grep "Tests run:" | tail -1
```

Pass: `Failures: 0, Errors: 0` in both, and more tests than the 4 and 2 you started with.

**Start both services** for the next checks. Use two new terminals, and leave them running:

```bash
cd ~/global-bank/global-bank-account && mvn spring-boot:run
```

```bash
cd ~/global-bank/global-bank-transaction && mvn spring-boot:run
```

Wait until each one prints `Started`. The account service listens on port 8086, and the transaction
service on port 8087. Run the next checks in a third terminal.

**Check 2 — a bad item posts nothing, and the response names it (AC1, AC2, AC4).** Item E2 goes to an
account that does not exist.

```bash
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
curl -s -X POST http://localhost:8087/transaction/api/v1/disbursements \
  -H "Content-Type: application/json" -w "\nHTTP %{http_code}\n" \
  -d '{"batchId":"PAY-CHK-1","valueDate":"2026-09-30","items":[
       {"employeeAccountId":"ACC-CLIENT-001","amountMinor":150000,"reference":"E1"},
       {"employeeAccountId":"ACC-NO-SUCH","amountMinor":150000,"reference":"E2"},
       {"employeeAccountId":"ACC-CLIENT-002","amountMinor":150000,"reference":"E3"}]}'
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
```

Pass: `balanceMinor` for ACC-PAYROLL is **the same** before and after. The response names item E2 and
says why it was rejected.

**Check 3 — the fixed batch posts in full (AC1, AC2).** Operations fix E2 and re-send the same batch.

```bash
curl -s -X POST http://localhost:8087/transaction/api/v1/disbursements \
  -H "Content-Type: application/json" -w "\nHTTP %{http_code}\n" \
  -d '{"batchId":"PAY-CHK-1","valueDate":"2026-09-30","items":[
       {"employeeAccountId":"ACC-CLIENT-001","amountMinor":150000,"reference":"E1"},
       {"employeeAccountId":"ACC-CLIENT-002","amountMinor":150000,"reference":"E2"},
       {"employeeAccountId":"ACC-CLIENT-002","amountMinor":150000,"reference":"E3"}]}'
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
```

Pass: ACC-PAYROLL's `balanceMinor` is now **450000 lower** than in check 2 (three items of ₹1,500).

**Check 4 — the size limit (AC3).** This makes two test batches, of 500 and 501 items of ₹1 each, in
the `target/` folder (git ignores it):

```bash
cd ~/global-bank/global-bank-transaction
python -c "import json;[json.dump({'batchId':'PAY-SIZE-%d'%n,'valueDate':'2026-09-30','items':[{'employeeAccountId':'ACC-CLIENT-002','amountMinor':100,'reference':'E%d'%i} for i in range(1,n+1)]},open('target/batch-%d.json'%n,'w')) for n in (500,501)]"
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
curl -s -X POST http://localhost:8087/transaction/api/v1/disbursements \
  -H "Content-Type: application/json" -d @target/batch-501.json -w "\nHTTP %{http_code}\n" | tail -c 300
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
curl -s -X POST http://localhost:8087/transaction/api/v1/disbursements \
  -H "Content-Type: application/json" -d @target/batch-500.json -w "\nHTTP %{http_code}\n" | tail -c 300
curl -s http://localhost:8086/account/api/v1/accounts/ACC-PAYROLL/balance; echo
cd ..
```

Pass: the 501-item batch posts **nothing** (the balance does not move) and the response says the
batch is too large. The 500-item batch posts in full: the balance falls by exactly **50000**.

**Check 5 — single postings still work (AC5).**

```bash
curl -s -X POST http://localhost:8086/account/api/v1/postings \
  -H "Content-Type: application/json" -w "\nHTTP %{http_code}\n" \
  -d '{"clientReference":"SINGLE-CHK-1","debitAccountId":"ACC-CLIENT-001","creditAccountId":"ACC-FEES","amountMinor":2500,"valueDate":"2026-09-30","narrative":"Single posting check"}'
```

Pass: `HTTP 201`, and the response has a `postingId`.

Stop both services with `Ctrl+C` when the checks pass.

**Repair prompt C-R** · Agent mode · agent: **coding** · **same chat as C3**. Paste it only when a
check fails. It counts as a turn and as rework.

```text
A check failed. This is what I saw:
<paste the failing output here>
Fix only this. Run "mvn test" in global-bank-account and global-bank-transaction again, and
tell me which acceptance criteria are now met.
```

After a repair, run the failed check again. The services do not reload code on their own: stop them
with `Ctrl+C` and start them again first.

### Stage 6 — The review agent, then you

The review agent did not write this code, and it is not told why it was written this way. That is
why it gets a new chat.

**Prompt C9** · Agent mode · agent: **review** · base model · **new chat**

```text
Review the change for GB-186. It is on branch GB-186-capstone in both global-bank-account and
global-bank-transaction. See the diff with "git diff capstone-start" in each repository.
The ticket is global-bank-account/specs/GB-186-ticket.md, and the criteria are AC1 to AC6 in
global-bank-account/specs/GB-186.md. Do not read specs/GB-186-plan.md or any summary of how
the change was made.
Review both repositories as one change: check that the producer and the consumer agree.
Write your review report in this chat. Follow your agent definition. Do not edit any file.
```

**What you should see:** a report with findings by severity, each naming a file, a line and a rule.

Now your own review. Read the **file list** before any description. This stops a confident summary
from setting what you look for.

**Prompt C10** · Agent mode · default agent · base model · **new chat**

```text
For global-bank-account and for global-bank-transaction, run "git diff --stat capstone-start"
and show me the output. Do not explain, summarise or judge the changes.
```

Then read the diff yourself, and answer the four questions from slide 5, in one line each. Write them
at the end of `global-bank-account/specs/GB-186.md`, under "## Human review":

1. Should we build this at all?
2. Will this be easy to live with?
3. Does it clash with anything outside this repository?
4. What did the review report not mention?

If the review found a real problem, fix it with the repair prompt in the coding agent's chat. That
counts as rework.

### Stage 7 — Two linked pull requests, merge order written down

**Prompt C11** · Agent mode · default agent · base model · **new chat**

```text
Write two pull request descriptions for GB-186, one per repository. Build every line from these
three sources only: global-bank-account/specs/GB-186.md, the diff ("git diff capstone-start"
in each repository), and global-bank-account/specs/GB-186-test-report.md. If a claim has no
source, leave it out.
Each description has:
- What changed, and which criterion each part meets
- Test evidence: one line per criterion, with the test name, or "not tested"
- Merge order: which pull request merges first, and why (follow ADR-009 in
  global-bank-account), and that each links to the other
- Rollback: which one to revert first
- Write-back: did this ticket produce a decision, a rule that was hard to find, or a document
  that is now wrong? If yes, name it. If no, say "none".
Save them as global-bank-account/specs/GB-186-pr-account.md and
global-bank-account/specs/GB-186-pr-transaction.md. Change no other file.
```

**Check:** does every line trace to the spec, the diff or the test report? A smooth description with
no criteria, no file count and no test names is a warning sign.

**Commit** in both repositories:

```bash
cd ~/global-bank/global-bank-account && git add -A && git commit -m "GB-186: post a payroll batch all-or-nothing"
cd ~/global-bank/global-bank-transaction && git add -A && git commit -m "GB-186: send each payroll run as one batch"
```

You do not push. Your committed branches and the two description files are the output of this stage.
In your own team, these two files are what you paste into the two pull requests, opened in the merge
order they give, each linking to the other.

### Stage 8 — Write back: the repository, the ticket, the page

Three short prompts. Each one only adds something, or fixes a document that this change made wrong.

**Prompt C12** · Agent mode · default agent · base model · **new chat**

```text
GB-186 is built on branch GB-186-capstone in both repositories. Find the documents in docs/ and
.github/ of both repositories that this change made wrong. Use "git diff capstone-start" in
each repository to see the change, and global-bank-account/specs/GB-186.md for the decisions,
including the answers under the open questions.
Show me each wrong line and why. Then fix them, changing the fewest lines you can.
If the spec records a decision with a rejected option that no ADR holds, draft it as the next
free ADR number in global-bank-account/docs/adr/, in the same shape as ADR-009, and add it to
docs/adr/README.md.
Show me the diff when you finish.
```

Commit it in the same branches, so the knowledge travels with the code:

```bash
cd ~/global-bank/global-bank-account && git add -A && git commit -m "GB-186: update the docs this change made wrong"
cd ~/global-bank/global-bank-transaction && git add -A && git commit -m "GB-186: update the docs this change made wrong"
```

**Prompt C13** · Agent mode · default agent · base model · **same chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-186. Use the atlassian MCP tool
jira_add_comment to add ONE comment to that issue. Start it with "Capstone write-back:". Then,
in short lines:
- the branch GB-186-capstone in both repositories, and the merge order
- the answer to each open question, and who gave it
- the documents fixed and any ADR added in this change
- which acceptance criteria are covered by tests, from specs/GB-186-test-report.md
Do not change the issue's status, fields or assignee. Show me the comment you added.
```

**Prompt C14** · Agent mode · default agent · base model · **same chat**

```text
Read course/labs/lab-keys.md. Find my Confluence space key and the CONFLUENCE-PAGE id.
Use the atlassian MCP tool confluence_create_page to create ONE new page in that space, under
that parent. Title: "GB-186 — Payroll batch posts all-or-nothing". Body, short:
- the decision in one sentence, and the option rejected
- the answer to the open question, and who gave it
- where the details live: specs/GB-186.md and any new ADR in global-bank-account, branch
  GB-186-capstone
Do not edit the parent page or any other page. Show me the new page's title and id.
```

**Stop the clock.** Stage 8 is done.

### Record

Fill the **capstone row** of your tally, in your issue on the board. Then post the row as a comment.

- The six counters: turns, tool calls, asked, rework, churn, clock.
- **Asked, rework and churn per acceptance criterion.** Divide your capstone numbers by **6** and your
  Lab 1.1 numbers by **5**. These three columns compare fairly. Turns, tool calls and clock do not:
  GB-186 is two repositories, six criteria and eight stages, so those will be higher for size alone.
- The stage you reached, if you did not finish.
- Which stage cost the most time, and was it worth it?

Report what you measured, even if it is worse than Lab 1.1. A first run of all eight stages includes
the cost of learning them. That is a finding, not a failure.

### If you are behind

There is no catch-up tag for the capstone. Stop where you are when the 50 minutes end, and record the
stage you reached. That stage is often the one that costs most, which is itself a finding.

---

## Stretch lab Capstone+ (optional)

**Goal:** review another participant's capstone change with your own review agent. Nobody pushes, so
you swap patch files. Pair with a neighbour who has also finished stage 8.

On Windows, run these commands in **Git Bash**: a patch file written by PowerShell does not apply.

**1. Export your change** and send the two files to your neighbour, in the workshop chat:

```bash
cd ~/global-bank/global-bank-account && git diff capstone-start GB-186-capstone > ~/GB-186-account.patch
cd ~/global-bank/global-bank-transaction && git diff capstone-start GB-186-capstone > ~/GB-186-transaction.patch
```

**2. Apply your neighbour's change** on a new branch in each repository. Save their files as
`~/neighbour-account.patch` and `~/neighbour-transaction.patch` first. Commit your own work before you
switch.

```bash
cd ~/global-bank/global-bank-account && git switch -c GB-186-neighbour capstone-start && git apply --index ~/neighbour-account.patch
cd ~/global-bank/global-bank-transaction && git switch -c GB-186-neighbour capstone-start && git apply --index ~/neighbour-transaction.patch
```

**3. Review it:**

**Prompt C+** · Agent mode · agent: **review** · base model · **new chat**

```text
Review another participant's GB-186 change. It is applied, not committed, on branch
GB-186-neighbour in global-bank-account and global-bank-transaction. See it with "git diff HEAD"
in each repository. Its specs/ files are part of the change: do not read them.
The criteria are the six numbered acceptance criteria in course/labs/tickets/GB-186.md. Judge
the change against those only.
Write your review report in this chat. Follow your agent definition. Do not edit any file.
```

Then compare the report with your neighbour's own review in their stage 6. What did your agent find
that theirs did not, and why?

**4. Clean up** and go back to your own branches:

```bash
cd ~/global-bank/global-bank-account && git reset --hard && git switch GB-186-capstone
cd ~/global-bank/global-bank-transaction && git reset --hard && git switch GB-186-capstone
```
