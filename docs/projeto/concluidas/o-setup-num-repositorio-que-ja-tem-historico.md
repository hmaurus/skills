# O setup num repositório que já tem histórico

Processo — entrevista: criar-spec · implementação: aicf-direto

Registrada em 2026-09-29, pela revisão de código de
[o setup supõe que o git init cria main](../concluidas/o-setup-supoe-que-o-git-init-cria-main.md),
que passou a nomear o caso "já existia, com commit em qualquer branch" em "O repositório local" do
`skills/setup/SKILL.md` sem resolver o que vem depois dele.

## Problema

O corpo do setup se oferece a projeto existente ("num projeto novo ou num que ainda não tem
`docs/projeto/`", e o parágrafo sobre `/init` para "Projeto que já tem código"), mas o roteiro de
git foi escrito supondo que é ele quem cria as branches. Num repositório com commits:

1. **O commit cai na branch ativa, e o texto diz que cai na produção.** Com uma `feature` ativa, a
   governança vai para `feature`, e a `develop` nasce de lá. Na variante sem `main` (`master` +
   `feature` ativa), a regra "senão, a branch ativa" elege a `feature` como produção.
2. **O código `0` de "A `main` no remoto" não significa histórico próprio.** O remoto costuma ser o
   upstream da própria `main`; o resumo afirma "a `main` remota tem histórico próprio", o que é
   falso.
3. **`git branch develop` sai com 128** (`fatal: a branch named 'develop' already exists`) quando
   o projeto já tem `develop`.
4. **O `git commit` leva o que o usuário tinha no índice.** O setup faz `git add` só dos caminhos
   dele, mas `git commit` sem caminhos commita o índice inteiro — inclusive um arquivo que o
   usuário deixou em stage antes de rodar o setup. _(Achado na entrevista; não estava na intent.)_

Reprodução de 1 a 3, com git 2.43:

```bash
d=$(mktemp -d); export HOME=$d GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x
git init -q --bare $d/remoto.git; git init -q -b main $d/r; cd $d/r
git commit -q --allow-empty -m a; git remote add origin $d/remoto.git; git push -q -u origin main
git switch -q -c feature; git commit -q --allow-empty -m gov; git branch --show-current   # 1: feature
git switch -q main; git commit -q --allow-empty -m gov2
git ls-remote --exit-code --heads origin main >/dev/null; echo $?; git push -q origin main; echo $?   # 2: 0 e 0
git branch develop; git branch develop; echo $?                                          # 3: 128
```

## Solução

**Com histórico, o setup não mexe em branch.** Tratamos a governança como qualquer outra mudança:
o commit vai para a branch ativa, e ela chega à produção pelo fluxo que o projeto já tem (PR,
merge). O setup não troca de branch, não cria `develop`, não envia nada ao remoto e não descreve o
fluxo de git do projeto. Repositório com histórico é o terceiro caso da tabela de "O repositório
local": `git rev-list -n 1 --all` devolve um sha.

O que muda, por seção do `skills/setup/SKILL.md`:

- **`description` (frontmatter)** — "Deixa tudo no primeiro commit, em main (ou na produção que o
  repositório já tinha), e entrega develop como branch de trabalho" passa a dizer que, em
  repositório novo, é `main` + `develop`; em repositório com histórico, um commit na branch ativa,
  sem mexer em branch.
- **"O repositório local"** — a tabela perde a coluna "Produção" como decisão do terceiro caso: a
  linha diz que o setup não decide produção nem mexe em branch, e que as seções "A `main` no
  remoto" e "A branch de trabalho" não rodam. O parágrafo "todo `main` desta skill… é a branch de
  produção" sai: sem push, sem `develop` e sem seção Git, não sobra `main` a trocar.
- **"O que criar"** — com histórico, o `CLAUDE.md` nasce **sem a seção `## Git`** do template. A
  exceção que hoje troca o `main` dessa seção pelo nome real sai junto. O caso de `CLAUDE.md` já
  existente não muda (só "Processos de desenvolvimento" é proposta).
- **"O primeiro commit"** — em qualquer caso, o commit nomeia os caminhos:
  `git commit -m '<mensagem>' -- <caminhos>`, depois do `git add` deles. Assim o que o usuário tinha
  em stage continua em stage e fora do commit. A frase "O commit cai na branch de produção" vira: em
  repositório novo, na `main`; com histórico, na branch ativa, que o resumo nomeia.
- **"O repositório no GitHub, e os labels"** — com histórico, `gh repo create` roda **sem
  `--push`** (`--private --source=. --remote=origin`): cria o repositório e o `origin`, e não envia
  nada. As issues e os labels não dependem de código no remoto. O resumo diz para enviar primeiro a
  branch de produção, porque a primeira enviada vira a default no GitHub.
- **"A `main` no remoto"** e **"A branch de trabalho"** — uma frase no topo de cada: não rodam em
  repositório com histórico. A oferta de criar o repositório no modo arquivo também não roda.
- **"Ao terminar"**, item 1 — com histórico, o resumo diz em que branch o commit ficou, que a seção
  Git do `CLAUDE.md` ficou de fora para o usuário escrever com o fluxo dele, e, no modo issue com
  repositório criado agora, qual branch enviar primeiro.

## Arquivos e interfaces

- `skills/setup/SKILL.md` — as seções acima.
- `skills/setup/templates/claude-md.md` — só se a omissão da seção `## Git` pedir um marcador no
  template; a preferência é o setup omitir sem mudar o template.
- `docs/referencias/verificacao-do-setup.md` — um item em "O que está em aberto" para a passada em
  repositório com histórico.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — versão e entrada, juntos.

## Fora de escopo

- **Levar o commit à produção** (perguntar qual é, `git switch`, tratar árvore suja, conferir
  fast-forward antes do push). Descartado: atropela o PR de quem protege a `main`, e é o setup
  mexendo em fluxo que não criou.
- **Recusar repositório com histórico.** Descartado: contradiz o corpo, que se oferece a projeto
  existente, e deixa sem caminho quem quer adotar o método num projeto em andamento.
- **Escrever a seção Git com as branches que existem.** Descartado: seria o agente deduzindo o
  fluxo do projeto; quem sabe é o usuário.
- **Perguntar qual branch enviar depois do `gh repo create`.** Descartado: o setup não envia nada
  em repositório com histórico, e a linha do resumo basta.
- **Quem mais lê a seção Git:** o `implementar-spec` tira dela o workspace default e, sem ela, usa
  a branch atual — o que, com histórico, é o certo.
  ``grep -rn '## Git' skills --include=SKILL.md | grep -v '^skills/setup'`` acha só essa linha em
  `1a9443c`; um leitor novo pede rever a omissão. _(A primeira versão desta linha usava
  `grep 'branch de trabalho'`, que não enxergava esse leitor; corrigida no fechamento.)_

## Verificação

1. **Os comandos que a spec prescreve**, num repositório com `main` e `develop` já enviadas, uma
   `feature` ativa e um arquivo do usuário em stage:

   ```bash
   d=$(mktemp -d); export HOME=$d GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x
   git init -q --bare $d/remoto.git; git init -q -b main $d/r; cd $d/r
   git commit -q --allow-empty -m a; git branch develop; git remote add origin $d/remoto.git; git push -q -u origin main develop
   git switch -q -c feature; echo u > user.txt; git add user.txt
   mkdir -p docs/projeto; echo g > CLAUDE.md; echo p > docs/projeto/PRD.md
   git add CLAUDE.md docs/projeto/PRD.md && git commit -q -m 'chore: estrutura de governança do projeto' -- CLAUDE.md docs/projeto/PRD.md
   git branch --show-current                                # feature
   git show --name-only --format= HEAD                      # CLAUDE.md e docs/projeto/PRD.md, nada mais
   git status --short                                       # A  user.txt — continua em stage
   git rev-parse main develop origin/main | uniq | wc -l    # 1 — nenhuma das três andou
   ```

   Rodado na entrevista, em 2026-09-29, com a saída acima.

2. **O texto**, em `skills/setup/SKILL.md`: `grep -c 'senão, a branch ativa'` passa de 1 a 0;
   ``grep -c 'sem `--push`'`` passa de 0 a ao menos 1; `grep -c ' -- <'` passa de 0 a ao menos 1
   (o commit com caminhos).
3. `./scripts/check.sh` termina em `Tudo verde.`
4. **Comportamento do setup** — a skill tem `disable-model-invocation: true`, então o agente não a
   roda. Fica em aberto até uma passada do titular num repositório com histórico (branch ativa que
   não é a produção, `develop` já existente, `origin` com a `main`), registrada em
   [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md): um commit na branch ativa
   só com os caminhos do setup, nenhuma branch criada ou enviada, `CLAUDE.md` sem `## Git`, e o
   resumo nomeando a branch.

## Relatório de implementação (2026-09-29)

**Status:** concluído. Sem CI conferido ainda — o push fica com o titular.

**Arquivos alterados**

- `skills/setup/SKILL.md` — a tabela de "O repositório local" passa a dizer onde o commit cai, e o
  caso com histórico não mexe em branch; o `CLAUDE.md` nasce sem `## Git`; o commit nomeia os
  caminhos; três estados param o setup antes do commit; `gh repo create` sem `--push`; "A `main` no
  remoto" e "A branch de trabalho" não rodam; o resumo nomeia a branch do commit.
- `docs/referencias/verificacao-do-setup.md` — a passada da `0.34.2`, nos ramos arquivo e issue.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.34.2`.

**Commits**

- `d8fad48` docs(projeto): entrevista do setup em repositório com histórico vira spec
- `8150915` fix(setup): repositório com histórico recebe o commit na branch ativa, sem mexer em branch
- `1a9443c` fix(setup): merge, HEAD destacado e branch sem commit param o setup antes do commit

**Validação**

- Verificação 1 rodada na entrevista e de novo no fechamento, com a saída prevista.
- Verificação 2: em `skills/setup/SKILL.md`, `grep -c 'senão, a branch ativa'` → 0,
  ``grep -c 'sem `--push`'`` → 2, `grep -c ' -- <'` → 1 (em `8150915`).
- `./scripts/check.sh` → `Tudo verde.` nos dois commits de código.
- Revisão por subagente sem contexto da implementação, sobre `8150915`: nove achados, nenhum
  bloqueante; os seis que mudavam texto entraram em `1a9443c`.
- Os três estados que param o setup, reproduzidos com git 2.43 e `HOME` vazio: `git commit -- <caminhos>`
  no meio de um merge sai com 128 (`cannot do a partial commit during a merge`) e
  `git rev-parse -q --verify MERGE_HEAD` sai com 0; depois de `git checkout --detach`,
  `git symbolic-ref -q HEAD` sai com 1; com `git init` + `git fetch`, o commit do setup não tem
  `git merge-base` com `origin/main` (sai com 1).
- **Verificação 4 em aberto:** a skill tem `disable-model-invocation: true`. Encerra na passada da
  `0.34.2` de [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), que o titular
  roda no uso real.

**Escopo efetivo** — além da spec: o quarto defeito (o índice do usuário), achado na entrevista; e,
da revisão, a parada nos três estados, o aviso de "enviar a produção primeiro" também para remoto
vazio que já existia, e a ressalva de que stage num arquivo que o setup também edita vai junto.

**Lições**

- A salvaguarda "nenhuma outra skill lê a seção Git" foi escrita com um grep pela frase do conteúdo,
  não pelo heading; o leitor real (`implementar-spec`) cita `## Git`. É a mesma regra que o
  `CLAUDE.md` já tem — o comando mira o trecho, não o assunto —, aplicada a quem lê em vez de a
  quem muda.

O ritual não gerou ADR, regra nova ou skill; o doc de referência tocado é o `verificacao-do-setup.md`,
acima. Nenhuma demanda nova nem obsoleta.
