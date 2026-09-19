# Mídia do registro: arquivos em `docs/projeto/`

A receita do modo arquivo, operação por operação. O que é comum às mídias — a linha de
configuração, os quatro estados, "um item, um lugar", o que não muda com a mídia — está no
`/aicf:workflow-demanda`.

## Operação por operação

| Operação | Comando |
| --- | --- |
| Gravar demanda incerta | `docs/projeto/intents/backlog/<nome>.md`, ou linha no `ROADMAP.md` → Backlog |
| Gravar demanda decidida | `docs/projeto/intents/<nome>.md`, ou linha no `ROADMAP.md` → Próximas |
| Gravar demanda que já nasce pronta | `docs/projeto/specs/<nome>.md` |
| Virar spec | `git mv docs/projeto/intents/<nome>.md docs/projeto/specs/` e reescrever; se era linha do `ROADMAP.md`, a linha sai |
| Ler a demanda | `cat docs/projeto/specs/<nome>.md` |
| Listar um estado | `head -qn1 docs/projeto/specs/*.md \| sed 's/^# //'` |
| Listar os três estados abertos | o mesmo `head`, com as três pastas |
| Gravar o relatório | no fim do arquivo da demanda |
| Concluir | `git mv` para `docs/projeto/specs/concluidas/` |
| Referenciar outra demanda | link relativo — `[título](../intents/<nome>.md)` |
| Corrigir referências após mover | `grep -rn '<nome-do-arquivo>' --include='*.md' .` |

**Mover quebra link.** `git mv` de `intents/` para `specs/`, e de `specs/` para `concluidas/`,
muda o caminho que outras demandas, ADRs e o `CHANGELOG.md` citam. O `grep` acima acha todos; rodar
depois de cada `git mv`, antes de commitar.

A linha `Processo` fica logo abaixo do título; o formato é o do `/aicf:fechar-demanda`.
