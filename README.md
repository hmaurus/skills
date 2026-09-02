# aicf — governança de projeto para desenvolver com agentes

_[English version](README.en.md)_

Um kit inicial para tocar um projeto de software com Claude Code: a estrutura de documentos que sustenta o projeto — visão, checklist de entregas, demandas versionadas — e o ciclo que leva cada demanda da ideia ao registro do que foi feito. Ele cuida da **governança** e do **planejamento macro**, que as coleções de skills de engenharia deixam de fora, e é **agnóstico** quanto ao caminho de implementação: a governança é a mesma quer a demanda seja entrevistada e implementada pelo caminho nativo, pelo Superpowers ou pelas skills do Matt Pocock.

## Onde ele entra

Coleções de skills como [Superpowers](https://github.com/obra/superpowers) e as [do Matt Pocock](https://github.com/mattpocock/skills) resolvem bem **a demanda individual**: interrogam a ideia, produzem uma spec, quebram em tarefas, executam com disciplina. E deixam rastro — o Superpowers grava spec e plano em arquivo; o Matt publica spec e tickets no issue tracker e ainda mantém glossário e ADRs.

Só que esse rastro é **por demanda** e escrito **antes** da execução. Três coisas ficam de fora, e nenhuma das duas coleções declara que elas são problema de outra pessoa — elas simplesmente começam na ideia já formulada e terminam no commit ou no merge:

- **O nível do produto.** Nenhuma das duas tem o documento que diz o que se está construindo, para quem, e o que ficou fora por decisão — nem a lista única do que já foi entregue e do que falta. Vinte specs bem escritas não respondem "onde o projeto está".
- **O planejamento macro.** Quando o pedido é grande demais para uma spec, o `brainstorming` do Superpowers ajuda a decompor em subprojetos e trabalha o primeiro; os outros ficam na conversa. Aqui a ideia que ainda não amadureceu tem arquivo próprio, o conjunto de demandas que anda junto aparece agrupado no checklist, e o que ainda não se sabe se será feito tem lugar para esperar sem se perder.
- **O depois.** Spec e plano dizem o que se pretendia. O que de fato saiu, onde a entrega divergiu do plano e por quê, só existe se alguém escrever ao fechar. O `implement` do Matt termina no commit e não fecha o ticket nem marca os critérios de aceite; o Superpowers lista as decisões que tomou por conta própria na mensagem final e apaga a pasta de trabalho, porque a partir dali o histórico do git é o registro. O `aicf` pede um relatório no arquivo da demanda, e é nele que a divergência plano×entrega fica escrita.

O `aicf` é essa camada, e a mesma camada vale para qualquer caminho de implementação. Ele funciona de dois jeitos:

- **Sozinho**, com um caminho nativo próprio para entrevista e implementação, sem instalar mais nada.
- **Por cima**, se você já usa as outras. Entreviste pelo `brainstorming` do Superpowers ou pelo `grill-with-docs` do Matt, implemente por `subagent-driven-development` ou por `to-tickets` + `implement`: o registro continua caindo no mesmo lugar, o fechamento é o mesmo, e a demanda anota qual caminho foi usado. Trocar de coleção, ou misturar as duas numa mesma demanda, não muda nada na governança.

## Instalação

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Reinicie a sessão depois de instalar — skills carregam no início e não trocam a quente.

Em projeto que já existe, comece por `/aicf:workflow-demanda`, que explica o ciclo.

## Começando um projeto novo

**1. `/aicf:setup`** — cria `docs/projeto/` com PRD e checklist, as pastas de intents e specs e o `CLAUDE.md` raiz. Pergunta pouco: o nome, uma ou duas frases sobre o projeto, onde ficam os padrões de engenharia e quais ferramentas você já usa.

**2. Preencher o `PRD.md`.** Ele nasce com as seções e uma pergunta em cada uma. A que mais se paga é **"fora de escopo, por decisão"** — é ela que impede a mesma discussão de voltar daqui a seis meses.

**`/aicf:criar-prd`** entrevista você seção por seção e escreve o arquivo. Começa pelo problema, não pela solução, e não deixa o "fora de escopo" passar em branco. Dois complementos, quando fizerem falta:

- **`grilling`** (Matt Pocock) — antes, se você já acha que sabe o que quer e prefere ser contestado. Ela não grava nada; o resultado da conversa entra na entrevista do PRD.
- **`domain-modeling`** (Matt Pocock) — depois, se o produto tem vocabulário próprio que já apareceu ambíguo. Grava o glossário em `CONTEXT.md`, ao lado do PRD e não dentro dele.

**O que não funciona é passar o PRD pelo ciclo da demanda.** Não por ser documento — spec serve bem para mudança de documentação. É que a spec descreve uma **mudança**, com escopo e um estado "pronto", enquanto o PRD descreve o **produto**, e é revisado toda vez que uma decisão o contraria. Envelopar um no outro rende uma spec vazia — a entrevista dela discutiria como escrever o arquivo, e as perguntas que importam, público e fora de escopo, continuariam sem resposta — mais um fechamento pedindo relatório, arquivamento e check de lint num `.md`.

**3. Tirar o `CHECKLIST.md` do PRD.** Cada coisa que o produto precisa ter vira uma linha. O que couber numa linha fica ali mesmo; o que precisar de contexto vira arquivo em `intents/`.

**4. Primeira demanda.** `/aicf:criar-spec` para amadurecer, `/aicf:implementar-spec` para executar e fechar. Daí em diante o ciclo se repete.

## As skills

| Skill                    | Quando                     | O que faz                                                                        |
| ------------------------ | -------------------------- | -------------------------------------------------------------------------------- |
| `/aicf:setup`            | uma vez, no projeto novo   | Cria `docs/projeto/` com PRD e checklist, as pastas de intents e specs, o `CLAUDE.md` (com `AGENTS.md` apontando para ele) e um `README.md` — e, se você quiser, os padrões de engenharia |
| `/aicf:criar-prd`        | começo do projeto          | Entrevista sobre o produto e escreve o `PRD.md` — roda de novo quando uma decisão o contraria |
| `/aicf:workflow-demanda` | o mapa                     | O ciclo, os caminhos de cada fase e as convenções de governança                   |
| `/aicf:criar-spec`       | fase de entrevista         | Interroga até não sobrar decisão em aberto, depois escreve a spec no repositório  |
| `/aicf:implementar-spec` | fase de implementação      | Lê a spec, implementa e verifica; ao final chama o fechamento                     |
| `/aicf:fechar-demanda`   | fase de fechamento         | Checks, relatório, arquivamento e promoção de conhecimento — o agente a aplica ao concluir qualquer demanda, por qualquer caminho |

## O problema que isso resolve

Sessão de agente é volátil. A conversa em que você decidiu **não** usar uma abordagem some no `/clear`, e três semanas depois alguém — humano ou agente — reabre a mesma discussão porque o motivo nunca foi escrito em lugar nenhum.

O ciclo tem quatro fases:

1. **Demanda** — o que se quer, ainda cru
2. **Entrevista** — amadurece a demanda e produz a spec
3. **Implementação** — consome a spec
4. **Fechamento** — relatório do que foi feito **de fato**, com as divergências plano×entrega

O que amarra tudo é o registro: cada demanda vira um arquivo no repositório, e ao concluir ganha um relatório e vai para `specs/concluidas/`. O porquê mora no repo, não na conversa.

## Caminhos, não trilho único

As fases 2 e 3 são independentes, e a escolha é do usuário — o agente sugere, não decide:

- **Entrevista** — `/aicf:criar-spec`, ou `brainstorming` (Superpowers), ou `grill-with-docs` + `to-spec` (Matt Pocock)
- **Implementação** — `/aicf:implementar-spec` (com ou sem plan mode), ou `writing-plans` + `subagent-driven-development`, ou `to-tickets` + `implement`

Dá para entrevistar por um caminho e implementar por outro. A demanda registra qual foi usado, numa linha `Processo`.

## A estrutura

```
docs/projeto/
├── PRD.md             # o porquê do produto: visão, público, modelo
├── CHECKLIST.md       # o que foi entregue e o que falta
├── intents/
│   ├── <intent>.md    # decidida, ainda não entrevistada
│   └── backlog/       # ainda não está claro que será feita
└── specs/
    ├── <spec>.md      # pronta para implementar
    └── concluidas/    # arquivadas, com relatório
```

A pasta diz a maturidade do documento. Uma demanda é a unidade de trabalho; o arquivo que a descreve nasce como **intent** (decidida, ainda não entrevistada), vira **spec** quando está pronta para implementar — o mesmo arquivo, movido — e termina em `specs/concluidas/` com o relatório. `intents/backlog/` é para o que ainda não se sabe se será feito.

Se o seu projeto precisar de outra estrutura, escreva a diferença no `CLAUDE.md` da raiz ou em `.claude/rules/`, nunca num `CLAUDE.md` dentro de `docs/projeto/`: `CLAUDE.md` de subpasta só entra no contexto quando o agente lê um arquivo daquela pasta, e registrar uma demanda nova não exige isso.

## Sobre

Feito para o curso [Claude Code: Criador de Apps](https://aicodingflow.com/curso), do [AI Coding Flow](https://aicodingflow.com). Use à vontade, com ou sem o curso.

MIT.
