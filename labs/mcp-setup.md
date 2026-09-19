# Connect Copilot to your Jira and Confluence

Do this once, before Day 1. It takes about 20 minutes.

In the labs, Copilot reads tickets from **your own Jira project** and writes pages in **your own
Confluence space**. It does this through an **MCP server**. MCP (Model Context Protocol) is a standard
way to give Copilot extra tools. The server runs on your laptop, inside your network. It uses your
own access tokens, so Copilot sees only what you can see.

You need only **VS Code with the GitHub Copilot extension**, and Python. No other command-line tools
are needed.

## What you need

| Item | Check |
|---|---|
| VS Code with GitHub Copilot Chat, signed in | Copilot Chat opens, and the mode list shows **Agent** |
| Python 3.12 or newer | In a VS Code terminal: `python --version` (or `python3 --version`) |
| A Jira project you can create issues in | You can create an issue in it from the browser |
| A Confluence space you can create pages in | You can create a page in it from the browser |
| Your company allows MCP servers in Copilot | Your GitHub administrator controls this. Step 6 shows how to tell |

The three repositories must sit side by side in one folder:

```text
<your folder>/
  <this course repository>
  global-bank-account
  global-bank-transaction
```

`labs/README.md` shows how to clone them.

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
| `JIRA_PROJECT_KEY` | Your project's key, for example `ADLC`. The lab tickets go here |
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
Confluence OK: space ADLC.
Keys written to labs/lab-keys.md
```

`labs/lab-keys.md` holds your project and space keys, and later your ticket keys. It holds no
secrets, so Copilot may read it. The lab prompts point Copilot at this file. **Never ask Copilot to
read `.env`**: that would send your tokens to the model.

If you see an error instead, go to [If something goes wrong](#if-something-goes-wrong). Do not go on
until both lines say OK.

## Step 4 — Install the MCP server's launcher

The server is a Python package called `mcp-atlassian`. A small tool called `uv` downloads it and
runs it. Install `uv` once:

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

In VS Code, select **File**, then **Open Workspace from File**, and pick `adlc-labs.code-workspace`
in the course repository. The Explorer now shows three folders: `course`, `global-bank-account` and
`global-bank-transaction`.

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
Use the atlassian MCP tools. Read course/labs/lab-keys.md to find my Confluence space key.
List the titles of up to five pages in that space. Do not change anything, and do not open
any other file.
```

You see up to five page titles, or a message that the space is empty.

Both tests pass? You are ready. Load the Module 1 ticket as `labs/README.md` describes.

## What Copilot is allowed to do

The server offers about 100 tools. `ENABLED_TOOLS` in `.env` switches on only the ten the labs need.
Fewer tools also help Copilot choose the right one.

| Tool | What it does | Used in |
|---|---|---|
| `jira_get_issue` | Reads one issue: description, comments, links | Every lab with a ticket |
| `jira_search` | Finds issues with a JQL query | Module 6 |
| `jira_get_project_issues` | Lists the issues in your project | Setup check |
| `jira_add_comment` | Adds a comment to an issue. **The only Jira write** | Modules 5 (stretch), 6 and 8 |
| `confluence_search` | Finds pages | Module 8 |
| `confluence_get_page` | Reads a page | Module 8 |
| `confluence_get_page_children` | Lists the pages under a page | Module 8 |
| `confluence_create_page` | Creates a page | Module 8, capstone |
| `confluence_update_page` | Edits a page | Module 8, capstone |
| `confluence_add_comment` | Comments on a page | Module 8 |

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
| `pip install` is blocked | Ask IT for the company Python package mirror. The labs cannot run without it |
| The server stops as soon as it starts | Run **MCP: List Servers**, select **atlassian**, then **Show Output**. The last lines say why |
| Copilot says it has no Jira tools | Check that the chat mode is **Agent**, and that **atlassian** is ticked in the tools list |

**Fallback: without `uv`.** Install the server directly:

```bash
python -m pip install --user mcp-atlassian
```

Then, in `adlc-labs.code-workspace`, change the server's `"command": "uvx"` to
`"command": "mcp-atlassian"`, and change `"args"` to `[]`.

## No Jira or Confluence at all?

Use GitHub issues instead. Only the ticket source changes. The labs are otherwise the same.

1. In `.env`, set `GITHUB_REPO` (the repository your issues go in) and `GITHUB_TOKEN` (a
   fine-grained personal access token with **Issues: read and write** on that repository).
2. Run the setup script with `--target github`, as each lab guide shows.
3. Use the **github** server in the workspace instead of **atlassian**. Start it the same way as in
   step 6, and sign in to GitHub when VS Code asks.

The Confluence steps in Module 8 then write to `docs/` in the repository instead.
