---
name: workflow-demanda
description: O mapa de uma demanda — ciclo, caminhos de entrevista e implementação, convenções de governança em docs/projeto/. Consultar ao começar, triar ou registrar uma demanda. O fechamento vive em fechar-demanda.
---

# Workflow de uma demanda

O trabalho tem duas camadas. A **governança** — registro, ritual de fechamento e checks — é
obrigatória e sempre a mesma. A **implementação** é roteiro, não trilho: se o caso pedir outra
coisa, o caso ganha. Ao sair do roteiro (pular etapa, trocar de caminho no meio, usar ferramenta
que a skill não cita), **dizer em uma linha o que vai fazer e por quê**, antes de fazer.
Ferramenta do agente — subagente, plan mode, worktree, code review, busca paralela — é escolha
livre em qualquer ponto, e o agente propõe a que couber sem esperar autorização.

## O ciclo

**Demanda** (item do checklist, arquivo em `intents/`, ou ideia ainda não registrada) →
**entrevista**, que produz a spec → **implementação**, que a consome → **fechamento**, que é
`/aicf:fechar-demanda` — relatório, arquivamento e linha `Processo` vivem lá, e o agente o
aplica em qualquer caminho. Demanda que já nasceu de entrevista volta à mesa: o agente diz se o
registrado basta ou se vale outra rodada. Pular a entrevista é legítimo quando a demanda já diz
o suficiente — o arquivo vai de `intents/` para `specs/` como está, e a linha `Processo` registra
`entrevista: nenhuma`.

**Três palavras, uma unidade de trabalho.** _Demanda_ é a coisa a fazer. _Intent_ e _spec_ são
os dois estados do arquivo que a descreve: intent é a demanda decidida e ainda não entrevistada;
spec é a demanda pronta para implementar. A pasta diz em qual estado o arquivo está.

**Entrevista e implementação são escolhas independentes. Na entrevista, o caminho é pergunta ao
usuário; na implementação, o agente segue a sugestão gravada na spec quando o caso é óbvio —
caminho aicf direto e diff que cabe numa frase — e pergunta com opções nos demais.** O agente
sugere pelo ponto forte que couber ao caso; a decisão é do usuário quando há escolha real, e o
caminho seguido vira a linha `Processo` na demanda.

## Governança — onde mora o quê

```
docs/projeto/
├── PRD.md             # Visão, público, modelo de negócio — o porquê do produto
├── CHECKLIST.md       # O entregue e o que falta (+ Backlog); cada item é uma demanda em potencial
├── intents/
│   ├── <intent>.md        # Decidida, ainda não entrevistada
│   └── backlog/           # Ainda não está claro que será feita
└── specs/
    ├── <spec>.md          # Pronta para implementar
    └── concluidas/        # Arquivadas, com relatório
```

Se o repositório nem tem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

`intents/` ou `intents/backlog/` se decide por **certeza, não urgência**: `intents/` é o que já
foi decidido fazer, mesmo que não seja agora; `backlog/` é o que ainda não se sustenta, depende
de decisão não tomada, ou o usuário nem sabe se quer — ideia que nunca sai de lá é uso legítimo.
Importa mais quando a ideia surge no meio de outra demanda: registrar o esboço, escolher a pasta
e voltar imediatamente ao que estava sendo feito.

Um caminho só: todo intent que vai ser feito vira spec — com entrevista ou sem —, e tudo termina
em `specs/concluidas/`, inclusive o que a entrevista concluiu não fazer.

## Entrevista — produz a spec

| Caminho         | Como                                | A spec fica em                                                                                                      |
| --------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Aicf**        | `/aicf:criar-spec`                  | `specs/<nome>.md` — o intent movido                                                                                 |
| **Superpowers** | `brainstorming`                     | `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md`, só no caminho _architectural_; ou `specs/<nome>.md`, se o projeto mandar |
| **Matt Pocock** | `grill-with-docs`, depois `to-spec` | issue no tracker; ou `specs/<nome>.md`, se o tracker configurado no setup apontar para lá                           |

No Superpowers, só o caminho _architectural_ do `brainstorming` grava arquivo, e ele honra o
local que o `CLAUDE.md` do projeto mandar. No Matt, quem grava a spec é `to-spec`; emendar
direto no `implement` deixa a spec só na janela de contexto.

## Implementação — consome a spec

| Caminho              | Como                                                    | Plano de implementação                          |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| **Aicf direto**      | `/aicf:implementar-spec`                                | depende do agente                               |
| **Aicf plan mode**   | plan mode ligado antes, ou escolhido no `implementar-spec` | depende do agente                            |
| **Superpowers**      | `writing-plans`, depois `subagent-driven-development`   | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` |
| **Matt Pocock**      | `to-tickets`, depois `implement`                        | tickets, com bloqueio declarado entre eles      |

Descer a tabela troca velocidade por rastro: nos caminhos aicf o plano vive na sessão e morre
com ela. As skills do Matt (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`)
exigem `/setup-matt-pocock-skills` rodado no repositório.

## Trabalho recorrente não é demanda

Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir (publicar
conteúdo, subir versão, disparar email, liberar acesso) vira **skill** ou **command** em
`.claude/`. Gatilho: o mesmo passo a passo explicado pela terceira vez — quando acontecer, propor
a criação. Mas skill é conselho que o modelo pode não seguir: regra que precisa valer sem exceção
— formatar após editar, barrar escrita em pasta protegida — é **hook**, script que roda sempre. O
critério é a regra poder falhar sem ninguém perceber.

## Demanda grande, e demandas que andam juntas

Demanda grande demais para uma sessão é **uma spec só**, com as entregas em checkboxes no corpo:
a sessão faz o que cabe e fecha parcial — `/aicf:fechar-demanda` cobre o caso — e a próxima
continua pelo mesmo arquivo. Várias demandas independentes que andam juntas são **specs
separadas**, agrupadas sob um título de seção no `CHECKLIST.md`; a relação mora na lista, não em
campo de cada spec nem em subpasta. O _porquê_ das decisões mora no arquivo, não na conversa.
