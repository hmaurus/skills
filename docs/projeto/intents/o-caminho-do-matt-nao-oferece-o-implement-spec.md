# O caminho do Matt não oferece o implement-spec

Processo — entrevista: a definir · implementação: a definir

O `/aicf:implementar-spec` só conhece um jeito de trabalhar os tickets do Matt: `/implement`
ticket a ticket, com `/clear` entre eles (tabela de caminhos em `skills/implementar-spec/SKILL.md`,
linha do Matt Pocock). Nas skills do Matt (versão 1.3.1) também existe o **`/implement-spec`**: ele
lê os tickets como grafo de tarefas pelas linhas de bloqueio, roda subagentes implementadores
em background, cada um na sua worktree e pelo `/tdd`, junta tudo numa branch de integração com
um subagente de merge, faz um `/code-review` final e apaga as worktrees. Também é
`disable-model-invocation: true`. Num projeto real, com os 14 tickets de uma spec já criados, o
aicf entregou só o comando do `/implement`, e o titular foi descobrir o `/implement-spec` pelo
`/ask-matt`. Decidido: o aicf passa a oferecer o `implement-spec` como segunda forma do caminho
do Matt.

A demanda cobre também o **critério que o agente usa para sugerir o caminho da implementação**.
Com o `implement-spec`, o aicf passa a oferecer duas formas de executar uma spec por subagentes:
uma serial, o `subagent-driven-development` (Superpowers), e uma paralela, o `/implement-spec`
(Matt). O critério de hoje — o parágrafo "O critério para sugerir", repetido em
`skills/criar-spec/SKILL.md` e `skills/implementar-spec/SKILL.md` — não distingue as duas.
Decidido em 2026-10-23: revisar o critério inteiro nesta demanda, porque é o mesmo parágrafo que a
inclusão do `implement-spec` já obriga a reescrever.

## O que já se sabe

- **Onde o aicf lista as skills do Matt:**
  - a tabela e os comandos do passo 3 de `skills/implementar-spec/SKILL.md`;
  - o critério de sugestão em `skills/criar-spec/SKILL.md`;
  - a linha "Coleções de skills de workflow instaladas" do template
    `skills/setup/templates/claude-md.md` e do `.claude/CLAUDE.md` deste repositório, que diz quais
    skills de caminho só o usuário invoca. Hoje ela cita `grill-with-docs`, `to-spec`,
    `to-tickets` e `implement`. Um projeto já acrescentou o `implement-spec` à mão;
  - o `README.md`, na lista "Na fase de implementação": o Matt aparece só como tickets
    "executados um a um". Em "Registro depois da execução", a frase "O `implement` do Matt
    termina no commit; não fecha o ticket" vale só para o `implement`: o `implement-spec` resolve
    os tickets no tracker ao terminar (passo 8 dele);
  - a nota da afirmação 4 de
    [governanca-nos-frameworks-vizinhos.md](../../referencias/governanca-nos-frameworks-vizinhos.md),
    que dá o `implement-spec` como "fora do plugin". Era verdade no sha pinado ali (`c55ee46`,
    v1.2.3), e deixou de ser na v1.3.0.
- **Onde cada forma se encaixa, segundo o `/ask-matt`:** `/implement` por ticket quando o titular
  quer conduzir cada ticket; `/implement-spec` quando prefere orquestrar a construção inteira de
  uma vez.
- **A worktree nasce sem o estado que não está versionado:** `.env`, banco e pastas no gitignore.
  Isso bate de frente com a regra de workspace do próprio `implementar-spec` ("nunca quando a
  verificação depende de estado não versionado"). No projeto que motivou a intent, os testes de
  domínio funcionam na worktree, porque leem a conexão da configuração versionada e usam dados
  únicos num Postgres compartilhado. Já o servidor local e o e2e precisam do `.env` e têm de rodar
  no checkout principal, na branch de integração.
- **Paralelismo com banco compartilhado** só é seguro se nenhum ticket paralelo gerar migration.
  No projeto que motivou a intent, o `to-tickets` já concentrou toda a migration no primeiro
  ticket por esse motivo.
- **A integração muda de forma:** o `/implement` commita na branch atual; o `/implement-spec`
  cria uma branch de integração e, conforme o tracker, abre um PR em rascunho. O aicf precisa
  dizer o que acontece depois: merge na branch de origem, PR, e o commit de fechamento indo onde o
  código ficou, como já manda o passo "Verificar e fechar".

### O `implement-spec` por dentro

Pinado em `mattpocock/skills` `5beb35b` (v1.3.1), clonado em `$R/skills`.

- **Entrou no plugin na v1.3.0.** Antes estava em `skills/in-progress/`. Conferir:
  `git -C $R/skills log --format='%h %cs %s' --diff-filter=A -- skills/engineering/implement-spec/SKILL.md`
  → `24f41cc 2026-09-24 Graduate implement-spec to engineering`.
- **Exige um harness com subagente em background e worktree por subagente.** Sem isso, a doc diz
  que *"it is only a slower `implement`"*. Para trabalho sem grafo de verdade, a doc manda usar o
  `/implement`. Conferir: `grep -n 'only a slower' $R/skills/docs/engineering/implement-spec.md`.
- **Problemas que a própria doc registra, relatados por usuários** (seção "Common questions" de
  `$R/skills/docs/engineering/implement-spec.md`):
  - worktree não evita colisão, adia para o merge. Dois tickets da mesma fronteira deram nomes
    diferentes ao mesmo campo (`blockedSince` × `blockedOn`). Remédio da doc: bloqueio entre
    tickets que tocam o mesmo arquivo, ou notas de exploração que fixam os nomes;
  - o ciclo de revisão e correção pode não parar: uma feature de 5 tickets levou ~4 h. A doc
    manda interromper uma segunda revisão ampla e pedir só checagens focadas nos achados
    corrigidos. O `/code-review` só faz sentido com todos os tickets na branch de integração;
  - no GitHub, ticket bloqueado só começa quando o bloqueador *fecha*, e isso acontece no fim.
    Remédio: o orquestrador calcula a fronteira pelo que já entrou na branch de integração;
  - teste que lê arquivo no gitignore é pulado em silêncio dentro da worktree, e o ticket
    reporta verde. Remédio: rodar a verificação desse ticket no checkout principal;
  - o titular deixa de ler cada ticket ao terminar e revisa a branch de integração no fim;
  - o pareamento de seams do `/implement` não existe; seam que importa vai escrito na spec ou no
    ticket.
- **`/implement` em paralelo** o Matt recomenda com uma worktree por sessão (`claude --worktree`),
  na [mattpocock/skills#429](https://github.com/mattpocock/skills/issues/429), fechada em
  2026-10-06. Conferir:
  `gh issue view 429 -R mattpocock/skills --json comments --jq '.comments[]|select(.author.login=="mattpocock")|.body'`.

### O Superpowers não tem forma paralela, e decidiu não ter

Pinado em `obra/superpowers` `2ce8aa1` (v7.0.1) e na branch `dev` em `b58deb3`, clonado em
`$R/superpowers`.

- **O `subagent-driven-development` é serial:** um implementador por vez, uma worktree para o
  plano inteiro. Conferir:
  `grep -n 'in parallel (conflicts)' $R/superpowers/skills/subagent-driven-development/SKILL.md`
  → linha 233; na `dev`,
  `git -C $R/superpowers show origin/dev:skills/subagent-driven-development/SKILL.md | grep -c 'in parallel (conflicts)'`
  → 1. O `dispatching-parallel-agents` é paralelo, mas serve para investigar falhas
  independentes, no mesmo checkout e sem worktree.
- **A recusa é decisão do mantenedor.** Na
  [obra/superpowers#945](https://github.com/obra/superpowers/issues/945) (2026-03-27):
  *"superpowers prefers iterative implementation over parallel implementation. Parallel work is
  more likely to lead to conflicts and we value correctness over raw speed."* As propostas
  [#1213](https://github.com/obra/superpowers/pull/1213) e
  [#1534](https://github.com/obra/superpowers/pull/1534) foram fechadas em 2026-09-27 ("by design;
  changing that needs eval evidence"). Seguem abertas a
  [#429](https://github.com/obra/superpowers/issues/429) (Agent Teams no
  `subagent-driven-development`) e a [#2368](https://github.com/obra/superpowers/issues/2368)
  (execução em ondas, opt-in). Conferir:
  `gh issue view 945 -R obra/superpowers --comments`; `gh pr view 1534 -R obra/superpowers --comments`.
- **Guias de terceiros descrevem o `subagent-driven-development` como paralelo** — Verdent
  (abr/2026), jamilxt no DEV (jul/2026), Zenn (jun/2026). O código não sustenta isso, e o aicf
  não deve repetir.
- **O custo dele é tempo.** Há relatos de lentidão na
  [#743](https://github.com/obra/superpowers/issues/743) e de revisão desproporcional em tarefa
  trivial na [#1120](https://github.com/obra/superpowers/issues/1120), ambas abertas. A
  mitigação da própria skill é agrupar tarefas pequenas do mesmo tipo num subagente só. Conferir:
  `grep -n 'Batch small same-shape work' $R/superpowers/skills/subagent-driven-development/references/batching.md`.

### Insumo para o critério de sugestão

Comparação levantada em 2026-10-23, nos shas acima:

| | `subagent-driven-development` | `/implement` por ticket | `/implement-spec` |
| --- | --- | --- | --- |
| Execução | serial, um subagente por tarefa | uma sessão por ticket, o titular despacha | paralela, na fronteira do grafo |
| Revisão | por tarefa (spec e qualidade), ciclo de correção, revisão final da branch | `/code-review` por ticket | só no fim, sobre a branch de integração |
| Workspace | uma worktree para o plano | a branch atual | uma worktree por ticket e branch de integração |
| Ponto forte | corretude passo a passo, tarefas acopladas em sequência | controle do titular, contexto limpo por ticket, atravessa sessões | vazão quando o grafo é largo |
| Custo | tempo | atenção do titular a cada ticket | diff combinado grande, colisões no merge, revisão tardia |

- **Paralelismo só existe no `/implement-spec`.** Sugerir o Superpowers "por velocidade" é erro.
- **O paralelismo só se paga com grafo largo.** O
  [resumo da v1.3](https://developer.tenten.co/mattpocock-skills-v1-3-pr-implement-spec-retro)
  sugere a partir de 4 tickets com fronteira paralela de verdade; a doc do Matt diz apenas "sem
  grafo de verdade, `/implement`".
- **As comparações publicadas usam o eixo método imposto × kit que o titular conduz**
  ([nocoders](https://www.nocoders.com/blog/superpowers-vs-pocock-agent-skills/), jun/2026).
  Nenhum benchmark independente compara o `subagent-driven-development` com o `/implement-spec`.
  Busca em 2026-10-23 no GitHub, no HN e na web.
- **Relato de uso de paralelismo sem revisão por ticket**
  ([DEV, set/2026](https://dev.to/day_b3fa2204948ded3059f6f/turning-matt-pococks-implement-into-a-parallel-orchestrator-in-claude-code-1d4a)):
  orquestrador caseiro sobre o `/implement`, antes do `implement-spec` oficial. Dois tickets
  colidiram no merge, foram ~3,24 M tokens de subagentes, e o oitavo implementador caiu com 429
  (limite de uso). Um `/code-review` posterior achou mais 23 problemas. Paralelismo pede cota de
  uso e revisão forte no fim.

## Em aberto para a entrevista

- **Uma linha na tabela ou duas:** o Matt continua um caminho só, com duas formas de executar,
  ou o `implement-spec` vira uma linha própria da tabela, com o critério de sugestão dele.
- **O critério de sugestão, entre todos os caminhos** (`aicf-direto`, `aicf-plan`,
  `subagent-driven-development`, `/implement` por ticket, `/implement-spec`). Sinais candidatos:
  - se cabe numa sessão;
  - o tamanho do grafo e a largura da fronteira;
  - o acoplamento entre as tarefas: tarefas em sequência pedem forma serial;
  - quanto o titular quer conduzir cada passo;
  - a dependência de estado não versionado;
  - arquivo compartilhado entre tickets da mesma fronteira;
  - migration concentrada num só ticket;
  - o custo em tempo e em cota.

  A redação de hoje — Superpowers "quando são muitos passos numa sessão, executados por subagente
  e com TDD" — não diz o que o distingue do `/implement-spec`.
- **Onde o critério mora:** hoje está repetido no `criar-spec`, que grava a sugestão, e no
  `implementar-spec`, que decide. A regra "critério mora na skill que o aplica" sustenta a
  repetição, mas duas cópias divergem; decidir se continua assim e como se confere que as duas
  batem.
- **O que o aicf avisa antes do `/implement-spec`:**
  - `.env` e banco nas worktrees;
  - migration fora do ticket que a concentra;
  - onde rodar a verificação ponta a ponta;
  - os remédios que a doc do Matt registra (bloqueio entre tickets que tocam o mesmo arquivo,
    parar a segunda revisão ampla, fronteira calculada pela branch de integração no GitHub,
    verificação de ticket com estado não versionado no checkout principal).
- **README e relatório:** corrigir as duas frases do `README.md`, e decidir se a nota do relatório
  de governança ganha uma linha datada ou um novo pino do Matt.
- **Fechamento:** o `/aicf:fechar-demanda` depois do `implement-spec` roda uma vez só, sobre a
  branch de integração, e o merge dela na branch de trabalho é pergunta ao titular.
- **Setup:** o template do `CLAUDE.md` passa a citar o `implement-spec`, e o setup de projeto já
  rodando ([intent](o-setup-nao-serve-a-projeto-ja-rodando.md)) atualiza a linha em projetos que
  já existem.
