# O agente não vê o que só o mapa diz sobre a entrevista por outra coleção

Processo — entrevista: a definir · implementação: a definir

Desde a `0.31.0`, o mapa (`/aicf:ajuda`) só carrega quando o usuário o chama. Três coisas sobre
entrevistar por outra coleção ficaram sem lugar que o agente leia:

- parar na fronteira `brainstorming` → `writing-plans` é legítimo, e o design doc vale como spec
  (`grep -n 'parar na fronteira' skills/ajuda/SKILL.md` → 1);
- só o caminho _architectural_ do `brainstorming` grava arquivo, e ele honra o local que o
  `CLAUDE.md` mandar;
- emendar o `to-spec` direto no `implement` deixa a spec só na janela de contexto.

As duas últimas saíram de vez com a tabela de entrevista:
`grep -rn '_architectural_\|janela de contexto' skills CLAUDE.md` → nada, contra 3 linhas em
`git show 0b3ce9a:skills/workflow-demanda/SKILL.md | grep -c '_architectural_\|janela de contexto'`.
Achado pela revisão de [o mapa pesa em toda demanda](../concluidas/o-mapa-pesa-em-toda-demanda.md).

> **Encerra quando** uma entrevista pelo Superpowers ou pelo Matt, com a `0.31.0` ou posterior, mostrar
> o agente tropeçando num desses pontos — e aí a regra vai para a linha da entrevista no
> `CLAUDE.md` — ou quando a entrevista concluir que o próprio framework já conduz certo e arquivar
> este arquivo em `concluidas/` com o motivo.
