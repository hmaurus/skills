# A governança orquestra o framework escolhido, não o substitui

Processo — entrevista: a definir · implementação: a definir

## Problema

Na primeira execução de ponta a ponta com três coleções instaladas no mesmo projeto — aicf na
governança, Superpowers na implementação, Matt Pocock disponível —, o agente **pulou o
encerramento do framework** por ler uma garantia do aicf como exclusão.

O caso: `hmaurus/mh-fin`, demanda de finanças pessoais. Entrevista pelo `/aicf:criar-spec`,
implementação pelo `superpowers:writing-plans` + `subagent-driven-development` (16 tarefas, 40
commits, 141 testes), fechamento pelo `/aicf:fechar-demanda`. O `subagent-driven-development`
termina em `finishing-a-development-branch`, que é a skill que **decide a integração** do código
— merge na base, PR, ou manter a branch. O agente não a rodou, porque o `implementar-spec` diz:

> esta skill para aqui e o caminho escolhido assume, e o fechamento continua sendo
> `/aicf:fechar-demanda`

Essa frase é uma **garantia** — o fechamento de governança sobrevive à escolha de qualquer
caminho. Foi lida como **exclusão**: "só o aicf fecha". O agente ainda invocou a regra "instrução
do usuário vence skill" para um caso em que não havia conflito nenhum: fabricou um.

**Sintoma verificável:** a demanda foi dada por concluída com `main` 40 commits atrás de
`develop`, e a decisão de integração nunca foi tomada, nem feita, nem registrada como pendente.
Ela só aconteceu depois, quando o titular percebeu a falta.

**A raiz é textual, não só de julgamento.** A palavra "fechamento" cobre duas coisas diferentes
nos documentos do aicf: fechar o *branch* (integração do código) e fechar a *demanda* (relatório,
mover spec, checklist, promoção de conhecimento). Enquanto uma palavra só nomear as duas, a
leitura errada continua disponível para o próximo agente.

Duas costuras menores apareceram na mesma execução:

- **A decisão de branch/worktree foi arbitrada sem avaliação.** O `subagent-driven-development`
  manda garantir workspace isolado; o `CLAUDE.md` do projeto manda commitar direto na branch de
  trabalho. O agente aplicou o default do projeto e chamou de decisão. O resultado foi certo, mas
  por sorte: worktree teria sido errado ali por um motivo que ninguém avaliou — a verificação de
  seis tarefas dependia de estado local **não versionado** (o SQLite e o `regras.json` em `data/`,
  que é gitignored), e uma worktree nasceria vazia.

- **O `scripts/task-brief` do `subagent-driven-development` só entende plano em inglês.** Ele
  procura heading `^#+ Task N`; plano em pt-BR usa "Tarefa N" e o script responde
  `task N not found`. Como o aicf recomenda documentação em português, isso reaparece em todo
  plano do Superpowers, e o agente teve que escrever um extrator próprio no meio da execução.

## O que já está decidido, e não é assunto de entrevista

Decisão do titular, tomada ao revisar a execução:

1. **Rodar o método de implementação escolhido inteiro, e só depois a governança.** As skills de
   governança do aicf **complementam e orquestram** os frameworks para conviverem no mesmo
   projeto — não substituem o encerramento de nenhum deles. A ordem é: encerramento do método
   escolhido → `/aicf:fechar-demanda`.

2. **Commitar direto na branch de trabalho continua o default** — é o processo prático para dev
   solo, e PR fica para o que a complexidade ou o risco justificarem. Mas a governança **deve
   avaliar** o caso, em vez de herdar o default em silêncio: branch própria ou worktree quando a
   demanda é grande ou se quer poder descartá-la em bloco; **contra worktree** quando a
   verificação depende de estado local não versionado.

## O que a entrevista precisa decidir

- **Onde cada ajuste mora.** O `implementar-spec` (que produziu a frase mal lida), o
  `fechar-demanda` (que descreve o ritual), o `workflow-demanda` (que é o mapa), ou os três.
- **Como nomear as duas coisas hoje chamadas de "fechamento"**, para a ambiguidade não voltar.
  Provavelmente vocabulário fixo, do jeito que um glossário faz.
- **Como evitar pagar dobrado quando os dois processos pedem o mesmo passo.** O `fechar-demanda`
  exige revisão por subagente fresco; o `subagent-driven-development` já faz a revisão ampla do
  branch no fim. Nesta execução o agente usou uma para satisfazer a outra e rodou uma vez só — se
  a regra virar literal sem ressalva, o próximo roda duas revisões de branch inteiro. Falta
  decidir o mecanismo: o relatório declara qual exigência da governança foi satisfeita por qual
  passo do framework?
- **A avaliação de branch/worktree é pergunta ao usuário ou decisão do agente com critério
  registrado?** E em qual momento do ciclo ela acontece.
- **O que fazer com a linha do `fechar-demanda`** que diz que ADR e glossário "saem de
  `/domain-modeling`, que o agente invoca em qualquer processo": na execução real o agente
  escreveu os dois ADRs direto pela tabela de promoção, sem invocar nada. Ou vira passo explícito,
  ou afrouxa para "consultar quando ajudar" — do jeito que está, descreve um comportamento que não
  aconteceu.
- **Se o problema do `task-brief` é assunto do aicf.** Ele é um script de outra coleção. As saídas
  possíveis: avisar no template do `setup`, entregar um extrator próprio, ou considerar fora de
  escopo e apenas documentar.

## Fora de escopo

- Mudar as skills do Superpowers ou do Matt Pocock. O aicf orquestra o que existe; não mantém
  coleção de terceiro.
- Reabrir a escolha entre commitar direto e PR. O default está decidido acima.

## Referências

- Execução que originou a demanda: `hmaurus/mh-fin`, spec em
  `docs/projeto/specs/concluidas/financas-pessoais-meu-pluggy.md` (seção Lições).
- Aprendizado completo, com os três problemas e as três soluções, no cerebro:
  `referencias/aprendizados.md`, entrada de 2026-09-08.
