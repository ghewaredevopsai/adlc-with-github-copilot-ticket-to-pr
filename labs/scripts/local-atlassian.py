#!/usr/bin/env python3
"""A local stand-in for Jira and Confluence, for the course labs.

Jira and Confluence are not open source, and Atlassian stopped issuing Data Center trial licences
on 30 March 2026. So this is NOT Jira or Confluence. It is a small server that answers the part of
the Jira and Confluence Data Center REST API that the labs use:

  - the ten mcp-atlassian tools switched on by ENABLED_TOOLS in .env.example
  - labs/scripts/setup-lab-tickets.py (--check, loading tickets, --confluence)

Copilot talks to it through the unchanged "atlassian" MCP server in adlc-labs.code-workspace. Only
the URLs and tokens in .env change. See labs/local-jira-confluence.md.

    python labs/scripts/local-atlassian.py            # Jira at http://127.0.0.1:8990/jira
                                                      # Confluence at http://127.0.0.1:8990/confluence

Python 3 standard library only. Data is one JSON file, by default in
$HOME/adlc-copilot-training/local-atlassian/. It listens on 127.0.0.1 only, and accepts any
non-empty token, so do not expose it to a network.

MIT License. Copyright (c) 2026 Rajesh Gheware.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software, to
deal in it without restriction, including the rights to use, copy, modify, merge, publish,
distribute, sublicense and/or sell copies of it, subject to including this notice. THE SOFTWARE IS
PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""
import argparse
import html
import json
import os
import re
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VERSION = "1.0"
USER = {"name": "participant", "key": "participant", "displayName": "Lab Participant",
        "emailAddress": "participant@localhost", "active": True, "timeZone": "UTC"}
ISSUE_TYPES = {name: str(i) for i, name in enumerate(["Story", "Bug", "Task", "Epic"], start=10001)}
# Won't Do comes before Done, so setup-lab-tickets.py closes the lab's rejected tickets as Won't Do
STATUSES = [("11", "To Do", "new"), ("21", "In Progress", "indeterminate"),
            ("41", "Won't Do", "done"), ("31", "Done", "done")]
LINK_TYPES = {"Blocks": ("is blocked by", "blocks"), "Relates": ("relates to", "relates to")}
LOCK = threading.Lock()


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")


# --------------------------------------------------------------------------- storage

class Store:
    def __init__(self, path, project, space):
        self.path = path
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))
        else:
            self.data = {"next_issue": 1, "next_id": 10001, "next_content": 1001,
                         "issues": {}, "links": [], "content": {}, "spaces": {}, "projects": {}}
        self.ensure_project(project)
        self.ensure_space(space)
        self.save()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=1), encoding="utf-8")
        os.replace(tmp, self.path)

    def new_id(self, counter):
        value = self.data[counter]
        self.data[counter] += 1
        return str(value)

    def ensure_project(self, key):
        if key not in self.data["projects"]:
            self.data["projects"][key] = {"id": self.new_id("next_id"), "key": key,
                                          "name": f"ADLC Workshop - Global Bank ({key})", "next": 1}

    def ensure_space(self, key):
        if key not in self.data["spaces"]:
            home = self.new_id("next_content")
            self.data["spaces"][key] = {"id": self.new_id("next_id"), "key": key,
                                        "name": f"ADLC Workshop - Global Bank ({key})", "homepage": home}
            self.data["content"][home] = {"id": home, "type": "page", "title": f"{key} Home", "space": key,
                                          "parent": None, "body": "<p>Home page of this space.</p>",
                                          "representation": "storage", "version": 1,
                                          "created": now(), "updated": now()}


# --------------------------------------------------------------------------- JQL and CQL

TOKEN = re.compile(r'\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|!=|!~|>=|<=|[=~<>(),]|[^\s=~!<>(),"\']+)')


class Query:
    """A small parser for the JQL and CQL the labs and Copilot send: AND, OR, NOT, brackets,
    = != ~ !~ IN, NOT IN, IS, IS NOT, and ORDER BY. Fields it does not know match everything,
    and are printed to the server log, so a query is never wrongly empty."""

    def __init__(self, text, field_value):
        text = text or ""
        order = re.search(r"\border\s+by\b(.*)$", text, re.I | re.S)
        self.order = []
        if order:
            text = text[:order.start()]
            for part in order.group(1).split(","):
                bits = part.split()
                if bits:
                    self.order.append((bits[0].strip('"').lower(), len(bits) > 1 and bits[1].lower() == "desc"))
        self.tokens = [t for t in TOKEN.findall(text) if t.strip()]
        self.pos = 0
        self.field_value = field_value
        self.tree = self.expr() if self.tokens else None

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        token = self.peek()
        self.pos += 1
        return token

    def word(self, *words):
        token = self.peek()
        return token is not None and token.lower() in words

    def expr(self):
        node = self.term()
        while self.word("or"):
            self.take()
            node = ("or", node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.word("and"):
            self.take()
            node = ("and", node, self.factor())
        return node

    def factor(self):
        if self.word("not"):
            self.take()
            return ("not", self.factor())
        if self.peek() == "(":
            self.take()
            node = self.expr()
            if self.peek() == ")":
                self.take()
            return node
        field = unquote(self.take() or "").lower()
        op = (self.take() or "").lower()
        if op == "not" and self.word("in"):
            self.take()
            op = "not in"
        elif op == "is" and self.word("not"):
            self.take()
            op = "is not"
        return ("clause", field, op, self.value())

    def value(self):
        if self.peek() == "(":
            self.take()
            values = []
            while self.peek() not in (None, ")"):
                token = self.take()
                if token != ",":
                    values.append(unquote(token))
            self.take()
            return values
        token = unquote(self.take() or "")
        if self.peek() == "(":  # a function, such as linkedIssues(GB-1) or currentUser()
            args = self.value()
            return ("fn", token.lower(), args)
        return token

    def matches(self, item, node=None):
        node = self.tree if node is None else node
        if node is None:
            return True
        if node[0] == "and":
            return self.matches(item, node[1]) and self.matches(item, node[2])
        if node[0] == "or":
            return self.matches(item, node[1]) or self.matches(item, node[2])
        if node[0] == "not":
            return not self.matches(item, node[1])
        _, field, op, value = node
        return self.field_value(item, field, op, value)


def unquote(token):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        token = token[1:-1].replace('\\"', '"').replace("\\'", "'")
    return token


def text_match(haystack, needle):
    """Jira-like ~: a quoted phrase must appear as written, otherwise every word must appear."""
    haystack = (haystack or "").lower()
    needle = needle.strip().lower()
    if len(needle) >= 2 and needle[0] == needle[-1] == '"':
        return needle.strip('"') in haystack
    words = re.findall(r"[\w\-\[\]]+", needle.replace("*", ""))
    return all(word in haystack for word in words)


def compare(actual, op, value):
    """= != IN NOT IN IS IS NOT ~ !~ for a single value or a list of values (labels)."""
    actual_list = [a.lower() for a in (actual if isinstance(actual, list) else [actual]) if a is not None]
    wanted = [str(v).lower() for v in (value if isinstance(value, list) else [value])]
    if op in ("is", "is not"):
        empty = not actual_list
        return empty if (op == "is") == (wanted[0] in ("empty", "null")) else not empty
    hit = any(a == w for a in actual_list for w in wanted)
    if op in ("=", "in"):
        return hit
    if op in ("!=", "not in"):
        return not hit
    if op in ("~", "!~"):
        found = any(text_match(a, w) for a in actual_list for w in wanted)
        return found if op == "~" else not found
    return True


# --------------------------------------------------------------------------- Jira

class Jira:
    def __init__(self, store, base):
        self.store = store
        self.base = base

    @property
    def data(self):
        return self.store.data

    def issue_json(self, issue, fields=None):
        status = next(s for s in STATUSES if s[1] == issue["status"])
        project = self.data["projects"][issue["project"]]
        full = {
            "summary": issue["summary"],
            "description": issue["description"],
            "issuetype": {"id": ISSUE_TYPES[issue["issuetype"]], "name": issue["issuetype"],
                          "subtask": False},
            "project": {"id": project["id"], "key": project["key"], "name": project["name"]},
            "status": {"id": status[0], "name": status[1],
                       "statusCategory": {"key": status[2], "name": status[1]}},
            "resolution": {"name": status[1]} if status[2] == "done" else None,
            "labels": issue["labels"],
            "priority": {"name": "Medium", "id": "3"},
            "reporter": USER, "creator": USER, "assignee": None,
            "created": issue["created"], "updated": issue["updated"],
            "comment": {"comments": [self.comment_json(c) for c in issue["comments"]],
                        "total": len(issue["comments"]), "maxResults": len(issue["comments"]), "startAt": 0},
            "issuelinks": self.links_json(issue["key"]),
            "components": [], "fixVersions": [], "attachment": [], "subtasks": [],
        }
        wanted = fields_list(fields)
        if wanted is not None:
            full = {k: v for k, v in full.items() if k in wanted}
        return {"id": issue["id"], "key": issue["key"], "self": f"{self.base}/rest/api/2/issue/{issue['id']}",
                "fields": full}

    def comment_json(self, comment):
        return {"id": comment["id"], "body": comment["body"], "author": USER, "updateAuthor": USER,
                "created": comment["created"], "updated": comment["created"]}

    def links_json(self, key):
        out = []
        for link in self.data["links"]:
            inward, outward = LINK_TYPES[link["type"]]
            kind = {"id": "1000" + str(list(LINK_TYPES).index(link["type"])), "name": link["type"],
                    "inward": inward, "outward": outward}
            if link["from"] == key:    # this issue blocks / relates to the other
                other, side = link["to"], "outwardIssue"
            elif link["to"] == key:    # this issue is blocked by / relates to the other
                other, side = link["from"], "inwardIssue"
            else:
                continue
            target = self.data["issues"].get(other)
            if target:
                out.append({"id": link["id"], "type": kind, side: {
                    "id": target["id"], "key": other,
                    "fields": {"summary": target["summary"], "status": {"name": target["status"]},
                               "issuetype": {"name": target["issuetype"]}}}})
        return out

    def find(self, key_or_id):
        issues = self.data["issues"]
        if key_or_id.upper() in issues:
            return issues[key_or_id.upper()]
        return next((i for i in issues.values() if i["id"] == key_or_id), None)

    def field_value(self, issue, field, op, value):
        if isinstance(value, tuple):  # a function
            _, name, args = value
            if name == "linkedissues" and args:
                keys = {l["from"] if l["to"] == args[0].upper() else l["to"] for l in self.data["links"]
                        if args[0].upper() in (l["from"], l["to"])}
                return (issue["key"] in keys) == (op in ("in", "="))
            return True  # currentUser(), startOfDay() and friends
        comments = " ".join(c["body"] for c in issue["comments"])
        values = {
            "project": [issue["project"], self.data["projects"][issue["project"]]["name"]],
            "key": issue["key"], "issuekey": issue["key"], "id": issue["id"],
            "summary": issue["summary"], "description": issue["description"], "comment": comments,
            "text": " ".join([issue["summary"], issue["description"] or "", comments]),
            "labels": issue["labels"], "status": issue["status"],
            "statuscategory": next(s[2] for s in STATUSES if s[1] == issue["status"]),
            "issuetype": issue["issuetype"], "type": issue["issuetype"],
            "assignee": None, "reporter": USER["name"],
            "resolution": issue["status"] if issue["status"] in ("Done", "Won't Do") else None,
        }
        if field not in values:
            log(f"JQL field '{field}' is not supported, so it matches every issue")
            return True
        if field == "statuscategory" and isinstance(value, str) and value.lower() == "to do":
            value = "new"
        return compare(values[field], op, value)

    def search(self, jql, start, limit, fields):
        query = Query(jql, self.field_value)
        hits = [i for i in self.data["issues"].values() if query.matches(i)]
        order = query.order or [("created", True)]
        for field, desc in reversed(order):
            if field in ("key", "issuekey", "id"):
                hits.sort(key=lambda i: int(i["id"]), reverse=desc)
            else:  # ties, such as tickets loaded in the same second, fall back to creation order
                hits.sort(key=lambda i: (str(i.get(field, i["created"]) or ""), int(i["id"])), reverse=desc)
        page = hits[start:start + limit]
        return {"startAt": start, "maxResults": limit, "total": len(hits),
                "issues": [self.issue_json(i, fields) for i in page]}

    def handle(self, method, path, query, body):
        m = re.fullmatch(r"/rest/api/(?:2|latest)(/.*)", path)
        if not m:
            return 404, {"errorMessages": [f"Not supported by the local stand-in: {method} {path}"]}
        route = m.group(1).rstrip("/")
        data = self.data
        if route == "/myself" or route == "/user":
            return 200, USER
        if route == "/serverInfo":
            return 200, {"baseUrl": self.base, "version": "9.12.0", "versionNumbers": [9, 12, 0],
                         "deploymentType": "Server", "serverTitle": "Local Jira stand-in"}
        if route == "/project":
            return 200, [self.project_json(p) for p in data["projects"].values()]
        if m2 := re.fullmatch(r"/project/([^/]+)", route):
            project = data["projects"].get(m2.group(1).upper())
            return (200, self.project_json(project)) if project else \
                (404, {"errorMessages": [f"No project could be found with key '{m2.group(1)}'."]})
        if route == "/field":
            return 200, [{"id": f, "key": f, "name": f.capitalize(), "custom": False, "navigable": True,
                          "searchable": True, "schema": {"type": "string", "system": f}}
                         for f in ("summary", "description", "issuetype", "project", "status", "labels",
                                   "priority", "reporter", "assignee", "created", "updated", "comment",
                                   "issuelinks", "resolution")]
        if route == "/issueLinkType":
            return 200, {"issueLinkTypes": [{"id": "1000" + str(n), "name": k, "inward": v[0], "outward": v[1]}
                                            for n, (k, v) in enumerate(LINK_TYPES.items())]}
        if route == "/search":
            params = body if method == "POST" else {k: v[0] for k, v in query.items()}
            fields = params.get("fields")
            return 200, self.search(params.get("jql", ""), int(params.get("startAt", 0) or 0),
                                    int(params.get("maxResults", 50) or 50), fields)
        if route == "/issue" and method == "POST":
            return self.create(body.get("fields", {}))
        if route == "/issueLink" and method == "POST":
            return self.link(body)
        m2 = re.fullmatch(r"/issue/([^/]+)(/[a-z]+)?", route)
        if not m2:
            return 404, {"errorMessages": [f"Not supported by the local stand-in: {method} {path}"]}
        issue = self.find(m2.group(1))
        if not issue:
            return 404, {"errorMessages": ["Issue Does Not Exist"]}
        tail = m2.group(2)
        if tail is None and method == "GET":
            return 200, self.issue_json(issue, query.get("fields", [None])[0])
        if tail is None and method == "PUT":
            fields = body.get("fields", {})
            for name in ("summary", "description", "labels"):
                if name in fields:
                    issue[name] = fields[name]
            issue["updated"] = now()
            return 204, None
        if tail == "/comment" and method == "GET":
            comments = [self.comment_json(c) for c in issue["comments"]]
            return 200, {"comments": comments, "total": len(comments), "maxResults": len(comments), "startAt": 0}
        if tail == "/comment" and method == "POST":
            comment = {"id": self.store.new_id("next_id"), "body": body.get("body", ""), "created": now()}
            issue["comments"].append(comment)
            issue["updated"] = now()
            return 201, self.comment_json(comment)
        if tail == "/transitions" and method == "GET":
            return 200, {"transitions": [{"id": s[0], "name": s[1], "to": {"name": s[1]}}
                                         for s in STATUSES if s[1] != issue["status"]]}
        if tail == "/transitions" and method == "POST":
            wanted = str(body.get("transition", {}).get("id"))
            status = next((s for s in STATUSES if s[0] == wanted), None)
            if not status:
                return 400, {"errorMessages": [f"Transition id '{wanted}' is not valid for this issue."]}
            issue["status"] = status[1]
            issue["updated"] = now()
            return 204, None
        if tail in ("/remotelink", "/watchers", "/worklog", "/properties"):
            return 200, [] if tail == "/remotelink" else {}
        return 404, {"errorMessages": [f"Not supported by the local stand-in: {method} {path}"]}

    def project_json(self, project):
        return {"id": project["id"], "key": project["key"], "name": project["name"],
                "projectTypeKey": "software", "lead": USER,
                "issueTypes": [{"id": v, "name": k, "subtask": False} for k, v in ISSUE_TYPES.items()]}

    def create(self, fields):
        key = (fields.get("project") or {}).get("key", "")
        project = self.data["projects"].get(key.upper())
        kind = (fields.get("issuetype") or {}).get("name")
        errors = {}
        if not project:
            errors["project"] = f"Project '{key}' does not exist. This server has: {', '.join(self.data['projects'])}"
        if kind not in ISSUE_TYPES:
            errors["issuetype"] = f"Issue type must be one of {', '.join(ISSUE_TYPES)}"
        if not fields.get("summary"):
            errors["summary"] = "You must specify a summary of the issue."
        if errors:
            return 400, {"errorMessages": [], "errors": errors}
        issue_key = f"{project['key']}-{project['next']}"
        project["next"] += 1
        issue = {"id": self.store.new_id("next_id"), "key": issue_key, "project": project["key"],
                 "summary": fields["summary"], "description": fields.get("description") or "",
                 "issuetype": kind, "labels": fields.get("labels") or [], "status": "To Do",
                 "comments": [], "created": now(), "updated": now()}
        self.data["issues"][issue_key] = issue
        return 201, {"id": issue["id"], "key": issue_key, "self": f"{self.base}/rest/api/2/issue/{issue['id']}"}

    def link(self, body):
        kind = (body.get("type") or {}).get("name")
        source = self.find((body.get("outwardIssue") or {}).get("key", ""))
        target = self.find((body.get("inwardIssue") or {}).get("key", ""))
        if kind not in LINK_TYPES or not source or not target:
            return 400, {"errorMessages": [f"Link type must be one of {', '.join(LINK_TYPES)}, between two existing issues."]}
        # outwardIssue blocks inwardIssue, as setup-lab-tickets.py writes "RISK-402 blocks GB-163".
        # A link that already exists is not added twice; Relates counts in both directions.
        pair = (source["key"], target["key"])
        for existing in self.data["links"]:
            if existing["type"] == kind and ((existing["from"], existing["to"]) == pair or
                                             (kind == "Relates" and (existing["to"], existing["from"]) == pair)):
                return 201, None
        self.data["links"].append({"id": self.store.new_id("next_id"), "type": kind,
                                   "from": source["key"], "to": target["key"]})
        return 201, None


def fields_list(fields):
    if fields is None:
        return None
    if isinstance(fields, str):
        fields = fields.split(",")
    fields = [f.strip() for f in fields if f.strip()]
    if not fields or "*all" in fields or "*navigable" in fields:
        return None
    return set(fields)


# --------------------------------------------------------------------------- Confluence

class Confluence:
    def __init__(self, store, base):
        self.store = store
        self.base = base

    @property
    def data(self):
        return self.store.data

    def content_json(self, page, expand=""):
        space = self.data["spaces"][page["space"]]
        out = {
            "id": page["id"], "type": page["type"], "status": "current", "title": page["title"],
            "space": {"id": space["id"], "key": space["key"], "name": space["name"], "type": "global",
                      "_links": {"self": f"{self.base}/rest/api/space/{space['key']}"}},
            "version": {"number": page["version"], "when": page["updated"], "by": self.user(),
                        "message": ""},
            "history": {"latest": True, "createdBy": self.user(), "createdDate": page["created"],
                        "lastUpdated": {"by": self.user(), "when": page["updated"], "number": page["version"]}},
            "body": {rep: {"value": page["body"], "representation": rep} for rep in ("storage", "view")},
            "ancestors": [{"id": a["id"], "type": "page", "title": a["title"]} for a in self.ancestors(page)],
            "metadata": {"labels": {"results": [], "size": 0}},
            "children": {"page": {"results": [], "size": 0}, "attachment": {"results": [], "size": 0},
                         "comment": {"results": [], "size": 0}},
            "_links": {"webui": f"/pages/viewpage.action?pageId={page['id']}", "base": self.base,
                       "self": f"{self.base}/rest/api/content/{page['id']}", "tinyui": f"/x/{page['id']}"},
        }
        if page["type"] == "comment":
            parent = self.data["content"].get(page["parent"])
            out["container"] = {"id": page["parent"], "type": "page", "title": parent and parent["title"]}
        if "body" not in expand and expand:
            out.pop("body")
        return out

    def user(self):
        return {"type": "known", "username": USER["name"], "userKey": USER["key"],
                "displayName": USER["displayName"]}

    def ancestors(self, page):
        chain = []
        parent = page.get("parent")
        while parent and parent in self.data["content"]:
            node = self.data["content"][parent]
            chain.insert(0, node)
            parent = node.get("parent")
        return chain

    def field_value(self, page, field, op, value):
        if isinstance(value, tuple):
            return True
        text = re.sub(r"<[^>]+>", " ", page["body"])
        values = {
            "type": page["type"], "space": page["space"], "space.key": page["space"],
            "title": page["title"], "text": page["title"] + " " + text,
            "sitesearch": page["title"] + " " + text, "id": page["id"], "content": page["id"],
            "parent": page.get("parent"),
            "ancestor": [a["id"] for a in self.ancestors(page)],
            "label": [], "creator": USER["name"], "contributor": USER["name"],
        }
        if field in ("created", "lastmodified"):
            return True
        if field not in values:
            log(f"CQL field '{field}' is not supported, so it matches every page")
            return True
        return compare(values[field], op, value)

    def search(self, cql, start, limit):
        query = Query(cql, self.field_value)
        hits = [p for p in self.data["content"].values() if query.matches(p)]
        hits.sort(key=lambda p: p["updated"], reverse=True)
        return hits[start:start + limit], len(hits)

    def listing(self, items, start, limit, total, expand, wrap=False):
        results = []
        for page in items:
            content = self.content_json(page, expand.replace("content.", ""))
            if wrap:
                text = re.sub(r"<[^>]+>", " ", page["body"])
                results.append({"content": content, "title": page["title"], "excerpt": " ".join(text.split())[:200],
                                "url": content["_links"]["webui"], "entityType": "content",
                                "lastModified": page["updated"],
                                "resultGlobalContainer": {"title": content["space"]["name"],
                                                          "displayUrl": f"/display/{page['space']}"}})
            else:
                results.append(content)
        return {"results": results, "start": start, "limit": limit, "size": len(results),
                "totalSize": total, "_links": {"base": self.base, "context": ""}}

    def handle(self, method, path, query, body):
        q = {k: v[0] for k, v in query.items()}
        start, limit = int(q.get("start", 0) or 0), int(q.get("limit", 25) or 25)
        expand = q.get("expand", "")
        content = self.data["content"]
        m = re.fullmatch(r"/rest/api(/.*)", path)
        if not m:
            return 404, {"message": f"Not supported by the local stand-in: {method} {path}"}
        route = m.group(1).rstrip("/")
        if route == "/user/current":
            return 200, self.user()
        if route == "/space":
            return 200, {"results": [self.space_json(s) for s in self.data["spaces"].values()],
                         "start": 0, "limit": 25, "size": len(self.data["spaces"])}
        if m2 := re.fullmatch(r"/space/([^/]+)", route):
            space = self.data["spaces"].get(m2.group(1))
            return (200, self.space_json(space)) if space else \
                (404, {"message": f"No space with key : {m2.group(1)}"})
        if route in ("/search", "/content/search"):
            hits, total = self.search(q.get("cql", ""), start, limit)
            return 200, self.listing(hits, start, limit, total, expand, wrap=route == "/search")
        if route == "/content" and method == "GET":
            hits = [p for p in content.values()
                    if p["type"] == q.get("type", "page")
                    and ("spaceKey" not in q or p["space"] == q["spaceKey"])
                    and ("title" not in q or p["title"] == q["title"])]
            return 200, self.listing(hits[start:start + limit], start, limit, len(hits), expand)
        if route == "/content" and method == "POST":
            return self.create(body)
        m2 = re.fullmatch(r"/content/(\d+)(/.*)?", route)
        if not m2 or m2.group(1) not in content:
            return 404, {"statusCode": 404, "message": f"No content found with id: {m2 and m2.group(1)}"}
        page, tail = content[m2.group(1)], m2.group(2)
        if tail is None and method == "GET":
            return 200, self.content_json(page, expand or "body")
        if tail is None and method == "PUT":
            return self.update(page, body)
        if tail in ("/child/page", "/child/comment", "/descendant/page", "/descendant/comment"):
            kind = tail.rsplit("/", 1)[1]
            if tail.startswith("/child"):
                hits = [p for p in content.values() if p["type"] == kind and p.get("parent") == page["id"]]
            else:
                hits = [p for p in content.values() if p["type"] == kind and page in self.ancestors(p)]
            hits.sort(key=lambda p: int(p["id"]))
            return 200, self.listing(hits[start:start + limit], start, limit, len(hits), expand)
        if tail and (tail.startswith("/child") or tail in ("/label", "/property", "/restriction")):
            return 200, {"results": [], "start": 0, "limit": limit, "size": 0}
        if tail == "/history":
            return 200, self.content_json(page, expand)["history"]
        return 404, {"message": f"Not supported by the local stand-in: {method} {path}"}

    def space_json(self, space):
        home = self.data["content"][space["homepage"]]
        return {"id": space["id"], "key": space["key"], "name": space["name"], "type": "global",
                "homepage": {"id": home["id"], "type": "page", "title": home["title"]},
                "_links": {"webui": f"/display/{space['key']}", "base": self.base}}

    def storage(self, body):
        body = body.get("body") or {}
        for rep in ("storage", "wiki", "editor", "view"):
            if rep in body:
                return body[rep].get("value", ""), rep
        return "", "storage"

    def create(self, body):
        kind = body.get("type", "page")
        content = self.data["content"]
        if kind == "comment":
            parent = str((body.get("container") or {}).get("id", ""))
            if parent not in content:
                return 400, {"message": "A comment needs a container page that exists."}
            space = content[parent]["space"]
            title = "Re: " + content[parent]["title"]
        else:
            space = (body.get("space") or {}).get("key", "")
            if space not in self.data["spaces"]:
                return 400, {"message": f"Space '{space}' does not exist. This server has: "
                                        f"{', '.join(self.data['spaces'])}"}
            title = body.get("title", "").strip()
            if not title:
                return 400, {"message": "A page needs a title."}
            if any(p["title"] == title and p["space"] == space and p["type"] == "page" for p in content.values()):
                return 400, {"statusCode": 400, "message":
                             f"A page with this title already exists: A page already exists with the title "
                             f"{title} in the space with key {space}"}
            ancestors = body.get("ancestors") or []
            parent = str(ancestors[-1]["id"]) if ancestors else self.data["spaces"][space]["homepage"]
            if parent not in content:
                return 400, {"message": f"Parent page {parent} does not exist."}
        value, rep = self.storage(body)
        page_id = self.store.new_id("next_content")
        content[page_id] = {"id": page_id, "type": kind, "title": title, "space": space, "parent": parent,
                            "body": value, "representation": rep, "version": 1,
                            "created": now(), "updated": now()}
        return 200, self.content_json(content[page_id], "body")

    def update(self, page, body):
        version = (body.get("version") or {}).get("number")
        if version is not None and int(version) != page["version"] + 1:
            return 409, {"statusCode": 409, "message":
                         f"Version must be incremented on update. Current version is: {page['version']}"}
        if body.get("title"):
            page["title"] = body["title"]
        if body.get("body"):
            page["body"], page["representation"] = self.storage(body)
        ancestors = body.get("ancestors") or []
        if ancestors and str(ancestors[-1]["id"]) in self.data["content"]:
            page["parent"] = str(ancestors[-1]["id"])
        page["version"] += 1
        page["updated"] = now()
        return 200, self.content_json(page, "body")


# --------------------------------------------------------------------------- pages for the browser

def page_html(title, inner):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:24px auto;padding:0 16px;color:#172b4d}}
a{{color:#0052cc}}pre{{white-space:pre-wrap;background:#f4f5f7;padding:12px;border-radius:4px}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #dfe1e6;padding:6px;text-align:left}}
.note{{color:#6b778c;font-size:13px}}</style></head><body>
<p class="note">Local stand-in for Jira and Confluence, for the course labs. Not an Atlassian product.
<a href="/jira/">Issues</a> · <a href="/confluence/">Pages</a></p>{inner}</body></html>"""


def browse(store, path, query):
    data = store.data
    e = html.escape
    if path in ("/", "/jira", "/jira/"):
        rows = "".join(f"<tr><td><a href='/jira/browse/{e(k)}'>{e(k)}</a></td><td>{e(i['issuetype'])}</td>"
                       f"<td>{e(i['status'])}</td><td>{e(i['summary'])}</td></tr>"
                       for k, i in sorted(data["issues"].items(), key=lambda kv: int(kv[1]["id"])))
        return page_html("Issues", f"<h1>Issues</h1><table><tr><th>Key</th><th>Type</th><th>Status</th>"
                                   f"<th>Summary</th></tr>{rows}</table>")
    if m := re.fullmatch(r"/jira/browse/([A-Za-z0-9]+-\d+)", path):
        issue = data["issues"].get(m.group(1).upper())
        if not issue:
            return None
        links = "".join(f"<li>{e(l['type'])}: <a href='/jira/browse/{e(o)}'>{e(o)}</a></li>"
                        for l in data["links"] for o in [l["to"] if l["from"] == issue["key"] else l["from"]]
                        if issue["key"] in (l["from"], l["to"]))
        comments = "".join(f"<pre>{e(c['body'])}</pre>" for c in issue["comments"])
        return page_html(issue["key"], f"<h1>{e(issue['key'])}: {e(issue['summary'])}</h1>"
                         f"<p>{e(issue['issuetype'])} · {e(issue['status'])} · labels: {e(', '.join(issue['labels']))}</p>"
                         f"<h2>Description</h2><pre>{e(issue['description'])}</pre>"
                         f"<h2>Links</h2><ul>{links}</ul><h2>Comments</h2>{comments}")
    if path in ("/confluence", "/confluence/"):
        def tree(parent):
            kids = sorted((p for p in data["content"].values() if p["type"] == "page" and p.get("parent") == parent),
                          key=lambda p: int(p["id"]))
            return "<ul>" + "".join(f"<li><a href='/confluence/pages/viewpage.action?pageId={p['id']}'>"
                                    f"{e(p['title'])}</a> <span class='note'>id {p['id']}</span>{tree(p['id'])}</li>"
                                    for p in kids) + "</ul>" if kids else ""
        return page_html("Pages", "<h1>Pages</h1>" + tree(None))
    if path == "/confluence/pages/viewpage.action":
        page = data["content"].get(query.get("pageId", [""])[0])
        if not page:
            return None
        comments = "".join(f"<div class='note'>Comment</div>{c['body']}" for c in data["content"].values()
                           if c["type"] == "comment" and c["parent"] == page["id"])
        # Page bodies are Confluence storage format (HTML) written by you or Copilot on your own machine.
        return page_html(page["title"], f"<h1>{e(page['title'])}</h1><p class='note'>Space {e(page['space'])} · "
                         f"version {page['version']}</p>{page['body']}<hr>{comments}")
    return None


# --------------------------------------------------------------------------- HTTP

def log(message):
    print(f"[{datetime.now():%H:%M:%S}] {message}", file=sys.stderr, flush=True)


class Handler(BaseHTTPRequestHandler):
    store = jira = confluence = None

    def log_message(self, fmt, *args):
        log(fmt % args)

    def reply(self, status, payload, content_type="application/json"):
        raw = b"" if payload is None else (payload if isinstance(payload, bytes) else json.dumps(payload).encode())
        self.send_response(status)
        if raw:
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def route(self, method):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if method == "GET" and "/rest/" not in url.path:
            page = browse(self.store, url.path, query)
            return self.reply(200, page.encode(), "text/html") if page else self.reply(404, b"Not found", "text/plain")
        if not (self.headers.get("Authorization") or "").split(" ", 1)[-1].strip():
            return self.reply(401, {"message": "Send a token: set JIRA_PERSONAL_TOKEN and "
                                               "CONFLUENCE_PERSONAL_TOKEN in .env (any value works here)."})
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return self.reply(400, {"message": "The request body is not valid JSON."})
        for prefix, app in (("/jira", self.jira), ("/confluence", self.confluence)):
            if url.path == prefix or url.path.startswith(prefix + "/"):
                with LOCK:
                    status, payload = app.handle(method, url.path[len(prefix):], query, body)
                    if method != "GET" and status < 300:
                        self.store.save()
                if status == 404:
                    log(f"404 {method} {self.path}")
                return self.reply(status, payload)
        return self.reply(404, {"message": "Use /jira or /confluence."})

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")

    def do_PUT(self):
        self.route("PUT")

    def do_DELETE(self):
        self.reply(403, {"message": "The labs never delete. This stand-in does not either."})


def main():
    parser = argparse.ArgumentParser(description="Local stand-in for Jira and Confluence, for the course labs.")
    parser.add_argument("--port", type=int, default=8990)
    parser.add_argument("--project", default="ADLC", help="Jira project key to create (default ADLC)")
    parser.add_argument("--space", default="ADLC", help="Confluence space key to create (default ADLC)")
    parser.add_argument("--data-dir", default=str(Path.home() / "adlc-copilot-training" / "local-atlassian"),
                        help="where data.json is kept")
    args = parser.parse_args()
    store = Store(Path(args.data_dir) / "data.json", args.project.upper(), args.space.upper())
    base = f"http://127.0.0.1:{args.port}"
    Handler.store = store
    Handler.jira = Jira(store, base + "/jira")
    Handler.confluence = Confluence(store, base + "/confluence")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Local Jira and Confluence stand-in {VERSION}\n"
          f"  JIRA_URL={base}/jira          project {args.project.upper()}\n"
          f"  CONFLUENCE_URL={base}/confluence  space {args.space.upper()}\n"
          f"  data: {store.path}\n"
          f"Leave this terminal open. Ctrl+C stops the server; your data stays.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
