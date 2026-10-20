# O PRD envelhece sem ninguém conferir

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

O PRD se diz "documento vivo" (`skills/setup/templates/prd.md`), mas nada no ciclo confere se ele
continua verdadeiro. O `/aicf:criar-prd` tem um **modo revisão**, só que ele lê o PRD e entrevista
o que o usuário diz ter mudado: não confronta o texto com o que foi implementado, com as demandas
abertas nem com os ADRs. E o nome "criar" não diz a quem quer atualizar o PRD que é ali que se faz
isso.

**Caso de origem, num projeto privado que consome estas skills.** O PRD tinha sido revisado 13 dias
antes, e o desenvolvimento andou mais rápido que ele. O titular adiantou itens que o PRD listava
como "fora do MVP", e o PRD ainda trazia um risco com data vencida. O `/aicf:proxima-demanda` usa
o PRD como régua da prioridade (`grep -n 'PRD' skills/proxima-demanda/SKILL.md`), então um PRD
defasado leva a uma ordem errada. Quem percebeu foi o titular, não o ciclo.

**O PRD deste repositório tem o mesmo sintoma.** A Proposta diz "Seis skills"
(`grep -n 'Seis skills' docs/projeto/PRD.md`), mas `ls skills/*/SKILL.md | wc -l` dá 7, porque o
`/aicf:proxima-demanda` entrou e o PRD não acompanhou. A linha **Última revisão** está em
2026-09-19, e o commit que mexeu no PRD em 2026-10-06 (`fcff2da`, a troca de nome do glossário) não
a mudou: ninguém conferiu o conteúdo.

E nenhuma skill do ciclo cita o PRD no fechamento (`grep -c 'PRD' skills/fechar-demanda/SKILL.md`
→ 0): uma demanda que contraria o PRD fecha sem aviso.

## Solução

**Uma skill só para o PRD, chamada `/aicf:prd`**, que cria o PRD ou o atualiza, conforme o estado
do arquivo. A invocação continua só do usuário (`disable-model-invocation: true`), para a
description não ocupar o contexto de toda sessão. Quem lembra o usuário de rodá-la são o
fechamento e a próxima demanda, cada um com uma frase.

### 1. `/aicf:criar-prd` passa a ser `/aicf:prd`

`git mv skills/criar-prd skills/prd`, `name: prd`, e a description diz os dois usos: criar quando o
PRD está vazio, atualizar quando já existe, conferindo-o contra o que o projeto fez. O título da
skill e a frase "Não confundir com `/aicf:criar-spec`" acompanham.

### 2. A revisão lê o projeto antes de perguntar

O modo revisão ganha um passo antes da primeira pergunta. O agente confronta o PRD com o
repositório, pela mídia do registro (a linha `**Mídia do registro:**` do `CLAUDE.md`, como a skill
já faz no fim):

- **Escopo, Dentro** — item cuja demanda já está concluída; item que ainda não tem demanda nenhuma.
- **Escopo, Fora** — item que voltou como demanda aberta (`ROADMAP.md`, `intents/`, `specs/`,
  `backlog/`, ou issue `aicf:*` aberta) ou que já foi concluído.
- **Riscos** — data ou condição que já passou.
- **Público e Modelo** — contra o `GLOSSARY.md` e os ADRs: termo trocado, decisão de modelo
  registrada fora do PRD.
- **Afirmação verificável do PRD** — número, nome de comando ou lista que o repositório desmente
  (o "Seis skills" deste repositório é o exemplo).
- **O ponteiro antigo** — o cabeçalho que o template gravou ("revisar por `/aicf:criar-prd`") vira
  `/aicf:prd`, sem perguntar.

O resultado aparece **antes da entrevista**, seção por seção, cada divergência com a fonte (arquivo
da demanda, issue, ADR, commit) e separada em dois grupos:

- **Fato**, que o agente corrige sozinho no texto proposto: contagem, nome, risco cuja data passou
  sem ter acontecido.
- **Decisão**, que só o usuário responde, e é o que vai para a entrevista: se a mudança de escopo
  foi decisão ou deriva, o motivo de um item novo em Fora, as metas de Sucesso, o que fazer com um
  risco vencido.

Depois da entrevista, a skill mostra o texto novo de cada seção que muda, grava só com aprovação e
atualiza a **Última revisão**. Seção sem divergência e sem pergunta do usuário não é reescrita, como
já é hoje.

### 3. O fechamento sugere a revisão

No passo 4 do `/aicf:fechar-demanda`, ao lado de "criou demanda nova ou tornou alguma obsoleta?",
uma frase: se a demanda contraria o PRD — entrou no que ele diz Fora, mudou Escopo, Público ou
Modelo, resolveu ou criou um Risco —, sugerir ao usuário rodar `/aicf:prd`. O fechamento não edita
o PRD.

### 4. A próxima demanda avisa

No `/aicf:proxima-demanda`, que já lê o PRD como régua, uma frase: demanda aberta que o PRD lista em
Fora, ou Risco com data vencida, faz a resposta avisar que a régua está defasada e sugerir
`/aicf:prd` antes de seguir a ordem. O critério é o conteúdo, não a idade da revisão (ver Fora de
escopo).

### 5. O nome novo onde o antigo era citado

Fora o histórico, que não muda (`CHANGELOG.md`, `docs/projeto/concluidas/`, ADRs, que são imutáveis,
e `docs/notas-de-sessao/`), `/aicf:criar-prd` vira `/aicf:prd` em todo arquivo vivo. Na mesma
passada, a contagem de skills dos dois READMEs ("São seis skills", "There are six skills") vira sete.
O "Seis skills" do PRD fica para a verificação (abaixo).

## Arquivos e interfaces

- `skills/criar-prd/` → `skills/prd/` — `SKILL.md`: frontmatter (`name`, `description`), título,
  seção *Onde ele fica* (o passo de leitura do modo revisão) e *Ao terminar* (gravar com aprovação,
  datar a revisão)
- `skills/fechar-demanda/SKILL.md` — uma frase no passo 4
- `skills/proxima-demanda/SKILL.md` — uma frase no passo 1 (o item do `PRD.md`) ou no passo 3
- `.claude-plugin/plugin.json` — o caminho `./skills/criar-prd` vira `./skills/prd`, e a versão sobe
  para `0.40.0`
- `CHANGELOG.md` — entrada `0.40.0` no topo
- Referências ao nome antigo: `skills/setup/SKILL.md`, `skills/setup/templates/prd.md`, `README.md`,
  `README.en.md`, `.claude/CLAUDE.md` (a regra do `disable-model-invocation`),
  `.claude/rules/templates.md`, `docs/projeto/PRD.md` (só o ponteiro do cabeçalho),
  `docs/projeto/backlog/o-ciclo-nunca-rodou-em-outro-agente.md`

Hoje são dez arquivos vivos que citam o nome antigo:

```
grep -rl 'criar-prd' --exclude-dir=.git . | grep -vE '^(\./)?(CHANGELOG\.md|docs/projeto/concluidas/|docs/adr/|docs/notas-de-sessao/|docs/projeto/(intents|specs)/o-prd-envelhece)' | sort
```

## Fora de escopo

- **O agente invocar a skill sozinho**, inclusive ao perceber na conversa uma mudança de regra ou de
  estratégia. Motivo: a description passaria a ocupar o contexto de toda sessão, e o gatilho
  dispararia no meio de outra demanda, contra a regra de registrar a ideia e voltar ao que se fazia.
  O fechamento e a próxima demanda cobrem os dois momentos em que a divergência já é fato.
- **Aviso pela idade da revisão** (N demandas concluídas desde a Última revisão). Motivo: o titular
  escolheu o critério por conteúdo, e a contagem pelo git não serve neste layout. O achatamento das
  pastas (`9be56e3`, 2026-09-20) moveu todas as demandas, e
  `git log --since=2026-09-19 --diff-filter=AR --name-only --format= -- docs/projeto/concluidas/ | grep -c '\.md$'`
  conta 38, o mesmo que `ls docs/projeto/concluidas/*.md | wc -l`.
- **O fechamento editar o PRD.** O PRD guarda decisões do titular, e a entrevista delas é da
  `/aicf:prd`. O fechamento só aponta.
- **Uma skill `atualizar-prd` ao lado da de criar.** Seriam dois mecanismos para o mesmo arquivo.
- **Manter `criar-prd` como segundo nome.** Pelo mesmo motivo. Os projetos que já têm o ponteiro
  antigo no PRD se corrigem na primeira revisão, e as notas da release avisam a mudança de nome.
- **Revisar o conteúdo do PRD deste repositório nesta demanda.** Fica para o primeiro uso real da
  `/aicf:prd`, que é a verificação de comportamento dela.

## Verificação

1. `./scripts/check.sh` → `Tudo verde.` Ele também valida o caminho novo no `plugin.json` e acusa
   link relativo quebrado pela renomeação.
2. O comando de *Arquivos e interfaces* lista só `skills/prd/SKILL.md`, que cita o nome antigo
   para trocá-lo no PRD dos projetos.
3. `test -d skills/criar-prd` falha, e
   `grep -c '^disable-model-invocation: true' skills/prd/SKILL.md` → 1.
4. **Comportamento da `/aicf:prd`, em aberto.** Ela tem `disable-model-invocation: true`, e o
   agente não a verifica. Encerra quando o titular, com o plugin atualizado e a sessão reiniciada
   (cabeçalho do comando em `cache/aicodingflow/aicf/0.40.0/skills/prd`), rodar `/aicf:prd` neste
   repositório e a lista de divergências trouxer, antes da primeira pergunta, pelo menos o "Seis
   skills" da Proposta contra `ls skills/*/SKILL.md | wc -l` → 7, e o ponteiro antigo do cabeçalho.
   A revisão gravada no `PRD.md` fica como registro.
5. **Os avisos do fechamento e da próxima demanda, em aberto até o uso real.** São frases curtas
   em skills que o titular invoca. Encerram no primeiro uso em que uma demanda aberta esteja no Fora
   do PRD, ou em que uma demanda concluída o contrarie, e o aviso apareça.

## Relatório de implementação (2026-10-19)

- **Status** — concluído no código; a verificação de comportamento segue em aberto (itens 4 e 5 da
  Verificação), com quem a encerra abaixo.
- **Arquivos alterados**
  - `skills/criar-prd/` → `skills/prd/` — `name`, description com os dois usos, a seção nova
    *Modo revisão: conferir o PRD contra o projeto* e o *Ao terminar* da revisão
  - `skills/fechar-demanda/SKILL.md` — uma frase no passo 4
  - `skills/proxima-demanda/SKILL.md` — uma frase no item do `PRD.md` (passo 1) e um item no passo 3
  - `.claude-plugin/plugin.json` — caminho da skill e versão `0.40.0`; `CHANGELOG.md` — entrada `0.40.0`
  - O nome novo em `README.md`, `README.en.md`, `skills/setup/SKILL.md`,
    `skills/setup/templates/prd.md`, `.claude/CLAUDE.md`, `.claude/rules/templates.md`,
    `docs/projeto/PRD.md` (só o cabeçalho) e no item de backlog do ciclo em outro agente
- **Commits**
  - `2c3819c` docs(projeto): spec para o PRD que envelhece sem ninguém conferir
  - `b09fb95` feat(prd)!: 0.40.0 — criar-prd vira prd, e a revisão confere o PRD contra o projeto
  - `8209bd6` fix(prd): achados da revisão — issues fechadas sem label, risco vencido é decisão,
    aviso no passo 3
- **Validação**
  - `./scripts/check.sh` → `Tudo verde.` depois de cada commit.
  - Verificação 2: o comando de *Arquivos e interfaces* lista só `skills/prd/SKILL.md`.
  - Verificação 3: `test -d skills/criar-prd` sai com 1, e
    `grep -c '^disable-model-invocation: true' skills/prd/SKILL.md` → 1.
  - Revisão de código por subagente que não viu a implementação, sobre `b09fb95`. Os achados
    aplicados em `8209bd6`: no modo issue, o filtro por `aicf:*` não acha issue fechada, porque o
    label sai no fechamento (`skills/midia/issues.md`), e o `gh issue list` corta em 30
    (`gh issue list --help | grep -- --limit`); risco vencido aparecia como fato e como decisão; o
    aviso da próxima demanda estava no passo 1 e faltava no 3, que monta a resposta; "São seis" no
    segundo parágrafo dos dois READMEs; o item de backlog contava duas skills manuais, e são três.
  - **Encerrada em 2026-10-19 — `/aicf:prd`** (`disable-model-invocation: true`, o agente não
    verifica). O titular rodou `/aicf:prd` neste repositório na `0.40.1`, depois de
    `/reload-plugins`, com o estado em `441a74b`. Antes da primeira pergunta, a tabela de fatos
    trouxe o "Seis skills" da Proposta contra `ls skills/*/SKILL.md | wc -l` → 7, cada linha com a
    fonte, e as decisões vieram separadas, uma pergunta por vez. A passada também achou o que a spec
    não previa: "framework" contra o verbete "Coleção de skills" do `GLOSSARY.md`, o "cerca de
    vinte pontos" do Fora (o `grep` do próprio PRD dá 23), e um risco que já aconteceu (o Claude
    Code 2.1.292, em 2026-10-06).
  - **Em aberto — avisos do fechamento e da próxima demanda.** Encerram no primeiro uso real em que
    uma demanda aberta esteja no Fora do PRD, ou uma concluída o contrarie, e o aviso apareça.
- **Escopo efetivo**
  - Plano × entrega: a spec punha "risco cuja data passou" no grupo Fato; a revisão mostrou que
    manter, remover ou reescrever o risco é decisão do usuário, e ele foi para o grupo Decisão.
  - A revisão também pediu os comandos do modo issue que a spec não detalhava.
  - O *Ao terminar* da revisão passou a propor demanda para item de Escopo sem demanda, o que a
    spec listava como conferência, mas não como saída.
- **Lições** — renomear skill deixa contagem em mais de um lugar do README: a linha 7 foi trocada
  pelo `sed` e o "São seis." do segundo parágrafo, não; quem pegou foi a revisão.
- **Promovido** — nada para `CLAUDE.md`, ADR ou glossário. O limite de 30 do `gh issue list` nas
  outras skills virou item de Backlog no `ROADMAP.md` ("A listagem de issues corta em 30 sem
  avisar").
