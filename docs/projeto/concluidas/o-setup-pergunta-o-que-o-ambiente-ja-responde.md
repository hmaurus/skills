# O setup pergunta o que o ambiente já responde, e despeja o mapa na tela

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

A primeira passada de verificação de cada ramo do `/aicf:setup` rodou em 2026-09-21, na `0.24.0`:
o ramo issue num diretório `teste-aicf-issues`, o ramo arquivo num `app1`. As duas **passaram** —
as condições de [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md) deram o
esperado e nenhum arquivo gerado tinha defeito. O que elas acharam foi o agente desviando do
roteiro em quatro pontos, três deles nas duas passadas, com agentes diferentes. Evidência nos
transcripts `~/.claude/projects/-home-mh-dev-tmp-teste-aicf-issues/*.jsonl` e
`~/.claude/projects/-home-mh-dev-tmp-app1/*.jsonl`.

1. **As perguntas de ferramentas perguntam o que o ambiente já responde.** O roteiro manda
   perguntar gerenciador de senhas, fonte de documentação e coleções de skills *"uma de cada vez,
   em pergunta aberta"*. Na máquina de quem já usa o método, o `~/.claude/CLAUDE.md` declara as
   duas primeiras, e as coleções estão instaladas. Os agentes leram o global e o disco e pediram
   uma confirmação só, ou nenhuma. O roteiro não prevê isso.
2. **O mapa do workflow cai na tela.** O passo 2 de "Ao terminar" manda *"carregar
   `/aicf:workflow-demanda`"*, e os dois agentes fizeram `cat` do `SKILL.md` — 167 linhas na
   `0.24.0` (`git show 7fcb5dc:skills/workflow-demanda/SKILL.md | wc -l`, no commit que subiu a `0.24.0`) no meio da apresentação
   do método, para quem está vendo o aicf pela primeira vez. Contraria
   [a entrada de quem chega](../concluidas/a-entrada-de-quem-chega.md), cuja restrição era o setup
   não virar muro de texto.
3. **A ordem das opções da mídia.** Na passada do ramo issue, *Issues (GitHub)* saiu como primeira
   opção, e o `AskUserQuestion` apresenta a primeira como a sugerida. O roteiro diz que o default é
   arquivo, mas não diz que default é a primeira opção. O nome do diretório provavelmente enviesou;
   num projeto real o nome também enviesa.
4. **Mídia e padrões numa chamada só.** O roteiro descreve duas chamadas de `AskUserQuestion`, e os
   dois agentes juntaram as duas perguntas numa. Funcionou e economizou uma rodada.

## Solução

Quatro mudanças no `skills/setup/SKILL.md`, uma por ponto.

### 1. Ferramentas: detectar, declarar, e só perguntar o que faltar

A seção "Ferramentas que o usuário já usa" deixa de ser três perguntas e passa a ser **detecção
seguida de declaração**. A regra de quando cada item se aplica não muda: senhas e docs só quando os
padrões de engenharia vão para o global ou para o projeto; coleções sempre.

- **Detectar antes de perguntar**, em duas fontes:
  - o `~/.claude/CLAUDE.md` — cofre e fonte de docs declarados em prosa;
  - `claude plugin list --json`, filtrado pelo que vale **neste diretório**:

    ```bash
    claude plugin list --json | jq -r --arg d "$PWD" \
      '.[] | select(.enabled and (.scope=="user" or .projectPath==$d)) | .id'
    ```

    Superpowers (`superpowers@…`), Matt Pocock (`mattpocock-skills@…`) e Context7 (`context7@…`)
    aparecem aí pelo id. **Não usar `ls ~/.claude/plugins/cache/`**, que foi o que os agentes das
    passadas fizeram: o cache guarda também plugin desabilitado — o `firecrawl` estava lá com
    `enabled: false` quando esta spec foi escrita. E **não dispensar o filtro de escopo**: sem ele,
    plugin habilitado só em outro projeto conta como instalado aqui (na máquina onde a spec foi
    escrita, o Superpowers aparecia cinco vezes, quatro delas de escopo `project` em outros
    diretórios).
- **Achou → declara numa linha e segue, sem perguntar.** Ex.: *"Achei Bitwarden e Context7 no seu
  global, e Superpowers e Matt Pocock habilitados; vou registrar assim."* A declaração é o que
  deixa o usuário corrigir antes do commit — pular a pergunta em silêncio não vale.
- **Não achou → explica em uma frase e sugere**: Bitwarden para senhas, Context7 para docs,
  Superpowers e Matt Pocock para coleções — o porquê de cada um já está no roteiro. **Aceitar
  "nenhum"** continua valendo; insistir transforma o setup em venda de stack.
- **Coleção se sugere, não se instala.** Plugin instalado no meio da sessão só carrega na próxima; a
  linha "Coleções de skills de workflow instaladas" registra o que estava habilitado na hora do
  setup.
- **Sem o CLI `claude`** (outro harness, pelo `AGENTS.md`), a detecção de plugin não existe: volta
  a perguntar o que o global não respondeu.

O registro das respostas não muda: senhas e docs nas seções dos padrões de engenharia, coleções na
linha do `CLAUDE.md`.

### 2. "Invocar pela ferramenta Skill", nomeando o que não fazer

O passo 2 de "Ao terminar" troca *"carregar `/aicf:workflow-demanda`"* por uma instrução que nomeia
o caminho certo e o errado: invocar `/aicf:workflow-demanda` pela ferramenta Skill (*Skill tool*),
**não ler o `SKILL.md` com `cat` nem `Read`** — o arquivo inteiro cairia na tela de quem está
conhecendo o método. A skill não tem `disable-model-invocation`
(`grep -c disable-model-invocation skills/workflow-demanda/SKILL.md` → 0), então a ferramenta
Skill a carrega sem imprimir nada.

### 3. O default é a primeira opção

A seção "A mídia do registro" passa a dizer que **a opção default vai primeiro** na lista do
`AskUserQuestion`, porque a ferramenta lê a primeira como a sugerida. Default é **arquivos**,
sempre — com a exceção que o roteiro já tem: se `docs/agents/issue-tracker.md` aponta para o
GitHub, o default proposto é issues, e issues vai primeiro.

### 4. Mídia e padrões podem ir numa chamada só

O roteiro deixa de descrever duas chamadas e diz que as duas perguntas **podem ir juntas**, a
critério do agente: nenhuma resposta muda a outra, e o `gh auth login` que o roteiro põe entre as
duas funciona igual depois delas.

## Arquivos e interfaces

- `skills/setup/SKILL.md` — seções "A mídia do registro", "Ferramentas que o usuário já usa" e
  "Ao terminar" (passo 2).
- `skills/setup/templates/claude-md.md` — conferir que o placeholder da linha "Coleções"
  (`<nenhuma | os nomes que o setup detectou>`) continua certo; a expectativa é não mudar.
- `docs/referencias/verificacao-do-setup.md` — ganha as condições da passada nova (abaixo) e
  registra o resultado dela.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump de versão e entrada, juntos, no commit de
  código.

## Fora de escopo

- **Instalar coleção ou plugin de docs durante o setup.** O plugin só carrega na sessão seguinte, e
  instalar ferramenta de terceiro é decisão do usuário fora do método.
- **Detectar o cofre por `command -v bw` / `command -v op`.** Ter o binário na máquina não diz que é
  o cofre deste projeto; o global declarar diz. Levantado na entrevista e deixado de fora por isso.
- **Prescrever a ordem das opções da pergunta dos padrões de engenharia.** Ela não tem default no
  roteiro, e o desvio observado foi só na da mídia.

## Verificação

O `setup` tem `disable-model-invocation: true`: nenhum agente o roda, então esta demanda fecha com
a verificação de comportamento em aberto e nomeada em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), onde fica a condição de
aceite. Quem a encerra é o titular, numa passada **no ramo arquivo**, em diretório novo, depois de
`/plugin update` e sessão nova, com a versão conferida no cabeçalho do comando.

No transcript da passada (`~/.claude/projects/<diretório>/*.jsonl`, com o `jq` do doc de
verificação), numa máquina com Bitwarden e Context7 no global e Superpowers e Matt Pocock
habilitados, e escolhendo "No global" para os padrões:

1. **Nenhuma pergunta de ferramenta**: o agente declara numa linha o que achou (cofre, docs,
   coleções) e segue.
2. **A detecção de coleções usa `claude plugin list`**, não `ls` do cache.
3. **Nenhum `cat` ou `Read` do `SKILL.md` do `workflow-demanda`**: o transcript mostra uma chamada
   da ferramenta Skill com `aicf:workflow-demanda`.
4. **A pergunta da mídia sai com *arquivos* como primeira opção.**
5. As condições do ramo arquivo que o doc de verificação já lista seguem passando.

A regressão do filtro de escopo se confere fora do setup, em qualquer diretório sem plugin de
escopo `project`: o comando da seção 1 lista cada coleção habilitada no escopo `user` uma vez só
(`… | sort | uniq -d` vazio).

## Relatório de implementação (2026-09-23)

**Status:** concluído no roteiro; a **verificação de comportamento segue aberta**, porque o `setup` tem
`disable-model-invocation` e nenhum agente o roda. Quem a encerra é o titular, numa passada no ramo
arquivo da `0.28.0`, pelas quatro condições que ficaram em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), seção "O que está em aberto" —
encerra quando aquela seção registrar a passada. A demanda vai para `concluidas/` agora, como as
anteriores do `setup`: a condição de aceite mora no doc de verificação, não aqui.

**Arquivos alterados**

- `skills/setup/SKILL.md` — "A mídia do registro" ganha a regra do default em primeiro e libera
  mídia e padrões numa chamada; "Ferramentas que o usuário já usa" vira detecção por três fontes,
  declaração do que achou e uma pergunta só com o que faltou; "Ao terminar" passo 2 invoca pela
  ferramenta Skill e proíbe `cat`/`Read`.
- `docs/referencias/verificacao-do-setup.md` — condições da passada da `0.28.0`, com o `jq` que
  lista as chamadas de ferramenta do transcript.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.28.0`.

**Commits**

- `aea3752` docs(governanca): entrevista do setup que pergunta o que o ambiente já responde vira spec
- `42a385a` feat(setup): detecta as ferramentas antes de perguntar e não despeja o mapa na tela
- `2107920` fix(setup): uma fonte de detecção por pergunta, e o que faltou numa pergunta só

**Validação**

- `./scripts/check.sh` → `Tudo verde.` depois de cada commit.
- O comando de detecção de coleções, rodado em `/home/mh/dev/skills`, lista `superpowers@…` e
  `mattpocock-skills@…` uma vez cada (`… | sort | uniq -d` vazio); sem o filtro de escopo,
  `claude plugin list --json | jq -r '.[] | select(.enabled) | .id' | grep -c '^superpowers@'`
  devolve 5.
- O `jq` das condições novas, rodado no transcript da passada da `0.24.0`
  (`~/.claude/projects/-home-mh-dev-tmp-app1/*.jsonl`), mostra o `ls` do cache e o `cat` do
  `SKILL.md` do `workflow-demanda` — é o que ele flagra numa regressão.
- Revisão por subagente fresco sobre o `42a385a`, contra a spec: nenhum defeito bloqueante; quatro
  ambiguidades corrigidas no `2107920`.

**Escopo efetivo** — duas divergências da spec, as duas vindas da revisão:

- **A fonte de docs é o global ou `claude mcp list`, não `claude plugin list`.** A spec detectava o
  Context7 pelo id do plugin; quem o tem como servidor MCP configurado direto receberia a sugestão
  de instalar o que já tem. `claude mcp list` mostra os dois casos (o plugin aparece como
  `plugin:context7:context7`).
- **O que a detecção não achou vai numa pergunta só**, e o fallback sem CLI deixou de dizer "uma
  pergunta aberta por ferramenta" — era a regra que as passadas tinham derrubado, e o primeiro
  rascunho a reintroduziu.
- A sugestão de cofre ficou só com Bitwarden, como decidido na entrevista; o 1Password saiu da
  lista de opções, mas um global que o declare continua sendo detectado.

**Lições**

- **As versões `0.23.0`, `0.23.1` e `0.24.0` não têm tag** (`git tag | sort -V` pula de `v0.22.0`
  para `v0.25.0`), então `git show v0.24.0:…` falha. O número das 167 linhas se pinou no sha que
  subiu a versão (`git log --format=%h -1 -S'0.24.0' -- .claude-plugin/plugin.json` → `7fcb5dc`).
- **O cache de plugins não é a lista do que está instalado.** Os dois agentes das passadas leram
  `~/.claude/plugins/cache/` e acertaram por sorte: lá também fica plugin desabilitado, e o
  `claude plugin list` sem filtro de escopo conta plugin de outro projeto. A regra ficou no próprio
  roteiro do `setup`, que é o único lugar que detecta coleção.

**Promoção (passo 3):** nada novo além do doc de verificação, que já recebeu as condições. A lição
do cache vive no `SKILL.md` que a usa; a das tags ausentes está aqui e na mensagem ao titular.
