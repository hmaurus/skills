# O critério de caminho ignora a presença do usuário e o porte

Processo — entrevista: a definir · implementação: a definir

O [`caminhos.md`](../../../skills/implementar-spec/caminhos.md) escolhe o caminho de implementação
só pela forma da demanda: se cabe numa sessão, se tem abordagem a decidir, se as fatias dependem
umas das outras. Não pergunta se o usuário vai acompanhar a implementação
(`grep -ciE 'ausente|autonom|dorm|presen' skills/implementar-spec/caminhos.md skills/implementar-spec/matt.md`
→ 0 e 0). Também não traz número de porte nem prevê o plan mode com subagentes. Num projeto
privado que consome estas skills, a análise de um mês de demandas mostrou que, na prática, a
escolha passou por essas três coisas. Decidido: o critério passa a considerá-las.

## O que já se sabe

Números de um mês num projeto privado que consome estas skills: 58 demandas concluídas, 535
transcrições de sessão, 977 commits. Uma demanda por caminho no porte grande, então é indício, não
prova.

- **A presença do usuário decidiu mais que a forma da demanda.**
  - As três demandas grandes rodaram de madrugada, com "autônomo até o deploy" no prompt.
  - As 33 sugestões de `aicf-direto` ou `aicf-plan` foram seguidas; 9 das 13 de `to-tickets`.
  - Os 4 desvios foram todos noites de autonomia. Em dois, o agente mandou para o Superpowers
    porque o caminho do Matt exige que o usuário digite os comandos.
  - Num terceiro caso, também de madrugada, o Matt funcionou: o usuário rodou o `/to-tickets` na
    sessão da entrevista e entregou o `/implement-spec` com a autonomia no argumento antes de
    dormir.
- **No porte de ~6.000 linhas, três caminhos, uma demanda cada:**

  | Caminho | Implementação | Subagentes | Contexto processado |
  | --- | --- | --- | --- |
  | `aicf-plan` com fatias delegadas | 172 min | 11 | 213 M tokens |
  | `implement-spec` do Matt | 181 min | 12, até 2 em paralelo | 263 M |
  | `subagent-driven-development` | 267 min | 32 | 226 M |

  - O paralelo do Matt ficou em 2 tickets juntos porque o grafo não deixou mais: o critério de
    hoje (4 ou mais tickets, ao menos 2 prontos ao mesmo tempo) foi atendido e não rendeu ganho.
  - O SDD foi o mais lento, como o `caminhos.md` já avisa
    (`grep -c 'não se sugere para ganhar velocidade' skills/implementar-spec/caminhos.md` → 1).
    O revisor por tarefa pegou cedo uma migration fora da regra do projeto e um desvio da spec, que
    nos outros caminhos só a revisão do fim pegaria.
- **O plan mode virou "plano + subagentes" sem regra.** Numa demanda grande, o agente decidiu
  sozinho, no plano aprovado, delegar uma fatia por subagente, em série, no mesmo checkout. Ele lia
  o diff, rodava o check e commitava cada fatia; um revisor independente fechou. É um SDD sem
  revisor por tarefa, e empatou com o `implement-spec` sem exigir comando do usuário.
- **Plano num contexto só custa 3×.** Outra demanda de porte parecido (162 arquivos), com plano
  único e sem delegar, reprocessou 575 M tokens no agente principal (662 M no total), contra
  213 M da demanda com fatias delegadas.
  - Nas 23 demandas de `aicf-plan` do mês, até ~30 arquivos o contexto único não saiu da curva.
  - No direto, as demandas ficaram em até ~15 arquivos (mediana de 11).
- **O plano aprovado do plan mode some.** O Claude Code o grava em `~/.claude/plans/`, com um nome
  aleatório de três palavras, fora do repositório. O aicf não o cita
  (`grep -rc '\.claude/plans' skills/ | grep -vc ':0'` → 0), e a tabela do `implementar-spec` diz
  "depende do agente" na coluna do plano. No projeto, 31 planos vivem só numa máquina.
- **Dois avisos do `implement-spec` vistos na prática.**
  - Um ticket abriu uma rota sem a trava de permissão, que só o ticket seguinte do grafo fechava;
    a revisão de segurança automática do Claude Code apontou o buraco no meio da execução.
  - Os implementadores não rodam e2e na worktree (a porta do servidor é compartilhada). As quebras
    só aparecem no orquestrador, a cada merge, e as duas do caso eram do teste.
- **Entrevista sem leitura do mecanismo deixa lacuna.** Numa demanda transversal (um aviso para
  vários destinatários, agir em nome de outra conta), o `criar-spec` saiu sem o mecanismo. Foi o
  explorador do `implementar-spec` que achou a lacuna, e ela pediu uma segunda rodada de
  entrevista. As entrevistas pelo `grill-with-docs` do mesmo porte não tiveram esse retorno.
- **Execução autônoma deixa resto.** Em 2 das 3 madrugadas ficaram shells e subagentes abertos ao
  fim: laços de espera com `pgrep -f`, que casam com o próprio comando, e esperas de CI por SHA
  curto, que o `gh run list` devolve vazio. O `fechar-demanda` não fala em segundo plano
  (`grep -ciE 'segundo plano|background' skills/fechar-demanda/SKILL.md` → 0).
- **O que se sustentou e fica.**
  - O passo "conferir o caminho da entrevista" da `0.45.0` sugeriu o `grill-with-docs` duas vezes,
    e o usuário aceitou as duas.
  - O revisor independente do `fechar-demanda` achou de 6 a 9 itens em todos os caminhos, inclusive
    no direto, onde pegou uma migration contra a regra do projeto.
  - O `/to-tickets` na sessão da entrevista funcionou: a conversa ajuda no corte.

## Em aberto para a entrevista

- **Como a presença entra no critério:** pergunta explícita no `criar-spec`, no `implementar-spec`
  ou nos dois; ou leitura do prompt ("autônomo", "vou dormir"). E o que muda em cada caminho com o
  usuário ausente.
- **Número de porte no `caminhos.md`** (~15 arquivos para o direto, ~30 para o plan mode num
  contexto) ou critério qualitativo. Número envelhece com o modelo e a janela de contexto.
- **O plan mode com fatias delegadas:** variante nomeada do `aicf-plan`, valor novo na linha
  `Processo` ou só uma frase no `caminhos.md`. E se a fatia pede revisor, como no SDD.
- **Onde o plano aprovado vai parar:** cópia junto da spec, seção do relatório ou só o nome do
  arquivo e as fatias.
- **Os avisos do `implement-spec`** (trava de permissão no mesmo ticket da rota, e2e só na
  integração): no `matt.md`, na proposta de fatias do `/to-tickets` ou no tracker.
- **A leitura do mecanismo no `criar-spec`:** explorador antes de escrever, ou sugestão do
  `grill-with-docs` quando a demanda é transversal.
- **O resto em segundo plano:** passo do `fechar-demanda`, regra do template do `CLAUDE.md`, ou
  demanda própria.
- **Escopo:** tudo numa demanda ou dividido entre `caminhos.md`, `criar-spec` e `fechar-demanda`.
