# A spec do aicf não tem histórias para o caminho do Matt

Processo — entrevista: criar-spec · implementação: aicf-direto

Funde o intent "O caminho do Matt pede a spec no argumento", que saiu de `intents/` com esta spec.

## Problema

Quem entrevista pelo `grill-with-docs` implementa pelo Matt quase sempre, com `/to-tickets` e
`/implement`. Duas coisas pioram esse caminho com o aicf:

- **A spec chega ao `to-tickets` sem histórias.** O `to-spec` do Matt escreve uma lista longa de
  histórias de usuário e uma seção de decisões de implementação; o `/aicf:criar-spec`, que o
  substitui no fluxo desde `debde95`, não tem nenhuma das duas. Num projeto privado que consome
  estas skills, a mesma entrevista gerou uma spec por cada um: das 35 histórias do `to-spec`, 4
  diziam algo que a prosa do aicf deixava implícito (um efeito que *não* acontece, uma restrição
  por papel, a perda de acesso ao desativar, uma regra de desenvolvedor escrita como necessidade).
  Medição feita à mão; não há comando que a refaça. É o risco 2 que a nota daquela demanda deixou
  para medir (`grep -n 'Saem as user stories' docs/notas-de-sessao/o-matt-com-e-sem-o-aicf.md`).
- **O `/implement` pede a spec num argumento que o Matt não usa.** O aicf entrega
  `/implement docs/projeto/specs/<nome>.md .scratch/<feature>/issues/<NN>-<slug>.md`, porque o
  ticket local do `to-tickets` não referencia a spec — no Matt padrão ela mora ao lado dos tickets,
  em `.scratch/<feature-slug>/spec.md`, e o aicf a tirou de lá. A regra mora no
  `/aicf:implementar-spec`, que não está carregado quando o usuário conduz o Matt direto: no projeto
  privado, o agente sugeriu o comando só com o ticket e, na pergunta seguinte, o com os dois.

## Solução

**A spec ganha as duas seções do `to-spec` quando a entrevista foi do Matt.** O gatilho é a
entrevista (`entrevista: grill-with-docs`), conhecida antes de a spec começar — não a sugestão de
implementação, que o `criar-spec` só grava depois de a spec estar escrita e mostrada. As seções
são copiadas como regra, não lidas do `to-spec` em runtime:

- **Histórias** — lista numerada "Como \<papel\>, quero \<x\>, para \<y\>", extensa, cobrindo todo
  o comportamento, inclusive o que cada papel *não* pode e o efeito que *não* acontece;
- **Decisões de implementação** — o que a entrevista decidiu e o código não mostra: arquitetura,
  schema, contrato de API, interação entre módulos.

**O ticket leva à spec, e o `/implement` volta a receber só o ticket.** No modo arquivo, o
`docs/agents/issue-tracker.md` do Matt passa a dizer que a spec da feature é a da demanda, em
`docs/projeto/specs/<nome>.md`, e que todo ticket abre com a linha
`**Spec:** docs/projeto/specs/<nome>.md`. O `to-tickets` segue o tracker e grava a linha; quem
implementa o ticket numa sessão limpa lê a linha e chega à spec. Os comandos entregues voltam ao
padrão do Matt: `/to-tickets docs/projeto/specs/<nome>.md` e
`/implement .scratch/<feature>/issues/<NN>-<slug>.md`; no modo issue, `/to-tickets #<n>` e
`/implement #<ticket>` — o ticket remoto já nasce com `## Parent` apontando a issue da spec.

**A convenção entra no tracker por uma receita só, chamada de dois pontos.** A operação "Alinhar
o tracker do Matt" mora no `skills/midia/arquivo.md`, que as duas skills já leem: confere a
convenção e, faltando, propõe a edição com o diff e aplica com o aceite do usuário. Quem a chama:

- o `/aicf:criar-spec`, no fim, quando a entrevista foi pelo `grill-with-docs` — é o único passo
  garantido antes do `/clear` que ele mesmo recomenda depois de entrevista longa. Sem isso, quem
  limpa a sessão e digita `/to-tickets` direto nunca passa pelo `implementar-spec`, e os tickets
  nascem sem a linha `Spec:`;
- o `/aicf:implementar-spec`, na checagem de alinhamento que ele já faz antes de oferecer o Matt —
  para a entrevista que foi por outro caminho e terminou no Matt.

Acontece uma vez por projeto — na segunda chamada a conferência já passa — e serve para projeto
novo e antigo sem nota de migração. O setup do aicf não a chama: costuma rodar antes do setup do
Matt, quando o arquivo ainda não existe, e roda uma vez.

**A edição troca as três frases do tracker que mandam a spec para `.scratch/`, e acrescenta a
exceção à regra de caminho.** Acrescentar ao lado deixaria o tracker se contradizendo, e o
`to-tickets` manda "avoid specific file paths" nos tickets
(`grep -n 'avoid specific file paths' …/to-tickets/SKILL.md` → linha 105), o que a linha `Spec:`
contraria se ninguém disser que ela é exceção. As operações de wayfinding, os tickets e os mapas
seguem em `.scratch/`, intocados. No `issue-tracker-local.md` do Matt `1.3.1`:

| Frase do Matt | Passa a ser |
| --- | --- |
| `Issues and specs for this repo live as markdown files in .scratch/.` | Os tickets deste repositório moram em `.scratch/`; a spec de cada feature é a da demanda do aicf, em `docs/projeto/specs/<nome>.md`. |
| `The spec is .scratch/<feature-slug>/spec.md` | A spec é a da demanda, em `docs/projeto/specs/<nome>.md`. Todo ticket abre, logo abaixo do título, com `**Spec:** docs/projeto/specs/<nome>.md`, com o caminho real da demanda. A linha é obrigatória mesmo onde a skill manda evitar caminho de arquivo: ela aponta a spec, não a implementação. |
| `Create a new file under .scratch/<feature-slug>/ (creating the directory if needed).` | a mesma frase, mais: "Spec não: vai para `docs/projeto/specs/<nome>.md`." |

**A conferência olha as duas obrigações e a localização antiga, separadas**, para que um tracker
convertido pela metade — à mão, por exemplo — não passe como alinhado. A convenção está presente só
quando as três dão o esperado em `docs/agents/issue-tracker.md`:

- localização nova: `grep -c 'docs/projeto/specs'` → ≥ 1;
- obrigação da referência: `grep -c '\*\*Spec:\*\*'` → ≥ 1;
- localização antiga ausente: `grep -c '\.scratch/<feature-slug>/spec\.md\|Issues and specs'` → 0.

Faltando alguma, a operação propõe só o que falta, preservando o resto do arquivo.

## Arquivos e interfaces

- `skills/midia/arquivo.md` — operação nova "Alinhar o tracker do Matt": as três conferências e
  as três trocas da Solução (arquivo ausente ou apontando para outro tracker fica com a regra de
  alinhamento que o `implementar-spec` já tem). O `skills/midia/issues.md` não muda: no modo issue o
  ticket remoto já nasce com `## Parent`.
- `skills/criar-spec/SKILL.md` — item novo na lista "A spec", de umas 5 linhas:

  ```markdown
  - **Histórias** e **Decisões de implementação** — só quando a entrevista foi pelo
    `grill-with-docs` (Matt), porque é o que o `to-tickets` usa para fatiar:
    - Histórias: lista numerada "Como <papel>, quero <x>, para <y>", extensa, cobrindo todo o
      comportamento, inclusive o que cada papel *não* pode e o efeito que *não* acontece
    - Decisões: o que a entrevista decidiu e o código não mostra (arquitetura, schema, contrato de
      API, interação entre módulos)
  ```

  e, em "Ao terminar", com a entrevista pelo `grill-with-docs` e mídia arquivo, a chamada à
  operação "Alinhar o tracker do Matt" antes de o usuário ir embora.

- `skills/implementar-spec/SKILL.md`, parágrafo "O Matt só entra entre as opções…" do passo 3:
  - a checagem de alinhamento passa a chamar a operação "Alinhar o tracker do Matt" do
    `midia/arquivo.md`, no modo arquivo;
  - sai a frase "os comandos entregues levam a spec junto, porque o ticket local não a referencia…"
    e os comandos de dois argumentos; entram os de um.
- `skills/setup/SKILL.md` — a frase "O aicf não escreve a config do Matt" fica falsa; passa a
  dizer que a convenção da spec entra no tracker do Matt na primeira spec entrevistada pelo
  `grill-with-docs`, ou na primeira vez que o caminho dele for escolhido. Só a frase: o setup não
  edita o tracker, porque as duas chamadas já cobrem projeto novo, antigo e tracker regravado, e o
  setup roda uma vez
  ([o setup não serve a projeto já rodando](../intents/o-setup-nao-serve-a-projeto-ja-rodando.md)).
- `skills/setup/templates/claude-md.md` e `.claude/CLAUDE.md` — o fim da regra "A passagem entre
  fases é da governança" troca a lista de exceções ("não em `docs/superpowers/specs/` nem pelo
  `to-spec`") pelo princípio: **spec mora só onde a mídia do registro manda** (`docs/projeto/specs/`,
  ou issue `aicf:spec`), **qualquer que seja a skill que a escreva** — nunca em
  `docs/superpowers/specs/` nem em `.scratch/`. Hoje o agente só conhece a pasta das specs dentro de
  uma skill do aicf, que manda ler o `midia/`; fora dela, segue o lugar que a skill da outra coleção
  manda. O template só chega a projeto novo; os que já existem ficam com o
  [intent do setup](../intents/o-setup-nao-serve-a-projeto-ja-rodando.md).
- `docs/adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md` — ADR novo. O
  [0004](../../adr/0004-midia-do-registro-e-config-propria.md) diz que o aicf **lê** o
  `issue-tracker.md` e não depende dele; escrever nele é relação nova. Registra: o que se escreve
  (só as três frases da Solução, no modo arquivo — abertura, localização da spec com a linha
  `Spec:` e a exceção à regra de caminho, e a operação de publicação; wayfinding fica intocado), quando (pela operação do
  `midia/arquivo.md`, chamada do `criar-spec` e do `implementar-spec`, com aceite), e o custo assumido — rodar `/setup-matt-pocock-skills` de novo
  regrava o arquivo e apaga a convenção; o Matt só pede isso para trocar de tracker ou recomeçar
  (`grep -n 're-running this skill' …/setup-matt-pocock-skills/SKILL.md`), e a próxima chamada
  da operação a repõe.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — versão nova, em par.

## Fora de escopo

- **O `to-spec` no fluxo, gravando em `specs/` e adotado pelo `criar-spec`.** Pesado contra a
  seção copiada: desfaria texto em quatro lugares (`.claude/CLAUDE.md`,
  `skills/setup/templates/claude-md.md`, `skills/ajuda/SKILL.md`, `skills/midia/issues.md`),
  deixaria dois formatos de spec em `specs/` e faria a adoção depender de o agente achar o intent
  da mesma demanda por julgamento. O ganho que ele trazia são as duas seções, agora copiadas.
- **O agente ler o `to-spec` do cache.** O `disable-model-invocation` não impede o `Read`, mas o
  caminho tem a versão do Matt (há duas no cache), e o texto dele manda o contrário do aicf —
  publicar no tracker, não incluir caminho de arquivo. A demanda anterior já tinha posto isso fora
  pelo mesmo motivo.
- **Seção de histórias nos outros caminhos** (entrevista pelo `criar-spec` ou pelo
  `brainstorming`). O ganho medido foi para o `to-tickets`; uma entrevista pelo `criar-spec` que
  acaba sugerindo o Matt fica sem as seções.
- **Arquivo de referência do Matt** lido só no caminho dele. A regra cabe em 5 linhas no
  `criar-spec` e a convenção no parágrafo do Matt que o `implementar-spec` já tem; o arquivo
  custaria uma leitura a mais e o risco de não ser lido.
- **Meia frase no bloco `## Agent skills` do `CLAUDE.md`** mandando o `/implement` ler a spec da
  linha `Spec:`. O `/implement` não abre o tracker, mas lê o ticket, e a linha está nele. Entra só
  se a Verificação 4 falhar.
- **Corrigir a linha `Spec:` quando a spec vai para `concluidas/`.** O fechamento total roda depois
  do último ticket, e ticket fechado não se reabre; no fechamento parcial a spec continua em
  `specs/`.
- **Entrevista fora do `grill-with-docs` seguida de `/to-tickets` direto**, sem passar pelo
  `implementar-spec`, num projeto cujo tracker ainda não tem a convenção: os tickets nascem sem a
  linha `Spec:`. É o caso raro — quem entrevista pelo Matt já passou pela operação no fim do
  `criar-spec` —, e a primeira entrevista pelo grill do projeto o fecha para sempre.
- **Nome da pasta do `.scratch/` igual ao nome da spec.** A linha `Spec:` já liga um ao outro, e a
  spec troca de nome quando a demanda se renomeia.

## Verificação

1. **O `criar-spec` pede as seções.** `grep -c 'istórias' skills/criar-spec/SKILL.md` → 0 antes,
   ≥ 1 depois; `grep -c 'Decisões de implementação' skills/criar-spec/SKILL.md` → 0 antes, 1 depois.
2. **Comportamento do `criar-spec`, por subagente.** Num repositório de rascunho com `docs/projeto/`,
   um subagente segue o `skills/criar-spec/SKILL.md` **deste repositório** (não o do cache) a
   partir de uma conversa de `grill-with-docs` já resolvida, com dois papéis de usuário. A spec
   gravada tem as seções Histórias e Decisões de implementação, e, com o
   `docs/agents/issue-tracker.md` do Matt copiado de `issue-tracker-local.md`, o subagente propõe
   a troca da linha da spec com diff antes de terminar. Contraprova: a mesma demanda com
   entrevista pelo próprio `criar-spec` sai sem as duas seções e sem tocar no tracker.
3. **Comportamento do `implementar-spec`, por subagente.** Num repositório de rascunho em modo
   arquivo, com `docs/agents/issue-tracker.md` copiado de
   `setup-matt-pocock-skills/issue-tracker-local.md`, um subagente segue o
   `skills/implementar-spec/SKILL.md` deste repositório com o caminho do Matt escolhido: propõe a
   troca das três frases com diff, e depois dela as três conferências da Solução, rodadas em
   `docs/agents/issue-tracker.md`, dão ≥ 1, ≥ 1 e 0; os comandos entregues têm um argumento cada.
   Contraprovas: com o tracker já convertido, não propõe edição; com o tracker convertido pela
   metade — localização trocada, sem a obrigação do `**Spec:**` —, propõe só a frase que falta.
4. **Uso real, encerrado pelo titular.** No primeiro projeto que implementar pelo Matt depois da
   versão nova: os tickets do `/to-tickets` abrem com `**Spec:**` seguido do caminho real da
   demanda (`grep -L '^\*\*Spec:\*\* docs/projeto/specs/[a-z0-9-]*\.md' .scratch/<feature>/issues/*.md`
   não lista nenhum), e `/implement <ticket>` numa
   sessão limpa lê a spec antes do primeiro teste (conferir no transcript). Depende de atualizar o
   plugin e de comandos que só o usuário digita; encerra nesse uso, e falhar traz a meia frase do
   `CLAUDE.md` de volta para o escopo.
5. **A regra da spec num lugar só.**
   `grep -c 'não em .docs/superpowers/specs/. nem pelo .to-spec.' skills/setup/templates/claude-md.md .claude/CLAUDE.md`
   → 1 e 1 antes, 0 e 0 depois; `grep -c 'Spec mora só onde a mídia' skills/setup/templates/claude-md.md .claude/CLAUDE.md`
   → 0 e 0 antes, 1 e 1 depois.
6. `./scripts/check.sh` termina em `Tudo verde.`

## Relatório de implementação (2026-10-12)

**Status:** concluído, com a Verificação 4 (uso real) em aberto. Encerra o titular no primeiro
projeto que implementar pelo Matt na `0.38.0`: os tickets do `/to-tickets` abrem com `**Spec:**`
e o caminho exato da demanda, e o `/implement <ticket>` numa sessão limpa lê **esse** arquivo antes
do primeiro teste (conferir no transcript qual spec foi lida). O `grep -L` da Verificação 4 aceita
qualquer nome sob `specs/`, inclusive inexistente ou de outra demanda; o aceite é, com
`S=docs/projeto/specs/<nome>.md`, `test -f "$S"` verdadeiro e
`grep -LFx "**Spec:** $S" .scratch/<feature>/issues/*.md` sem saída — ele lista o ticket que
aponta outra spec. Ajuste vindo do
[parecer do Codex](../../agente-codex/revisoes/revisao-implementacao-a-spec-nao-tem-historias-para-o-matt.md).
Falhar traz de volta a meia frase do bloco `## Agent skills` do `CLAUDE.md`, que estava fora de
escopo.

**Arquivos alterados**

- `skills/midia/arquivo.md` — operação "Alinhar o tracker do Matt": conferências, as três trocas,
  e a regra de propor só o que falta.
- `skills/criar-spec/SKILL.md` — item Histórias e Decisões de implementação, condicionado ao
  `grill-with-docs`; passo 3 novo em "Ao terminar", chamando a operação.
- `skills/implementar-spec/SKILL.md` — a operação roda com o Matt escolhido; comandos de um
  argumento.
- `skills/setup/SKILL.md` — a frase "o aicf não escreve a config do Matt" virou "o setup não edita
  o tracker", com quando a convenção entra.
- `skills/ajuda/SKILL.md` — fora da lista da spec, veio da revisão: o aicf também escreve no tracker.
- `.claude/CLAUDE.md` e `skills/setup/templates/claude-md.md` — "Spec mora só onde a mídia do
  registro manda".
- [ADR 0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md) — novo.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.38.0`.

**Commits**

- `ddb49fa` feat(matt): spec com histórias e ticket que leva à spec
- `83e3d21` fix(matt): ajustes da revisão na operação do tracker

**Validação**

- Verificação 1: `grep -c 'istórias' skills/criar-spec/SKILL.md` 0 → 2;
  `grep -c 'Decisões de implementação' skills/criar-spec/SKILL.md` 0 → 1 (em `83e3d21`).
- Verificação 2, por subagente seguindo o `criar-spec` deste repositório, em repositório de
  rascunho com o tracker copiado do `issue-tracker-local.md` do Matt `1.3.1`: com
  `entrevista: grill-with-docs`, a spec saiu com Histórias (9) e Decisões de implementação, e o
  subagente propôs com diff as três trocas antes de terminar. Contraprova, entrevista pelo próprio
  `criar-spec`: spec sem as duas seções, tracker intocado.
- Verificação 3, por subagente seguindo o `implementar-spec` deste repositório, com o Matt
  escolhido: tracker original → três trocas propostas com diff, conferências 0/0/2 antes e 3/1/0
  depois, comandos `/to-tickets docs/projeto/specs/<nome>.md` e
  `/implement .scratch/<feature>/issues/<NN>-<slug>.md`. Contraprovas: tracker já convertido →
  nenhuma edição; convertido pela metade (sem `**Spec:**`) → só a frase da spec, 3/1/0 depois.
  Rodadas em `ddb49fa`, antes da quarta conferência; ela dá 0 no `issue-tracker-local.md` original
  e 1 nos quatro trackers que os subagentes deixaram convertidos.
- Verificação 5: `grep -c 'não em .docs/superpowers/specs/. nem pelo .to-spec.'` no template e no
  `.claude/CLAUDE.md` 1 e 1 → 0 e 0; `grep -c 'Spec mora só onde a mídia'` 0 e 0 → 1 e 1.
- Verificação 6: `./scripts/check.sh` termina em `Tudo verde.` em `ddb49fa` e em `83e3d21`.
- Revisão por subagente fresco, contra a spec: nenhum bloqueio, quatro ajustes e três notas; seis
  adotados em `83e3d21`, o sétimo é o desvio de momento abaixo.

**Escopo efetivo**

- **A operação roda com o Matt já escolhido, não na checagem antes de oferecê-lo**, como dizia a
  Solução. A Verificação 3 já a rodava "com o caminho do Matt escolhido", e assim quem escolhe outro
  caminho não recebe proposta de edição no tracker.
- **Quarta conferência**, `grep -c 'Spec não: vai para'` ≥ 1, vinda da revisão: com as três da
  spec, um tracker sem a troca da frase de publicação passava como alinhado, e "propor só a frase
  que falta" não tinha conferência para essa frase.
- A tabela das trocas reproduz as crases e o marcador de lista do original do Matt, para a troca
  literal casar.
- `skills/ajuda/SKILL.md` ganhou uma frase, fora da lista da spec.

**Lições**

- Inserir o passo 3 em "Ao terminar" do `criar-spec` deixou o "(passo 3)" do passo 2, que aponta
  para o próprio arquivo, mirando o passo errado; a revisão pegou. É a regra "Passo citado por
  número é ponteiro" do `.claude/CLAUDE.md`, já com o `grep` que acusa — nenhuma regra nova.
- Achado dos subagentes, registrado no Backlog do `ROADMAP.md`: o aviso de divergência do tracker
  no `criar-spec` e no `fechar-demanda` não diz que alinhar é o tipo e não a pasta.
- Promoção do passo 3: o [ADR 0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md),
  escrito como parte da demanda; nenhuma regra, skill ou doc de referência novos.

