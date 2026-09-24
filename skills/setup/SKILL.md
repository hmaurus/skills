---
name: setup
description: Cria a base de governança de um projeto novo — inicializa o repositório git se faltar, pergunta se a demanda mora em arquivos ou em issues do GitHub, e monta o que a escolha pedir: docs/projeto/ com PRD e roadmap e as pastas de demanda, ou o repositório no GitHub e os labels aicf:*, mais o CLAUDE.md raiz — e, se o usuário quiser, os padrões de engenharia. Deixa tudo no primeiro commit, em main, e entrega develop como branch de trabalho. Rodar uma vez, no começo do projeto.
disable-model-invocation: true
---

# Setup da governança do projeto

Monta a estrutura que o restante do método assume. Roda uma vez, num projeto novo ou num que
ainda não tem `docs/projeto/`.

**Nunca sobrescrever arquivo existente.** Se algum dos alvos já existe, mostrar quais e
perguntar antes: pular, ou mostrar o diff e deixar o usuário decidir arquivo por arquivo.

## A apresentação

**Antes da primeira pergunta**, dizer em três a cinco linhas o que vem pela frente. Não mais que
isso: quem roda este comando pela primeira vez está prestes a agir, e três parágrafos sobre
governança seriam o muro que a apresentação existe para derrubar. Cobrir só:

- **o que vai ser montado** — onde a visão do produto mora, onde cada demanda é registrada, e como
  o agente sabe disso em toda sessão;
- **que são poucas perguntas**, e que nenhuma resposta é definitiva: tudo vira arquivo que o
  usuário edita depois;
- **que nada é criado antes de ele confirmar.**

**Sem prometer um número.** Os ramos do roteiro têm tamanhos diferentes — o modo issue com
repositório a criar passa de qualquer faixa que coubesse aqui —, e número que o próprio roteiro
desmente é pior que número nenhum.

## Antes de criar

Perguntar, em pergunta aberta:

1. **Nome do projeto** — se o diretório já tem nome óbvio, propor esse e confirmar.
2. **O que é, em uma ou duas frases** — o suficiente para o `CLAUDE.md` não nascer vazio.

Não entrevistar além disso. Visão, público e modelo entram no PRD depois, com calma — o setup
só prepara o lugar onde eles vão morar.

## O repositório local

**Antes da pergunta da mídia**, conferir se o diretório é repositório git. Não sendo, explicar **em
uma linha** por que o método depende de versionamento — a demanda muda de estado por `git mv`, o
relatório vive no histórico, e `.gitkeep` num diretório sem git não segura pasta nenhuma — e
perguntar. Sim, `git init`: é local, barato e desfeito com `rm -rf .git`.

Montar a governança num diretório sem repositório entrega um método que não funciona, e o usuário
só descobre no primeiro fechamento de demanda.

**Dito não, o setup segue em modo arquivo**, sem primeiro commit e sem oferecer o modo issue — e
diz isso em uma linha, porque as duas coisas passam a existir assim que o usuário rodar `git init`
por conta própria. Não insistir: a estrutura criada continua válida, só não versionada.

## O que o ambiente permite

Com o repositório local de pé, ler o ambiente **na ordem abaixo**, anotando o que falta. Nada é
executado aqui: a leitura só decide o que a pergunta seguinte oferece, e o que o setup terá de
resolver se a resposta for issue.

1. **`command -v gh`** — sem o GitHub CLI o modo issue não existe nesta máquina, e a opção **não é
   oferecida**. Uma linha: o modo issue precisa do GitHub CLI (<https://cli.github.com>); quem o
   quiser para aqui, instala e roda o `/aicf:setup` de novo — este comando roda uma vez, e trocar
   de mídia num projeto que já tem governança montada não é dele.
2. **`gh auth status`** — falhando, falta login, que o setup **conduz**.
3. **`git remote -v`** — vazio, falta o repositório no GitHub, que o setup **cria**. Apontando para
   outro provedor, a opção **não é oferecida**: a receita inteira do modo issue é `gh`. Este
   comando só vale depois da seção anterior — em diretório sem `.git` ele sai com 128 e
   `fatal: not a git repository`, que não é a mesma coisa que vazio.

**As pendências se acumulam, e no projeto novo as duas aparecem juntas** — quem acabou de rodar
`git init` tem o remote vazio, e quem nunca usou o `gh` também não tem login. Resolver na ordem da
lista: criar o repositório exige estar autenticado.

A opção issue só some nos dois casos que o setup **não** resolve. Deixar o usuário escolher um
caminho que falha no primeiro comando é pior que não oferecer — e esconder o que bastava um comando
para habilitar é pior ainda.

## A mídia do registro

**Antes de criar a estrutura** — é esta resposta que decide o que criar. `AskUserQuestion`,
com a explicação curta de cada uma:

- **Arquivos em `docs/projeto/`** (default) — a demanda é um `.md` versionado. Zero setup,
  sobrevive ao `git clone` sem rede, entra no `grep` do repositório, não depende de fornecedor.
- **Issues (GitHub)** — a demanda é uma issue. Conversa com comentário e notificação, contribuição
  de fora em dois cliques, referência estável por `#12`, e `Fixes #12` fecha pelo merge.

**Se `docs/agents/issue-tracker.md` existe**, o `/setup-matt-pocock-skills` já respondeu a mesma
pergunta — onde o trabalho mora. Ler e propor o default a partir dele ("o tracker do Matt aponta
para GitHub; usar issues aqui também?") em vez de perguntar do zero. As duas configs seguem
independentes: divergir é legítimo, e a do aicf é a linha do `CLAUDE.md`.

**O default vai primeiro na lista**, porque o `AskUserQuestion` apresenta a primeira opção como a
sugerida. É arquivo, sempre — o nome do diretório não muda isso, nem um `-issues` no fim dele. A
única exceção é o tracker do Matt apontar para o GitHub: aí o default proposto é issues, e issues
vai primeiro.

**Respondida a pergunta, resolver o login, se ele faltava.** `gh auth login` é **conduzido, não
executado**: mostrar o comando, pedir que o usuário rode (pelo `!` da própria sessão) e reconferir
com `gh auth status` antes de seguir. Existe caminho não interativo — `gh auth login --with-token`
lê de stdin —, e é justamente por isso que ele não serve aqui: o token teria que passar pelo chat,
e credencial não entra no chat.

**A escolha fica guardada e vira uma linha no `CLAUDE.md` quando ele for criado** (em "O que
criar"), na seção "Processos de desenvolvimento" — sempre, nos dois modos:

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

Linha ausente significa arquivo — é a compatibilidade com projeto anterior a esta escolha existir,
não um valor a ser deixado implícito em projeto novo. As receitas estão em
`workflow-demanda/references/`, uma por mídia:
[`midia-arquivo.md`](../workflow-demanda/references/midia-arquivo.md) e
[`midia-issues.md`](../workflow-demanda/references/midia-issues.md).

Perguntar também **o que fazer com os padrões de engenharia** (idioma, KISS/YAGNI, validação antes
do commit, testes, acessibilidade, tratamento de credencial). Pode ir na mesma chamada de
`AskUserQuestion` que a mídia, a critério do agente — nenhuma das duas respostas muda a outra, e o
login do `gh` funciona igual depois das duas.

**As opções dependem do que o global já tem**, porque a pergunta é sobre o que acontece com o que
existe, não só sobre onde colar. Ler `~/.claude/CLAUDE.md` antes: ele **tem padrões** quando tem
seção equivalente a alguma de `templates/preferencias.md`.

Global com padrões — o default primeiro:

- **Manter o global como está** — nada é copiado nem alterado.
- **Completar o global** — acrescenta ao `~/.claude/CLAUDE.md` só as seções que faltam lá.
- **Acrescentar no projeto** — o `CLAUDE.md` do projeto recebe só as seções que o global não tem,
  somando a ele. Quem trabalha em equipe e quer o padrão inteiro no repositório copia o resto à
  mão: o global não viaja no `git clone`.

Sem global, ou global sem padrões:

- **No global** — vale para todos os projetos da máquina.
- **No projeto** — fica versionado e viaja com o repositório.
- **Não usar** — o usuário já tem os seus em outro lugar.

## Ferramentas que o usuário já usa

Três ferramentas mudam o comportamento do agente daqui para a frente. **As duas primeiras só
importam quando o setup vai escrever padrões** — completar o global, acrescentar no projeto, no
global ou no projeto —, porque é nas seções dos padrões que as respostas moram; com "Manter o
global como está" ou "Não usar", nada é escrito. A terceira é sempre.

**1. Gerenciador de senhas.** Onde mora a credencial que não cabe no `.env` — senha de painel,
chave de produção, credencial usada em mais de uma máquina. Importa porque esses cofres têm CLI:
o agente lê um campo específico sem o valor passar pelo chat, o que não acontece quando o
usuário cola a chave na conversa. Sem nenhum, o `.env` sozinho funciona numa máquina só, mas some
com ela e não dá para compartilhar.

**2. Fonte de documentação de biblioteca.** Conhecimento de treino envelhece; a API da lib que o
agente "lembra" pode ser de duas versões atrás. Um MCP de documentação faz o agente consultar a doc
atual antes de escrever a chamada. Sem nenhum, registrar que a doc oficial é consultada na mão.

**3. Coleções de skills de workflow.** Com Superpowers ou as skills do Matt Pocock instaladas, os
caminhos de entrevista e implementação que `/aicf:workflow-demanda` oferece mudam — sem elas, só o
caminho aicf existe, e propor `brainstorming` seria propor algo que não roda.

**Detectar antes de perguntar.** Quem já usa o método costuma ter as três respostas na máquina, e
perguntar o que o ambiente responde é rodada gasta. Três fontes, uma por pergunta:

- **cofre** — o `~/.claude/CLAUDE.md`, onde ele aparece declarado em prosa. Ter o binário `bw` ou
  `op` na máquina não conta: não diz que é o cofre que o usuário usa;
- **fonte de docs** — o global, ou `claude mcp list`, que mostra o Context7 tanto instalado como
  plugin (`plugin:context7:context7`) quanto configurado direto como servidor MCP;
- **coleções** — os plugins habilitados **neste diretório**; Superpowers e Matt Pocock aparecem
  pelo id (`superpowers@…`, `mattpocock-skills@…`):

  ```bash
  claude plugin list --json | jq -r --arg d "$PWD" \
    '.[] | select(.enabled and (.scope=="user" or .projectPath==$d)) | .id'
  ```

  **Não ler `~/.claude/plugins/cache/`**: o cache guarda também plugin desabilitado. E **não
  tirar o filtro de escopo**: sem ele, plugin habilitado só em outro projeto conta como instalado
  aqui.

**O que a detecção achou, declarar numa linha e seguir, sem perguntar** — *"Achei Bitwarden e
Context7 no seu global, e Superpowers e Matt Pocock habilitados; vou registrar assim."* **A linha
vai no texto que acompanha a pergunta da mídia**, antes de qualquer arquivo existir: a detecção roda
antes dela, e é essa posição que deixa o usuário corrigir. Aparecer só no resumo final, depois do
commit, é o mesmo que não declarar.

**O que não achou, explicar em uma frase e sugerir, numa pergunta só com os itens que faltaram** —
Bitwarden (CLI `bw`, plano gratuito generoso) para senhas, Context7 para docs, Superpowers e Matt
Pocock para coleções — e aceitar "nenhum" como resposta: quem está começando não tem nada disso, e insistir transforma o setup em
venda de stack. **Coleção se sugere, não se instala:** plugin instalado no meio da sessão só carrega
na próxima, e a linha do `CLAUDE.md` registra o que estava habilitado agora.

**Sem o CLI `claude`** — outro harness, lendo pelo `AGENTS.md` —, a detecção pelo CLI não existe:
perguntar o que o global não respondeu, do mesmo jeito.

Registrar as respostas onde elas já têm lugar: as duas primeiras nas seções de segurança e de
dependências dos padrões de engenharia (abaixo); a terceira, na linha "Coleções de skills de
workflow instaladas" de "Processos de desenvolvimento" do `CLAUDE.md` — é dela que o
`implementar-spec` tira os caminhos que oferece. **Nome da ferramenta e nome da variável de ambiente — nunca o valor.**

## O que criar

|                                                        | Modo arquivo | Modo issue |
| ------------------------------------------------------ | ------------ | ---------- |
| `CLAUDE.md`, `AGENTS.md` (link), `README.md`            | sim          | sim        |
| A linha `**Mídia do registro:**`                        | sim          | sim        |
| `docs/projeto/PRD.md`                                   | sim          | sim        |
| `docs/projeto/ROADMAP.md`                               | sim          | **não**    |
| `backlog/`, `intents/`, `specs/`, `concluidas/`         | sim          | **não**    |
| Os três labels `aicf:*`                                 | não          | **sim**    |

O `CLAUDE.md`, o `AGENTS.md`, o `README.md` e o que `docs/projeto/` pedir são desta seção. Os três
labels — e o repositório no GitHub, quando ele ainda não existe — nascem depois do primeiro commit,
e têm seção própria mais abaixo.

```
CLAUDE.md                       # raiz, se ainda não existir
AGENTS.md -> CLAUDE.md          # link simbólico
README.md                       # se ainda não existir
docs/projeto/
├── PRD.md                      # nos dois modos
├── ROADMAP.md                  # só modo arquivo
├── backlog/.gitkeep            # as quatro pastas de demanda ficam no
├── intents/.gitkeep            # mesmo nível, e só existem no modo arquivo
├── specs/.gitkeep
└── concluidas/.gitkeep
```

**No modo issue, `docs/projeto/` fica só com o `PRD.md`** — as pastas de demanda não existem, e
`ROADMAP.md` não tem substituto: ele só fazia sentido onde criar arquivo custa mais que ter a
ideia, e a issue não tem esse custo. O critério **certeza, não urgência** que ele explicava passa a
viver na descrição do label `aicf:backlog`.

Os templates estão em `templates/` dentro desta skill:

| Template                 | Vai para                                        |
| ------------------------ | ----------------------------------------------- |
| `templates/claude-md.md` | `CLAUDE.md` (raiz)                              |
| `templates/prd.md`       | `docs/projeto/PRD.md`                           |
| `templates/roadmap.md`   | `docs/projeto/ROADMAP.md` — **só no modo arquivo** |
| `templates/readme.md`    | `README.md` (raiz) — a tabela "Onde ficam as coisas" tem um bloco por mídia; escolher um e apagar o outro |
| `templates/preferencias.md` | conforme a resposta acima — ver abaixo       |

Copiar cada template trocando `<NOME>` pelo nome do projeto e preenchendo a descrição no lugar
indicado. **A linha `**Mídia do registro:**` recebe o valor que a pergunta da mídia respondeu** — é
a única fonte da verdade da escolha, e deixá-la com o texto do template faz toda skill ler a mídia
errada. **Não reescrever o template por conta própria:** o que estiver marcado como a preencher
fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser.

Se o projeto já tem `CLAUDE.md` na raiz, não substituir: mostrar a seção "Processos de
desenvolvimento" do template e propor acrescentá-la ao arquivo existente.

Projeto que já tem código também tem a parte do `CLAUDE.md` que se deduz dele — comandos, layout,
convenções —, e essa parte não é deste setup: sugerir `/init` numa sessão aberta com
`CLAUDE_CODE_NEW_INIT=1` no ambiente (`CLAUDE_CODE_NEW_INIT=1 claude` — é variável do processo,
não liga de dentro da sessão), que explora o repositório com subagente e apresenta uma proposta
antes de escrever qualquer arquivo. O setup segue dono da governança — PRD, e o que a mídia
escolhida pedir. Num projeto sem código não há o que deduzir, e nada muda.

## `AGENTS.md` como link simbólico

`ln -s CLAUDE.md AGENTS.md` na raiz. **Um arquivo, dois nomes** — o Claude Code lê `CLAUDE.md`;
Codex, Cursor e outros leem `AGENTS.md`. Manter os dois como arquivos separados garante que um
envelheça sem ninguém perceber.

- Se `AGENTS.md` já existe — arquivo ou link —, não tocar.
- O git versiona o link como link (modo `120000`), então ele viaja no clone.
- Em Windows sem Developer Mode, `ln -s` falha. Nesse caso, usar o que a documentação indica no
  lugar do link: o conteúdo vai para `AGENTS.md`, e o `CLAUDE.md` fica só com a linha
  `@AGENTS.md`, que importa o outro — continua um arquivo, dois nomes. Daí em diante, onde esta
  skill diz `CLAUDE.md`, o arquivo a editar é `AGENTS.md`. **Não criar uma cópia**, que é
  justamente o que o link existe para evitar.

## Os padrões de engenharia

`templates/preferencias.md` é um corpo de seções (`## Idioma`, `## Implementação`, …) feito
para ser colado dentro de um `CLAUDE.md`, não para virar arquivo próprio.

**Manter o global como está, ou Não usar:** não colar nada, e conferir que o `CLAUDE.md` gerado
não ficou com seção equivalente vinda do outro template.

**Completar o global, ou No global:**

1. Se `~/.claude/CLAUDE.md` não existe, criar com o conteúdo do template.
2. Se existe, **não sobrescrever e não anexar direto**: mostrar quais seções do template ainda
   não têm equivalente lá e propor acrescentar só essas. Aquele arquivo vale para todos os
   projetos da máquina — inclusive os que não usam este método. Mexer nele sem confirmação
   é fora de escopo desta skill.

**Acrescentar no projeto, ou No projeto:** colar no `CLAUDE.md` da raiz, depois de "Processos de
desenvolvimento", as seções que o global não tem — todas, quando não há global com padrões.

Havendo global com padrões, **padrão que já vale por ele não se repete no projeto**: cópia
reduzida da regra global enfraquece a regra.

Em qualquer caso, avisar sobre a única regra do template que muda o comportamento do usuário,
não só o do agente: **credencial não entra no chat** — o valor vai para o `.env` e o agente
recebe apenas o nome da variável.

## O primeiro commit

Depois de criar os arquivos e colar os padrões de engenharia, **nos dois modos**. Sem ele o
`.gitkeep` não segura pasta nenhuma, e no modo issue o push do passo seguinte não tem o que empurrar.

**Só os caminhos que o setup escreveu, um a um** — `CLAUDE.md`, `AGENTS.md`, `README.md`,
`docs/projeto/PRD.md`, e o `ROADMAP.md` e os quatro `.gitkeep` quando a mídia é arquivo. **Nunca
`git add -A`, e nem `git add docs/projeto/`:** num diretório que já tem código não commitado, o
`-A` varre tudo, inclusive um `.env` que ainda não tem `.gitignore` para segurá-lo, e o diretório
inteiro leva junto o que estiver lá dentro. O setup não decide o que vai para o histórico de
arquivo que ele não criou.

A mensagem segue o idioma do projeto que está nascendo: `chore: estrutura de governança do projeto`.

**Máquina sem identidade de git configurada** faz o `git commit` falhar com
`Author identity unknown`. Acontece justamente onde o `git init` acabou de rodar. Nesse caso,
mostrar `git config --global user.name` e `user.email` para o usuário rodar, e commitar depois —
não configurar a identidade dele por conta própria.

**O commit cai em `main`**, que é a branch que o `git init` cria. A branch de trabalho nasce depois
de tudo — ver "A branch de trabalho", no fim.

## O repositório no GitHub, e os labels

Só no modo issue, e **depois do commit**.

### Criar o repositório, se faltar

`gh repo create` é a primeira ação do setup que cria algo fora do disco local, então vai com
**confirmação explícita — nome e visibilidade**, e `--private` como sugestão.

```bash
gh repo create <nome> --private --source=. --remote=origin --push
```

**A ordem é o que esta skill fixa.** O `--push` empurra commits locais, e o `gh` confere isso
**antes** de chamar a API: sem commit nenhum ele sai com 1 e
``--push` enabled but no commits found``, sem criar repositório nenhum. Fora de um repositório
git, recusa com `current directory is not a git repository`. Nada quebra pela metade, mas o
onboarding para com um erro — e criar o remoto antes de os arquivos existirem é exatamente como se
chega lá.

**Fora dessa ordem, pesquisar em vez de improvisar.** O comando acima cobre o caso comum;
organização em vez de conta pessoal, SSH em vez de HTTPS, GitHub Enterprise, escopo de token
faltando, nome já em uso — cada um tem resposta na documentação do `gh`, e consultá-la na hora é o
certo. O que não se faz é copiá-la para cá: ela envelheceria sozinha dentro desta skill, enquanto
`gh repo create --help` está sempre atual.

### Os três labels

Criar com `gh label create`. **Label que já existe faz o comando sair com 1** —
`label with name "X" already exists; use --force to update its color and description` —, e é o
`|| true` que deixa a sequência seguir. A idempotência é da sequência, não do comando: quem
conferir o exit code, ou rodar sob `set -e`, precisa saber disso. Os comandos, com as descrições,
estão em
[`workflow-demanda/references/midia-issues.md`](../workflow-demanda/references/midia-issues.md), na
seção "Criar os labels".

**O setup é quem cria os labels**, e não a primeira demanda: `gh issue create --label` com label
inexistente **falha em vez de criar**. É a armadilha mais repetida sobre setups que só gravam o
mapeamento e deixam os labels para depois.

## A branch de trabalho

**O último passo antes do fechamento**, nos dois modos. O `CLAUDE.md` que o setup acabou de escrever
descreve `develop` como branch de trabalho e `main` como produção; este passo é o que faz o
repositório corresponder a isso, em vez de o arquivo descrever algo que não existe.

```bash
git branch develop
git switch develop
git push -u origin develop   # só no modo issue
```

**A posição na ordem é o que importa, e ela não é arbitrária.** O `gh repo create --push` roda com
`main` ativa, então é `main` que sobe primeiro e fica sendo o default do repositório no GitHub —
produção como default, que é o que o fluxo pede. Criar a `develop` antes disso inverte o resultado:
ela sobe primeiro e vira o default remoto, e desfazer isso depois é mexer em configuração do
repositório em vez de rodar um comando.

Ao fim, `develop` é a branch ativa: é onde a primeira demanda vai commitar.

## Ao terminar

O setup é a primeira vez que o usuário vê o método funcionando, e ele termina sabendo o que ganhou
e o que fazer em seguida — não só o que foi criado no disco.

1. Listar o que foi criado e onde — os arquivos, o commit, as duas branches, e, no modo issue, o
   repositório e os labels.
2. **Apresentar o método em linguagem comum.** Invocar `/aicf:workflow-demanda` pela ferramenta
   Skill (*Skill tool*) — **não ler o `SKILL.md` dele com `cat` nem `Read`**: o arquivo inteiro
   cairia na tela de quem está conhecendo o método, que é o muro de texto que esta apresentação
   evita. Contar o que ele diz, em vez de colar um texto guardado aqui: texto guardado seria a
   segunda cópia do mapa e envelheceria sozinho, enquanto a skill é a fonte da verdade do ciclo. Cobrir, nesta ordem:
   - as quatro fases, uma frase cada, sem o vocabulário de governança;
   - **um exemplo concreto de primeira demanda**, do pedido até o registro fechado, usando o nome
     real do projeto e a mídia que o usuário acabou de escolher — é o exemplo que faz o ciclo sair
     do abstrato;
   - que a governança é a mesma em qualquer caminho de implementação, inclusive os de outras
     coleções.
3. Pedir que, na próxima sessão, o usuário rode `/context` e confira o `CLAUDE.md` na lista
   **Memory files**. O arquivo carrega no início da sessão, e essa lista é a prova de que carregou
   — em vez de supor.
4. Sugerir `/aicf:criar-prd` como próximo passo — é do PRD que saem as primeiras demandas (no
   modo arquivo, o roadmap inicial; no modo issue, as primeiras issues). Depois dele, a primeira
   demanda começa por `/aicf:criar-spec`.
5. Dizer que `/aicf:workflow-demanda` é o lugar de voltar quando quiser reler como o método
   funciona.
