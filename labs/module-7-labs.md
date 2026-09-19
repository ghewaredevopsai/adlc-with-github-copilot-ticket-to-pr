# Module 7 labs — Multi-repo engineering

**Day 2** · Labs 7.1, 7.2 (+ stretch) · about 75 minutes · Repositories: `global-bank-account` and
`global-bank-transaction` · Start from: `m7-start` (Lab 7.1) and branch `m7.2-review` (Lab 7.2)

These are the first labs that use both repositories. In Lab 7.1 you take one ticket, GB-158, across
the boundary between two services. You agree the contract first, then change the producer, then write
two linked pull request descriptions. In Lab 7.2 you review a change that someone else already wrote.
The review agent looks at each side alone, then at both together. Watch what it can see from one
repository, and which file lets it see across the boundary.

You merge nothing in these labs. Both labs stop where a person would decide.

## Words used in these labs

| Word | Meaning here |
|---|---|
| **Producer** | The service that offers the API. Here: `global-bank-account`, which serves the posting API. |
| **Consumer** | The service that calls the API. Here: `global-bank-transaction`, which sends payroll postings. |
| **Contract** | What the API accepts and returns. Both sides depend on it. |
| **Mirrored type** | A class in the consumer, copied by hand from a producer class. `client/PostingRequest` is one. |
| **Value date** | The date a posting takes effect in the accounts. Postings already carry `valueDate`. |
| **Settlement date** | The date the money actually moves. GB-158 adds it as `settlementDate`. |
| **Additive change** | A change that only adds something optional. Old callers keep working unchanged. |
| **Rollback** | Undoing a change that is already merged or deployed. |

## Before you start

**1. Load this module's ticket into your Jira.** In a terminal, at the root of the course repository:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 7
```

It loads **GB-158** and adds its key to `labs/lab-keys.md`.

**2. Open the workspace.** In VS Code, open `adlc-labs.code-workspace`. You need all three folders:
`course`, `global-bank-account` and `global-bank-transaction`.

**3. Make a branch in each repository.** In a terminal:

```bash
cd ~/global-bank/global-bank-account
git fetch --tags origin
git switch -c GB-158-settlement-date m7-start
mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0

cd ~/global-bank/global-bank-transaction
git fetch --tags origin
git switch -c GB-158-send-settlement-date m7-start
mvn test
# expect: Tests run: 2, Failures: 0, Errors: 0
```

Both branch names carry the ticket key. Anyone who looks at either repository can see the pair.

**4. Read the consumer's contract file (3 minutes).** Open
`global-bank-transaction/docs/contract.md`. It lists what the consumer calls in the producer. It says
the request and response types are copied by hand. It also says the merge-order rule is ADR-009, and
ADR-009 lives in the **producer** repository. That is the problem this module is about: a rule in one
repository binds a team that cannot see it.

---

## Lab 7.1 — Cross-repo GB-158, contract first

**Goal:** Agree the contract change before any code, ship the producer side as an additive change,
and write two linked pull request descriptions. · **Ticket:** GB-158 · **Timebox:** 30 min ·
**Output:** a contract-change document, a green producer branch, and two pull request descriptions

Work in this order: contract, then shape, then producer, then descriptions. Step 4 (the consumer) is
optional. Do it only if you are ahead of the clock.

### Step 1 — Write the contract change first

**Prompt 7.1-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Then read global-bank-transaction/docs/contract.md and
global-bank-account/docs/adr/ADR-009-versioning-the-posting-contract.md.
Before any code is written, write the contract change for GB-158 as a short document.
Create the file global-bank-account/docs/contract-changes/GB-158-settlement-date.md with four parts:
1. The field: its name, its JSON type and format, and whether it is optional.
2. What happens when a caller does not send it, and which service applies the default.
3. What GET /api/v1/postings/{id} returns for it.
4. What stays the same for a caller that does not know about the field.
Keep the document under 25 lines. Do not change any Java file.
Stop and show me the document.
```

**What you should see:** Copilot reads the ticket and the two files. It creates one new Markdown file
and shows it to you. No Java file changes.

**Check:** read the document yourself. Compare part 2 with acceptance criterion 1 of the ticket. Then
run this in `global-bank-account`:

```bash
git status --short
# expect only: ?? docs/contract-changes/
```

If part 2 does not match the ticket, tell Copilot what is wrong in the same chat, in one sentence.

### Step 2 — Choose the shape of the change

**Prompt 7.1-B** · Agent mode · base model · **same chat**

```text
Now choose how to ship this contract change. The options are: an additive change, expand-and-contract,
or a new versioned endpoint under /api/v2. Use ADR-009 and acceptance criterion 4 of the ticket to decide.
Add a section called "Shape" to global-bank-account/docs/contract-changes/GB-158-settlement-date.md.
Name the option you chose in one line. Give the reason in two or three sentences.
Then say in one line each why the other two options are not needed.
Also add a section called "Order": which repository merges first, and why, in two sentences.
Do not change any Java file. Stop and show me the new sections.
```

**What you should see:** two new sections in the same document. Each names an ADR rule or an
acceptance criterion as its reason.

**Check:** does the "Order" section give a reason, or only a rule? A reason explains what would break
in the other order. Write the shape and the order on your worksheet (see **Record**).

### Step 3 — The producer change: additive only

**Prompt 7.1-C** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue.
Implement the producer side of GB-158 in the global-bank-account folder only.
Follow the agreed contract in global-bank-account/docs/contract-changes/GB-158-settlement-date.md.
Do not re-decide it.
Rules for this change:
- It must be additive. A caller that does not send settlementDate must see no change in behaviour.
- When settlementDate is missing, the posting's value date is stored as its settlement date.
- Store settlementDate on the posting. Return it from POST /api/v1/postings and GET /api/v1/postings/{id}.
- Do not edit the four existing tests in PostingServiceTest. Add new tests, including one for the
  case where settlementDate is missing.
- Do not change any file in the global-bank-transaction folder.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say how acceptance criteria 1, 2 and 4 are met.
```

**What you should see:** changes in the `posting` package (`api/`, `domain/`, `service/`), new tests,
and a passing build. Nothing changes in `global-bank-transaction`.

**Check 1 — the build.** In `global-bank-account`:

```bash
mvn test
# expect: Tests run: 5 or more, Failures: 0, Errors: 0
```

**Check 2 — the existing tests are untouched.** This is the simple test for "additive":

```bash
git diff --numstat m7-start -- src/test
# each line shows: lines added, lines removed, file. The second number must be 0.
```

**Check 3 — old and new callers, against the running service.** Start the service in one terminal:

```bash
cd ~/global-bank/global-bank-account
mvn spring-boot:run
```

In a second terminal, send a posting the old way, with no `settlementDate`:

```bash
curl -s -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"GB158-OLD","debitAccountId":"ACC-CLIENT-001","creditAccountId":"ACC-FEES","amountMinor":1234,"valueDate":"2026-03-01","narrative":"Old caller"}'
```

Look at `settlementDate` in the reply. Compare it with acceptance criterion 1.

Now send one with the new field:

```bash
curl -s -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"GB158-NEW","debitAccountId":"ACC-CLIENT-001","creditAccountId":"ACC-FEES","amountMinor":1234,"valueDate":"2026-03-01","settlementDate":"2026-03-03","narrative":"New caller"}'
```

Copy the `postingId` from that reply, and read the posting back (acceptance criterion 2):

```bash
curl -s http://localhost:8086/account/api/v1/postings/<postingId from the reply>
```

Stop the service with **Ctrl+C** when you finish.

If a check fails, use the repair prompt below. Then commit your work in `global-bank-account`:

```bash
git add -A
git commit -m "GB-158: add optional settlementDate to the posting contract"
```

**Repair prompt 7.1-R** · Agent mode · **same chat** · only when a check fails

```text
A check failed. This is what I saw:
<paste the failing output here>
Fix only this. Run "mvn test" in global-bank-account again, and tell me which acceptance
criteria are now met.
```

### Step 4 — The consumer change (optional: only if you are ahead of the clock)

**Prompt 7.1-D** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue.
Implement the consumer side of GB-158 in the global-bank-transaction folder only.
The producer side is done. Its agreed contract is in
global-bank-account/docs/contract-changes/GB-158-settlement-date.md. Read that file, and read no
other file in the global-bank-account folder.
Also read global-bank-transaction/.github/copilot-instructions.md and global-bank-transaction/docs/contract.md.
Make these changes:
- Add settlementDate to the mirrored type client/PostingRequest.
- Let POST /api/v1/disbursements accept an optional settlementDate for the whole batch. Send it on
  every posting in the batch. When it is missing, leave it empty, so the producer applies its default.
- Update docs/contract.md so that its section on the mirrored types mentions settlementDate.
- Do not edit the two existing tests in PayrollDisbursementServiceTest. Add a new test that checks
  the settlement date is sent on each posting.
Run "mvn test" in global-bank-transaction until it passes.
When you finish, list the files you changed, and say how acceptance criterion 3 is met.
```

**What you should see:** changes under `payroll/` and in `docs/contract.md`, a new test, and a passing
build. Nothing changes in `global-bank-account`.

**Check:** in `global-bank-transaction`:

```bash
mvn test
# expect: Tests run: 3 or more, Failures: 0, Errors: 0
git diff --numstat m7-start -- src/test
# the second number must be 0
```

Then commit:

```bash
git add -A
git commit -m "GB-158: send settlementDate on payroll postings"
```

For a repair, use prompt 7.1-R, with `global-bank-transaction` in place of `global-bank-account`.

**Optional end-to-end check.** Run both services from your two GB-158 branches, in two terminals:
`mvn spring-boot:run` in `global-bank-account` (port 8086), then in `global-bank-transaction`
(port 8087). Send a payroll batch:

```bash
curl -s -X POST http://localhost:8087/transaction/api/v1/disbursements \
  -H 'Content-Type: application/json' \
  -d '{"batchId":"BATCH-158","valueDate":"2026-03-25","settlementDate":"2026-03-27","items":[{"reference":"E1","employeeAccountId":"ACC-CLIENT-001","amountMinor":1000}]}'
# expect: "accepted":1
```

The reply does not include the posting ID. To read the posting back, open
`http://localhost:8086/account/h2-console` in a browser. Set **JDBC URL** to `jdbc:h2:mem:account`,
**User Name** to `root` and **Password** to `root`, then run:

```sql
SELECT client_reference, value_date, settlement_date FROM posting;
```

The row `BATCH-158-E1` should show the settlement date you sent. Stop both services with **Ctrl+C**.

### Step 5 — Write both pull request descriptions

**Prompt 7.1-E** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue.
Read global-bank-account/docs/contract-changes/GB-158-settlement-date.md and
global-bank-account/docs/adr/ADR-009-versioning-the-posting-contract.md.
Write two pull request descriptions for GB-158, one for each repository:
- global-bank-account, branch GB-158-settlement-date (the producer)
- global-bank-transaction, branch GB-158-send-settlement-date (the consumer)
Each description must have: a title that starts with my Jira key for GB-158; what the change does,
in two or three sentences; whether it is additive; a line that links to the other pull request;
the merge order, in words; and a rollback line that says which pull request to revert first, and why.
The consumer description must say it must not merge until the producer pull request is deployed,
not only approved.
Write both descriptions here in the chat. Do not create or change any file.
```

**What you should see:** two short descriptions in the chat. No file changes.

**Check:** read both. Each must name the other pull request, state the order in words, and say which
side to revert first. Copy them into your notes. You do not push or open pull requests in this course.

### Record

Write these on your worksheet:

| Question | Your answer |
|---|---|
| Shape chosen (additive, expand-and-contract or versioned), and why | |
| Did any existing test need changing? (check 2 in step 3) | |
| The merge order, in one sentence | |
| The rollback order, in one sentence | |

### If you are behind

Lab 7.2 does not need your Lab 7.1 work. When the timebox ends, commit what you have in each
repository, then go to Lab 7.2:

```bash
git add -A
git commit -m "GB-158: work in progress"
```

---

## Lab 7.2 — Review a cross-repo change set

**Goal:** Review a prepared two-repository change for GB-158. Find out which inputs let a review of
one repository catch a problem that crosses into the other. · **Ticket:** GB-158 · **Timebox:** 45 min (30 running, 15 debrief) · **Output:**
three review reports and a comparison table

Someone else has already written a GB-158 change in both repositories. It is on the branch
`m7.2-review`. You **review** it. You do not apply, fix or merge anything.

### Before you start

Commit or stop any Lab 7.1 work first. Then, in a terminal:

```bash
cd ~/global-bank/global-bank-account
git fetch origin
git switch m7.2-review
mvn test
# expect: Tests run: 5, Failures: 0, Errors: 0

cd ~/global-bank/global-bank-transaction
git fetch origin
git switch m7.2-review
mvn test
# expect: Tests run: 3, Failures: 0, Errors: 0
```

Both builds are green. That tells you nothing yet about whether the change is right.

**Three rules for the three runs:**

- Pick the **review** agent in the Chat view's agent list before each prompt.
- Start a **new chat** for each run. The earlier run must not be in the reviewer's context.
- Give the reviewer only what the prompt names. Do not add what you learned in Lab 7.1. You wrote
  your own GB-158 an hour ago, so you may spot things fast. The lab measures what the **agent** finds,
  not what you find.

### Run 1 — The producer change alone

**Prompt 7.2-A** · **review** agent · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Review a prepared change for GB-158 in the global-bank-account folder. Do not edit any file.
Get the change by running "git diff m7-start..m7.2-review" in the global-bank-account folder.
Your other inputs are the ADRs in global-bank-account/docs/adr/ and global-bank-account/docs/conventions.md.
Do not open, read or search anything in the global-bank-transaction folder.
Write a review report: findings ranked by severity. For each finding, give the file and line, the
acceptance criterion or rule it breaks, and what would fix it. If you find nothing, say so plainly.
```

**What you should see:** Copilot runs the `git diff` command (read the request, then select **Allow**),
reads the ticket and the ADRs, and writes a report.

**Check:** the chat shows no file opened from `global-bank-transaction`. If it opened one, note it on
your worksheet: the run was not isolated.

### Run 2 — The consumer change alone

**Prompt 7.2-B** · **review** agent · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Review a prepared change for GB-158 in the global-bank-transaction folder. Do not edit any file.
Get the change by running "git diff m7-start..m7.2-review" in the global-bank-transaction folder.
Your other inputs are global-bank-transaction/docs/contract.md and
global-bank-transaction/.github/copilot-instructions.md.
Do not open, read or search anything in the global-bank-account folder.
Write a review report: findings ranked by severity. For each finding, give the file and line, the
acceptance criterion or rule it breaks, and what would fix it. If you find nothing, say so plainly.
```

**What you should see:** a report on the consumer diff only. For each finding, note which input it
came from: the diff, the ticket, `docs/contract.md` or the instruction file.

**Check:** the chat shows no file opened from `global-bank-account`. Write down the number of
findings from Run 1 and Run 2 **before** you start Run 3.

### Run 3 — Both changes together

**Prompt 7.2-C** · **review** agent · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Review a prepared change for GB-158 that spans two repositories. Do not edit any file.
Get the producer change by running "git diff m7-start..m7.2-review" in the global-bank-account folder.
Get the consumer change by running "git diff m7-start..m7.2-review" in the global-bank-transaction folder.
Your other inputs are global-bank-account/docs/adr/, global-bank-transaction/docs/contract.md, and the
current code in both folders.
First, write a short interface summary as a table. List every HTTP endpoint that the consumer code
calls on global-bank-account. For each one, say whether global-bank-account serves it, in its diff
or in its current code, and name the file that proves it.
Then write a review report for the whole change set: findings ranked by severity. For each finding,
give the repository, file and line, the acceptance criterion or rule it breaks, and what would fix it.
```

**What you should see:** an interface summary table first, then one report that covers both
repositories.

### Record

Fill in this table, then answer the two questions under it:

| | Run 1: producer alone | Run 2: consumer alone | Run 3: both together |
|---|---|---|---|
| Number of findings | | | |
| Anything about the acceptance criteria? | | | |
| Anything about a call to the producer? | | | |
| Which input showed the call problem? (diff, ticket, `docs/contract.md`, code) | | | |
| Anything about the merge order? | | | |

1. Run 2 saw only the consumer repository. Did it find anything about a call to the producer? If
   yes, which file let it see across the boundary?
2. What did Run 3 add that neither Run 1 nor Run 2 caught?
3. Which finding needed the ticket's acceptance criteria, and not just the code?

Bring the table to the debrief. The last slides of the Module 7 deck, and its quiz, are shown in the
debrief.

### If you are behind

Runs 1 and 2 are the core of this lab. Do them first. If the clock runs out before Run 3, bring the
Run 1 and Run 2 results to the debrief.

When you finish, go back to your own branches if you want to keep working on them:

```bash
cd ~/global-bank/global-bank-account && git switch GB-158-settlement-date
cd ~/global-bank/global-bank-transaction && git switch GB-158-send-settlement-date
```

---

## Stretch lab 7.1+ (optional) — When only the producer lands

**Goal:** Write the rollback plan for a half-landed change. The producer pull request merges and
deploys. The consumer pull request is blocked for two weeks. Is that safe, and how do you undo it?

Do this on your `GB-158-settlement-date` branch in `global-bank-account`, after step 3.

**Prompt 7.1+-A** · Agent mode · base model · **new chat**

```text
Read global-bank-account/docs/contract-changes/GB-158-settlement-date.md and
global-bank-account/docs/adr/ADR-009-versioning-the-posting-contract.md.
Suppose only the global-bank-account pull request for GB-158 has merged and deployed. The
global-bank-transaction pull request is blocked, and may not merge for two weeks.
Add a section called "If only the producer lands" to the contract-change document. Answer in short lines:
1. Is production safe in this state? Say what every existing caller sends, and what it gets back.
2. What settlementDate is stored for postings made in this state?
3. If we must undo the producer change now, what happens to postings already stored with a settlementDate?
4. Suppose the consumer pull request had merged, and then someone reverted the producer. What would
   happen to the settlementDate the consumer sends?
5. Which one check would you run in production to confirm the state is safe?
Do not change any Java file. Stop and show me the section.
```

**Check answer 4 yourself.** Run the producer as it was **before** GB-158, and send it the new field.
Commit your work first. Then, in `global-bank-account`:

```bash
git switch --detach m7-start
mvn spring-boot:run
```

In a second terminal:

```bash
curl -s -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"GB158-EARLY","debitAccountId":"ACC-CLIENT-001","creditAccountId":"ACC-FEES","amountMinor":1234,"valueDate":"2026-03-01","settlementDate":"2026-03-03","narrative":"Consumer ahead of producer"}'
```

Look at the status and the reply. Did it fail, or did something else happen to `settlementDate`? Does
that match answer 4? Stop the service with **Ctrl+C**, then go back to your branch:

```bash
git switch GB-158-settlement-date
```

Note on your worksheet whether the real behaviour matched Copilot's answer. Bring it to the debrief.

## Stretch lab 7.2+ (optional) — Take the contract file away

**Goal:** Run the consumer review of Run 2 again, **without** `docs/contract.md`. Compare the two
reports. What does the reviewer lose when that one short file is missing?

Stay on the `m7.2-review` branch in both repositories. The consumer's instruction file tells the agent
to read `docs/contract.md`, so the prompt forbids it by name.

**Prompt 7.2+-A** · **review** agent · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-158. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Review a prepared change for GB-158 in the global-bank-transaction folder. Do not edit any file.
Get the change by running "git diff m7-start..m7.2-review" in the global-bank-transaction folder.
Your only other input is global-bank-transaction/.github/copilot-instructions.md.
Do not open, read or search global-bank-transaction/docs/contract.md, even if the instruction file
tells you to read it.
Do not open, read or search anything in the global-bank-account folder.
Write a review report: findings ranked by severity. For each finding, give the file and line, the
acceptance criterion or rule it breaks, and what would fix it. If you find nothing, say so plainly.
```

**Check:** the chat shows no read of `docs/contract.md` and no file opened from `global-bank-account`.
If it read either one, note it on your worksheet: the run was not isolated.

**Compare** this report with your Run 2 report, finding by finding. Which findings are gone? Which
input did each of them come from in Run 2? The contract file is under 30 lines. Note whether those
lines made the difference, and bring the answer to the debrief.
