# O aicf quebra fora do Claude Code

Processo — entrevista: criar-spec · implementação: aicf-plan

Era backlog desde 2026-09-19, à espera de alguém rodar o aicf em outro agente. Em 2026-10-19 o
titular instalou o Antigravity CLI para escrever um sistema novo com o aicf, e a análise daquele dia
testou os três harnesses instalados nesta máquina: `agy --version` → 1.4.2, `codex --version` →
0.163.0, `opencode --version` → 1.17.11.

## Problema

Quem usa o aicf fora do Claude Code recebe as skills, mas algumas instruções dão resultado errado
lá. Os números abaixo são do commit `504276c`.

1. **O Antigravity corta o `setup` no meio.** Ele carrega no máximo 24.000 bytes de cada
   `SKILL.md`. O `skills/setup/SKILL.md` tem 31.930 (`wc -c skills/setup/SKILL.md`), e o corte
   cai no meio de "O repositório no GitHub, e os labels". O agente nunca lê "A `main` no remoto",
   "A branch de trabalho" nem "Ao terminar", que trazem o envio ao remoto, a `develop`, a
   apresentação do método e a sugestão do `/aicf:prd`. Para ver o aviso, monte a forma que o
   `agy plugin install` gera a partir do plugin do Claude Code:
   `T=$(mktemp -d); mkdir $T/aicf; cp -r skills .claude-plugin $T/aicf/; echo '{"name":"aicf"}' > $T/aicf/plugin.json; agy plugin validate $T/aicf`
   → `⚠ skills/setup/SKILL.md: the body is 31260 bytes; only the first 24000 are loaded`.
2. **O Codex ignora o `disable-model-invocation`.** Com o aicf instalado pelo marketplace, o
   `codex exec` mostrou `aicf:setup`, `aicf:ajuda` e `aicf:criar-prd` no contexto do modelo. A
   description das três ocupa o contexto de toda sessão, e é exatamente isso que o campo evita no
   Claude Code ([o PRD envelhece sem ninguém conferir](../concluidas/o-prd-envelhece-sem-ninguem-conferir.md)).
   O opencode também ignora o campo, e o `SKILL.md` não tem outro jeito de esconder uma skill dele.
3. **A promoção de conhecimento grava onde só o Claude Code lê.** O passo 3 do
   `/aicf:fechar-demanda` e o template do `CLAUDE.md` mandam regra para `.claude/rules/`, skill
   para `.claude/skills/` e hook para `.claude/settings.json`. São 5 ocorrências:
   `grep -rnoE '\.claude/(rules|skills|settings\.json)' skills/ | wc -l` → 5. O Antigravity lê
   `.agents/rules/`, `.agents/skills/` e `.agents/hooks.json`, e lá a regra por caminho usa
   `trigger: glob` com `globs:`, não `paths:`. A doc fica em
   `~/.gemini/antigravity-cli/builtin/skills/agy-customizations/docs/`, e o formato da regra no
   `agy changelog | grep 'a .glob. rule'`.
4. **O setup detecta o ambiente pelo Claude Code.** Ele lê as coleções do `claude plugin list`, as
   docs do `claude mcp list` e o cofre do `~/.claude/CLAUDE.md`. No Antigravity, numa máquina onde
   o CLI `claude` também existe, isso acha o que está instalado no Claude Code, não no `agy`.
   `grep -noE 'claude (plugin|mcp) list|~/\.claude/CLAUDE\.md' skills/setup/SKILL.md | wc -l` → 6.
5. **A prosa trata ferramenta do Claude Code como se fosse de todos.** São 18 citações:
   ``grep -rnoE 'AskUserQuestion|/clear|ferramenta `?Read`?|ferramenta Skill|CLAUDE_CODE_NEW_INIT|/code-review' skills/ --include='*.md' | wc -l``
   → 18. Subagente e plan mode existem nos três harnesses e ficam como estão.
6. **O PRD e o README só falam de Claude Code.** O PRD põe outros agentes fora do escopo
   (`grep -n 'Outros agentes' docs/projeto/PRD.md`). O README só ensina a instalar pelo `/plugin`,
   e não diz como invocar uma skill fora do Claude Code.

**O que já funciona e não muda**, testado em 2026-10-19:

- O `AGENTS.md` como link para o `CLAUDE.md`, que o setup cria, é lido pelo Antigravity e pelo
  Codex. O teste foi uma palavra-código no `CLAUDE.md` de uma pasta de teste, e os dois a
  repetiram.
- No Antigravity, `/aicf:nome` invoca a skill: o evento `init` de
  `agy -p "/aicf:ajuda" --output-format stream-json` traz
  `"expanded_commands": [{"name": "aicf:ajuda", "type": "skill"}]`, e `/ajuda` não expande. O
  Antigravity também esconde do modelo as três skills com `disable-model-invocation`.
- O opencode acha as sete skills copiadas para `.opencode/skills/` (`opencode debug skill`) e
  ignora a pasta `midia/`. Com link simbólico, ele acha zero.

## Solução

**Claude Code e Antigravity passam a ser alvos. Codex e opencode passam a ser compatíveis, sem
garantia:** o aicf evita quebrar neles e registra o que foi testado, mas não os testa a cada
versão. Motivo: o titular usa o Antigravity e consegue exercitá-lo; nos outros dois ninguém
exercita o ciclo.

1. **PRD.** Em "Dentro", o Antigravity entra como alvo ao lado do Claude Code. A entrada "Outros
   agentes" de "Fora, por decisão" passa a dizer que Codex e opencode são compatíveis, sem
   garantia, e que Cursor e os demais seguem fora, com o motivo. Em "Riscos", o Antigravity mudar
   o formato ou o limite, e a mitigação: o `check.sh` pega o limite de tamanho, e o
   `agy plugin validate` roda localmente.
2. **`GLOSSARY.md`.** Entra **Harness**: o agente que carrega e roda as skills (Claude Code,
   Antigravity, Codex, opencode). A entrada separa **alvo**, testado a cada versão, de
   **compatível**, que não quebra de propósito mas não é testado. _Evitar_: ferramenta, CLI.
3. **O `setup` fica abaixo de 22.000 bytes**, uma folga de 2.000 sob o corte. O que só vale em
   alguns casos sai para arquivos na própria pasta da skill:
   - `skills/setup/remoto.md`: "O repositório no GitHub, e os labels" e "A `main` no remoto";
   - `skills/setup/ferramentas.md`: "Ferramentas que o usuário já usa";
   - `skills/setup/padroes.md`: "Os padrões de engenharia", que só roda se o usuário quiser.

   No ponto de onde cada seção saiu, o `SKILL.md` diz em que condição ler o arquivo e manda lê-lo
   inteiro antes de seguir. A regra é do próprio setup, então o ponteiro é para arquivo da pasta
   dele, não para outra skill. "Ao terminar" fica no `SKILL.md`. Se os três arquivos não bastarem
   para descer de 22.000, o plano diz o que mais sai antes de mover.
4. **O `check.sh` reprova `SKILL.md` acima de 24.000 bytes**, num quarto bloco que imprime quantas
   skills conferiu e roda também no CI. O limite vale só para o `SKILL.md`: o corte do Antigravity
   é sobre ele. A seção "Verificação" do `.claude/CLAUDE.md` passa a citar a linha nova da saída
   saudável.
5. **`agents/openai.yaml` em `setup`, `prd` e `ajuda`**, com
   `policy:` / `allow_implicit_invocation: false`. É o campo que o Codex lê para esconder a skill
   do modelo e continuar aceitando `$aicf:nome`. Uma cópia com o arquivo passou no
   `claude plugin validate skills --strict`. Na pasta de teste, o Codex listou só `criar-spec`,
   `fechar-demanda`, `implementar-spec` e `proxima-demanda`. As descriptions não ganham frase
   nenhuma: o campo existe para poupar contexto, e uma frase a mais gastaria contexto nos harnesses
   que não o leem.
6. **Promoção de conhecimento pelo harness em uso.** A tabela do passo 3 do `/aicf:fechar-demanda`
   dá, em cada linha, o caminho do Claude Code e o do Antigravity (`.agents/rules/<tema>.md` com
   `trigger: glob` e `globs:`, `.agents/skills/`, `.agents/hooks.json`). O agente grava no do
   harness em que está rodando. Uma linha cobre os compatíveis: skill em `.agents/skills/`, que
   Codex e opencode leem; regra por caminho e hook vão como regra no `AGENTS.md`. O template
   `skills/setup/templates/claude-md.md` troca as duas menções a `.claude/` pela mesma dupla.
7. **A detecção do setup pelo harness em uso**, em `skills/setup/ferramentas.md`:
   - no Claude Code, como é hoje;
   - no Antigravity, as coleções saem de
     `agy plugin list --json | jq -r '.[] | select(.enabled) | .name'`, as docs de `agy mcp list` e
     o cofre do `~/.gemini/config/AGENTS.md` (também `~/.gemini/GEMINI.md` e `~/.gemini/AGENTS.md`);
   - em outro harness, perguntar, como o texto já faz quando não há CLI `claude`, **mesmo que o
     CLI `claude` exista na máquina**.
8. **Ferramenta do Claude Code ganha nome genérico, com o nome dela entre parênteses.** Por
   exemplo: "pergunta com opções (`AskUserQuestion` no Claude Code)", "limpar a sessão (`/clear`
   no Claude Code)", "ler o arquivo com a ferramenta de leitura (`Read` no Claude Code)". O
   `CLAUDE_CODE_NEW_INIT` e o `/code-review` ganham "só no Claude Code". Sempre "Claude Code" por
   extenso: cada skill carrega sozinha, e uma sigla não teria definição no contexto dela.
9. **README, em `README.md` e `README.en.md`.** A frase de abertura passa a dizer "para Claude Code
   e Antigravity". "Instalação" ganha uma subseção por harness, com instalar e atualizar, e diz
   qual é alvo e qual é compatível. Uma tabela diz como invocar em cada um: `/aicf:nome` no Claude
   Code e no Antigravity, `$aicf:nome` no Codex, e no opencode pedir a skill pelo nome, sem
   prefixo. No opencode: copiar as pastas, porque link simbólico não é lido, e o agente pode
   invocar `setup`, `prd` e `ajuda` sozinho. As skills continuam escrevendo `/aicf:nome`.
10. **[`verificacao-do-setup.md`](../../referencias/verificacao-do-setup.md)** ganha a passada do
    Antigravity como condição em aberto (ver Verificação).

## Arquivos

- `skills/setup/SKILL.md`, mais `skills/setup/remoto.md`, `ferramentas.md` e `padroes.md`, novos
- `skills/setup/templates/claude-md.md`
- `skills/{setup,prd,ajuda}/agents/openai.yaml`, novos
- `skills/fechar-demanda/SKILL.md` (passo 3) e a prosa das skills com as 18 citações
- `scripts/check.sh` e `.claude/CLAUDE.md` (seção "Verificação")
- `docs/projeto/PRD.md`, `GLOSSARY.md`, `README.md`, `README.en.md`
- `docs/referencias/verificacao-do-setup.md`
- `.claude-plugin/plugin.json` e `CHANGELOG.md`: versão nova

## Testes

O código que muda é o `scripts/check.sh`, e o ponto de teste é ele mesmo. O bloco novo tem que
reprovar o setup de hoje antes da divisão e passar depois dela. O teste parecido que já existe é o
bloco da versão no `CHANGELOG.md`, no mesmo script. O resto é texto de skill, conferido pelas
passadas da Verificação.

## Fora de escopo

- **Atualizar as cópias instaladas nesta máquina** (agy em 0.39.0, Codex em 0.38.1, opencode sem
  o aicf). É a próxima demanda, decidida na entrevista. Ela segue o README que esta escrever, e
  isso testa o README.
- **Manifesto nativo do Antigravity e publicação no marketplace dele.** O `agy plugin install`
  converte o plugin do Claude Code: `agy plugin validate .` diz
  `This looks like a Claude Code plugin: plugin install converts it`.
- **Esconder `setup`, `prd` e `ajuda` do modelo no opencode.** O frontmatter dele só reconhece
  `name`, `description`, `license`, `compatibility` e `metadata`, e uma frase na description
  gastaria o contexto que o campo existe para poupar. O README avisa.
- **Trocar a sintaxe `/aicf:nome` nas skills.** Ela vale nos dois alvos, e o README traduz para os
  compatíveis.
- **Detecção automática no Codex e no opencode.** São compatíveis, então o setup pergunta.
- **`agy plugin validate` no CI.** O CI não tem o `agy`. O limite conhecido fica no `check.sh`, e
  o validate roda localmente, na Verificação.
- **O aviso `AGENTS.md: never loaded` do `agy plugin validate`.** O `AGENTS.md` da raiz é o link de
  desenvolvimento deste repositório, não regra do plugin.
- **Cursor e outros agentes.** Ninguém os exercita.

## Verificação

1. **O check pega o setup grande.** Com o bloco novo no `check.sh` e o setup ainda inteiro,
   `./scripts/check.sh` reprova citando `skills/setup/SKILL.md`. Depois da divisão, termina em
   `Tudo verde.` com a linha nova do tamanho. Conferir com `git diff --stat` que a divisão de fato
   mudou o arquivo antes de acreditar no verde.
2. `wc -c skills/setup/SKILL.md` → abaixo de 22.000.
3. **Antigravity**: o mesmo `agy plugin validate $T/aicf` do Problema, numa cópia nova, não traz
   mais o aviso `only the first 24000 are loaded`.
4. **Codex**: num repositório de teste com `skills/` copiado para `.agents/skills/`,
   `codex exec -s read-only "Sem executar comandos: liste os nomes das skills do seu contexto cujo caminho fica em .agents/skills. Só a lista."`
   lista `criar-spec`, `fechar-demanda`, `implementar-spec` e `proxima-demanda`, e não lista
   `setup`, `prd` nem `ajuda`.
5. **opencode**: num repositório de teste com `skills/` copiado para `.opencode/skills/`,
   `opencode debug skill` lista as sete.
6. **A prosa**: `grep -rnE 'AskUserQuestion|/clear' skills/ --include='*.md' | grep -vc 'no Claude Code'`
   → 0. E `grep -rnE '\.claude/(rules|skills|settings\.json)' skills/ | grep -vc '\.agents/'` →
   0: toda linha com caminho do Claude Code traz o do Antigravity.
7. **Em aberto, pelo titular: o `/aicf:setup` no Antigravity.** Só o usuário o invoca, e o agente
   não o roda. Encerra no primeiro uso real, que é o setup do sistema novo, depois que a próxima
   demanda atualizar a cópia do `agy`. Três coisas precisam aparecer: o setup chega a "Ao
   terminar" (apresenta o método e sugere `/aicf:prd`); a `develop` existe
   (`git branch --list develop`); e a linha da detecção declara o que o `agy plugin list` mostra,
   não o `claude plugin list`. A condição fica em `verificacao-do-setup.md`.

## Relatório de implementação (2026-10-20)

- **Status** — concluído na `0.41.0`. Fica em aberto, pelo titular, a passada do `/aicf:setup` no
  Antigravity (Verificação 7), registrada em
  [`verificacao-do-setup.md`](../../referencias/verificacao-do-setup.md): encerra no primeiro uso
  real, depois que a demanda seguinte do `ROADMAP.md` atualizar a cópia do `agy`.
- **Arquivos alterados**
  - `skills/setup/SKILL.md`, e os novos `ferramentas.md`, `padroes.md` e `remoto.md` na mesma pasta
  - `skills/{setup,prd,ajuda}/agents/openai.yaml`, novos
  - `skills/fechar-demanda/SKILL.md` (passo 3, description, revisão), `criar-spec`, `prd`,
    `implementar-spec` e `skills/setup/templates/claude-md.md`
  - `scripts/check.sh` (quarto bloco) e `.claude/CLAUDE.md` (Verificação e Publicação)
  - `docs/projeto/PRD.md`, `GLOSSARY.md`, `README.md`, `README.en.md`,
    `docs/referencias/verificacao-do-setup.md`, `.claude-plugin/plugin.json`, `CHANGELOG.md`
- **Commits**
  - `14876db` refactor(setup): move as seções condicionais para arquivos da pasta
  - `4571432` feat: 0.41.0 — o aicf roda no Antigravity, e não quebra no Codex nem no opencode
  - `1cec23c` fix(setup): achados da revisão da 0.41.0
- **Validação**
  - Teste antes: com o bloco novo e o setup inteiro, `./scripts/check.sh` reprovou com
    `skills/setup/SKILL.md tem 31930 bytes`; depois do `14876db`, `Tudo verde.` com
    `7 skills conferidas, nenhuma acima de 24000 bytes`.
  - `wc -c skills/setup/SKILL.md` → 21496.
  - Antigravity: o `agy plugin validate` do Problema numa cópia nova → `✔ Validation passed`, sem
    `only the first 24000 are loaded`.
  - Codex: o `codex exec` da Verificação 4 listou `criar-spec`, `fechar-demanda`,
    `implementar-spec` e `proxima-demanda`.
  - opencode: `opencode debug skill` achou as sete em `.opencode/skills/` e em
    `~/.config/opencode/skills/` (com `HOME` isolado).
  - Os dois greps da Verificação 6 → 0 e 0.
  - Os comandos de instalar e atualizar do README rodaram com `HOME` e `CODEX_HOME` isolados no
    scratchpad, sem tocar nas cópias instaladas.
  - Revisão de código por subagente fresco, sobre `4c4ad88..4571432`: nada bloqueava; os três
    pontos a corrigir e quatro dos menores entraram no `1cec23c`.
- **Escopo efetivo**
  - Saiu do setup mais que as três seções da spec: os parágrafos do Matt Pocock da pergunta da
    mídia foram para `ferramentas.md`. Só as três deixariam o arquivo perto de 22.400 bytes,
    acima da meta de 22.000.
  - O ponteiro de `ferramentas.md` ficou no topo de "A mídia do registro", não no lugar antigo da
    seção, porque a detecção roda antes dessa pergunta.
  - "O global" passou a depender do harness também na pergunta dos padrões e em `padroes.md`, não
    só na detecção do cofre: sem isso, o setup no Antigravity completaria o global do Claude Code.
  - O `/code-review` da tabela do `implementar-spec` ficou sem "só no Claude Code": é a skill do
    Matt Pocock que o `implement` chama.
  - O `.claude/CLAUDE.md` ganhou o `agy plugin validate` como passo antes da release. A revisão
    apontou que "testado a cada versão" não tinha mecanismo que o cumprisse.
  - A data "Última revisão" do PRD não mudou: ela marca a revisão pelo `/aicf:prd`, e esta edição
    veio da spec.
- **Lições**
  - `opencode debug skill` direto num pipe corta a saída, e o `jq` acusa `parse error`; salvo em
    arquivo, sai inteira. O comando certo está em
    [`harnesses.md`](../../referencias/harnesses.md).
  - Sobram citações só do Claude Code que o grep da spec não cobre: o `!` da sessão no setup, o
    `/doctor` no fechamento e no template, e o "Other" do menu no `criar-spec`. Nenhuma quebra o
    fluxo fora dele.
  - Passo 3: nasceu [`docs/referencias/harnesses.md`](../../referencias/harnesses.md), com como
    testar em cada harness sem mexer nas cópias instaladas e os limites de cada um. Entrou um item
    no Backlog do `ROADMAP.md`: o corte de 24.000 bytes também vale para o `AGENTS.md`.
