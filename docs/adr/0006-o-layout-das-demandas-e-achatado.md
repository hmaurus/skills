# 0006 — O layout das demandas é achatado

Data: 2026-09-20 · Status: aceita · Versão: `0.22.0`

## Decisão

**As quatro pastas de demanda são irmãs**, sob `docs/projeto/`: `backlog/`, `intents/`, `specs/` e
`concluidas/`. Antes, duas delas moravam um nível abaixo — `intents/backlog/` e
`specs/concluidas/`.

A pasta continua sendo o estado, e o [ADR 0003](0003-um-item-um-lugar.md) fica de pé: o que muda é
o aninhamento, não quem é a fonte da verdade.

**A referência entre demandas é sempre `[título](../<pasta>/<nome>.md)`**, inclusive para arquivo
da mesma pasta.

## Por quê

O `git mv` do fechamento mudava de nível, e todo link relativo que **saía** do arquivo movido
passava a resolver errado — `../../adr/` virava `../../../adr/`. O ritual só ensinava o sentido
contrário: o `grep -rn '<nome-do-arquivo>'` do passo 2 acha quem aponta **para** o arquivo movido e
não enxerga nada do que sai dele.

O dano já tinha sido pago no commit `07cb4a9`, que consertou dois links de saída depois que o CI
acusou. Quem pegou foi o `scripts/check_links.py`, que existe **neste** repositório; num projeto
que instala o plugin e não tem check de links, o mesmo `git mv` quebra em silêncio.

A prova de que a profundidade era a causa, e não o movimento: `intents/` → `specs/` é o outro
`git mv` da governança, acontece na mesma frequência e nunca quebrou um link de saída — as duas
pastas já estavam no mesmo nível.

Com as quatro irmãs, o arquivo muda de pasta sem mudar de profundidade, e o sentido de saída deixa
de existir como problema. Sobra o sentido de entrada, que o `grep` de hoje já cobre. Daí a
convenção do `../`: link para irmão da mesma pasta escrito como `[título](<nome>.md)` continuaria
quebrando, porque a pasta de origem deixa de conter o alvo.

**Por que o estado continua na pasta.** A alternativa é a do Matt Pocock, que guarda o estado num
campo do corpo (`Status: claimed` → `Status: resolved`) com o arquivo parado em
`.scratch/<feature>/issues/NN-<slug>.md` — nada se move, e os dois sentidos somem de uma vez.
Descartada: trocaria o `ls` de um estado por `grep`, tiraria "a pasta diz o estado" das skills e
exigiria um ADR que supersedesse o 0003 — preço alto para o sentido que o `grep` já cobre.

## Consequências

- **16 arquivos mudaram de caminho**
  (`ls docs/projeto/backlog/*.md docs/projeto/concluidas/*.md | wc -l`), e os links relativos de
  dentro e de fora deles foram recomputados — 33 só de dentro
  (`grep -rno '](\.\./[^)]*)' docs/projeto/backlog/*.md docs/projeto/concluidas/*.md | wc -l`). A
  conta não é uniforme: de `concluidas/X.md`, `../../../adr/` virou `../../adr/`, mas
  `../a-primeira-tela-...md` virou `../specs/a-primeira-tela-...md`.
- **Os ponteiros dos ADRs anteriores foram reapontados sem o texto mudar.** O
  [0005](0005-a-documentacao-humana-e-um-arquivo-so.md) tem dois links para demandas concluídas;
  mudou só o caminho dentro dos parênteses. O comando `head -qn1` do
  [0003](0003-um-item-um-lugar.md) (linha 29) **não** mudou: é prosa que descreve o repositório da
  época, e o mesmo vale para as entradas antigas do `CHANGELOG.md` e para a prosa das demandas em
  `concluidas/`.
- **Projeto que já instalou o plugin e não migrar continua funcionando.** O plugin é instrução,
  não código: as skills vão falar de uma pasta que lá tem outro nome. As notas da `0.22.0` trazem
  os dois `git mv` e o comando de correção dos links.
- **Reverter** significaria refazer os dois `git mv` no sentido inverso, recomputar os mesmos 46
  links e desfazer a convenção do `../` — que passou a valer também entre irmãos da mesma pasta, e
  é a parte que os projetos consumidores já terão absorvido.
