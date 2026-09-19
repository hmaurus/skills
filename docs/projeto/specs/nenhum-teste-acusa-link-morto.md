# Nenhum teste acusa link morto: o repositório ganha um script de verificação, e o GitHub o roda

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (três arquivos novos e duas linhas removidas, e todo o desenho ficou decidido na entrevista)

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
