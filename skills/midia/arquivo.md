# Mídia do registro: arquivos em `docs/projeto/`

A receita do modo arquivo, operação por operação.

## Os quatro estados

| Estado | Onde |
| --- | --- |
| Backlog — incerto, nem se sabe se será feito | `backlog/<nome>.md`, ou linha em `ROADMAP.md` → Backlog |
| Intent — decidido, ainda não entrevistado | `intents/<nome>.md`, ou linha em `ROADMAP.md` → Próximas |
| Spec — pronta para implementar | `specs/<nome>.md` |
| Concluída | `concluidas/<nome>.md`, com o relatório no fim |

O estado se decide por **certeza, não urgência**: decidido é o que já se resolveu fazer, mesmo que
não seja agora; incerto é o que ainda não se sustenta.

**Um item, um lugar.** Enquanto a demanda não tem arquivo ela é uma linha no `ROADMAP.md`; quando
vira arquivo, a pasta é o registro inteiro e **a linha sai do roadmap**.

## Operação por operação

| Operação | Comando |
| --- | --- |
| Gravar demanda incerta | `docs/projeto/backlog/<nome>.md`, ou linha no `ROADMAP.md` → Backlog |
| Gravar demanda decidida | `docs/projeto/intents/<nome>.md`, ou linha no `ROADMAP.md` → Próximas |
| Gravar demanda que já nasce pronta | `docs/projeto/specs/<nome>.md` |
| Triar issue aberta por alguém de fora, aceita pelo usuário | vira arquivo em `backlog/` ou `intents/`, com `Origem: #<n>` num parágrafo próprio abaixo da linha `Processo`; commit e `git push` do arquivo, e só então `gh issue close <n> --comment "$(gh browse <caminho-do-arquivo> --commit=$(git rev-parse HEAD) -n)"` — o link no sha não quebra quando o arquivo muda de pasta |
| Triar issue aberta por alguém de fora, recusada pelo usuário | `gh issue close <n> --reason "not planned" --comment "<motivo>"` |
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

## Alinhar o tracker do Matt

Chamada pelo `/aicf:criar-spec` (entrevista pelo `grill-with-docs`) e pelo
`/aicf:implementar-spec` (caminho do Matt escolhido). Faz o `to-tickets` deixar a spec em
`docs/projeto/specs/` e abrir cada ticket com a linha que leva até ela, para que o `/implement`
numa sessão limpa chegue à spec só pelo ticket.

Vale só com `docs/agents/issue-tracker.md` apontando para markdown local (`.scratch/`). Arquivo
ausente, ou apontando para outro tracker: esta operação não roda.

**Conferir**, em `docs/agents/issue-tracker.md` — a convenção está presente só quando as quatro dão
o esperado:

```bash
grep -c 'docs/projeto/specs' docs/agents/issue-tracker.md                           # ≥ 1
grep -c '\*\*Spec:\*\*' docs/agents/issue-tracker.md                                 # ≥ 1
grep -c '\.scratch/<feature-slug>/spec\.md\|Issues and specs' docs/agents/issue-tracker.md  # 0
grep -c 'Spec não: vai para' docs/agents/issue-tracker.md                           # ≥ 1
```

**Faltando alguma, propor com o diff só a troca que falta, e aplicar com o aceite do usuário.**
Cada troca é de uma frase do arquivo do Matt, que traz crases e marcador de lista como abaixo; o
resto do arquivo — wayfinding, tickets, mapas — fica como está:

| Frase do Matt | Passa a ser |
| --- | --- |
| ``Issues and specs for this repo live as markdown files in `.scratch/`.`` | Os tickets deste repositório moram em `.scratch/`; a spec de cada feature é a da demanda do aicf, em `docs/projeto/specs/<nome>.md`. |
| ``- The spec is `.scratch/<feature-slug>/spec.md` `` | - A spec é a da demanda, em `docs/projeto/specs/<nome>.md`. Todo ticket abre, logo abaixo do título, com `**Spec:** docs/projeto/specs/<nome>.md`, com o caminho real da demanda. A linha é obrigatória mesmo onde a skill manda evitar caminho de arquivo: ela aponta a spec, não a implementação. |
| ``Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).`` | a mesma frase, mais: "Spec não: vai para `docs/projeto/specs/<nome>.md`." |

Tracker convertido pela metade — à mão, por exemplo — recebe só a troca que falta: a primeira
conferência cobre a abertura, a segunda a linha `**Spec:**` da frase da spec, a terceira acusa a
frase antiga que sobrou, e a quarta a frase de publicação.
Rodar `/setup-matt-pocock-skills` de novo regrava o arquivo e apaga a convenção; a próxima chamada
desta operação a repõe.
