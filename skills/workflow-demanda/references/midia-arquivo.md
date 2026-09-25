# Mídia do registro: arquivos em `docs/projeto/`

A receita do modo arquivo, operação por operação. O que é comum às mídias — a linha de
configuração, os quatro estados, "um item, um lugar", o que não muda com a mídia — está no
`/aicf:workflow-demanda`.

## Operação por operação

| Operação | Comando |
| --- | --- |
| Gravar demanda incerta | `docs/projeto/backlog/<nome>.md`, ou linha no `ROADMAP.md` → Backlog |
| Gravar demanda decidida | `docs/projeto/intents/<nome>.md`, ou linha no `ROADMAP.md` → Próximas |
| Gravar demanda que já nasce pronta | `docs/projeto/specs/<nome>.md` |
| Triar issue aberta por alguém de fora, aceita | vira arquivo em `backlog/` ou `intents/`, com `Origem: #<n>` na linha abaixo da `Processo`; depois `gh issue close <n> --comment "<permalink>"`, com o permalink no sha do commit que criou o arquivo (`/blob/<sha>/...`), que não quebra quando o arquivo muda de pasta |
| Triar issue aberta por alguém de fora, recusada | `gh issue close <n> --reason "not planned" --comment "<motivo>"` |
| Virar spec | `git mv docs/projeto/intents/<nome>.md docs/projeto/specs/` e reescrever; se era linha do `ROADMAP.md`, a linha sai |
| Ler a demanda | `cat docs/projeto/specs/<nome>.md` |
| Listar um estado | `head -qn1 docs/projeto/specs/*.md \| sed 's/^# //'` |
| Listar os três estados abertos | o mesmo `head`, com as três pastas |
| Gravar o relatório | no fim do arquivo da demanda |
| Concluir | `git mv` para `docs/projeto/concluidas/` |
| Referenciar outra demanda | link relativo, **sempre** `[título](../<pasta>/<nome>.md)` — inclusive para arquivo da mesma pasta |
| Corrigir referências após mover | `grep -rn '<nome-do-arquivo>' --include='*.md' .` |

**As quatro pastas são irmãs.** `backlog/`, `intents/`, `specs/` e `concluidas/` ficam no mesmo
nível sob `docs/projeto/`, e é isso que faz o `../<pasta>/<nome>.md` da tabela continuar resolvendo
depois de um `git mv` — o arquivo muda de pasta sem mudar de profundidade. Link para irmão da mesma
pasta escrito como `[título](<nome>.md)` **quebra**, porque a pasta de origem deixa de conter o
alvo; daí a forma ser sempre com `../`.

**Mover quebra link — no sentido de quem aponta para o arquivo.** `git mv` de `intents/` para
`specs/`, e de `specs/` para `concluidas/`, muda o caminho que outras demandas, ADRs e o
`CHANGELOG.md` citam. O `grep` acima acha todos; rodar depois de cada `git mv`, antes de commitar.
O sentido contrário — os links que **saem** do arquivo movido — não precisa de comando: são os
`../<pasta>/` que as pastas irmãs mantêm de pé.

A linha `Processo` fica logo abaixo do título; o formato é o do `/aicf:fechar-demanda`.
