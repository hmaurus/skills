# aicf — project governance for building with agents

_[Versão em português](README.md)_

Twenty well-written specs do not tell you where the project stands.

Engineering skill collections handle one work item at a time, and handle it well: they interrogate the idea, write the spec, break it into tasks, execute with discipline. They start from a request that is already bounded and stop at the commit. What falls outside is the level above — the document stating what you are building and for whom, the place where a raw idea waits its turn, and the record of what actually shipped.

`aicf` is that layer. It sets up the project's documents and takes each work item from the idea to the report of what was done. It works on its own, and it works on top of the collections you already use.

> **Written in Portuguese.** The skills instruct the agent in pt-BR and the file conventions mix the playbook's terms with Portuguese names (`intents/` and `specs/` for the two states of a work item, `backlog/`, `concluidas/` for completed). The GitHub labels of the issue mode are the same words: `aicf:backlog`, `aicf:intent`, `aicf:spec`. They work fine in an English-speaking session — Claude reads the instructions and answers you in whatever language you write — but if you want the artifacts named in English, fork and translate.

## Install

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Restart your session afterwards — skills load at startup and do not hot-swap.

On a new project, start with `/aicf:setup`. On an existing one, start with `/aicf:workflow-demanda`, which explains the cycle.

## The cycle

Every work item goes through the same four phases.

```mermaid
flowchart LR
  D[Work item<br/>what you want, still raw]
  E[Interview<br/>produces the spec]
  I[Implementation<br/>consumes the spec]
  F[Closing<br/>report of what shipped]
  D --> E --> I --> F
  F -.-> D
```

- **Work item** — the idea recorded, even before it is mature.
- **Interview** — questions until no decision is left open. A spec comes out.
- **Implementation** — someone executes the spec, by any path.
- **Closing** — the report of what was actually done, including what came out different from the plan.

Each work item is a versioned file in the repository, or a GitHub issue. You pick which one at setup.

## The problem this solves

### The conversation disappears with /clear

You spent half an hour with the agent deciding not to take a certain approach. You ran `/clear`. Three weeks later someone reopens the same argument, because the reason was never written down anywhere.

In `aicf` the decision and the reason live in the work item, inside the repository. `/aicf:criar-spec` runs the interview and records all of it, including what was decided **against**.

### Nobody knows where the project stands

Specs tell each change, one by one. None of them says what the product is, who it serves, and what was ruled out by decision.

`/aicf:criar-prd` interviews you and writes `PRD.md`. The section that pays off most is "ruled out, by decision": it is what keeps the same argument from coming back six months later.

### What actually shipped never gets written

A spec and a plan say what was intended, and they were written before execution. What changed along the way only exists if someone writes it at the end.

`/aicf:fechar-demanda` asks for that report and keeps it with the work item. The agent applies closing on any implementation path, including the ones that are not `aicf`'s.

## Starting a new project

**1. `/aicf:setup`.** Sets up the base: `PRD.md`, the place where work items will live, and the root `CLAUDE.md`, the file the agent reads at the start of every session. It asks little — the name, a sentence or two about the project, whether a work item lives in a file or an issue, where the engineering defaults live, and which tools you already use.

**2. Fill in `PRD.md`.** It ships with the sections and a prompt under each. `/aicf:criar-prd` interviews you section by section and writes the file, starting from the problem rather than the solution.

<details>
<summary>Why the PRD does not go through the work item cycle</summary>

Not because it is a document — a spec works fine for a documentation change. It is that a spec describes a **change**, with a scope and a "done" state, while the PRD describes the **product**, and gets revised every time a decision contradicts it. Wrapping one in the other yields an empty spec: its interview would discuss how to write the file, and the questions that matter — audience, what is ruled out — would stay unanswered. Plus a closing asking for a report, archiving and a lint check on a `.md`.

</details>

**3. List what the product needs to have.** Each item becomes a roadmap line, or a backlog issue. Anything that needs context gets its own record right away, and the line goes away — what has a file has no line, and no index is left to grow stale.

**4. First work item.** `/aicf:criar-spec` to mature it, `/aicf:implementar-spec` to execute and close. From there the cycle repeats.

The interview and implementation phases accept paths from outside `aicf`, if you already use other skill collections. Governance does not change, and the work item notes which path was used.

## The skills

There are six, and the axis that matters is who can invoke each one.

**You type them.** They only exist when you call them, and they drive a whole session.

| Skill | When | What it does |
| --- | --- | --- |
| `/aicf:setup` | once, on a new project | Asks whether work items live in files or issues and sets up whatever the answer requires: `docs/projeto/` with the PRD, roadmap and work item folders, or the three `aicf:*` labels. In both cases, `CLAUDE.md` (with `AGENTS.md` pointing to it), a `README.md` and, if you want, the engineering defaults |
| `/aicf:criar-prd` | start of the project | Interviews you about the product and writes `PRD.md`. Run it again whenever a decision contradicts it |

**You type them, or the agent reaches for them.** They answer a request in plain language — "interview me about X", "implement spec Y" — and the agent loads them when it recognizes the intent.

| Skill | When | What it does |
| --- | --- | --- |
| `/aicf:workflow-demanda` | the map | The cycle, the paths for each phase, and the governance conventions |
| `/aicf:criar-spec` | interview phase | Interrogates until no decision is left open, then writes the spec, with a suggested implementation path. `/aicf:criar-spec #12` adopts an issue that already exists |
| `/aicf:implementar-spec` | implementation phase | Picks the path from the spec's suggestion, implements and verifies. At the end it calls closing |
| `/aicf:fechar-demanda` | closing phase | Checks, report, archiving and knowledge promotion, on any implementation path |

The skills are deliberately small: they say what the agent could not infer — where to write, what to record, when to close — and stop there. What the tool already does well, and what is better decided case by case, stays with the agent.

<details>
<summary><strong>Where things live</strong> — the folder structure, or the labels</summary>

In file mode, the folder tells the document's maturity:

```
docs/projeto/
├── PRD.md             # why the product exists: vision, audience, model
├── ROADMAP.md         # what has no file yet: Próximas and Backlog
├── backlog/           # not yet clear it will be done
├── intents/           # decided, not yet interviewed
├── specs/             # ready to implement
└── concluidas/        # archived, with a report
```

A work item is the unit of work. The file describing it is born as an **intent**, becomes a **spec** once it is ready to implement — the same file, moved — and ends in `concluidas/` with the report. The four folders sit at the same level, so moving the file does not break the relative links that point out of it.

**In issue mode**, maturity lives in a label (`aicf:backlog`, `aicf:intent`, `aicf:spec`), a work item is a single issue from birth to closing — the label changes, the number does not — and completed means the issue is closed, with the report in a comment. Then `docs/projeto/` holds only `PRD.md`. The PRD, ADRs and the glossary stay in files in both modes.

You switch by editing one line of `CLAUDE.md`, and a missing line means files, so a project created before this option keeps working untouched. The choice applies from that point on: there is no migration, what is already in files stays where it is, and new work items are born in the new medium.

Each one buys you something different. Files: zero setup, survives `git clone` with no network, shows up in the repository's `grep`, no vendor dependency. Issues: conversation with comments and notifications, outside contribution in two clicks, a stable `#12` reference, and `Fixes #12` closing on merge. The default is files because that is what works with no `gh`, no login and no remote.

If your project needs a different structure, write the difference in the root `CLAUDE.md` or in `.claude/rules/`, never in a `CLAUDE.md` inside `docs/projeto/`: a subfolder `CLAUDE.md` only enters context when the agent reads a file from that folder, and recording a new work item does not require that.

</details>

<details>
<summary><strong>Neighbouring commands worth knowing</strong> — and what each one is for</summary>

None of these ship with `aicf`. They belong to the [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock](https://github.com/mattpocock/skills) collections, and they apply if you already have them installed.

**Before writing the work item**

- `grill-me` and `grill-with-docs` (Matt) — challenge the idea before you write it down, with questions until every branch of the decision is resolved. Use them when you already think you know what you want. They record nothing; the result feeds the interview.
- `wayfinder` (Matt) — maps a request too big for one session as decision tickets on your tracker, and resolves them one at a time. Use it when the way to the result is not visible yet. The map belongs to that effort.
- `domain-modeling` (Matt) — records the project's vocabulary in a `CONTEXT.md`, if the product has terms of its own that have already turned out ambiguous.

**In the interview phase, instead of `/aicf:criar-spec`**

- `brainstorming` (Superpowers) — interviews you and, on the _architectural_ path, writes a design doc that counts as a spec.
- `grill-with-docs` + `to-spec` (Matt) — the same thing in two steps, ending with the spec published to the tracker.

**In the implementation phase, instead of `/aicf:implementar-spec`**

- `writing-plans` + `subagent-driven-development` (Superpowers) — the plan goes to a file, and subagents execute task by task.
- `to-tickets` + `implement` (Matt) — the spec becomes tickets with declared dependencies between them, executed one at a time.
- `code-review` (Matt) — reviews the diff on two axes, repository standards and faithfulness to the spec, in parallel subagents.

You can interview by one path and implement by another. Going down this list trades speed for a trail: on the `aicf` paths the plan lives in the session and dies with it.

</details>

<details>
<summary><strong>Why this one, and not Superpowers, Matt Pocock, GSD or BMAD</strong></summary>

Because it is not the same question. Superpowers and Matt's skills handle **the individual work item** well: they interrogate the idea, produce a spec, break it into tasks, and execute with discipline. And they do leave a trail — Superpowers writes the spec and plan to files on its _architectural_ path, Matt's publish spec and tickets to the tracker you picked in his setup (GitHub, GitLab or local markdown, plus any other tracker you describe in prose), and maintain a glossary and ADRs.

That trail, though, is **per work item** and written **before** execution. Three things fall outside it, and neither collection declares them somebody else's problem — they stop at the effort: they start from a request that is already bounded, however large, and end at the commit or the merge.

- **The product level.** Neither has the document stating what is being built, for whom, and what was ruled out by decision, nor the record of what shipped and what is missing. Matt's come close: they keep the request they turned down and what they ruled out of the effort in hand, with the reasoning — by effort, not by product.
- **Macro planning.** When a request is too big for one spec, `brainstorming` helps decompose it into sub-projects and works on the first one; the others stay in the conversation. Here, an idea that has not matured yet gets its own record, each work item declares in its own prose what it blocks and what it depends on, and what may never be done has a place to wait without getting lost. Matt's `wayfinder` comes close: it maps a request too big for one session and has `Not yet specified` for the idea that cannot be ticketed yet. The map belongs to one effort and ends with it; what is left over returns as a fresh effort, not as a queue that outlives it.
- **The afterwards.** A spec and a plan say what was intended. Matt's `implement` ends at the commit and neither closes the ticket nor ticks the acceptance criteria. Superpowers writes the plan and design doc into the repository, and they stay: the code is reviewed against the plan after each task, but plan and spec do not move — nothing updates them with what shipped. `aicf` asks for a report in the work item itself, and that is where the plan×delivery divergence gets written down.

`aicf` is that layer, and the same layer applies to any implementation path. Switching collections, or mixing both within one work item, changes nothing in governance.

**GSD and BMAD are the opposite case: they already have this layer.** GSD Core's `PROJECT.md` has "What This Is", "Core Value", "Out of Scope" with the reasoning, and "Key Decisions"; `complete-milestone` and `extract-learnings` do what `fechar-demanda` does here. The difference is that in both the layer comes welded to an execution loop of their own — 72 `/gsd-*` commands in GSD Core, 30 skills and a hard `uv` requirement in BMAD — and that loop is exactly what `aicf` leaves out by decision ([ADR 0001](docs/adr/0001-fronteira-de-fase.md)): here, whatever runs inside the implementation phase is the method you picked for it. If you want the whole package, GSD does more than `aicf`; if you want just the layer, and to implement by whatever path you prefer, this is it.

</details>

## About

Built for the [Claude Code: Criador de Apps](https://aicodingflow.com/curso) course, by [AI Coding Flow](https://aicodingflow.com). Use it freely, with or without the course.

MIT.
