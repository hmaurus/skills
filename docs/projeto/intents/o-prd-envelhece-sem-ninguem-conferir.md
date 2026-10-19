# O PRD envelhece sem ninguém conferir

Processo — entrevista: a definir · implementação: a definir

O PRD se diz "documento vivo" (`skills/setup/templates/prd.md`), mas nada no ciclo confere se ele
continua verdadeiro. O `/aicf:criar-prd` já tem um **modo revisão** (`grep -c 'modo revisão'
skills/criar-prd/SKILL.md` → 2), só que ele lê o PRD e entrevista o que o usuário diz ter mudado:
não confronta o texto com o que foi implementado, com as demandas abertas nem com os ADRs. E o nome
"criar" não sugere a quem quer atualizar o PRD que é ali que se faz isso.

Decidido (titular, 2026-10-19): passa a existir um caminho para pedir ao agente uma atualização do
PRD — por sugestão do usuário ou depois de um tempo sem mexer nele —, que **lê o projeto antes de
perguntar** e entrevista o usuário só no que o projeto não responde.

## O que já se sabe

- **Caso de origem, num projeto privado que consome estas skills.** O PRD tinha sido revisado 13
  dias antes, e o desenvolvimento andou mais rápido que ele. O titular decidiu adiantar itens que o
  PRD lista como "fora do MVP", e o PRD ainda trazia um risco com data já vencida. O
  `/aicf:proxima-demanda` usa o PRD como régua da prioridade (`grep -n 'PRD' skills/proxima-demanda/SKILL.md`),
  então um PRD defasado leva a uma ordem errada. Quem percebeu foi o titular, não o ciclo.
- **O que o agente pode conferir sozinho**, sem perguntar:
  - item de **Escopo** cuja demanda já está em `concluidas/`, ou que ainda não tem demanda nenhuma;
  - item de **Fora** que voltou ao `ROADMAP.md`, a uma intent ou a uma spec;
  - **Riscos** com data ou condição que já passou;
  - **Público** e **Modelo** contra o `GLOSSARY.md` e os ADRs (termo trocado, decisão de modelo
    registrada fora do PRD);
  - a data de **Última revisão** contra o histórico do git (`git log --since=<data> --oneline --
    docs/projeto/concluidas/`).
- **O que só o usuário responde:** se a mudança de escopo foi decisão ou deriva, o motivo de um item
  novo em Fora, e as metas de Sucesso.
- **O `criar-prd` só o usuário invoca** (`disable-model-invocation: true`). Pela regra do
  `.claude/CLAUDE.md`, o agente não verifica o comportamento dele: a mudança entra com a verificação
  em aberto até um uso real do titular.
- Nenhuma skill do ciclo cita o PRD no fechamento (`grep -c 'PRD' skills/fechar-demanda/SKILL.md`
  → 0): uma demanda que contraria o PRD fecha sem aviso.

## Em aberto para a entrevista

- **Skill nova ou modo do `criar-prd`.** Sugestão do agente: reforçar o modo revisão que já existe,
  com um passo que lê o projeto antes da primeira pergunta, em vez de criar `atualizar-prd` ao lado.
  Duas skills para o mesmo arquivo são dois mecanismos para a mesma coisa. O custo da sugestão é o
  nome: decidir se o comando passa a se chamar outra coisa (`/aicf:prd`?) ou se a descrição basta
  para quem procura "atualizar".
- **Quem dispara.** Só o usuário, como hoje, ou o agente também pode sugerir. Candidatos: o
  `/aicf:fechar-demanda`, quando a demanda contraria o PRD; o `/aicf:proxima-demanda`, quando a
  última revisão é mais antiga que N demandas concluídas.
- **Invocação pelo modelo.** Se o agente puder rodar a atualização sozinho, o
  `disable-model-invocation` sai, e o comportamento passa a ser verificável pelo agente.
- **Formato da saída.** O diff do PRD proposto seção por seção, com a fonte de cada mudança
  (arquivo da demanda, ADR, commit), antes de gravar.
