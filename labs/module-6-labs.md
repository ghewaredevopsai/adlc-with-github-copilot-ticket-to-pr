# Module 6 labs — The ticket as the unit of work

**Day 2** · Labs 6.1, 6.2 (+ stretch) · about 90 minutes · Repository: `global-bank-account` ·
Start from: the tag `m6-start`

Until now Copilot read one ticket at a time, because the prompt told it which key to fetch. In these
labs you decide what else to **pull** around a ticket, and what that costs: its comments, its links and
its epic. Copilot also **writes back**: it adds a comment to the ticket.
Lab 6.1 shows what the connection costs, on a ticket you know. Lab 6.2 is the main lab of the
module. Work through it in order, and do not read ahead.

**Words used in these labs**

| Word | Meaning |
|---|---|
| **MCP server** | The program that gives Copilot its Jira tools, such as `jira_get_issue` |
| **Tool call** | One use of a tool. The chat shows each one, and asks you to **Allow** it |
| **Tool budget** | How many Jira tool calls a ticket is worth. You decide it before you start |
| **Surroundings** | Everything around a ticket except its description: comments, linked issues, the epic |
| **Epic** | A group of related tickets |
| **Write-back** | Copilot writing into Jira. In this course, that is a comment and nothing else |
| **Spec** | Your written copy of a ticket: what it must do, and where each rule comes from. Module 5 introduced it. Here it lives in `specs/<ticket>.md` |

## Before you start

**1. Load the Module 6 tickets.** In a terminal at the root of the course repository:

```bash
cd ~/adlc-copilot-training/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --module 6
```

This loads six tickets into your Jira project: GB-100, GB-207, GB-163, GB-118, GB-119 and RISK-402.
GB-100 and GB-207 may say `exists`, because Module 4 loaded them. That is fine. Open
`labs/lab-keys.md` and check that all six have a key.

One of these tickets is closed. Many Jira projects have only a **Done** status, so its summary ends
with `(CLOSED - WON'T DO)`. Read the summary, not the status.

**2. Open the workspace.** In VS Code, open `adlc-labs.code-workspace`. Check that the **atlassian**
server is **Running** (Command Palette, then **MCP: List Servers**).

**3. Make the Lab 6.1 branch and build it.**

```bash
cd ~/adlc-copilot-training/global-bank-account
git fetch --tags --force
# m6-start is a tag: git tag lists it, git branch does not. Never use main instead.
git switch -c GB-207-lab-6.1 m6-start && mvn test
# "already exists"? The branch is from an earlier run: see "Running a lab again" in README.md
# expect: Tests run: 4, Failures: 0, Errors: 0
```

**4. Open a notes file.** You record numbers as you go, not afterwards. Any text file outside the
repositories is fine.

---

## Lab 6.1 — The connected run: GB-207 pulled, not pasted

**Goal:** pull a ticket by its key, work from a spec, and write back one safe comment. Count what the
connection costs. · **Ticket:** GB-207 · **Timebox:** 40 min · **Mode:** solo ·
**Output:** `specs/GB-207.md`, a commit on `GB-207-lab-6.1`, and one comment on your GB-207 issue

GB-207 is the ticket from Lab 4.2, so you already know what to build. That is on purpose. In this lab,
watch the two ends: the pull at the start and the write-back at the end.

### Step 1 — Decide your tool budget

This step has no prompt. Before Copilot does anything, write this line in your notes:

```text
Lab 6.1 tool budget: ___ Jira tool calls for GB-207
```

Use the rule from the slides. A normal ticket is worth about three calls: the ticket, its comments,
its links. Read GB-207 in `labs/tickets/` only if you have forgotten it. Do not paste it anywhere.

### Step 2 — Pull the ticket by its key

**Prompt 6.1-A** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tools to pull
that one Jira issue by its key, with its comments, its linked issues and its epic.
Do not search Jira. Read another ticket only if this issue links to it.
Show me the summary, the status and the acceptance criteria. Then list the surroundings you found:
the comments, the linked issues and the epic, or "none" for each.
Then stop. Do not open any code, and do not write any files.
```

**What you should see:** Copilot reads `lab-keys.md`, then asks to run `jira_get_issue`. Read the
request, then select **Allow**. It shows the ticket and a list of surroundings.

**Check:** count the Jira tool calls in the chat. Write the number in your notes. Did Copilot try
`jira_search`? If so, write down why it said it needed to.

### Step 3 — Save the ticket as a spec, not in the chat

**Prompt 6.1-B** · Agent mode · base model · **same chat**

```text
Write a spec for this ticket to global-bank-account/specs/GB-207.md. Use only what you pulled in
this chat. Do not call the Jira tools again.
At the top, write the lab ticket name GB-207 and my Jira key.
Include: the problem in one paragraph, the acceptance criteria numbered as on the ticket, and any
open questions. Say what must happen, not how to build it: name no code files.
For every rule in the spec, name its source: the description, a comment, a linked issue, or a file
in the repository.
Stop when the file is written. Do not change any code.
```

**What you should see:** a new file `global-bank-account/specs/GB-207.md`. No new Jira tool calls.

**Check:** open the file. Is each acceptance criterion there, with a source? Does it name the date a
posting *takes effect* (the value date), not the date it was recorded?

### Step 4 — Two or three turns of coding

The spec is now your copy of the ticket. The coding agent works from it, so nobody re-reads Jira.

**Prompt 6.1-C** · Agent: **coding** (pick it in the Chat view's agent list) · base model ·
**new chat**

```text
Implement global-bank-account/specs/GB-207.md in the global-bank-account folder. Work from the
spec only. Do not call the Jira tools: the spec is your copy of the ticket.
Start with the service method and the controller change.
Run "mvn test" in global-bank-account. Then stop, and list the files you changed.
```

**Prompt 6.1-D** · Agent: **coding** · base model · **same chat**

```text
Check acceptance criteria 3 and 4 in global-bank-account/specs/GB-207.md against your change.
Without asAt, the balance endpoint must behave exactly as before. An unknown account must be
rejected exactly as before. Fix anything that does not match.
Run "mvn test" in global-bank-account again. Then stop, and tell me which acceptance criteria
are met and which are not met yet.
```

**Check 1:** `mvn test` in `global-bank-account` shows `Failures: 0, Errors: 0`.

**Check 2 (if you have 5 minutes):** start the service in one terminal:

```bash
mvn spring-boot:run
```

In a second terminal, post ₹1,000 with a value date far in the future, then read the balance twice:

```bash
curl -s -X POST http://localhost:8086/account/api/v1/postings -H "Content-Type: application/json" \
  -d '{"clientReference":"LAB61-1","debitAccountId":"ACC-CLIENT-001","creditAccountId":"ACC-CLIENT-002","amountMinor":100000,"valueDate":"2099-12-31","narrative":"lab 6.1"}'
curl -s http://localhost:8086/account/api/v1/accounts/ACC-CLIENT-002/balance
curl -s "http://localhost:8086/account/api/v1/accounts/ACC-CLIENT-002/balance?asAt=2030-01-01"
```

Write down both `balanceMinor` values. Stop the service with `Ctrl+C`.

Do not finish the ticket. Two or three coding turns are enough. Commit what you have:

```bash
git add -A
git commit -m "GB-207: balance as at a date (Lab 6.1, work in progress)"
```

### Step 5 — Write back one comment

A comment only **adds** to the ticket, and anyone can delete it. So the agent may post it without a
person checking first. Changing the status is different: people and automations act on it. So this
step posts one comment and nothing else.

**Prompt 6.1-E** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tool
jira_add_comment to add one comment to that issue. Make no other Jira call.
The comment text is exactly:
[copilot-agent] GB-207: work in progress on branch GB-207-lab-6.1 in global-bank-account.
Spec: specs/GB-207.md. Acceptance criteria not yet checked by the test agent.
Do not change the issue's status, fields or assignee. Stop after the comment is posted.
```

**What you should see:** one `jira_add_comment` request. Read it before you select **Allow**.

**Check:** open the issue in Jira in your browser. The comment is there, under your name.

### Record

Write these in your notes:

| Item | Your result |
|---|---|
| Jira tool calls: budgeted / made | |
| Calls you did not plan, and why | |
| The largest thing a tool call returned | |
| Did Copilot search Jira at any point? | |
| Places the key GB-207 appears: branch, commit, spec, comment | |
| Both `balanceMinor` values from Check 2 (if you ran it) | |

### If you are behind

Skip Step 4. Go straight to Step 5, so you still post the write-back. Lab 6.2 starts from
`m6-start`, so you lose nothing that it needs.

---

## Lab 6.2 — GB-163: raise the posting limit

**Goal:** work one small ticket twice, and compare the two results. · **Ticket:** GB-163 ·
**Timebox:** 50 min (35 min running, then a 15-minute debrief) · **Mode:** pairs ·
**Output:** a written verdict for Part A, and a record of what the agent did in Part B

Work in pairs. One person drives, and the other writes the notes. **Do Part A before Part B.** Do not
open GB-163 in Jira, and do not open `labs/tickets/GB-163.md`, until Part B tells you to.

### Part A — work it from the description (10 min)

Most tickets reach an agent the way this one does: someone pastes the description. Do that here.

```bash
cd ~/adlc-copilot-training/global-bank-account
git switch -c GB-163-lab-6.2-part-a m6-start
```

#### Step A1 — Implement the ticket

**Prompt 6.2-A** · Agent mode · base model · **new chat**

```text
Here is Jira ticket GB-163. Work only from this text.

GB-163 - Raise the posting limit
Description: Raise the posting limit as discussed with ops.
Acceptance criteria:
- The limit is raised.

Implement the ticket in the global-bank-account folder. Add a test for the change.
Run "mvn test" in global-bank-account until it passes.
When you finish, list the files you changed, and say whether the acceptance criterion is met.
```

Let it work. Do not add anything.

**If Copilot asks what the new limit should be,** write "Asked: yes" in your notes, then send this:

**Prompt 6.2-A2** · Agent mode · base model · **same chat** · only if Copilot asked for a number

```text
I do not have an exact number. The ticket says it was discussed with ops. Choose a sensible new
limit, tell me which one you chose, and go ahead.
```

**Check:** `mvn test` in `global-bank-account` shows `Failures: 0, Errors: 0`. Then commit:

```bash
git add -A
git commit -m "GB-163: raise the posting limit (Lab 6.2 Part A)"
```

#### Step A2 — Review the change

Review it the usual way: the change, checked against the ticket.

**Prompt 6.2-B** · Agent: **review** (pick it in the agent list) · base model · **new chat**

```text
Review the last commit in global-bank-account against the ticket below. Run "git show HEAD" in
global-bank-account to see the change.

GB-163 - Raise the posting limit
Description: Raise the posting limit as discussed with ops.
Acceptance criteria:
- The limit is raised.

Give me your review report, in the format your instructions describe. Do not edit any file.
```

#### Step A3 — Write your verdict

Before you go on, answer these in your notes. Answer from what you saw, not from what you expect.

| Question | Your answer |
|---|---|
| Did Copilot ask you anything before it changed code? | |
| What is the new limit, in rupees? | |
| Do the tests pass? | |
| Did the review agent object? What did it say? | |
| Is the acceptance criterion met? | |
| Would you raise a pull request for this change? Yes or no, and why | |

**Answer from your own run first.** Read the example below only after all six rows are filled. It
shows how much detail each row needs. Your run will differ, because the agent chooses the number.

<details>
<summary><b>An example of five of the answers</b> — open after you have filled the table</summary>

> | Question | Example answer |
> |---|---|
> | Did Copilot ask you anything before it changed code? | Yes. It asked what the new limit should be, so I sent Prompt 6.2-A2. (Write "No" if it chose a number and carried on.) |
> | What is the new limit, in rupees? | ₹50 crore. `Money.MAX_POSTING_MINOR` went from `100_000_000_00L` to `500_000_000_00L`. The old limit was ₹10 crore. |
> | Do the tests pass? | Yes. 5 tests, 0 failures. The new test posts an amount above the old limit and expects it to be accepted. |
> | Did the review agent object? What did it say? | No blocking finding. One minor point: the test does not check the new upper bound. |
> | Is the acceptance criterion met? | Yes. The criterion says "the limit is raised", and it is raised. |

Write the **constant and the rupee figure**, as the second row does. Paise are easy to get wrong:
`500_000_000L` is ₹50 lakh, which *lowers* the limit, and a test written against that constant still
passes.

**The last row has no example.** Your answer to "would you raise a pull request" is yours, and Part B
is the test of it. Give one reason, and name the one thing that would change your mind.

</details>

### Part B — pull the whole ticket (25 min)

Start again, from the checkpoint, in a new chat. Keep your Part A branch as evidence.

```bash
git switch -c GB-163-raise-posting-limit m6-start
```

Write your tool budget in your notes first. The slides give about three calls for a normal ticket,
and about five for a ticket with a history. Decide which kind GB-163 is:

```text
Lab 6.2 tool budget: ___ Jira tool calls for GB-163
```

#### Step B1 — Pull GB-163 and its surroundings, by name

**Prompt 6.2-C** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-163. Use the atlassian MCP tools to pull
that issue by its key, with all of its comments. Then pull each issue it links to, by key, and
the epic named on it, by key. Do not search Jira.
Write what you found to global-bank-account/specs/GB-163.md. At the top, write GB-163 and my Jira
key. List every rule, number and condition you found. For each one, give its source: the
description, a comment (its author and how old it is), or a linked issue (its key and status).
List any question on the ticket that nobody has answered.
Stop when the file is written. Do not change any code.
```

**What you should see:** several `jira_get_issue` requests. Allow each one after you read it.

**Check:** count the Jira tool calls. Open `specs/GB-163.md`. Does every line have a source?

#### Step B2 — Rank the sources

**Prompt 6.2-D** · Agent mode · base model · **same chat**

```text
Now rank the sources in global-bank-account/specs/GB-163.md. For each source, say how recent it is
and which team owns the decision it makes. Put the source that should carry the most weight first.
Say where two sources disagree, and name both.
Add the ranking to the end of the spec file. Do not call the Jira tools again. Do not change any code.
```

#### Step B3 — Work the ticket, with a stop condition

A **stop condition** is a rule that tells the agent when to stop and ask, instead of guessing. You
wrote them in Module 3. This one is shaped for tickets, and the questions go onto the ticket.

**Prompt 6.2-E** · Agent mode · base model · **same chat**

```text
Now work GB-163 from global-bank-account/specs/GB-163.md.
Stop condition: before you change any code, check the spec. If two sources disagree, or an issue
that blocks this one is still open, or a past ticket for this change was closed Won't Do, do not
change any code. Instead, write your questions, and use
jira_add_comment to post them as one comment on my GB-163 issue. Start the comment with
"[copilot-agent] GB-163:" and name the source of each question.
If none of these is true, implement the ticket in global-bank-account and run "mvn test".
Either way, tell me which path you took and why.
```

**Check:** run `git status` in `global-bank-account`. Then open your GB-163 issue in Jira in the
browser, and look for a new comment.

### Record

| Item | Your result |
|---|---|
| Part A: tests passed? | |
| Part A: did the review agent object? | |
| Part A: was the acceptance criterion met? | |
| Part B: Jira tool calls, budgeted / made | |
| Part B: rules and numbers found, and their sources | |
| Part B: which source did the agent rank first? | |
| Part B: did the agent change any code? | |
| Part B: did it post a comment? Copy its questions here | |
| Part A and Part B together: what does Part B know that Part A did not? | |

Bring these notes to the debrief. Your trainer runs it for the last 15 minutes of the lab.

### If you are behind

Never skip Part A. If time is short in Part B, run Prompt 6.2-C and then go straight to Prompt 6.2-E.

---

## Stretch lab 6.1+ (optional) — pulled against pasted

**Goal:** measure what the pull cost on GB-207, against a paste of the same ticket. Do it if you
finish Lab 6.1 early. It is not scored.

Stay on branch `GB-207-lab-6.1`.

**Prompt 6.1+-A** · Agent mode · base model · **new chat**

Copy the prompt below into the chat box. Then open `labs/tickets/GB-207.md`, copy all of it, and
paste it on a new line under the prompt. Send the two together.

```text
The Jira ticket GB-207 is pasted below. Do not use any Jira tools.
Show me the summary and the acceptance criteria. Then list the surroundings the paste includes:
comments, linked issues and epic, or "none" for each.
Then stop. Do not open any code, and do not write any files.
```

**Check:** compare this chat with your chat from Step 2 of Lab 6.1.

1. **Turns and tool calls.** Count each chat's prompts and tool calls.
2. **Context size.** Measure the size of what reached the chat. For the paste:

   ```bash
   python -c "print(len(open('../adlc-with-github-copilot-ticket-to-pr/labs/tickets/GB-207.md', encoding='utf-8').read()))"
   ```

   For the pull: in the Lab 6.1 chat, expand the `jira_get_issue` call and copy its output into a
   scratch file outside the repositories. Count it the same way. If your Copilot Chat shows how full
   the context window is, note that figure for both chats too.
3. **Content.** Did the pull contain anything the paste did not? Did the paste contain anything the
   pull did not?

Write one sentence: for GB-207, was the pull worth its cost? Would your answer be the same for a
ticket with many comments and links?

<details>
<summary><b>An example of the sentence</b> — open after you have written yours</summary>

> For GB-207 the pull added little: the ticket has no comments and one link, the epic GB-100, so the
> pull carried nearly the same words as the paste and cost a tool call. On a ticket with a history my
> answer changes, because the comments and the linked issues are the part nobody pastes.

</details>

## Stretch lab 6.2+ (optional) — the stop condition as a skill

**Goal:** save the stop condition from Lab 6.2 as a skill file, so every chat gets it without a long
prompt. Then try it on another ticket. A **skill file** is a set of steps that Copilot loads when the
task matches its description. You wrote one in Lab 3.1.

GB-147 was loaded in Module 5. If `labs/lab-keys.md` has no key for it, run
`python labs/scripts/setup-lab-tickets.py --module 5` from the course repository first.

```bash
git switch -c GB-147-lab-6.2-stretch m6-start
```

**Prompt 6.2+-A** · Agent mode · base model · **new chat**

```text
Create a skill file at global-bank-account/.github/skills/ticket-intake/SKILL.md. Use the same
front matter format as global-bank-account/.github/skills/account-change/SKILL.md, with the name
ticket-intake. The skill applies before work starts on any Jira ticket. It must say:
1. Pull the ticket by its key, with its comments, its linked issues and its epic. Never search Jira.
2. List every rule and number, with its source.
3. Stop and ask, and change no code, when two sources disagree, when an issue that blocks this
   ticket is still open, or when a past ticket for the same change was closed Won't Do.
4. Post the questions as one Jira comment on the ticket. Start it with "[copilot-agent]" and the
   ticket key.
Keep the file under 40 lines. Do not change any other file. Stop when the file is written.
```

**Prompt 6.2+-B** · Agent mode · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-147. Follow the skill in
global-bank-account/.github/skills/ticket-intake/SKILL.md to start work on that issue.
Follow the skill exactly. If the skill says to stop, stop. Do not change any code in this chat.
```

**Record:** Did the agent stop? If it stopped, was the stop right, or noisy? If it went on, should it
have stopped? If your answer is "it should have stopped", write the rule you would add to the skill
file.
