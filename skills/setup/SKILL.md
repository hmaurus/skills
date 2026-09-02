---
name: setup
description: Cria a base de governança de um projeto novo — docs/projeto/ com PRD e checklist, as pastas de intents e specs e o CLAUDE.md raiz — e, se o usuário quiser, os padrões de engenharia. Rodar uma vez, no começo do projeto.
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

```
CLAUDE.md                       # raiz, se ainda não existir
AGENTS.md -> CLAUDE.md          # link simbólico
README.md                       # se ainda não existir
docs/projeto/
├── PRD.md
├── CHECKLIST.md
├── intents/
│   ├── .gitkeep
│   └── backlog/.gitkeep
└── specs/
    └── concluidas/.gitkeep
```

Os templates estão em `templates/` dentro desta skill:

| Template                 | Vai para                                        |
| ------------------------ | ----------------------------------------------- |
| `templates/claude-md.md` | `CLAUDE.md` (raiz)                              |
| `templates/prd.md`       | `docs/projeto/PRD.md`                           |
| `templates/checklist.md` | `docs/projeto/CHECKLIST.md`                     |
| `templates/readme.md`    | `README.md` (raiz)                              |
| `templates/preferencias.md` | conforme a resposta acima — ver abaixo       |

Copiar o conteúdo trocando `<NOME>` pelo nome do projeto e preenchendo a descrição no lugar
indicado. **Não reescrever o template por conta própria** — o que estiver marcado como a
preencher fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser.

Se o projeto já tem `CLAUDE.md` na raiz, não substituir: mostrar a seção "Processos de
desenvolvimento" do template e propor acrescentá-la ao arquivo existente.

Projeto que já tem código também tem a parte do `CLAUDE.md` que se deduz dele — comandos, layout,
convenções —, e essa parte não é deste setup: sugerir `/init` numa sessão aberta com
`CLAUDE_CODE_NEW_INIT=1` no ambiente (`CLAUDE_CODE_NEW_INIT=1 claude` — é variável do processo,
não liga de dentro da sessão), que explora o repositório com subagente e apresenta uma proposta
antes de escrever qualquer arquivo. O setup segue dono da governança: PRD, checklist, `intents/`, `specs/`. Num projeto sem código não
há o que deduzir, e nada muda.

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
4. Sugerir `/aicf:criar-prd` como primeira coisa — é do PRD que sai o checklist inicial.
