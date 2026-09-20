# O bullet do planejamento macro ignora o `wayfinder` do Matt

Processo — entrevista: a definir · implementação: a definir

## Problema

A seção "Por que este" do `README.md` tem três bullets do que fica de fora das coleções vizinhas. O
do **planejamento macro** diz que só o `brainstorming` do Superpowers trata pedido grande demais
para uma spec, que ele "trabalha o primeiro subprojeto e os outros ficam na conversa", e conclui
que ter registro próprio para ideia ainda não madura é do aicf.

O `wayfinder` do Matt Pocock existe exatamente para esse caso, e tem os dois mecanismos:

- Para que serve: "Plan a huge chunk of work (more than one agent session can hold) as a shared map
  of decision tickets on your issue tracker" — "A loose idea has arrived, too big for one agent
  session, and wrapped in fog"
  (`sed -n 1,8p $R/skills/skills/engineering/wayfinder/SKILL.md`, sha `c55ee46`).
- Onde a ideia não madura espera: a seção `## Not yet specified` do mapa — "everything here is in
  scope, just not sharp enough to ticket … it doubles as a signpost for collaborators reading where
  the effort is headed" (`grep -n 'Not yet specified' $R/skills/skills/engineering/wayfinder/SKILL.md`).

O mesmo bullet, e o parágrafo acima dele ("elas simplesmente começam na ideia já formulada"),
afirmam o contrário. A frase como está é absoluta, e um leitor que usa o `wayfinder` derruba a
comparação inteira.

**O recorte que torna a frase verdadeira é esforço × projeto**, não "tem" × "não tem". Os comandos
abaixo usam `W=$R/skills/skills/engineering/wayfinder/SKILL.md`, no sha `c55ee46`:

- O `wayfinder` planeja **um esforço**, e o destino é o que o define: "The destination varies per
  effort, and naming it is the first act of charting" (`sed -n 9p $W`).
- O mapa acaba quando aquele destino fica alcançável: "the map is done when the way is clear, with
  nothing left to decide before someone goes and does the thing" (`sed -n 13p $W`).
- O que ficou fora não fica esperando o próximo: "it returns only if the destination is redrawn,
  and then as a fresh effort, not a resumption" (`sed -n 99p $W`).
- Nada no arquivo liga um mapa ao seguinte:
  `grep -nic 'across efforts\|between efforts\|multiple maps\|previous map' $W` devolve `0`. É
  esse comando que encerra a afirmação se a skill ganhar o mecanismo.

O aicf registra **o projeto**: `intents/` e `backlog/` existem fora de qualquer demanda, e o PRD
diz o que ficou fora do produto, não de um esforço. É por isso que o Matt marca PARCIAL no critério
2 da pesquisa, e é o `wayfinder` que sustenta esse parcial — o mecanismo existe, o alcance é outro.
Uma redação que troque "o aicf tem, o Matt não" por "o alcance é outro" fica verdadeira sem perder
o argumento.

A pesquisa [governança macro nos frameworks vizinhos](../../referencias/governanca-nos-frameworks-vizinhos.md)
já registrou isto no item 6 da seção de achados. A demanda
[a comparação com os vizinhos erra e ignora o GSD](../specs/concluidas/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md)
corrigiu três frases nomeadas na spec e esta é uma quarta, achada na revisão de código do
fechamento dela, em 2026-09-20 — fora do escopo daquela, registrada aqui.

## O que falta decidir

- Se o bullet ganha a ressalva do `wayfinder` (como o bullet do nível do produto ganhou a do
  `triage`), ou se o parágrafo de abertura é que precisa parar de dizer "começam na ideia já
  formulada". O recorte a aplicar já está decidido acima; o que falta é onde ele entra e em quantas
  palavras.
- Se o `wayfinder` também entra na seção "Comandos vizinhos que valem conhecer", que hoje não o
  cita — ele é o comando do Matt para a fase que o aicf chama de planejamento macro.
- O `README.en.md` acompanha seção por seção.

**Encerra quando** o `README.md` e o `README.en.md` pararem de afirmar que o registro de ideia
ainda não madura é exclusivo do aicf — seja porque a frase saiu, seja porque passou a dizer que o
que muda é o alcance, esforço contra projeto. Enquanto
`grep -n 'ainda não amadureceu\|has not matured' README.md README.en.md` devolver a frase antiga
nos dois, a demanda está aberta.
