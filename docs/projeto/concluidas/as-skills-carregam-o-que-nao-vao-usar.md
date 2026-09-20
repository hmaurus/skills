# As skills carregam o que não vão usar

Processo — entrevista: criar-spec · implementação: aicf-plan

## Problema

Uma revisão das seis skills em 2026-09-19 achou treze pontos, em quatro grupos. Nenhum é regra
errada: são texto que o agente paga para ler e não usa, três casos que nenhuma skill executa, e três
trechos que ficaram longe do que explicam.

**Custo por invocação hoje** (`wc -c skills/*/SKILL.md skills/workflow-demanda/references/*.md`):

| Arquivo | Bytes |
| --- | --- |
| `setup/SKILL.md` | 13.667 |
| `workflow-demanda/references/midia.md` | 12.747 |
| `workflow-demanda/SKILL.md` | 11.289 |
| `fechar-demanda/SKILL.md` | 9.098 |
| `criar-spec/SKILL.md` | 4.963 |
| `criar-prd/SKILL.md` | 4.273 |
| `implementar-spec/SKILL.md` | 4.043 |
| **Total** | **60.080** |

### 1. O `midia.md` entrega as duas receitas a quem só usa uma

A mídia é escolhida no setup e não muda. Mesmo assim, quem abre o `midia.md` no modo arquivo carrega
as seções que só existem para issue — gotcha do `--label`, índice atrasado, criar labels, adotar
issue, `gh` indisponível —, que somam 5.666 bytes dos 12.747
(`awk '/^### O gotcha/,/^## A linha/' skills/workflow-demanda/references/midia.md | head -n -1 | wc -c` +
`awk '/^## Criar os labels/,/^## Divergência/' skills/workflow-demanda/references/midia.md | head -n -1 | wc -c`).
A receita do modo arquivo inteira cabe na coluna de uma tabela: `git mv`, escrever no fim do arquivo,
`grep` dos links. E o modo issue paga o inverso, menor.

Parte do arquivo não é instrução: as medições que provaram os dois comportamentos do `gh` (o exemplo
em `denoland/deno`, "4 de 6 rodadas") são evidência para quem mantém o plugin, e já estão na entrada
da `0.17.0` do `CHANGELOG.md` (`grep -c 'denoland' CHANGELOG.md` → 1). O agente precisa da regra e do
comando.

### 2. O mesmo texto em vários arquivos

- **O parágrafo de mídia em `criar-spec`, `implementar-spec` e `fechar-demanda`** — "onde mora depende
  da mídia, linha ausente significa arquivo, receita em `midia.md`, se `issue-tracker.md` discorda
  avisar uma vez" — está quase idêntico nos três (`grep -c 'discorda' skills/*/SKILL.md`). A revisão
  da `0.17.0` pôs o aviso de divergência nas três de propósito, porque no modo arquivo o `midia.md`
  não é aberto; o alcance fica, o tamanho não precisa.
- **"Linha ausente significa arquivo"** está em sete arquivos
  (`grep -rl 'inha ausente significa arquivo' --include='*.md' skills/ README.md | wc -l`).
- **A tabela dos quatro estados** está em `workflow-demanda/SKILL.md` e no `midia.md`
  (`grep -rl 'Incerto — nem se sabe' skills/ | wc -l` → 2).
- **A linha `Processo`** está especificada em `fechar-demanda`, exemplificada em `criar-spec` e
  repetida com a variante de issue no `midia.md`.

### 3. Três casos sem operador

- **Pular a entrevista.** O `workflow-demanda` diz que a demanda "muda de estado para pronta para
  implementar como está" e grava `entrevista: nenhuma`. Nenhuma skill faz isso: `criar-spec` é a
  entrevista, e `implementar-spec` só lê specs (`grep -l 'entrevista: nenhuma' skills/*/SKILL.md`
  devolve só `fechar-demanda`, e ali é exemplo de formato).
- **Respostas do setup sem lugar.** As perguntas sobre gerenciador de senhas e fonte de documentação
  são gravadas "nas seções de segurança e de dependências dos padrões de engenharia". Quem responde
  "nenhum dos dois" para os padrões não tem essas seções, e as duas respostas somem.
- **A apresentação promete "cerca de seis" perguntas.** São sete: nome, descrição, mídia, padrões e
  três ferramentas (`grep -c 'cerca de seis' skills/setup/SKILL.md` → 1).

### 4. Três trechos longe do que explicam

- Em `criar-spec`, a lista das cinco seções da spec vem depois de vinte linhas sobre mídia e estado,
  sem heading — o leitor não sabe que aqueles itens são o conteúdo da spec.
- Em `setup`, o parágrafo que manda copiar os templates trocando `<NOME>` ficou abaixo da subseção
  dos labels, longe da tabela de templates, numa frase só de sessenta palavras.
- Em `implementar-spec`, a primeira linha do corpo fala de plan mode antes de qualquer heading, e o
  passo 3 é onde o plan mode se decide.

## Solução

Uma demanda só, com as entregas em checkboxes; a sessão faz o que cabe e fecha parcial se precisar.

### O `midia.md` vira um arquivo por mídia

- [x] `references/midia.md` deixa de existir. Nascem `references/midia-arquivo.md` e
      `references/midia-issues.md`, cada um com a coluna da sua mídia da tabela "Operação por
      operação" e o que só vale nela: o de arquivo leva a correção de links após `git mv`; o de issue
      leva `--body-file`, os dois gotchas do `gh` (só regra e comando, sem as medições), criar labels,
      adotar issue, `gh` indisponível, e as duas particularidades da linha `Processo` (primeira linha
      do corpo; sem o número da própria issue).
- [x] O que é comum às duas mídias fica só em `workflow-demanda/SKILL.md`, que já o tem: a linha de
      configuração e o fallback, a tabela dos quatro estados, "um item, um lugar", o que não muda com
      a mídia. A seção "Divergência com o tracker do Matt Pocock" vai para lá também, resumida a um
      parágrafo. O `workflow-demanda` aponta para os dois arquivos: "os comandos estão no arquivo da
      mídia que a linha nomeia".
- [x] Uma terceira mídia passa a ser um terceiro arquivo, não uma terceira coluna. A decisão do
      [ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md) fica de pé — config na linha do
      `CLAUDE.md`, skills neutras, comando concreto num lugar só por mídia —; só a forma da referência
      muda, e isso vai na entrada do `CHANGELOG.md`, sem ADR novo: é reversível num `cat`.

### As skills apontam, em vez de repetir

- [x] Em `criar-spec`, `implementar-spec`, `fechar-demanda` e `criar-prd`, o parágrafo de mídia vira
      duas frases: uma que aponta — "a linha `Mídia do registro` do `CLAUDE.md` diz qual arquivo de
      `workflow-demanda/references/` seguir; sem linha, `midia-arquivo.md`" — e uma que mantém o
      alcance do aviso de divergência: "se `docs/agents/issue-tracker.md` discordar da linha, avisar
      uma vez e seguir a linha". A justificativa do aviso ("divergir é legítimo, mas precisa ser
      escolha") fica só no `workflow-demanda`.
- [x] O `setup` mantém a explicação do fallback (é ele quem grava a linha e precisa dizer por quê); os
      links dele para o `midia.md` passam a apontar para `midia-issues.md`, que é onde estão os
      labels.
- [x] A linha `Processo`: `fechar-demanda` segue sendo a especificação; `criar-spec` mantém só a
      linha de exemplo que ele grava; o resto sai.

### Os três casos ganham dono

- [x] `implementar-spec`, passo 1, ganha o caso: alvo que ainda é intent (arquivo em `intents/`,
      linha do `ROADMAP.md`, ou issue `aicf:intent`) e o usuário manda implementar sem entrevista →
      virar spec pela receita da mídia, com `entrevista: nenhuma` na linha `Processo`, e seguir. O
      texto do `workflow-demanda` que declara o caso legítimo não muda.
- [x] `setup`: as perguntas 1 e 2 de "Ferramentas que o usuário já usa" só acontecem quando os
      padrões de engenharia vão para algum lugar (global ou projeto). Quem escolheu "nenhum dos dois"
      declarou que já tem os seus, e é lá que essas respostas morariam. A pergunta 3 fica sempre:
      ela vai para "Processos de desenvolvimento".
- [x] A apresentação diz "entre cinco e sete perguntas", que é o que a ramificação acima produz.

### Os três trechos voltam para perto do que explicam

- [x] `criar-spec`: a seção "A spec" abre com a lista das cinco seções, sob o heading; o material de
      mídia e de mudança de estado desce para um subheading "Onde ela mora".
- [x] `setup`: o parágrafo de cópia dos templates fica logo abaixo da tabela de templates, em duas ou
      três frases; a subseção dos labels vem depois dele.
- [x] `implementar-spec`: a linha solta sobre plan mode sai do topo e entra no ramo `aicf-plan` do
      passo 3, que é onde o plan mode é ligado.

## Arquivos e interfaces

- `skills/workflow-demanda/references/midia.md` → apagado; nascem `midia-arquivo.md` e
  `midia-issues.md` na mesma pasta.
- `skills/workflow-demanda/SKILL.md` — absorve a divergência com o Matt e aponta para os dois
  arquivos.
- `skills/criar-spec/SKILL.md`, `skills/implementar-spec/SKILL.md`, `skills/fechar-demanda/SKILL.md`,
  `skills/criar-prd/SKILL.md` — parágrafo de mídia encolhido; os três primeiros com os ajustes de
  colocação e de operador.
- `skills/setup/SKILL.md` — links, perguntas condicionais, contagem, colocação do parágrafo de cópia.
- `CHANGELOG.md` e `.claude-plugin/plugin.json` — versão nova, no commit de código.
- Interface pública intocada: a linha `Mídia do registro` e seus dois valores, os três labels, a
  linha `Processo`. O que muda é só o caminho de uma referência interna; `CHANGELOG.md` e ADR 0004
  seguem citando `midia.md` como histórico, e isso não é link relativo, então o check de links não
  acusa.

## Fora de escopo

- **As seções "Lema" e "Registro" do template `claude-md.md`, e o par `develop`/`main` da seção
  Git.** Entram em todo projeto novo, mesmo quando o usuário não quis padrões de engenharia, e
  custam ~1.100 tokens em toda sessão. É decisão de método — o que o plugin considera governança
  mínima —, não de escrita, e vira demanda própria se o autor quiser rever.
- **As quatro linhas de detalhe de ramo no `workflow-demanda`** (o heading `## Task N` do Superpowers
  e o `/setup-matt-pocock-skills`). Movê-las para um arquivo de referência de coleções custaria um
  arquivo novo para poupar ~80 tokens. Ficam.
- **Migrar alguma coisa deste repositório.** A mídia dele segue arquivo; a demanda
  [governança em issues neste repo](../intents/governanca-em-issues-neste-repo.md) é outra.

## Verificação

1. **Custo.** `wc -c skills/*/SKILL.md skills/workflow-demanda/references/*.md | tail -1` → total
   ≤ 56.500 bytes (hoje 60.080). E o que o modo arquivo carrega ao abrir a referência:
   `wc -c < skills/workflow-demanda/references/midia-arquivo.md` → ≤ 3.000 (hoje 12.747, no arquivo
   único).
2. **Repetição.** `grep -c 'discorda' skills/*/SKILL.md` → no máximo 1 linha por skill;
   `grep -rl 'Incerto — nem se sabe' skills/ | wc -l` → 1; `grep -rl 'denoland' skills/ | wc -l` → 0;
   `ls skills/workflow-demanda/references/` → `midia-arquivo.md midia-issues.md`, e nada mais.
3. **Operadores.** `grep -l 'entrevista: nenhuma' skills/implementar-spec/SKILL.md` acha;
   `grep -c 'cerca de seis' skills/setup/SKILL.md` → 0.
4. **Ponta a ponta, modo arquivo, nesta sessão ou na seguinte:** num intent deste repositório,
   pedir "implementa sem entrevista" e observar o agente fazer o `git mv` e gravar
   `entrevista: nenhuma` sem abrir `midia-issues.md`. Depois, `./scripts/check.sh` → `Tudo verde.`
   (os sete links para `midia.md` foram trocados; um esquecido aparece aqui).
5. **O que o agente não verifica.** `setup` tem `disable-model-invocation: true`: a ramificação das
   perguntas e a contagem só se confirmam com o usuário rodando `/aicf:setup` num diretório
   descartável, escolhendo "nenhum dos dois" e conferindo que as perguntas de senha e documentação
   não vêm. O relatório registra se isso aconteceu ou fica em aberto.

## Relatório de implementação (2026-09-19)

- **Status** — concluído. Valida o run 35476857251 do CI (`gh run list --workflow=ci.yml --limit 1`).
- **Arquivos alterados** — `skills/workflow-demanda/references/midia.md` apagado; `midia-arquivo.md`
  e `midia-issues.md` criados na mesma pasta; `workflow-demanda/SKILL.md` (ponteiro para os dois,
  divergência com o Matt, o comum que só existia no `midia.md`); `criar-spec`, `implementar-spec`,
  `fechar-demanda` e `criar-prd` (parágrafo de mídia em duas frases; operador do "sem entrevista";
  colocação); `setup/SKILL.md` (perguntas condicionais, contagem, links, colocação);
  `.claude-plugin/plugin.json` e `CHANGELOG.md` (0.20.0).
- **Commits** — `23c924e` a spec; `06f09a7` o código. Os dois foram reescritos antes do push: o
  primeiro par tinha a remoção do `midia.md` no commit da spec, e o commit intermediário ficava com
  sete links quebrados.
- **Validação** — `./scripts/check.sh` verde nos dois commits, cada um extraído com `git archive` e
  conferido isolado. Os pontos da Verificação da spec:
  1. Total das skills e referências: **56.556 bytes**, contra o alvo de 56.500 — não bateu, por 56.
     A spec afirmava que o comum do `midia.md` "já estava no `workflow-demanda`", e a revisão
     mostrou três trechos que não estavam (o comando que lê a configuração, "não existe modo misto",
     o passo 3 valendo nas duas mídias); devolvê-los, mais as duas frases que faltavam no
     `criar-prd`, custou 527 bytes sobre os 56.029 medidos antes da revisão. Referência do modo
     arquivo: 1.585 bytes, abaixo dos 3.000.
  2. `discorda` no máximo uma vez por skill; a tabela dos quatro estados num arquivo só;
     `denoland` em nenhum; `references/` com os dois arquivos e nada mais.
  3. `entrevista: nenhuma` no `implementar-spec`; `cerca de seis` em lugar nenhum.
  4. Check verde. O ponta a ponta do "sem entrevista" **não rodou** nesta sessão; encerra na primeira
     demanda deste repositório que partir de um intent com "implementa sem entrevista".
  5. A ramificação das perguntas do `setup` **fica em aberto**: `disable-model-invocation` impede o
     agente de rodar; encerra quando o usuário rodar `/aicf:setup` num diretório descartável,
     responder "nenhum dos dois" e as perguntas de senha e documentação não vierem.
  - Revisão de código por subagente que não viu a implementação, sobre o commit de código: quatro
    achados, todos procedentes, corrigidos antes do push — a remoção no commit errado; os três
    trechos sem destino; o `criar-prd` fora das duas frases que a spec pedia; e, no CHANGELOG, a
    base do "60.080" sem sha e um "que já o tinha" falso.
- **Escopo efetivo** — além do previsto: os parágrafos do `setup` sobre `CLAUDE.md` existente e
  `/init` subiram junto com o de cópia, senão ficariam sob a subseção dos labels; o link geral do
  `setup` aponta para os dois arquivos, não só para `midia-issues.md`; a receita de arquivo diz o
  que fazer com a linha do `ROADMAP.md` ao virar spec.
- **Lições** — `git rm` deixa a remoção no índice, e `git add <arquivo>` seguido de commit a
  leva junto: conferir `git diff --cached --stat` antes de um commit seletivo. Afirmação sobre o
  que "já existe" em outro arquivo pede o `grep` na spec, não a memória da leitura. E o `git mv`
  desta spec para `concluidas/` quebrou dois links **de dentro dela**, que o CI do commit de
  fechamento acusou (run 35476882735): o `grep` do passo 2 acha quem aponta para o arquivo, não o
  que o arquivo aponta — e ler só a última linha do check, em vez do exit code, deixou passar.
- **Promoção (passo 3)** — a lição do `midia.md` virou regra no `CLAUDE.md`: referência que o
  agente carrega leva regra e comando; a medição vai para o CHANGELOG ou para a spec. Dois números
  do backlog mudaram com esta demanda e foram ajustados inline
  ([o setup não avisa que o Matt pergunta o mesmo](../backlog/o-setup-nao-avisa-que-o-matt-pergunta-o-mesmo.md),
  [o ciclo nunca rodou em outro agente](../backlog/o-ciclo-nunca-rodou-em-outro-agente.md)).
  Nenhum ADR, skill ou termo de glossário.
