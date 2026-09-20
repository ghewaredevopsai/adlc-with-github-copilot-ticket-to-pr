# Module 4 labs — Specialised agents

**Day 1** · Labs 4.1, 4.2 (+ stretch) · about 90 minutes · Repository: `global-bank-account` · Start from: your Lab 3.1 branch `GB-151-lab-3.1` (catch-up: `m4-start`). Lab 4.2 brings in agents from `m5-start`

In these labs you build two **custom agents** and then use them on a real ticket. A custom agent is an
agent you define yourself, with one job and its own rules. Lab 4.1 writes the test agent and the review
agent. These two matter most, because their value comes from what they are **not** given. Lab 4.2 runs
one ticket through separate agents, in separate chats. You look for one thing: two agents that read the
ticket differently.

## Words used in these labs

| Word | Meaning |
|---|---|
| **Agent file** | A Markdown file in `.github/agents/`, named `<name>.agent.md`. VS Code reads it and adds the agent to the Chat view |
| **Frontmatter** | The block between two `---` lines at the top of the file. It holds settings such as `name` and `tools` |
| **Tools list** | The `tools:` line in the frontmatter. The agent can use only the tools listed there |
| **Rationale** | The coding agent's own explanation of why it wrote the code |
| **Hand-off artifact** | A file one agent passes to the next, for example `spec.md` or a test report |
| **Hand-off folder** | In these labs: `global-bank-account/handoff/GB-207/`. The artifacts for the ticket go here |

## Before you start

1. Load this module's ticket into your Jira project. In a terminal, at the root of the course
   repository:

   ```bash
   cd ~/adlc-with-github-copilot-ticket-to-pr
   python labs/scripts/setup-lab-tickets.py --module 4
   ```

   The script adds GB-207 and its epic, GB-100, to `labs/lab-keys.md`. You use GB-207 in Lab 4.2.

2. Open the lab workspace: **File**, then **Open Workspace from File**, then `adlc-labs.code-workspace`.
   Check that the **atlassian** MCP server is running (**MCP: List Servers**).

3. Go back to your Lab 3.1 branch, which holds your skill file and prompt file, and start a new
   branch from it. Lab 3.2's eval runs stay behind on `eval-lab-3.2`:

   ```bash
   cd ~/global-bank/global-bank-account
   git switch GB-151-lab-3.1
   git status --short
   # must print nothing. If it lists files, commit them first
   # branch already there from an earlier run? see "Running a lab again" in README.md
   git switch -c lab-4.1-agents
   mvn test
   # expect: Failures: 0, Errors: 0. Tests run: 4, or more if your earlier labs added tests
   ```

   No Lab 3.1 branch, or it is broken? Start from the checkpoint instead:
   `git switch -c lab-4.1-agents m4-start`, and skip step 4.

4. Add the reference knowledge files that you did not write in Module 2. The agents in this module
   point at them: the test rules, the ADR index, three ADRs and three files in `docs/`. This keeps your
   own `copilot-instructions.md`, `domain.instructions.md`, `ADR-001`, skill file and prompt file:

   ```bash
   git checkout m2.2-start -- .github/instructions/tests.instructions.md \
     .github/instructions/api.instructions.md docs/architecture.md docs/conventions.md \
     docs/glossary.md docs/adr/README.md docs/adr/ADR-003-amounts-as-minor-units.md \
     docs/adr/ADR-005-no-lombok.md docs/adr/ADR-007-duplicate-suppression.md \
     docs/adr/ADR-009-versioning-the-posting-contract.md
   git commit -m "Module 4: add the reference knowledge files"
   ```

   `ADR-007` is the reference version of your own `ADR-001`. Keep both. The ADR index lists `ADR-007`.

---

## Lab 4.1 — Two agent definitions

**Goal:** write `test.agent.md` and `review.agent.md`, with all seven parts and the withheld input
written down · **Ticket:** none · **Timebox:** 45 min · **Output:** two agent files, committed

### The seven parts, and how to check each one

The deck's "Seven parts of an agent file" slide lists them. Use this table to check each file.

| Part | What it says | Your check |
|---|---|---|
| Role | One sentence: what this agent is for | Could anyone mix it up with another agent's role? |
| Goal | The file or report it must produce | Is it a file or report, or only a chat? |
| Allowed tools | The tools, listed | Does the `tools:` list allow something a Never line forbids? |
| Inputs | What it gets, and a line saying what it does not get | Is the withheld input written down as a line? |
| Guardrails | The team rules for this role | Do they point to repository files, instead of copying them? |
| Hand-off contract | The shape of the report it passes on | Could a person judge the report without reading the chat? |
| Never | What it must not do, even when that seems reasonable | Would this line stop the agent when it feels sure it is right? |

A rule in the text is only a request. The `tools:` list is what VS Code enforces. If the file says
"no edits", the `tools:` list must not contain `edit`.

### Step 1 — Draft the test agent

In the Chat view, pick **Agent** from the agent list. Then paste this prompt.

**Prompt 4.1-A** · Agent mode · base model · **new chat**

```text
Create the file global-bank-account/.github/agents/test.agent.md. It defines a VS Code custom
agent named "test". Its job: write tests that prove each acceptance criterion of a ticket,
working from the ticket only.
First read global-bank-account/.github/instructions/tests.instructions.md and
global-bank-account/.github/copilot-instructions.md. Point to these files; do not copy them.
Start the file with YAML frontmatter that has: name: test, a one-line description,
version: 1, owner: TODO-OWNER, and a tools list. Put in the tools list only the tools this
role needs, chosen from: read, search, edit, execute, atlassian/jira_get_issue.
Then write seven sections, in this order: Role, Goal, Allowed tools, Inputs, Guardrails,
Hand-off contract, Never.
- Inputs: the first line says what the agent is NOT given: the coding agent's rationale and
  summary, and the design spec. These are spec.md and coding-summary.md in the handoff folder.
  Add one sentence that says why.
- Guardrails: include "run every new test against the code before the change first".
- Hand-off contract: a test report shown in the chat. One line per acceptance criterion,
  marked covered or not covered, with the name of the test. A criterion it cannot cover is
  listed, never dropped.
- Never: at least three things this agent must never do, even when they seem reasonable.
Write named checks. Do not use words like "be thorough" or "be careful".
Create only this one file. When it is written, list the tools you chose and give one line
of reason for each. Then stop.
```

**What you should see:** one new file with the frontmatter and seven sections. The chat lists the
tools and the reasons.

**Check:** open the file. Replace `TODO-OWNER` with your own name: a person, not a team. Then read the
Inputs section. The withheld input must be a line of its own, not hidden inside a sentence.

### Step 2 — Draft the review agent

**Prompt 4.1-B** · Agent mode · base model · **new chat**

```text
Create the file global-bank-account/.github/agents/review.agent.md. It defines a VS Code custom
agent named "review". Its job: find what is wrong, and what is missing, in a change. It reports.
It never fixes.
First read global-bank-account/.github/copilot-instructions.md and
global-bank-account/docs/adr/README.md. Point to these files; do not copy them.
Start the file with YAML frontmatter that has: name: review, a one-line description,
version: 1, owner: TODO-OWNER, and a tools list. Put in the tools list only the tools this
role needs, chosen from: read, search, edit, execute, atlassian/jira_get_issue.
Then write seven sections, in this order: Role, Goal, Allowed tools, Inputs, Guardrails,
Hand-off contract, Never.
- Inputs: the diff, the ticket and its acceptance criteria, docs/adr/, docs/conventions.md and
  the instruction files. Then one line that says what the agent is NOT given: the coding
  agent's rationale and summary, and the design spec (spec.md and coding-summary.md in the
  handoff folder). Add one sentence that says why.
- Guardrails: a numbered checklist, worked in this order: 1 acceptance criteria, 2 scope,
  3 ADRs and conventions, 4 would the tests fail on the code before the change,
  5 what is missing. "What is missing" must be last.
- Hand-off contract: a review report shown in the chat. For each finding: severity, file and
  line, the rule or criterion it breaks, and what would satisfy it. If it finds nothing, it
  says so plainly.
- Never: at least three things this agent must never do, even when they seem reasonable.
Write named checks. Do not use words like "be thorough" or "be careful".
Create only this one file. When it is written, list the tools you chose and give one line
of reason for each. Then stop.
```

**What you should see:** a second file with the same shape. The checklist has five numbered checks,
with "what is missing" last.

**Check:** replace `TODO-OWNER` with your name. Look at the `tools:` line. If it contains `edit`,
delete `edit` now. A reviewer that can edit will edit one day, whatever the text says.

### Step 3 — Audit both files

This step uses **Ask** mode, so Copilot cannot change the files.

**Prompt 4.1-C** · Ask mode · base model · **new chat**

```text
Read global-bank-account/.github/agents/test.agent.md and
global-bank-account/.github/agents/review.agent.md. Audit each file against these questions:
1. Does it have all seven sections: Role, Goal, Allowed tools, Inputs, Guardrails,
   Hand-off contract, Never?
2. Does the tools list in the frontmatter allow anything that a Never line forbids?
3. Does the Allowed tools section say the same as the tools list?
4. Is the withheld input written as its own line in Inputs?
5. Could a person judge the hand-off report without reading the chat?
6. Does any line use an adjective instead of a named check, for example "be thorough"?
7. Does the review checklist end with "what is missing"?
Answer as one table per file: question, yes or no, and the line you are quoting.
Do not suggest a rewrite of the whole file. Do not edit anything.
```

**What you should see:** two tables, each answer quoting a line from the file.

**Check:** fix every "no" by hand, in the file. For example, remove a tool, split out the withheld
input, or change an adjective into a named check. Keep each fix small.

VS Code may underline `version` and `owner` in the frontmatter, because it does not use them. That is
fine. They are there for people: who looks after the file, and which version is in use.

### Step 4 — Check that VS Code sees the agents

1. Save both files.
2. In the Chat view, open the agent list (the list that shows **Agent**, **Ask** and **Plan**).
3. Find **test** and **review** in the list.

**Check:** both agents appear in the list. Pick **review** and look at the chat box: its description
shows as the hint text.

Agent missing? Check these, in order:
- The file name ends in `.agent.md`, and the file is in `global-bank-account/.github/agents/`.
- The first line of the file is exactly `---`.
- Run **Developer: Reload Window** from the Command Palette, then look again.

Then commit:

```bash
git add .github/agents
git commit -m "Lab 4.1: test and review agent definitions"
```

### Record

Write down, for your debrief:
- Which tools did Copilot choose for the review agent at first? Did it include `edit`?
- Which audit questions came back "no"?
- The one line you changed by hand that you think matters most.

### If you are behind

Lab 4.2 can run without your files. Start it from the checkpoint `m5-start`, which holds all four agent
definitions. The steps in Lab 4.2 show how.

---

## Lab 4.2 — The four-agent hand-off on GB-207

**Goal:** take one ticket through design and coding, then test, then review, in three separate chats,
and record whether the agents disagreed · **Ticket:** GB-207 (balance as at a date) ·
**Timebox:** 45 min (35 running, 10 debrief) · **Output:** `spec.md`, `coding-summary.md`,
`test-report.md`, `review-report.md` and a verdict

### Three chats, never one

| Chat | Agents | Sees | Hands over |
|---|---|---|---|
| 1 | design, then coding | design: the ticket, the ADRs, the docs. Coding: the spec and the code | `spec.md`, the change, `coding-summary.md` |
| 2 | test | the ticket only (and the code's public methods) | the tests, `test-report.md` |
| 3 | review | the diff, the ticket, the ADRs | `review-report.md` |

Design and coding share one chat on purpose: the coding agent builds what the spec says. The two
separate readings of the ticket are the test agent's and the review agent's.

**Always start a new chat for chats 2 and 3.** If two agents share one chat, they share one reading of
the ticket. You still get three reports, and they still agree. But the agreement means nothing, and
nothing warns you.

### Set up

Pick **one** starting point.

**A — you finished Lab 4.1.** Keep your test and review agents. Bring in the design and coding agents
from the checkpoint. Skip the `git checkout` line if you wrote your own in the stretch lab 4.1+.

```bash
cd ~/global-bank/global-bank-account
git switch -c GB-207-lab-4.2
git checkout m5-start -- .github/agents/design.agent.md .github/agents/coding.agent.md
git commit -m "Lab 4.2: add the design and coding agents"
```

**B — catching up.** Start from the checkpoint. It holds all four agent definitions.

```bash
cd ~/global-bank/global-bank-account
git switch -c GB-207-lab-4.2 m5-start
```

Then, for both A and B:

```bash
git branch GB-207-base
mkdir -p handoff/GB-207
mvn test
# expect: Failures: 0, Errors: 0. Tests run: 4, or more with A if your earlier labs added tests
```

`GB-207-base` marks where you started. Later you use it to produce the diff for the review agent.

Check that the four agents (**design**, **coding**, **test**, **review**) appear in the Chat view's
agent list.

An agent says it cannot read the Jira issue? Its `tools:` list is missing
`atlassian/jira_get_issue`. Add it to that agent file, save, and paste the prompt again in a new chat.

### Step 1 — Design: write the spec (chat 1)

In the Chat view, start a new chat and pick the **design** agent from the agent list.

**Prompt 4.2-A** · agent: **design** · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tools to
read that Jira issue, including its comments.
Write the spec for this ticket, in the shape your agent file gives for spec.md. Work only from
the ticket and the documents your agent file lists as inputs: global-bank-account/docs/adr/,
global-bank-account/docs/architecture.md and global-bank-account/docs/glossary.md.
Do not open the Java code.
Every claim about existing behaviour names the file it came from. List anything these
documents cannot answer under "Open questions". Do not guess.
Show the spec in the chat. Do not create or edit any file. Stop when the spec is shown.
```

**What you should see:** a spec with two or three options, one recommendation, the deciding rule with
its source file, and open questions.

**Check (gate 1, a person's check):** read the spec. Does every claim name a file? Is the
recommendation sound? Then create `global-bank-account/handoff/GB-207/spec.md` and paste the spec into
it.

### Step 2 — Coding: build the change (still chat 1)

Stay in the same chat. Switch the agent in the agent list from **design** to **coding**.

**Prompt 4.2-B** · agent: **coding** · base model · **same chat**

```text
Implement the spec in global-bank-account/handoff/GB-207/spec.md, in the global-bank-account
folder. Where the spec lists open questions, choose the answer the ticket supports, and name
each choice in your summary.
Do not write or change any test. Tests are the test agent's job.
Run "mvn test" in global-bank-account until the existing tests pass.
When you finish, write a summary: every file you changed, and why. Show it in the chat.
Do not edit anything under handoff/. Then stop.
```

**What you should see:** changes under `src/main`, no changes under `src/test`, and a summary naming
each file.

**Check:**

```bash
mvn test
# expect: Failures: 0, Errors: 0, and the same number of tests as before this step
git status
# expect: changes under src/main, and your new handoff/ folder. Nothing under src/test
```

Create `global-bank-account/handoff/GB-207/coding-summary.md` and paste the summary into it. Then
commit:

```bash
git add -A && git commit -m "GB-207: design and coding"
```

### Step 3 — Test: work from the ticket only (chat 2)

Start a **new chat**. Pick the **test** agent from the agent list.

**Prompt 4.2-C** · agent: **test** · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tools to
read that Jira issue, including its comments. The ticket is your only description of the
change.
Do not open any file under global-bank-account/handoff/.
Write tests in global-bank-account/src/test that prove each acceptance criterion, as the
ticket states it. Follow global-bank-account/.github/instructions/tests.instructions.md.
Do not change any file under src/main.
Run "mvn test" in global-bank-account. If a new test fails, do not change it to pass.
A failing test is a finding: report it.
Show the test report in the chat, in the shape your agent file gives. Then stop.
```

**What you should see:** new tests under `src/test`, a test run, and a report with one line per
acceptance criterion.

**Check:**
1. Scroll through the chat and look at each file the agent opened. Did it open anything in
   `handoff/`? If yes, this reading was not separate. Write that down in your verdict.
2. Run the tests yourself, and note every failing test by name:

   ```bash
   mvn test
   ```

A failing test here is not a problem with the lab. It may be the finding you are looking for.

Create `global-bank-account/handoff/GB-207/test-report.md` and paste the report into it. Then commit
the tests and produce the diff for the reviewer:

```bash
git add -A && git commit -m "GB-207: tests from the ticket"
git diff GB-207-base -- src > handoff/GB-207/change.diff
```

### Step 4 — Review: try to prove it wrong (chat 3)

Start a **new chat**. Pick the **review** agent from the agent list.

**Prompt 4.2-D** · agent: **review** · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tools to
read that Jira issue, including its comments.
The change is in global-bank-account/handoff/GB-207/change.diff. Also read
global-bank-account/docs/adr/, global-bank-account/docs/conventions.md and the files in
global-bank-account/.github/instructions/.
Do not open spec.md, coding-summary.md or test-report.md in the handoff folder.
Try to prove that this change does not meet the ticket. Work through your checklist in
order, and do not skip "what is missing". Then report what you could not disprove.
Show the review report in the chat, in the shape your agent file gives. Do not edit any file.
Then stop.
```

**What you should see:** a review report with findings by severity, each with a file, a line and the
rule or criterion it breaks. "Nothing found" is also a valid report.

**Check:** look at the files the agent opened. Did it open `spec.md`, `coding-summary.md` or
`test-report.md`? If yes, note it. Then create `global-bank-account/handoff/GB-207/review-report.md`,
paste the report and commit:

```bash
git add -A && git commit -m "GB-207: hand-off artifacts"
```

### Step 5 — Compare your agent files with the reference

Only if you started from your own Lab 4.1 files. In a terminal:

```bash
git diff m5-start -- .github/agents/test.agent.md .github/agents/review.agent.md
```

Look for one thing: a **Never** line in the reference that you did not think to write.

The reference files are an older layout. They call the hand-off contract "Outputs — the hand-off
artifact" and put it before Guardrails, and the test agent states its withheld input as a Never line,
not in Inputs. Your files follow this lab's seven-part order. Do not change yours to match.

### Record — the verdict

| Question | Your answer |
|---|---|
| Did any test fail? Which acceptance criterion? | |
| Did the coding agent and the test agent read the ticket differently? How? | |
| What did the reviewer find that the tests did not? | |
| Was any finding wrong? How many minutes did it take you to decide that? | |
| Did chat 2 or chat 3 open a file it should not have seen? | |
| A Never line in the reference that yours did not have (Step 5) | |

**Everything agreed?** That is a valid result. Check the last-but-one row first. Agreement is evidence
only if the two readings were really separate. If they were, record "agreed" and say so in the
debrief.

### If you are behind

Start from Set up, option **B** (`m5-start`). If time is short, keep chats 2 and 3 and use the
reference files. Never merge chats 2 and 3 into chat 1 to save time.

---

## Stretch lab 4.1+ (optional) — The design and coding agents

**Goal:** write the other two agent definitions yourself. Then Lab 4.2 uses all four of your own files.
Do this inside the Lab 4.1 timebox, after Step 4.

**Prompt 4.1+-A** · Agent mode · base model · **new chat**

```text
Create the file global-bank-account/.github/agents/design.agent.md. It defines a VS Code custom
agent named "design". Its job: read a ticket and recommend one of two or three options, naming
the rule that decides it. It writes no code.
First read global-bank-account/docs/adr/README.md and global-bank-account/docs/architecture.md.
Point to these files; do not copy them.
Start the file with YAML frontmatter that has: name: design, a one-line description,
version: 1, owner: TODO-OWNER, and a tools list. Put in the tools list only the tools this
role needs, chosen from: read, search, edit, execute, atlassian/jira_get_issue.
Then write seven sections, in this order: Role, Goal, Allowed tools, Inputs, Guardrails,
Hand-off contract, Never.
- Inputs: the ticket, the ADRs, docs/architecture.md and docs/glossary.md. Not the Java code.
- Hand-off contract: spec.md, shown in the chat, with: the problem in one paragraph, two or
  three options, a recommendation with the rule that decides it and its source file, and
  open questions.
- Never: at least three things this agent must never do, even when they seem reasonable.
Create only this one file. When it is written, list the tools you chose and give one line
of reason for each. Then stop.
```

**Prompt 4.1+-B** · Agent mode · base model · **new chat**

```text
Create the file global-bank-account/.github/agents/coding.agent.md. It defines a VS Code custom
agent named "coding". Its job: build what an agreed spec says, touching only the files it
needs. It does not change design decisions.
First read global-bank-account/.github/copilot-instructions.md and
global-bank-account/docs/conventions.md. Point to these files; do not copy them.
Start the file with YAML frontmatter that has: name: coding, a one-line description,
version: 1, owner: TODO-OWNER, and a tools list. Put in the tools list only the tools this
role needs, chosen from: read, search, edit, execute, atlassian/jira_get_issue.
Then write seven sections, in this order: Role, Goal, Allowed tools, Inputs, Guardrails,
Hand-off contract, Never.
- Guardrails: include the rule "Would design have chosen differently, if it had known? If
  yes, stop and hand back. If no, decide it and note it in the summary."
- Hand-off contract: the change, plus a summary naming every file touched and why.
- Never: at least three things this agent must never do, even when they seem reasonable.
Create only this one file. When it is written, list the tools you chose and give one line
of reason for each. Then stop.
```

**Check:** replace `TODO-OWNER` in both files. Run Prompt 4.1-C again, with the two new file names in
place of the old ones. Check that **design** and **coding** appear in the agent list, then commit.

---

## Stretch lab 4.2+ (optional) — The reviewer, with and without the rationale

**Goal:** see what the coder's rationale does to a review. Do this inside the Lab 4.2 timebox, after
Step 4.

Start a **new chat** and pick the **review** agent.

**Prompt 4.2+-A** · agent: **review** · base model · **new chat**

```text
Read course/labs/lab-keys.md to find my Jira key for GB-207. Use the atlassian MCP tools to
read that Jira issue, including its comments.
The change is in global-bank-account/handoff/GB-207/change.diff. Also read
global-bank-account/handoff/GB-207/spec.md and global-bank-account/handoff/GB-207/coding-summary.md.
They explain why the change was made this way.
Also read global-bank-account/docs/adr/, global-bank-account/docs/conventions.md and the files
in global-bank-account/.github/instructions/.
Try to prove that this change does not meet the ticket. Work through your checklist in
order, and do not skip "what is missing". Then report what you could not disprove.
Show the review report in the chat, in the shape your agent file gives. Do not edit any file.
Then stop.
```

Save the report as `global-bank-account/handoff/GB-207/review-report-with-rationale.md`.

**Compare** the two reports:

| Question | Without the rationale | With the rationale |
|---|---|---|
| Number of findings | | |
| Highest severity | | |
| Findings that appear in only one report | | |
| Does the report repeat the coder's reasons back to you? | | |
