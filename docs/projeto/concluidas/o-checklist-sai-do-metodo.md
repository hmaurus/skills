# O `CHECKLIST.md` sai do método: um item, um lugar

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (o desenho fechou na entrevista; o diff é o mesmo movimento repetido em arquivos já nomeados)

## Problema

Três das cinco seções do `CHECKLIST.md` — `Decidido`, `Em andamento`, `Entregue` — espelham três
pastas. Toda demanda existe duas vezes: como arquivo na pasta, e como linha na seção.

O método defende essa duplicação como detecção de erro. O argumento está invertido, e o
[ADR 0002](../../adr/0002-conferencia-do-indice-por-inclusao.md) prova: ele decidiu que a
conferência corre **num sentido só** — todo arquivo tem linha, e o inverso não é exigido. Isso não
é partida dobrada, em que duas fontes independentes se conferem. É a declaração formal de que a
pasta é a fonte e o checklist é uma cópia derivada dela **à mão**.

Cópia manual não detecta erro na fonte. Ela fabrica uma classe de erro nova — a cópia divergir — e
depois gasta ritual detectando o erro que ela mesma criou.

O que essa cópia já custou, tudo existindo exclusivamente por causa dela:

- **16 linhas** no passo 5 do `fechar-demanda`
  (`awk '/^5\. \*\*Conferir o índice/,/^O fechamento vai num commit/' skills/fechar-demanda/SKILL.md | head -n -1 | wc -l`, 2026-09-13),
  carregadas em toda demanda fechada, de todo projeto que usa o plugin.
- O ADR 0002 inteiro, para definir a semântica de uma comparação.
- A intent [a conferência do índice vira script](a-conferencia-do-indice-vira-script.md),
  que existe só para transformar essa comparação em código.
- Cinco dos seis itens da `0.14.0` no `CHANGELOG.md`.

E falhou no trabalho para o qual existe. O relato da `0.14.0`: *"o checklist ficou desatualizado em
três lugares e o agente não achou nenhum sozinho — nem no ritual, nem nas duas vezes em que o
titular mandou conferir."*

Enquanto isso, um comando devolve as mesmas três seções, com os títulos de verdade e sempre
correto:

```
head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'
```

## Solução

**Um item, um lugar.** Enquanto a demanda não tem arquivo, ela é uma linha no roadmap. Quando vira
arquivo, a pasta é a verdade inteira. Nunca as duas.

A regra de hoje diz: *"quando precisa de mais, vira arquivo em `intents/`, **a linha vira ponteiro**
e passa para `Decidido`"*. A mudança cabe em três palavras: **a linha sai**.

Sem ponteiro não há o que sincronizar, não há conferência de índice e não há script a escrever.

`docs/projeto/CHECKLIST.md` é substituído por `docs/projeto/ROADMAP.md`, com duas seções — as duas
que nunca tiveram pasta e por isso nunca derivaram:

```markdown
# Roadmap — <NOME>

O que ainda não tem arquivo. Quando um item precisa de contexto, vira arquivo em `intents/` e a
linha **sai daqui** — a pasta passa a ser o registro inteiro. O que já tem arquivo se lê com
`head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'`.

## Próximas

> Decidido, ainda sem arquivo.

- [ ] Repositório, branch de trabalho e CI mínimo
- [ ] `PRD.md` preenchido

## Backlog

> Ainda não é certeza. O que separa daqui de `Próximas` é **certeza, não urgência**.
>
> **Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item
> continua plausível depois de resolvido, e ninguém percebe.

> - ...
```

Arquivo próprio, não seção do `PRD.md`: os dois têm ritmos opostos de escrita — em 44 commits, o
checklist mudou 6 vezes e o PRD mudou 1, a de criação
(`git log --oneline -- docs/projeto/CHECKLIST.md | wc -l` e o mesmo para `PRD.md`, 2026-09-13).
Juntá-los faz `git log docs/projeto/PRD.md` deixar de responder *quando a visão mudou*.

O `Entregue` não migra. A história já está em `specs/concluidas/` e, onde houver, no
`CHANGELOG.md`, com mais detalhe do que a linha tinha.

## Arquivos e interfaces

**Governança deste repositório**

| Arquivo | O quê |
| --- | --- |
| `docs/projeto/CHECKLIST.md` | apagado |
| `docs/projeto/ROADMAP.md` | criado, com `Próximas` (as duas linhas de `Fundação`) e `Backlog` |
| `docs/projeto/intents/a-conferencia-do-indice-vira-script.md` | **cancelada** — vai para `specs/concluidas/` com relatório dizendo que o mecanismo que ela scriptaria deixou de existir |
| `docs/projeto/intents/escolher-entre-arquivos-e-issues.md` | ganha nota: depende desta demanda, e encolheu por causa dela |

**Skills**

| Arquivo | O quê |
| --- | --- |
| `skills/fechar-demanda/SKILL.md` | passo 3 (`- [x]`, linha entre seções) **morre**; passo 5 encolhe de 16 para ~4 linhas — sai a conferência dos três pares, ficam a saída dos passos 1–4 (o link do ADR passa a entrar no relatório da própria demanda) e "isto criou item novo no roadmap?"; a "Sessão que acaba antes da demanda" perde a menção a `Em andamento` |
| `skills/workflow-demanda/SKILL.md` | a árvore perde a linha do `CHECKLIST.md` e ganha a do `ROADMAP.md`; "item do checklist" vira "linha do roadmap"; o agrupamento de demandas que andam juntas passa a viver na prosa das specs, não em subtítulo de seção |
| `skills/criar-spec/SKILL.md` | "a linha da demanda acompanha o arquivo: sai de `Decidido` e entra em `Em andamento`" vira "a linha do roadmap, se existir, sai" |
| `skills/criar-prd/SKILL.md` | passo 2 passa a tirar do PRD o primeiro **roadmap** |
| `skills/setup/SKILL.md` | árvore, tabela de templates e `description` trocam checklist por roadmap |
| `skills/setup/templates/checklist.md` | renomeado para `templates/roadmap.md`, reescrito com as duas seções |
| `skills/setup/templates/readme.md` | linha da tabela |

**Documentação**

`README.md`, `README.en.md` (linhas 5, 14, 35, 46, 54, 90 e equivalentes) e `CLAUDE.md` (linha 5).
O passo 3 dos READMEs — "a linha vira ponteiro para ele" — é a frase que a demanda inverte, e é
onde a regra nova precisa aparecer com todas as letras.

**Decisão a registrar**

ADR novo supersedendo o 0002. ADR é imutável: o 0002 não se edita, o novo diz que a conferência de
inclusão deixou de ter objeto porque o índice derivado saiu. Entra pelo passo 3 do fechamento.

**Não se reescreve:** `CHANGELOG.md`, `docs/adr/0002-*.md` e os três arquivos de
`specs/concluidas/`. São registro histórico — o precedente é a `0.13.0`, que ao trocar "nativo" por
"aicf" deixou explícito que *"demandas já arquivadas não são reescritas"*.

## Fora de escopo

- **Skill de migração** para converter o `CHECKLIST.md` antigo nos projetos consumidores. É código
  novo no plugin para uma operação que acontece uma vez por projeto; o `CHANGELOG` da versão
  descreve o procedimento e basta.
- **Escolher entre arquivos e issues.** Continua como intent e passa a depender desta. O motivo de
  separar: tirar o índice derivado vale sozinho, e feito antes transforma aquela demanda de
  "refatorar seis skills" em "trocar quatro verbos" — o doc de convenção dela cai de ~55 para ~25
  linhas, porque o grosso do que iria para lá era a maquinaria checklist↔pasta.
- **Índice gerado e commitado** (um `ROADMAP.md` que também lista o que tem arquivo, produzido por
  script). Seria a mesma cópia derivada com outro nome, e o mesmo envelhecimento.
- **Ordem de prioridade entre demandas que já têm arquivo.** Some com as seções, e não se
  substitui: as dependências já vivem na prosa das próprias intents ("Bloqueia", "Habilita",
  "Depende de"), onde sobrevivem a renomeação.

## Verificação

O passo ponta a ponta é **fechar esta própria demanda pelo método novo**: rodar
`/aicf:fechar-demanda` e chegar ao fim sem que nenhum passo peça um checklist. Antes disso:

```bash
# 1. o arquivo saiu, o novo entrou com as duas seções
test ! -f docs/projeto/CHECKLIST.md && grep -c '^## ' docs/projeto/ROADMAP.md   # 2

# 2. nenhum link vivo aponta para o arquivo (saída vazia). Menção em prosa é
#    legítima: CHANGELOG, ADR 0002 e as intents narram a remoção no passado
grep -rn '](.*CHECKLIST' --include='*.md' --exclude='o-checklist-sai-do-metodo.md' .

# 3. a skill mais cara do plugin encolheu
wc -l < skills/fechar-demanda/SKILL.md   # < 130

# 4. a intent cancelada saiu de intents/
test ! -f docs/projeto/intents/a-conferencia-do-indice-vira-script.md
```

## Relatório de implementação (2026-09-14)

- **Status** — concluído. Sem CI: este repositório não tem workflow, e a seção `## Verificação` do
  `CLAUDE.md` ainda é o placeholder "a preencher quando houver código" — encerra quando houver
  script de check no `package.json` ou equivalente.
- **Arquivos alterados** — 19 ao todo (`git show --stat a6276e7`). `docs/projeto/CHECKLIST.md`
  apagado e `ROADMAP.md` criado; `skills/setup/templates/checklist.md` renomeado para `roadmap.md`;
  as seis skills, os dois READMEs, o `CLAUDE.md`, os dois manifestos em `.claude-plugin/` (versão
  `0.16.0` e descrição) e as três intents que argumentavam em cima do mecanismo removido.
- **Commits** — `a6276e7` (`feat(governanca)!: 0.16.0 — o índice derivado sai do método`) traz a
  implementação; o commit que carrega este relatório traz o fechamento, incluindo as sete correções
  vindas da revisão.
- **Validação** — os quatro comandos da seção acima; `python3 -c json.load` nos dois manifestos;
  frontmatter das seis skills; script de resolução de todos os links relativos `.md` do repositório;
  e revisão por subagente fresco, que não viu a implementação. Lint, teste e build não existem no
  projeto.
- **Escopo efetivo** — passou do previsto em quatro pontos, todos da mesma classe: prosa que a
  remoção tornou **falsa**. (1) As três intents abertas argumentavam em cima do índice duplicado —
  `escolher-entre-arquivos-e-issues` defendia arquivo por "detecção de erro", que era exatamente o
  argumento invertido; `governanca-em-issues-neste-repo` vendia issues por "índice gerado", que
  deixou de ser diferencial; `a-entrada-de-quem-chega` apoiava uma bala no passo 5. (2) A versão e
  as descrições em `.claude-plugin/*.json`, que o `grep --include='*.md'` da spec não alcançava.
- **Lições**
  - **Renumerar um passo quebra quem cita o número de fora.** O passo 4 virou 3, e quatro
    referências externas ficaram apontando para o lugar errado — a pior em
    `skills/setup/templates/claude-md.md`, que vai para o `CLAUDE.md` de todo projeto novo e é lido
    inteiro em toda sessão. Nenhum grep por "checklist" as pegaria: elas citam o **número**.
  - **A mesma receita escrita de três jeitos é a deriva que a demanda combate.** O comando
    `head -qn1 ...` nasceu com três conjuntos de caminhos diferentes em cinco arquivos. Unificado.
  - **Número em prosa se pina num commit, não numa data.** "Em 44 commits" virou 45 no dia
    seguinte; `git log --oneline ddc7477 | wc -l` reproduz para sempre.
- **Promoção** — [ADR 0003 — um item, um lugar](../../adr/0003-um-item-um-lugar.md), que
  supersede o 0002; e duas regras no `CLAUDE.md`, ambas vindas da revisão: passo citado por número
  é ponteiro (com o `grep` que o confere), e número tirado do histórico do git se pina num commit.
  Nenhum doc de referência, skill ou regra de `paths:` saiu desta demanda. No `ROADMAP.md`, nada a
  ajustar: os dois itens de `Próximas` não foram tocados nem tornados obsoletos.
