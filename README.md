# aicf — governança de projeto para desenvolver com agentes

_[English version](README.en.md)_

Um kit inicial para tocar um projeto de software com Claude Code: a estrutura de documentos que sustenta o projeto — visão, checklist de entregas, demandas versionadas — e o ciclo que leva cada demanda da ideia ao registro do que foi feito.

## Onde ele entra

Coleções de skills como [Superpowers](https://github.com/obra/superpowers) e as [do Matt Pocock](https://github.com/mattpocock/skills) resolvem bem **a demanda individual**: interrogam a ideia, produzem uma spec, quebram em tarefas, executam com disciplina. E deixam rastro — o Superpowers grava spec e plano em arquivo; o Matt publica spec e tickets no issue tracker e ainda mantém glossário e ADRs.

Só que esse rastro é **por demanda** e escrito **antes** da execução. Duas coisas ficam de fora:

- **O nível do produto.** Nenhum dos dois tem o documento que diz o que se está construindo, para quem, e o que ficou fora por decisão — nem a lista única do que já foi entregue e do que falta. Vinte specs bem escritas não respondem "onde o projeto está".
- **O depois.** Spec e plano dizem o que se pretendia. O que de fato saiu, onde a entrega divergiu do plano e por quê, só existe se alguém escrever ao fechar — e nenhum dos dois pipelines pede isso.

O `aicf` é essa camada — e funciona de dois jeitos:

- **Sozinho**, com um caminho nativo próprio para entrevista e implementação, sem instalar mais nada.
- **Por cima**, se você já usa as outras. Entreviste pelo `brainstorming` do Superpowers ou pelo `grill-with-docs` do Matt: o registro continua caindo no mesmo lugar, e a demanda anota qual caminho foi usado.

## Instalação

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Reinicie a sessão depois de instalar — skills carregam no início e não trocam a quente.

Em projeto que já existe, comece por `/aicf:workflow-demanda`, que explica o ciclo.

## Começando um projeto novo

**1. `/aicf:setup`** — cria `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz. Pergunta pouco: o nome, uma ou duas frases sobre o projeto, onde ficam os padrões de engenharia e quais ferramentas você já usa.

**2. Preencher o `PRD.md`.** Ele nasce com as seções e uma pergunta em cada uma. A que mais se paga é **"fora de escopo, por decisão"** — é ela que impede a mesma discussão de voltar daqui a seis meses.

Não há skill dedicada a isso, aqui nem nas outras coleções. Três caminhos funcionam:

- **Entrevista em linguagem natural** — _"me entreviste seção por seção para preencher o `docs/projeto/PRD.md`"_. É o padrão quando a ideia ainda está se formando: pergunta aberta abre espaço que menu de opção fecha.
- **`grilling`** (Matt Pocock) — quando você já acha que sabe o que quer e prefere ser contestado antes de escrever. Ela não grava nada; o resultado da conversa você transcreve para o PRD.
- **`domain-modeling`** (Matt Pocock) — depois, se o produto tem vocabulário próprio que já apareceu ambíguo. Grava o glossário em `CONTEXT.md`, ao lado do PRD e não dentro dele.

**O que não funciona é passar o PRD pelo ciclo da demanda.** Não por ser documento — spec serve bem para mudança de documentação. É que a spec descreve uma **mudança**, com escopo e um estado "pronto", enquanto o PRD descreve o **produto**, e é revisado toda vez que uma decisão o contraria. Envelopar um no outro rende uma spec vazia — a entrevista dela discutiria como escrever o arquivo, e as perguntas que importam, público e fora de escopo, continuariam sem resposta — mais um fechamento pedindo relatório, arquivamento e check de lint num `.md`.

**3. Tirar o `CHECKLIST.md` do PRD.** Cada coisa que o produto precisa ter vira uma linha. O que couber numa linha fica ali mesmo; o que precisar de contexto vira arquivo em `demandas/`.

**4. Primeira demanda.** `/aicf:criar-spec` para amadurecer, `/aicf:implementar-spec` para executar e fechar. Daí em diante o ciclo se repete.

## As skills

| Skill                    | Quando                     | O que faz                                                                        |
| ------------------------ | -------------------------- | -------------------------------------------------------------------------------- |
| `/aicf:setup`            | uma vez, no projeto novo   | Cria `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz — e, se você quiser, os padrões de engenharia |
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
