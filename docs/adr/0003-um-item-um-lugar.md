# 0003 — Um item, um lugar

Data: 2026-09-14 · Status: aceita · Versão: `0.16.0` · **Supersede o [0002](0002-conferencia-do-indice-por-inclusao.md)**

## Decisão

**Uma demanda existe num lugar só.** Enquanto não tem arquivo, é uma linha em
`docs/projeto/ROADMAP.md`; quando vira arquivo, a pasta é o registro inteiro e a linha sai do
roadmap. Não há índice que espelhe pastas, e por isso não há conferência de índice no fechamento.

## Por quê

O ADR 0002 decidiu que a conferência do índice corre num sentido só — todo arquivo tem linha, o
inverso não é exigido. Essa assimetria não era detalhe de implementação: era a declaração de que a
pasta é a fonte e o `CHECKLIST.md`, uma cópia derivada mantida à mão.

Cópia manual não detecta erro na fonte. Ela fabrica uma classe de erro nova — a cópia divergir — e
depois gasta ritual achando o erro que ela mesma criou. O argumento de "detecção por duplicação"
só vale quando as duas fontes chegam à realidade por caminhos independentes, como na partida
dobrada; aqui só havia um caminho, com a pasta de um lado e a transcrição dela do outro.

O 0002 continua correto sobre o que decidiu — apenas o objeto dele deixou de existir.

## Consequências

- O que a demanda 0002 protegia (item entregue apagado em vez de movido) deixa de ser detectável e
  deixa de ser possível: sem linha a manter, não há como o arquivo e o índice discordarem.
- O índice legível volta gerado, com os títulos reais em vez dos slugs:
  `head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'`.
- Perde-se a leitura offline de "em que pé está o projeto" num arquivo só. Quem clona sem rede tem
  o `PRD.md`, o `ROADMAP.md` e as pastas.
- Perde-se a ordem de prioridade entre demandas que já têm arquivo. As dependências continuam na
  prosa de cada uma ("bloqueia", "habilita", "depende de"), onde sobrevivem a renomeação.
- Reverter significaria recriar o `CHECKLIST.md`, o passo que o marca e o passo que o confere, nas
  seis skills e nos dois READMEs.
