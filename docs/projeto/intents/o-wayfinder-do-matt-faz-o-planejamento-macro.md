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
afirmam o contrário. É por esforço e não por produto — o mapa morre com o esforço, e não há nada
que atravesse esforços —, mas a frase como está é absoluta e um leitor que usa o `wayfinder`
derruba a comparação inteira.

A pesquisa [governança macro nos frameworks vizinhos](../../referencias/governanca-nos-frameworks-vizinhos.md)
já registrou isto no item 6 da seção de achados. A demanda
[a comparação com os vizinhos erra e ignora o GSD](../specs/concluidas/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md)
corrigiu três frases nomeadas na spec e esta é uma quarta, achada na revisão de código do
fechamento dela, em 2026-09-20 — fora do escopo daquela, registrada aqui.

## O que falta decidir

- Se o bullet ganha a ressalva do `wayfinder` (como o bullet do nível do produto ganhou a do
  `triage`), ou se o parágrafo de abertura é que precisa parar de dizer "começam na ideia já
  formulada".
- Se o `wayfinder` também entra na seção "Comandos vizinhos que valem conhecer", que hoje não o
  cita — ele é o comando do Matt para a fase que o aicf chama de planejamento macro.
- O `README.en.md` acompanha seção por seção.

**Encerra quando** o `README.md` e o `README.en.md` não afirmarem mais que o registro de ideia
ainda não madura é exclusivo do aicf, ou quando a afirmação vier com o recorte que a torna
verdadeira.
