# Verificação de comportamento do `/aicf:setup`

O que cada passada tem que provar, o que já passou, e o que ainda não rodou.

## Por que este doc existe

O `skills/setup/SKILL.md` tem `disable-model-invocation: true`: o harness recusa a invocação e também
imitar o roteiro por fora. **Nenhum agente verifica essa skill** — quem roda é o titular, e a demanda
que a altera fecha com a verificação em aberto e nomeada.

Isso se repete a cada mudança do setup, e a condição de aceite acabou espalhada por quatro demandas
concluídas. Aqui ela fica junta.

## Antes de qualquer passada

1. `/plugin update`, e **sessão nova** — a skill que roda é a carregada no início da sessão, não a do
   disco.
2. Conferir o cabeçalho do comando: `cache/aicodingflow/aicf/<versão>/skills/setup`. Sem isso, a
   passada pode estar exercitando a versão anterior.
3. **Diretório novo.** O setup roda uma vez por projeto, e não migra projeto que já tem governança.

## O que cada ramo prova

### Modo arquivo

```bash
git log --oneline | wc -l                    # 1
git show --stat --name-only HEAD             # só o que o setup escreveu
git branch --show-current                    # develop
git branch --format='%(refname:short)'       # develop, main
ls docs/projeto/                             # PRD.md, ROADMAP.md e as quatro pastas
grep '^\*\*Coleções' CLAUDE.md               # "Superpowers" uma vez só na linha
grep -n 'develop' CLAUDE.md                  # a seção Git descreve o que existe
sed -n '/^## Próximas/,/^## /p' docs/projeto/ROADMAP.md | grep -c '^- \[ \]'  # 0

T=~/.claude/plugins/cache/aicodingflow/aicf/<versão>/skills/setup/templates
for p in "CLAUDE.md claude-md.md" "README.md readme.md" \
         "docs/projeto/PRD.md prd.md" "docs/projeto/ROADMAP.md roadmap.md"; do
  set -- $p; diff "$T/$2" "$1"
done   # só nome, descrição, as duas linhas do CLAUDE.md, e o bloco de escolha do README apagado
```

**O `diff` é o comando que pega defeito de template**, e é o único do bloco cuja resposta esperada
não é um valor fixo — quem roda lê as diferenças e julga se são só as quatro do comentário. Ele está
aqui porque os três defeitos que esta verificação já achou de verdade (2026-09-20, viraram a
`0.23.1`) eram todos de conteúdo de template: com eles no lugar, os oito comandos acima passariam
verdes. O `diff` também pega o inverso, que nenhum `grep` pega — uma substituição que o setup fez e
não devia.

### Modo issue

```bash
gh label list | grep -c '^aicf:'                                # 3
git log origin/main --oneline | wc -l                           # 1 — o --push funcionou
gh repo view --json defaultBranchRef -q .defaultBranchRef.name  # main
git branch --show-current                                       # develop
ls docs/projeto/                                                # só PRD.md

T=~/.claude/plugins/cache/aicodingflow/aicf/<versão>/skills/setup/templates
for p in "CLAUDE.md claude-md.md" "README.md readme.md" "docs/projeto/PRD.md prd.md"; do
  set -- $p; diff "$T/$2" "$1"
done   # só nome, descrição, as duas linhas do CLAUDE.md, e o bloco de escolha do README apagado

gh repo delete <nome> --yes                                     # o repositório de teste é descartável
```

São três pares, e não os quatro do modo arquivo: neste ramo o `roadmap.md` não é copiado, como a
tabela "O que criar" do roteiro marca. O `diff` do `README.md` mostra um bloco maior que no modo
arquivo — aqui sobra a linha única das issues no lugar das cinco das pastas.

O repositório sai da máquina, então é privado e some no fim. `gh label list` num repositório criado
pelo próprio setup é a condição que encerra o ramo issue.

**O `gh repo delete` é o último passo, e só depois de a passada ter sido avaliada.** Metade das
condições — os labels e o default branch — só existe enquanto o repositório existe; apagá-lo junto
com o resto do bloco destrói a evidência antes de alguém a ler.

**O agente consegue avaliar a passada sozinho, com o caminho do diretório.** O transcript da sessão
fica em `~/.claude/projects/<caminho-com-barras-virando-hífen>/*.jsonl` — extrair com `jq`, nunca ler
inteiro, que passa de meio megabyte:

```bash
jq -r 'select(.type=="user") | (.message.content | if type=="string" then . else (map(select(.type=="text").text)|join(" ")) end) | select(length>0)' <arquivo>.jsonl
```

A primeira linha do bloco da skill traz a versão que de fato rodou
(`cache/aicodingflow/aicf/<versão>/skills/setup`), que é a conferência do passo 2 sem depender de
ninguém ter olhado o cabeçalho na hora.

## O que já passou

| Quando | Ramo | Versão | Resultado |
| --- | --- | --- | --- |
| 2026-09-20 | arquivo | `0.23.0` | **passou** — um commit, só os caminhos criados, `git init` oferecido antes da pergunta da mídia, e a pergunta da mídia feita com a opção issue dizendo o que faltava |
| 2026-09-21 | issue | `0.24.0` | **passou** — os cinco comandos do bloco acima, num repositório que o próprio setup criou; `git ls-tree -r HEAD` traz só os quatro caminhos do setup, com `AGENTS.md` em modo `120000` |
| 2026-09-21 | arquivo | `0.24.0` | **passou** — os oito comandos do bloco acima, num diretório vazio onde o próprio setup rodou o `git init`; `ROADMAP.md` e o par `develop`/`main`, que eram o que faltava, conferidos |

**A passada de 2026-09-20 achou três defeitos que nenhuma revisão tinha achado** — todos nos
templates, nenhum no roteiro. Viraram a `0.23.1`
([os templates contradizem o projeto que nasce](../projeto/concluidas/os-templates-contradizem-o-projeto-que-nasce.md)).
É o argumento para rodar a passada de verdade em vez de confiar em leitura: o `check.sh` estava
verde, e um subagente tinha revisado o diff inteiro.

**A passada de 2026-09-21 no ramo issue não achou defeito nos arquivos gerados** — `CLAUDE.md`,
`README.md` e `PRD.md` batem com os templates, com a linha da mídia, a das coleções e a seção Git
corretas. Achou quatro desvios do roteiro, nenhum com consequência no resultado, todos no transcript
(`~/.claude/projects/-home-mh-dev-tmp-teste-aicf-issues/*.jsonl`):

1. A pergunta da mídia saiu com **issue como primeira opção**, e o roteiro marca arquivo como
   default. O diretório se chamava `teste-aicf-issues`, o que provavelmente enviesou.
2. Mídia e padrões de engenharia saíram numa **única chamada de `AskUserQuestion`**; o roteiro
   descreve duas.
3. As três perguntas de ferramentas saíram **juntas e já pré-respondidas** a partir do
   `~/.claude/CLAUDE.md` global, contra o "perguntar uma de cada vez, em pergunta aberta" do
   roteiro. Funcionou melhor que o roteiro: o global já respondia às três.
4. O passo "Carregar `/aicf:workflow-demanda`" foi feito com **`cat` do `SKILL.md`**, então 167
   linhas do mapa caíram na tela no meio da apresentação do método. A skill não tem
   `disable-model-invocation`; invocá-la pela ferramenta Skill não imprime nada.

**A passada de 2026-09-21 no ramo arquivo fechou o que faltava, e também não achou defeito nos
arquivos gerados.** As substituições de nome e descrição estão nos quatro templates, o bloco de
instrução do `readme.md` foi apagado, e as linhas da mídia e das coleções saíram preenchidas
(`diff` de cada arquivo gerado contra o template do cache da `0.24.0`). A sessão inteira teve duas
falas do usuário: a resposta em prosa a nome, descrição e `git init`, e uma chamada de
`AskUserQuestion`. Dos quatro desvios de roteiro que o ramo issue achou, três voltaram
(`~/.claude/projects/-home-mh-dev-tmp-app1/*.jsonl`):

1. **Mídia e padrões numa chamada só de `AskUserQuestion`** — igual à passada anterior.
2. **`cat` do `SKILL.md` do `workflow-demanda`** — as mesmas 167 linhas na tela
   (`wc -l < skills/workflow-demanda/SKILL.md`), de novo no meio da apresentação do método.
3. **As perguntas de ferramentas, com uma variação.** As duas primeiras o roteiro dispensa quando os
   padrões de engenharia não vão para lugar nenhum, que foi a escolha do usuário. A terceira — a das
   coleções, que o roteiro diz ser sempre e pede *"confirmar o que está instalado em vez de supor"* —
   não foi feita: o agente detectou as duas coleções com `ls ~/.claude/plugins/cache/` e gravou a
   linha certa. Ler o diretório de cache é mais confiável que perguntar, e é o argumento mais forte
   contra essa pergunta continuar no roteiro.

**O quarto não voltou:** a pergunta da mídia saiu com arquivo como primeira opção, como o roteiro
quer. É evidência a favor da hipótese registrada na intent — o diretório da passada anterior se
chamava `teste-aicf-issues`, e o desta se chama `app1`.

Os quatro pontos estão em
[o setup pergunta o que o ambiente já responde](../projeto/concluidas/o-setup-pergunta-o-que-o-ambiente-ja-responde.md).

## O que está em aberto

**Nenhuma condição dos dois ramos.** O bloco do modo issue rodou em 2026-09-21 e o do modo arquivo
no mesmo dia, ambos na `0.24.0`; o `ROADMAP.md` e o par `develop`/`main`, que a passada do issue não
alcançava, foram os últimos.

**A passada da `0.28.0`, no ramo arquivo, rodou em 2026-09-23** (`~/.claude/projects/-home-mh-dev-tmp-app2/*.jsonl`;
as duas skills carregaram de `aicf/0.28.0/`, conferido com `grep -o 'Base directory for this skill: [^"\\]*'`).
As condições do modo arquivo passaram, sem defeito nos arquivos gerados. Das quatro da
[spec](../projeto/concluidas/o-setup-pergunta-o-que-o-ambiente-ja-responde.md):

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")
  | "\(.name) \(.input | tostring | .[0:160])"' <arquivo>.jsonl \
  | grep -E 'workflow-demanda|plugin|AskUserQuestion'
```

1. **Metade.** Nenhuma pergunta de ferramenta — mas também nenhuma declaração antes do commit: as
   coleções detectadas só aparecem no resumo final, depois do `445110a`. O roteiro pede a linha
   justamente para o usuário corrigir antes do commit. E o usuário escolheu "Nenhum dos dois" para
   os padrões, então a detecção de cofre e de docs **não foi exercitada**.
2. **Passou.** Uma chamada `claude plugin list --json` com o filtro de escopo, e `claude mcp list`
   no mesmo comando; nenhum `ls` do cache.
3. **Passou.** `Skill {"skill":"aicf:workflow-demanda"}`, e nenhum `cat` ou `Read` do `SKILL.md`.
4. **Passou.** A primeira `label` da mídia é `Arquivos em docs/projeto/`.

**A passada da `0.29.0`**, que corrigiu os dois pontos acima e mudou a
pergunta dos padrões ([a pergunta dos padrões parece apagar o global](../projeto/concluidas/a-pergunta-dos-padroes-parece-apagar-o-global.md)).
Numa máquina com padrões no global, escolhendo **Completar o global** ou **Acrescentar no projeto**:

1. A linha do que foi detectado — cofre, docs e coleções — aparece **no texto da pergunta da
   mídia**, antes de qualquer `Write` ou `git add` no transcript.
2. A pergunta dos padrões oferece *Manter o global como está* em primeiro, *Completar o global* e
   *Acrescentar no projeto*, e nenhum "Nenhum dos dois".
3. Com *Acrescentar no projeto*, o `CLAUDE.md` gerado não repete seção que o global já tem; com
   *Completar o global*, o agente mostra as seções que faltam antes de tocar o `~/.claude/CLAUDE.md`.
4. As condições 2 a 4 da `0.28.0` e as do modo arquivo seguem passando.

**Ela rodou em 2026-09-24, no ramo arquivo, escolhendo *Acrescentar no projeto***
(`~/.claude/projects/-home-mh-dev-tmp-app3/*.jsonl`, as duas skills de `aicf/0.29.0/`). As
condições do modo arquivo passaram — 1 commit, `develop` ativa, `develop` e `main`, as linhas da mídia
e das coleções preenchidas. Das quatro:

1. **Falhou de novo.** A detecção rodou (`claude plugin list --json` e `claude mcp list` num `Bash`
   antes da pergunta), mas nenhum texto do agente saiu entre esse comando e o `AskUserQuestion`: o
   que foi detectado só aparece no resumo final, depois do commit. É a segunda passada com o mesmo
   desvio, agora com o roteiro dizendo onde a linha vai — o agente não escreve texto antes de
   chamar a ferramenta.
2. **Passou.** A pergunta abre com *"Seu ~/.claude/CLAUDE.md já tem os padrões"*, e as opções são
   *Manter o global como está (Recomendado)*, *Completar o global*, *Acrescentar no projeto*.
3. **Passou, pelo lado vazio.** O global já cobre todas as seções do template, então *Acrescentar no
   projeto* não colou nada — o `CLAUDE.md` gerado tem só as seções do `claude-md.md`
   (`grep '^## ' CLAUDE.md`), e o agente disse isso. **Consequência:** nesta máquina, nenhuma opção
   escreve padrões, e a detecção de cofre e de docs não tem onde ser gravada — ela só se exercita
   com um global que não cubra o template.
4. **Passou.** Nenhum `cat` do `workflow-demanda`, a primeira opção da mídia é arquivo.

Um detalhe sem efeito: a linha das coleções saiu `Superpowers, Matt Pocock (mattpocock-skills)` —
o id entre parênteses é ruído, não erro.

**A condição 1 passou na `0.29.1`**, em 2026-09-24 (`~/.claude/projects/-home-mh-dev-tmp-app4/*.jsonl`,
as duas skills de `aicf/0.29.1/`). O enunciado da primeira pergunta abriu com *"Achei no seu global
Bitwarden como cofre de senhas e Context7 como fonte de docs, e neste diretório estão habilitados
Superpowers e Matt Pocock. Vou registrar assim."* — antes de qualquer arquivo, e o commit veio
depois. As condições do modo arquivo seguem passando. O `jq` que confere:

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="AskUserQuestion")
  | .input.questions[0].question' <arquivo>.jsonl | head -1
```

A linha das coleções saiu de novo com o id entre parênteses — `Superpowers, Matt Pocock
(mattpocock-skills)` — em `app3` e `app4`. Sem efeito no `implementar-spec`, que lê os nomes.

**O que segue aberto: a detecção de cofre e de docs gravada nos padrões, que não é verificável nesta máquina:** o global
cobre o template inteiro, e nenhuma opção escreve padrões. Encerra numa máquina — ou com um
`HOME` — cujo global não tenha as seções de segurança e de dependências.

**O `## Próximas` vazio passou na `0.29.2`**, em 2026-09-24 (`~/.claude/projects/-home-mh-dev-tmp-app5/*.jsonl`,
as duas skills de `aicf/0.29.2/`): o template deixou de trazer as duas linhas de exemplo
([o template do roadmap entrega item de exemplo](../projeto/concluidas/o-template-do-roadmap-oferece-item-de-exemplo.md)),
e `sed -n '/^## Próximas/,/^## /p' docs/projeto/ROADMAP.md | grep -c '^- \[ \]'` devolveu `0` no
projeto gerado. O resto do bloco do modo arquivo seguiu passando, e o `diff` mostrou só as quatro
diferenças esperadas. A linha das coleções saiu `Superpowers, Matt Pocock`, desta vez sem o id entre
parênteses.

**O aviso sobre o Matt na pergunta da mídia, na `0.29.3`**
([o setup não avisa que o Matt pergunta o mesmo](../projeto/concluidas/o-setup-nao-avisa-que-o-matt-pergunta-o-mesmo.md)).
Duas passadas num diretório novo, sem `docs/agents/`:

1. **Matt habilitado — passou** em 2026-09-24 (`~/.claude/projects/-home-mh-dev-tmp-app6/*.jsonl`, as
   duas skills de `aicf/0.29.3/`). A opção de arquivos terminou em *"O /setup-matt-pocock-skills vai
   fazer a mesma pergunta, e em modo arquivo o Matt guarda o trabalho dele em .scratch/, separado de
   docs/projeto/."*, e a de issues em *"No setup do Matt, escolha GitHub para os dois usarem as mesmas
   issues."* O enunciado ficou só com a linha da detecção e a pergunta.
2. **Matt desabilitado — não rodou; risco aceito pelo titular.** A falha possível é o agente pôr as
   frases do Matt nas opções mesmo sem ele: ruído na tela, sem arquivo errado, e visível para o
   primeiro usuário que não tem o Matt. Encerra na primeira passada sem o Matt habilitado: nenhuma
   descrição cita `.scratch/`.

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="AskUserQuestion")
  | .input.questions[] | .question, (.options[] | .label + " — " + .description)' <arquivo>.jsonl
```

**A apresentação do método na `0.31.0`**
([o mapa pesa em toda demanda](../projeto/concluidas/o-mapa-pesa-em-toda-demanda.md)). O mapa virou
`/aicf:ajuda`, com `disable-model-invocation: true`, e o harness recusa a ferramenta Skill para ele.
A condição 3 da `0.28.0` — *Skill, e nenhum `cat` ou `Read`* — passa a ser: **`Read` de
`ajuda/SKILL.md`, nenhum `cat`, e nenhuma chamada `Skill` para `aicf:ajuda`**; o passo 5 da
despedida cita `/aicf:ajuda`. Não rodou. Encerra na próxima passada do setup, em qualquer ramo:

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")
  | "\(.name) \(.input | tostring | .[0:160])"' <arquivo>.jsonl \
  | grep -E 'ajuda|workflow-demanda'
```

A saída esperada é uma linha `Read` com `ajuda/SKILL.md`, e nenhuma `Skill` nem `Bash` com `cat`.
