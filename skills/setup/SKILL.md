---
name: setup
description: Cria a base de governança de um projeto novo — inicializa o repositório git se faltar, pergunta se a demanda mora em arquivos ou em issues do GitHub, e monta o que a escolha pedir: docs/projeto/ com PRD e roadmap e as pastas de demanda, ou o repositório no GitHub e os labels aicf:*, mais o CLAUDE.md raiz — e, se o usuário quiser, os padrões de engenharia. Em repositório novo, deixa tudo no primeiro commit, em main, e entrega develop como branch de trabalho; em repositório com histórico, um commit na branch ativa, sem mexer em branch nem no remoto. Rodar uma vez, no começo do projeto.
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
perguntar. Sim, `git init -b main`: é local, barato e desfeito com `rm -rf .git`. O `-b` é o que
garante o nome — sem `init.defaultBranch` configurado, o `git init` puro cria `master`.

Montar a governança num diretório sem repositório entrega um método que não funciona, e o usuário
só descobre no primeiro fechamento de demanda.

**Dito não, o setup segue em modo arquivo**, sem primeiro commit e sem oferecer o modo issue — e
diz isso em uma linha, porque as duas coisas passam a existir assim que o usuário rodar `git init`
por conta própria. Não insistir: a estrutura criada continua válida, só não versionada.

**Onde o commit cai se decide aqui, antes de qualquer commit:**

| Estado do repositório | O setup | O commit cai em |
| --- | --- | --- |
| o setup acabou de rodar o `git init -b main` | nada | `main` |
| já existia, sem commit em branch nenhuma (`git rev-list -n 1 --all` sai vazio) | `git branch -m main`, se a branch ativa não for `main` — não há histórico para perder | `main` |
| já existia, com commit em qualquer branch | nada — as branches e o remoto são do projeto, e ele já tem um fluxo para levar mudança à produção | a branch ativa |

**Com histórico, o setup não mexe em branch.** A governança é uma mudança como outra qualquer: vai
para a branch ativa e chega à produção pelo fluxo que o projeto já tem (PR, merge). Daí em diante,
neste caso: o `CLAUDE.md` nasce sem a seção `## Git`, o `gh repo create` roda sem `--push`, e "A
`main` no remoto" e "A branch de trabalho" não rodam — trocar de branch, criar `develop` ou enviar
ao remoto seria decidir o fluxo de um projeto que o setup não criou.

## O que o ambiente permite

Com o repositório local de pé, ler o ambiente **na ordem abaixo**, anotando o que falta. Nada é
executado aqui: a leitura só decide o que a pergunta seguinte oferece, o que o setup terá de
resolver se a resposta for issue, e — no modo arquivo — se "A `main` no remoto" pode oferecer criar
o repositório.

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

**Antes desta pergunta — ou da dos padrões, quando esta não é feita —, ler
[`ferramentas.md`](ferramentas.md) inteiro**, nesta pasta: a detecção do que o usuário já usa roda
antes dela, e a linha do que achou abre o enunciado. Lá também está o que muda nesta pergunta
quando o tracker do Matt Pocock existe ou a detecção o acha.

**Antes de criar a estrutura** — é esta resposta que decide o que criar. Pergunta com opções
(`AskUserQuestion` no Claude Code), com a explicação curta de cada uma:

- **Arquivos em `docs/projeto/`** (default) — a demanda é um `.md` versionado. Zero setup,
  sobrevive ao `git clone` sem rede, entra no `grep` do repositório, não depende de fornecedor.
- **Issues (GitHub)** — a demanda é uma issue. Conversa com comentário e notificação, contribuição
  de fora em dois cliques, referência estável por `#12`, e `Fixes #12` fecha pelo merge.

**O default vai primeiro na lista**, porque a pergunta com opções apresenta a primeira como a
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
`midia/`, uma por mídia: [`arquivo.md`](../midia/arquivo.md) e [`issues.md`](../midia/issues.md).

Perguntar também **o que fazer com os padrões de engenharia** (idioma, KISS/YAGNI, validação antes
do commit, testes, acessibilidade, tratamento de credencial). Pode ir na mesma pergunta com
opções que a mídia, a critério do agente — nenhuma das duas respostas muda a outra, e o
login do `gh` funciona igual depois das duas.

**As opções dependem do que o global já tem**, porque a pergunta é sobre o que acontece com o que
existe, não só sobre onde colar. Ler o global antes — qual arquivo é, por harness, está em
`ferramentas.md`: ele **tem padrões** quando tem seção equivalente a alguma de
`templates/preferencias.md`.

Global com padrões — o default primeiro:

- **Manter o global como está** — nada é copiado nem alterado.
- **Completar o global** — acrescenta a ele só as seções que faltam lá.
- **Acrescentar no projeto** — o `CLAUDE.md` do projeto recebe só as seções que o global não tem,
  somando a ele. Quem trabalha em equipe e quer o padrão inteiro no repositório copia o resto à
  mão: o global não viaja no `git clone`.

Sem global, ou global sem padrões:

- **No global** — vale para todos os projetos da máquina.
- **No projeto** — fica versionado e viaja com o repositório.
- **Não usar** — o usuário já tem os seus em outro lugar.

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
fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser. A exceção é a seção
`## Git` do `CLAUDE.md`, que **sai inteira em repositório com histórico**: ela descreve o par
`main`/`develop` que o setup entrega, e ali ele não entrega — o fluxo de git do projeto quem escreve
é o usuário. A linha dela sobre o commit de fechamento não se perde: é regra do `/aicf:fechar-demanda`.

Se o projeto já tem `CLAUDE.md` na raiz, não substituir: mostrar a seção "Processos de
desenvolvimento" do template e propor acrescentá-la ao arquivo existente.

Projeto que já tem código também tem a parte do `CLAUDE.md` que se deduz dele — comandos, layout,
convenções —, e essa parte não é deste setup. Só no Claude Code: sugerir `/init` numa sessão
aberta com `CLAUDE_CODE_NEW_INIT=1` no ambiente (`CLAUDE_CODE_NEW_INIT=1 claude` — é variável do
processo, não liga de dentro da sessão), que explora o repositório com subagente e apresenta uma
proposta antes de escrever qualquer arquivo. O setup segue dono da governança — PRD, e o que a mídia
escolhida pedir. Num projeto sem código não há o que deduzir, e nada muda.

## `AGENTS.md` como link simbólico

`ln -s CLAUDE.md AGENTS.md` na raiz. **Um arquivo, dois nomes** — o Claude Code lê `CLAUDE.md`;
Antigravity, Codex e outros leem `AGENTS.md`. Manter os dois como arquivos separados garante que um
envelheça sem ninguém perceber.

- Se `AGENTS.md` já existe — arquivo ou link —, não tocar.
- O git versiona o link como link (modo `120000`), então ele viaja no clone.
- Em Windows sem Developer Mode, `ln -s` falha. Nesse caso, usar o que a documentação indica no
  lugar do link: o conteúdo vai para `AGENTS.md`, e o `CLAUDE.md` fica só com a linha
  `@AGENTS.md`, que importa o outro — continua um arquivo, dois nomes. Daí em diante, onde esta
  skill diz `CLAUDE.md`, o arquivo a editar é `AGENTS.md`. **Não criar uma cópia**, que é
  justamente o que o link existe para evitar.

## Os padrões de engenharia

**Manter o global como está, ou Não usar:** não colar nada, e conferir que o `CLAUDE.md` gerado
não ficou com seção equivalente vinda de `templates/preferencias.md`. **Nas outras quatro respostas, ler
[`padroes.md`](padroes.md) inteiro antes de seguir.**

Em qualquer caso, avisar sobre a única regra do template que muda o comportamento do usuário,
não só o do agente: **credencial não entra no chat** — o valor vai para o `.env` e o agente
recebe apenas o nome da variável.

## O primeiro commit

Depois de criar os arquivos e colar os padrões de engenharia, **nos dois modos**. Sem ele o
`.gitkeep` não segura pasta nenhuma, e, em repositório novo no modo issue, o push do passo seguinte
não tem o que empurrar.

**Só os caminhos que o setup escreveu, um a um** — `CLAUDE.md`, `AGENTS.md`, `README.md`,
`docs/projeto/PRD.md`, e o `ROADMAP.md` e os quatro `.gitkeep` quando a mídia é arquivo. **Nunca
`git add -A`, e nem `git add docs/projeto/`:** num diretório que já tem código não commitado, o
`-A` varre tudo, inclusive um `.env` que ainda não tem `.gitignore` para segurá-lo, e o diretório
inteiro leva junto o que estiver lá dentro. O setup não decide o que vai para o histórico de
arquivo que ele não criou.

**E o commit também nomeia os caminhos**, depois do `git add` deles:

```bash
git commit -m 'chore: estrutura de governança do projeto' -- <caminhos>
```

`git commit` sem caminhos commita o índice inteiro — inclusive o que o usuário deixou em stage antes
de rodar o setup. Com os caminhos, isso continua em stage e fora do commit — salvo o que o usuário
tinha em stage num arquivo que o setup também edita, como um `CLAUDE.md` existente, que vai junto.

**Em repositório com histórico, três estados param o setup antes do commit**, e o usuário resolve:

| Estado | Como se lê | Por que parar |
| --- | --- | --- |
| merge em andamento | `git rev-parse -q --verify MERGE_HEAD` sai com 0 | o commit com caminhos sai com 128 (`cannot do a partial commit during a merge`) |
| HEAD destacado | `git symbolic-ref -q HEAD` sai com 1 | o commit não fica em branch nenhuma |
| branch ativa sem commit, com histórico em outra ref | `git rev-parse -q --verify HEAD` sai com 1 | o commit vira raiz de uma branch sem ligação com o histórico do projeto |

Dizer o estado em uma linha e pedir que o usuário termine o merge ou faça checkout de uma branch
com histórico; o setup continua do commit, com os arquivos já criados.

A mensagem segue o idioma do projeto que está nascendo.

**Máquina sem identidade de git configurada** faz o `git commit` falhar com
`Author identity unknown`. Acontece justamente onde o `git init` acabou de rodar. Nesse caso,
mostrar `git config --global user.name` e `user.email` para o usuário rodar, e commitar depois —
não configurar a identidade dele por conta própria.

**O commit cai onde "O repositório local" decidiu:** na `main`, em repositório novo; na branch
ativa, em repositório com histórico. A branch de trabalho, quando o setup a cria, nasce depois de
tudo — ver "A branch de trabalho", no fim.

## O repositório no GitHub, e a `main` no remoto

**Ler [`remoto.md`](remoto.md) inteiro antes de seguir** quando a mídia é issue, ou quando o
repositório não tinha histórico (ver "O repositório local"). Lá estão "O repositório no GitHub, e
os labels", só do modo issue, e "A `main` no remoto", só sem histórico, nos dois modos. Modo
arquivo em repositório com histórico: pular este passo.

## A branch de trabalho

**Não roda em repositório com histórico:** a `develop` pode já existir (`git branch develop` sairia
com 128), e criar a branch de trabalho de um projeto em andamento não é do setup.

**O último passo antes do fechamento**, nos dois modos. O `CLAUDE.md` que o setup acabou de escrever
descreve `develop` como branch de trabalho e `main` como produção; este passo é o que faz o
repositório corresponder a isso, em vez de o arquivo descrever algo que não existe.

```bash
git branch develop
git switch develop
git push -u origin develop   # só se a main subiu neste setup
```

**A posição na ordem é o que importa, e ela não é arbitrária.** O `gh repo create --push` e o push
de "A `main` no remoto" rodam com `main` ativa, então é `main` que sobe primeiro
e fica sendo o default do repositório no GitHub — produção como default, que é o que o fluxo pede.
Criar a `develop` antes disso inverte o resultado: ela sobe primeiro e vira o default remoto, e
desfazer isso depois é mexer em configuração do repositório em vez de rodar um comando.

**A `develop` só sobe se a `main` subiu neste setup**, por qualquer dos dois caminhos. Remoto que
já tinha `main`, que não respondeu, ou push que o usuário recusou: a `develop` fica local, e o
remoto como o usuário o deixou.

Ao fim, `develop` é a branch ativa: é onde a primeira demanda vai commitar.

## Ao terminar

O setup é a primeira vez que o usuário vê o método funcionando, e ele termina sabendo o que ganhou
e o que fazer em seguida — não só o que foi criado no disco.

1. Listar o que foi criado e onde — os arquivos, o commit, as duas branches, o repositório se o
   setup o criou, e, no modo issue, os labels. **E o estado do remoto:** o que foi enviado, ou a linha de "A `main` no
   remoto" do caso que ficou sem envio. **Em repositório com histórico**, no lugar das branches e
   do remoto: em que branch o commit ficou, que a seção `## Git` do `CLAUDE.md` ficou de fora para
   o usuário escrever com o fluxo dele, e, se o remoto não tem branch nenhuma — criado agora ou
   vazio —, que a produção é a primeira branch a enviar.
2. **Apresentar o método em linguagem comum.** Ler o mapa com a ferramenta de leitura de arquivo (`Read` no Claude Code),
   em [`../ajuda/SKILL.md`](../ajuda/SKILL.md) — a skill `/aicf:ajuda` só o usuário invoca, e o
   harness recusaria invocá-la. **Não com `cat`**: a saída do `cat` cai inteira na tela de quem está
   conhecendo o método, que é o muro de texto que esta apresentação evita; a da ferramenta de
   leitura fica recolhida. Contar o que ele diz, em vez de colar um texto guardado aqui: texto guardado seria a
   segunda cópia do mapa e envelheceria sozinho, enquanto a skill é a fonte da verdade do ciclo. Cobrir, nesta ordem:
   - as quatro fases, uma frase cada, sem o vocabulário de governança;
   - **um exemplo concreto de primeira demanda**, do pedido até o registro fechado, usando o nome
     real do projeto e a mídia que o usuário acabou de escolher — é o exemplo que faz o ciclo sair
     do abstrato;
   - que a governança é a mesma em qualquer caminho de implementação, inclusive os de outras
     coleções.
3. Sugerir `/aicf:prd` como próximo passo — é do PRD que saem as primeiras demandas (no
   modo arquivo, o roadmap inicial; no modo issue, as primeiras issues). Depois dele, a primeira
   demanda começa por `/aicf:criar-spec`.
4. Dizer que `/aicf:ajuda` é o lugar de voltar quando quiser reler como o método
   funciona.
