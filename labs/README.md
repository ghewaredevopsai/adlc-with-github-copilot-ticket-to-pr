# Labs — how they work, and one-time setup

The course has **14 labs and a capstone**, across 8 modules. Each module has one guide:

| Day | Guide | Labs |
|---|---|---|
| 1 | [Module 1 — The ADLC operating model and token economics](module-1-labs.md) | 1.1 |
| 1 | [Module 2 — Knowledge harnessing](module-2-labs.md) | 2.1 · 2.2 |
| 1 | [Module 3 — Prompt and context engineering](module-3-labs.md) | 3.1 · 3.2 |
| 1 | [Module 4 — Specialised agents](module-4-labs.md) | 4.1 · 4.2 |
| 2 | [Module 5 — Spec-driven development](module-5-labs.md) | 5.1 · 5.2 |
| 2 | [Module 6 — The ticket as the unit of work](module-6-labs.md) | 6.1 · 6.2 |
| 2 | [Module 7 — Multi-repo engineering](module-7-labs.md) | 7.1 · 7.2 |
| 2 | [Module 8 — Closing the loop](module-8-labs.md) | 8.1 · capstone |

Every lab also has an **optional stretch lab**, marked with a `+` (for example **1.1+**). Do it if
you finish early. Nobody waits for it, and it is not scored.

## How a lab step looks

Every step gives you a prompt to copy into **Copilot Chat**. The line above each prompt tells you how
to run it:

> **Prompt 1.1-A** · Agent mode · base model · **new chat**

- **Agent mode:** in the Copilot Chat box, set the mode to **Agent**. Some steps say **Ask**.
- **Base model** or **premium reasoning model:** pick the model class the step names, from the model
  list in the chat box. Your trainer shows which models count as which on Day 1.
- **New chat:** start a new chat first (the **+** at the top of the Chat view). **Same chat:** stay
  in the chat you are in.

Copy the prompt **exactly**. Everyone runs the same words, so the numbers on the board compare fairly.

When Copilot asks to run a command or a tool, **read the request before you select Allow**.

## What you count

Labs 1.1, 2.2 and the capstone are **measured runs**. You count six numbers on your
[tally](board/README.md) as you go, not afterwards:

| Counter | What it counts |
|---|---|
| **Turns** | Every prompt you send, including repair prompts |
| **Tool calls** | Files Copilot opened or searched. The chat shows each one |
| **Asked** | Questions Copilot asked you that a file in the repository could have answered |
| **Rework** | Repair prompts you had to send (they also count as turns) |
| **Churn** | Lines Copilot wrote and then threw away, to the nearest ten |
| **Clock** | Minutes from your first prompt to a change you would raise a pull request for |

A measured run has one **repair prompt**. Paste it only when a check fails. It is the same for
everyone, so the number of repairs is what differs between your runs.

## One-time setup (before Day 1)

### 1. Tools

- VS Code with **GitHub Copilot Chat**, signed in
- Git
- **JDK 25** and **Maven 3.9** or newer. Check with `java -version` and `mvn -version`
- **Python 3.12** or newer (for the ticket script)

### 2. Clone the three repositories side by side

Clone, do not fork. Put all three in one folder:

```bash
mkdir adlc && cd adlc
git clone <this course repository URL>
git clone https://github.com/brainupgrade-in/global-bank-account.git
git clone https://github.com/brainupgrade-in/global-bank-transaction.git
```

Then fetch the lab checkpoints. They are git tags, and a plain clone does not always bring them all:

```bash
cd global-bank-account && git fetch --tags && cd ..
cd global-bank-transaction && git fetch --tags && cd ..
```

Check that it worked: `git -C global-bank-account tag` lists `m1-start` … `capstone-start`.

**Your pull requests** go to a copy of these repositories that your team can push to, for example in
your company's GitHub organisation. Your trainer tells you which one on Day 1. Until then, you work
on local branches, and nothing needs pushing.

### 3. Build both once

```bash
cd global-bank-account && git switch -c setup-check m1-start && mvn test
# expect: Tests run: 4, Failures: 0, Errors: 0
cd ../global-bank-transaction && git switch -c setup-check m1-start && mvn test
# expect: Tests run: 2, Failures: 0, Errors: 0
```

The first build downloads Maven packages, so it takes a few minutes. You may see long `jacoco`
warnings in `global-bank-account`. They are harmless: look only at the `Tests run` line.

### 4. Connect Copilot to your Jira and Confluence

Follow [mcp-setup.md](mcp-setup.md). At the end, both test prompts must work.

### 5. Open the lab workspace

In VS Code: **File**, then **Open Workspace from File**, then `adlc-labs.code-workspace` in the course
repository. Always work from this workspace. It shows all three repositories, and it starts the Jira
and Confluence connection.

## Tickets: your own keys

The lab tickets (GB-142, GB-151 …) are loaded into **your** Jira project, one module at a time. Each
guide tells you when:

```bash
python labs/scripts/setup-lab-tickets.py --module 1
```

Jira gives each ticket its own key, such as `ADLC-7`. The script writes `labs/lab-keys.md`, which
maps each lab ticket to your key. **The prompts tell Copilot to look the key up in that file**, so you
paste them unchanged.

Running the script twice is safe: it skips tickets that already exist. No Jira at all? See the
fallback at the end of [mcp-setup.md](mcp-setup.md).

## Checkpoints: catching up

Each lab starts from a **checkpoint**: a git tag that holds the code as that lab expects it. Every
guide says which tag to start from. If you did not finish a lab, start the next one from its tag. You
lose nothing that the next lab needs.

| Tag | What the repository holds |
|---|---|
| `m1-start` | The posting code only. No team knowledge written down |
| `m2.2-start`, `m3-start` | Adds the team knowledge: instructions, architecture, conventions, glossary, ADRs |
| `m4-start` | Adds the `account-change` skill file and the `gb-change` prompt file |
| `m5-start`, `m6-start`, `m7-start`, `capstone-start` | Adds the design, coding, test and review agents |

`m2.2-start`, `m4-start` and `m5-start` each hold a **reference answer**: the knowledge files (Lab
2.1), the skill file (Lab 3.1) and the agents (Lab 4.1). Try each lab yourself first. Look at the tag
only to catch up, or to compare afterwards. The later tags add nothing new, because Modules 5 to 8
work on tickets, not on files the repository keeps.

Start every lab on a new branch from its tag, named after the ticket and the lab:

```bash
git switch -c GB-142-lab-1.1 m1-start
```

## If Copilot goes wrong

- It edits the wrong thing: select **Undo** on the change in the chat, or run `git restore .` in the
  repository.
- It gets stuck: stop it with the **Stop** button, then start a new chat and paste the step's prompt
  again.
- It asks to run a command you do not understand: select **Skip**, and ask your trainer.
