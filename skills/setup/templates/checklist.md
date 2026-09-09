# Checklist — \<NOME\>

Índice das demandas. `Decidido`, `Em andamento` e `Entregue` espelham as pastas de governança: todo arquivo da pasta tem linha na seção. `Fundação` e `Backlog` não têm pasta. Demanda que cabe numa linha fica só aqui; quando precisa de mais, vira arquivo em [`intents/`](intents/), a linha vira ponteiro e passa para `Decidido`.

Marcar `- [x]` faz parte do ritual de fechamento — não é registro paralelo.

## Fundação

- [ ] Repositório, branch de trabalho e CI mínimo
- [ ] `PRD.md` preenchido

## Decidido

> Demanda decidida, ainda não entrevistada — uma linha por arquivo em [`intents/`](intents/). Sai daqui quando o arquivo vira spec.

## Em andamento

> Uma linha por spec em [`specs/`](specs/) — entrevistada, ainda não concluída.

## Entregue

> Uma linha por arquivo em [`specs/concluidas/`](specs/concluidas/), crescendo por baixo. Não apagar item entregue — ele é o histórico do que o produto virou.

## Backlog

Ideia que ainda não é certeza. Se couber numa linha, fica aqui; se precisar de contexto, vira arquivo em [`intents/backlog/`](intents/backlog/).

O que separa daqui para `intents/` é **certeza, não urgência**: demanda certa e sem prioridade já sai do backlog e entra em `Decidido`.

**Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item continua plausível depois de resolvido, e ninguém percebe.

> - ...
