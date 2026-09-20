# Governança macro nos frameworks vizinhos — pesquisa de 2026-09-19

Sete frameworks de desenvolvimento com agente, lidos em fonte primária (código, templates, issues e
blog dos autores), contra os quatro critérios que definem a governança do aicf. Serve a quem for
ajustar a comparação do `README.md`, decidir o que o aicf copia ou deixa de fora, ou responder "por
que não o X?".

**Toda afirmação está pinada num sha e vem com o comando que a confere.** Os comandos usam `$R`
como diretório dos clones; para reproduzir, clonar cada repositório e conferir o sha:

```bash
R=/tmp/frameworks && mkdir -p $R
for r in obra/superpowers mattpocock/skills github/spec-kit Fission-AI/openspec open-gsd/gsd-pi glittercowboy/get-shit-done open-gsd/gsd-core bmad-code-org/bmad-method eyaltoledano/claude-task-master; do
  git clone -q https://github.com/$r $R/${r#*/}
done
for d in $R/*; do echo "$(basename $d) $(git -C $d rev-parse --short HEAD)"; done
```

Sha diferente da tabela abaixo significa que o repositório andou: `git -C $R/<nome> checkout <sha>`
recupera o estado pesquisado, e o que mudou desde então é assunto de pesquisa nova, não desta.

A seção "Afirmações do README/CLAUDE.md do aicf" descreve o estado do repositório em `07cb4a9`; a
demanda [a comparação com os vizinhos erra e ignora o GSD](../projeto/specs/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md)
corrige o que ela aponta.

| Repositório | Clone | sha |
|---|---|---|
| obra/superpowers | `$R/superpowers` | `5bf4e78` |
| mattpocock/skills | `$R/skills` | `c55ee46` |
| github/spec-kit | `$R/spec-kit` | `d4229c0` |
| Fission-AI/openspec | `$R/openspec` | `bae58cf` |
| open-gsd/gsd-pi | `$R/gsd-pi` | `fa83b79` |
| glittercowboy/get-shit-done | `$R/get-shit-done` | `bdcaab2` (arquivado; README só redireciona) |
| open-gsd/gsd-core | `$R/gsd-core` | `6dcc042` (GSD canônico para Claude Code, ver §GSD) |
| bmad-code-org/bmad-method | `$R/bmad-method` | `f033e70` |
| eyaltoledano/claude-task-master | `$R/claude-task-master` | `c0c98d3` |

Conferir: `for d in $R/*; do echo "$(basename $d) $(git -C $d rev-parse --short HEAD)"; done`

## Os quatro critérios (definição do aicf)

1. **Documento de produto** — PRD/visão vivo: o que se constrói, para quem, o que ficou fora por decisão.
2. **Planejamento macro** — roadmap/backlog com estado de maturidade, dependências declaradas, lugar para ideia crua.
3. **Registro versionado por demanda** — cada demanda como arquivo no repo ou issue, sobrevivendo ao `/clear`.
4. **Registro do que foi feito** — relatório na própria demanda (plano × entrega), arquivamento, promoção do aprendizado para CLAUDE.md/ADR/glossário.

## Tabela-resumo

| Framework | 1. Doc de produto | 2. Planejamento macro | 3. Registro por demanda | 4. Registro do feito |
|---|---|---|---|---|
| Superpowers | NÃO | NÃO | PARCIAL | NÃO |
| Matt Pocock | NÃO (com nota) | PARCIAL | TEM | NÃO (com nota) |
| spec-kit | NÃO | PARCIAL | TEM | PARCIAL |
| openspec | PARCIAL | NÃO (experimento interno) | TEM | PARCIAL |
| GSD (gsd-core) | TEM | TEM | TEM | TEM |
| GSD Pi | TEM | TEM | TEM | TEM |
| BMAD | TEM | TEM | TEM | TEM |
| task-master | PARCIAL | PARCIAL | TEM | PARCIAL |

Leitura rápida: os dois que o README do aicf cita (Superpowers, Matt) de fato não têm a camada; os "pesados" (GSD, BMAD) têm os quatro itens, e em forma muito parecida com a do aicf; spec-kit, openspec e task-master têm o registro por demanda e um pedaço do "depois", mas não o documento de produto vivo.

---

## Superpowers (`5bf4e78`)

**Filosofia declarada** (README §Philosophy): "Test-Driven Development · Systematic over ad-hoc · Complexity reduction · Evidence over claims". O README abre com "a complete software development methodology" e o fluxo descrito é brainstorming → worktree → writing-plans → SDD/executing-plans → TDD → code review → finishing-a-development-branch.
Conferir: `awk '/^## Philosophy/,/^## Contributing/' $R/superpowers/README.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **NÃO** | Nenhuma skill, template ou doc produz documento de produto. `grep` por PRD/roadmap/backlog/vision nas 15 skills só acha "the spec is a vision document" (frase sobre a spec da demanda). | `grep -rniE 'PRD\|roadmap\|backlog\|product requirements' $R/superpowers/skills --include='*.md' \| wc -l` → só linhas de `code-reviewer.md`/`writing-plans` com "spec is a vision document" |
| 2 | **NÃO** | `brainstorming` diz: projeto grande demais → "help the user decompose into sub-projects ... Then brainstorm the first sub-project". Os outros subprojetos não vão para arquivo. Não há roadmap, backlog, estado ou dependência entre demandas. | `grep -n 'sub-project' $R/superpowers/skills/brainstorming/SKILL.md` |
| 3 | **PARCIAL** | Só no caminho **Architectural**: spec em `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` e plano em `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`, commitados. Nos caminhos **Bounded** e **Spike**: "No spec file, no implementation plan document". Não há índice nem estado. | `grep -n 'docs/superpowers/specs\|No spec file' $R/superpowers/skills/brainstorming/SKILL.md; grep -n 'Save plans to' $R/superpowers/skills/writing-plans/SKILL.md` |
| 4 | **NÃO** | `finishing-a-development-branch` = testes → merge/PR/keep → limpar worktree. Nada escreve no plano ou na spec depois. O SDD mantém um **ledger** `<workspace>/progress.md` (tarefas concluídas + rulings), mas ele vive no workspace da execução, não na demanda. A issue **#1075 "Plans and specs have no completion status after execution"** está ABERTA e é a thread canônica (#789 e #1599 fechadas como duplicatas dela). | `sed -n 1,30p $R/superpowers/skills/finishing-a-development-branch/SKILL.md; grep -n 'progress.md' $R/superpowers/skills/subagent-driven-development/SKILL.md; gh issue view 1075 -R obra/superpowers --json state,title` |

Nuance importante para o README do aicf: o código **é** revisto contra o plano durante a execução (SDD: "task review (spec compliance + code quality) after each"). O que não existe é o documento ser revisto/atualizado com o que saiu. Conferir: `sed -n 8p $R/superpowers/skills/subagent-driven-development/SKILL.md`.

## Matt Pocock (`c55ee46`)

**Filosofia declarada** (README): "My agent skills that I use every day to do real engineering — not vibe coding. ... Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control ... These skills are designed to be small, easy to adapt, and composable." Skills promovidas: `engineering/` e `productivity/`; `in-progress/`, `misc/`, `deprecated/` não entram no plugin (ADR 0002).
Conferir: `sed -n 15,20p $R/skills/README.md; sed -n 1,12p $R/skills/.agents/adr/0002-ship-as-a-claude-code-plugin.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **NÃO** (com nota) | `CONTEXT.md` é **só glossário**: "`CONTEXT.md` should be totally devoid of implementation details ... It is a glossary and nothing else." ADRs em `docs/adr/`. Não há doc de "o que / para quem". **Nota:** a parte "o que ficou fora por decisão" tem um lugar parcial: `.out-of-scope/<conceito>.md`, escrito pelo `triage` quando um enhancement é `wontfix` ("Institutional memory: why a feature was rejected"). E o `wayfinder` tem seções "Destination" e "Out of scope", mas por esforço, não por produto. | `grep -n 'glossary and nothing else' $R/skills/skills/engineering/domain-modeling/SKILL.md; sed -n 1,10p $R/skills/skills/engineering/triage/OUT-OF-SCOPE.md; grep -n '^## Out of scope\|^## Destination' $R/skills/skills/engineering/wayfinder/SKILL.md` |
| 2 | **PARCIAL** | Não há roadmap de produto. Mas: (a) `triage` é uma máquina de estados por issue (`needs-triage` → `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`); (b) `to-tickets` grava "Blocked by" por ticket, com dependência nativa no GitHub; (c) `wayfinder` é um mapa para "a loose idea ... too big for one agent session", com seção "Not yet specified" para o que ainda não dá para ticketar ("fog of war"). Ou seja: maturidade, dependências e ideia crua existem **por issue/esforço**, sem visão do todo. | `grep -n 'needs-triage\|ready-for-agent' $R/skills/skills/engineering/triage/SKILL.md \| head -3; grep -n 'Blocked by' $R/skills/skills/engineering/to-tickets/SKILL.md \| head -3; grep -n 'Not yet specified\|fog of war' $R/skills/skills/engineering/wayfinder/SKILL.md \| head -3` |
| 3 | **TEM** | `setup-matt-pocock-skills` grava `docs/agents/issue-tracker.md`. Opções no sha: **GitHub** (`gh`), **GitLab** (`glab`), **Local markdown** (`.scratch/<feature>/spec.md` + `issues/NN-slug.md`), **Other** ("Jira, Linear, etc.": o usuário descreve em prosa). `to-spec` publica a spec no tracker; `to-tickets` um arquivo/issue por ticket. | `sed -n 44,47p $R/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md; sed -n 1,12p $R/skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` |
| 4 | **NÃO** (com nota) | `implement` inteiro: "Implement the work ... Use /tdd ... Once done, use /code-review ... Commit your work to the current branch." Não fecha ticket nem marca critério de aceite. `to-tickets`: "Do NOT close or modify any parent issue." `code-review` tem um eixo **Spec** que compara o diff com a issue de origem, mas é revisão, não registro. `retro` (in-progress, não publicado) é retrospectiva do **ambiente do agente**, não da demanda. `implement-spec` (in-progress, não publicado) abre PR "marked as 'closing' the spec issue and tickets" — o fechamento viria do merge do PR, e só nessa skill não promovida. | `cat $R/skills/skills/engineering/implement/SKILL.md; grep -n 'Do NOT close' $R/skills/skills/engineering/to-tickets/SKILL.md; grep -n "closing" $R/skills/skills/in-progress/implement-spec/SKILL.md; grep -n 'name: retro' -A3 $R/skills/skills/in-progress/retro/SKILL.md` |

## spec-kit (`d4229c0`)

**Filosofia declarada** (README): "Build with a spec, fix a bug, or assess an idea — with your coding agent. ... Constitution once per project; specify → plan → tasks → implement → converge per feature." Três processos independentes: SDD (core), bug fixing e idea assessment (extensões).
Conferir: `sed -n 20,35p $R/spec-kit/README.md; grep -n 'Constitution once per project' $R/spec-kit/README.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **NÃO** | `constitution` grava `.specify/memory/constitution.md`, e o template é de **princípios de engenharia** (exemplos: "Library-First", "CLI Interface", "Test-First (NON-NEGOTIABLE)", "Integration Testing", "Observability"), com versionamento semântico das emendas. Não diz o que o produto é nem para quem. O termo "PRD" aparece só no ensaio `spec-driven.md`. | `sed -n 1,30p $R/spec-kit/templates/constitution-template.md; grep -c PRD $R/spec-kit/spec-driven.md` |
| 2 | **PARCIAL** | Não há comando. Há a **convenção documentada** "spec of specs" (`docs/concepts/spec-of-specs.md`): `specs/<epic>/roadmap.md` ou `ROADMAP.md` na raiz, tabela com ID estável, intent, scope boundary, `Depends on`, `Status` (planned · in-progress · done) e link para a sub-spec — "an ordinary Markdown file you author ... there is no special tooling behind it". Ideia crua: a extensão **idea assessment** ("Decide whether an idea deserves investment → go, clarify, or stop"), instalada à parte. | `sed -n 45,75p $R/spec-kit/docs/concepts/spec-of-specs.md; grep -n 'Idea assessment' $R/spec-kit/README.md` |
| 3 | **TEM** | `specify` cria `specs/NNN-<slug>/spec.md` (numeração sequencial ou por branch); `plan` e `tasks` gravam `plan.md` e `tasks.md` na mesma pasta. A spec tem `**Status**: Draft` no cabeçalho. | `grep -n 'specs/\|NNN' $R/spec-kit/templates/commands/specify.md \| head -5; sed -n 1,8p $R/spec-kit/templates/spec-template.md` |
| 4 | **PARCIAL** | `implement` marca tarefas `[X]` em `tasks.md`. `converge` lê spec+plan+tasks como "sole source of intent", avalia o código atual e **acrescenta** as lacunas como `## Phase N: Convergence` em `tasks.md` — é a divergência plano×entrega, mas expressa como trabalho restante, não como relatório do que mudou. Não há arquivamento, retro nem promoção de aprendizado; `docs/concepts/spec-persistence.md` deixa explícito: "Spec Kit intentionally leaves teams in control of what happens to spec.md, plan.md, and tasks.md after requirements change." | `grep -n 'mark the task off as \[X\]' $R/spec-kit/templates/commands/implement.md; grep -n 'Close the gap\|APPEND-ONLY' $R/spec-kit/templates/commands/converge.md; sed -n 1,8p $R/spec-kit/docs/concepts/spec-persistence.md` |

## openspec (`bae58cf`)

**Filosofia declarada** (README): "fluid not rigid · iterative not waterfall · easy not complex · built for brownfield not just greenfield · scalable from personal projects to enterprises". "vs. Spec Kit — Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup."
Conferir: `sed -n 28,36p $R/openspec/README.md; grep -n 'vs. \[Spec Kit\]' $R/openspec/README.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **PARCIAL** | `openspec/specs/<capability>/spec.md` é "Source of truth — how your system currently works": requisitos + cenários por capacidade, em linguagem de comportamento. Responde "o que o sistema faz hoje", não "para quem" nem "o que ficou fora por decisão". `openspec/config.yaml` tem um campo `context` livre (no repo deles: stack, regras de path, linguagem de produto). | `sed -n 30,50p $R/openspec/docs/concepts.md; sed -n 1,12p $R/openspec/openspec/config.yaml` |
| 2 | **NÃO** (experimento interno) | `changes/` é uma lista plana de pastas; não há roadmap, estado além de "ativa/arquivada", nem dependência entre changes. `explore` é conversa e diz "Track decisions in the conversation, not in files". **Mas** o próprio repo tem um experimento não documentado em `openspec/work/README.md`: "goal -> roadmap -> slice -> result", com `goal.md` (destino e porquê), `roadmap.md` ("expected to change as implementation reveals better sequencing") e `slices/<id>/result.md` ("records what actually happened and the evidence"). Não aparece em `docs/` nem no CHANGELOG (que registra a remoção do modelo anterior "workspace and initiative"). | `grep -n 'Track decisions in the conversation' $R/openspec/skills/openspec-explore/SKILL.md; sed -n 1,30p $R/openspec/openspec/work/README.md; grep -rln -i 'goal.md' $R/openspec/docs \| wc -l` → 0 |
| 3 | **TEM** | `propose` cria `openspec/changes/<name>/` com `proposal.md` (what & why), `specs/<capability>/spec.md` (delta), `design.md` (how), `tasks.md`. | `grep -n 'proposal.md\|design.md\|tasks.md' $R/openspec/skills/openspec-propose/SKILL.md \| head -4` |
| 4 | **PARCIAL** | `archive`: confere artefatos e checkboxes de `tasks.md`, **faz merge dos delta specs nos specs principais** (ADDED/MODIFIED/REMOVED/RENAMED) e move a pasta para `changes/archive/YYYY-MM-DD-<name>/`. Isso registra "o que agora é verdade", não "o que divergiu do plano"; a `proposal.md` fica como foi escrita. Nada promove aprendizado. | `grep -n 'Sync now\|mv "<changeRoot>"' $R/openspec/skills/openspec-archive-change/SKILL.md` |

## GSD — qual repositório é o canônico

- `glittercowboy/get-shit-done` (`bdcaab2`) está **arquivado**: o README diz "GSD Has Moved ... The project now continues as GSD Core in the Open GSD repository: https://github.com/open-gsd/gsd-core". Conferir: `sed -n 1,12p $R/get-shit-done/README.md`.
- `open-gsd/gsd-core` (`6dcc042`) é a continuação para Claude Code e outros harnesses: comandos `/gsd-new-project`, `/gsd-plan-phase` etc. em `commands/gsd/*.md`, estado em `.planning/`. É o que este relatório chama de **GSD**.
- `open-gsd/gsd-pi` (`fa83b79`) é outro produto da mesma organização: agente de terminal próprio (TUI/web, SQLite como fonte de verdade, projeções markdown em `.gsd/`). `VISION.md` conta a história: "the original maintainer (TÂCHES, GitHub glittercowboy) stopped responding ... around 2026-04-01 ... The v1 line continues separately as the community-maintained gsd-core". Conferir: `grep -n 'glittercowboy\|gsd-core' $R/gsd-pi/VISION.md`.

## GSD Core (`6dcc042`)

**Filosofia declarada** (README): "A light-weight meta-prompting, context engineering, and spec-driven development system ... It solves context rot ... by running all heavy research, planning, and execution work in fresh-context subagents". Loop por fase: Discuss → Plan → Execute → Verify → Ship. "structured artifacts like STATE.md and CONTEXT.md survive session boundaries".
Conferir: `sed -n 20,40p $R/gsd-core/README.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **TEM** | `.planning/PROJECT.md` ("the living project context document"): `## What This Is`, `## Core Value`, `## Business Context` (opcional), `## Requirements` com `### Validated` / `### Active` / `### Out of Scope` ("Includes reasoning to prevent re-adding"), `## Constraints`, `## Key Decisions`. Criado por `/gsd-new-project`, "updated by /gsd-complete-milestone as decisions are validated". | `sed -n 1,60p $R/gsd-core/gsd-core/templates/project.md; grep -n 'PROJECT.md' -A4 $R/gsd-core/docs/reference/planning-artifacts.md \| head -12` |
| 2 | **TEM** | `ROADMAP.md`: fases com checkbox, `**Depends on:**`, `**Requirements:** [REQ-IDs]`, `**Success Criteria**`, fases decimais para inserção urgente. `REQUIREMENTS.md`: v1 / v2 (deferred) / Out of Scope / tabela de rastreabilidade. Backlog: fases `999.x` + `/gsd-review-backlog` (Promote / Keep / Remove) e `BACKLOG.md` opcional. `STATE.md` é o ponteiro de posição. | `sed -n 1,50p $R/gsd-core/gsd-core/templates/roadmap.md; sed -n 1,40p $R/gsd-core/commands/gsd/review-backlog.md; grep -n 'BACKLOG.md\|STATE.md' $R/gsd-core/docs/reference/planning-artifacts.md \| head -4` |
| 3 | **TEM** | `.planning/phases/<NN>-<slug>/` com `<NN>-CONTEXT.md` (decisões da discussão), `RESEARCH.md`, `<NN>-<PP>-PLAN.md`, `SUMMARY.md`, `VERIFICATION.md`, `UAT.md`. | `sed -n 10,40p $R/gsd-core/docs/reference/planning-artifacts.md` |
| 4 | **TEM** | Por plano: `SUMMARY.md` ("Execution record"). Por fase: `VERIFICATION.md` — "checks that what was built matches what was intended ... requirement coverage ... decision coverage". Por milestone: `/gsd-complete-milestone` arquiva roadmap+requirements em `.planning/milestones/`, "PROJECT.md evolved, git tagged"; `RETROSPECTIVE.md` (What Worked / What Was Inefficient / Patterns Established / Key Lessons / Cross-Milestone Trends); `/gsd-extract-learnings` → `LEARNINGS.md`; `/gsd-milestone-summary` → `.planning/reports/`. Promoção para CLAUDE.md: não como passo; o equivalente é `LEARNINGS.md`/`DECISIONS-INDEX.md` lidos pelos workflows. | `sed -n 1,25p $R/gsd-core/commands/gsd/complete-milestone.md; sed -n 1,30p $R/gsd-core/gsd-core/templates/retrospective.md; grep -n 'VERIFICATION.md' $R/gsd-core/docs/explanation/the-phase-loop.md \| head -2` |

Escala: `ls $R/gsd-core/commands/gsd | wc -l` → 72 comandos; `ls $R/gsd-core/gsd-core/templates | wc -l` → 35 templates.

## GSD Pi (`fa83b79`)

**Filosofia declarada** (README/VISION): "a local-first coding agent for planning, implementing, verifying, and tracking project work from the command line ... Local project memory — Store project requirements, decisions, runtime notes, generated plans, summaries, and validation evidence under `.gsd/`". Hierarquia Milestone → Slice → Task. **Fonte de verdade é SQLite** (`.gsd/gsd.db`, gitignored); os `.md` em `.gsd/` são projeções.
Conferir: `sed -n 12,22p $R/gsd-pi/README.md; grep -n 'authoritative runtime' $R/gsd-pi/gitbook/core-concepts/project-structure.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **TEM** | `.gsd/PROJECT.md` — "living description of what the project is": `## What This Is`, `## Core Value`, `## Current State`, `## Milestone Sequence`. `.gsd/REQUIREMENTS.md`: "requirement contract (active/validated/deferred)" com `Out of Scope`. | `sed -n 1,40p $R/gsd-pi/src/resources/extensions/gsd/templates/project.md; grep -n 'PROJECT.md\|REQUIREMENTS.md' $R/gsd-pi/gitbook/core-concepts/project-structure.md` |
| 2 | **TEM** | Milestone com `NN-ROADMAP.md` (Vision, Success Criteria, Key Risks, Proof Strategy; slices `[sketch]` ainda não expandidas), `/gsd backlog` (`add`/`promote`/`remove`/`list`), `/gsd explore` ("Socratic ideation before committing an idea to backlog, knowledge, research, spike, sketch, or a milestone"), `/gsd capture` + `/gsd triage`, `STATE.md`, `QUEUE-ORDER.json` para reordenar milestones. | `sed -n 1,30p $R/gsd-pi/src/resources/extensions/gsd/templates/roadmap.md; grep -n 'gsd backlog\|gsd explore\|gsd capture' $R/gsd-pi/docs/user-docs/commands.md` |
| 3 | **TEM** | `.gsd/phases/<NN-slug>/` com `CONTEXT.md`, `ROADMAP.md`, `PLAN.md`, `SUMMARY.md`, `UAT.md`. | `sed -n 40,60p $R/gsd-pi/gitbook/core-concepts/project-structure.md` |
| 4 | **TEM** | `SUMMARY.md` por task/slice ("what was built and what changed"), `UAT.md`, **Validate Milestone** ("compares roadmap success criteria against actual results, catches gaps before sealing the milestone"), `complete-milestone` com recibo idempotente, `/gsd extract-learnings` ("writes `<MID>-LEARNINGS.md` ... projects reviewable knowledge into `.gsd/KNOWLEDGE.md` ... Runs automatically at milestone completion"), `DECISIONS.md` (registro append-only), `KNOWLEDGE.md` (Rules / Patterns / Lessons Learned — "GSD injects Rules from the file ... at the start of every task": função equivalente ao CLAUDE.md), `/gsd report` (retrospectiva). | `grep -n 'Validate Milestone\|extract-learnings' $R/gsd-pi/docs/user-docs/auto-mode.md $R/gsd-pi/docs/user-docs/commands.md \| head -4; sed -n 1,20p $R/gsd-pi/src/resources/extensions/gsd/templates/knowledge.md` |

## BMAD Method (`f033e70`)

**Filosofia declarada** (README): "Agile Ai Driven Development — turn an idea or change request into working software without giving up the thinking. ... decisions stay explicit, context carries forward, and the process sizes itself to the work. Small changes go straight to build. Complex work gets the depth it needs." Loop: Clarify → Plan → Build and verify → Learn and adjust. Requer `uv`; as skills rodam scripts Python (`render_skill.py`, `memlog.py`, `sprint_plan.py`).
Conferir: `sed -n 8,10p $R/bmad-method/README.md; ls $R/bmad-method/skills | wc -l` → 30 skills

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **TEM** | `bmad-product-brief` → `brief.md` (frontmatter `status`); `bmad-prd` → `prd.md` com intents **Create / Update / Validate**, `status: draft` → `final`, `.memlog.md` append-only de decisões, `addendum.md` com "rejected-alternative rationale". `bmad-project-context` monta o contexto do repo para o agente (`project-context.md`). Caminho de planejamento (help.md): brief ou PRFAQ → PRD → UX → architecture → epics → sprint. | `grep -n 'Create.*Update.*Validate\|status: final' $R/bmad-method/skills/bmad-prd/SKILL.md \| head -3; sed -n 114,120p $R/bmad-method/skills/bmad/references/help.md` |
| 2 | **TEM** (dependências entre stories: não confirmado) | `bmad-create-epics-and-stories` → `epics.md`; `bmad-sprint-planning` → `sprint-status.yaml` com status por epic (`backlog` / `in-progress` / `done`) e por story (`backlog` / `ready-for-dev` / `in-progress` / `review` / `done`), mais `action_items` de retro; `bmad-correct-course` avalia mudança midstream "across the PRD, epics, architecture, and UX" e produz Sprint Change Proposal. Ideia crua: `bmad-brainstorming`, `bmad-forge-idea`. Não achei campo de dependência entre stories no template (`grep -n 'depend' sprint-status-template.yaml` → vazio). | `sed -n 12,40p $R/bmad-method/skills/bmad-sprint-planning/sprint-status-template.yaml; sed -n 1,6p $R/bmad-method/skills/bmad-correct-course/SKILL.md` |
| 3 | **TEM** | Stories como arquivos (`story_location: docs/stories`, `stories/<id>-*.md` com `status` no frontmatter) ou tracker (`bmad-preview-ticketing`); "Durable specs and their story lists live under `{output_folder}/specs`". | `sed -n 158,165p $R/bmad-method/skills/bmad/references/help.md` |
| 4 | **TEM** | `bmad-retrospective`: "Review a completed epic against the evidence it left behind — spec, stories, diffs, commits, sprint status — and produce a retrospective with sourced findings, action items, and an acceptance decision"; grava `RETROSPECTIVE.md`, marca a retro `done` e **acrescenta action items ao `sprint-status.yaml`**. "Fixes and spec reconciliations are *proposed here*, not auto-applied; the human decides." Promoção para CLAUDE.md não é passo do ritual (existe `bmad-project-context` como skill separada). | `sed -n 1,4p $R/bmad-method/skills/bmad-retrospective/SKILL.md; sed -n 99,104p $R/bmad-method/skills/bmad-retrospective/workflow.md` |

## Task Master (`c0c98d3`)

**Filosofia declarada** (README): "A task management system for AI-driven development, designed to work seamlessly with any AI chat." Fonte de verdade: `.taskmaster/tasks/tasks.json` via CLI/MCP.
Conferir: `sed -n 12p $R/claude-task-master/README.md`

| Critério | Veredito | Mecanismo / evidência | Conferir |
|---|---|---|---|
| 1 | **PARCIAL** | O PRD é **entrada**: "Place your PRD document in the `.taskmaster/docs/` directory (e.g., `.taskmaster/docs/prd.txt`)" → `parse-prd` gera tarefas (`--append` para acrescentar). Nada revisa o PRD depois; não há campo de "para quem" nem "fora por decisão" fora do texto livre. | `grep -n 'prd.txt' $R/claude-task-master/docs/tutorial.md \| head -3; grep -n "'--append'" $R/claude-task-master/scripts/modules/commands.js \| head -1` |
| 2 | **PARCIAL** | `tasks.json`: `status` (`pending`, `done`, `deferred` …), `dependencies` (IDs), `priority`; `next` escolhe pela dependência; **tags** isolam contextos (por branch, por feature, `experiment-*`, `mvp`/`v1.0+`). Maturidade + dependência + "deferred" existem por tarefa; não há roadmap em prosa nem visão do produto. | `sed -n 5,20p $R/claude-task-master/docs/task-structure.md; sed -n 52,90p $R/claude-task-master/assets/rules/dev_workflow.mdc` |
| 3 | **TEM** | Tarefa em `tasks.json` + arquivo por tarefa; uma "demanda" grande = tag + PRD próprio (`.taskmaster/docs/feature-xyz-prd.txt` → `parse-prd --tag feature-xyz`). | `sed -n 80,92p $R/claude-task-master/assets/rules/dev_workflow.mdc` |
| 4 | **PARCIAL** | `set-status --status=done`; `update-subtask` "**appends** new information to the existing subtask details, marking it with a timestamp" (o mais perto de "registro do feito", por subtarefa); `update --from=<id>` reescreve tarefas futuras "when implementation differs from original plan" (ajusta o plano, não registra a divergência). Sem arquivamento, retro ou promoção. | `sed -n 100,106p $R/claude-task-master/docs/command-reference.md; grep -n 'implementation differs' $R/claude-task-master/assets/rules/dev_workflow.mdc` |

---

## Por que o Superpowers não tem

Não achei uma frase do autor do tipo "Superpowers não faz gestão de projeto". O que existe é um **padrão consistente de recusas** em issues, mais uma frase no post de lançamento. Discussions do repositório estão desabilitadas (`gh api graphql` → `hasDiscussionsEnabled: false`), então issues são o único canal.

**Post de lançamento** (https://blog.fsck.com/2025/10/09/superpowers/, 2025-10-09): descreve "brainstorm -> plan -> implement" e diz sobre memória: "The pieces of the memory system are all there. I just haven't had time to wire them together." Duas semanas depois memória virou **plugin separado** (episodic-memory, https://blog.fsck.com/2025/10/23/episodic-memory/), e o post não fala de roadmap, PRD ou estado de projeto.

**Issues, com a resposta do mantenedor** (`gh issue view <n> -R obra/superpowers --json state,stateReason,comments`):

| Issue | Pedido | Estado | Resposta de obra (Jesse) |
|---|---|---|---|
| [#1579](https://github.com/obra/superpowers/issues/1579) | skill `writing-prd` entre brainstorming e writing-plans | CLOSED NOT_PLANNED | "After brainstorming, the agent should write a spec document. That *is* this durable artifact." |
| [#1273](https://github.com/obra/superpowers/issues/1273) | Backlog → Changelog tracking | CLOSED | "This feels somewhat out of scope. And I don't feel like superpowers should be enforcing a single issue tracking platform." |
| PR [#880](https://github.com/obra/superpowers/pull/880) (de [#551](https://github.com/obra/superpowers/issues/551), project memory) | memória de projeto entre sessões | fechado | "I don't think that a memory system is a great fit for superpowers. I believe strongly that memory systems are important, but enough people have enough divergent opinions about them that I'm not going to force mine onto every superpowers user." (`gh api repos/obra/superpowers/issues/comments/4375663188 --jq .body`) |
| [#931](https://github.com/obra/superpowers/issues/931) | `/create_handoff` + `/resume_plan` | OPEN | "I've literally never had a problem with just telling superpowers to just continue with the plan in $filename. ... we should never need to add new slash commands. Just talk to the agent." |
| [#1597](https://github.com/obra/superpowers/issues/1597) | RFC: workflow run state + project preferences | CLOSED | "Phases 2 and 3 are speculative — 'workflow run state' and 'project preferences' as standalone concepts without a concrete failure mode to address." |
| [#1238](https://github.com/obra/superpowers/issues/1238) | feature-doc-pack (PLAN/BUSINESS-RULES/API-CONTRACT…) | OPEN | resposta postada por Claude na conta de obra, "Jesse reviewed the finding and approved": "the gap is real - brainstorming writes one spec and writing-plans writes one plan, with no concern-split or role-ownership artifact anywhere. What's missing is the evidence to design against. ... v6.3.0 moved the other way for small work: ceremony now scales down". |
| [#1192](https://github.com/obra/superpowers/issues/1192) | skill `maintaining-roadmap` (`docs/superpowers/roadmap.md` em três tiers, com handoff) | **OPEN, sem resposta de mantenedor** (5 comentários, todos de usuários) | — . O autor da issue diz que mantém o arquivo à mão: "I've been hand-maintaining it for three weeks". Outro: "I wouldn't even call this proposal for enhancement. It's clearly a relevant, missing feature." |
| [#1075](https://github.com/obra/superpowers/issues/1075) | plano/spec sem status depois da execução | **OPEN**, thread canônica (arittr consolidou #789 e #1599 nela) | — |
| [#1515](https://github.com/obra/superpowers/issues/1515) | camada SDD + memória de projeto | CLOSED DUPLICATE | arittr: "the underlying problems are valid. But this issue combines several different product directions"; aponta #551, #601, #1192, #1238 |
| [#2039](https://github.com/obra/superpowers/issues/2039) | passo de handover em finishing-a-development-branch | CLOSED DUPLICATE | arittr: "tracked in #1192, and obra declined the new-slash-commands shape in #931" |
| [#2332](https://github.com/obra/superpowers/issues/2332) | camada durável de QA/acceptance | OPEN | obra: "I need a human written explanation of what you're looking for here." |

(`arittr` fecha e consolida issues; não consegui confirmar a permissão dele — `gh api repos/obra/superpowers/collaborators/arittr/permission` → 403 sem push access.)

**Síntese:** o autor trata a spec por demanda como *o* artefato durável (#1579), recusa impor tracker (#1273) ou sistema de memória (#880), recusa comandos de estado (#931) e pede evidência concreta de falha antes de qualquer camada de estado (#1597, #1238). Nenhum desses é um princípio escrito no README; é uma fronteira que se vê pelo padrão das recusas. Enquanto isso, as issues que pedem exatamente os itens 2 e 4 do aicf (#1192 roadmap, #1075 status pós-execução) continuam abertas e sem resposta do autor.

---

## Afirmações do README/CLAUDE.md do aicf que refutei ou que precisam de nuance

Todas contra os shas desta pesquisa. Trechos do aicf: `sed -n 159,175p README.md` e `grep -n 'GitHub, Linear ou markdown local' CLAUDE.md`.

1. **REFUTADA (imprecisão):** CLAUDE.md diz "o setup dele oferece GitHub, Linear ou markdown local em `.scratch/`" e o README diz "(GitHub Issues, Linear ou markdown local)". No `c55ee46` as opções da Seção A são **GitHub, GitLab, Local markdown, Other** — Linear entra só como "Other (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph". Linear não é opção de primeira classe; GitLab é.
   Conferir: `sed -n 44,47p $R/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`

2. **NUANCE:** "O Superpowers grava plano e design doc no repositório ... e nada pede que sejam revistos contra o que saiu." O **código** é revisto contra o plano a cada tarefa (SDD: "task review (spec compliance + code quality) after each") e há um ledger `<workspace>/progress.md`. O que não acontece é o **documento** ser revisto ou atualizado (issue #1075 aberta). Sugestão de texto: "o código é revisto contra o plano durante a execução, mas o plano e a spec ficam como foram escritos: nada os atualiza com o que saiu".
   Conferir: `sed -n 8p $R/superpowers/skills/subagent-driven-development/SKILL.md`

3. **NUANCE:** "O Superpowers grava spec e plano em arquivo" — só no caminho **Architectural**. Bounded e Spike: "No spec file, no implementation plan document." Para uma demanda pequena, o Superpowers não deixa rastro nenhum além do commit.
   Conferir: `grep -n 'No spec file\|No design' $R/superpowers/skills/brainstorming/SKILL.md`

4. **CONFIRMADA, com nota:** "O `implement` do Matt termina no commit e não fecha o ticket nem marca os critérios de aceite." A skill inteira cabe em cinco linhas e termina em "Commit your work to the current branch." Nota: a skill `implement-spec` (pasta `in-progress/`, fora do plugin) abre um PR "marked as 'closing' the spec issue and tickets" — fechamento via merge, mas não está publicada.
   Conferir: `cat $R/skills/skills/engineering/implement/SKILL.md`

5. **NUANCE:** "Nenhuma das duas tem o documento que diz o que se está construindo, para quem, e o que ficou fora por decisão." Superpowers: confirmado. Matt: "o que ficou fora por decisão" tem casa parcial em `.out-of-scope/<conceito>.md` (triage, "Institutional memory: why a feature was rejected"), e o `wayfinder` tem "Destination" e "Out of scope" por esforço. O que falta mesmo é o "o quê / para quem".
   Conferir: `sed -n 1,10p $R/skills/skills/engineering/triage/OUT-OF-SCOPE.md`

6. **NUANCE:** "elas simplesmente começam na ideia já formulada" e "a ideia que ainda não amadureceu tem registro próprio [no aicf]". Para o Matt, o `wayfinder` começa de "A loose idea ... wrapped in fog" e tem a seção "Not yet specified" no mapa (na issue do tracker) para o que ainda não dá para ticketar. É por esforço, não por produto, mas é registro de ideia imatura.
   Conferir: `sed -n 6p $R/skills/skills/engineering/wayfinder/SKILL.md; grep -n 'Not yet specified' $R/skills/skills/engineering/wayfinder/SKILL.md | head -2`

7. **CONFIRMADA:** "o `brainstorming` ajuda a decompor em subprojetos e trabalha o primeiro; os outros ficam na conversa." Texto literal: "help the user decompose into sub-projects ... Then brainstorm the first sub-project through the normal design flow."
   Conferir: `grep -n 'Then brainstorm the first sub-project' $R/superpowers/skills/brainstorming/SKILL.md`

8. **CONFIRMADA:** "o Matt ... ainda mantém glossário e ADRs" — `domain-modeling` grava `CONTEXT.md` e `docs/adr/`.

---

## Conclusão para o usuário

### (1) Lacuna real ou necessidade inventada?

**Real, e não inventada por você.** Três evidências independentes:

- Nos dois frameworks que o README cita, os itens 1, 2 e 4 não existem (tabela acima), e os usuários do Superpowers pedem exatamente isso nas issues #1192 (roadmap com estado e handoff), #1075 (status do plano depois da execução), #551 (memória de projeto), #2332 (evidência durável de aceite). Um deles diz que mantém `roadmap.md` à mão há três semanas.
- Os frameworks que **têm** a camada (GSD Core, GSD Pi, BMAD) a implementam com artefatos quase idênticos aos seus: `PROJECT.md` do GSD = seu PRD (What This Is / Core Value / Out of Scope com motivo / Key Decisions); `ROADMAP.md` + `phases/` = seu roadmap + specs; `SUMMARY.md` + `VERIFICATION.md` + `complete-milestone` + `extract-learnings` = seu `fechar-demanda`.
- Os mantenedores do openspec estão experimentando, no próprio repositório e sem documentar, um modelo `goal → roadmap → slice → result` onde `result.md` "records what actually happened" — o seu item 4, em construção por quem já tem os itens 3.

### (2) É subentendido e todo mundo faz igual?

**Não.** Ninguém faz "igual sem framework": quem não tem a camada ou a improvisa à mão (issue #1192) ou não tem (o autor do Superpowers diz que "just telling superpowers to just continue with the plan in $filename" basta para ele). Quem tem, tem porque o framework impõe — e impõe junto com o motor de implementação. Não existe hoje um framework que ofereça a governança **sem** ser dono da implementação; é essa combinação que é sua.

### (3) Você está complicando?

Em relação a quem tem a camada, **não**: GSD Core tem 72 comandos e 35 templates; GSD Pi tem SQLite como fonte de verdade e markdown como projeção; BMAD tem 30 skills e scripts Python obrigatórios (`uv`). O aicf tem 6 skills e quatro lugares de escrita (PRD, roadmap/specs, CLAUDE.md, ADR/CONTEXT).

Em relação a quem não tem, **sim, um pouco** — e os pontos onde os leves resolveram com menos são referência útil:
- spec-kit resolve "roadmap" com **um arquivo markdown e nenhuma ferramenta** (`docs/concepts/spec-of-specs.md`: tabela ID / intent / scope boundary / depends on / status / link). Se o seu roadmap é mais que isso, vale perguntar por quê.
- O aicf carrega dois mecanismos de mídia (arquivo e issue) — o próprio lema do repositório marca "dois mecanismos coexistindo" como gatilho de revisão. O Matt faz o mesmo (GitHub / GitLab / local / other), então não é exótico, mas é a parte que mais custa manter.

### (4) O que os outros fazem que o aicf não faz, e vice-versa

**Eles fazem, o aicf não:**
- **Requisitos com ID e rastreabilidade** (GSD `REQUIREMENTS.md` AUTH-01 → fase; spec-kit FR-###/SC-###; gsd-pi contrato active/validated/deferred). O PRD do aicf não tem unidade checável abaixo da demanda.
- **Verificação separada do relatório** (GSD `VERIFICATION.md` + `UAT.md`; gsd-pi Validate Milestone; BMAD "acceptance decision" na retro; spec-kit `converge`). No aicf o relatório de fechamento acumula as duas funções.
- **Registro de decisões como tabela append-only** (gsd-pi `DECISIONS.md`; GSD `Key Decisions` no PROJECT.md). O aicf usa ADR, que é mais pesado por decisão e por isso captura menos.
- **Fonte de verdade de comportamento atual** (openspec `specs/`, com merge no archive). O PRD do aicf diz o porquê; nada no aicf diz "o que o sistema faz hoje" além do código.
- **Estado legível por máquina** (`STATE.md`, `sprint-status.yaml`, `tasks.json`). O aicf usa pasta/label; é mais simples e mais frágil.
- **Retrospectiva entre milestones** (GSD `RETROSPECTIVE.md` com "Cross-Milestone Trends").

**O aicf faz, eles não:**
- **Governança agnóstica do caminho de implementação.** GSD e BMAD são donos da execução; spec-kit, openspec e task-master são donos do planejamento da demanda. Nenhum aceita "rode o Superpowers ou o Matt dentro da fase". É o seu diferencial e é o que o próprio Matt aponta como problema dos outros ("they take away your control").
- **Promoção do aprendizado para CLAUDE.md/ADR/glossário como passo do ritual.** GSD extrai para `LEARNINGS.md` e gsd-pi injeta `KNOWLEDGE.md` em toda task (função equivalente, mecanismo próprio); BMAD só *propõe* action items; os outros não têm nada. Nenhum escreve no `CLAUDE.md` como regra de fechamento.
- **Relatório plano × entrega na própria demanda.** O mais perto é `SUMMARY.md`+`VERIFICATION.md` do GSD (dois arquivos, por plano/fase) e o `result.md` experimental do openspec.

**Onde o aicf duplica:** a camada de governança do GSD Core (`.planning/PROJECT.md`, `ROADMAP.md`, `phases/`, `complete-milestone`, `extract-learnings`). Dito sem rodeio: o aicf é a pasta `.planning/` do GSD sem o loop de execução do GSD, e plugável a Superpowers/Matt. Isso é uma posição legítima — o seu PRD argumenta que o loop é o que se burla no meio do projeto — mas o README hoje compara só com Superpowers e Matt, e o leitor que conhece GSD vai perguntar "por que não o GSD?". A resposta existe (o GSD é dono da implementação; 72 comandos; não aceita outro caminho), e vale estar escrita.
