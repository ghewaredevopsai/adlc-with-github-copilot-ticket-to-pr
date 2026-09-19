# Agentic ADLC with GitHub Copilot

*From JIRA Ticket to Merged PR — Knowledge, Specialised Agents & Spec-Driven Delivery*
2 days · Advanced · 8 modules · 14 labs + capstone · 40% theory / 60% demo + hands-on

This repository holds the course outline, the eight module decks and the lab guides. The outline and
decks open straight from the filesystem: no build step, no install, no network needed.

## Start here

Open **`course-outline-agentic-adlc-github-copilot.html`** in a browser. Each module heading links to
its deck, and every deck links back to the outline.

```
course-outline-agentic-adlc-github-copilot.html   the two-day outline (PDF copy beside it)
presentation/
  module-1-adlc-token-economics.html                the ADLC operating model and token economics
  module-2-knowledge-harnessing.html                instruction files, ADRs and knowledge in the repo
  module-3-prompt-context-engineering.html          prompts, skill files and grounding
  module-4-specialised-agents.html                  agents for specific tasks and their hand-offs
  module-5-spec-driven-development.html             spec, plan, tasks, with gates between them
  module-6-ticket-as-unit-of-work.html              the JIRA ticket as the unit of work, over MCP
  module-7-multi-repo-engineering.html              changes that cross repositories
  module-8-closing-the-loop.html                    review, pull requests and documentation
labs/
  README.md                                         how the labs work, and one-time setup
  mcp-setup.md                                      connect Copilot to your Jira and Confluence
  confluence-setup.md                               create the Confluence pages the labs write under
  module-1-labs.md … module-8-labs.md               one lab guide per module
  tickets/                                          the lab tickets, loaded into your own Jira
  scripts/                                          setup-lab-tickets.py (you run it), and deck checks
adlc-labs.code-workspace                            the VS Code workspace every lab uses
```

The course works on **Global Bank**, a set of Spring Boot services on JDK 25, and a small weather app
used to demonstrate the Jira → agent → pull request flow. Your trainer gives you a machine setup check
before Day 1. Before Day 1, also do the one-time setup in [labs/README.md](labs/README.md).

## The code you work on

All repositories are public. You clone them; you do not fork them. [participants-instructions.md](participants-instructions.md) walks you through it.

| Repository | What it is |
|---|---|
| [global-bank-platform](https://github.com/brainupgrade-in/global-bank-platform) | Start here: the map of all services, and scripts that run the whole app on your machine |
| [global-bank-account](https://github.com/brainupgrade-in/global-bank-account) | Accounts and balances (Spring Boot) |
| [global-bank-transaction](https://github.com/brainupgrade-in/global-bank-transaction) | Deposits, withdrawals and transaction history (Spring Boot) |
| [global-bank-customer](https://github.com/brainupgrade-in/global-bank-customer) | Customer records (Spring Boot) |
| [global-bank-authentication](https://github.com/brainupgrade-in/global-bank-authentication) | Sign-in and tokens (Spring Boot) |
| [global-bank-rules](https://github.com/brainupgrade-in/global-bank-rules) | Minimum-balance and service-charge rules (Spring Boot) |
| [global-bank-frontend](https://github.com/brainupgrade-in/global-bank-frontend) | The web app (React + Vite) |

The trainer also runs a demo on a separate repository,
[weather-app](https://github.com/brainupgrade-in/weather-app): a Jira ticket starts an agent, and the
agent opens a pull request. You watch this demo. You do not clone weather-app.

## Using the decks

| Key | Does |
|---|---|
| `←` `→` | previous / next slide |
| `O` | slide index |
| `N` | speaker notes, the argument behind each slide |
| `F` | fullscreen |
| `Home` / `End` | first / last slide |
| `k` / `Shift+K` | jump along the key path: the slides taught live |
| `L` | show the slides held back until after their lab |

Deep links work: `module-2-knowledge-harnessing.html#12` opens slide 12.

Every slide is tagged **K** (taught live), **D** (demo: the trainer leaves the deck and shows the real
thing) or **R** (reference, for reading afterwards). Some slides carry an **AFTER LAB** chip: they hold
the answer to a lab, so **read them after you have done that lab**, not before. The labs measure what
changes when you work differently, and knowing the answer in advance leaves nothing to measure.

## The worked examples

The decks show complete files as worked examples: `copilot-instructions.md`, path-scoped instruction
files, an ADR, a skill file, agent definitions, a contract document and several tickets (`GB-142`,
`GB-147`, `GB-151`, `GB-158`, `GB-163`, `GB-207`, and the capstone `GB-186`). They are written for the
Global Bank services and are the kind of file you write in the labs.
