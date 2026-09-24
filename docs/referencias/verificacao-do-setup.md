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
grep -n 'Repositório' docs/projeto/ROADMAP.md  # "Repositório no GitHub e CI mínimo"

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

**A passada da `0.28.0`, no ramo arquivo.** A [spec dos quatro pontos](../projeto/concluidas/o-setup-pergunta-o-que-o-ambiente-ja-responde.md)
foi implementada, e o comportamento novo ainda não rodou. Numa máquina com cofre e fonte de docs
declarados no global e Superpowers e Matt Pocock habilitados, escolhendo "No global" para os
padrões, além das condições do modo arquivo acima:

```bash
jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")
  | "\(.name) \(.input | tostring | .[0:160])"' <arquivo>.jsonl \
  | grep -E 'workflow-demanda|plugin|AskUserQuestion'
```

1. **Nenhuma pergunta de ferramenta** — o agente declara numa linha o que achou e segue (ler as falas
   com o `jq` da seção anterior).
2. **Coleções por `claude plugin list`**, sem `ls ~/.claude/plugins/cache/`.
3. **`Skill` com `aicf:workflow-demanda`**, e nenhum `cat` ou `Read` do `SKILL.md` dele.
4. **A pergunta da mídia com *arquivos* como primeira opção** — é a primeira `label` do
   `AskUserQuestion`.

Na passada da `0.24.0` o mesmo comando mostra o `ls` do cache e o `cat` do `SKILL.md` — é o que ele
flagra.
