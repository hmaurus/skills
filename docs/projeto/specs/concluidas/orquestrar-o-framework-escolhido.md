# A governança orquestra o framework escolhido, não o substitui

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

Na primeira execução de ponta a ponta com três coleções no mesmo projeto — aicf na governança,
Superpowers na implementação, Matt Pocock disponível —, o agente **pulou o encerramento do
framework** por ler uma garantia do aicf como exclusão.

O caso: `hmaurus/mh-fin`. Entrevista pelo `/aicf:criar-spec`, implementação pelo
`superpowers:writing-plans` + `subagent-driven-development` (16 tarefas, 40 commits, 141 testes),
fechamento pelo `/aicf:fechar-demanda`. O `subagent-driven-development` termina em
`finishing-a-development-branch` — a skill que **decide o destino do código**: merge na base, PR,
ou a branch fica. O agente não a rodou, porque o `implementar-spec` diz:

> esta skill para aqui e o caminho escolhido assume, e o fechamento continua sendo
> `/aicf:fechar-demanda`

Essa frase é uma **garantia** — o registro de governança sobrevive à escolha de qualquer caminho.
Foi lida como **exclusão**: "só o aicf fecha". O agente ainda invocou "instrução do usuário vence
skill" para um conflito que não existia: fabricou um.

**Sintoma verificável:** a demanda foi dada por concluída com `main` 40 commits atrás de
`develop`, e a decisão de destino do código nunca foi tomada, nem feita, nem registrada como
pendente. Só aconteceu depois, quando o titular percebeu a falta.

**A raiz é textual, não só de julgamento.** A palavra "fechamento" cobre duas coisas nos
documentos do aicf: fechar o *branch* (destino do código) e fechar a *demanda* (relatório, mover
spec, checklist, promoção de conhecimento). Enquanto uma palavra só nomear as duas, a leitura
errada continua disponível para o próximo agente.

Duas costuras menores apareceram na mesma execução:

- **A decisão de branch/worktree foi arbitrada sem avaliação.** O `subagent-driven-development`
  manda garantir workspace isolado; o `CLAUDE.md` do projeto manda commitar direto na branch de
  trabalho. O agente aplicou o default e chamou de decisão. O resultado foi certo por sorte:
  worktree teria sido errado ali por um motivo que ninguém avaliou — a verificação de seis tarefas
  dependia de estado local **não versionado** (o SQLite e o `regras.json` em `data/`, gitignored),
  e uma worktree nasceria vazia.

- **O `scripts/task-brief` do `subagent-driven-development` só entende plano em inglês.** Procura
  heading `^#+[ \t]+Task[ \t]+[0-9]+`; plano em pt-BR usa "Tarefa N" e o script responde
  `task N not found`. Verificado na versão mais nova em cache (6.3.0) — continua valendo. Como o
  aicf recomenda documentação em português, reaparece em todo plano do Superpowers, e o agente
  teve que escrever um extrator próprio no meio da execução.

## Solução

Cinco mudanças de texto, todas em documento do aicf. Nenhuma toca coleção de terceiro.

### 1. Vocabulário fixo: integração e fechamento

O `workflow-demanda` é a fonte canônica; as outras skills usam as palavras sem redefini-las.
Acrescentar à seção de nomenclatura ("Três palavras, uma unidade de trabalho"):

> **Integração e fechamento são coisas diferentes.** _Integração_ é decidir o destino do código —
> merge na base, PR, ou a branch fica. É o último passo da **implementação**, e pertence ao método
> escolhido. _Fechamento_ é o registro da demanda — relatório, `specs/concluidas/`, checklist,
> promoção de conhecimento. É `/aicf:fechar-demanda`, e nada além. **O método fecha o código, a
> governança fecha a demanda — e a segunda só começa depois da primeira.**

Não há fase nova no ciclo: continuam quatro — demanda → entrevista → implementação → fechamento.
A integração é o último passo da terceira, e é por isso que ela não é assunto da governança.

### 2. A borda entre governança e framework

Também no `workflow-demanda`, logo depois do vocabulário:

> **A governança escolhe o caminho de cada fase; dentro da fase, o encadeamento do framework roda
> inteiro.** Skill que o método declara como passo seguinte dentro da mesma fase não se pula nem se
> substitui — no Superpowers, `executing-plans` e `subagent-driven-development` declaram
> `finishing-a-development-branch` como `REQUIRED SUB-SKILL`. Ela **roda automaticamente, sem
> perguntar**, e o agente conta em uma linha o que ficou decidido. Interferir ali é degradar a
> qualidade de um processo que não é nosso.
>
> Na **passagem entre fases**, quem decide é a governança, mesmo quando o framework recomenda
> continuar nele: o `brainstorming` declara `writing-plans` como estado terminal, e ainda assim
> parar na fronteira é legítimo — o design doc dele vale como spec, e a implementação é escolha
> nova.

A tabela de implementação ganha uma coluna, **Integração**, que diz quem faz e como:

| Caminho | Integração |
| --- | --- |
| Aicf direto / plan mode | o agente, pelo critério de workspace abaixo |
| Superpowers | `finishing-a-development-branch`, encadeada e automática |
| Matt Pocock | o próprio `implement`: `/code-review` e commit na branch atual |

### 3. Critério de workspace, avaliado em vez de herdado

No `workflow-demanda`, junto da tabela de implementação:

> **Branch, ou worktree.** O default é commitar direto na branch de trabalho — processo prático
> para dev solo, com PR para o que a complexidade ou o risco justificarem. O agente **avalia** em
> vez de herdar o default em silêncio: branch própria ou worktree quando a demanda é grande ou se
> quer poder descartá-la em bloco; **contra worktree quando a verificação depende de estado local
> não versionado** — banco, arquivo de dados, `.env`, qualquer coisa em pasta gitignored: a
> worktree nasce sem eles. A avaliação acontece no `implementar-spec`, junto da escolha de caminho;
> o agente diz numa linha o que decidiu e por quê, e sair do default é pergunta ao usuário.

### 4. `implementar-spec`: contrato de saída em vez de frase ambígua

O trecho do passo 3 que produziu a leitura errada passa a delimitar até onde vai o caminho
escolhido:

> outra coleção, esta skill para aqui e o caminho escolhido assume **até o fim, inclusive a
> integração que ele encadeia** — o aicf não interrompe nem substitui passo interno de método; ao
> terminar, `/aicf:fechar-demanda` registra a demanda.

E o passo 3 ganha a avaliação de workspace, na mesma linha em que já decide o caminho.

### 5. `fechar-demanda`: portão de entrada, não duplicação, e `domain-modeling` honesto

**Portão de entrada**, logo abaixo da abertura:

> **Antes de qualquer coisa: a implementação terminou inteira?** Caminho de outra coleção termina
> no passo que ele encadeia — no Superpowers, `finishing-a-development-branch`, que decide o
> destino do código. Fechar a demanda com essa decisão não tomada é o erro que este parágrafo
> existe para evitar: o registro diz "concluído" e o código fica parado numa branch. Se o método
> tem passo de integração e ele não rodou, rodar antes.

**Não duplicação**, na seção "Antes do relatório", depois da revisão de código:

> **Exigência da governança já satisfeita por um passo do caminho escolhido não se repete** — o
> `subagent-driven-development` termina com revisão do branch inteiro, e pedir outra é pagar duas
> vezes pela mesma leitura. O relatório declara em uma linha, na **Validação**, qual passo cobriu
> qual exigência: "Revisão: coberta pelo code reviewer final do subagent-driven-development".

**`domain-modeling`**, no passo 4. A frase atual — "ADR e glossário saem de `/domain-modeling`, que
o agente invoca em qualquer processo — não depende das skills do Matt" — descreve um comportamento
que não aconteceu (os dois ADRs do `mh-fin` saíram direto da tabela) e erra o fato: `domain-modeling`
**é** da coleção do Matt Pocock. Passa a:

> ADR e glossário podem sair de `/domain-modeling`, quando instalado; escrever direto pela tabela
> também serve.

### 6. A regra sobe para o `CLAUDE.md`

O bug foi de um agente que não abriu a skill certa. A regra vira a quarta linha de "Processos de
desenvolvimento", no `templates/claude-md.md` do `setup` e no `CLAUDE.md` deste repositório:

> - **O método escolhido fecha o código; a governança fecha a demanda.** Rodar o processo de
>   implementação inteiro — inclusive o passo de integração que ele encadeia — e só então
>   `/aicf:fechar-demanda`.

### 7. Nota do `task-brief`

Na linha do Superpowers da tabela de implementação do `workflow-demanda`:

> No Superpowers, os headings de tarefa do plano ficam em inglês (`## Task 3`) mesmo com o corpo em
> português: `scripts/task-brief` procura `^#+ Task N` e responde `task N not found` para
> "Tarefa N".

## Arquivos e interfaces

**A fonte editável é este repositório** (`hmaurus/skills`), não
`~/.claude/plugins/cache/aicodingflow/aicf/<versão>/`, que é cópia gerada e some no próximo update.

| Arquivo | Mudança |
| --- | --- |
| `skills/workflow-demanda/SKILL.md` | Vocabulário (1), borda (2), coluna Integração e nota do `task-brief` (2, 7), critério de workspace (3) |
| `skills/implementar-spec/SKILL.md` | Contrato de saída e avaliação de workspace no passo 3 (4) |
| `skills/fechar-demanda/SKILL.md` | Portão de entrada, não duplicação, `domain-modeling` (5) |
| `skills/setup/templates/claude-md.md` | Quarta regra em "Processos de desenvolvimento" (6) |
| `CLAUDE.md` | A mesma quarta regra (6) |
| `.claude-plugin/plugin.json` | `version`: `0.13.4` → `0.13.5` |
| `CHANGELOG.md` | Entrada `## 0.13.5 — <data>` no topo |

O `workflow-demanda` é o único que ganha texto de peso; ele já é o mapa, e concentrar ali evita
três fontes para a mesma regra. As outras duas skills recebem só o que muda o passo delas.

A entrada do changelog segue a voz das anteriores: diz o que mudou e **por que a regra anterior não
bastava** — não só o que foi acrescentado.

## Fora de escopo

- **Mudar as skills do Superpowers ou do Matt Pocock.** O aicf orquestra o que existe; não mantém
  coleção de terceiro.
- **Reabrir a escolha entre commitar direto e PR.** O default está decidido: branch de trabalho,
  com PR pelo que a complexidade ou o risco justificarem.
- **Extrator próprio de tarefas para planos em pt-BR.** Substituiria uma ferramenta de terceiro e
  quebraria junto quando eles mudassem o formato. A nota de (7) resolve na origem, sem código.
- **Fase nova de "integração" no ciclo.** Criá-la devolveria a fronteira à governança e reintroduziria
  exatamente o bug: a integração ficaria negociável entre fases, quando ela é interna ao método.
- **Tabela de equivalências entre exigências do aicf e passos de cada framework.** É conhecimento de
  terceiro que envelhece a cada versão deles; a regra de não duplicação com declaração no relatório
  cobre o caso sem nada para manter.
- **`/domain-modeling` como passo obrigatório do fechamento.** Poria skill de terceiro no caminho
  crítico da camada que precisa rodar sozinha.

## Verificação

Não há build nem suíte neste repositório — o produto é texto de skill. O passo ponta a ponta é uma
leitura simulada, feita por **subagente fresco** que não viu esta sessão, recebendo só as skills
alteradas e a pergunta:

> Uma demanda foi implementada por `superpowers:subagent-driven-development`, que terminou as 16
> tarefas e a revisão final. Qual é o próximo passo?

A resposta certa nomeia `finishing-a-development-branch` **antes** de `/aicf:fechar-demanda`, e não
trata as duas como alternativas. Se o subagente responder "chamar `/aicf:fechar-demanda`", o texto
ainda não resolveu o problema.

Conferir também, à mão:

1. `grep -rn "fechamento" skills/` — nenhuma ocorrência restante nomeia destino de código.
2. A quarta regra aparece em `CLAUDE.md` e em `skills/setup/templates/claude-md.md`, com a mesma
   redação.
3. `.claude-plugin/plugin.json` em `0.13.5`, com a entrada correspondente no topo do `CHANGELOG.md`.

## Relatório de implementação (2026-09-08)

**Status** — concluído, na versão `0.13.5`. Não há CI nem PR: o produto é texto de skill e o
commit foi direto em `main`.

**Causa raiz** — uma palavra para duas coisas. "Fechamento" nomeava tanto decidir o destino do
código quanto registrar a demanda, e a garantia do `implementar-spec` ("o fechamento continua
sendo `/aicf:fechar-demanda`") era lida como exclusão. A execução revelou que a ambiguidade não
estava só no julgamento do agente: nenhum documento definia a palavra, então qualquer leitura era
defensável.

**Arquivos alterados**

| Arquivo | O que entrou |
| --- | --- |
| `skills/workflow-demanda/SKILL.md` | Vocabulário integração×fechamento, a borda de fronteira de fase, coluna **Integração** na tabela, critério de branch/worktree, nota do `task-brief` |
| `skills/implementar-spec/SKILL.md` | Contrato de saída no passo 3 ("assume até o fim, inclusive a integração que ele encadeia") e a avaliação de workspace |
| `skills/fechar-demanda/SKILL.md` | Portão de entrada, regra de não duplicação, `domain-modeling` afrouxado |
| `skills/setup/templates/claude-md.md` e `CLAUDE.md` | A quarta regra, mesma redação nos dois |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.13.4` → `0.13.5` |

**Commits**

- `e31e090` — `feat(governanca): 0.13.5 — integração é do método, fechamento é da governança`
- o commit deste registro, com o ADR `0001`

**Validação**

- **Revisão: coberta pela verificação da spec** — subagente fresco, que não viu a implementação,
  leu as quatro skills alteradas e respondeu à situação "o `subagent-driven-development` terminou,
  qual o próximo passo?". Nomeou `finishing-a-development-branch` **antes** de
  `/aicf:fechar-demanda`, disse que a revisão não se repete e declarou a distinção
  integração×fechamento. Não foi pedida uma segunda revisão — é a regra que esta demanda criou,
  aplicada a si mesma.
- Conferências à mão: nenhuma ocorrência de "fechamento" nas skills nomeia destino de código; a
  quarta regra está nos dois arquivos com redação idêntica; `plugin.json` em `0.13.5` com a
  entrada correspondente no topo do `CHANGELOG.md`.
- **Não há check de projeto para rodar.** Sem build, testes ou lint — a seção `## Verificação` do
  `CLAUDE.md` continua com `<comando>` por preencher, porque o produto é texto.

**Escopo efetivo**

Duas coisas apareceram na leitura do que estava instalado e mudaram o desenho:

1. O `brainstorming` do Superpowers declara `writing-plans` como estado terminal obrigatório
   ("the ONLY skill you invoke after brainstorming is writing-plans"). O intent supunha que ele
   fosse uma peça independente. Foi o que obrigou a escolher um critério explícito para a borda —
   sem ele, "não interferir no processo do framework" teria matado a independência entre
   entrevista e implementação, que é a razão de o aicf existir.
2. A frase do `fechar-demanda` sobre `/domain-modeling` errava um fato: dizia "não depende das
   skills do Matt", e a skill **é** da coleção do Matt Pocock. Corrigido junto.

**Lições**

- **Ambiguidade de palavra não se resolve com mais instrução, e sim com definição.** O
  `implementar-spec` já dizia a coisa certa; o que faltava era a palavra ter um dono. A correção
  que funcionou foi o par de definições no mapa, não um aviso a mais na skill que falhou.
- **Regra que precisa valer antes de o agente abrir a skill certa mora no `CLAUDE.md`.** O bug
  aconteceu com um agente que nunca abriu o documento onde a regra estaria. Duas linhas no arquivo
  lido em toda sessão custam menos que o erro que elas evitam.
- **Verificar o texto de terceiro em vez de confiar na memória do que ele faz.** Três premissas
  foram checadas no que está instalado e duas se confirmaram (`REQUIRED SUB-SKILL` do
  `finishing-a-development-branch`; regex do `task-brief`, ainda quebrada na 6.3.0); a terceira,
  sobre o `brainstorming`, era falsa e mudou a solução.
- **Glossário em `CONTEXT.md` foi avaliado e descartado.** As definições de integração e
  fechamento já vivem no `workflow-demanda`, que é o mapa e é lido por quem mexe neste
  repositório; um `CONTEXT.md` seria segunda fonte da mesma definição — exatamente o que o lema do
  projeto manda evitar. Quando aparecer termo ambíguo que não seja vocabulário exportado pelo
  plugin, o arquivo nasce.
