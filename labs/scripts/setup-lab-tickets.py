#!/usr/bin/env python3
"""Load the lab tickets into YOUR Jira project (or, as a fallback, your GitHub repository).

Each file in labs/tickets/ becomes one ticket, with its labels, comments and links. Run it once per
module, when the lab guide tells you to. Running it again is safe: a ticket that already exists is
left alone.

    python3 labs/scripts/setup-lab-tickets.py --check              # test the .env settings, create nothing
    python3 labs/scripts/setup-lab-tickets.py --module 1           # Jira (the default)
    python3 labs/scripts/setup-lab-tickets.py --module 8           # also creates the Confluence page
    python3 labs/scripts/setup-lab-tickets.py --module 1 --target github   # fallback: GitHub issues

Settings come from the .env file at the root of your course-repo clone (copy .env.example).
Jira and Confluence assign their own keys, so the script writes labs/lab-keys.md: it maps each
lab ticket (GB-142 ...) to your real key. The lab prompts read that file.

Python 3.8+ standard library only. No other tools are needed.
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

LABS = Path(__file__).resolve().parent.parent
TICKETS = LABS / "tickets"
KEYS_FILE = LABS / "lab-keys.md"
ENV_FILE = LABS.parent / ".env"

META = re.compile(r"<!--\s*module:\s*([^·]+?)\s*·\s*labels:\s*([^·]+?)\s*(?:·\s*state:\s*(\S+)\s*)?-->")
COMMENT = re.compile(r"<!--\s*comment:\s*(.+?)\s*-->")
PLACEHOLDER = re.compile(r"\{([A-Z]+-\d+)\}")
BLOCKED_BY = re.compile(r"blocked by \{([A-Z]+-\d+)\}", re.IGNORECASE)
ISSUE_TYPES = {"bug": "Bug", "story": "Story", "task": "Task", "epic": "Epic", "risk": "Task"}
LABEL_COLOURS = {"bug": "d73a4a", "story": "0e8a16", "task": "c5def5", "epic": "5319e7",
                 "risk": "b60205", "agent-ready": "1d76db", "eval-set": "fbca04", "wont-do": "ffffff"}

CONFLUENCE_TITLE = "Global Bank posting API - decisions"
CONFLUENCE_BODY = (
    "<p>Decisions for the posting API in <code>global-bank-account</code>. The full ADRs live in the "
    "repository under <code>docs/adr/</code>; this page is where the team reads them.</p>"
    "<table><tbody>"
    "<tr><th>ADR</th><th>Decision</th></tr>"
    "<tr><td>ADR-003</td><td>Amounts are <code>long</code> minor units (paise)</td></tr>"
    "<tr><td>ADR-005</td><td>Lombok removed, and not to be reintroduced</td></tr>"
    "<tr><td>ADR-007</td><td>Duplicate suppression keys on client reference + value date</td></tr>"
    "<tr><td>ADR-009</td><td>Posting contract changes are versioned and sequenced</td></tr>"
    "</tbody></table>"
    "<p><em>Created by setup-lab-tickets.py for the Module 8 write-back lab. Edit freely.</em></p>"
)


# --------------------------------------------------------------------------- settings and tickets

def load_env():
    """Read .env without any library. Real environment variables win over the file."""
    values = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip().strip('"').strip("'")
    values.update({k: v for k, v in os.environ.items() if k.startswith(("JIRA_", "CONFLUENCE_", "GITHUB_"))})
    # Network settings from .env apply to this script's own requests too.
    for name in ("HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY", "SSL_CERT_FILE"):
        if values.get(name) and name not in os.environ:
            os.environ[name] = values[name]
    return values


def parse(path):
    text = path.read_text(encoding="utf-8")
    heading, rest = text.split("\n", 1)
    key, title = re.match(r"#\s*(\S+)\s+—\s+(.+)", heading).groups()
    meta = META.search(rest)
    parts = COMMENT.split(META.sub("", rest, count=1))
    return {
        "key": key, "title": title,
        "modules": {m.strip() for m in meta.group(1).split(",")},
        "labels": [label.strip() for label in meta.group(2).split(",")],
        "closed": meta.group(3) == "closed-not-planned",
        "body": parts[0].strip(),
        "comments": [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)],
    }


def summary(ticket):
    text = f"[{ticket['key']}] {ticket['title']}"
    # Many Jira projects offer only a "Done" resolution. An agent that reads the status alone would
    # think this change shipped, so the summary says what really happened.
    return text + " (CLOSED - WON'T DO)" if ticket["closed"] else text


def link_text(text, keys, style):
    def replace(match):
        return keys.get(match.group(1), match.group(1))
    return PLACEHOLDER.sub(replace, text)


def to_wiki(markdown):
    """Enough Markdown-to-Jira-wiki conversion for the ticket files. Jira Cloud's v2 API reads it too."""
    out = []
    for line in markdown.splitlines():
        line = re.sub(r"^## (.*)", r"h2. \1", line)
        line = re.sub(r"^(\s*)\d+\. ", lambda m: "#" * (1 + len(m.group(1)) // 3) + " ", line)
        line = re.sub(r"^(\s*)- ", lambda m: "*" * (1 + len(m.group(1)) // 2) + " ", line)
        line = re.sub(r"\*\*(.+?)\*\*", r"*\1*", line)
        line = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"_\1_", line) if line.startswith(">") else line
        line = re.sub(r"`([^`]+)`", r"{{\1}}", line)
        out.append(line)
    return "\n".join(out)


def write_keys(keys, where, env):
    lines = ["# My lab ticket keys", "",
             f"Written by `setup-lab-tickets.py`. Tickets live in: {where}.",
             "When a lab prompt names a lab ticket such as GB-142, use the key on its right.",
             "This file holds no secrets. Copilot may read it; it must never read `.env`.", "",
             f"- Jira project: {env.get('JIRA_PROJECT_KEY', '-')}",
             f"- Confluence space: {env.get('CONFLUENCE_SPACE_KEY', '-')}",
             f"- GitHub repository (fallback only): {env.get('GITHUB_REPO', '-')}", "",
             "| Lab ticket | My key |", "|---|---|"]
    lines += [f"| {lab} | {real} |" for lab, real in sorted(keys.items())]
    KEYS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Keys written to {KEYS_FILE.relative_to(LABS.parent)}")


def read_keys():
    if not KEYS_FILE.exists():
        return {}
    return dict(re.findall(r"^\| ([A-Z]+-\d+|CONFLUENCE-PAGE) \| (\S+) \|$", KEYS_FILE.read_text(encoding="utf-8"), re.M))


# --------------------------------------------------------------------------- Jira and Confluence

class Api:
    """A small JSON REST client. A username means Basic auth (Atlassian Cloud); otherwise a Bearer token
    (Jira and Confluence Data Center personal access tokens, and GitHub tokens)."""

    def __init__(self, base, token, username=None):
        self.base = base.rstrip("/")
        if username:
            self.auth = "Basic " + base64.b64encode(f"{username}:{token}".encode()).decode()
        else:
            self.auth = f"Bearer {token}"
        self.cloud = ".atlassian.net" in self.base

    def call(self, method, path, payload=None, fail_ok=False):
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method, headers={
            "Authorization": self.auth, "Accept": "application/json", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as err:
            message = err.read().decode(errors="replace")[:300]
            if fail_ok:
                return {"_error": f"HTTP {err.code}: {message}"}
            sys.exit(f"{method} {path} failed with HTTP {err.code}:\n{message}")
        except urllib.error.URLError as err:
            sys.exit(f"Cannot reach {self.base}: {err.reason}. Are you on the network that can see it?")


def jira_client(env):
    missing = [name for name in ("JIRA_URL", "JIRA_PROJECT_KEY") if not env.get(name)]
    token = env.get("JIRA_PERSONAL_TOKEN") or env.get("JIRA_API_TOKEN")
    if missing or not token:
        sys.exit("Set JIRA_URL, JIRA_PROJECT_KEY and JIRA_PERSONAL_TOKEN (Data Center) or "
                 "JIRA_USERNAME + JIRA_API_TOKEN (Cloud) in .env. See .env.example.")
    username = None if env.get("JIRA_PERSONAL_TOKEN") else env.get("JIRA_USERNAME")
    return Api(env["JIRA_URL"], token, username)


def jira_find(api, project, ticket):
    jql = f'project = "{project}" AND summary ~ "\\"[{ticket["key"]}]\\""'
    path = "/rest/api/3/search/jql" if api.cloud else "/rest/api/2/search"
    found = api.call("GET", f"{path}?jql={urllib.parse.quote(jql)}&fields=summary&maxResults=5")
    for issue in found.get("issues", []):
        if issue["fields"]["summary"].startswith(f"[{ticket['key']}]"):
            return issue["key"]
    return None


def jira_create(api, project, ticket, keys):
    fields = {"project": {"key": project}, "summary": summary(ticket),
              "description": to_wiki(link_text(ticket["body"], keys, "jira")),
              "issuetype": {"name": ISSUE_TYPES.get(ticket["labels"][0], "Task")},
              "labels": ticket["labels"] + (["wont-do"] if ticket["closed"] else [])}
    created = api.call("POST", "/rest/api/2/issue", {"fields": fields}, fail_ok=True)
    if "_error" in created:  # the project may not have that issue type, or needs an Epic Name
        fields["issuetype"] = {"name": "Task"}
        created = api.call("POST", "/rest/api/2/issue", {"fields": fields})
    return created["key"]


def jira_finish(api, ticket, keys):
    """Everything that needs the other tickets' keys: final description, comments, links, closing."""
    key = keys[ticket["key"]]
    api.call("PUT", f"/rest/api/2/issue/{key}",
             {"fields": {"description": to_wiki(link_text(ticket["body"], keys, "jira"))}}, fail_ok=True)
    for author, text in ticket["comments"]:
        api.call("POST", f"/rest/api/2/issue/{key}/comment",
                 {"body": f"*{author}:*\n{to_wiki(link_text(text, keys, 'jira'))}"}, fail_ok=True)
    blockers = set(BLOCKED_BY.findall(ticket["body"]))
    for other in sorted(set(PLACEHOLDER.findall(ticket["body"])) - {ticket["key"]}):
        if other not in keys:
            continue
        if other in blockers:  # "RISK-402 blocks GB-163"
            link = {"type": {"name": "Blocks"}, "outwardIssue": {"key": keys[other]}, "inwardIssue": {"key": key}}
        else:
            link = {"type": {"name": "Relates"}, "outwardIssue": {"key": key}, "inwardIssue": {"key": keys[other]}}
        result = api.call("POST", "/rest/api/2/issueLink", link, fail_ok=True)
        if "_error" in result and link["type"]["name"] == "Blocks":
            link["type"]["name"] = "Relates"
            result = api.call("POST", "/rest/api/2/issueLink", link, fail_ok=True)
        if "_error" in result:
            print(f"    ! could not link {key} to {keys[other]}. Add the link by hand: the lab needs it.")
    if ticket["closed"]:
        moves = api.call("GET", f"/rest/api/2/issue/{key}/transitions", fail_ok=True).get("transitions", [])
        done = [t for t in moves if t["to"]["name"].lower() in ("done", "closed", "resolved", "won't do")]
        if done:
            api.call("POST", f"/rest/api/2/issue/{key}/transitions", {"transition": {"id": done[0]["id"]}}, fail_ok=True)
        else:
            print(f"    ! could not close {key}. Close it by hand as Won't Do: the lab needs it closed.")


def run_jira(env, tickets, check_only):
    api = jira_client(env)
    project = env["JIRA_PROJECT_KEY"]
    me = api.call("GET", "/rest/api/2/myself")
    api.call("GET", f"/rest/api/2/project/{project}")
    print(f"Jira OK: signed in as {me.get('displayName') or me.get('name')}, project {project}.")
    if check_only:
        write_keys(read_keys(), f"Jira project {project}", env)
        return
    keys = read_keys()
    fresh = []
    for ticket in tickets:
        existing = jira_find(api, project, ticket)
        if existing:
            keys[ticket["key"]] = existing
            print(f"  exists   {ticket['key']:<9} {existing}")
            continue
        keys[ticket["key"]] = jira_create(api, project, ticket, keys)
        fresh.append(ticket)
        print(f"  created  {ticket['key']:<9} {keys[ticket['key']]}")
    for ticket in fresh:
        jira_finish(api, ticket, keys)
    write_keys(keys, f"Jira project {project}", env)


def run_confluence(env, check_only):
    base, space = env.get("CONFLUENCE_URL"), env.get("CONFLUENCE_SPACE_KEY")
    token = env.get("CONFLUENCE_PERSONAL_TOKEN") or env.get("CONFLUENCE_API_TOKEN")
    if not (base and space and token):
        print("Confluence skipped: set CONFLUENCE_URL, CONFLUENCE_SPACE_KEY and a token in .env.")
        return
    username = None if env.get("CONFLUENCE_PERSONAL_TOKEN") else env.get("CONFLUENCE_USERNAME")
    api = Api(base, token, username)
    query = urllib.parse.urlencode({"spaceKey": space, "title": CONFLUENCE_TITLE})
    found = api.call("GET", f"/rest/api/content?{query}")
    print(f"Confluence OK: space {space}.")
    if check_only:
        return
    if found.get("results"):
        page = found["results"][0]["id"]
        print(f"  exists   page {page} '{CONFLUENCE_TITLE}'")
    else:
        page = api.call("POST", "/rest/api/content", {
            "type": "page", "title": CONFLUENCE_TITLE, "space": {"key": space},
            "body": {"storage": {"value": CONFLUENCE_BODY, "representation": "storage"}}})["id"]
        print(f"  created  page {page} '{CONFLUENCE_TITLE}'")
    keys = read_keys()
    keys["CONFLUENCE-PAGE"] = page
    write_keys(keys, "Jira and Confluence", env)


# --------------------------------------------------------------------------- GitHub fallback

def run_github(env, tickets, check_only):
    repo, token = env.get("GITHUB_REPO"), env.get("GITHUB_TOKEN")
    if not (repo and token):
        sys.exit("Set GITHUB_REPO=owner/name and GITHUB_TOKEN in .env. See .env.example.")
    api = Api(env.get("GITHUB_API_URL", "https://api.github.com"), token)
    api.call("GET", f"/repos/{repo}")
    print(f"GitHub OK: {repo}.")
    if check_only:
        return
    keys = read_keys()
    for issue in api.call("GET", f"/repos/{repo}/issues?state=all&per_page=100"):
        match = re.match(r"\[(\S+)\]", issue["title"])
        if match and "pull_request" not in issue:
            keys[match.group(1)] = f"#{issue['number']}"
    for label in sorted({label for t in tickets for label in t["labels"]} | {"wont-do"}):
        api.call("POST", f"/repos/{repo}/labels",
                 {"name": label, "color": LABEL_COLOURS.get(label, "ededed")}, fail_ok=True)  # 422 = exists
    fresh = []
    for ticket in tickets:
        if ticket["key"] in keys:
            print(f"  exists   {ticket['key']:<9} {keys[ticket['key']]}")
            continue
        labels = ticket["labels"] + (["wont-do"] if ticket["closed"] else [])
        issue = api.call("POST", f"/repos/{repo}/issues",
                         {"title": summary(ticket), "body": link_text(ticket["body"], keys, "github"), "labels": labels})
        keys[ticket["key"]] = f"#{issue['number']}"
        fresh.append(ticket)
        print(f"  created  {ticket['key']:<9} {keys[ticket['key']]}")
    for ticket in fresh:
        path = f"/repos/{repo}/issues/{keys[ticket['key']].lstrip('#')}"
        api.call("PATCH", path, {"body": link_text(ticket["body"], keys, "github")})
        for author, text in ticket["comments"]:
            api.call("POST", path + "/comments", {"body": f"**{author}:**\n\n{link_text(text, keys, 'github')}"})
        if ticket["closed"]:
            api.call("PATCH", path, {"state": "closed", "state_reason": "not_planned"})
    write_keys(keys, f"GitHub {repo}", env)


# --------------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--module", help="1-8, capstone, or all")
    parser.add_argument("--target", choices=("jira", "github"), default="jira",
                        help="jira (default) or github (the fallback when Jira is not reachable)")
    parser.add_argument("--check", action="store_true", help="test the settings in .env and create nothing")
    args = parser.parse_args()
    if not (args.check or args.module):
        parser.error("give --module N, or --check")

    env = load_env()
    tickets = [parse(p) for p in sorted(TICKETS.glob("*.md"))]
    wanted = [t for t in tickets if args.module in (None, "all") or args.module in t["modules"]]
    if args.module and not wanted and args.module != "8":
        sys.exit(f"No tickets for module {args.module}. Use 1-8, capstone or all.")

    if args.target == "github":
        run_github(env, wanted, args.check)
    else:
        if wanted or args.check:
            run_jira(env, wanted, args.check)
        if args.check or args.module in ("8", "all"):
            run_confluence(env, args.check)


if __name__ == "__main__":
    main()
