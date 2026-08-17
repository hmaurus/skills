# aicf — governança de projeto para desenvolver com agentes

_[English version](README.en.md)_

Um kit inicial para tocar um projeto de software com Claude Code: a estrutura de documentos que sustenta o projeto — visão, checklist de entregas, demandas versionadas — e o ciclo que leva cada demanda da ideia ao registro do que foi feito.

## Onde ele entra

Coleções de skills como [Superpowers](https://github.com/obra/superpowers) e as [do Matt Pocock](https://github.com/mattpocock/skills) resolvem bem **a demanda individual**: interrogam a ideia, produzem uma spec, quebram em tarefas, executam com disciplina. O Matt vai além e cobre conhecimento de domínio — glossário em `CONTEXT.md`, decisões em ADRs.

O que nenhuma das duas traz é a camada acima: **onde está escrito o que o produto é, o que já foi entregue, o que falta, e o histórico do que foi decidido e por quê.** Sem ela, cada demanda é bem executada e o projeto inteiro não tem memória.

O `aicf` é essa camada — e funciona de dois jeitos:

- **Sozinho**, com um caminho nativo próprio para entrevista e implementação, sem instalar mais nada.
- **Por cima**, se você já usa as outras. Entreviste pelo `brainstorming` do Superpowers ou pelo `grill-with-docs` do Matt: o registro continua caindo no mesmo lugar, e a demanda anota qual caminho foi usado.

## Instalação

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Reinicie a sessão depois de instalar — skills carregam no início e não trocam a quente.

Em projeto novo, comece por `/aicf:setup`, que cria a estrutura e o `CLAUDE.md` raiz. Em projeto que já existe, comece por `/aicf:workflow-demanda`, que explica o ciclo.

## As skills

| Skill                    | Quando                     | O que faz                                                                        |
| ------------------------ | -------------------------- | -------------------------------------------------------------------------------- |
| `/aicf:setup`            | uma vez, no projeto novo   | Cria `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz |
| `/aicf:workflow-demanda` | o mapa                     | O ciclo inteiro, os caminhos de cada fase e as convenções de governança          |
| `/aicf:criar-spec`       | fase de entrevista         | Interroga até não sobrar decisão em aberto, depois escreve a spec no repositório  |
| `/aicf:implementar-spec` | fase de implementação      | Lê a spec, implementa, verifica e conduz o fechamento até o registro              |

## O problema que isso resolve

Sessão de agente é volátil. A conversa em que você decidiu **não** usar uma abordagem some no `/clear`, e três semanas depois alguém — humano ou agente — reabre a mesma discussão porque o motivo nunca foi escrito em lugar nenhum.

O ciclo tem quatro fases:

1. **Demanda** — o que se quer, ainda cru
2. **Entrevista** — amadurece a demanda e produz a spec
3. **Implementação** — consome a spec
4. **Fechamento** — relatório do que foi feito **de fato**, com as divergências plano×entrega

O que amarra tudo é o registro: cada demanda vira um arquivo no repositório, e ao concluir ganha um relatório e vai para `concluidas/`. O porquê mora no repo, não na conversa.

## Caminhos, não trilho único

As fases 2 e 3 são independentes, e a escolha é do usuário — o agente sugere, não decide:

- **Entrevista** — `/aicf:criar-spec`, ou `brainstorming` (Superpowers), ou `grill-with-docs` + `to-spec` (Matt Pocock)
- **Implementação** — `/aicf:implementar-spec` (com ou sem plan mode), ou `writing-plans` + `subagent-driven-development`, ou `to-tickets` + `implement`

Dá para entrevistar por um caminho e implementar por outro. A demanda registra qual foi usado, numa linha `Processo:`.

## A estrutura

```
docs/projeto/
├── PRD.md             # o porquê do produto: visão, público, modelo
├── CHECKLIST.md       # o que foi entregue e o que falta
└── demandas/
    ├── <demanda>.md   # uma demanda por arquivo
    ├── concluidas/    # arquivadas, com relatório
    └── backlog/       # ainda não está claro que serão feitas
```

Se o seu projeto precisar de outra estrutura, escreva as diferenças num `CLAUDE.md` dentro de `docs/projeto/` — o Claude Code carrega esse arquivo ao tocar a pasta, e **instrução do projeto tem precedência sobre a da skill**. É assim que um repositório adota o método sem forkar as skills.

## Sobre

Feito para o curso [Claude Code: Criador de Apps](https://aicodingflow.com/curso), do [AI Coding Flow](https://aicodingflow.com). Use à vontade, com ou sem o curso.

MIT.
