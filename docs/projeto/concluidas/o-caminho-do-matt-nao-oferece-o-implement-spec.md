# O caminho do Matt não oferece o implement-spec

Processo — entrevista: criar-spec · implementação: aicf-plan

## Problema

O `/aicf:implementar-spec` só conhece um jeito de trabalhar os tickets do Matt: `/implement`
ticket a ticket, com `/clear` entre eles. As skills do Matt (v1.3.1) têm também o
**`/implement-spec`**. Ele lê os tickets como grafo pelas linhas de bloqueio, roda subagentes
implementadores em background, cada um na sua worktree e pelo `/tdd`, junta tudo numa branch de
integração com um subagente de merge, faz um `/code-review` final e apaga as worktrees. Num
projeto real, com os 14 tickets de uma spec já criados, o aicf entregou só o comando do
`/implement`, e o titular descobriu o `/implement-spec` pelo `/ask-matt`.

O critério que o agente usa para sugerir o caminho não distingue as duas formas de executar por
subagentes: a serial, `subagent-driven-development` (Superpowers), e a paralela,
`/implement-spec` (Matt). Hoje o Superpowers é sugerido "quando são muitos passos numa sessão,
executados por subagente e com TDD", e isso vale para os dois. O parágrafo está repetido em
`skills/criar-spec/SKILL.md` e `skills/implementar-spec/SKILL.md`
(`grep -rl 'quando cabe numa sessão' skills/` → os dois arquivos).

Fora das skills, três textos dizem coisas sobre o Matt que deixaram de valer:

- a linha "Coleções de skills de workflow instaladas" cita como skills de caminho só
  `grill-with-docs`, `to-spec`, `to-tickets` e `implement`;
- o `README.md` diz que os tickets são "executados um a um" e que o `implement` não fecha o
  ticket, sem mencionar o `implement-spec`, que fecha;
- o relatório de governança dá o `implement-spec` como "fora do plugin", o que valia na v1.2.3.

## Solução

O Matt continua sendo **um caminho só**, com duas formas de executar. O caminho se escolhe como
hoje, e a forma se escolhe **depois do `/to-tickets`**, com o grafo à vista. Antes dos tickets o
tamanho do grafo não se conhece.

### Os critérios moram em dois arquivos de apoio

Os dois ficam em `skills/implementar-spec/` e são lidos por ordem dada no passo que os aplica, do
mesmo jeito que as skills já fazem com `midia/`. Cada um tem os seus consumidores, para que
nenhuma skill carregue o que não vai aplicar.

**`caminhos.md`**, o critério dos quatro caminhos. O `criar-spec` (ao gravar a sugestão, pelo link
`../implementar-spec/caminhos.md`) e o `implementar-spec` (ao decidir) mandam lê-lo. O parágrafo
repetido sai das duas skills. Conteúdo decidido:

- **`aicf-direto`**: cabe numa sessão e o diff se descreve numa frase, sem decisão de abordagem.
- **`aicf-plan`**: cabe numa sessão, mas tem abordagem a decidir ou vários arquivos. O plano é
  aprovado antes de mexer no disco.
- **`subagent-driven-development`** (Superpowers): muitos passos acoplados, em sequência, numa
  sessão, quando acertar cada passo vale mais que o tempo. Cada tarefa é revisada antes da
  próxima. É serial, um implementador por vez: **não se sugere para ganhar velocidade**.
- **`to-tickets`** (Matt): fatias verticais com dependência entre elas, que podem atravessar
  sessões. A forma de executar se decide depois dos tickets, no `implementar-spec`.

**`matt.md`**, o que só o `implementar-spec` usa depois do `/to-tickets`: o critério da forma e o
procedimento dos itens 2 a 7 da seção seguinte. Abre com o título e uma frase de contrato: *"Lido
pelo `implementar-spec`, no passo 3, ao voltar do `/to-tickets` ou retomar uma spec com tickets,
antes de escolher a forma."* O `fechar-demanda` não o lê: as regras de fechamento ficam no
`SKILL.md` dele e em `midia/issues.md`.

No `matt.md` vai a regra e o comando; o que é prova fica nesta spec e no `CHANGELOG.md`: a citação
do resumo da v1.3 com o `curl`, o caso `blockedSince` × `blockedOn` e a citação da doc da CLI do
Antigravity. Continuam em runtime, sem a prova: o critério numérico, a regra de fixar nomes ou
bloquear, o procedimento da dependência nativa do GitHub e o aviso do Antigravity com a condição
que o encerra.

O critério da forma:

- **`/implement` por ticket**: é o padrão. O titular conduz cada ticket e lê o trabalho de cada um
  ao terminar.
- **`/implement-spec`**: quando a spec se divide em **4 ou mais tickets com fronteira paralela de
  verdade**, isto é, com pelo menos 2 tickets prontos ao mesmo tempo em algum ponto do grafo. É o
  critério do [resumo da v1.3](https://developer.tenten.co/mattpocock-skills-v1-3-pr-implement-spec-retro)
  (*"four or more tickets with independent parallel frontiers"*:
  `curl -s <url> | grep -o 'four or more tickets[^<]*'`). A doc do Matt diz só que, sem grafo de
  verdade, se usa o `/implement`. Pesam contra, e viram aviso: arquivo compartilhado entre tickets
  da mesma fronteira; migration em mais de um ticket; verificação de ticket que depende de estado
  não versionado. Fronteira é o conjunto de tickets sem bloqueio pendente. Custo: o titular revisa
  a branch de integração inteira no fim, e precisa de cota de uso para vários subagentes ao mesmo
  tempo.

### O passo 3 do `implementar-spec`, no caminho do Matt

No `SKILL.md` ficam a tabela (item 1), o ponteiro para o `matt.md` (item 2) e a nota de
workspace. O resto do item 2 e os itens 3 a 7 vão para o `matt.md`, nessa ordem. O ponteiro é
instrução do passo 3, fora de um ramo só de quem acabou de criar tickets, para que a retomada
também passe por ele.

1. **Tabela:** a linha do Matt passa a dizer, em "Como", `/to-tickets` e depois `/implement` por
   ticket ou `/implement-spec` para o grafo inteiro. Em "Integração": no `implement`,
   `/code-review` e commit na branch atual; no `implement-spec`, branch de integração,
   `/code-review` final e tickets resolvidos no tracker, ou, quando o tracker fecha trabalho por
   PR, um PR aberto em rascunho e marcado como pronto no fim (passos 3 e 8 do `implement-spec`).
2. **Os comandos** continuam: alinhar o tracker (nos dois modos, pela receita da mídia) e entregar o `/to-tickets`.
   Acrescenta-se o que vem depois, em dois pontos de entrada:
   - **de volta do `/to-tickets`, na mesma sessão**;
   - **retomada**: `/aicf:implementar-spec <spec>` numa sessão nova, quando a spec já tem tickets
     (modo arquivo: arquivos em `.scratch/<feature>/issues/` com a linha `**Spec:**` apontando para
     ela; modo issue: issues com `## Parent` apontando a issue da spec). Aqui o agente não entrega
     o `/to-tickets` de novo: vai direto à medição. É a exceção à regra de que a skill para ao
     entregar o caminho de uma coleção, e o `criar-spec` a anuncia ao gravar a sugestão
     `to-tickets`.

   No `SKILL.md`, isso é o ponteiro, de cerca de três linhas: de volta do `/to-tickets`, ou numa
   sessão nova em que a spec já tem tickets (sem entregar o `/to-tickets` de novo), ler
   `matt.md` e seguir. O reconhecimento dos tickets pela linha `**Spec:**` ou por
   `## Parent`, a exceção à parada da skill e o que segue ficam no `matt.md`.

   Nos dois casos o agente lê os tickets e mede quatro coisas: a largura da fronteira, se dois
   tickets da mesma fronteira tocam o mesmo arquivo, quantos geram migration, e se a verificação de
   algum depende de `.env`, banco ou pasta no gitignore. Com essas medidas, recomenda a forma numa
   pergunta com opções.
3. **Escolhido o `/implement-spec`, o agente propõe a edição dos tickets e aplica com o aceite do
   usuário, mostrando o diff.** O que é para os subagentes vai no ticket, que é o que eles leem:
   - dois tickets da mesma fronteira que tocam o mesmo arquivo: bloqueio entre eles, ou os nomes
     fixados nos dois (o caso `blockedSince` × `blockedOn` da doc);
   - migration em mais de um ticket da mesma fronteira: bloqueio, para que elas não rodem em
     paralelo contra o mesmo banco;
   - ticket cuja verificação depende de estado não versionado: a linha
     `**Verificação no checkout principal:** <comando> — na worktree ela não roda; reportar isso em vez de verde.`
     Na worktree, o teste que lê arquivo no gitignore é pulado em silêncio. A linha diz ao
     implementador o que reportar; o que o orquestrador faz com ela está no tracker (item 4).

   **Bloqueio, por mídia:** no modo arquivo, a linha `Blocked by:` do ticket; no modo issue, a
   dependência nativa do GitHub, pelo procedimento do tracker do Matt
   (`issue-tracker-github.md`, linha 42: `gh api --method POST .../dependencies/blocked_by` com o
   id de banco do bloqueador), e o corpo acompanha. A linha `Blocked by: #<n>` no corpo só
   substitui a dependência onde a plataforma não a oferece. Depois de acrescentar bloqueios, a
   largura da fronteira se mede de novo antes da decisão final.
4. **O que é para o orquestrador, e vale para toda execução, mora no tracker do Matt**, o
   `docs/agents/issue-tracker.md`. A doc do Matt manda *"tell the orchestrator"* em dois desses
   casos (linhas 60 e 68 de `docs/engineering/implement-spec.md`), e o tracker é o lugar onde
   dizer isso sobrevive ao `/clear` e chega também a quem digita o `/implement-spec` sem passar
   pelo aicf — a mesma razão do
   [ADR 0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md).

   **Nada no Matt manda o orquestrador abrir o tracker.** O `implement-spec` só supõe que ele foi
   fornecido (*"should have been provided to you"*, linha 9 do `SKILL.md` dele), e o setup do Matt
   grava no `CLAUDE.md` uma linha `See docs/agents/issue-tracker.md.` (linha 91 do
   `setup-matt-pocock-skills/SKILL.md`): o ponteiro entra no contexto, o arquivo não. O que leva o
   agente a abri-lo é precisar saber como o tracker fecha trabalho (passos 3 e 8). A mesma cadeia
   já funcionou para o `to-tickets`, que diz a mesma frase (linha 11): num projeto privado, os
   tickets saíram com a linha `**Spec:**`, que só existe no tracker. Por isso a leitura vem por dois
   caminhos:
   - **o comando entregue pelo aicf manda ler** (abaixo) — leitura garantida;
   - **sem o sufixo**, esquecido ou com o Matt chamado direto, sobra a cadeia indireta, e a
     operação de alinhar confere o elo dela que o aicf alcança: a linha do `CLAUDE.md`.

   A operação "Alinhar o tracker do Matt" acrescenta ao fim do arquivo a seção
   `## Quando o /implement-spec roda`, com:
   - **nos dois modos:** calcular a fronteira pelo que já entrou na branch de integração, não pelo
     estado do ticket no tracker, porque os tickets só se resolvem no fim (passo 8 do
     `implement-spec`). A doc registra o problema no GitHub; no markdown local o `Status: resolved`
     também só vem no passo 8;
   - **nos dois modos:** ticket com a linha `**Verificação no checkout principal:**` tem o comando
     rodado no checkout principal, com a branch de integração em checkout, **depois do merge
     daquele ticket**, um por vez, e só então se liberam os que ele bloqueia;
   - **só no markdown local:** passar cada ticket aos subagentes pelo **caminho absoluto no checkout
     principal**. O `/to-tickets` não faz commit dos tickets, e a worktree só tem o que tem commit;
     com a `.scratch/` no gitignore, nem um commit os levaria.

   No `matt.md`, este item é conferir o alinhamento antes da pergunta da forma — na retomada, o
   tracker pode ser de antes da `0.44.0` — e propor o que falta, pela receita da mídia.

   O comando é o nativo com um sufixo que **aponta a seção, sem copiar as regras**:

   ```
   /implement-spec <spec> — antes de começar, ler docs/agents/issue-tracker.md, seção "Quando o /implement-spec roda"
   ```

   O `<spec>` é o mesmo do `/to-tickets` — o caminho no modo arquivo, `#<n>` no modo issue —, como
   a doc do Matt manda: *"with a pointer to the spec"* (linha 40). As regras ficam num lugar só, a
   seção do tracker; copiá-las no argumento daria ao `matt.md` um segundo texto delas, que teria de
   ficar igual ao do tracker.
5. **O que é do titular, o agente diz na conversa:** se começar uma segunda revisão ampla depois
   da correção, interromper e pedir só checagens focadas nos achados corrigidos; revisar a branch
   de integração inteira no fim; a verificação ponta a ponta da spec roda no checkout principal,
   na branch de integração.
6. **No Antigravity**, uma linha a mais: os subagentes rodam em background (a
   [doc da CLI](https://antigravity.google/docs/cli/features) os descreve como *"independent,
   concurrent agent sessions"*), mas a worktree por subagente não está documentada nem foi
   testada. O aviso sai quando uma passada no `agy` confirmar ou derrubar isso.
7. Então o agente entrega `/clear` e o comando do item 4, com o sufixo, e espera.

**Workspace:** com o `/implement-spec`, quem cria a branch de integração e as worktrees é o
método, e o aicf não decide workspace além de dizer isso numa linha. A regra de hoje ("worktree
nunca quando a verificação depende de estado não versionado") continua valendo para a escolha do
próprio aicf. No `implement-spec`, ela vira a marcação do item 3 e a regra do tracker do item 4. A nota
vai no `SKILL.md`, logo depois da regra de workspace, como exceção explícita a ela: *"Com
`/implement-spec`, não escolher workspace: branch e worktrees são do método; a restrição acima
vale para a escolha do aicf, e o estado não versionado segue o tratamento de `matt.md`."* Só dizer
quem cria a worktree não basta: o agente leria o "nunca" como veto à forma paralela.

### O fechamento depois do `implement-spec`

O `/aicf:fechar-demanda` roda uma vez, quando o `/implement-spec` termina, sobre a branch de
integração. A regra é a que já vale para branch própria (`implementar-spec`, "Verificar e
fechar"; `fechar-demanda`, linhas 16–20): a integração termina quando **o destino do código está
decidido**, não só com o merge. Entram três coisas:

- **o destino é pergunta com opções:** merge na branch de origem, PR, ou deixar a branch. Se o
  `implement-spec` já abriu o PR, as opções são fazer o merge dele agora ou deixá-lo aberto para
  revisão. Qualquer escolha fecha a demanda; o commit de fechamento vai onde o código ficou, e no
  PR aberto ele entra no PR;
- **a issue da spec fechada pelo merge:** o PR do `implement-spec` fecha a spec e os tickets
  (passo 3 dele). Se o merge veio antes do ritual, a issue `aicf:spec` já está fechada, com o label.
  O fechamento a adota: comenta o relatório e tira o label, sem reabrir. Isso entra na operação
  "Concluir" de `skills/midia/issues.md`, onde hoje ela supõe a issue aberta;
- **o `/code-review` final do `implement-spec`** cobre a exigência de revisão, como o
  `subagent-driven-development` já cobre. Não se pede outra.

### Fora das skills

- **`skills/midia/arquivo.md`**, operação "Alinhar o tracker do Matt": onde diz "para que o
  `/implement` numa sessão limpa", passa a dizer `/implement` ou `/implement-spec`. A operação
  ganha a seção do item 4 (os três itens), acrescentada ao fim do arquivo do Matt e não troca de
  frase, e mais duas conferências:
  `grep -c 'Quando o /implement-spec roda' docs/agents/issue-tracker.md` → ≥ 1, e o ponteiro
  que o setup do Matt grava na raiz,
  `cat CLAUDE.md AGENTS.md 2>/dev/null | grep -c 'docs/agents/issue-tracker.md'` → ≥ 1. Faltando
  o ponteiro, propor repor a seção `## Agent skills` com a linha do tracker, no arquivo que já
  existe (o setup do Matt edita o `CLAUDE.md`, ou o `AGENTS.md` sem `CLAUDE.md`: linhas 76–80 do
  `setup-matt-pocock-skills/SKILL.md`).
- **`skills/midia/issues.md`**: a operação "Alinhar o tracker do Matt", nova, só com a seção do
  item 4 (os dois itens dos dois modos), as mesmas duas conferências e aceite com diff. Até aqui o
  modo issue não escrevia nada no tracker do Matt.
- **`skills/implementar-spec/SKILL.md`** e **`skills/criar-spec/SKILL.md`**: as chamadas da
  operação deixam de ser só do modo arquivo e passam a seguir a receita da mídia.
- **`docs/adr/0010-o-aicf-escreve-as-regras-do-implement-spec-no-tracker-do-matt.md`**: novo, e
  amplia o [0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md), que dizia "no
  modo issue nada se escreve" e "só três frases". O 0008 continua valendo para as três frases. A
  decisão: o aicf acrescenta, nos dois modos, a seção do `implement-spec`; o motivo é o do item 4.
  A alternativa recusada, o sufixo no argumento do comando, vai em Fora de escopo.
- **`skills/setup/templates/claude-md.md`** e **`.claude/CLAUDE.md`**: a lista de skills de caminho
  do Matt ganha o `implement-spec`.
- **`README.md`** e **`README.en.md`**, na lista "Na fase de implementação": os tickets são
  executados um a um pelo `implement`, ou em paralelo pelo `implement-spec`, cada um numa
  worktree e juntos numa branch de integração. Em "Registro depois da execução": o `implement`
  termina no commit sem fechar o ticket; o `implement-spec` resolve os tickets ao terminar, ou
  pelo merge do PR que abre; nenhum dos dois marca critério de aceite. O resto do parágrafo fica.
- **`docs/referencias/governanca-nos-frameworks-vizinhos.md`**, na tabela (linha 90) e na nota da
  afirmação 4 (linha 215): uma frase datada, mantendo o pino `c55ee46`. "Em 2026-10-23: o
  `implement-spec` saiu de `in-progress/` e está publicado desde a v1.3.0; conferido no cache
  v1.3.1, ele resolve os tickets no fim (passo 8)", com os comandos que conferem a promoção
  (`sed -n '9,16p' $M/CHANGELOG.md`, entrada `1.3.0`) e a regra
  (`grep -n 'resolve each ticket' $M/skills/engineering/implement-spec/SKILL.md` → linha 38).
- **`skills/midia/issues.md`**, operação "Concluir": quando a issue já foi fechada pelo merge de um
  PR, comentar o relatório e tirar o label, sem reabrir.
- **[O setup não serve a projeto já rodando](../intents/o-setup-nao-serve-a-projeto-ja-rodando.md)**,
  em "O que já se sabe": um item com este segundo caso concreto, a linha de coleções que ganhou o
  `implement-spec`.
- **`.claude-plugin/plugin.json`** e **`CHANGELOG.md`**: `0.44.0`, porque o plugin passa a oferecer
  um caminho novo. As notas da release pedem que quem já tem projeto montado acrescente o
  `implement-spec` à linha de coleções do `CLAUDE.md` à mão, até o setup de projeto já rodando
  existir.

## Arquivos e interfaces

- `skills/implementar-spec/caminhos.md`: novo, só com o critério dos quatro caminhos. Lido pelo
  `criar-spec` e pelo `implementar-spec`.
- `skills/implementar-spec/matt.md`: novo, com o critério da forma e o procedimento depois do
  `/to-tickets` (itens 2 a 7). Lido só pelo `implementar-spec`, no passo 3, de volta do
  `/to-tickets` ou na retomada.
- `skills/implementar-spec/SKILL.md`: passo 3, com a tabela, o critério substituído pela ordem de
  ler `caminhos.md`, o ponteiro para o `matt.md` e a exceção de workspace. O procedimento não
  entra nele.
- `skills/criar-spec/SKILL.md`: "Ao terminar", passo 2, com o critério substituído pela ordem de
  ler `caminhos.md` (link `../implementar-spec/caminhos.md`), e o
  anúncio da retomada por `/aicf:implementar-spec <spec>` quando a sugestão é `to-tickets`.
- `skills/fechar-demanda/SKILL.md`: a integração do `implement-spec` e o `/code-review` que já
  cobre a revisão.
- `skills/midia/issues.md`: a issue da spec já fechada pelo merge, e a operação "Alinhar o tracker
  do Matt", nova.
- `skills/midia/arquivo.md`: a seção do `implement-spec` na operação de alinhar.
- `docs/adr/0010-o-aicf-escreve-as-regras-do-implement-spec-no-tracker-do-matt.md`: novo.
- `skills/setup/templates/claude-md.md`, `.claude/CLAUDE.md`,
  `README.md`, `README.en.md`, `docs/referencias/governanca-nos-frameworks-vizinhos.md`,
  `docs/projeto/intents/o-setup-nao-serve-a-projeto-ja-rodando.md`, `.claude-plugin/plugin.json`,
  `CHANGELOG.md`.

## Testes

Nenhum código muda, só texto de skills e documentação. O ponto de teste é o
`./scripts/check.sh`, que já existe e confere os três links novos (dos dois consumidores para o
`caminhos.md` e do `implementar-spec` para o `matt.md`), o tamanho dos `SKILL.md`, o par versão ×
`CHANGELOG.md` e os manifestos. Ele confere que os destinos existem, não que a ordem de leitura é
obedecida nem que o procedimento chegou inteiro ao `matt.md`: isso fica para o item 6 da
Verificação.

## Fora de escopo

- **Duas linhas do Matt na tabela, escolhidas antes dos tickets.** Seria escolher sem ver o grafo.
- **As regras copiadas no sufixo do argumento.** Seriam dois textos da mesma regra, no `matt.md` e
  no tracker, que teriam de ficar iguais. E, sozinho, o sufixo só chega a quem copia o comando que
  o aicf entregou — o erro que o
  [ADR 0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md) desfez: até a
  `0.37.0` o `/implement` levava a spec junto no argumento, e quem conduzia o Matt direto o
  digitava sem ela. O sufixo fica, mas só aponta a seção.
- **O `criar-spec` sugerir a forma.** A spec não diz a largura da fronteira; a sugestão continua
  `to-tickets`.
- **Testar a worktree por subagente no `agy` agora.** Fica como aviso, que sai depois de uma
  passada.
- **Novo pino do Matt no relatório de governança.** Exigiria conferir de novo todas as afirmações;
  a frase datada corrige a única que mudou.
- **O setup atualizar a linha em projetos que já existem.** É a demanda
  [o setup não serve a projeto já rodando](../intents/o-setup-nao-serve-a-projeto-ja-rodando.md);
  aqui entra só como caso concreto lá, e nas notas da release.
- **Check que compare duas cópias do critério.** Com um arquivo só, não existe cópia para
  comparar.
- **Um arquivo de apoio só, com seções.** Economiza um arquivo, mas o `criar-spec` e toda decisão
  de caminho carregariam o procedimento do Matt. Mandar ler só uma seção exigiria manter a
  seleção do trecho, e o `check.sh` não confere âncoras.
- **Deixar o procedimento no `SKILL.md`.** Seriam cerca de 30 linhas a mais carregadas em toda
  invocação, inclusive no caminho aicf direto.
- **Paralelismo no Superpowers.** O mantenedor recusou
  ([obra/superpowers#945](https://github.com/obra/superpowers/issues/945); PRs
  [#1213](https://github.com/obra/superpowers/pull/1213) e
  [#1534](https://github.com/obra/superpowers/pull/1534) fechados em 2026-09-27, "by design").
- **As notas de sessão** em `docs/notas-de-sessao/`, que citam o `/implement`: são registro do que
  valia na data.

## Verificação

1. `./scripts/check.sh` termina em `Tudo verde.`.
2. O critério sai das skills e cada arquivo de apoio tem os seus consumidores. O trecho buscado é
   do parágrafo antigo, não a abertura "O critério para sugerir", que o ponteiro novo reaproveita:
   - `grep -lF 'subagente e com TDD' skills/*/SKILL.md` → nada (hoje, os dois `SKILL.md`);
   - `grep -l 'caminhos.md' skills/criar-spec/SKILL.md skills/implementar-spec/SKILL.md | wc -l` → 2
     (hoje, 0);
   - `grep -lF 'matt.md' skills/*/SKILL.md` → só `skills/implementar-spec/SKILL.md` (hoje, nada).

   Presença de texto não prova o fluxo; quem o prova é o item 6.
3. O `implement-spec` aparece onde o aicf lista o Matt:
   `grep -c 'implement-spec' skills/implementar-spec/SKILL.md skills/implementar-spec/matt.md skills/fechar-demanda/SKILL.md skills/midia/arquivo.md skills/setup/templates/claude-md.md .claude/CLAUDE.md README.md README.en.md`
   → ≥ 1 em cada um (hoje, 0 nos que já existem, e erro para o `matt.md`, que ainda não existe).
   O `caminhos.md` fica fora da lista: ele só conhece o `to-tickets`.
4. A regra mora no tracker, nas duas mídias, e o sufixo só aponta para ela:
   `grep -c 'Quando o /implement-spec roda' skills/midia/arquivo.md skills/midia/issues.md` → ≥ 1
   em cada (hoje, 0);
   `grep -c 'seção "Quando o /implement-spec roda"' skills/implementar-spec/matt.md` → 1 (hoje,
   erro: o arquivo não existe);
   e a regra não é copiada nele: `grep -c 'calcular a fronteira' skills/implementar-spec/matt.md`
   → 0, enquanto `grep -c 'calcular a fronteira' skills/midia/arquivo.md skills/midia/issues.md` →
   ≥ 1 em cada (hoje, 0);
   `grep -c "AGENTS.md 2>/dev/null | grep -c 'docs/agents/issue-tracker.md'" skills/midia/arquivo.md skills/midia/issues.md`
   → 1 em cada (hoje, 0);
   `test -f docs/adr/0010-o-aicf-escreve-as-regras-do-implement-spec-no-tracker-do-matt.md`.
5. As frases antigas do README saem:
   `grep -c 'executados um a um' README.md` e `grep -c 'executed one at a time' README.en.md` → 0
   (hoje, 1 cada); a frase datada entra: `grep -c '2026-10-23' docs/referencias/governanca-nos-frameworks-vizinhos.md` → ≥ 1 (hoje, 0).
6. **Comportamento, em aberto até o uso real**, numa sessão aberta depois de atualizar o plugin
   para a `0.44.0`. Quem encerra é o titular, no uso; o relatório diz isso em vez de prometer um
   teste agora. As duas entradas (de volta do `/to-tickets` e retomada) se observam nos dois modos,
   arquivo e issue. Cada cenário passa quando:
   - **caminho aicf direto:** o agente não abre o `matt.md`. É o ganho de carregamento, que nenhum
     grep mede;
   - **grafo estreito**, ou largo com o titular escolhendo a forma serial: o agente oferece e
     entrega `/implement <ticket>`;
   - **grafo largo, forma paralela escolhida:** o agente confere o tracker alinhado, propõe a
     edição dos tickets quando algum sinal aparece e entrega `/clear` + o comando com o sufixo
     que aponta a seção do tracker;
   - **execução do `/implement-spec`, com o sufixo:** o orquestrador abre o `issue-tracker.md` e
     segue a seção — libera o ticket bloqueado assim que o bloqueador entra na branch de
     integração, roda no checkout principal a verificação marcada e, no modo arquivo, passa os
     tickets por caminho absoluto;
   - **execução sem o sufixo** (`/implement-spec <spec>` digitado direto): observar se o
     orquestrador abre o `issue-tracker.md` por conta própria. Abrindo, segue a seção como acima;
     não abrindo, a cadeia indireta não basta, e isso se registra como achado, sem reprovar a
     demanda: o comando que o aicf entrega leva o sufixo;
   - **retomada:** `/aicf:implementar-spec <spec>` numa sessão nova, com os tickets já criados,
     vai à medição sem pedir `/to-tickets` de novo e sem duplicar tickets;
   - **fechamento:** com o PR deixado aberto, o commit de fechamento entra no PR; com a issue da
     spec já fechada pelo merge, o relatório vira comentário e o label `aicf:spec` sai.

## Contexto levantado

Os fatos de que as decisões acima partem, com o comando que confere cada um.

### O `implement-spec` por dentro

Conferido na cópia instalada da v1.3.1, `M=~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1`.
O comando de histórico usa um clone do `mattpocock/skills` em `$R/skills`, montado pelo bloco de
clone do [relatório de governança](../../referencias/governanca-nos-frameworks-vizinhos.md). O
`5beb35b` citado na intent não é a tag: `git -C $R/skills describe --tags 5beb35b` →
`v1.3.1-47-g5beb35b`, e a doc dele já difere da do cache; os comandos abaixo valem para o cache.

- **Entrou no plugin na v1.3.0**, saindo de `skills/in-progress/`. Conferir num clone:
  `git -C $R/skills log --format='%h %cs %s' --diff-filter=A -- skills/engineering/implement-spec/SKILL.md`
  → `24f41cc 2026-09-24 Graduate implement-spec to engineering`.
- **Exige um harness com subagente em background e worktree por subagente**; sem isso, *"a slower
  `implement`"*: `grep -n 'gives each one a git worktree' $M/docs/engineering/implement-spec.md` →
  linha 22. Sem grafo de verdade, a doc manda usar o `implement`, e manda limpar a sessão antes:
  `grep -n 'clear the context and type' $M/docs/engineering/implement-spec.md` → linha 40.
- **Problemas que a própria doc registra**, na seção "Common questions" de
  `$M/docs/engineering/implement-spec.md`:
  - a worktree não evita a colisão, só a adia para o merge (`blockedSince` × `blockedOn`);
  - o ciclo de revisão e correção pode não parar (~4 h numa feature de 5 tickets);
  - no GitHub, um ticket bloqueado só começa quando o bloqueador fecha, e o bloqueador só fecha no
    fim, e a doc manda dizer ao orquestrador que calcule a fronteira pela branch de integração:
    `grep -n 'Tell the orchestrator to track' $M/docs/engineering/implement-spec.md` → linha 60;
  - teste que lê arquivo no gitignore é pulado na worktree:
    `grep -n 'run it in the main checkout' $M/docs/engineering/implement-spec.md` → linha 68;
  - o pareamento de seams do `/implement` não existe; *"name the seams in the spec or the tickets"*
    (linha 52).
- **Resolve os tickets no fim, ou marca o PR em rascunho como pronto:**
  `grep -n 'resolve each ticket' $M/skills/engineering/implement-spec/SKILL.md` → linha 38.
- **`/implement` em paralelo**, o Matt recomenda com uma worktree por sessão (`claude --worktree`),
  na [mattpocock/skills#429](https://github.com/mattpocock/skills/issues/429).

### O Superpowers é serial, por decisão

Pinado em `obra/superpowers` `2ce8aa1` (v7.0.1).

- **Um implementador por vez, uma worktree para o plano inteiro:**
  `grep -n 'in parallel (conflicts)' $R/superpowers/skills/subagent-driven-development/SKILL.md` →
  linha 233. O `dispatching-parallel-agents` é paralelo, mas serve para investigar falhas
  independentes, no mesmo checkout.
- **A recusa é do mantenedor**, na #945: *"we value correctness over raw speed"*. Conferir:
  `gh issue view 945 -R obra/superpowers --comments`.
- **Guias de terceiros o descrevem como paralelo** (Verdent, jamilxt no DEV, Zenn). O código não
  sustenta isso, e o aicf não repete.
- **O custo dele é tempo** ([#743](https://github.com/obra/superpowers/issues/743),
  [#1120](https://github.com/obra/superpowers/issues/1120)). A mitigação da skill é agrupar tarefas
  pequenas do mesmo tipo:
  `grep -n 'Batch small same-shape work' $R/superpowers/skills/subagent-driven-development/references/batching.md`.

### Comparação entre as três formas por subagente

| | `subagent-driven-development` | `/implement` por ticket | `/implement-spec` |
| --- | --- | --- | --- |
| Execução | serial, um subagente por tarefa | uma sessão por ticket, o titular despacha | paralela, na fronteira do grafo |
| Revisão | por tarefa, e a branch no fim | `/code-review` por ticket | só no fim, sobre a branch de integração |
| Workspace | uma worktree para o plano | a branch atual | uma worktree por ticket e branch de integração |
| Ponto forte | corretude passo a passo | controle do titular, atravessa sessões | vazão com grafo largo |
| Custo | tempo | atenção do titular a cada ticket | diff combinado grande, colisão no merge, revisão tardia, cota |

Um relato de orquestrador caseiro sobre o `/implement`
([DEV, set/2026](https://dev.to/day_b3fa2204948ded3059f6f/turning-matt-pococks-implement-into-a-parallel-orchestrator-in-claude-code-1d4a))
teve dois tickets colidindo no merge, ~3,24 M tokens de subagentes, um 429 no oitavo implementador
e 23 problemas num `/code-review` posterior. Nenhum benchmark independente compara o
`subagent-driven-development` com o `/implement-spec` (busca em 2026-10-23 no GitHub, no HN e na
web).

## Relatório de implementação (2026-10-24)

- **Status:** concluído; a verificação de comportamento (item 6) segue em aberto até o uso real.
  CI: run `40069748924`, `completed success`
  (`gh run view 40069748924 --json conclusion -q .conclusion` → `success`).
- **Arquivos alterados:**
  - `skills/implementar-spec/caminhos.md` (novo): o critério dos quatro caminhos;
  - `skills/implementar-spec/matt.md` (novo): entrada, medição, forma, edição dos tickets,
    conferência do tracker, o que dizer, comando com o sufixo;
  - `skills/implementar-spec/SKILL.md`: tabela, ordem de ler `caminhos.md`, retomada antes da
    pergunta do caminho, ponteiro para o `matt.md`, exceção de workspace;
  - `skills/criar-spec/SKILL.md`: ordem de ler `caminhos.md`, anúncio da entrada pelo
    `/aicf:implementar-spec`, alinhamento nos dois modos;
  - `skills/fechar-demanda/SKILL.md`: branch de integração e `/code-review` final do método;
  - `skills/midia/arquivo.md` e `skills/midia/issues.md`: a seção `## Quando o /implement-spec roda`
    e a conferência do ponteiro na operação de alinhar, que o modo issue ganha; "Concluir" com a
    issue já fechada pelo merge;
  - `docs/adr/0010-o-aicf-escreve-as-regras-do-implement-spec-no-tracker-do-matt.md` (novo);
  - `skills/ajuda/SKILL.md`, os dois READMEs, a linha de coleções (template e `.claude/CLAUDE.md`),
    o relatório de governança, a intent do setup, `plugin.json` e `CHANGELOG.md` (`0.44.0`).
- **Commits:**
  - `4df9641` docs: revisar spec do implement-spec — regras no tracker do Matt, sufixo só aponta;
  - `8a98ce4` feat(implementar-spec): 0.44.0 — o caminho do Matt oferece o implement-spec;
  - `6f875af` fix(implementar-spec): achados da revisão do implement-spec.
- **Validação:**
  - `./scripts/check.sh` → `Tudo verde.` antes de cada commit;
  - os itens 2 a 5 da Verificação dão o esperado no `6f875af`: `subagente e com TDD` → nada;
    `caminhos.md` → 2; `matt.md` → só no `implementar-spec`; `implement-spec` ≥ 1 nos oito
    arquivos; a seção ≥ 1 nas duas mídias; o sufixo → 1 no `matt.md`; `calcular a fronteira` → 0
    no `matt.md` e 1 em cada mídia; as frases antigas dos READMEs → 0; `2026-10-23` ≥ 1 no
    relatório de governança;
  - os comandos novos de achar tickets testados: o `grep -rlF '**Spec:** …'` num `.scratch/` de
    teste, e a regex de `## Parent` num JSON de teste, onde acha o `#12` e não o `#123`;
  - revisão por um subagente que não viu a implementação. Dos 15 achados, 14 foram aplicados no
    `6f875af`, entre eles o de severidade alta: a retomada perguntava o caminho e entregava o
    `/to-tickets` de novo antes de chegar ao `matt.md`. O que ficou de fora está em Escopo efetivo;
  - o item 6 (comportamento) segue em aberto. Quem o encerra é o titular, numa sessão nova na
    `0.44.0`, no primeiro projeto com tickets do Matt, pelos cenários do item 6.
- **Escopo efetivo:**
  - **Uma mudança de desenho antes de implementar:** na conversa desta sessão, as instruções ao
    orquestrador saíram do argumento do comando e foram para uma seção do tracker do Matt, nos dois
    modos. O sufixo ficou, mas só aponta a seção. A spec foi revisada em `4df9641`, e a decisão
    está no ADR 0010.
  - **Divergência mantida:** a conferência do tracker roda depois de escolhido o
    `/implement-spec`, e não antes da pergunta da forma, como o item 4 previa. O `/implement` não
    precisa da seção.
  - **Fora da lista da spec:** o `ajuda` teve duas frases corrigidas. Uma dizia que o aicf só
    escreve no tracker no modo arquivo; a outra, que a integração é sempre do método.
  - **Título da seção sem crase**, para casar com o texto do sufixo; os `grep` da spec acompanham.
  - **A seção do tracker local ganhou um quarto item:** como achar os tickets da spec, pela linha
    `**Spec:**`.
- **Lições:**
  - **Nada no Matt manda o agente abrir o `docs/agents/issue-tracker.md`.** As skills dele só
    supõem que o tracker "foi fornecido", e o `CLAUDE.md` traz o ponteiro, não o conteúdo. Regra
    que só mora no tracker depende de o agente decidir abri-lo; para isso servem o sufixo e a
    conferência do ponteiro.
  - **O formato de bloqueio dos tickets não é o do wayfinding:** o `to-tickets` escreve
    `**Blocked by:**` e `## Blocked by`, e o tracker do Matt descreve `Blocked by: NN` só para os
    mapas
    (`sed -n '75p;99,101p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/to-tickets/SKILL.md`).
    Quem lê só o tracker escreve a linha errada.
- **Saída do ritual:** o [ADR 0010](../../adr/0010-o-aicf-escreve-as-regras-do-implement-spec-no-tracker-do-matt.md).
  Nenhuma regra nova no `CLAUDE.md`: as duas lições cabem na regra que já existe, de conferir
  afirmação sobre ferramenta de terceiro no código dela. O PRD não muda.
