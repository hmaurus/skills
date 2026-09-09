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

**Integração e fechamento são coisas diferentes.** _Integração_ é decidir o destino do código —
merge na base, PR, ou a branch fica. É o último passo da **implementação**, e pertence ao método
escolhido. _Fechamento_ é o registro da demanda — relatório, `specs/concluidas/`, checklist,
promoção de conhecimento. É `/aicf:fechar-demanda`, e nada além. **O método fecha o código, a
governança fecha a demanda — e a segunda só começa depois da primeira.**

**Entrevista e implementação são escolhas independentes. Na entrevista, o caminho é pergunta ao
usuário; na implementação, o agente segue a sugestão gravada na spec quando o caso é óbvio —
caminho aicf direto e diff que cabe numa frase — e pergunta com opções nos demais.** O agente
sugere pelo ponto forte que couber ao caso; a decisão é do usuário quando há escolha real, e o
caminho seguido vira a linha `Processo` na demanda.

**A governança escolhe o caminho de cada fase; dentro da fase, o encadeamento do framework roda
inteiro.** Skill que o método declara como passo seguinte dentro da mesma fase não se pula nem se
substitui — no Superpowers, `executing-plans` e `subagent-driven-development` declaram
`finishing-a-development-branch` como `REQUIRED SUB-SKILL`: ela roda automaticamente, sem
perguntar, e o agente conta em uma linha o que ficou decidido. Interferir ali degrada a qualidade
de um processo que não é nosso. Na **passagem entre fases** quem decide é a governança, mesmo
quando o framework recomenda continuar nele: o `brainstorming` declara `writing-plans` como estado
terminal, e ainda assim parar na fronteira é legítimo — o design doc dele vale como spec, e a
implementação é escolha nova.

## Governança — onde mora o quê

```
docs/projeto/
├── PRD.md             # Visão, público, modelo de negócio — o porquê do produto
├── CHECKLIST.md       # Índice: cada seção espelha uma pasta abaixo (+ Fundação e Backlog)
├── intents/
│   ├── <intent>.md        # Decidida, ainda não entrevistada
│   └── backlog/           # Ainda não está claro que será feita
└── specs/
    ├── <spec>.md          # Pronta para implementar
    └── concluidas/        # Arquivadas, com relatório
```

Só governança de demanda entra aí. Doc que descreve o mundo em vez de um trabalho a fazer —
configuração, ID externo, decisão de marca, número de negócio, aprendizado — vai para fora de
`docs/projeto/`, e a raiz de `docs/` basta até haver arquivo suficiente para uma pasta de domínio.

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

| Caminho            | Como                                                       | Plano de implementação                          | Integração                                          |
| ------------------ | ---------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Aicf direto**    | `/aicf:implementar-spec`                                   | depende do agente                               | o agente, pelo critério de workspace abaixo         |
| **Aicf plan mode** | plan mode ligado antes, ou escolhido no `implementar-spec` | depende do agente                               | o agente, pelo critério de workspace abaixo         |
| **Superpowers**    | `writing-plans`, depois `subagent-driven-development`      | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` | `finishing-a-development-branch`, encadeada e automática |
| **Matt Pocock**    | `to-tickets`, depois `implement`                           | tickets, com bloqueio declarado entre eles      | o próprio `implement`: `/code-review` e commit na branch atual |

Descer a tabela troca velocidade por rastro: nos caminhos aicf o plano vive na sessão e morre
com ela. As skills do Matt (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`)
exigem `/setup-matt-pocock-skills` rodado no repositório.

No Superpowers, os headings de tarefa do plano ficam em inglês (`## Task 3`) mesmo com o corpo em
português: `scripts/task-brief` procura `^#+ Task N` e responde `task N not found` para "Tarefa N".

**Branch, ou worktree.** O default é commitar direto na branch de trabalho — processo prático para
dev solo, com PR para o que a complexidade ou o risco justificarem. O agente **avalia** em vez de
herdar o default em silêncio: branch própria ou worktree quando a demanda é grande ou se quer poder
descartá-la em bloco; **contra worktree quando a verificação depende de estado local não
versionado** — banco, arquivo de dados, `.env`, qualquer coisa em pasta gitignored: a worktree
nasce sem eles. A avaliação acontece no `implementar-spec`, junto da escolha de caminho; o agente
diz numa linha o que decidiu e por quê, e sair do default é pergunta ao usuário.

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
separadas**, agrupadas sob um subtítulo dentro de `Em andamento` — seção nova quebraria os pares
que o fechamento confere; a relação mora na lista, não em
campo de cada spec nem em subpasta. O _porquê_ das decisões mora no arquivo, não na conversa.
