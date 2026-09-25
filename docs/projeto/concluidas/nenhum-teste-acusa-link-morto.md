# Nenhum teste acusa link morto: o repositório ganha um script de verificação, e o GitHub o roda

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

Este repositório não tem verificação nenhuma. A seção `## Verificação` do `CLAUDE.md` está com o
texto do template — *"a preencher quando houver código"* — e os relatórios de fechamento registram
a consequência literalmente: *"Não há CI nem PR neste repositório; a validação foi local"* — a
ausência está anotada em **seis** specs concluídas
(`grep -rlE 'Não há CI|Sem CI' docs/projeto/specs/concluidas/ | wc -l`).

A falta tem um dano medido, e ele é sempre o mesmo: **link relativo que o `git mv` do passo 2 do
ritual quebra.**

- **2026-09-14**, implementando *o índice envelhece sem avisar*: mover um intent para `specs/`
  quebrou **cinco links de uma vez** em outras demandas. O achado virou a instrução de `grep` que
  hoje está no passo 2 do `/aicf:fechar-demanda`.
- **2026-09-18**, fechando *a entrada de quem chega*: **três links**, e o intent
  [governança em issues neste repo](../intents/governanca-em-issues-neste-repo.md) registra que
  *"eles só foram achados porque o passo 2 do ritual manda procurá-los"*.

O mesmo intent escreve a frase que é a justificativa desta demanda — **"nenhum teste acusa link de
markdown morto neste repositório"** — e mede a exposição: **29 links entre as demandas**
(`grep -rno '\](\.\./[^)]*\.md\|\]([a-z0-9-]*\.md)' docs/projeto/intents/*.md docs/projeto/intents/backlog/*.md docs/projeto/specs/concluidas/*.md | wc -l`)
mais **14 apontando de fora para dentro**
(`grep -rn 'docs/projeto/\(intents\|specs\)' --include='*.md' CLAUDE.md README.md README.en.md CHANGELOG.md docs/adr/ skills/ | wc -l`).

A rede que existe hoje é um `grep` dentro de um passo de um ritual, disparado pela memória do
agente, e que cobre só o arquivo que acabou de se mover. As duas vezes que ela funcionou foram as
duas vezes em que alguém lembrou.

**E há uma classe pior, hoje sem rede nenhuma: o plugin mal formado.** `plugin.json`,
`marketplace.json` e o frontmatter das seis skills definem o que o Claude Code carrega na máquina
de quem instala. Um erro ali não quebra nada aqui — quebra a instalação de quem usa, e só se
descobre pelo relato de terceiro.

## De onde veio esta demanda, e de onde não veio

A linha `- [ ] Repositório, branch de trabalho e CI mínimo` está em `## Próximas` do
`ROADMAP.md`, mas **não foi decidida**: ela é o item de exemplo do template, copiado junto quando
o roadmap nasceu. O `docs/projeto/ROADMAP.md` e o `skills/setup/templates/roadmap.md` nasceram no
mesmo commit, e os dois itens de `Próximas` daqui são, palavra por palavra, os dois do template
(`git show a6276e7 -- docs/projeto/ROADMAP.md skills/setup/templates/roadmap.md | grep 'CI mínimo'`
mostra a linha nascendo nos dois arquivos no mesmo diff). Repositório e branch já existiam desde
agosto.

Registrar isso importa por dois motivos. O primeiro é que a demanda real **não é "montar CI porque
o roadmap manda"** — é fechar a falta de rede contra link morto, que tem dano medido e é o que
decide o escopo abaixo. O segundo é que o template deste plugin entrega, a todo projeto novo, dois
itens de exemplo que se leem como itens decididos; aqui isso produziu uma linha fantasma que
sobreviveu quatro versões. Corrigir o template está **fora do escopo** desta demanda, mas o achado
fica escrito para o fechamento decidir se vira intent.

## Solução

Um script no repositório, rodado localmente antes de cada commit, e um workflow de GitHub Actions
que **chama esse mesmo script** depois do push. A lógica existe uma vez só: o YAML não repete
comando nenhum, ele executa o script.

Os três checks, todos com o resultado esperado conhecido hoje:

1. **Links relativos de markdown.** Todo link em sintaxe de markdown cujo destino não seja
   `http(s)` nem `mailto` tem que existir no disco. Hoje, depois das exclusões abaixo: **0
   quebrados**, em 49 links conferidos — número que cresce com o repositório, e que este arquivo
   já conta a si mesmo. O comando que o remede é o próprio `scripts/check_links.py`.
2. **`claude plugin validate --strict`**, nos dois alvos: `.` (que valida o
   `.claude-plugin/marketplace.json`) e `skills` (que valida o frontmatter das seis skills). Hoje
   os dois passam. O subcomando é offline — não fala com modelo, não pede login, não gasta token:
   verificado com `env -i PATH=$PATH HOME=<vazio> claude plugin validate . --strict`, que passou
   com exit 0. Nada aqui tem relação com a Claude Code GitHub Action, que roda o modelo em PR e
   precisa de credencial.
3. **A versão tem entrada no `CHANGELOG.md`.** O `version` do `.claude-plugin/plugin.json` precisa
   achar a própria linha `## <versão> — <data>` no changelog. Hoje `0.18.0` acha.

### As exclusões do check de links, e o ponto cego que elas criam

O verificador **ignora `skills/setup/templates/**`** e ignora qualquer link cujo caminho contenha
`<` ou `>`. O motivo é um só: nos templates, o link relativo fala do **projeto que vai receber a
cópia**, não deste repositório — `docs/projeto/PRD.md` e `intents/` não existem aqui e não deveriam
existir. Sem a exclusão o check nasceria vermelho com **7 falsos positivos** (6 nos templates, 1 no
placeholder `../intents/<nome>.md` de `skills/workflow-demanda/references/midia.md`), e um check
que nasce vermelho não é lido.

O preço, escrito para não ser esquecido: **um link realmente quebrado dentro de um template passa
batido**, e template é o arquivo que vai para todo projeto novo. A alternativa examinada — ignorar
só os links que apontam para caminhos do projeto destino — cobre o ponto cego ao custo de uma lista
de exceções que alguém precisa manter a cada template novo, e foi descartada pelo lema. Encerra
quando um link quebrado num template chegar ao projeto de um usuário.

### A versão pinada, e o que a atualiza

O workflow instala uma versão exata do Claude Code (`npm i -g @anthropic-ai/claude-code@2.1.278`,
que é a instalada hoje — `claude --version`). Localmente o script usa a versão que estiver na
máquina, que se atualiza sozinha.

As duas réguas têm papéis diferentes, e a divergência é intencional: a **local é sempre a mais
nova** e é ela que descobre cedo uma exigência nova do formato de plugin; a **pinada** só existe
para o dia em que ninguém rodou a local, e o pin impede que o CI fique vermelho por uma mudança
que não foi nossa. Por isso o script **imprime a versão que usou** — sem isso a divergência é
invisível.

Condição que encerra o número solto no YAML: **quando o check local reprovar com uma versão mais
nova que a pinada, sobe o pin no workflow.** Não é revisão periódica; é um evento observável.

### O que o CI é, e o que ele não é

Aqui se commita direto na `main`, sem PR e sem branch protection: **o workflow não bloqueia nada**,
ele avisa depois do fato. O valor está no script local, que é o que a regra global *"antes de
commitar, rodar no projeto inteiro"* passa a ter como comando; o Actions é a rede para quando a
execução local for esquecida — a mesma classe de falha que deixou passar os oito links.

## Arquivos e interfaces

| Arquivo | O que acontece |
|---|---|
| `scripts/check.sh` | **novo.** Orquestra os três checks, imprime a versão do `claude` usada, e sai com 1 se qualquer um falhar. Se o `claude` não estiver instalado, avisa e falha — não pula em silêncio |
| `scripts/check_links.py` | **novo.** O verificador de links, em `python3` (presente no runner do GitHub e nos dois ambientes do mantenedor). Recebe as exclusões como constante no topo do arquivo, não como argumento |
| `.github/workflows/ci.yml` | **novo.** `on: push` na `main` e `workflow_dispatch`; instala o Node do runner, `npm i -g @anthropic-ai/claude-code@2.1.278`, roda `./scripts/check.sh` |
| `CLAUDE.md`, seção `## Verificação` | o texto do template sai; entra o comando único (`./scripts/check.sh`) com o que é saída saudável, e a linha de conferir o run após o push |
| `docs/projeto/ROADMAP.md` | **já feito ao gravar esta spec:** a linha `- [ ] Repositório, branch de trabalho e CI mínimo` saiu — quem tem arquivo não tem linha |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | bump e entrada, pela sistemática de publicação |

## Fora de escopo

- **Gerar CI nos projetos que usam o aicf** (o `/aicf:setup` criando workflow no projeto do
  usuário). É demanda maior e de outra natureza: cada projeto tem stack, comandos e gerenciador
  próprios, e o aicf não tem como saber o que é saudável lá. O que esta demanda entrega é
  verificação **deste** repositório. Vale notar que `.github/` e `scripts/` **serão copiados** para
  `~/.claude/plugins/cache/` de quem instalar o plugin, porque o cache leva o repositório inteiro —
  mas nada os executa: o Claude Code lê o `plugin.json` e carrega skills, e um workflow só tem
  significado no GitHub, no repositório onde mora.
- **`grep -rn 'passo [0-9]'` como check.** Não tem resultado esperado: o número certo não é zero,
  então só poderia ser aviso — e aviso que nunca reprova não é lido. O `CLAUDE.md` já manda rodar
  esse `grep` no momento em que ele significa alguma coisa, que é ao renumerar um passo.
- **O grep de anonimização** (`grep -rn '<nome-do-projeto>'`). O padrão a procurar é o nome de um
  projeto privado; escrevê-lo num workflow público entrega exatamente o que a regra existe para
  esconder. Um secret do GitHub resolveria, e é complexidade maior que o risco de um check que
  rodou duas vezes na história do repositório.
- **Âncoras de markdown** (`arquivo.md#secao`). O check confere o arquivo, não a seção. Conferir
  âncora exige interpretar cabeçalho e *slug*, e nenhum dos oito links quebrados era de âncora.
- **Corrigir o template do roadmap**, que oferece itens de exemplo lidos como decididos. Achado
  desta entrevista, registrado acima; o fechamento decide se vira intent.
- **`claude plugin eval`.** Não há suíte de evals neste repositório, e criar uma é demanda própria
  — roda o modelo, custa token e tempo, e duas das seis skills (`setup` e `criar-prd`) têm
  `disable-model-invocation: true`, o que a suíte teria que contornar.

## Verificação

Ponta a ponta, na ordem:

1. **O script pega o defeito que originou a demanda.** Quebrar um link de propósito e ver o check
   reprovar, com o arquivo e o caminho na saída:
   ```
   sed -i 's|(../intents/governanca-em-issues-neste-repo.md)|(../intents/nao-existe.md)|' \
     docs/projeto/specs/concluidas/o-checklist-sai-do-metodo.md
   ./scripts/check.sh; echo "exit=$?"   # esperado: exit=1, apontando o arquivo e o link
   git checkout docs/projeto/specs/concluidas/o-checklist-sai-do-metodo.md
   ```
2. **O script passa no repositório limpo**, com os três checks verdes, a contagem de links e a
   versão do `claude` impressas: `./scripts/check.sh; echo "exit=$?"` → `exit=0`.
3. **O workflow roda no GitHub e fica verde** após o push:
   `gh run list --workflow=ci.yml --limit 1` mostra `completed success`, e
   `gh run view --log | grep -i 'claude code'` confirma a versão pinada que o runner instalou.
4. **A seção `## Verificação` do `CLAUDE.md` não tem mais o texto do template:**
   `grep -c 'A preencher quando houver código' CLAUDE.md` → `0`.

## Relatório de implementação (2026-09-19)

- **Status** — concluído. Os quatro passos da Verificação rodaram, inclusive o do GitHub: run
  [35456252117](https://github.com/hmaurus/skills/actions/runs/35456252117), `completed success`
  em 12s (`gh run list --workflow=ci.yml --limit 1`).

- **Arquivos alterados**
  - `scripts/check_links.py` — **novo**, 74 linhas (`wc -l < scripts/check_links.py`). Varre todo
    `*.md` do repositório, ignora `skills/setup/templates/**` e destino com `<`/`>`, e confere no
    disco o que sobra. Exclusões como constante no topo, como a spec pediu.
  - `scripts/check.sh` — **novo**, 54 linhas. Roda os três checks **sempre**, mesmo se um falhar —
    quem rodou quer ver tudo o que está vermelho de uma vez —, imprime a versão do `claude` e sai
    com 1 se qualquer um reprovar. Sem `claude` instalado, falha com a instrução de instalar.
  - `.github/workflows/ci.yml` — **novo**, 28 linhas. `push` na `main` e `workflow_dispatch`;
    `actions/checkout@v7`, `actions/setup-node@v7` com Node 24,
    `npm i -g @anthropic-ai/claude-code@2.1.278`, `./scripts/check.sh`.
  - `CLAUDE.md` — a seção `## Verificação` perdeu o texto do template
    (`grep -c 'A preencher quando houver código' CLAUDE.md` → `0`) e ganhou o comando único, a
    saída saudável, o ponto cego dos templates e a condição que sobe o pin. A seção `## Publicação`
    mudou uma regra (abaixo).
  - `.claude-plugin/plugin.json` — `0.18.0` → `0.19.0`; `CHANGELOG.md` — a entrada da versão.

- **Commits**
  - `38ba8da` — `docs(governanca): entrevista o CI e grava a spec da rede contra link morto`
  - `4b665a8` — `feat(ci): 0.19.0 — o repositório ganha verificação, e o GitHub a roda`

- **Validação**
  - **Checks do projeto: existem a partir desta demanda, e é o que ela entrega.**
    `./scripts/check.sh` → `exit=0`, com `53 links conferidos, 0 quebrados` neste commit
    (`python3 scripts/check_links.py`), os dois
    `✔ Validation passed` e `0.19.0 tem entrada no changelog`. É o primeiro fechamento em que a
    linha "não há CI" dos seis relatórios anteriores
    (`grep -rlE 'Não há CI|Sem CI' docs/projeto/specs/concluidas/ | wc -l` → `6`) deixa de valer.
  - Verificação 1 (o script pega o defeito que originou a demanda) — **o comando da spec estava
    errado e o erro se disfarçou de sucesso**; ver Lições. Com o link certo
    (`sed -i 's|(a-conferencia-do-indice-vira-script.md)|(nao-existe.md)|' docs/projeto/specs/concluidas/o-checklist-sai-do-metodo.md`),
    o check reprova com `exit=1` e imprime
    `docs/projeto/specs/concluidas/o-checklist-sai-do-metodo.md:25 -> nao-existe.md`.
  - Verificação 3 (o runner instalou a versão pinada) —
    `gh run view 35456252117 --log | grep -i 'claude code'` → `Claude Code: 2.1.278 (Claude Code)`,
    e o mesmo log traz os três checks verdes.
  - As exclusões valem os 7 falsos positivos que a spec previu: apagando as duas constantes do topo
    do `check_links.py`, o check vai a `59 links conferidos, 6 quebrados`, todos nos templates —
    o placeholder `../intents/<nome>.md` do `midia.md` passou a ser coberto pela máscara de
    código.
  - **O check pegou o defeito de verdade, no fechamento desta própria demanda.** O `git mv` do
    passo 2 do ritual moveu esta spec para `specs/concluidas/` e quebrou o link relativo da linha
    20 (`../intents/...` virou um nível curto demais). `./scripts/check.sh` reprovou com `exit=1`
    apontando arquivo e linha — pela primeira vez o link quebrado pelo ritual foi achado por um
    comando, e não pela memória de quem estava rodando o ritual. Corrigido para
    `../../intents/governanca-em-issues-neste-repo.md`; o check voltou ao verde.
  - **Revisão de código: subagente fresco, que não viu a implementação**, sobre o commit `4b665a8`.
    Dez achados, dos quais **cinco viraram correção** no commit de fechamento e quatro viraram
    registro. Um deles — a receita errada da Verificação 1 — a revisão achou de forma independente,
    depois de eu já ter tropeçado nele, o que é a confirmação de que a leitura de fora é mesmo "o
    check não pegou o defeito".
    - **Corrigidos.** (a) Link de exemplo dentro de bloco cercado ou de crase era conferido como
      link de verdade — num repositório que existe para ensinar a escrever markdown com link
      relativo, o próximo exemplo deixaria o check vermelho por um não-defeito. Conferível
      criando um `.md` com um link inexistente dentro de um bloco cercado: reprovava, e agora
      passa — enquanto o mesmo link fora do bloco continua reprovando. (b) Falha do
      `python3` virava a acusação "há link quebrado"; agora dependência ausente falha com o próprio
      nome. (c) `claude plugin validate .` valida os **dois** manifestos de `.claude-plugin/`, não
      só o `marketplace.json` — a mensagem culpava o arquivo errado, e a spec e o `CLAUDE.md`
      repetiam o erro. (d) Chamado por symlink, o script rodava no diretório errado; `readlink -f`
      resolve. (e) O check 3 aceitava qualquer linha do changelog, então **esquecer o bump inteiro
      passava verde**; agora exige a entrada do topo
      (`sed -i 's/0.19.0/0.18.0/' .claude-plugin/plugin.json` faz o check reprovar).
    - **Registrados, sem correção.** Link de referência (`[rótulo][id]`) não é conferido — forma
      que o repositório não usa (`grep -rnE '^\s*\[[^]]+\]:\s*\S' --include='*.md' .` → vazio);
      está no docstring do `check_links.py`. A máscara também não cobre crase dentro de crase — a
      primeira redação deste relatório caiu nisso, e o check a pegou; a saída foi reescrever a
      frase, não o script. Destino com parêntese, rótulo com colchete aninhado e
      `%20` são lidos errado pela regex — nenhum existe aqui, e cobri-los é o CommonMark inteiro,
      que o lema descarta. O CI não roda em `pull_request`: foi decisão da spec, e aqui se commita
      direto na `main`; encerra quando a primeira branch com PR aparecer. E `re.DOTALL` era
      decorativo — saiu, junto com o `pipefail` de um script sem pipe.
    - **Efeito colateral do (a):** a exclusão de destino com `<`/`>` deixou de existir. O
      placeholder `../intents/<nome>.md` do `midia.md` está dentro de crases, então a máscara de
      código já o cobre — um mecanismo no lugar de dois, que é o gatilho de revisão do lema. Os
      falsos positivos que a exclusão de templates evita passaram de 7 para 6.
- **Escopo efetivo** — uma mudança **fora do que a spec previu**, decidida com o usuário:
  **a entrada do `CHANGELOG.md` passa a subir junto com o bump da versão**, e não mais no commit de
  fechamento. O check 3, do jeito que a spec o definiu, colide com a regra de publicação: entre o
  commit de código e o de fechamento a versão não tem entrada, e é exatamente aí que
  `./scripts/check.sh` roda. Um check vermelho em todo commit de release é o mesmo defeito que a
  spec usou para justificar as exclusões — *check que nasce vermelho não é lido*. As alternativas
  examinadas foram afrouxar o check para "a versão não regride" (mecanismo a mais, e deixa de pegar
  o esquecimento de vez) e tirar o check 3 (a spec pediu os três). A regra do `CLAUDE.md` foi
  reescrita; o commit de fechamento ainda pode ajustar o texto da entrada.

- **Lições**
  - **O comando de repro escrito na entrevista estava errado, e passou como verde.** A Verificação
    1 da spec mandava `sed -i 's|(../intents/governanca-...)|...|'` num arquivo
    que não tem esse link — `sed` sem casamento sai com 0, o arquivo não mudou, e o check ficou
    verde. Lido de fora, isso se lê como "o check não pegou o defeito". Virou regra no `CLAUDE.md`.
    Segunda armadilha do mesmo tipo, já dentro do fechamento: o `sed -i` que **corrigiu** o link
    quebrado pelo `git mv` também reescreveu as duas citações dele neste relatório, que
    documentavam justamente o caminho errado. `sed` global não distingue o texto do seu uso.
  - **Link de markdown pode ter o rótulo quebrado em duas linhas, e quatro deles existem aqui**
    (`grep -rPzo --include='*.md' '\[[^\]]*\n[^\]]*\]\([^)]+\)' docs | tr '\0' '\n' | grep -c ']('`
    → `4`). A primeira versão do verificador varria linha a linha e contou 45 links, não 49 — o
    número da spec é que denunciou a falha. Está no docstring do `check_links.py`.
  - **`claude plugin validate` roda no runner sem credencial nenhuma**, como a entrevista previu:
    12s de run, sem login e sem token.

- **O que este fechamento abriu**
  - **Regra nova no `CLAUDE.md`** — *"Verificação que quebra algo de propósito confirma que
    quebrou"*, vizinha da regra de afirmação verificável. Nasceu do erro da Verificação 1 acima.
  - **Regra alterada no `CLAUDE.md`**, seção `## Publicação` — a entrada do `CHANGELOG.md` sobe
    junto com o bump.
  - **Intent novo no backlog** —
    [o template do roadmap entrega item de exemplo](../specs/o-template-do-roadmap-oferece-item-de-exemplo.md),
    que é o achado que esta spec registrou e deixou fora de escopo. A linha
    `- [ ] PRD.md preenchido` do `ROADMAP.md` **fica**: veio do mesmo template, mas é pendência
    real (`diff <(sed 's/aicf/<NOME>/g' docs/projeto/PRD.md) skills/setup/templates/prd.md` mostra
    só as seções preenchidas, e as legendas `>` continuam no lugar do conteúdo).
  - Nenhum ADR: as duas decisões desta demanda — as exclusões do check e a régua local × pinada —
    já estão escritas na Solução acima com a condição que as encerra, e nenhuma é difícil de
    reverter.
