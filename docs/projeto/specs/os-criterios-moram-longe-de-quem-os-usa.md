# Os critérios moram longe de quem os usa

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (três arquivos de texto, decisões fechadas na entrevista)

## Problema

Duas skills remetem a um critério que só existe no `/aicf:workflow-demanda`, sem mandar carregá-lo:

- o passo 3 do `implementar-spec` manda avaliar o workspace *"pelo critério do
  `/aicf:workflow-demanda`"* (`grep -cF 'critério do `/aicf:workflow-demanda`' skills/implementar-spec/SKILL.md` → 1);
- a tabela de promoção do `fechar-demanda` remete ao *"critério skill×hook no
  `/aicf:workflow-demanda`"* (`grep -cF 'critério skill×hook no' skills/fechar-demanda/SKILL.md` → 1).

Quem entra por `/aicf:implementar-spec` ou chega ao fechamento sem ter invocado o mapa aplica um
critério que não tem em contexto: decide de cabeça, ou abre o arquivo por fora. E os dois critérios,
lidos onde estão, têm lacunas:

**Workspace** (seção "Branch, ou worktree" do `workflow-demanda`):
- o default que ele declara já está na seção `## Git` do `CLAUDE.md` do projeto
  (`skills/setup/templates/claude-md.md`, *"Commitar direto na branch de trabalho por padrão"*) —
  duas fontes para a mesma regra;
- não distingue branch própria de worktree: o mesmo motivo ("demanda grande, ou descartar em
  bloco") serve às duas, e "grande" não tem critério;
- a coluna Integração da tabela de implementação diz, para os caminhos aicf, *"o agente, pelo
  critério de workspace abaixo"* — e o critério fala de onde trabalhar, não de como integrar. Os
  caminhos aicf não têm passo de integração;
- o próprio texto diz *"A avaliação acontece no `implementar-spec`"*: o único consumidor mora em
  outra skill.

**Skill×hook** (seção "Trabalho recorrente não é demanda"):
- o gatilho discorda entre os dois textos: *"terceira vez"* no mapa, *"Procedimento que já se
  repetiu"* na tabela do fechamento;
- hook não aparece como destino na tabela de promoção, que é onde a decisão acontece;
- não diz onde o hook mora; "skill ou command" usa vocabulário que o Claude Code já unificou;
- a seção mistura a pergunta de triagem ("isto é demanda?") com a de promoção ("skill ou hook?").

## Solução

Cada critério muda para a skill que o aplica, preenchido e mais curto. O mapa fica com uma frase
que aponta para lá. Nenhum arquivo novo.

### `implementar-spec` — o critério de workspace, no passo 3

O parágrafo "Junto do caminho, avaliar o workspace…" vira:

> **Junto do caminho, decidir o workspace.** O default é o da seção `## Git` do `CLAUDE.md`; sem
> ela, a branch atual. Sair dele é pergunta ao usuário, e o agente propõe quando couber:
> **branch própria** quando vale poder descartar em bloco ou revisar antes de entrar — mais de um
> commit de código, ou área onde erro custa dinheiro ou dado (migration, auth, pagamento);
> **worktree** — outra pasta, com a própria branch — só quando o checkout atual precisa continuar
> em uso (outra sessão, servidor rodando), e nunca quando a verificação depende de estado não
> versionado (`.env`, banco, pasta gitignored): a worktree nasce sem ele. Dizer numa linha o que
> decidiu e por quê — em qualquer caminho, inclusive o de outra coleção, antes de passar a vez.

E "Verificar e fechar" ganha a integração dos caminhos aicf, entre a verificação e o fechamento:

> **Em branch própria, integrar antes de fechar:** `AskUserQuestion` com merge na branch de
> trabalho, PR, ou deixar a branch. O fechamento começa depois da escolha.

### `fechar-demanda` — skill e hook, na tabela de promoção

A linha *"Procedimento que já se repetiu | skill — gatilho e critério skill×hook no
`/aicf:workflow-demanda`"* vira duas:

> | Procedimento que apareceu pela terceira vez | skill em `.claude/skills/` |
> | Regra que precisa valer sem exceção — a que pode falhar sem ninguém perceber | hook em `.claude/settings.json`: roda sempre, enquanto skill é conselho que o modelo pode não seguir |

O gatilho no meio da sessão não precisa de texto novo: o `CLAUDE.md` que o setup gera já diz
*"Operação que se repete vira **skill** em `.claude/skills/`"* (`grep -cF 'Operação que se repete'
skills/setup/templates/claude-md.md` → 1), e esse arquivo carrega em toda sessão.

### `workflow-demanda` — só o mapa

- Sai o parágrafo **"Branch, ou worktree."** inteiro.
- Na tabela de implementação, as duas linhas aicf trocam *"o agente, pelo critério de workspace
  abaixo"* por *"o `/aicf:implementar-spec`, que pergunta"*.
- A seção "Trabalho recorrente não é demanda" fica só com a triagem:

  > Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir — publicar
  > conteúdo, subir versão, liberar acesso — não é demanda: vira skill ou hook, pelo critério da
  > tabela de promoção do `/aicf:fechar-demanda`.

A referência cita a tabela pelo nome, não pelo número do passo (regra do `CLAUDE.md` sobre passo
citado por número).

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `skills/implementar-spec/SKILL.md` | passo 3: o critério de workspace; "Verificar e fechar": a integração em branch própria |
| `skills/fechar-demanda/SKILL.md` | tabela de promoção: uma linha vira duas (skill, hook) |
| `skills/workflow-demanda/SKILL.md` | sai "Branch, ou worktree"; coluna Integração; "Trabalho recorrente" reduzida à triagem |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.29.4` → `0.30.0` — muda comportamento: os caminhos aicf passam a perguntar a integração |

## Fora de escopo

- **`references/` compartilhado para os critérios.** Cada critério tem um consumidor só; arquivo
  compartilhado seria abstração antecipada.
- **Mandar as skills carregarem o `workflow-demanda`.** Custaria o `SKILL.md` inteiro (12.225 bytes,
  `wc -c < skills/workflow-demanda/SKILL.md`) para usar um parágrafo, desfazendo
  [as skills carregam o que não vão usar](../concluidas/as-skills-carregam-o-que-nao-vao-usar.md).
- **Palavra de fechamento de issue no PR (`Closes #<n>`).** No modo issue, ela fecharia a issue no
  merge, antes do relatório. Só acontece com PR para a branch default, e o aicf entrega `develop`
  como branch de trabalho; se aparecer, vira demanda própria.
- **O template do `CLAUDE.md` e o `/aicf:setup`.** O setup já grava o default: em projeto novo o
  `CLAUDE.md` nasce do template, que tem `## Git` com *"Commitar direto na branch de trabalho por
  padrão; branch + PR só para mudança grande ou a pedido"*
  (`grep -cF 'Commitar direto na branch de trabalho' skills/setup/templates/claude-md.md` → 1). Em
  projeto com `CLAUDE.md` próprio, o setup só propõe acrescentar a seção "Processos de
  desenvolvimento" (`skills/setup/SKILL.md`, parágrafo "Se o projeto já tem `CLAUDE.md` na raiz"),
  e o `## Git` pode faltar — é o caso que o fallback "sem ela, a branch atual" cobre. O "mudança
  grande" do template continua vago de propósito: é a regra do projeto, que o usuário ajusta; o
  critério do `implementar-spec` diz quando propor sair dela.

## Verificação

Os valores de "hoje" foram medidos em `ac94ff1`.

1. **Os ponteiros saíram.**
   ```
   grep -cF 'critério do `/aicf:workflow-demanda`' skills/implementar-spec/SKILL.md   # hoje 1; depois 0
   grep -cF 'critério skill×hook no' skills/fechar-demanda/SKILL.md                 # hoje 1; depois 0
   grep -cF 'Branch, ou worktree' skills/workflow-demanda/SKILL.md                  # hoje 1; depois 0
   grep -cF 'critério de workspace abaixo' skills/workflow-demanda/SKILL.md         # hoje 2; depois 0
   ```
2. **Os critérios chegaram.**
   ```
   grep -cF '`## Git`' skills/implementar-spec/SKILL.md          # hoje 0; depois 1
   grep -cF '.claude/settings.json' skills/fechar-demanda/SKILL.md # hoje 0; depois 1
   ```
3. **O texto encurtou.** `cat skills/{workflow-demanda,implementar-spec,fechar-demanda}/SKILL.md | wc -c`
   → abaixo de 25.365 (hoje).
4. **O repositório passa.** `./scripts/check.sh` → `Tudo verde.`
5. **Comportamento, depois da release.** Em sessão nova, com a versão `0.30.0` no cabeçalho do
   comando (`cache/aicodingflow/aicf/0.30.0/skills/implementar-spec`), `/aicf:implementar-spec`
   numa spec deste repositório diz numa linha o workspace citando o `## Git` do `CLAUDE.md`, sem
   abrir o `workflow-demanda`.
