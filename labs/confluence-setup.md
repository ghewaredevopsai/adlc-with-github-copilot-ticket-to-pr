# Set up your Confluence pages

Do this once, before Day 1. It takes about 5 minutes. [mcp-setup.md](mcp-setup.md) sends you here
after its step 3.

## Why you need this

A new Confluence space holds only one page: the space home page, with Confluence's "Welcome to your
new space" text. Nothing in the space says what Global Bank is. There is also no page for your lab
pages to go under.

In Module 8 and the capstone, Copilot creates pages under a **parent page**. The prompts find the
parent's id in `labs/lab-keys.md`. Without that page, Copilot has no id to use, and the step fails.
The Confluence check in [mcp-setup.md](mcp-setup.md) (test 2) also has nothing to find.

## What the script creates

The script creates two pages in your space and writes their ids to `labs/lab-keys.md`:

```text
Your space (for example ADLC)
  <space name> Home                        Confluence made this page with the space
    Global Bank                            what the app is: the seven repositories, their
                                           ports, and where the documents live
                                           → CONFLUENCE-HOME in lab-keys.md
      Global Bank posting API - decisions  the decisions (ADRs) of the posting API
                                           → CONFLUENCE-PAGE in lab-keys.md
        ADR-011 — Reversal as a ...        you add this page in Lab 8.1+
        GB-186 — Payroll batch ...         you add this page in the capstone
```

The code stays the source of truth. These pages are short pointers to it, for people who do not read
the code.

## Step 1 — Check that you can create pages

Open your space in the browser. Select **+ Create** (or **Create**). If you can start a new page, you
have the permission you need. Close the new page without saving it.

Cannot create pages? See [If something goes wrong](#if-something-goes-wrong).

## Step 2 — Create the pages

In a VS Code terminal, at the root of the course repository:

```bash
cd ~/adlc-with-github-copilot-ticket-to-pr
python labs/scripts/setup-lab-tickets.py --confluence
```

On macOS or Linux, use `python3` if `python` is not found. You should see:

```text
Confluence OK: space ADLC.
  created  page 1234567 'Global Bank'
  created  page 1234568 'Global Bank posting API - decisions'
Keys written to labs/lab-keys.md
```

Your page ids are different. Running the command again is safe: it says `exists` and creates nothing.

## Step 3 — Check `labs/lab-keys.md`

Open `labs/lab-keys.md`. The table now has two new lines:

```text
| CONFLUENCE-HOME | 1234567 |
| CONFLUENCE-PAGE | 1234568 |
```

## Step 4 — Check the pages in the browser

1. Open your space. Under the space home page, you see **Global Bank**.
2. Open **Global Bank**. It shows a table of the seven repositories. At the bottom, under "Pages under
   this page", it lists **Global Bank posting API - decisions**.
3. Open **Global Bank posting API - decisions**. It shows a table of four ADRs.

The welcome text on the space home page does not matter to the labs. You may replace it with a link to
**Global Bank**, or leave it.

Now go back to [mcp-setup.md, step 4](mcp-setup.md#step-4--install-the-mcp-servers-launcher). Test 2
at the end of that guide asks Copilot to read these pages.

## If something goes wrong

| What you see | What to do |
|---|---|
| `HTTP 401` | The Confluence token in `.env` is wrong or has expired. Create a new one ([mcp-setup.md, step 1](mcp-setup.md#step-1--create-your-access-tokens)) |
| `HTTP 404` for the space | The space key is wrong. Find the key in the space's address: `/spaces/ADLC/` or `/display/ADLC/`. Set `CONFLUENCE_SPACE_KEY` and `CONFLUENCE_SPACES_FILTER` in `.env` |
| `HTTP 403` when the page is created | You cannot create pages in this space. Ask the space administrator for the **Add pages** permission, or use your personal space (next line) |
| You cannot create a space, and have no space of your own | Use your **personal space**. Open your profile picture, then **Personal space**. Its key starts with `~`, for example `~jdoe`. Put that key in `.env`, in `CONFLUENCE_SPACE_KEY` and `CONFLUENCE_SPACES_FILTER` |
| The first run says `exists`, not `created` | Someone else already made these pages in this space. Page titles are unique in a space, so the script found theirs. Use your own space, then run step 2 again |
| The pages are at the top of the space, not under the home page | Your space has no home page. That is fine: the labs need only the two ids |
| `Confluence skipped: set CONFLUENCE_URL ...` | `.env` is missing a Confluence setting. Fill it in ([mcp-setup.md, step 2](mcp-setup.md#step-2--fill-in-env)) |

**No Confluence at all?** Skip this guide. In Module 8, you write the pages as Markdown files instead.
See [No Jira or Confluence at all?](mcp-setup.md#no-jira-or-confluence-at-all).
