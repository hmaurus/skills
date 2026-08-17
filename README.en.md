# aicf — workflow skills for Claude Code

_[Versão em português](README.md)_

Three skills covering the life of a work item: **interview** it until it becomes a spec, **implement** from that spec, **close** it with a record of what was actually done.

Not a framework, not a new methodology. It is the minimum that keeps an agent-driven project from losing track of what was decided and why.

> **Written in Portuguese.** The skills instruct the agent in pt-BR and the file conventions use Portuguese names (`demandas/`, `concluidas/`, `backlog/`). They work fine in an English-speaking session — Claude reads the instructions and answers you in whatever language you write — but if you want the artifacts named in English, fork and translate.

## Install

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Restart your session afterwards — skills load at startup and do not hot-swap.

## The three skills

| Skill                    | Phase          | What it does                                                                  |
| ------------------------ | -------------- | ----------------------------------------------------------------------------- |
| `/aicf:workflow-demanda` | the map        | The whole cycle, the paths available at each phase, and the governance conventions |
| `/aicf:criar-spec`       | interview      | Interrogates until no open decision is left, then writes the spec into the repo |
| `/aicf:implementar-spec` | implementation | Reads the spec, implements, verifies, and runs the closing ritual              |

Start with `/aicf:workflow-demanda` — the other two are its phases on the native path.

## The problem this solves

Agent sessions are volatile. The conversation where you decided **not** to take some approach dies with `/clear`, and three weeks later someone — human or agent — reopens the same argument, because the reasoning was never written down anywhere.

The cycle has four phases:

1. **Work item** — what you want, still raw
2. **Interview** — matures it and produces the spec
3. **Implementation** — consumes the spec
4. **Closing** — a report of what was **actually** done, including where delivery diverged from plan

What holds it together is the record: each work item is a file in the repository, and on completion it gets a report and moves to `concluidas/` (_completed_). The reasoning lives in the repo, not in the chat.

## Paths, not a single track

Phases 2 and 3 are not locked to these skills. Each has alternatives, and the choice belongs to the user — the agent suggests, it does not decide:

- **Interview** — `/aicf:criar-spec`, or `brainstorming` ([Superpowers](https://github.com/obra/superpowers)), or `grill-with-docs` + `to-spec` ([Matt Pocock](https://github.com/mattpocock/skills))
- **Implementation** — `/aicf:implementar-spec` (with or without plan mode), or `writing-plans` + `subagent-driven-development`, or `to-tickets` + `implement`

You can interview one way and implement another. The work item records which was used, on a `Processo:` line.

## Conventions the skills assume

```
docs/projeto/            # project
├── PRD.md               # why the product exists
├── CHECKLIST.md         # what shipped and what is missing
└── demandas/            # work items
    ├── <demanda>.md
    ├── concluidas/      # completed
    └── backlog/
```

Your project may diverge from this — if there is a `CLAUDE.md` inside `docs/projeto/`, it wins.

## About

Built for [Claude Code: Criador de Apps](https://aicodingflow.com/curso), a course by [AI Coding Flow](https://aicodingflow.com). Use it freely, with or without the course.

MIT.
