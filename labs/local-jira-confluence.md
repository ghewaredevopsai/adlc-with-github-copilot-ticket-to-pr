# Local Jira and Confluence: setup instructions for a Copilot agent

**Reader: GitHub Copilot in Agent mode**, opened on `adlc-labs.code-workspace`. A participant asks you
to "set up local Jira and Confluence". Follow these steps in order, in a bash terminal (Git Bash on
Windows). Stop and report if a check fails.

**What you are installing.** `labs/scripts/local-atlassian.py` is a small open-source (MIT) server,
using only the Python standard library. It answers the part of the Jira and Confluence Data Center REST API that the labs use.
It is **not** Atlassian software, and it needs no licence, Java, Docker or admin rights. The
`atlassian` MCP server in `adlc-labs.code-workspace` stays **unchanged**. Only four values in `.env` change.
Data is kept in `$HOME/adlc-copilot-training/local-atlassian/data.json`.

## Rules for you, the agent

- **Never print, `cat`, open or quote `.env`.** It may hold the participant's real tokens. Change it only
  with the commands in step 3.
- Run every command from the course repository root: `$HOME/adlc-copilot-training/adlc-with-github-copilot-ticket-to-pr`.
- Use `python`. If that is not found, use `python3` for every command instead.
- Do not edit the workspace file, the server script, or any Global Bank repository.

## Step 1: Check Python

```bash
cd "$HOME/adlc-copilot-training/adlc-with-github-copilot-ticket-to-pr" && python --version
```

Needs Python 3.8 or newer.

## Step 2: Start the server in a background terminal

Run this as a **background** terminal command. It keeps running, and it must stay running whenever the
labs use Jira or Confluence:

```bash
python labs/scripts/local-atlassian.py
```

It prints `JIRA_URL=http://127.0.0.1:8990/jira` and `CONFLUENCE_URL=http://127.0.0.1:8990/confluence`,
and creates Jira project `ADLC` and Confluence space `ADLC`. Then check it, in a normal terminal:

```bash
curl -s -H "Authorization: Bearer local" http://127.0.0.1:8990/jira/rest/api/2/myself
```

Expect JSON with `"displayName": "Lab Participant"`. If you see `Address already in use`, see the table below.

## Step 3: Point `.env` at the server

If `.env` already exists, first ask the participant: *"Your `.env` may hold your company Jira settings.
Can I keep a copy as `.env.company` and point `.env` at the local server?"* Continue only on yes.

```bash
[ -f .env ] && ! grep -q '^JIRA_URL=http://127.0.0.1' .env && cp .env .env.company
[ -f .env ] || cp .env.example .env
sed -E -i.bak '/^(JIRA|CONFLUENCE)_(URL|PERSONAL_TOKEN|USERNAME|API_TOKEN|PROJECT_KEY|PROJECTS_FILTER|SPACE_KEY|SPACES_FILTER)=/d' .env && rm -f .env.bak
cat >> .env <<'END'
# Local Jira and Confluence stand-in: labs/local-jira-confluence.md
JIRA_URL=http://127.0.0.1:8990/jira
JIRA_PERSONAL_TOKEN=local
JIRA_PROJECT_KEY=ADLC
JIRA_PROJECTS_FILTER=ADLC
CONFLUENCE_URL=http://127.0.0.1:8990/confluence
CONFLUENCE_PERSONAL_TOKEN=local
CONFLUENCE_SPACE_KEY=ADLC
CONFLUENCE_SPACES_FILTER=ADLC
END
grep -q '^HTTPS_PROXY=' .env && ! grep -q '^NO_PROXY=.*127\.0\.0\.1' .env && echo 'NO_PROXY=127.0.0.1,localhost' >> .env
grep -cE '^(JIRA_URL=http://127|CONFLUENCE_URL=http://127|JIRA_PROJECT_KEY=ADLC|CONFLUENCE_SPACE_KEY=ADLC)' .env
```

The last line must print `4`. `.env.company` is gitignored, like `.env`. Running this step again is safe: it
never overwrites `.env.company` with the local settings.

## Step 4: Create the Confluence pages, and check

```bash
python labs/scripts/setup-lab-tickets.py --confluence
python labs/scripts/setup-lab-tickets.py --check
```

Expect `Jira OK: signed in as Lab Participant, project ADLC.`, then `Confluence OK: space ADLC.` with
`page 'Global Bank'` and `page 'Global Bank posting API - decisions'` both listed. The `missing GB-…` lines
are expected: each module's lab guide loads its own tickets.

## Step 5: Hand back to the participant

You cannot restart an MCP server yourself. Tell the participant, in these words:

> The local Jira and Confluence are running. Now restart the MCP server so it reads the new `.env`:
> Command Palette, **MCP: List Servers**, **atlassian**, **Restart Server**. Then run the two test prompts
> in `labs/mcp-setup.md`, step 8. You can also browse your issues at http://127.0.0.1:8990/jira/ and your
> pages at http://127.0.0.1:8990/confluence/. Keep the terminal running `local-atlassian.py` open all day.

## Every later session

The server does not start by itself. Run step 2 again, then restart the `atlassian` MCP server. The data is
kept. To start over, stop the server with `Ctrl+C` and delete `$HOME/adlc-copilot-training/local-atlassian/`.
To go back to company Jira: `cp .env.company .env`, then restart the MCP server.

## If something goes wrong

| What you see | What to do |
|---|---|
| `Address already in use` | Start with `--port 8991`. In `.env`, change both `8990` to `8991` with `sed -i.bak 's#:8990/#:8991/#' .env && rm .env.bak` |
| `Cannot reach http://127.0.0.1:8990/...` | The server is not running. Do step 2 again |
| `HTTP 401` | A token is empty. Re-run step 3 |
| `HTTP 400 ... Project 'X' does not exist` | `.env` names a project other than `ADLC`. Re-run step 3 |
| MCP tools fail but step 4 passes | The MCP server still has the old `.env`. Restart it (step 5) |
| The server log says `JQL field ... is not supported` | That part of the search was ignored, so the result may hold extra issues. Nothing to fix |

**Limits.** It is enough for the labs, not a full Jira. There is one user, no permissions and no boards.
Workflows are fixed: To Do, In Progress, Won't Do, Done. Search understands the common JQL and CQL: `=`, `!=`, `~`,
`IN`, `IS EMPTY`, `AND`, `OR`, `NOT`, `ORDER BY` and `linkedIssues()`. Nothing is ever deleted. It listens on
`127.0.0.1` only and accepts any token, so never expose it to a network.
