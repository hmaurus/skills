# Roadmap — aicf

O que ainda não tem arquivo. Quando um item precisa de contexto, vira arquivo em [`intents/`](intents/) e **a linha sai daqui** — a pasta passa a ser o registro inteiro, e nada aponta para nada.

O que já tem arquivo se lê da pasta:

```
head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/concluidas/*.md | sed 's/^# //'
```

## Próximas

> Decidido, ainda sem arquivo.

- **Atualizar o aicf nos outros harnesses desta máquina, pelo README.** O Antigravity tem a cópia 0.39.0 e o Codex a 0.38.1 (`agy plugin list --json | jq -r '.[] | select(.name=="aicf") | .version'`, `codex plugin list | grep aicf@`), e o opencode não tem o aicf. Vem depois de [o aicf quebra fora do Claude Code](concluidas/o-ciclo-nunca-rodou-em-outro-agente.md), seguindo os comandos de instalar e atualizar que ela escreve no README: é rodá-los que os prova. Decidido pelo titular em 2026-10-20.

## Backlog

> Ainda não é certeza. O que separa daqui de `Próximas` é **certeza, não urgência**: demanda certa e sem prioridade já é `Próximas`.
>
> **Item de backlog carrega a condição que o encerra** — "encerra quando houver X". Sem ela o item continua plausível depois de resolvido, e ninguém percebe.

> - ...

- **A listagem de issues corta em 30 sem avisar.** O `gh issue list` devolve no máximo 30 por padrão (`gh issue list --help | grep -- --limit`), e quatro comandos das skills listam sem `--limit` (``grep -rn '`gh issue list --' skills/ | grep -vc -- '--limit'`` → 4, em `skills/midia/issues.md` e `skills/proxima-demanda/SKILL.md`). Num projeto em modo issue com mais de 30 demandas abertas num estado, a próxima demanda e a receita leem só parte delas. Visto na revisão de [o PRD envelhece sem ninguém conferir](concluidas/o-prd-envelhece-sem-ninguem-conferir.md), cujo `/aicf:prd` já passa `--limit 500`. Encerra quando o comando der 0.
- **O aviso de divergência do tracker do Matt confunde pasta com tipo.** O `criar-spec`, o `implementar-spec` e o `fechar-demanda` mandam avisar quando o `docs/agents/issue-tracker.md` "discordar da linha" da mídia (`grep -rn 'discordar da linha' skills/` → 3). Num teste por subagente, o `criar-spec` leu "specs em `.scratch/`" do tracker local do Matt como divergência, num projeto em modo arquivo, e daria um aviso falso. O `implementar-spec` já diz que alinhar é o tipo, não a pasta; os outros dois não. Encerra quando as três frases disserem "tipo, não pasta", ou quando um uso real com tracker local não alinhado passar pelo `criar-spec` sem aviso.
