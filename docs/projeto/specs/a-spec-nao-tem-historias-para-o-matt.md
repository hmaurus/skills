# A spec do aicf não tem histórias para o caminho do Matt

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (texto curto em skills, template e um ADR, sem decisão de abordagem em aberto)

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
Matt, quando o arquivo ainda não existe, e roda uma vez. A edição **troca** a linha
`The spec is .scratch/<feature-slug>/spec.md` em vez de acrescentar uma segunda, para o tracker não
se contradizer.

## Arquivos e interfaces

- `skills/midia/arquivo.md` — operação nova "Alinhar o tracker do Matt": a conferência
  (`grep -c 'docs/projeto/specs' docs/agents/issue-tracker.md` → 0 é convenção ausente; arquivo
  ausente ou apontando para outro tracker fica com a regra de alinhamento que o `implementar-spec`
  já tem), a linha que sai e a que entra. O `skills/midia/issues.md` não muda: no modo issue o
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
  (só a linha da spec e a linha `Spec:` dos tickets, no modo arquivo), quando (pela operação do
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
   troca da linha da spec com diff, e depois dela `grep -c '.scratch/<feature-slug>/spec.md'` → 0 e
   `grep -c 'docs/projeto/specs' docs/agents/issue-tracker.md` → ≥ 1; os comandos entregues têm um
   argumento cada. Contraprova: com o tracker já convertido, não propõe edição.
4. **Uso real, encerrado pelo titular.** No primeiro projeto que implementar pelo Matt depois da
   versão nova: os tickets do `/to-tickets` abrem com `**Spec:**`, e `/implement <ticket>` numa
   sessão limpa lê a spec antes do primeiro teste (conferir no transcript). Depende de atualizar o
   plugin e de comandos que só o usuário digita; encerra nesse uso, e falhar traz a meia frase do
   `CLAUDE.md` de volta para o escopo.
5. **A regra da spec num lugar só.**
   `grep -c 'não em .docs/superpowers/specs/. nem pelo .to-spec.' skills/setup/templates/claude-md.md .claude/CLAUDE.md`
   → 1 e 1 antes, 0 e 0 depois; `grep -c 'Spec mora só onde a mídia' skills/setup/templates/claude-md.md .claude/CLAUDE.md`
   → 0 e 0 antes, 1 e 1 depois.
6. `./scripts/check.sh` termina em `Tudo verde.`
