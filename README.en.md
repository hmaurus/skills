# aicf — project governance for building with agents

_[Versão em português](README.md)_

A starter kit for running a software project with Claude Code: the documents that hold a project together — vision, delivery checklist, versioned work items — and the cycle that takes each one from raw idea to a record of what was actually done. It covers **governance** and **macro planning**, which engineering skill collections leave out, and it is **agnostic** about the implementation path: governance is the same whether a work item is interviewed and implemented through the aicf path, through Superpowers, or through Matt Pocock's skills.

> **Written in Portuguese.** The skills instruct the agent in pt-BR and the file conventions mix the playbook's terms with Portuguese names (`intents/` and `specs/` for the two states of a work item, `backlog/`, `concluidas/` for completed). They work fine in an English-speaking session — Claude reads the instructions and answers you in whatever language you write — but if you want the artifacts named in English, fork and translate.

## Where it fits

Skill collections like [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock's](https://github.com/mattpocock/skills) handle **the individual work item** well: they interrogate the idea, produce a spec, break it into tasks, and execute with discipline. And they do leave a trail — Superpowers writes the spec and plan to files; Matt's publish spec and tickets to an issue tracker and maintain a glossary and ADRs.

That trail, though, is **per work item** and written **before** execution. Three things fall outside it, and neither collection declares them somebody else's problem — they simply start at an idea that is already formed and stop at the commit or the merge:

- **The product level.** Neither has the document stating what is being built, for whom, and what was ruled out by decision — nor the single list of what shipped and what is missing. Twenty well-written specs do not answer "where does the project stand".
- **Macro planning.** When a request is too big for one spec, Superpowers' `brainstorming` helps decompose it into sub-projects and works on the first one; the others stay in the conversation. Here, an idea that has not matured yet gets its own file, a set of work items that move together shows up grouped in the checklist, and what may never be done has a place to wait without getting lost.
- **The afterwards.** A spec and a plan say what was intended. What actually shipped, where delivery diverged from the plan and why, only exists if someone writes it at closing time. Matt's `implement` ends at the commit and neither closes the ticket nor ticks the acceptance criteria; Superpowers lists the decisions it made on its own in the final message and deletes the working folder, because from there on git history is the record. `aicf` asks for a report in the work item's file, and that is where the plan×delivery divergence gets written down.

`aicf` is that layer, and the same layer applies to any implementation path. It works two ways:

- **On its own**, with an aicf path of its own for interview and implementation. Nothing else to install.
- **On top**, if you already use the others. Interview with Superpowers' `brainstorming` or Matt's `grill-with-docs`, implement with `subagent-driven-development` or with `to-tickets` + `implement`: the record still lands in the same place, closing is the same, and the work item notes which path was used. Switching collections, or mixing both within one work item, changes nothing in governance.

## Install

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Restart your session afterwards — skills load at startup and do not hot-swap.

On an existing project, start with `/aicf:workflow-demanda`, which explains the cycle.

## Starting a new project

**1. `/aicf:setup`** — creates `docs/projeto/` with a PRD and checklist, the `intents/` and `specs/` folders, and the root `CLAUDE.md`. It asks little: the name, a sentence or two about the project, where the engineering defaults live, and which tools you already use.

**2. Fill in `PRD.md`.** It ships with the sections and a prompt under each. The one that pays off most is **"ruled out, by decision"** — it is what keeps the same argument from coming back six months later.

**`/aicf:criar-prd`** interviews you section by section and writes the file. It starts from the problem rather than the solution, and does not let "out of scope" go blank. Two complements, when you need them:

- **`grilling`** (Matt Pocock) — beforehand, if you think you already know what you want and would rather be challenged. It stores nothing; what comes out of the conversation feeds the PRD interview.
- **`domain-modeling`** (Matt Pocock) — afterwards, if the product has vocabulary of its own that has already turned ambiguous. It writes the glossary into `CONTEXT.md`, beside the PRD rather than inside it.

**What does not work is running the PRD through the work-item cycle.** Not because it is a document — a spec handles documentation changes fine. It is that a spec describes a **change**, with a scope and a "done" state, while the PRD describes the **product**, and gets revised whenever a decision contradicts it. Wrapping one in the other yields an empty spec — its interview would debate how to write the file, while the questions that matter, audience and what is ruled out, stay unanswered — plus a closing ritual asking for a report, archiving, and a lint check on a `.md`.

**3. Derive `CHECKLIST.md` from the PRD.** Every thing the product needs becomes one line. What fits in a line stays there; what needs context becomes a file under `intents/`.

**4. First work item.** `/aicf:criar-spec` to mature it, `/aicf:implementar-spec` to execute and close. Both also answer a plain-language request — "interview me about X", "implement spec Y" — because the agent loads them on its own when it recognizes the intent. From there the cycle repeats.

## The skills

| Skill                    | When                    | What it does                                                                    |
| ------------------------ | ----------------------- | -------------------------------------------------------------------------------- |
| `/aicf:setup`            | once, on a new project  | Creates `docs/projeto/` with a PRD and checklist, the `intents/` and `specs/` folders, the root `CLAUDE.md` (with `AGENTS.md` symlinked to it) and a `README.md` — plus engineering defaults, if you want them |
| `/aicf:criar-prd`        | start of the project    | Interviews you about the product and writes `PRD.md` — run it again when a decision contradicts it |
| `/aicf:workflow-demanda` | the map                 | The cycle, the paths available at each phase, and the governance conventions      |
| `/aicf:criar-spec`       | interview phase         | Interrogates until no open decision is left, then writes the spec into the repo, with a suggested implementation path |
| `/aicf:implementar-spec` | implementation phase    | Picks the path from the spec's suggestion — follows it when the case is obvious, asks otherwise —, implements and verifies; calls the closing ritual at the end |
| `/aicf:fechar-demanda`   | closing phase           | Checks, report, archiving and knowledge promotion — the agent applies it when any work item completes, whatever the path |

The skills are deliberately small: they say what the agent could not infer on its own — where to write, what to record, when to close — and stop there. What the tool already does well, and what is better decided case by case, stays with the agent; the more a skill describes, the more it has to be rewritten with every evolution of the model.

## The problem this solves

Agent sessions are volatile. The conversation where you decided **not** to take some approach dies with `/clear`, and three weeks later someone — human or agent — reopens the same argument, because the reasoning was never written down anywhere.

The cycle has four phases:

1. **Work item** — what you want, still raw
2. **Interview** — matures it and produces the spec
3. **Implementation** — consumes the spec
4. **Closing** — a report of what was **actually** done, including where delivery diverged from plan

What holds it together is the record: each work item is a file in the repository, and on completion it gets a report and moves to `specs/concluidas/`. The reasoning lives in the repo, not in the chat.

## Paths, not a single track

Phases 2 and 3 are independent. At the interview, the path is the user's call; at implementation, the agent follows the suggestion recorded in the spec when the case is obvious — the direct aicf path and a diff that fits in one sentence — and asks with options otherwise. The agent suggests, and when there is a real choice the decision is the user's:

- **Interview** — `/aicf:criar-spec`, or `brainstorming` (Superpowers), or `grill-with-docs` + `to-spec` (Matt Pocock)
- **Implementation** — `/aicf:implementar-spec` (with or without plan mode), or `writing-plans` + `subagent-driven-development`, or `to-tickets` + `implement`

You can interview one way and implement another. The work item records which was used, on a `Processo` line.

## The structure

```
docs/projeto/            # project
├── PRD.md               # why the product exists: vision, audience, model
├── CHECKLIST.md         # what shipped and what is missing
├── intents/
│   ├── <intent>.md      # decided, not yet interviewed
│   └── backlog/         # not yet certain it will be done
└── specs/
    ├── <spec>.md        # ready to implement
    └── concluidas/      # archived, with a report
```

The folder tells the document's maturity. A work item is the unit of work; the file describing it is born as an **intent** (decided, not yet interviewed), becomes a **spec** when it is ready to implement — the same file, moved — and ends in `specs/concluidas/` with its report. `intents/backlog/` holds what may never be done.

If your project needs a different structure, write the difference into the root `CLAUDE.md` or into `.claude/rules/`, never into a `CLAUDE.md` inside `docs/projeto/`: a subdirectory `CLAUDE.md` only enters the context when the agent reads a file in that folder, and registering a new work item does not require that.

## About

Built for [Claude Code: Criador de Apps](https://aicodingflow.com/curso), a course by [AI Coding Flow](https://aicodingflow.com). Use it freely, with or without the course.

MIT.
