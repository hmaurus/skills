# aicf — project governance for building with agents

_[Versão em português](README.md)_

A starter kit for running a software project with Claude Code: the documents that hold a project together — vision, delivery checklist, versioned work items — and the cycle that takes each one from raw idea to a record of what was actually done.

> **Written in Portuguese.** The skills instruct the agent in pt-BR and the file conventions use Portuguese names (`demandas/` for work items, `concluidas/` for completed, `backlog/`). They work fine in an English-speaking session — Claude reads the instructions and answers you in whatever language you write — but if you want the artifacts named in English, fork and translate.

## Where it fits

Skill collections like [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock's](https://github.com/mattpocock/skills) handle **the individual work item** well: they interrogate the idea, produce a spec, break it into tasks, and execute with discipline. And they do leave a trail — Superpowers writes the spec and plan to files; Matt's publish spec and tickets to an issue tracker and maintain a glossary and ADRs.

That trail, though, is **per work item** and written **before** execution. Two things fall outside it:

- **The product level.** Neither has the document stating what is being built, for whom, and what was ruled out by decision — nor the single list of what shipped and what is missing. Twenty well-written specs do not answer "where does the project stand".
- **The afterwards.** A spec and a plan say what was intended. What actually shipped, where delivery diverged from the plan and why, only exists if someone writes it at closing time — and neither pipeline asks for that.

`aicf` is that layer — and it works two ways:

- **On its own**, with a native path for interview and implementation. Nothing else to install.
- **On top**, if you already use the others. Interview with Superpowers' `brainstorming` or Matt's `grill-with-docs`: the record still lands in the same place, and the work item notes which path was used.

## Install

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Restart your session afterwards — skills load at startup and do not hot-swap.

On an existing project, start with `/aicf:workflow-demanda`, which explains the cycle.

## Starting a new project

**1. `/aicf:setup`** — creates `docs/projeto/` with a PRD and checklist, the work-item folders, and the root `CLAUDE.md`. It asks little: the name, a sentence or two about the project, where the engineering defaults live, and which tools you already use.

**2. Fill in `PRD.md`.** It ships with the sections and a prompt under each. The one that pays off most is **"ruled out, by decision"** — it is what keeps the same argument from coming back six months later.

**`/aicf:criar-prd`** interviews you section by section and writes the file. It starts from the problem rather than the solution, and does not let "out of scope" go blank. Two complements, when you need them:

- **`grilling`** (Matt Pocock) — beforehand, if you think you already know what you want and would rather be challenged. It stores nothing; what comes out of the conversation feeds the PRD interview.
- **`domain-modeling`** (Matt Pocock) — afterwards, if the product has vocabulary of its own that has already turned ambiguous. It writes the glossary into `CONTEXT.md`, beside the PRD rather than inside it.

**What does not work is running the PRD through the work-item cycle.** Not because it is a document — a spec handles documentation changes fine. It is that a spec describes a **change**, with a scope and a "done" state, while the PRD describes the **product**, and gets revised whenever a decision contradicts it. Wrapping one in the other yields an empty spec — its interview would debate how to write the file, while the questions that matter, audience and what is ruled out, stay unanswered — plus a closing ritual asking for a report, archiving, and a lint check on a `.md`.

**3. Derive `CHECKLIST.md` from the PRD.** Every thing the product needs becomes one line. What fits in a line stays there; what needs context becomes a file under `demandas/`.

**4. First work item.** `/aicf:criar-spec` to mature it, `/aicf:implementar-spec` to execute and close. From there the cycle repeats.

## The skills

| Skill                    | When                    | What it does                                                                    |
| ------------------------ | ----------------------- | -------------------------------------------------------------------------------- |
| `/aicf:setup`            | once, on a new project  | Creates `docs/projeto/` with a PRD and checklist, the work-item folders, the root `CLAUDE.md` (with `AGENTS.md` symlinked to it) and a `README.md` — plus engineering defaults, if you want them |
| `/aicf:criar-prd`        | start of the project    | Interviews you about the product and writes `PRD.md` — run it again when a decision contradicts it |
| `/aicf:workflow-demanda` | the map                 | The cycle, the paths available at each phase, and the governance conventions      |
| `/aicf:criar-spec`       | interview phase         | Interrogates until no open decision is left, then writes the spec into the repo   |
| `/aicf:implementar-spec` | implementation phase    | Reads the spec, implements and verifies; calls the closing ritual at the end      |
| `/aicf:fechar-demanda`   | closing phase           | Checks, report, archiving and knowledge promotion — the agent applies it when any work item completes, whatever the path |

## The problem this solves

Agent sessions are volatile. The conversation where you decided **not** to take some approach dies with `/clear`, and three weeks later someone — human or agent — reopens the same argument, because the reasoning was never written down anywhere.

The cycle has four phases:

1. **Work item** — what you want, still raw
2. **Interview** — matures it and produces the spec
3. **Implementation** — consumes the spec
4. **Closing** — a report of what was **actually** done, including where delivery diverged from plan

What holds it together is the record: each work item is a file in the repository, and on completion it gets a report and moves to `concluidas/`. The reasoning lives in the repo, not in the chat.

## Paths, not a single track

Phases 2 and 3 are independent, and the choice belongs to the user — the agent suggests, it does not decide:

- **Interview** — `/aicf:criar-spec`, or `brainstorming` (Superpowers), or `grill-with-docs` + `to-spec` (Matt Pocock)
- **Implementation** — `/aicf:implementar-spec` (with or without plan mode), or `writing-plans` + `subagent-driven-development`, or `to-tickets` + `implement`

You can interview one way and implement another. The work item records which was used, on a `Processo:` line.

## The structure

```
docs/projeto/            # project
├── PRD.md               # why the product exists: vision, audience, model
├── CHECKLIST.md         # what shipped and what is missing
└── demandas/            # work items
    ├── <demanda>.md     # one per file
    ├── concluidas/      # archived, with a report
    └── backlog/         # not yet certain they will be done
```

If your project needs a different structure, write the differences into a `CLAUDE.md` inside `docs/projeto/` — Claude Code loads that file when it touches the folder, and **project instructions take precedence over the skill's**. That is how a repository adopts the method without forking the skills.

## About

Built for [Claude Code: Criador de Apps](https://aicodingflow.com/curso), a course by [AI Coding Flow](https://aicodingflow.com). Use it freely, with or without the course.

MIT.
