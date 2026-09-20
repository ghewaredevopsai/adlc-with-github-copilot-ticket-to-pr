# Connect Copilot to your Jira and Confluence

Do this once, before Day 1. It takes about 20 minutes.

In the labs, Copilot reads tickets from **your own Jira project** and writes pages in **your own
Confluence space**. It does this through an **MCP server**. MCP (Model Context Protocol) is a standard
way to give Copilot extra tools. The server runs on your laptop, inside your network. It uses your
own access tokens, so Copilot sees only what you can see.

For this connection you need only **VS Code with the GitHub Copilot extension**, and Python. The labs
also need Git, JDK 25 and Maven, which [participants-instructions.md](../participants-instructions.md)
sets up.

## What you need

| Item | Check |
|---|---|
| VS Code with GitHub Copilot Chat, signed in | Copilot Chat opens, and the mode list shows **Agent** |
| Python 3.12 or newer | In a VS Code terminal: `python --version` (or `python3 --version`) |
| A Jira project you can create issues in | You can create an issue in it from the browser |
| A Confluence space you can create pages in | You can create a page in it from the browser |
| Your company allows MCP servers in Copilot | Your GitHub administrator controls this. Step 6 shows how to tell |

### Name your project and space

Use the **same key** for your Jira project and your Confluence space.

| Your setup | Key | Name |
|---|---|---|
| Your own Jira and Confluence site | `ADLC` | ADLC Workshop – Global Bank |
| One Jira shared with other participants | `ADLC` plus your seat number, for example `ADLC07` | ADLC Workshop – *your name* |

**Each participant needs their own project and space.** The ticket script skips a ticket that is
already in the project. In a shared project, it would give you someone else's tickets.

The Jira project must be a **software** project (Scrum or Kanban), with the issue types **Story**,
**Bug**, **Task** and **Epic**. A key has at most 10 characters: capital letters and digits,
starting with a letter.

The repositories must be in these folders, in your home folder:

```text
$HOME/
  adlc-with-github-copilot-ticket-to-pr/   the course repository
  global-bank/
    global-bank-account/
    global-bank-transaction/
    ...                                    the other Global Bank repositories
```

[participants-instructions.md](../participants-instructions.md) shows how to clone them.

## Step 1 — Create your access tokens

**Jira Data Center or Server** (most company Jira):
1. In Jira, open your profile picture, then **Profile**, then **Personal Access Tokens**.
2. Select **Create token**. Name it `adlc-labs`. Set it to expire after the course.
3. Copy the token now. Jira shows it only once.

**Confluence Data Center or Server:** do the same in Confluence. Confluence tokens are separate
from Jira tokens.

**Atlassian Cloud** (the address ends in `.atlassian.net`): create one **API token** at
id.atlassian.com, under **Security**, then **API tokens**. It works for both Jira and Confluence,
together with your email address.

Treat a token like a password. Do not paste it into a chat, a ticket or a commit.

## Step 2 — Fill in `.env`

In VS Code, open the course repository. Copy `.env.example` to a new file named `.env`, in the same
folder. Then fill it in:

| Setting | What to put |
|---|---|
| `JIRA_URL` | Your Jira address, for example `https://jira.yourcompany.com` |
| `JIRA_PERSONAL_TOKEN` | The Jira token from step 1 |
| `JIRA_PROJECT_KEY` | Your project's key, for example `ADLC` or `ADLC07`. See [Name your project and space](#name-your-project-and-space). The lab tickets go here |
| `JIRA_PROJECTS_FILTER` | The same key. It stops Copilot searching other projects |
| `CONFLUENCE_URL` | Your Confluence address |
| `CONFLUENCE_PERSONAL_TOKEN` | The Confluence token from step 1 |
| `CONFLUENCE_SPACE_KEY` and `CONFLUENCE_SPACES_FILTER` | Your space's key |
| `ENABLED_TOOLS` | Leave as it is. See [What Copilot is allowed to do](#what-copilot-is-allowed-to-do) |

On **Atlassian Cloud**, leave the two `PERSONAL_TOKEN` lines empty. Set `JIRA_USERNAME`,
`JIRA_API_TOKEN`, `CONFLUENCE_USERNAME` and `CONFLUENCE_API_TOKEN` instead. Your Confluence
address then ends in `/wiki`.

`.env` is listed in `.gitignore`, so git never commits it. Check with `git status`: `.env` must not
appear.

## Step 3 — Check that your laptop can reach Jira and Confluence

In a VS Code terminal, at the root of the course repository:

```bash
python labs/scripts/setup-lab-tickets.py --check
```

You should see:

```text
Jira OK: signed in as <your name>, project ADLC.
Keys written to labs/lab-keys.md
Confluence OK: space ADLC.
  missing  page 'Global Bank'. Create it: see labs/confluence-setup.md
```

The `missing` line is expected the first time. A new space has no page about Global Bank yet.

`labs/lab-keys.md` holds your project and space keys, and later your ticket keys. It holds no
secrets, so Copilot may read it. The lab prompts point Copilot at this file. **Never ask Copilot to
read `.env`**: that would send your tokens to the model.

If you see an error instead, go to [If something goes wrong](#if-something-goes-wrong). Do not go on
until both lines say OK.

**Now set up your Confluence pages.** Follow [confluence-setup.md](confluence-setup.md). It creates the
two pages the labs use, and takes about 5 minutes. Then come back here for step 4. Run the check again
afterwards: both pages now say `exists`.

## Step 4 — Install the MCP server's launcher

The server is a Python package called `mcp-atlassian`. A small tool called `uv` downloads it and
runs it. Install `uv` once, with the command for your operating system.

**macOS or Linux:**

```bash
python3 -m pip install --user --break-system-packages uv
```

Without `--break-system-packages`, pip may stop with `externally-managed-environment`. That error
protects the Python that came with your system. `--user` puts `uv` in your home folder only, so the
system Python is not changed.

**Windows:**

```bash
python -m pip install --user uv
```

Then check that the server starts:

```bash
uvx mcp-atlassian --version
```

You should see `mcp-atlassian, version 0.23` or newer. The first run downloads about 100 packages,
through your company's Python package mirror.

## Step 5 — Open the lab workspace

If you already opened it in Step 3 of
[participants-instructions.md](../participants-instructions.md), it is the same workspace: skip to
Step 6.

In VS Code, select **File**, then **Open Workspace from File**, and pick `adlc-labs.code-workspace`
in the course repository. The Explorer now shows eight folders: `course` and the seven
`global-bank-*` repositories.

The workspace file tells VS Code how to start the MCP server:

```json
"atlassian": {
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-atlassian"],
  "envFile": "${workspaceFolder:course}/.env"
}
```

`envFile` is the important line. The server reads your URLs and tokens from `.env`, so the tokens are
never written into the workspace file.

## Step 6 — Start the server

1. Open the Command Palette (`Ctrl+Shift+P`, or `Cmd+Shift+P` on a Mac).
2. Run **MCP: List Servers**.
3. Select **atlassian**, then **Start Server**. If VS Code asks whether you trust this server, choose
   **Trust**.
4. Run **MCP: List Servers** again. **atlassian** should say **Running**.

To see what went wrong, select the server and choose **Show Output**.

If there is no **MCP** command at all, or the server never appears, your company has probably turned
MCP off in Copilot. Only your GitHub administrator can change that. Tell your trainer before Day 1.

## Step 7 — Check the tools

1. Open Copilot Chat and switch the mode to **Agent**.
2. Select the **tools** icon in the chat box.
3. Find **atlassian**. It should list the ten tools from [What Copilot is allowed to do](#what-copilot-is-allowed-to-do).

## Step 8 — Test it with two prompts

Paste each prompt into Copilot Chat, in **Agent** mode, in a new chat.

**Test 1 — Jira**

```text
Use the atlassian MCP tools. Read course/labs/lab-keys.md to find my Jira project key.
List the five most recent issues in that project. For each one, show the key, the summary
and the status. Do not change anything, and do not open any other file.
```

Copilot asks to run `jira_search` or `jira_get_project_issues`. Select **Allow**. It then shows up to
five issues. An empty project is fine: Copilot says there are no issues, and no error appears.

**Test 2 — Confluence**

```text
Use the atlassian MCP tools. Read course/labs/lab-keys.md to find my Confluence space key
and the CONFLUENCE-HOME page id. Show the title of that page, and list the titles of the
pages under it. Do not change anything, and do not open any other file.
```

Copilot asks to run `confluence_get_page` and `confluence_get_page_children`. You see the title
**Global Bank**, and one page under it: **Global Bank posting API - decisions**.

Both tests pass? You are ready. Load the Module 1 ticket as `labs/README.md` describes.

## What Copilot is allowed to do

The server offers about 100 tools. `ENABLED_TOOLS` in `.env` switches on only the ten the labs need.
Fewer tools also help Copilot choose the right one.

| Tool | What it does | Used in |
|---|---|---|
| `jira_get_issue` | Reads one issue: description, comments, links | Every lab with a ticket |
| `jira_search` | Finds issues with a JQL query | Setup check (test 1). Module 6 counts it when Copilot uses it without being asked |
| `jira_get_project_issues` | Lists the issues in your project | Setup check (test 1) |
| `jira_add_comment` | Adds a comment to an issue. **The only Jira write** | Modules 5 (stretch), 6 and 8 |
| `confluence_search` | Finds pages | No lab step asks for it. Copilot may use it to find a page |
| `confluence_get_page` | Reads a page | Setup check (test 2) |
| `confluence_get_page_children` | Lists the pages under a page | Setup check (test 2) |
| `confluence_create_page` | Creates a page | Module 8 (stretch 8.1+) and the capstone |
| `confluence_update_page` | Edits a page | Only to fix a page Copilot just created. The prompts forbid editing any other page |
| `confluence_add_comment` | Comments on a page | No lab step asks for it |

Copilot cannot change an issue's status, fields or assignee, and it cannot delete anything. Module 6
explains why this split is a good default for your team as well.

Each time Copilot wants to use a tool, VS Code asks you first. Read the request before you select
**Allow**. That check is part of the course.

## If something goes wrong

| What you see | What to do |
|---|---|
| `HTTP 401` in step 3 | The token is wrong or has expired. Create a new one (step 1) |
| `HTTP 403` or `HTTP 404` for the project | The project key is wrong, or you have no access to that project |
| `Cannot reach …` in step 3 | Your laptop cannot see Jira from this network. Connect to the network or VPN you use for Jira |
| `CERTIFICATE_VERIFY_FAILED` | Your company uses its own certificate authority. Ask IT for its certificate file. Add two lines to `.env`: `SSL_CERT_FILE=<path to the file>` and `REQUESTS_CA_BUNDLE=<the same path>` |
| `Cannot reach …`, and you normally use a proxy | Set `HTTPS_PROXY` (and `NO_PROXY` if needed) in `.env`. The script and the server both read them |
| `uvx` is not found | Close and reopen the terminal. Still missing? Use the fallback below |
| `externally-managed-environment` from pip | Add `--break-system-packages` to the command, as step 4 shows for macOS and Linux |
| `pip install` is blocked | Ask IT for the company Python package mirror. The labs cannot run without it |
| The server stops as soon as it starts | Run **MCP: List Servers**, select **atlassian**, then **Show Output**. The last lines say why |
| Test 2 finds no `CONFLUENCE-HOME` in `lab-keys.md` | You skipped the Confluence pages. Follow [confluence-setup.md](confluence-setup.md) |
| Copilot says it has no Jira tools | Check that the chat mode is **Agent**, and that **atlassian** is ticked in the tools list |

**Fallback: without `uv`.** Install the server directly:

```bash
python -m pip install --user mcp-atlassian
```

On macOS or Linux, use `python3` and add `--break-system-packages`, as in step 4.

Then, in `adlc-labs.code-workspace`, change the server's `"command": "uvx"` to
`"command": "mcp-atlassian"`, and change `"args"` to `[]`.

## No Jira or Confluence at all?

Use GitHub issues instead. The lab tickets become issues in a GitHub repository, and Copilot reads
them through the **github** MCP server. The prompts in the guides are written for Jira, so you add
one line above each of them. Everything else in the labs is the same.

### Set it up once

1. In `.env`, set `GITHUB_REPO` (the repository your issues go in, as `owner/name`) and
   `GITHUB_TOKEN` (a fine-grained personal access token with **Issues: read and write** on that
   repository).
2. Check it: `python labs/scripts/setup-lab-tickets.py --check --target github`. You should see
   `GitHub OK: <owner/name>.`
3. Start the **github** server instead of **atlassian**, the same way as in step 6. Sign in to GitHub
   when VS Code asks. In step 7, look for **github** in the tools list instead.

### In every lab

- **Loading tickets.** Add `--target github` to every `setup-lab-tickets.py` command in the guides.
  For example: `python labs/scripts/setup-lab-tickets.py --module 1 --target github`.
  `labs/lab-keys.md` then maps each lab ticket to an issue number, such as `#7`.
- **Prompts.** Paste this line first, then the prompt from the guide, unchanged:

  ```text
  I use GitHub issues, not Jira. Read every "Jira key" below as a GitHub issue number, and every "Jira issue" or "Jira ticket" as a GitHub issue, in the repository named in course/labs/lab-keys.md. Instead of jira_get_issue use the github tool issue_read, instead of jira_add_comment use add_issue_comment, and instead of jira_search use search_issues. "Jira tools" and "Jira calls" mean these github tools, and "Do not search Jira" or "Never search Jira" means do not search GitHub issues. GitHub issues have no links, epics or "blocked by" fields: a linked issue, an epic or an issue that blocks this one appears as a #number in the issue body or its comments, so read each #number issue it mentions.
  ```

  GitHub has no issue links. So when a prompt says "each issue it links to", "the epic" or "an issue
  that blocks this one", Copilot finds them as `#12`-style references in the issue text, for example
  "blocked by #12". The line above tells it to read those issues too.

- **Module 8, Confluence steps** (Prompts 8.1-D and C14). There is no Confluence page to write to.
  Paste this line as well, under the first one:

  ```text
  I have no Confluence. Instead of confluence_create_page, write the page as a new Markdown file in global-bank-account/docs/pages/, named after the page title, with the same content. There is no CONFLUENCE-PAGE parent. Do not edit any other file.
  ```

- **Custom agents** (Module 4 onwards). Their `tools:` lines name `atlassian/jira_get_issue`, so an
  agent cannot read a GitHub issue. Each time you make a branch from a checkpoint tag, send this in
  a new chat, in Agent mode, before the lab's first prompt:

  ```text
  In global-bank-account/.github/agents/, replace atlassian/jira_get_issue with github/issue_read in every tools: line. Change nothing else. Then show me the tools: lines.
  ```

Your numbers still count. Write "GitHub issues" in the notes line of your record prompt, so it lands
in `metrics.md`: the extra line adds nothing to your turns, but the tool names differ from everyone
else's.
