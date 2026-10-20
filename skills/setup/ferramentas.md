# Ferramentas que o usuário já usa

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
caminhos de entrevista e implementação que o aicf oferece mudam — sem elas, só o
caminho aicf existe, e propor `brainstorming` seria propor algo que não roda.

**Detectar antes de perguntar.** Quem já usa o método costuma ter as três respostas na máquina, e
perguntar o que o ambiente responde é rodada gasta. **As fontes são as do harness em que o setup
está rodando**, não as de qualquer CLI que exista na máquina: no Antigravity, um CLI `claude`
instalado ao lado responde pelo Claude Code, e acharia o que não está no `agy`.

**O global** é o arquivo de instruções do usuário que vale para todos os projetos da máquina:
`~/.claude/CLAUDE.md` no Claude Code; no Antigravity, `~/.gemini/config/AGENTS.md`, ou
`~/.gemini/GEMINI.md` e `~/.gemini/AGENTS.md`, que ele também lê. É o que a pergunta dos padrões
lê, e o que `padroes.md` completa. Três fontes, uma por pergunta:

- **cofre** — o global, onde ele aparece declarado em prosa. Ter o binário `bw` ou `op` na máquina
  não conta: não diz que é o cofre que o usuário usa;
- **fonte de docs** — o global, ou a lista de servidores MCP: no Claude Code, `claude mcp list`,
  que mostra o Context7 tanto instalado como plugin (`plugin:context7:context7`) quanto
  configurado direto como servidor MCP; no Antigravity, `agy mcp list`, onde ele aparece como
  `context7`;
- **coleções** — no Claude Code, os plugins habilitados **neste diretório**; Superpowers e Matt
  Pocock aparecem pelo id (`superpowers@…`, `mattpocock-skills@…`):

  ```bash
  claude plugin list --json | jq -r --arg d "$PWD" \
    '.[] | select(.enabled and (.scope=="user" or .projectPath==$d)) | .id'
  ```

  **Não ler `~/.claude/plugins/cache/`**: o cache guarda também plugin desabilitado. E **não
  tirar o filtro de escopo**: sem ele, plugin habilitado só em outro projeto conta como instalado
  aqui. No Antigravity, os plugins habilitados aparecem pelo nome (`superpowers`,
  `mattpocock-skills`):

  ```bash
  agy plugin list --json | jq -r '.[] | select(.enabled) | .name'
  ```

**Em outro harness** — Codex, opencode, qualquer um que leia o `AGENTS.md` —, não há detecção:
perguntar o global e as três respostas, **mesmo que o CLI `claude` exista na máquina**.

**O que a detecção achou, declarar numa linha e seguir, sem perguntar** — *"Achei Bitwarden e
Context7 no seu global, e Superpowers e Matt Pocock habilitados; vou registrar assim."* **A linha
abre o enunciado da pergunta da mídia** (o campo `question` do `AskUserQuestion` no Claude Code),
antes da pergunta em si —
não num texto solto antes da chamada, que o agente pula. A detecção roda antes dela, e é essa
posição que deixa o usuário corrigir antes de qualquer arquivo existir. Aparecer só no resumo
final, depois do commit, é o mesmo que não declarar.

**O que não achou, explicar em uma frase e sugerir, numa pergunta só com os itens que faltaram** —
Bitwarden (CLI `bw`, plano gratuito generoso) para senhas, Context7 para docs, Superpowers e Matt
Pocock para coleções — e aceitar "nenhum" como resposta: quem está começando não tem nada disso, e insistir transforma o setup em
venda de stack. **Coleção se sugere, não se instala:** plugin instalado no meio da sessão só carrega
na próxima, e a linha do `CLAUDE.md` registra o que estava habilitado agora.

Registrar as respostas onde elas já têm lugar: as duas primeiras nas seções de segurança e de
dependências dos padrões de engenharia (em `padroes.md`); a terceira, na linha "Coleções de skills de
workflow instaladas" de "Processos de desenvolvimento" do `CLAUDE.md` — é dela que o
`implementar-spec` tira os caminhos que oferece. **Nome da ferramenta e nome da variável de ambiente — nunca o valor.**

## O Matt Pocock e a pergunta da mídia

**Se `docs/agents/issue-tracker.md` existe**, o `/setup-matt-pocock-skills` já respondeu a mesma
pergunta — onde o trabalho mora. Ler e propor o default a partir dele ("o tracker do Matt aponta
para GitHub; usar issues aqui também?") em vez de perguntar do zero. As duas configs seguem
independentes: divergir é legítimo, e a do aicf é a linha do `CLAUDE.md`; divergindo, o caminho do
Matt sai das opções do `/aicf:implementar-spec`.

**Se o arquivo não existe e a detecção achou o Matt Pocock habilitado**, o setup dele ainda vai
fazer a mesma pergunta, do zero. A descrição de cada opção ganha uma frase, que fica ao lado da
escolha e não no enunciado:

- **arquivos**: o `/setup-matt-pocock-skills` vai perguntar o mesmo, e em arquivo o Matt guarda o
  trabalho dele em `.scratch/`, separado de `docs/projeto/` — no setup do Matt, escolher markdown
  local;
- **issues**: no setup do Matt, escolher GitHub, e os dois ficam nas mesmas issues.

Só informar no modo arquivo, sem ensinar a apontar o tracker do Matt para `docs/projeto/`: o tracker local do Matt recebe também tickets e
mapas, e apontá-lo para `docs/projeto/` misturaria tudo isso nas pastas de estado do aicf. O setup
não edita o tracker do Matt: a convenção que manda a spec para `docs/projeto/specs/` entra nele na
primeira spec entrevistada pelo `grill-with-docs`, ou na primeira vez que o caminho do Matt for
escolhido no `/aicf:implementar-spec`.
