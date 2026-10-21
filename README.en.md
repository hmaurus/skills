![AI Coding Flow — Skills for AI software engineering, written in Portuguese](docs/assets/banner.en.png)

# AI Coding Flow Skills

_[Versão em português](README.md)_

**You don't have to choose between Superpowers and Matt Pocock: pick both, with `aicf`.**

`aicf` is a skill plugin for Claude Code and Antigravity that brings together product management and software engineering, running the lifecycle of each work item from the moment it is recorded to closing. [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock's skills](https://github.com/mattpocock/skills) are two of the most popular software engineering skill collections on GitHub: 302k and 298k stars on 2026-10-20 (`gh api repos/obra/superpowers --jq .stargazers_count`, and the same for `mattpocock/skills`). `aicf` joins the two, and you can interview a work item with one and implement it with the other. On top of them it adds the PRD, the roadmap, the work item registry, and the report of what shipped. With neither installed, the `aicf` path, which ships with the plugin, handles interview and implementation on its own. There are seven skills.

Both collections cover one work item at a time, and cover it well. Three questions go unanswered:

- **Where does the project stand?** Specs describe each change, one by one. None of them says what the product is, who it serves, and what was ruled out by decision.
- **Why did we decide against that?** The reason for dropping an approach stayed in the conversation with the agent, and the conversation is not saved. Weeks later the same argument comes back.
- **What actually shipped?** The spec and the plan were written before execution. Neither of them is updated with what changed during implementation.

> **Written in Portuguese.** The skills instruct the agent in pt-BR and the file conventions mix the playbook's terms with Portuguese names (`intents/` and `specs/` for the two states of a work item, `backlog/`, `concluidas/` for completed). The GitHub labels of the issue mode are the same words: `aicf:backlog`, `aicf:intent`, `aicf:spec`. They work fine in an English-speaking session: Claude reads the instructions and answers you in whatever language you write. If you want the artifacts named in English, fork and translate.

## Install

aicf runs in four harnesses, the agents that load and run the skills. **Claude Code and Antigravity are targets**: every release is tested on them. **Codex and opencode are compatible**: aicf avoids breaking on them, but does not test them on every release.

### Claude Code (target)

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

To update: `claude plugin update aicf@aicodingflow`.

### Antigravity (target)

`agy` installs the Claude Code plugin from a folder, converting it:

```bash
git clone https://github.com/hmaurus/skills ~/aicf
agy plugin install ~/aicf
```

To update: `git -C ~/aicf pull && agy plugin install ~/aicf`, which installs over the old copy.

`~/aicf` is only a suggestion, here and for opencode: any folder works, as long as the update — and, for opencode, the config — points to it.

### Codex (compatible)

```bash
codex plugin marketplace add hmaurus/skills
codex plugin add aicf@aicodingflow
```

To update: `codex plugin marketplace upgrade aicodingflow`.

### opencode (compatible)

opencode reads the skills straight from the clone, through the `skills` key in its config:

```bash
git clone https://github.com/hmaurus/skills ~/aicf
```

In `~/.config/opencode/opencode.json` (or `.jsonc`), which applies to every project, or in a project's `opencode.json`:

```json
"skills": { "paths": ["~/aicf/skills"] }
```

Use the form with `paths`. The bare list, `"skills": ["~/aicf/skills"]`, is in the published schema, but opencode 1.17 rejects a config that uses it.

To update: `git -C ~/aicf pull`. **opencode does not hide `setup`, `prd` and `ajuda` from the agent.** In the other harnesses only you invoke them; in opencode the agent may call them on its own.

### After installing

Start a new session: skills load at the start of a session and do not hot-swap. On a new project, start with `setup`. On an existing one, with `ajuda`, which explains the cycle.

| Harness | How to invoke a skill |
| --- | --- |
| Claude Code | `/aicf:setup` |
| Antigravity | `/aicf:setup` |
| Codex | `$aicf:setup` |
| opencode | ask for it by name, no prefix: "use the setup skill" |

The skills write `/aicf:name` when they refer to each other. In Codex and opencode, translate with the table.

## The cycle

Every work item goes through the same four phases. Each one leaves it in a state, which is the folder the file lives in or the issue's label.

```mermaid
flowchart LR
  R[Intake<br/>backlog or intent]
  E[Interview<br/>spec]
  I[Implementation<br/>the code, still spec]
  F[Closing<br/>done, in concluidas/]
  R --> E --> I --> F
  F -.-> R
```

- **Intake** — the idea recorded, even before it is mature. It goes to backlog while uncertain, to intent once decided.
- **Interview** — questions until no decision is left open. The work item becomes a spec.
- **Implementation** — someone executes the spec, through the `aicf` path, Superpowers or Matt. The state does not change.
- **Closing** — the report of what was done, including what came out different from the plan. The work item moves to `concluidas/`.

Each work item is a versioned file in the repository, or a GitHub issue. You pick which one at setup.

## The problem this solves

![aicf: product management on top; Superpowers, Matt Pocock and the aicf path below](docs/assets/hero.en.svg)

### Where does the project stand?

`/aicf:prd` interviews you and writes `PRD.md`. It has a "ruled out, by decision" section, which holds what you decided against and why.

### Why did we decide against that?

`/aicf:criar-spec` runs the interview for a work item and writes the result to a file in the repository, including what was decided **against**.

### What actually shipped?

`/aicf:fechar-demanda` asks for a report of what shipped and keeps it with the work item. It runs whatever the implementation path: `aicf`'s, Superpowers' or Matt's.

## Starting a new project

**1. `/aicf:setup`.** Sets up the base: `PRD.md`, the place where work items will live, and the root `CLAUDE.md`, the file the agent reads at the start of every session.

It asks for the project name, a sentence or two about it, whether a work item lives in a file or an issue, and what to do with the engineering defaults. The tools you already use (password manager, library docs, skill collections) it looks up on your machine, and only asks about what it cannot find. If the directory is not a git repository yet, it offers `git init` before asking where work items live. At the end it leaves what it created in a first commit on `main` and hands you `develop`, the working branch.

**2. Fill in `PRD.md`.** It ships with the sections and a prompt under each. `/aicf:prd` interviews you section by section and writes the file, starting from the problem rather than the solution.

<details>
<summary>Why the PRD does not go through the work item cycle</summary>

A spec describes a change, with a scope and a "done" state. The PRD describes the product, and gets revised every time a decision contradicts it. If the PRD were a work item, its interview would discuss how to write the file, and the questions that matter (audience, what is ruled out) would stay unanswered. Then would come a closing asking for a report, archiving and a lint check on a `.md`.

</details>

**3. List what the product needs to have.** Each item becomes a line in `ROADMAP.md`, or a backlog issue. When an item gets a record of its own, its line leaves the roadmap, so that two places are not holding the same item.

**4. First work item.** `/aicf:criar-spec` to mature it, `/aicf:implementar-spec` to execute and close. From there the cycle repeats.

The interview and implementation phases accept Superpowers and Matt Pocock's skills, if installed, and you can interview with one and implement with the other. The work item registry does not change, and the work item notes which path was used.

## The skills

There are seven. What separates them is who can invoke each one.

**You type them.** They only exist when you call them; the first two drive a whole session.

| Skill | When | What it does |
| --- | --- | --- |
| `/aicf:setup` | once, on a new project | Initializes the git repository if missing, asks whether work items live in files or issues and sets up whatever the answer requires: `docs/projeto/` with the PRD, roadmap and work item folders, or the GitHub repository and the three `aicf:*` labels. In both cases it creates `CLAUDE.md` (with `AGENTS.md` pointing to it), a `README.md`, the engineering defaults if you want them, the first commit on `main` and a `develop` branch |
| `/aicf:prd` | start of the project, and when the PRD goes stale | Interviews you about the product and writes `PRD.md`. When revising, it checks the PRD against the work items, the ADRs and the glossary before asking, and only interviews you on what the project can't answer |
| `/aicf:ajuda` | whenever you want to reread the method | The map: the cycle, what each phase produces, and the work item registry conventions |

**You type them, or the agent reaches for them.** They answer requests in plain language, such as "interview me about X" or "implement spec Y", and the agent loads them when it recognizes the intent.

| Skill | When | What it does |
| --- | --- | --- |
| `/aicf:criar-spec` | interview phase | Interrogates until no decision is left open, then writes the spec, with a suggested implementation path. `/aicf:criar-spec #12` adopts an issue that already exists |
| `/aicf:implementar-spec` | implementation phase | Picks the path from the spec's suggestion, implements and verifies. At the end it calls closing |
| `/aicf:fechar-demanda` | closing phase | Checks, report, archiving and knowledge promotion, whatever the implementation path |
| `/aicf:proxima-demanda` | between work items | Reads the body of everything still open, in the record and outside it (unmerged branch, ticket, plan), and suggests the next one, with the alternatives and the command to start it |

The skills are small on purpose. They say what the agent could not infer: where to write, what to record, and when to close. What the tool already does well, and what is better decided case by case, stays with the agent.

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

A work item is the unit of work. The file describing it is born as an **intent**, becomes a **spec** once it is ready to implement (the same file, moved) and ends in `concluidas/` with the report. The four folders sit at the same level, so moving the file does not break the relative links that point out of it.

In issue mode, maturity lives in a label (`aicf:backlog`, `aicf:intent`, `aicf:spec`). A work item is a single issue from birth to closing: the label changes, the number does not. Completed means the issue is closed, with the report in a comment. In that mode `docs/projeto/` holds only `PRD.md`. The PRD, ADRs and the glossary stay in files in both modes.

You switch modes by editing one line of `CLAUDE.md`. A missing line means files, so a project created before this option keeps working untouched. The choice applies from that point on: there is no migration, what is already in files stays where it is, and new work items are born in the new medium.

| | Files | Issues |
| --- | --- | --- |
| Setup | none | needs `gh`, a login and a remote |
| Offline | survives `git clone` with no network | no |
| Search | shows up in the repository's `grep` | GitHub search |
| Conversation | none | comments and notifications |
| Outside contribution | issue as input, triaged into a file | two clicks |
| Reference | the file path | `#12`, and `Fixes #12` closes on merge |

The default is files, because that works with no `gh`, no login and no remote.

If your project needs a different structure, write the difference in the root `CLAUDE.md` or in `.claude/rules/`, never in a `CLAUDE.md` inside `docs/projeto/`. A subfolder `CLAUDE.md` only enters context when the agent reads a file from that folder, and recording a new work item does not require that.

</details>

<details>
<summary><strong>Neighbouring commands worth knowing</strong> — and what each one is for</summary>

None of these ship with `aicf`. They belong to the [Superpowers](https://github.com/obra/superpowers) and [Matt Pocock](https://github.com/mattpocock/skills) collections, the two `aicf` integrates, and they apply if you have them installed.

**Before writing the work item**

- `grill-me` (Matt) — challenges the idea with questions, until every branch of the decision is resolved. It records nothing; the result feeds the interview.
- `grill-with-docs` (Matt) — the same grilling, recording along the way: a resolved term goes to `GLOSSARY.md`, and a hard-to-reverse decision becomes an ADR ([its `SKILL.md` at v1.3.1](https://github.com/mattpocock/skills/blob/v1.3.1/skills/engineering/grill-with-docs/SKILL.md), which calls `grilling` and `domain-modeling`).
- `wayfinder` (Matt) — maps a request too big for one session as decision tickets on your tracker, and resolves them one at a time. The map covers that request.
- `domain-modeling` (Matt) — records the project's vocabulary in a `GLOSSARY.md`.

**In the interview phase, instead of `/aicf:criar-spec`**

- `brainstorming` (Superpowers) — interviews you up to an approved design; the spec comes out of it through `/aicf:criar-spec`.
- `grill-with-docs` (Matt) — interviews you by grilling; the spec comes out of the conversation through `/aicf:criar-spec`, which the agent invokes when it ends.

**In the implementation phase, instead of `/aicf:implementar-spec`**

- `writing-plans` + `subagent-driven-development` (Superpowers) — the plan goes to a file, and subagents execute task by task.
- `to-tickets` + `implement` (Matt) — the spec becomes tickets with declared dependencies between them, executed one at a time.
- `code-review` (Matt) — reviews the diff on two axes, repository standards and faithfulness to the spec, in parallel subagents.

You can interview by one path and implement by another. These flows write different amounts of documentation: on `aicf`'s own paths the implementation plan is not persisted to the repository.

</details>

<details>
<summary><strong>Why this one, and not Superpowers, Matt Pocock, GSD or BMAD</strong></summary>

Superpowers and Matt Pocock's skills cover one work item at a time: they interview the idea, produce a spec, break it into tasks and execute. Both write files. Superpowers writes the spec and plan on the _architectural_ path. Matt's publish spec and tickets to the tracker picked in his setup (GitHub, GitLab, local markdown, or another one you describe in prose), and maintain a glossary and ADRs.

Those files describe one work item and are written before execution. Three things appear in neither collection:

- **Product document.** Neither creates a file stating what the product is, who it serves and what was ruled out by decision. Matt's keep rejected requests in `.out-of-scope/<concept>.md`, with the reasoning. That covers one request at a time.
- **Planning across work items.** Superpowers' `brainstorming` breaks a large request into sub-projects and works the first one; the others stay in the conversation. Matt's `wayfinder` builds a ticket map for a large request, with `Not yet specified` for what cannot be detailed yet, and that map ends along with that piece of work. Neither keeps a list that spans several work items.
- **A record after execution.** Matt's `implement` ends at the commit; it neither closes the ticket nor ticks the acceptance criteria. Superpowers reviews the code against the plan after each task, but does not update the plan or the spec with what changed. In `aicf`, `fechar-demanda` asks for a report in the work item itself, and that is where the differences between what was planned and what shipped are written down.

If you already use one of these collections, you can keep it and add the other. `aicf` adds product management and handles the handoff between phases; inside each phase, the path you picked is in charge.

**GSD and BMAD already have this part.** GSD Core's `PROJECT.md` has "What This Is", "Core Value", "Out of Scope" with the reasoning, and "Key Decisions"; `complete-milestone` and `extract-learnings` do what `fechar-demanda` does here. The difference is that in both, product management comes together with an execution engine of their own: 72 `/gsd-*` commands in GSD Core, 30 skills and a hard `uv` requirement in BMAD. `aicf` leaves that engine out by decision ([ADR 0001](docs/adr/0001-fronteira-de-fase.md)): inside the implementation phase, whatever runs is the method you picked. GSD delivers more than `aicf`. The choice is between adopting its execution engine or using Superpowers and Matt Pocock with `aicf`.

</details>

## About

Built for the [Claude Code: Criador de Apps](https://aicodingflow.com/curso) course, by [AI Coding Flow](https://aicodingflow.com). Use it freely, with or without the course.

Suggestions and problems come in through an [issue](https://github.com/hmaurus/skills/issues/new/choose). Each one is triaged into `docs/projeto/`, and the issue closes with a link to the file it produced, or with the reason it was declined.

MIT.
