# Checklist — aicf

Índice das demandas. `Decidido`, `Em andamento` e `Entregue` espelham as pastas de governança: todo arquivo da pasta tem linha na seção. `Fundação` e `Backlog` não têm pasta. Demanda que cabe numa linha fica só aqui; quando precisa de mais, vira arquivo em [`intents/`](intents/), a linha vira ponteiro e passa para `Decidido`.

Marcar `- [x]` faz parte do ritual de fechamento — não é registro paralelo.

## Fundação

- [ ] Repositório, branch de trabalho e CI mínimo
- [ ] `PRD.md` preenchido

## Decidido

> Demanda decidida, ainda não entrevistada — uma linha por arquivo em [`intents/`](intents/). Sai daqui quando o arquivo vira spec.

- [ ] A entrada de quem chega: o setup se apresenta, e a documentação se divide em duas — [intent](intents/a-entrada-de-quem-chega.md)
- [ ] O usuário escolhe se a governança mora em arquivos ou em issues — [intent](intents/escolher-entre-arquivos-e-issues.md)
- [ ] A governança deste repositório passa a viver em issues — [intent](intents/governanca-em-issues-neste-repo.md)

## Em andamento

> Uma linha por spec em [`specs/`](specs/) — entrevistada, ainda não concluída.

- [ ] O índice envelhece sem avisar, e pedir atenção não conserta — [spec](specs/o-indice-envelhece-sem-avisar.md)

## Entregue

> Uma linha por arquivo em [`specs/concluidas/`](specs/concluidas/), crescendo por baixo. Não apagar item entregue — ele é o histórico do que o produto virou.

- [x] Exceção de idioma quando o domínio regulado perde na tradução (`0.13.4`) — [spec](specs/concluidas/excecao-de-idioma-no-dominio.md)
- [x] A governança orquestra o framework escolhido, não o substitui (`0.13.5`) — [spec](specs/concluidas/orquestrar-o-framework-escolhido.md) · [ADR 0001](../adr/0001-fronteira-de-fase.md)

## Backlog

Ideia que ainda não é certeza. Se couber numa linha, fica aqui; se precisar de contexto, vira arquivo em [`intents/backlog/`](intents/backlog/).

O que separa daqui para `intents/` é **certeza, não urgência**: demanda certa e sem prioridade já sai do backlog e entra em `Decidido`.

**Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item continua plausível depois de resolvido, e ninguém percebe.

> - ...
