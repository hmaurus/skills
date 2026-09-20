# O bullet do planejamento macro ignora o `wayfinder` do Matt

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (prosa em dois READMEs; recorte e redações decididos aqui, e a versão não muda)

## Problema

A seção "Por que este" do `README.md` tem três bullets do que fica de fora das coleções vizinhas. O
do **planejamento macro** diz que só o `brainstorming` do Superpowers trata pedido grande demais
para uma spec, que ele "trabalha o primeiro subprojeto e os outros ficam na conversa", e conclui
que ter registro próprio para ideia ainda não madura é do aicf. O parágrafo logo acima dele diz que
as duas coleções "simplesmente começam na ideia já formulada".

O `wayfinder` do Matt Pocock existe exatamente para esse caso, e tem os dois mecanismos. Os
comandos abaixo usam `W=$R/skills/skills/engineering/wayfinder/SKILL.md`, no sha `c55ee46` de
`mattpocock/skills`:

- Para que serve: "Plan a huge chunk of work (more than one agent session can hold) as a shared map
  of decision tickets on your issue tracker" — "A loose idea has arrived, too big for one agent
  session, and wrapped in fog" (`sed -n 1,8p $W`).
- Onde a ideia não madura espera: a seção `## Not yet specified` do mapa — "everything here is in
  scope, just not sharp enough to ticket … it doubles as a signpost for collaborators reading where
  the effort is headed" (`grep -n 'Not yet specified' $W`).

As duas frases do README afirmam o contrário, em absoluto, e um leitor que usa o `wayfinder`
derruba a comparação inteira.

**O recorte que torna as frases verdadeiras é esforço × projeto**, não "tem" × "não tem":

- O `wayfinder` planeja **um esforço**, e o destino é o que o define: "The destination varies per
  effort, and naming it is the first act of charting" (`sed -n 9p $W`).
- O mapa acaba quando aquele destino fica alcançável: "the map is done when the way is clear, with
  nothing left to decide before someone goes and does the thing" (`sed -n 13p $W`).
- O que ficou fora não fica esperando o próximo: "it returns only if the destination is redrawn,
  and then as a fresh effort, not a resumption" (`sed -n 99p $W`).
- Nada no arquivo liga um mapa ao seguinte:
  `grep -nic 'across efforts\|between efforts\|multiple maps\|previous map' $W` devolve `0`. É esse
  comando que encerra a afirmação se a skill ganhar o mecanismo.

O aicf registra **o projeto**: `intents/` e `backlog/` existem fora de qualquer demanda, e o PRD diz
o que ficou fora do produto, não de um esforço. É por isso que o Matt marca PARCIAL no critério 2 da
pesquisa [governança macro nos frameworks vizinhos](../../referencias/governanca-nos-frameworks-vizinhos.md),
e é o `wayfinder` que sustenta esse parcial — o mecanismo existe, o alcance é outro.

A pesquisa já registrou isto no item 6 da seção de achados. A demanda
[a comparação com os vizinhos erra e ignora o GSD](concluidas/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md)
corrigiu três frases nomeadas na spec dela; esta é uma quarta, achada na revisão de código do
fechamento daquela, em 2026-09-20.

## Solução

- [ ] **O parágrafo de abertura para de dizer "começam na ideia já formulada".** No `README.md`,
      "Três coisas ficam de fora, e nenhuma das duas declara que são problema de outra pessoa:
      elas simplesmente começam na ideia já formulada e terminam no commit ou no merge" passa a
      "Três coisas ficam de fora, e nenhuma das duas declara que são problema de outra pessoa —
      elas param no esforço: começam num pedido já recortado, por maior que ele seja, e terminam no
      commit ou no merge."
- [ ] **O bullet do planejamento macro ganha a ressalva do `wayfinder`, no fim.** Depois de "tem
      lugar para esperar sem se perder": "O `wayfinder` do Matt chega perto: mapeia um pedido grande
      demais para uma sessão e tem `Not yet specified` para a ideia que ainda não dá para ticketar.
      O mapa é de um esforço e acaba com ele; o que sobra volta como esforço novo, não como fila que
      atravessa o projeto."
- [ ] **O `wayfinder` entra na seção "Comandos vizinhos que valem conhecer"**, na subseção "Antes de
      escrever a demanda", entre `grill-me` e `domain-modeling`: "`wayfinder` (Matt) — mapeia um
      pedido grande demais para uma sessão como tickets de decisão no seu tracker, e resolve um por
      vez. Use quando o caminho até o resultado ainda não está visível. O mapa é daquele esforço."
      **Sem ressalva sobre `disable-model-invocation`**: o `grill-with-docs`, que fica na mesma
      subseção, e `to-spec`, `to-tickets` e `implement`, logo abaixo, também o têm — a flag não
      distingue o `wayfinder` de quem já está na lista
      (`grep -l 'disable-model-invocation' $R/skills/skills/engineering/*/SKILL.md | xargs -n1 dirname | xargs -n1 basename`
      devolve nove nomes, entre eles esses quatro).
- [ ] **O `README.en.md` acompanha, seção por seção** (`grep -c '^## ' README.md README.en.md`
      devolve o mesmo número). As três redações em inglês:
      "— they stop at the effort: they start from a request that is already bounded, however large,
      and end at the commit or the merge"; "Matt's `wayfinder` comes close: it maps a request too
      big for one session and has `Not yet specified` for the idea that cannot be ticketed yet. The
      map belongs to one effort and ends with it; what is left over returns as a fresh effort, not
      as a queue that outlives it."; e "`wayfinder` (Matt) — maps a request too big for one session
      as decision tickets on your tracker, and resolves them one at a time. Use it when the way to
      the result is not visible yet. The map belongs to that effort."
- [ ] **A versão não muda.** A `0.21.0` ainda não foi publicada — sem push e sem tag
      (`git tag -l v0.21.0` vazio) —, e as duas demandas mexem na mesma seção. Esta vira um bullet
      novo na entrada `0.21.0` do `CHANGELOG.md`, e o `.claude-plugin/plugin.json` fica em `0.21.0`.

## Arquivos e interfaces

- `README.md` — o parágrafo acima dos três bullets, o bullet "O planejamento macro", e a subseção
  "Antes de escrever a demanda" da seção "Comandos vizinhos que valem conhecer".
- `README.en.md` — os três lugares equivalentes.
- `CHANGELOG.md` — bullet novo na entrada `0.21.0`, que ainda não foi publicada.
- `.claude-plugin/plugin.json` — **não muda**.
- `docs/referencias/governanca-nos-frameworks-vizinhos.md` — a fonte; não muda nesta demanda.

## Fora de escopo

- **Varrer a seção de novo contra o Matt.** A revisão de código de `a94322a` já leu a seção inteira
  contra os quatro repositórios nos shas pinados, conferiu a paridade PT × EN e achou exatamente
  duas imprecisões: a primeira foi corrigida naquele commit e a segunda é esta demanda. Nada aponta
  para uma terceira, e repetir a varredura é pagar duas vezes pela mesma leitura.
- **Conferir a seção "Comandos vizinhos que valem conhecer" inteira.** Ela descreve oito comandos de
  terceiros e nunca passou por conferência contra o código-fonte — é demanda própria, do tamanho da
  pesquisa de 2026-09-19, e não cabe junto com três parágrafos. Esta demanda acrescenta uma linha
  ali e confere só a linha que acrescenta.
- **Reescrever o bullet inteiro** trocando "elas não têm" por "o alcance é outro". Foi considerado
  na entrevista: fica mais curto no resultado, mas mexe em texto que a revisão não acusou, e o
  acréscimo no fim já diz o que precisa ser dito.
- **Mexer no `CLAUDE.md`.** A regra sobre afirmação de terceiro já recebeu a lição desta linhagem
  no fechamento anterior; aqui não há regra nova.

## Verificação

1. `grep -n 'começam na ideia já formulada' README.md` e
   `grep -n 'start at an idea that is already formed' README.en.md` não devolvem nada.
2. `grep -c 'wayfinder' README.md README.en.md` devolve pelo menos 2 em cada — a ressalva no bullet
   e a linha em "Comandos vizinhos".
3. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois.
4. Cada afirmação nova sobre o `wayfinder` tem o comando que a confere nesta spec, e o comando foi
   **rodado** no clone de `mattpocock/skills` no sha `c55ee46` — não só citado. O bloco de clone
   está na [pesquisa](../../referencias/governanca-nos-frameworks-vizinhos.md).
5. `./scripts/check.sh` termina em `Tudo verde.`, e `0.21.0` continua sendo a versão do
   `plugin.json` e a entrada do topo do `CHANGELOG.md`.
