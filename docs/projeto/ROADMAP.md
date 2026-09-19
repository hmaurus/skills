# Roadmap — aicf

O que ainda não tem arquivo. Quando um item precisa de contexto, vira arquivo em [`intents/`](intents/) e **a linha sai daqui** — a pasta passa a ser o registro inteiro, e nada aponta para nada.

O que já tem arquivo se lê da pasta:

```
head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'
```

## Próximas

> Decidido, ainda sem arquivo.

- [ ] O `git mv` de uma demanda quebra os links que saem dela, e o passo 2 do fechamento só procura os que entram — encerra quando `midia-arquivo.md` e o passo 2 mandarem conferir os dois sentidos, ou rodar o check de links

## Backlog

> Ainda não é certeza. O que separa daqui de `Próximas` é **certeza, não urgência**: demanda certa e sem prioridade já é `Próximas`.
>
> **Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item continua plausível depois de resolvido, e ninguém percebe.

> - ...
