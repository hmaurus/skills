# Roadmap — aicf

O que ainda não tem arquivo. Quando um item precisa de contexto, vira arquivo em [`intents/`](intents/) e **a linha sai daqui** — a pasta passa a ser o registro inteiro, e nada aponta para nada.

O que já tem arquivo se lê da pasta:

```
head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/concluidas/*.md | sed 's/^# //'
```

## Próximas

> Decidido, ainda sem arquivo.


## Backlog

> Ainda não é certeza. O que separa daqui de `Próximas` é **certeza, não urgência**: demanda certa e sem prioridade já é `Próximas`.
>
> **Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item continua plausível depois de resolvido, e ninguém percebe.

> - ...

- **O aviso de divergência do tracker do Matt confunde pasta com tipo.** O `criar-spec`, o `implementar-spec` e o `fechar-demanda` mandam avisar quando o `docs/agents/issue-tracker.md` "discordar da linha" da mídia (`grep -rn 'discordar da linha' skills/` → 3). Num teste por subagente, o `criar-spec` leu "specs em `.scratch/`" do tracker local do Matt como divergência, num projeto em modo arquivo, e daria um aviso falso. O `implementar-spec` já diz que alinhar é o tipo, não a pasta; os outros dois não. Encerra quando as três frases disserem "tipo, não pasta", ou quando um uso real com tracker local não alinhado passar pelo `criar-spec` sem aviso.
