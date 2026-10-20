# O ponteiro antigo só se troca na revisão

Processo — entrevista: nenhuma · implementação: aicf-direto

Achado depois do fechamento de [o PRD envelhece sem ninguém conferir](o-prd-envelhece-sem-ninguem-conferir.md),
ao explicar ao titular quando o cabeçalho do PRD troca `/aicf:criar-prd` por `/aicf:prd`.

## Problema

Na `0.40.0`, a regra que troca o ponteiro estava só na lista do modo revisão do `/aicf:prd`. Um
projeto que fez o setup antes da `0.40.0` e nunca preencheu o PRD entra em modo criação, que não
lê aquela lista, e o cabeçalho copiado do template antigo podia ficar com o nome que não existe
mais.

## Solução

A frase sai da lista do modo revisão e vai para *Onde ele fica*, que o agente lê nos dois modos.
O grupo Fato deixa de citar "ponteiro".

## Relatório de implementação (2026-10-19)

- **Status** — concluído.
- **Arquivos alterados** — `skills/prd/SKILL.md` (a frase muda de seção);
  `.claude-plugin/plugin.json` (`0.40.1`); `CHANGELOG.md` (entrada `0.40.1`).
- **Commits** — `d4a0d53` fix(prd): 0.40.1 — o ponteiro antigo do cabeçalho se troca também na
  criação.
- **Validação** — `./scripts/check.sh` → `Tudo verde.`;
  `grep -n 'Nos dois modos' skills/prd/SKILL.md | wc -l` → 1; `grep -c 'Ponteiro antigo'
  skills/prd/SKILL.md` → 0. Sem revisão de código: a mudança move uma frase. O comportamento da
  `/aicf:prd` segue em aberto como na demanda anterior (`disable-model-invocation: true`), e
  encerra no primeiro uso real num projeto com o PRD ainda no template antigo.
- **Promovido** — nada.
