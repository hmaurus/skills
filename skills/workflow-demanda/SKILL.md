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

Estas skills são deliberadamente pequenas: dizem o que o agente não teria como inferir — onde
gravar, o que registrar, quando fechar — e param aí. Ausência de instrução é liberdade, não
lacuna: o que a ferramenta nativa já faz bem e o que se decide melhor no caso concreto ficam
com o agente. Quanto mais a skill descreve, mais ela precisa ser reescrita a cada evolução dele.

## O ciclo

**Demanda** (item do checklist, arquivo em `demandas/`, ou ideia ainda não registrada) →
**entrevista**, que produz a spec → **implementação**, que a consome → **fechamento**, que é
`/aicf:fechar-demanda` — relatório, arquivamento e linha `Processo:` vivem lá, e o agente o
aplica em qualquer caminho. Demanda que já nasceu de entrevista volta à mesa: o agente diz se o
registrado basta ou se vale outra rodada. Pular a entrevista é legítimo quando a demanda já diz
o suficiente — a implementação a consome como está, e a linha `Processo:` fica sem seta.

**Entrevista e implementação são escolhas independentes, e ambas são pergunta ao usuário, não
dedução**: o agente sugere pelo ponto forte que couber ao caso, e a resposta vira a linha
`Processo:` na demanda.

## Governança — onde mora o quê

```
docs/projeto/
├── PRD.md             # Visão, público, modelo de negócio — o porquê do produto
├── CHECKLIST.md       # O entregue e o que falta (+ Backlog); cada item é uma demanda em potencial
└── demandas/
    ├── <demanda>.md       # Item que precisa de mais que uma linha no checklist
    ├── PLANO-<titulo>.md  # Plano ativo (conjunto de demandas)
    ├── concluidas/        # Demandas e planos concluídos, com relatório
    └── backlog/           # Ainda não está claro que será feita
```

Se houver um `CLAUDE.md` em `docs/projeto/`, ele manda sobre essa estrutura. Se o repositório
nem tem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

`demandas/` ou `backlog/` se decide por **certeza, não urgência**: `demandas/` é o que já foi
decidido fazer, mesmo que não seja agora; `backlog/` é o que ainda não se sustenta, depende de
decisão não tomada, ou o usuário nem sabe se quer — ideia que nunca sai de lá é uso legítimo.
Importa mais quando a ideia surge no meio de outra demanda: registrar o esboço, escolher a pasta
e voltar imediatamente ao que estava sendo feito.

## Entrevista — produz a spec

| Caminho         | Como                                | A spec fica em                                         |
| --------------- | ----------------------------------- | ------------------------------------------------------ |
| **Nativo**      | `/aicf:criar-spec`                  | `demandas/<nome>.md`                                   |
| **Superpowers** | `brainstorming`                     | `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md` |
| **Matt Pocock** | `grill-with-docs`, depois `to-spec` | issue no tracker                                       |

No Matt, `grill-with-docs` interroga e grava glossário e ADRs pelo caminho, mas quem escreve e
publica a spec é `to-spec`; emendando direto no `implement`, a spec não vira arquivo nem issue —
fica só na janela de contexto.

## Implementação — consome a spec

| Caminho              | Como                                                    | Plano de implementação                          |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| **Nativo direto**    | `/aicf:implementar-spec`                                | depende do agente                               |
| **Nativo plan mode** | plan mode ligado, depois `/aicf:implementar-spec`       | depende do agente                               |
| **Superpowers**      | `writing-plans`, depois `subagent-driven-development`   | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` |
| **Matt Pocock**      | `to-tickets`, depois `implement`                        | tickets, com bloqueio declarado entre eles      |

Descer a tabela troca velocidade por rastro: nos caminhos nativos o plano vive na sessão e morre
com ela. Plan mode liga com `Shift+Tab` **antes** de chamar a skill (`Ctrl+G` abre o plano no
editor). As skills do Matt (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`)
exigem `/setup-matt-pocock-skills` rodado no repositório.

## Trabalho recorrente não é demanda

Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir (publicar
conteúdo, subir versão, disparar email, liberar acesso) vira **skill** ou **command** em
`.claude/`. Gatilho: o mesmo passo a passo explicado pela terceira vez — quando acontecer, propor
a criação.

## Checklists e PLANOs multi-demanda

O checklist e os PLANOs (`demandas/PLANO-*.md`) consolidam várias demandas — o ideal, sem ser
regra rígida, é cada uma rodar em **sessão própria**, com `/clear` ou `/compact` entre elas.
**Cada demanda no doc é auto-contida** (Problema, Solução, DoD): a próxima sessão lê o doc,
escolhe, executa. O _porquê_ das decisões mora no doc, não na conversa; a **Origem** da leva
fica no cabeçalho do plano, uma vez.

Demanda que não coube na sessão não vira prompt de continuação: fecha parcial, com o estado
gravado no próprio doc — `/aicf:fechar-demanda` cobre o caso.
