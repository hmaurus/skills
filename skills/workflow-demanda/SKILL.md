---
name: workflow-demanda
description: O ciclo de vida de uma demanda — entrevista, implementação, fechamento e registro —, os caminhos de cada fase e as convenções de governança em docs/projeto/. Consultar ao começar, rodar ou fechar uma demanda.
---

# Workflow de uma demanda

O trabalho tem duas camadas. A **governança** — registro, ritual de fechamento e checks — é
obrigatória e sempre a mesma. A **implementação** é roteiro, não trilho: se o caso pedir outra
coisa, o caso ganha. Ao sair do roteiro (pular etapa, trocar de caminho no meio, usar ferramenta
que a skill não cita), **dizer em uma linha o que vai fazer e por quê**, antes de fazer.
Ferramenta do agente — subagente, plan mode, worktree, code review, busca paralela — é escolha
livre em qualquer ponto, e o agente propõe a que couber sem esperar autorização.

## O ciclo

**Demanda** (item do checklist, arquivo em `demandas/`, ou ideia ainda não registrada) →
**entrevista**, que produz a spec → **implementação**, que a consome → **fechamento**. Demanda
que já nasceu de entrevista volta à mesa: o agente diz se o registrado basta ou se vale outra
rodada. Pular a entrevista é legítimo quando a demanda já diz o suficiente — a implementação a
consome como está, e a linha `Processo:` fica sem seta.

**Entrevista e implementação são escolhas independentes, e ambas são pergunta ao usuário, não
dedução**: o agente sugere pelo ponto forte que couber ao caso, e a resposta vira a linha
`Processo:` na demanda.

## Governança — onde mora o quê

```
docs/projeto/
├── PRD.md             # Visão, público, modelo de negócio — o porquê do produto
├── CHECKLIST.md       # O entregue e o que falta (+ Backlog); cada item é uma demanda em potencial
└── demandas/
    ├── <demanda>.md       # Item que precisa de mais que uma linha no checklist
    ├── PLANO-<titulo>.md  # Plano ativo (conjunto de demandas)
    ├── concluidas/        # Demandas e planos concluídos, com relatório
    └── backlog/           # Ainda não está claro que será feita
```

Se houver um `CLAUDE.md` em `docs/projeto/`, ele manda sobre essa estrutura. Se o repositório
nem tem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

`demandas/` ou `backlog/` se decide por **certeza, não urgência**: `demandas/` é o que já foi
decidido fazer, mesmo que não seja agora; `backlog/` é o que ainda não se sustenta, depende de
decisão não tomada, ou o usuário nem sabe se quer — ideia que nunca sai de lá é uso legítimo.
Importa mais quando a ideia surge no meio de outra demanda: registrar o esboço, escolher a pasta
e voltar imediatamente ao que estava sendo feito.

## Entrevista — produz a spec

| Caminho         | Como                                | A spec fica em                                         |
| --------------- | ----------------------------------- | ------------------------------------------------------ |
| **Nativo**      | `/aicf:criar-spec`                  | `demandas/<nome>.md`                                   |
| **Superpowers** | `brainstorming`                     | `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md` |
| **Matt Pocock** | `grill-with-docs`, depois `to-spec` | issue no tracker                                       |

No Matt, `grill-with-docs` interroga e grava glossário e ADRs pelo caminho, mas quem escreve e
publica a spec é `to-spec`; emendando direto no `implement`, a spec não vira arquivo nem issue —
fica só na janela de contexto.

## Implementação — consome a spec

| Caminho              | Como                                                    | Plano de implementação                          |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| **Nativo direto**    | `/aicf:implementar-spec`                                | depende do agente                               |
| **Nativo plan mode** | plan mode ligado, depois `/aicf:implementar-spec`       | depende do agente                               |
| **Superpowers**      | `writing-plans`, depois `subagent-driven-development`   | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` |
| **Matt Pocock**      | `to-tickets`, depois `implement`                        | tickets, com bloqueio declarado entre eles      |

Descer a tabela troca velocidade por rastro: nos caminhos nativos o plano vive na sessão e morre
com ela. Plan mode liga com `Shift+Tab` **antes** de chamar a skill (`Ctrl+G` abre o plano no
editor). As skills do Matt (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`)
exigem `/setup-matt-pocock-skills` rodado no repositório.

## Registrar o caminho na demanda

Logo abaixo do título, na forma `entrevista → implementação`; **sem seta significa que não houve
entrevista**. Processo com pipeline próprio dos dois lados leva só o nome dele; processo que
publica fora do repositório carrega as referências na linha — issue fechada não se perde, mas não
aparece em `grep` nem em `git log -S`.

```
Processo: nativo-direto
Processo: grill-with-docs → nativo-plan
Processo: mattpocock — issues #12, #13, #14
```

## Trabalho recorrente não é demanda

Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir (publicar
conteúdo, subir versão, disparar email, liberar acesso) vira **skill** ou **command** em
`.claude/`. Gatilho: o mesmo passo a passo explicado pela terceira vez — quando acontecer, propor
a criação.

## Fechamento — o agente aplica proativamente

Antes do relatório, rodar o script de check do projeto (lint + format + typecheck) **no projeto
inteiro, nunca só nos arquivos tocados**, e propor revisão de código quando a mudança for além de
ajuste de texto — `/code-review`, subagente fresco que não viu a implementação, ou o code review
do harness. Reler o próprio diff na mesma sessão é a opção mais fraca: o agente defende o que
acabou de escrever.

Não importa por onde a demanda começou, ela termina sempre nos mesmos cinco passos:

1. **Relatório** no arquivo da demanda. Se a demanda não tinha arquivo, criar agora.
2. **Mover** para `concluidas/`.
3. **Marcar `- [x]`** no checklist ou no PLANO.
4. **Reler o próprio relatório procurando o que vale além desta demanda** — decisão que outra
   sessão vai reencontrar, armadilha que vai morder de novo, ID externo — e promover, porque
   ninguém abre demanda concluída procurando informação: conhecimento operacional → doc de
   referência; regra que muda como o agente age → `CLAUDE.md`; decisão difícil de reverter,
   surpreendente e com trade-off real → ADR numerado e imutável em `docs/adr/` (`0001-slug.md`);
   termo ambíguo do domínio → glossário em `CONTEXT.md`. Os dois últimos saem de
   `/domain-modeling`, que o agente invoca em qualquer processo — não depende das skills do Matt.
5. **Conferir se a execução criou item novo no checklist/PLANO ou tornou algum obsoleto**, e
   ajustar inline.

O fechamento vai num commit próprio, separado do commit de código; quando o processo escolhido já
commitou por conta própria, cobre só o registro. Tarefa pequena (fix trivial, copy, renomeação)
cabe num commit, e a demanda pode nascer já no fechamento: o relatório registra o que foi feito
e o arquivo vai direto para `concluidas/`. Ao final, avaliar o peso do contexto e sugerir
`/clear` se estiver pesado — não a cada demanda por reflexo.

### O relatório

`## Relatório de implementação (YYYY-MM-DD)` no fim do arquivo. Documenta como a demanda foi
resolvida **de fato**, não como foi planejada — registrar divergências plano×entrega. É para quem
**não viveu a implementação**: sem narrativa cronológica nem detalhes de conversa.

- **Status** — concluído / parcial / bloqueado, com o CI run ou PR que valida
- **Causa raiz** (se bug) — o que estava errado de fato, e o que a execução revelou
- **Arquivos alterados** — os principais, uma linha cada
- **Commits** — hashes e mensagens, incluindo fixes parciais e revertidos
- **Validação** — comandos executados, runs de CI, testes manuais
- **Escopo efetivo** — se o fix afetou mais coisas que a demanda previa
- **Lições** (opcional) — armadilhas, hipóteses erradas, diffs dev/prod

## Checklists e PLANOs multi-demanda

O checklist e os PLANOs (`demandas/PLANO-*.md`) consolidam várias demandas — o ideal, sem ser
regra rígida, é cada uma rodar em **sessão própria**, com `/clear` ou `/compact` entre elas.
**Cada demanda no doc é auto-contida** (Problema, Solução, DoD): a próxima sessão lê o doc,
escolhe, executa. O _porquê_ das decisões mora no doc, não na conversa; a **Origem** da leva
fica no cabeçalho do plano, uma vez.

## Prompt para a próxima sessão

Quando o usuário pedir o prompt para a próxima demanda (para copiar após `/clear`), entregar
**cercado por uma linha só com `---` acima e outra abaixo**, sem rótulos nem cercas de código, e
com **linha em branco entre cada `---` e o corpo** — senão o markdown transforma a última linha
em título e come o delimitador.

O corpo é autocontido: contexto, o que ler, escopo, fora de escopo, skills obrigatórias, checks,
DoD, branch, ritual de fechamento. O teste: a próxima sessão, fria, executa lendo só ele e o que
ele mandar ler — sem impedi-la de investigar mais se achar que precisa.
