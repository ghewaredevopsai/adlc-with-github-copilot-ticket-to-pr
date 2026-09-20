# Module 1 labs — The ADLC operating model and token economics

**Day 1** · Lab 1.1 (+ stretch) · about 45 minutes · Repository: `global-bank-account` · Start from: `m1-start`

You fix one real bug with Copilot, on a repository where the team has written nothing down. At the
end, Copilot saves the run as one row of `metrics.md`, with a list of what it had to assume. That is your
**baseline**: the first measurement, taken before the course teaches anything. In Lab 2.2 you run this same ticket again, on a
repository where your team's knowledge is written down, and compare. The goal is an honest number, not a good one.

**Words used in this lab**

- **Posting** — one payment instruction. It moves money from one account to another.
- **Client reference** — the sender's own id for a payment instruction.
- **Value date** — the date the payment takes effect.
- **Paise** — amounts are whole numbers of paise. `2500000` means ₹25,000.00.

## Before you start (5 minutes, not measured)

**1. Load the ticket into your Jira.** In a VS Code terminal:

```bash
cd ~/adlc-copilot-training/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 1
```

Use `python3` if `python` is not found. The script creates GB-142 and writes its key to
`labs/lab-keys.md`.

**2. Open the workspace.** **File** → **Open Workspace from File** → `adlc-labs.code-workspace`.
Check that **atlassian** is running (**MCP: List Servers**).

**3. Make your branch and check the build:**

```bash
cd ~/adlc-copilot-training/global-bank-account
git fetch --tags --force
git switch -c GB-142-lab-1.1 m1-start && mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
```

**"a branch named ... already exists"?** You ran this lab before. The tests do not run, because the
two commands are chained. Delete the old branch, or rename it to keep it, and run the block again:

```bash
git switch main
git branch -D GB-142-lab-1.1                          # or: git branch -m GB-142-lab-1.1 first-try
```

**Starting the whole course again?** Clear every lab branch and your own notes first:

```bash
cd ~/adlc-copilot-training/global-bank-account
git switch main
git fetch --tags --force                              # the tags move when a lab is fixed
git branch | grep -v '^\*\| main$' | xargs -r git branch -D
cd ~/adlc-copilot-training/adlc-with-github-copilot-ticket-to-pr && git pull && rm -f labs/my-work/*
```

Your Jira keeps the tickets from the earlier run, with their comments. The setup script finds them
and makes no copies, so running it again is safe.

**Any number other than 4** means you are not on a fresh branch from `m1-start`. Check with
`git branch --show-current`.

If you see long `jacoco` stack traces, your branch came from an old tag. Run `git switch main` and
`git branch -D GB-142-lab-1.1`, then repeat this step.

**Do not** read the code first, open a later tag such as `m2.2-start`, or change the prompts. The
run must measure the repository as it is, with the same words for everyone.

## Lab 1.1 — The baseline run

**Goal:** fix GB-142 on an unprepared repository · **Timebox:** 35 minutes of work, then one record
prompt · **Output:** the fix and `metrics.md`, committed on `GB-142-lab-1.1`

**The ticket in one line.** GB-142, *Retried payments are booked twice*. When a payment is sent again
after a timeout, the service books it a second time. Copilot reads the full ticket, with its five
acceptance criteria, from your Jira.

### Step 1 — Choose your four decisions

Decide these four for this ticket, using slides 11 to 18. You type them into the record prompt at
the end.

1. **Kind of task:** mechanical / reasoning / review
2. **Model class:** base model / premium reasoning model
3. **Mode:** Ask / Plan / Agent
4. **Working style:** interactive / delegated

The measured run itself uses fixed settings (Agent mode, base model), so every run compares fairly.

**Answer for yourself first.** These are your decisions, and the debrief compares the room's answers.
Read the example below only after you have chosen all four.

<details>
<summary><b>An example of the four decisions</b> — open after you have chosen</summary>

> 1. **Kind of task:** reasoning. The ticket hides a design choice — what counts as a duplicate, and
>    what the retry gets back. The code change is small, which makes it look mechanical.
> 2. **Model class:** base model for this run. This is a reasoning task about client money, which is
>    the "worth paying for" case on the slides. Once the rule is written down, a base model can do it.
> 3. **Mode:** Agent. It has to find the files and run the tests, and I do not know this repository yet.
> 4. **Working style:** interactive. I cannot say what "done" means until the duplicate rule is chosen,
>    and this is client money, so I read each step.

Your answers may differ from these, and still be right. What matters is that you can say **why** for
each one.

</details>

### Step 2 — Send the opener

**Prompt 1.1-A** · Agent mode · base model · **new chat**

**Your run is one chat.** Everything from this prompt to the record prompt goes in it, and nothing
else does. That is what makes the numbers you read in Step 6 the cost of this ticket. On **Copilot
CLI**, start the CLI fresh as well: `/usage` reports the whole session, so anything you ran in it
before this prompt would land in your row.

```text
Read course/labs/lab-keys.md to find my Jira key for GB-142. Use the atlassian MCP tools to read
that Jira issue, including its comments. Read no other issue, and do not search Confluence.
Implement the ticket in the global-bank-account folder. Meet every acceptance criterion.
Work only from the files on the current branch. Do not read any other git branch.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say which acceptance criteria are met and how.
```

Read each tool request before you select **Allow**. You do not need to count anything: the record
prompt does that from the chat.

**If Copilot stops and asks you a question,** reply in the same chat with:

**Prompt 1.1-Q** · Agent mode · **same chat**

```text
I have no more information than the ticket and the repository. Make the choice you think is right,
tell me what you chose and why, and continue.
```

### Step 3 — Check the tests

When Copilot has finished, in a terminal in `global-bank-account`:

```bash
mvn test
```

**Check 1 passes when** `Tests run` is **more than 4**, with `Failures: 0` and `Errors: 0`.
Criterion 5 asks for tests, so the count must go up.

### Step 4 — Start the service

In a **second** terminal in `global-bank-account` (stop the whole Global Bank app first if it is
running):

```bash
mvn spring-boot:run
```

Wait for `Started AccountserviceApplication` (port 8086). Data is kept in memory, so every restart
starts with empty accounts. On **Windows**, run the `curl` commands below in **Git Bash**, not
PowerShell.

### Step 5 — Checks 2 to 5

Run these in a third terminal. `post` is a small helper so each check is one line.

```bash
post() { curl -s -w '\nHTTP %{http_code}\n' -X POST http://localhost:8086/account/api/v1/postings \
  -H 'Content-Type: application/json' -d "$1"; }
balance() { curl -s http://localhost:8086/account/api/v1/accounts/$1/balance; echo; }

MARCH='{"clientReference":"PAY-2026-03-0001","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-001","amountMinor":2500000,"valueDate":"2026-03-31","narrative":"March payroll"}'
APRIL='{"clientReference":"PAY-2026-03-0001","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-001","amountMinor":2500000,"valueDate":"2026-04-30","narrative":"April payroll"}'
NEW='{"clientReference":"PAY-2026-03-0002","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-002","amountMinor":750000,"valueDate":"2026-03-31","narrative":"March payroll"}'
RESEND='{"clientReference":"PAY-2026-03-0001","debitAccountId":"ACC-PAYROLL","creditAccountId":"ACC-CLIENT-001","amountMinor":2500000,"valueDate":"2026-03-31","narrative":"March payroll resend"}'
```

**Nothing prints.** That block only sets up the helpers. The checks below are what run them, and
they are the lines in the **Run** column.

| Check | Run | Passes when |
|---|---|---|
| **2** — the same instruction twice (criteria 1, 2) | `post "$MARCH"; post "$MARCH"; balance ACC-CLIENT-001` | Both calls return HTTP 200 or 201 with the **same** `postingId`. Balance `2500000` (one payment, not two) |
| **3** — same reference, new value date (criterion 3) | `post "$APRIL"; balance ACC-CLIENT-001` | HTTP 201, a **new** `postingId`, `"valueDate":"2026-04-30"`. Balance `5000000` |
| **4** — a new instruction (criterion 4) | `post "$NEW"; balance ACC-CLIENT-002` | HTTP 201 with a `postingId`. Balance `750000` |
| **5** — the March payment again, worded differently (criterion 1) | `post "$RESEND"; balance ACC-CLIENT-001` | The **same** `postingId` as your first `MARCH` call. Balance still `5000000` |

**Check 5 is the interesting one.** It sends the March payment a third time, with the same client
reference and the same value date, and only the wording changed. Your team treats that as the same
payment: the narrative is not part of what makes a payment unique. Nobody has written that down,
so the agent has to guess, and a common guess is to compare every field. That guess passes Checks 2
to 4 and books the March payroll **twice** — the very bug GB-142 was raised for. If Check 5 fails,
your run is normal. Repair it, and record it.

All five checks pass? Stop the service with `Ctrl+C` and go to [Step 6](#step-6--record).

**When a check fails,** send the repair prompt in the **same chat**, with the failing output in
place of the `<>` line:

**Prompt 1.1-R** · Agent mode · **same chat**

```text
A check failed. This is what I saw:
<paste the failing output here>
Fix only this. Run "mvn test" in global-bank-account again, and tell me which acceptance
criteria are now met.
```

Then restart the service (`Ctrl+C`, `mvn spring-boot:run`) and run **all** the checks again from
Step 3. Send at most **three** repairs, and stop at **35 minutes** even mid-repair. An unfinished run
is still a result.

### Step 6 — Record

**First, read what the run cost.** You type these into the record prompt, so read them now, before
you send it — the record prompt costs credits of its own.

- **Copilot CLI:** type `/usage`. It gives the model, the input, output and total tokens, and the
  **AIC** (AI credits) for the **whole session**, not for one chat. That is this run only if you
  started the CLI fresh at Step 2.
- **VS Code:** in the chat input box, hover over the **context window control** — the bar that shows
  how full the chat is — and select it. The popover gives this chat's total tokens and its cost in
  credits. The model name is in the model picker under the chat box. If input and output tokens are
  not shown separately, leave those two lines empty.

**Do not ask Copilot to run `/usage` for you.** It is a command to your Copilot client, not to the
agent. The agent cannot run it, and it cannot see its own tokens or credits.

The Copilot icon in the status bar shows something else: the share of your monthly allowance used so
far, across every chat. That is not this run's cost.

Then send this in the **same chat**. Replace every `<...>` line before you send: the six values you
just read, your four decisions from Step 1, and your notes. A line you leave as it is becomes a `-`
in the table, and Copilot carries on instead of stopping to ask you.

**Prompt 1.1-M** · Agent mode · **same chat**

```text
The run is over. Do not ask me anything: if something below is missing, write "-" and carry on.
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
Create metrics.md at the root of global-bank-account with this table and one row:
| Run | Ticket | Model | Model ID | Turns | Tool calls | Asked | Rework | Churn | Input tokens | Output tokens | Total tokens | AIC |
Use "1.1" as the run and "GB-142" as the ticket. Under the table, add a line "Decisions:" with my
four decisions below, then "Assumptions (N):" with N the number you counted and the list below it,
then one line "Notes:" with my notes below, and one line "How counted:" that says anything you could
not count exactly, and says that the model, token and AIC values were read from my client just
before this prompt, so they leave this prompt out.
Then run: git add -A && git commit -m "GB-142 lab 1.1 baseline run". Show me the table.
My four decisions: <kind of task>, <model class>, <mode>, <working style>
My notes: <anything unusual, for example "MCP failed", or leave empty>
```

**Send it as soon as the checks pass.** Your 35 minutes run until you send it, so a break here
eats the timebox.

**A `-` in the model or usage columns?** You sent the prompt with those lines unchanged. Open
`metrics.md`, type the values in yourself, and commit again:
`git commit -am "GB-142 lab 1.1 usage"`.

**Check:** `git show --stat HEAD` lists `metrics.md` and your code changes. Leave the numbers as
Copilot counted them, even if they look bad. A run that went badly is a finding, not a failure.

### If you are behind

There is no catch-up tag, because the lab is the measurement. At 35 minutes, send Prompt 1.1-M
anyway. Lab 2.1 starts again from `m1-start`, so nothing from this run carries over.

## Stretch lab 1.1+ (optional)

**Goal:** run GB-142 again with one setting changed, and see which numbers move. Not scored. You
have now seen the code once, so part of any change comes from you.

```bash
git switch -c GB-142-lab-1.1plus m1-start
```

This is a second run, so give it its own boundary: a **new chat**, and on **Copilot CLI** a fresh
CLI session again. Without that, `/usage` still holds Lab 1.1, and the two rows differ by that alone.

Pick one:

- **Option A — the other model class.** Send Prompt 1.1-A word for word, in a **new chat**, with the
  **premium reasoning model**.
- **Option B — plan first.** In a **new chat**, set the mode to **Plan**. Plan mode reads the
  repository and writes an implementation plan. It changes no code. Send:

  **Prompt 1.1+-B** · Plan mode · base model · **new chat**

  ```text
  The ticket is course/labs/tickets/GB-142.md. Plan the change in the global-bank-account folder,
  so that every acceptance criterion is met and each one has a test.
  ```

  Read the plan. If it names a duplicate rule you disagree with, say so once and ask for a new plan.
  That reply is a turn. Count the prompts you send in this chat, including that one, and keep the
  number. Copilot cannot see this chat from the implementation chat, so you add them in yourself.
  Then select **Start Implementation** and pick the Agent to carry it out.


Run Steps 3 to 5 as before. Then send Prompt 1.1-M with `1.1+` as the run and `GB-142 lab 1.1+` in
the commit message.

**Option A is one chat.** Read the model and usage numbers the way Step 6 says.

**Option B is two chats,** and the plan chat is the part you are measuring. Read the tokens and the
AIC in **both** chats and **add them together** before you type them in. Send Prompt 1.1-M in the
implementation chat, and put "planned first, usage is both chats added" in the notes line. Then open
`metrics.md`, add your plan chat's prompts to the Turns cell, and commit again:
`git commit -am "GB-142 lab 1.1+ plan chat"`. Leave tool calls and churn as Copilot counted them: it
can only see the chat it is in, and the plan chat wrote no code.

Compare the two files:

```bash
git diff GB-142-lab-1.1 GB-142-lab-1.1plus -- metrics.md
```

Which number changed most? Did the other setting change the design of the fix, or only the effort?
In Option B, the plan usually costs turns and saves churn. Your `metrics.md` shows whether it did.
