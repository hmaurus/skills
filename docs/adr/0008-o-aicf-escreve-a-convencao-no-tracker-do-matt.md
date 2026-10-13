# 0008 — O aicf escreve a convenção da spec no tracker do Matt

Data: 2026-10-12 · Status: aceita · Versão: `0.38.0`

## Decisão

No modo arquivo, o aicf **edita** o `docs/agents/issue-tracker.md` do Matt Pocock, com o aceite do
usuário, para que a spec da feature seja a da demanda, em `docs/projeto/specs/<nome>.md`, e todo
ticket do `to-tickets` abra com a linha `**Spec:** docs/projeto/specs/<nome>.md`.

**O que se escreve:** só três frases do arquivo que o `/setup-matt-pocock-skills` grava — a
abertura (`Issues and specs … live in .scratch/`), a localização da spec com a linha `Spec:` e a
exceção à regra "avoid specific file paths" do `to-tickets`, e a operação de publicação. As
operações de wayfinding, os tickets e os mapas seguem em `.scratch/`, intocados. No modo issue nada
se escreve: o ticket remoto já nasce com `## Parent` apontando a issue da spec
(`grep -n '^## Parent' …/mattpocock-skills/1.3.1/skills/engineering/to-tickets/SKILL.md` → linha 86).

**Quando:** pela operação "Alinhar o tracker do Matt" do `skills/midia/arquivo.md`, chamada de dois
pontos — o fim do `/aicf:criar-spec` com entrevista pelo `grill-with-docs`, e o
`/aicf:implementar-spec` quando o caminho do Matt é escolhido. Ela confere antes e propõe com o diff
só o que falta. O `/aicf:setup` não a chama.

## Por quê

O [0004](0004-midia-do-registro-e-config-propria.md) diz que o aicf **lê** o `issue-tracker.md` e
não depende dele. Escrever nele é relação nova, e só se justifica porque a alternativa não chega a
quem precisa: o `/implement` numa sessão limpa só lê o ticket, e o ticket local do `to-tickets` não
referencia a spec, que o aicf tirou de `.scratch/<feature-slug>/spec.md`. Até a `0.37.0` a regra
"passe a spec junto no argumento" morava no `/aicf:implementar-spec`, que não está carregado quando
o usuário conduz o Matt direto; num projeto privado que consome estas skills, o agente sugeriu o
comando só com o ticket.

A edição troca as frases em vez de acrescentar ao lado: acrescentar deixaria o tracker se
contradizendo sobre onde a spec mora, e a linha `Spec:` contrariaria o "avoid specific file paths"
do `to-tickets`
(`grep -n 'avoid specific file paths' …/mattpocock-skills/1.3.1/skills/engineering/to-tickets/SKILL.md`
→ linha 105) se ninguém dissesse que ela é exceção.

O setup não a chama porque costuma rodar antes do setup do Matt, quando o arquivo ainda não existe,
e roda uma vez; as duas chamadas cobrem projeto novo, projeto antigo e tracker regravado.

## Consequências

- **Rodar `/setup-matt-pocock-skills` de novo regrava o arquivo e apaga a convenção.** O Matt só
  pede isso para trocar de tracker ou recomeçar
  (`grep -n 're-running this skill' …/mattpocock-skills/1.3.1/skills/engineering/setup-matt-pocock-skills/SKILL.md`
  → linha 116), e a próxima chamada da operação a repõe.
- **A troca exata depende do texto de três frases do Matt `1.3.1`.** Se o Matt mudar essas frases,
  a terceira conferência deixa de achar a localização antiga, mas a segunda (`**Spec:**` ≥ 1)
  continua falhando enquanto a linha não estiver lá, e a operação propõe o que falta, adaptando a
  troca à frase nova.
- **Reverter** é tirar a operação do `midia/arquivo.md` e voltar os comandos de dois argumentos no
  `/aicf:implementar-spec`; os trackers já editados ficam com a convenção, que não atrapalha o Matt.
