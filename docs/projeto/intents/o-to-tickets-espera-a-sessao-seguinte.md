# O `/to-tickets` espera a sessão seguinte

Processo — entrevista: a definir · implementação: a definir

Quando a entrevista vai pelo `grill-with-docs` e a spec sai com a sugestão `to-tickets`, o
fatiamento só acontece na sessão seguinte. O `/aicf:criar-spec` grava a spec, alinha o tracker do
Matt e, com a entrevista longa, sugere limpar a sessão. A implementação começa então por
`/aicf:implementar-spec <spec>`, que relê a spec, pergunta o caminho, confere o tracker de novo e
só então entrega o `/to-tickets`. O usuário ainda volta para escolher a forma (`/implement` ou
`/implement-spec`) e limpa a sessão uma segunda vez. São duas sessões até o primeiro ticket, e a
primeira delas não implementa nada.

Num projeto privado que consome estas skills, depois de uma entrevista longa pelo
`grill-with-docs`, o usuário pediu que o fatiamento e o registro fossem feitos ainda na sessão da
entrevista, para a sessão nova ir direto ao `/implement-spec`. Decidido registrar a mudança.

## O que já se sabe

- **O `criar-spec` já faz metade:** ele roda o "Alinhar o tracker do Matt" ao fim da entrevista
  pelo `grill-with-docs` (`grep -c 'Alinhar o tracker do Matt' skills/criar-spec/SKILL.md` → 1, na
  0.45.0). Mas ele sugere o `/clear` com a entrevista longa (`grep -c 'Entrevista longa'
  skills/criar-spec/SKILL.md` → 1) e diz que quem decide o caminho é o `implementar-spec`
  (``grep -c 'Quem decide é o `/aicf:implementar-spec`' skills/criar-spec/SKILL.md`` → 1).
- **O `implementar-spec` é quem entrega o comando:**
  ``grep -c 'comando: `/to-tickets docs/projeto/specs/<nome>.md`' skills/implementar-spec/SKILL.md``
  → 1. Ele também cobre a volta numa sessão nova, com a spec já fatiada: o
  [`matt.md`](../../../skills/implementar-spec/matt.md) vai direto à medição do grafo
  (`grep -c 'Retomada' skills/implementar-spec/matt.md` → 1). Portanto o caminho de volta já
  existe; falta só o de ida.
- **O `/to-tickets` aproveita a conversa:** o passo 1 dele é "Work from whatever is already in the
  conversation context"
  (`grep -c 'Work from whatever is already in the conversation context'
  ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.2/skills/engineering/to-tickets/SKILL.md`
  → 1, na 1.3.2). Fatiar logo depois da entrevista usa o que ela decidiu. Fatiar numa sessão limpa
  depende só do texto da spec.
- **O motivo do `/clear` não se aplica ao fatiamento.** O `criar-spec` limpa a sessão porque "o
  resíduo da conversa ancora a implementação na memória em vez do texto". O `/to-tickets` não
  implementa: ele escreve tickets que a sessão de implementação lê limpa.
- **O `/to-tickets` só o usuário invoca** (`disable-model-invocation: true` no frontmatter). O
  agente entrega o comando e espera, como o `implementar-spec` já faz.

## A proposta do usuário

Levar a entrega do `/to-tickets` para o fim do `criar-spec`, ou para uma regra do `CLAUDE.md`, em
vez de deixá-la no `implementar-spec`. A conversa que motivou este registro sugeriu a primeira
forma:

- Com a sugestão `to-tickets` aceita ao fim da entrevista, o `criar-spec` entrega
  `/to-tickets <spec>` na mesma sessão.
- De volta dele, o agente segue o `matt.md` (medir o grafo, escolher a forma, editar os bloqueios)
  e grava a forma na linha `Processo`.
- Só então sugere o `/clear`, com o comando de implementação pronto.

A regra no `CLAUDE.md` parece pior: o método é do aicf, e cada projeto que o consome teria de
repeti-la.

## Mover a entrega não basta: o `implementar-spec` faz mais no caminho do Matt

Antes e depois do `/to-tickets`, o `implementar-spec` e o `matt.md` fazem mais coisas que o
`criar-spec` não tem. Mover só a entrega do comando as perderia:

| O que | Onde está hoje | O `criar-spec` já faz? |
| --- | --- | --- |
| Conferir se a mídia e o tracker casam; com divergência, tirar o Matt das opções | `implementar-spec`, passos 1 e 3 | Em parte: alinha o tracker só quando a entrevista foi pelo `grill-with-docs`. Spec entrevistada pelo `criar-spec` ou pelo `brainstorming` com sugestão `to-tickets` ficaria sem o alinhamento |
| Ler os arquivos da spec, e perguntar se o trecho ficou complexo demais para a demanda (refatoração num commit próprio, antes) | `implementar-spec`, passo 2 | Não. O passo 2 do `/to-tickets` explora o código e procura refatoração prévia; falta conferir se cobre o que o aicf pede |
| Perguntar o caminho com opções e gravar `implementação: <caminho>` na linha `Processo` | `implementar-spec`, passo 3 | Não: o `criar-spec` grava só a sugestão ("Quem decide é o `/aicf:implementar-spec`") |
| Decidir o workspace (no Matt, depois da forma) | `implementar-spec`, passo 3, e `matt.md` | Não |
| Medir o grafo, escolher entre `/implement` e `/implement-spec`, pôr os bloqueios nos tickets, conferir o tracker, os avisos da conversa e o comando com o sufixo da seção do tracker | `matt.md` | Não |

**Por isso, a forma mais simples é o `criar-spec` emendar o `implementar-spec` na mesma sessão**,
em vez de copiar essas regras. Com a sugestão `to-tickets` aceita, o `criar-spec` não sugere o
`/clear`: invoca o `/aicf:implementar-spec <spec>`, que já pergunta o caminho, alinha o tracker,
entrega o `/to-tickets` e, de volta dele, segue o `matt.md` até entregar o comando de
implementação. O `/clear` vem só no fim, antes da sessão de implementação. A mudança fica numa
frase do passo 4 do `criar-spec`, e as regras do Matt continuam num lugar só. Copiar as regras
para o `criar-spec` seria ter dois mecanismos para a mesma coisa.

## Em aberto para a entrevista

- **A frase do `/clear`:** o passo 4 do `criar-spec` diz para limpar a sessão antes da
  implementação, porque o resíduo da conversa ancora a implementação. Reescrevê-la para separar o
  fatiamento, que se beneficia da conversa, da implementação, que não deve se apoiar nela.
- **Só com a sugestão `to-tickets`, ou sempre?** Com as sugestões `aicf-direto` e `aicf-plan`, o
  `implementar-spec` implementa na mesma sessão, e aí o motivo do `/clear` volta a valer.
- **O passo 2 do `implementar-spec`:** se a exploração do `/to-tickets` dispensa a leitura e a
  pergunta de complexidade, ou se o `implementar-spec` as roda antes de entregar o comando, como
  já faz hoje. **O caso de origem pende para manter o passo 2 antes do comando.** Rodado entre o
  fim da entrevista e o `/to-tickets`, numa leitura por subagente, ele mudou a spec em quatro
  pontos que a entrevista não tinha visto:
  - três refatorações prévias, uma delas porque o acesso aos dados a mover estava em quatro
    módulos e a spec citava dois;
  - um campo obrigatório novo que quebraria o salvar de um tipo de conta que manda só parte do
    formulário;
  - uma gravação que a spec queria "na mesma transação", mas o código atual não abria
    transação;
  - um componente de interface que a spec citou, mas que uma revisão anterior tinha reservado à
    landing.

  O `/to-tickets` fatiaria a spec sem esses pontos, e o "procurar refatoração prévia" dele não
  garante o commit próprio nem a volta à spec que o aicf pede.
- **Tickets nascidos numa worktree:** a sessão do caso de origem precisou de worktree para editar.
  Era uma sessão em segundo plano, e o guarda do Claude Code recusa edição no checkout
  compartilhado. Os tickets do `/to-tickets` nascem então na branch da worktree, sem commit. A
  seção que o "Alinhar o tracker do Matt" escreve já diz que o `/to-tickets` não faz commit e
  manda passar os tickets pelo caminho do checkout principal
  (``grep -c 'o `/to-tickets` não faz commit dos tickets' skills/midia/arquivo.md`` → 1). Falta dizer que, fatiado numa worktree, os tickets e a spec revisada vão em commit e para
  a branch de trabalho antes do comando de implementação.
- **Entrevista curta:** o `criar-spec` já permite emendar a implementação na mesma sessão. Decidir
  se a mudança vale para os dois tamanhos de entrevista.
- **O `/aicf:ajuda` e o README:** o mapa do ciclo diz que o fatiamento é da fase de
  implementação.
