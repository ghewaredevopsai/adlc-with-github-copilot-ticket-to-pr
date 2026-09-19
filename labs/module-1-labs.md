# Module 1 labs — The ADLC operating model and token economics

**Day 1** · Lab 1.1 (+ stretch) · about 45 minutes · Repository: `global-bank-account` · Start from: `m1-start`

Module 1 has one lab. You fix one real bug with Copilot, on a repository where the team has written
nothing down. While you work, you count six numbers. Those numbers are your **baseline**: the
starting point that the rest of the course is measured against. At the end of Day 2 you measure again
and compare. The goal is an honest number, not a good one.

**Words used in this lab**

- **Posting** — one payment instruction. It moves money from one account to another.
- **Ledger entry** — one side of a posting. Each posting writes two: a debit and a credit.
- **Client reference** — the sender's own id for a payment instruction.
- **Value date** — the date the payment takes effect.
- **Paise** — amounts are whole numbers of paise. `2500000` means ₹25,000.00.
- **Baseline** — your first measurement, taken before the course teaches anything.

## Before you start

These steps take about 5 minutes. They are not part of the measured run.

**1. Load the Module 1 ticket into your Jira.** In a VS Code terminal, at the root of the course
repository:

```bash
python labs/scripts/setup-lab-tickets.py --module 1
```

Use `python3` if `python` is not found. The script creates GB-142 in your Jira project and writes its
key to `labs/lab-keys.md`.

**2. Open the lab workspace.** In VS Code, select **File**, then **Open Workspace from File**, then
`adlc-labs.code-workspace`. Check that **atlassian** is running (**MCP: List Servers**).

**3. Make your branch and check the build.** In a terminal, in the `global-bank-account` folder:

```bash
git switch -c GB-142-lab-1.1 m1-start
mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
```

Ignore any long `jacoco` warnings. Look only at the `Tests run` line. A green build now means that
any red test later comes from this lab's change.

**4. Open your tally issue on the board.** Your trainer shares the board link. On the board, select
**New issue**, then **Workshop tally**. Title it with your name, for example `Tally — Priya Sharma`.
Select **Submit**. You open this issue once, and you use it for the whole course. See
[board/README.md](board/README.md).

**5. Get paper and a pen.** You will count on paper while Copilot works. A counter in another window
is a counter you forget.

**Three things not to do before the run**

- Do not read the code first. The run must measure the repository as it is.
- Do not open any later tag, such as `m2.2-start`. Later tags hold later answers.
- Do not change the prompts. Everyone sends the same words, so the numbers compare fairly.

## Lab 1.1 — The baseline run

**Goal:** fix GB-142 on an unprepared repository, and count six numbers as you go · **Ticket:**
GB-142 · **Timebox:** 45 min (35 working, 10 recording) · **Output:** row 1.1 on your tally issue

**The ticket in one line.** GB-142, *Retried payments are booked twice*. When a payment is sent again
after a timeout, the service books it a second time. Copilot reads the full ticket, with its five
acceptance criteria, from your Jira.

### Step 1 — Write down your four decisions

Before you send anything, write these four on your paper. One word each, plus a reason in one line.
The deck (slides 11 to 18) explains each choice.

1. **Kind of task:** mechanical / reasoning / review — because ...
2. **Model class:** base model / premium reasoning model — because ...
3. **Mode:** Ask / Edit / Agent — because ...
4. **Interactive or delegated:** interactive / delegated — because ...

Write what **you** would choose for this ticket. The measured run itself uses fixed settings (Agent
mode, base model), so that every row on the board compares fairly. You compare these four answers
with your choices at the capstone. The stretch lab lets you try a different choice.

### Step 2 — Start the clock and send the opener

Write down the time. Then send the prompt below. This is turn 1.

**Prompt 1.1-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-142. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Implement the ticket in the global-bank-account folder. Meet every acceptance criterion.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say which acceptance criteria are met and how.
```

**What you should see:** Copilot asks to use `jira_get_issue`, then reads and searches files, edits
code and runs `mvn test`. Read each request before you select **Allow**. At the end, it lists the
files it changed and the criteria it says are met.

**While it works, count.** See [How to count](#how-to-count) below. Make a mark on paper each time
something happens. Do not wait until the end.

**If Copilot stops and asks you a question,** mark it on your paper under **Asked**. Then reply with
this prompt. It counts as a turn.

**Prompt 1.1-Q** · Agent mode · **same chat**

```text
I have no more information than the ticket and the repository. Make the choice you think is right,
tell me what you chose and why, and continue.
```

### Step 3 — Check the tests

Wait until Copilot says it has finished. Then, in a terminal in `global-bank-account`:

```bash
mvn test
```

**Check 1 passes when:** `Tests run` is **more than 4**, with `Failures: 0` and `Errors: 0`. The
ticket asks for tests (criterion 5), so the count must go up.

If Check 1 fails, go to [When a check fails](#when-a-check-fails).

### Step 4 — Start the service

Open a **second** terminal in `global-bank-account`, and leave it running:

```bash
mvn spring-boot:run
```

Wait for the line `Started AccountserviceApplication`. The service listens on port 8086.

On **Windows**, run the `curl` commands in the next steps in a **Git Bash** terminal. Pick it from
the **+** list in the terminal panel. PowerShell treats the quotes differently, and the commands fail.

The service keeps its data in memory. Every restart starts again with empty accounts, so every
balance starts at `0`.

### Step 5 — Check criteria 1 and 2: the same instruction, sent twice

This is the retry from the ticket. Send the **same** payroll payment twice, in a third terminal:

```bash
curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"PAY-2026-03-0001","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-001","amountMinor":2500000,"valueDate":"2026-03-31","narrative":"March payroll"}'
```

Run the **same command** again. Up-arrow and Enter is fine. Then read the balance of the account that
received the money:

```bash
curl -s http://localhost:8086/account/api/v1/accounts/ACC-CLIENT-001/balance
```

**Check 2 passes when all of these are true:**

- Both calls return `HTTP 200` or `HTTP 201`. Neither returns an error.
- Both responses show a `postingId`, and it is the **same** id both times.
- The balance shows `"balanceMinor":2500000`. That is one payment of ₹25,000, not two.

If the balance shows `5000000`, the payment was booked twice.

### Step 6 — Check criterion 3: the same reference on a different value date

A standing order sends the same client reference every month. Each month is a real, new payment.
Send the April payment:

```bash
curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"PAY-2026-03-0001","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-001","amountMinor":2500000,"valueDate":"2026-04-30","narrative":"April payroll"}'
curl -s http://localhost:8086/account/api/v1/accounts/ACC-CLIENT-001/balance
```

**Check 3 passes when:**

- The call returns `HTTP 201`, with a **new** `postingId`, different from the March one.
- The response shows `"valueDate":"2026-04-30"`.
- The balance is now `"balanceMinor":5000000`.

### Step 7 — Check criterion 4: a brand-new instruction

A new payment, with a new client reference, must work exactly as before:

```bash
curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' \
  -d '{"clientReference":"PAY-2026-03-0002","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-002","amountMinor":750000,"valueDate":"2026-03-31","narrative":"March payroll"}'
curl -s http://localhost:8086/account/api/v1/accounts/ACC-CLIENT-002/balance
```

**Check 4 passes when:** the call returns `HTTP 201` with a `postingId`, and the balance shows
`"balanceMinor":750000`.

All four checks pass? **Stop the clock.** Write down the minutes since your first prompt. Stop the
service with `Ctrl+C`. Go to [Record](#record).

### When a check fails

Paste the repair prompt below into the **same chat**. Replace the second line with what you saw: the
failing `Tests run` line, or the curl command and its output. This is the only part of any prompt you
change. Each repair counts as **one turn** and **one rework**.

**Repair prompt 1.1-R** · Agent mode · **same chat**

```text
A check failed. This is what I saw:
<paste the failing output here>
Fix only this. Run "mvn test" in global-bank-account again, and tell me which acceptance
criteria are now met.
```

After Copilot finishes:

1. Stop the service with `Ctrl+C`, and start it again with `mvn spring-boot:run`. The running
   service still has the old code, and the restart also empties the accounts.
2. Run **all** the checks again from Step 3. A repair can break a check that passed before.

**Limits.** Send at most **three** repairs. Stop at **35 minutes** from your first prompt, even in the
middle of a repair. A run that did not finish is still a result. Record it as it is.

### How to count

Keep six columns on paper and make a mark as each thing happens.

| Counter | Mark one each time ... | Do not count |
|---|---|---|
| **Turns** | you send a prompt. The opener is turn 1. Every 1.1-Q and 1.1-R reply is one more | Changing the mode or the model |
| **Tool calls** | the chat shows Copilot reading a file, searching, or fetching the ticket. Expand the collapsed lists in the chat to see each one | File edits, terminal commands, files **you** opened |
| **Asked** | Copilot asks you something that a well-kept repository could answer: where code lives, a team rule, a past decision, what a word means | Questions about what **you** want |
| **Rework** | you send repair prompt 1.1-R. Count it under **Turns** too | — |
| **Churn** | Copilot replaces or deletes lines that it wrote earlier in this run. Estimate the lines, to the nearest ten | Lines in the final change |
| **Clock** | minutes from your first prompt until all four checks pass, or 35 if you stop at the timebox | Setup time, reading this guide |

Tips:

- Be **consistent** rather than perfect. You count again the same way in Lab 2.2 and at the
  capstone, so the same habits give a fair comparison.
- Count tool calls after each reply, while they are still on screen. Scrolling back later is slow.
- For churn, watch the diff in each edit. When Copilot rewrites a method it wrote ten minutes ago,
  note how many lines it replaced.

### Record

You have 10 minutes. Do not skip them: a run with no row on the board cannot be compared later.

1. **Save the numbers in the repository.** Create `metrics.md` at the root of `global-bank-account`,
   with one line: the run, the ticket, and your six numbers. For example:

   ```text
   | 1.1 | GB-142 | turns | tool calls | asked | rework | churn | clock |
   ```

   Put your own numbers in place of the words. Then commit it with your work:

   ```bash
   git add -A
   git commit -m "GB-142 lab 1.1 baseline run"
   ```

2. **Fill in row 1.1 on your tally issue.** Edit the issue body, and put your six numbers in the
   **1.1** row. Write the clock as a number of minutes. If you stopped at the timebox, write
   `35 (not finished)`.
3. **Post the same row as a comment** on the issue. The comment keeps a record of what you reported
   and when.
4. **Say what could make your numbers hard to defend.** Use the last box in the issue. For example:
   you had read the code before, the MCP server failed, or you lost count for a few minutes.
5. **Keep your paper.** It holds your four decisions. You need them at the capstone.

Report what you measured, even if it looks bad. A run that went badly is a finding, not a failure.

### If you are behind

There is no catch-up tag for this lab, because the lab is the measurement. At 35 minutes, stop and
record what you have, marked `35 (not finished)`. Lab 2.1 starts again from `m1-start` on a new
branch, so nothing from this run carries over.

## Stretch lab 1.1+ (optional)

**Goal:** run GB-142 again with a different model class or a different mode, and see how the six
numbers change. Do this only if you finish early. It is not scored, and it does not go on the board.

This second run is not a clean measurement. You have now seen the code and the ticket once, so part of
any change comes from you. Keep that in mind when you compare.

**1. Make a fresh branch** from the same starting point. Commit Lab 1.1 first (see Record).

```bash
git switch -c GB-142-lab-1.1plus m1-start
```

**2. Choose one change,** and use a fresh sheet of paper to count.

**Option A — the other model class.** Send the same opener, word for word, with the premium reasoning
model.

**Prompt 1.1-A** · Agent mode · **premium reasoning model** · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-142. Use the atlassian MCP tools to read
that Jira issue, including its comments.
Implement the ticket in the global-bank-account folder. Meet every acceptance criterion.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say which acceptance criteria are met and how.
```

**Option B — the other mode.** Edit mode changes only the files you give it. It cannot read Jira or
run commands, so you give it the ticket file and run the tests yourself. In a new chat, set the mode
to **Edit**. Select **Add Context**, and add these three files:

- `course/labs/tickets/GB-142.md`
- `global-bank-account/src/main/java/in/brainupgrade/accountservice/posting/service/PostingService.java`
- `global-bank-account/src/test/java/in/brainupgrade/accountservice/posting/PostingServiceTest.java`

Then send:

**Prompt 1.1+-B** · Edit mode · base model · **new chat**

```text
The ticket is in GB-142.md. Implement it by changing only PostingService.java and
PostingServiceTest.java. Meet every acceptance criterion, and add tests for each one.
When you finish, list what you changed, and say which acceptance criteria are met and how.
```

Select **Keep** to accept the changes. Then run `mvn test` yourself. If your mode list has no **Edit**
mode, do Option A instead.

**3. Run the same checks** as Lab 1.1, Steps 3 to 7. Use the same repair prompt 1.1-R, with the same
limit of three repairs. In Option B, send it in Edit mode, then run `mvn test` yourself.

**4. Compare.** Write both rows side by side on paper: Lab 1.1 and 1.1+. Then answer in one line each:

- Which counter changed the most?
- Did the other setting change the design of the fix, or only the effort to reach it?
- Would you make the same four decisions from Step 1 again?

Keep this comparison for yourself or for the room discussion. Do not change row 1.1 on your tally
issue.
