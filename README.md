# aicf — governança de projeto para desenvolver com agentes

_[English version](README.en.md)_

![A camada de governança do aicf sobre os caminhos de implementação](docs/assets/hero.svg)

Superpowers, Matt Pocock, spec-kit: cuidam de **uma demanda por vez**, e cuidam bem. Três perguntas nenhum deles responde:

- **Onde o projeto está?** Specs descrevem cada mudança, uma por uma. Nenhuma diz o que o produto é, para quem serve e o que ficou de fora por decisão.
- **Por que decidimos não fazer aquilo?** O motivo de recusar um caminho ficou na conversa com o agente, e a conversa não é salva. Onde sobra registro, ele é do esforço que estava aberto, não do produto — semanas depois a mesma discussão volta.
- **O que saiu de fato?** Spec e plano foram escritos antes de executar, e nenhum dos dois é atualizado com o que mudou no caminho.

O aicf é a camada de cima: PRD, roadmap, demanda versionada e o relatório do que foi feito. Seis skills, por cima do caminho de implementação que você já usa, sem trocar nada.

## Instalação

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Reinicie a sessão depois de instalar — skills carregam no início e não trocam a quente.

Em projeto novo, comece por `/aicf:setup`. Em projeto que já existe, por `/aicf:workflow-demanda`, que explica o ciclo.

## O ciclo

Toda demanda passa pelas mesmas quatro fases.

```mermaid
flowchart LR
  D[Demanda<br/>o que se quer, ainda cru]
  E[Entrevista<br/>produz a spec]
  I[Implementação<br/>consome a spec]
  F[Fechamento<br/>relatório do que saiu]
  D --> E --> I --> F
  F -.-> D
```

- **Demanda** — a ideia registrada, mesmo antes de estar madura.
- **Entrevista** — perguntas até não sobrar decisão em aberto. Sai uma spec.
- **Implementação** — alguém executa a spec, por qualquer caminho.
- **Fechamento** — o relatório do que foi feito de fato, com o que saiu diferente do planejado.

Cada demanda é um arquivo versionado no repositório, ou uma issue do GitHub. Você escolhe qual no setup.

## O problema que isso resolve

### Onde o projeto está?

`/aicf:criar-prd` entrevista você e escreve o `PRD.md`. A seção que mais se paga é "fora de escopo, por decisão": é ela que impede a mesma discussão de voltar daqui a seis meses.

### Por que decidimos não fazer aquilo?

No aicf a decisão e o motivo ficam na demanda, dentro do repositório. `/aicf:criar-spec` conduz a entrevista e grava tudo, inclusive o que foi decidido **não** fazer.

### O que saiu de fato?

`/aicf:fechar-demanda` pede o relatório do que saiu e o guarda junto da demanda. O agente aplica o fechamento em qualquer caminho de implementação, inclusive nos que não são do aicf.

## Começando um projeto novo

**1. `/aicf:setup`.** Monta a base: o `PRD.md`, o lugar onde as demandas vão morar, e o `CLAUDE.md` da raiz, que é o arquivo que o agente lê no início de toda sessão. Pergunta pouco — o nome, uma ou duas frases sobre o projeto, se a demanda vive em arquivo ou em issue, onde ficam os padrões de engenharia, e quais ferramentas você já usa. Se o diretório ainda não é repositório git, ele oferece o `git init` antes da pergunta sobre onde as demandas moram, deixa o que criou no primeiro commit em `main`, e te entrega em `develop`, a branch de trabalho.

**2. Preencher o `PRD.md`.** Ele nasce com as seções e uma pergunta em cada uma. `/aicf:criar-prd` entrevista seção por seção e escreve o arquivo, começando pelo problema em vez da solução.

<details>
<summary>Por que o PRD não passa pelo ciclo da demanda</summary>

Não é por ser documento — spec serve bem para mudança de documentação. É que a spec descreve uma **mudança**, com escopo e um estado "pronto", enquanto o PRD descreve o **produto**, e é revisado toda vez que uma decisão o contraria. Envelopar um no outro rende uma spec vazia: a entrevista dela discutiria como escrever o arquivo, e as perguntas que importam — público, fora de escopo — continuariam sem resposta. Mais um fechamento pedindo relatório, arquivamento e check de lint num `.md`.

</details>

**3. Listar o que o produto precisa ter.** Cada item vira uma linha do roadmap, ou uma issue de backlog. O que precisar de contexto ganha registro próprio na hora, e a linha sai — quem tem arquivo não tem linha, e não sobra índice para envelhecer.

**4. Primeira demanda.** `/aicf:criar-spec` para amadurecer, `/aicf:implementar-spec` para executar e fechar. Daí em diante o ciclo se repete.

As fases de entrevista e de implementação aceitam caminhos de fora do aicf, se você já usa outras coleções de skills. A governança não muda, e a demanda anota qual caminho foi usado.

## As skills

São seis, e o eixo que importa é quem pode chamar cada uma.

**Você digita.** Só existem quando você as chama, e conduzem uma sessão inteira.

| Skill | Quando | O que faz |
| --- | --- | --- |
| `/aicf:setup` | uma vez, no projeto novo | Inicializa o repositório git se faltar, pergunta se a demanda mora em arquivo ou em issue e monta o que a escolha pedir: `docs/projeto/` com PRD, roadmap e as pastas de demanda, ou o repositório no GitHub e os três labels `aicf:*`. Nos dois casos, o `CLAUDE.md` (com `AGENTS.md` apontando para ele), um `README.md`, se você quiser os padrões de engenharia, o primeiro commit em `main` e a branch `develop` para trabalhar |
| `/aicf:criar-prd` | começo do projeto | Entrevista sobre o produto e escreve o `PRD.md`. Roda de novo quando uma decisão o contraria |

**Você digita, ou o agente alcança sozinho.** Respondem ao pedido em linguagem natural — "me entreviste sobre X", "implementa a spec Y" — e o agente as carrega quando reconhece a intenção.

| Skill | Quando | O que faz |
| --- | --- | --- |
| `/aicf:workflow-demanda` | o mapa | O ciclo, os caminhos de cada fase e as convenções de governança |
| `/aicf:criar-spec` | fase de entrevista | Interroga até não sobrar decisão em aberto, depois escreve a spec, com a sugestão de caminho de implementação. `/aicf:criar-spec #12` adota uma issue que já existe |
| `/aicf:implementar-spec` | fase de implementação | Decide o caminho pela sugestão da spec, implementa e verifica. Ao final chama o fechamento |
| `/aicf:fechar-demanda` | fase de fechamento | Checks, relatório, arquivamento e promoção de conhecimento, por qualquer caminho de implementação |

As skills são deliberadamente pequenas: dizem o que o agente não teria como inferir — onde gravar, o que registrar, quando fechar — e param aí. O que a ferramenta já faz bem, e o que se decide melhor no caso concreto, fica com o agente.

<details>
<summary><strong>Onde as coisas ficam</strong> — a estrutura de pastas, ou os labels</summary>

No modo arquivo, a pasta diz a maturidade do documento:

```
docs/projeto/
├── PRD.md             # o porquê do produto: visão, público, modelo
├── ROADMAP.md         # o que ainda não tem arquivo: Próximas e Backlog
├── backlog/           # ainda não está claro que será feita
├── intents/           # decidida, ainda não entrevistada
├── specs/             # pronta para implementar
└── concluidas/        # arquivadas, com relatório
```

Uma demanda é a unidade de trabalho. O arquivo que a descreve nasce como **intent**, vira **spec** quando está pronta para implementar — o mesmo arquivo, movido — e termina em `concluidas/` com o relatório. As quatro pastas ficam no mesmo nível, para que mover o arquivo não quebre os links relativos que saem dele.

**Em issues**, a maturidade fica num label (`aicf:backlog`, `aicf:intent`, `aicf:spec`), a demanda é uma issue só do nascimento ao fechamento — o label troca, o número não —, e concluída é a issue fechada, com o relatório em comentário. Aí `docs/projeto/` fica só com o `PRD.md`. PRD, ADR e glossário ficam em arquivo nos dois modos.

Você troca editando uma linha do `CLAUDE.md`, e a linha ausente significa arquivo, então projeto criado antes desta opção segue funcionando sem tocar em nada. A escolha vale do ponto em diante: não há migração, o que está em arquivo fica onde está, e demanda nova nasce na mídia nova.

Cada uma ganha coisas diferentes. Arquivo: zero setup, sobrevive ao `git clone` sem rede, entra no `grep` do repositório, não depende de fornecedor. Issue: conversa com comentário e notificação, contribuição de fora em dois cliques, referência estável por `#12`, e `Fixes #12` fechando pelo merge. O default é arquivo porque é o que funciona sem `gh`, sem login e sem remote.

Se o seu projeto precisar de outra estrutura, escreva a diferença no `CLAUDE.md` da raiz ou em `.claude/rules/`, nunca num `CLAUDE.md` dentro de `docs/projeto/`: `CLAUDE.md` de subpasta só entra no contexto quando o agente lê um arquivo daquela pasta, e registrar uma demanda nova não exige isso.

</details>

<details>
<summary><strong>Comandos vizinhos que valem conhecer</strong> — e para que serve cada um</summary>

Nenhum deles vem com o aicf. São das coleções [Superpowers](https://github.com/obra/superpowers) e [Matt Pocock](https://github.com/mattpocock/skills), e valem se você já as tem instaladas.

**Antes de escrever a demanda**

- `grill-me` e `grill-with-docs` (Matt) — contestam a ideia antes de você escrevê-la, com perguntas até cada ramo da decisão estar resolvido. Use quando você já acha que sabe o que quer. Não gravam nada; o resultado entra na entrevista.
- `wayfinder` (Matt) — mapeia um pedido grande demais para uma sessão como tickets de decisão no seu tracker, e resolve um por vez. Use quando o caminho até o resultado ainda não está visível. O mapa é daquele esforço.
- `domain-modeling` (Matt) — grava o vocabulário do projeto num `CONTEXT.md`, se o produto tem termos próprios que já apareceram ambíguos.

**Na fase de entrevista, no lugar de `/aicf:criar-spec`**

- `brainstorming` (Superpowers) — entrevista e, no caminho _architectural_, grava um design doc que vale como spec.
- `grill-with-docs` + `to-spec` (Matt) — a mesma coisa em dois passos, terminando com a spec publicada no tracker.

**Na fase de implementação, no lugar de `/aicf:implementar-spec`**

- `writing-plans` + `subagent-driven-development` (Superpowers) — o plano vai para arquivo, e subagentes executam tarefa por tarefa.
- `to-tickets` + `implement` (Matt) — a spec vira tickets com dependência declarada entre eles, executados um a um.
- `code-review` (Matt) — revisa o diff em dois eixos, padrões do repositório e fidelidade à spec, em subagentes paralelos.

Dá para entrevistar por um caminho e implementar por outro. Descer essa lista troca velocidade por rastro: nos caminhos aicf o plano vive na sessão e morre com ela.

</details>

<details>
<summary><strong>Por que este, e não o Superpowers, o Matt Pocock, o GSD ou o BMAD</strong></summary>

Porque não é a mesma pergunta. O Superpowers e as skills do Matt resolvem bem **a demanda individual**: interrogam a ideia, produzem uma spec, quebram em tarefas, executam com disciplina. E deixam rastro — o Superpowers grava spec e plano em arquivo no caminho _architectural_, o Matt publica spec e tickets no tracker que você escolheu no setup dele (GitHub, GitLab ou markdown local, e outro tracker descrito em prosa), e ainda mantém glossário e ADRs.

Só que esse rastro é **por demanda** e escrito **antes** da execução. Três coisas ficam de fora, e nenhuma das duas declara que são problema de outra pessoa — elas param no esforço: começam num pedido já recortado, por maior que ele seja, e terminam no commit ou no merge.

- **O nível do produto.** Nenhuma das duas tem o documento que diz o que se está construindo, para quem, e o que ficou fora por decisão, nem o registro do que já foi entregue e do que falta. O Matt chega perto: guarda o pedido que recusou e o que tirou do esforço em andamento, com o motivo — por esforço, não por produto.
- **O planejamento macro.** Quando o pedido é grande demais para uma spec, o `brainstorming` ajuda a decompor em subprojetos e trabalha o primeiro; os outros ficam na conversa. Aqui a ideia que ainda não amadureceu tem registro próprio, cada demanda declara na própria prosa o que bloqueia e do que depende, e o que ainda não se sabe se será feito tem lugar para esperar sem se perder. O `wayfinder` do Matt chega perto: mapeia um pedido grande demais para uma sessão e tem `Not yet specified` para a ideia que ainda não dá para ticketar. O mapa é de um esforço e acaba com ele; o que sobra volta como esforço novo, não como fila que atravessa o projeto.
- **O depois.** Spec e plano dizem o que se pretendia. O `implement` do Matt termina no commit e não fecha o ticket nem marca os critérios de aceite. O Superpowers grava plano e design doc no repositório, e eles ficam: o código é revisto contra o plano a cada tarefa, mas plano e spec não mudam — nada os atualiza com o que saiu. O aicf pede um relatório na própria demanda, e é nele que a divergência plano×entrega fica escrita.

O aicf é essa camada, e a mesma camada vale para qualquer caminho de implementação. Trocar de coleção, ou misturar as duas numa mesma demanda, não muda nada na governança.

**GSD e BMAD são o caso oposto: já têm essa camada.** O `PROJECT.md` do GSD Core tem "What This Is", "Core Value", "Out of Scope" com o motivo e "Key Decisions", e `complete-milestone` e `extract-learnings` fazem o que o `fechar-demanda` faz aqui. A diferença é que nos dois a camada vem grudada num loop de execução próprio — 72 comandos `/gsd-*` no GSD Core, 30 skills e `uv` obrigatório no BMAD —, e é esse loop que o aicf deixa de fora por decisão ([ADR 0001](docs/adr/0001-fronteira-de-fase.md)): aqui quem manda dentro da fase de implementação é o método que você escolheu para ela. Se você quer o pacote inteiro, o GSD faz mais do que o aicf; se quer só a camada, e implementar pelo caminho que preferir, é este.

</details>

## Sobre

Feito para o curso [Claude Code: Criador de Apps](https://aicodingflow.com/curso), do [AI Coding Flow](https://aicodingflow.com). Use à vontade, com ou sem o curso.

MIT.
