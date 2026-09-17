---
name: setup
description: Cria a base de governança de um projeto novo — pergunta se a demanda mora em arquivos ou em issues do GitHub, e monta o que a escolha pedir: docs/projeto/ com PRD e roadmap e as pastas de demanda, ou os labels aicf:*, mais o CLAUDE.md raiz — e, se o usuário quiser, os padrões de engenharia. Rodar uma vez, no começo do projeto.
disable-model-invocation: true
---

# Setup da governança do projeto

Monta a estrutura que o restante do método assume. Roda uma vez, num projeto novo ou num que
ainda não tem `docs/projeto/`.

**Nunca sobrescrever arquivo existente.** Se algum dos alvos já existe, mostrar quais e
perguntar antes: pular, ou mostrar o diff e deixar o usuário decidir arquivo por arquivo.

## Antes de criar

Perguntar, em pergunta aberta:

1. **Nome do projeto** — se o diretório já tem nome óbvio, propor esse e confirmar.
2. **O que é, em uma ou duas frases** — o suficiente para o `CLAUDE.md` não nascer vazio.

Não entrevistar além disso. Visão, público e modelo entram no PRD depois, com calma — o setup
só prepara o lugar onde eles vão morar.

## A mídia do registro

**Antes de criar qualquer coisa** — é esta resposta que decide o que criar. `AskUserQuestion`,
com a explicação curta de cada uma:

- **Arquivos em `docs/projeto/`** (default) — a demanda é um `.md` versionado. Zero setup,
  sobrevive ao `git clone` sem rede, entra no `grep` do repositório, não depende de fornecedor.
- **Issues (GitHub)** — a demanda é uma issue. Conversa com comentário e notificação, contribuição
  de fora em dois cliques, referência estável por `#12`, e `Fixes #12` fecha pelo merge.

**Só oferecer issues se o repositório aguentar.** Conferir antes: `gh auth status` passa, e
`git remote -v` aponta para GitHub. Não aguentando, oferecer só arquivo e dizer **em uma linha** o
que falta para a outra opção existir — deixar o usuário escolher um caminho que falha no primeiro
comando é pior que não oferecer.

**Se `docs/agents/issue-tracker.md` existe**, o `/setup-matt-pocock-skills` já respondeu a mesma
pergunta — onde o trabalho mora. Ler e propor o default a partir dele ("o tracker do Matt aponta
para GitHub; usar issues aqui também?") em vez de perguntar do zero. As duas configs seguem
independentes: divergir é legítimo, e a do aicf é a linha do `CLAUDE.md`.

**Gravar a linha sempre, nos dois modos**, na seção "Processos de desenvolvimento" do `CLAUDE.md`:

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

Linha ausente significa arquivo — é a compatibilidade com projeto anterior a esta escolha existir,
não um valor a ser deixado implícito em projeto novo. As receitas de cada mídia estão em
[`workflow-demanda/references/midia.md`](../workflow-demanda/references/midia.md).

Depois, com `AskUserQuestion`, perguntar **onde ficam os padrões de engenharia** (idioma,
KISS/YAGNI, validação antes do commit, testes, acessibilidade, tratamento de credencial):

- **No global** (`~/.claude/CLAUDE.md`) — valem para todos os projetos da máquina. Escolha
  natural para quem trabalha sozinho em vários repositórios com o mesmo padrão.
- **No projeto** (`CLAUDE.md` da raiz) — ficam versionados e viajam com o repositório. Escolha
  natural para trabalho em equipe, ou quando este projeto tem padrão próprio.
- **Nenhum dos dois** — o usuário já tem os seus.

## Ferramentas que o usuário já usa

Três perguntas, porque as três mudam o comportamento do agente daqui para a frente. Perguntar
uma de cada vez, em pergunta aberta, e aceitar "nenhuma" como resposta — quem está começando
não tem nada disso, e insistir transforma o setup em venda de stack.

**1. Gerenciador de senhas.** Onde mora a credencial que não cabe no `.env` — senha de painel,
chave de produção, credencial usada em mais de uma máquina. Importa porque esses cofres têm CLI:
o agente lê um campo específico sem o valor passar pelo chat, o que não acontece quando o
usuário cola a chave na conversa. Se não usa nenhum: o `.env` sozinho funciona numa máquina só,
mas some com ela e não dá para compartilhar. Opções: Bitwarden (CLI `bw`, plano gratuito
generoso), 1Password (CLI `op`, integra direto no `.env` com `op://`).

**2. Fonte de documentação de biblioteca.** Conhecimento de treino envelhece; a API da lib que o
agente "lembra" pode ser de duas versões atrás. Um MCP de documentação — Context7, por exemplo —
faz o agente consultar a doc atual antes de escrever a chamada. Se não usa nenhum: registrar
que a doc oficial é consultada na mão.

**3. Coleções de skills de workflow.** Se o usuário já tem Superpowers ou as skills do Matt
Pocock instaladas, os caminhos de entrevista e implementação que `/aicf:workflow-demanda`
oferece mudam — sem elas, só o caminho aicf existe, e propor `brainstorming` seria propor algo
que não roda. Confirmar o que está instalado em vez de supor.

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
| `intents/`, `intents/backlog/`, `specs/concluidas/`     | sim          | **não**    |
| Os três labels `aicf:*`                                 | não          | **sim**    |

```
CLAUDE.md                       # raiz, se ainda não existir
AGENTS.md -> CLAUDE.md          # link simbólico
README.md                       # se ainda não existir
docs/projeto/
├── PRD.md                      # nos dois modos
├── ROADMAP.md                  # só modo arquivo
├── intents/                    # só modo arquivo
│   ├── .gitkeep
│   └── backlog/.gitkeep
└── specs/                      # só modo arquivo
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
| `templates/readme.md`    | `README.md` (raiz)                              |
| `templates/preferencias.md` | conforme a resposta acima — ver abaixo       |

### Os três labels, no modo issue

Criar com `gh label create`. **Criação idempotente**: label que já existe vira aviso, não erro —
daí o `|| true`. Os comandos, com as descrições, estão em
[`workflow-demanda/references/midia.md`](../workflow-demanda/references/midia.md), na seção "Criar
os labels".

**O setup é quem cria os labels**, e não a primeira demanda: `gh issue create --label` com label
inexistente **falha em vez de criar**. É a armadilha mais repetida sobre setups que só gravam o
mapeamento e deixam os labels para depois.

Copiar o conteúdo trocando `<NOME>` pelo nome do projeto, **escrevendo na linha `**Mídia do registro:**` o valor que a pergunta da mídia respondeu** — é a única fonte da verdade da escolha, e deixá-la com o texto do template faz toda skill ler a mídia errada — e preenchendo a descrição no lugar
indicado. **Não reescrever o template por conta própria** — o que estiver marcado como a
preencher fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser.

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

**Se o usuário escolheu o global:**

1. Ler `~/.claude/CLAUDE.md`. Se não existe, criar com o conteúdo do template.
2. Se existe, **não sobrescrever e não anexar direto**: mostrar quais seções do template ainda
   não têm equivalente lá e propor acrescentar só essas. Aquele arquivo vale para todos os
   projetos da máquina — inclusive os que não usam este método. Mexer nele sem confirmação
   é fora de escopo desta skill.

**Se o usuário escolheu o projeto:** colar as seções no `CLAUDE.md` da raiz, depois de
"Processos de desenvolvimento".

**Se escolheu nenhum dos dois:** não colar nada, e conferir que o `CLAUDE.md` gerado não
ficou com seção equivalente vinda do outro template. Padrão que já vale pelo global não se
repete no projeto — cópia reduzida da regra global enfraquece a regra.

Em qualquer caso, avisar sobre a única regra do template que muda o comportamento do usuário,
não só o do agente: **credencial não entra no chat** — o valor vai para o `.env` e o agente
recebe apenas o nome da variável.

## Ao terminar

1. Listar o que foi criado e onde.
2. Pedir que, na próxima sessão, o usuário rode `/context` e confira o `CLAUDE.md` na lista
   **Memory files**. O arquivo carrega no início da sessão, e essa lista é a prova de que carregou
   — em vez de supor.
3. Dizer que o mapa do ciclo está em `/aicf:workflow-demanda`, e que a primeira demanda pode
   começar por `/aicf:criar-spec`.
4. Sugerir `/aicf:criar-prd` como primeira coisa — é do PRD que saem as primeiras demandas (no
   modo arquivo, o roadmap inicial; no modo issue, as primeiras issues).
