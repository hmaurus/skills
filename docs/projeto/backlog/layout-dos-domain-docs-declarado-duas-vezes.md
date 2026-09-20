# O layout dos domain docs está declarado duas vezes

Processo — entrevista: a definir · implementação: a definir

> **Encerra quando** `grep -n 'CONTEXT.md\|docs/adr' skills/setup/templates/claude-md.md` devolver
> ponteiro em vez de layout — ou quando a entrevista concluir que a duplicação se sustenta e
> arquivar este arquivo em `concluidas/` com o motivo.
>
> **Reabrir quando** existir o primeiro monorepo com as duas coleções instaladas — é o único caso em
> que as duas declarações divergem. Até lá elas concordam, e este arquivo é registro de achado, não
> pendência: passar na frente dele não pede reavaliação.

## Problema

Onde moram o glossário do domínio e os ADRs está escrito em dois lugares independentes, num
repositório que rode as duas coleções:

| Onde | O que diz |
| --- | --- |
| `docs/agents/domain.md`, gravado pelo `/setup-matt-pocock-skills` | `CONTEXT.md` na raiz **ou** `CONTEXT-MAP.md` apontando para um `CONTEXT.md` por contexto; `docs/adr/` na raiz e, em monorepo, também `src/<contexto>/docs/adr/` |
| Seção "Registro" de `skills/setup/templates/claude-md.md`, que o aicf cola no `CLAUDE.md` | `CONTEXT.md` (sem dizer onde) e `docs/adr/`, numerado e imutável, criados preguiçosamente |

**Concordam hoje por coincidência**, no caso de repositório de contexto único — que é quase todo
repositório. Em monorepo divergem: o template do aicf não sabe que `CONTEXT-MAP.md` existe, nem que
pode haver ADR por contexto, e vai mandar escrever na raiz um ADR que deveria ser do contexto.

O `/aicf:fechar-demanda` já delega o formato: *"ADR e glossário são do `/domain-modeling` (Matt
Pocock) — formato e numeração são dele; sem ele, um parágrafo em `docs/adr/0001-slug.md`, imutável,
basta"*. A delegação está feita no passo que **usa** os arquivos; o que ficou para trás é o template
que **declara onde eles ficam**.

## Saída provável

O template apontar para `docs/agents/domain.md` quando ele existir, e manter a declaração própria —
raiz, preguiçosa — como fallback para quem não tem a outra coleção. Mesmo padrão dos dois lugares
onde o método já defere ao vizinho.

## O que decidir na entrevista

- **O template é estático, colado uma vez no setup.** Ele não pode "ler o arquivo se existir" depois
  de colado. Então a escolha acontece no `/aicf:setup`, que já sabe se a outra coleção está
  instalada — ou o texto colado traz as duas hipóteses, o que é pior de ler.
- **Quem chega a monorepo depois.** O repositório vira monorepo, o Matt reescreve `domain.md` com
  `CONTEXT-MAP.md`, e o `CLAUDE.md` do aicf continua dizendo raiz. Nada reconcilia, e não
  necessariamente precisa.
- **Vale o custo? Hoje, não — e o motivo não é o preço.** O conserto não fecha o buraco. O caso que
  dói é o repositório virar monorepo, ou o Matt ser instalado, **depois** do setup; a ramificação
  cobriria só quem já tem as duas coisas no dia em que o template é colado, e deixaria a impressão
  de que o problema foi resolvido — pior que não mexer. Em repositório de contexto único, que é
  quase todo, os dois concordam. Decidido em 2026-09-15, na entrevista que originou este arquivo;
  o gatilho de reabertura está no topo.

## Origem

Levantado durante a entrevista de
[o usuário escolhe se a governança mora em arquivos ou em issues](../concluidas/escolher-entre-arquivos-e-issues.md),
ao mapear o que o aicf e o conjunto do Matt duplicam. Aquela demanda tratou a duplicação do
**substrato** — onde o trabalho mora — e deixou esta, que é de outro assunto, fora do escopo.
