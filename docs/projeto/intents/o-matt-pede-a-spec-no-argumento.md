# O caminho do Matt pede a spec no argumento

Processo — entrevista: a definir · implementação: a definir

Desde [o agente não oferece o caminho do Matt](../concluidas/o-agente-nao-oferece-o-caminho-do-matt.md),
o aicf entrega `/implement docs/projeto/specs/<nome>.md .scratch/<feature>/issues/<NN>-<slug>.md`,
com dois argumentos, no modo arquivo. No Matt padrão, `/implement` recebe só o ticket. O uso fica
diferente do que a documentação dele ensina, e o próprio agente oscila. Num projeto privado que
consome estas skills, depois de um `/to-tickets` rodado pelo usuário, o agente sugeriu primeiro o
comando só com o ticket e, na pergunta seguinte, o comando com os dois. A regra mora no
`/aicf:implementar-spec`, que não está carregado quando o usuário conduz o Matt direto.

A ideia é devolver o uso padrão do Matt: `/implement <ticket>`, com o ticket levando à spec.

## O que já se sabe

- **Por que a spec foi para o argumento.** O parecer do Codex sobre aquela demanda
  (`docs/agente-codex/revisoes/revisao-spec-o-agente-nao-oferece-o-caminho-do-matt.md`) apontou que
  o ticket local do `to-tickets` não referencia a spec. Hoje a mesma frase está no passo 3 do
  `implementar-spec`: "o ticket local não a referencia e uma sessão nova perderia os pontos de
  teste".
  - O modelo de ticket local do `to-tickets` não tem referência à spec. A seção `Parent` só existe
    no modelo de issue remota:
    `grep -c '^## Parent' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/to-tickets/SKILL.md` → 1.
  - No Matt padrão, a spec não precisa de referência porque mora ao lado dos tickets:
    `grep -c 'The spec is `.scratch' …/setup-matt-pocock-skills/issue-tracker-local.md` → 1.
    O aicf tirou a spec do `.scratch/` e a levou para `docs/projeto/specs/`, e o que ligava ticket e
    spec era só a pasta comum.
  - O `implement` não manda ler o tracker:
    `grep -ci 'issue tracker' …/engineering/implement/SKILL.md` → 0. Ele trabalha sobre "the
    spec or tickets" que o usuário descreve.
  - `grep -c 'levam a spec junto' skills/implementar-spec/SKILL.md` → 1.
- **O modo issue não precisava dos dois argumentos.** O ticket remoto já nasce com `## Parent`
  apontando a issue da spec, então `/implement #<ticket>` chega à spec sozinho. Os dois argumentos
  só compensam o modo arquivo.
- **O `docs/agents/issue-tracker.md` é do Matt, e o aicf não o escreve.** O setup do aicf só o lê
  para propor a mídia (`grep -c 'issue-tracker.md' skills/setup/SKILL.md` → 1). No projeto privado,
  o arquivo foi editado à mão depois da `0.37.0`: a linha "A spec é `.scratch/<feature-slug>/spec.md`"
  virou "a spec é a da demanda, em `docs/projeto/specs/<nome>.md`, passada no argumento do
  `/to-tickets` e do `/implement`". A linha nova manteve os dois argumentos.
- **Os tickets do projeto privado já trazem a referência por conta própria.** Cada ticket abre com
  `**Spec:** <caminho da spec> (seções …)`, sem regra que o mande. O `to-tickets` copiou o formato
  dos tickets anteriores.

## Proposta a amadurecer

O que liga ticket e spec deixa de ser a pasta e passa a ser uma linha no ticket:

- no modo arquivo, a convenção do tracker diz que a spec da feature é
  `docs/projeto/specs/<nome>.md` e que todo ticket abre com a linha `Spec:` apontando para ela. O
  `to-tickets` grava a linha porque segue o tracker; ao buscar um ticket, quem o lê lê também a spec
  da linha;
- a linha "Agent skills" do `CLAUDE.md`, que é lido em toda sessão, ganha meia frase com a mesma
  regra, porque o `implement` não abre o tracker;
- os comandos entregues voltam ao do Matt: `/to-tickets docs/projeto/specs/<nome>.md` e
  `/implement .scratch/<feature>/issues/<NN>-<slug>.md`. No modo issue, `/to-tickets #<n>` e
  `/implement #<ticket>`;
- quem ajusta o `docs/agents/issue-tracker.md` é o aicf: o setup, quando o arquivo existe e a mídia
  é arquivo, e uma nota de migração para os projetos que já rodaram o setup.

## Em aberto para a entrevista

- **O `to-spec` gravar direto em `docs/projeto/specs/`.** O titular quer o `to-spec` como opção
  manual na entrevista do Matt: o tracker diria que a spec publicada vai para
  `docs/projeto/specs/<nome>.md`, e não para `.scratch/`. O que pesa contra, da demanda anterior:
  - o `to-spec` proíbe caminho de arquivo (`grep -c 'Do NOT include specific file paths'
    …/to-spec/SKILL.md` → 1);
  - ele não escreve a linha `Processo`, de que o `implementar-spec` e o `fechar-demanda` dependem,
    nem a Verificação, nem faz o `git mv` do intent.

  Duas specs de formatos diferentes na mesma pasta é o gatilho de revisão "dois mecanismos
  coexistindo". Saídas possíveis:
  - o tracker manda o `to-spec` acrescentar a linha `Processo` e seguir a receita da mídia, mas ele
    tem o próprio modelo de spec;
  - o `/aicf:criar-spec` continua sendo o único que grava, e o ganho do `to-spec` vem pela
    [seção de histórias](../intents/a-spec-nao-tem-historias-para-o-matt.md);
  - o `to-spec` grava, e o `/aicf:criar-spec #<arquivo>` adota a spec e a completa, como já adota a
    issue no modo issue.

  Decidir junto com aquela intent.
- **O nome da pasta do `.scratch/` igual ao nome da spec.** Ajudaria a achar uma pela outra, mas a
  linha `Spec:` já resolve. E a spec troca de nome quando a demanda se renomeia: no projeto privado,
  o arquivo da spec manteve um nome antigo depois que o título mudou.
- **A spec muda de pasta no fechamento.** Ela vai de `specs/` para `concluidas/`, e a linha `Spec:`
  dos tickets quebra. Opções: o `fechar-demanda` corrige a linha com o `grep` de referências, que já
  roda depois do `git mv`; ou a linha fica parada, porque ticket fechado não se reabre.
- **Verificação de comportamento:** numa sessão nova, rodar `/implement` só com o caminho do ticket
  e conferir no transcript que o agente leu a spec antes do primeiro teste. Contraprova: um ticket
  sem a linha `Spec:` não leva o agente à spec.
