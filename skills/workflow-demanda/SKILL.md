---
name: workflow-demanda
description: O ciclo de vida de uma demanda — entrevista, implementação, fechamento e registro —, os caminhos disponíveis em cada fase (nativo, Superpowers, Matt Pocock) e as convenções de governança em docs/projeto/. Consultar ao começar, rodar ou fechar uma demanda.
---

# Workflow de uma demanda

O trabalho tem duas camadas. A **governança** registra o que será feito e o que foi feito, e é
sempre a mesma. A **implementação** é como o código sai, e nela há caminhos à escolha.

## O que esta skill não decide

A governança é obrigatória: o registro, o ritual de fechamento e os checks não são negociáveis.
O resto é roteiro, não trilho.

Ferramenta do agente — subagente, plan mode, worktree, code review, busca paralela — é escolha
livre em qualquer ponto, e o agente propõe a que couber sem esperar autorização. Quando sair do
roteiro (pular etapa, trocar de caminho no meio, usar ferramenta que a skill não cita), **dizer
em uma linha o que vai fazer e por quê**, antes de fazer.

Se o roteiro conflitar com o que o caso pede, o caso ganha — e o agente diz que ganhou.

## O ciclo

1. **Demanda** — item do checklist, arquivo em `demandas/`, ou ideia ainda não registrada.
2. **Entrevista** — amadurece a demanda e produz a spec. Demanda que já nasceu de entrevista
   volta à mesa aqui: o agente diz se o registrado basta ou se vale outra rodada.
3. **Implementação** — consome a spec, venha ela de onde vier.
4. **Fechamento** — o ritual de cinco passos, mais abaixo.

**As escolhas de 2 e 3 são independentes e ambas são pergunta ao usuário, não dedução** — dá
para entrevistar por um caminho e implementar por outro. O agente sugere pelo ponto forte que
couber ao caso; a decisão é do usuário, e a resposta vira a linha `Processo:` na demanda.

## Governança — onde mora o quê

`PRD.md` responde o porquê do produto: visão, público, modelo de negócio. O que já foi entregue
e o que falta vive no `CHECKLIST.md`, onde cada item é uma demanda em potencial. Item que
precisa de mais que uma linha vira arquivo em `demandas/`.

```
docs/projeto/
├── PRD.md             # Visão, público, modelo de negócio — o porquê do produto
├── CHECKLIST.md       # O que foi entregue e o que falta (+ seção Backlog)
└── demandas/
    ├── <demanda>.md       # Demanda certa de implementar
    ├── PLANO-<titulo>.md  # Plano ativo (conjunto de demandas)
    ├── concluidas/        # Demandas e planos concluídos
    └── backlog/           # Ainda não está claro que será feita
```

Em andamento: `nome-da-demanda.md`; plano: `PLANO-nome.md`. Ao concluir, adicionar o relatório e
mover para `concluidas/`. O projeto pode divergir dessa estrutura — se houver um `CLAUDE.md` em
`docs/projeto/`, ele manda.

## `demandas/` ou `backlog/` — é certeza, não urgência

O que separa as duas pastas é **o quanto já se sabe sobre a ideia**, não quando será feita.
`demandas/` é o que já foi decidido fazer, mesmo que não seja agora; `backlog/` é o que ainda
não se sustenta, depende de decisão não tomada, ou o usuário nem sabe se quer. Ideia que nunca
sai do backlog é uso legítimo da pasta.

Isso importa mais quando a ideia surge no meio de outra demanda: registrar o esboço, escolher a
pasta pelo critério acima e voltar imediatamente ao que estava sendo feito.

## Entrevista — produz a spec

Demanda que ainda é esboço não vai direto para a implementação: é entrevistada primeiro, e a
entrevista termina escrevendo a spec.

| Caminho         | Como                                | A spec fica em                                         |
| --------------- | ----------------------------------- | ------------------------------------------------------ |
| **Nativo**      | `/aicf:criar-spec`                  | `demandas/<nome>.md`                                   |
| **Superpowers** | `brainstorming`                     | `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md` |
| **Matt Pocock** | `grill-with-docs`, depois `to-spec` | issue no tracker                                       |

No Matt os dois passos são separados: `grill-with-docs` interroga e vai gravando glossário e
ADRs pelo caminho, mas quem escreve e publica a spec é `to-spec`.

## Implementação — consome a spec

Entrada de qualquer caminho é a spec, esteja ela em `demandas/`, em `docs/superpowers/specs/` ou
numa issue. Pular a entrevista é legítimo quando a demanda já diz o suficiente — aí o que a
implementação consome é ela como está, e a linha `Processo:` fica sem seta.

| Caminho              | Como                                                    | Plano de implementação                          |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| **Nativo direto**    | `/aicf:implementar-spec`                                | depende do agente                               |
| **Nativo plan mode** | plan mode ligado, depois `/aicf:implementar-spec`       | depende do agente                               |
| **Superpowers**      | `writing-plans`, depois `subagent-driven-development`   | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` |
| **Matt Pocock**      | `to-tickets`, depois `implement`                        | tickets, com bloqueio declarado entre eles      |

Descer a tabela troca velocidade por rastro: nos caminhos nativos o plano vive na sessão e morre
com ela; nos outros dois fica em arquivo ou ticket.

Plan mode liga com `Shift+Tab` **antes** de chamar a skill, e `Ctrl+G` abre o plano no editor
para ajustar antes de aprovar. As skills do Matt (`to-spec`, `to-tickets`, `triage`,
`wayfinder`, `code-review`) exigem `/setup-matt-pocock-skills` rodado no repositório.

## Registrar o caminho na demanda

Logo abaixo do título, na forma `entrevista → implementação`. **Sem seta significa que não houve
entrevista.** Quando os dois lados vêm do mesmo processo com pipeline próprio, basta o nome
dele; quando o processo publica fora do repositório, a linha carrega as referências — issue
fechada não se perde, mas não aparece em `grep` nem em `git log -S`.

```
Processo: nativo-direto
Processo: nativo → nativo-plan
Processo: grill-with-docs → nativo-plan
Processo: mattpocock — issues #12, #13, #14
```

## Trabalho recorrente não é demanda

Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir (publicar
conteúdo, subir versão, disparar email, liberar acesso) vira **skill** ou **command** em
`.claude/`, não demanda. Gatilho: o mesmo passo a passo explicado pela terceira vez, e ainda vai
ser preciso de novo — quando acontecer, propor a criação.

## Relatório de implementação

Ao concluir, adicionar `## Relatório de implementação (YYYY-MM-DD)` no fim do arquivo, antes de
arquivar. Documenta como a demanda foi resolvida **de fato**, não como foi planejada — registrar
divergências plano×entrega. É para quem **não viveu a implementação**: sem narrativa cronológica
nem detalhes de conversa.

- **Status** — concluído / parcial / bloqueado, com o CI run ou PR que valida
- **Causa raiz** (se bug) — o que estava errado de fato, e o que a execução revelou
- **Arquivos alterados** — os principais, uma linha cada
- **Commits** — hashes e mensagens, incluindo fixes parciais e revertidos
- **Validação** — comandos executados, runs de CI, testes manuais
- **Escopo efetivo** — se o fix afetou mais coisas que a demanda previa
- **Lições** (opcional) — armadilhas, hipóteses erradas, diffs dev/prod

## Ritual de fechamento — o agente aplica proativamente

Antes de escrever o relatório, confirmar que a mudança funciona: rodar o script de check do
projeto (lint + format + typecheck) **no projeto inteiro, nunca só nos arquivos tocados**, e
propor revisão de código quando a mudança for além de ajuste de texto — por `/code-review`, por
um subagente fresco que não viu a implementação, ou pelo code review do próprio harness. Reler o
próprio diff na mesma sessão é a opção mais fraca: o agente defende o que acabou de escrever.

Não importa por onde a demanda começou, ela termina sempre nos mesmos cinco passos:

1. **Relatório** no arquivo da demanda. Se a demanda não tinha arquivo, criar agora.
2. **Mover** para `concluidas/`.
3. **Marcar `- [x]`** no checklist ou no PLANO.
4. **Reler o próprio relatório procurando o que vale além desta demanda** — decisão que outra
   sessão vai reencontrar, armadilha que vai morder de novo, ID ou caminho externo. Promover em
   vez de deixar enterrado, porque ninguém abre demanda concluída procurando informação. Quatro
   destinos: conhecimento operacional → doc de referência do projeto; regra que muda como o
   agente age → `CLAUDE.md`; decisão difícil de reverter, surpreendente e com trade-off real →
   ADR em `docs/adr/`, numerado (`0001-slug.md`) e imutável; termo do domínio que ficou ambíguo →
   glossário em `CONTEXT.md`.

   Os dois últimos moram nos caminhos que as skills do Matt esperam, mas **não dependem delas**:
   quem escreve é `/domain-modeling`, que o agente invoca por conta própria em qualquer processo.
5. **Conferir se a execução criou item novo no checklist/PLANO ou tornou algum obsoleto**, e
   ajustar inline.

O fechamento vai num commit próprio, separado do commit de código. Quando o processo escolhido
já commitou por conta própria, o commit de fechamento cobre só o registro. Ao final, avaliar o
peso do contexto e sugerir `/clear` se estiver pesado — não a cada demanda por reflexo.

## Tarefa pequena

Ajuste pontual, fix trivial, mudança de copy, renomeação: cabe num commit pequeno, e a demanda
pode nascer já no fechamento — o relatório registra o que foi feito e o arquivo vai direto para
`concluidas/`.

## Checklists e PLANOs multi-demanda

O checklist e os PLANOs (`demandas/PLANO-*.md`) consolidam várias demandas. O ideal é cada
demanda rodar em **sessão própria**, com `/clear` ou `/compact` entre elas — não é regra rígida.

**Cada demanda no doc deve ser auto-contida** (Problema, Solução, DoD): a próxima sessão lê o
doc, escolhe a demanda, executa. O _porquê_ das decisões mora no doc, não na conversa. A
**Origem** da leva fica no cabeçalho do plano, uma vez.

## Prompt para a próxima sessão

Quando o usuário pedir o prompt para a próxima demanda (para copiar após `/clear`), entregar
**cercado por uma linha só com `---` acima e outra abaixo**, sem rótulos nem cercas de código —
e com **linha em branco logo depois do `---` de cima e logo antes do de baixo**, senão o markdown
transforma a última linha em título e come o delimitador.

O corpo é autocontido: contexto, o que ler, escopo, fora de escopo, skills obrigatórias, checks,
DoD, branch, ritual de fechamento. A próxima sessão, fria, deve executar lendo só ele e os
arquivos que ele mandar ler.
