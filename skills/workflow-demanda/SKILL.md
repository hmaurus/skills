---
name: workflow-demanda
description: O mapa de uma demanda — ciclo, caminhos de entrevista e implementação, convenções de governança e a mídia do registro (arquivos em docs/projeto/, ou issues do GitHub). Consultar ao começar, triar ou registrar uma demanda. O fechamento vive em fechar-demanda.
---

# Workflow de uma demanda

O trabalho tem duas camadas. A **governança** — registro, ritual de fechamento e checks — é
obrigatória e sempre a mesma. A **implementação** é roteiro, não trilho: se o caso pedir outra
coisa, o caso ganha. Ao sair do roteiro (pular etapa, trocar de caminho no meio, usar ferramenta
que a skill não cita), **dizer em uma linha o que vai fazer e por quê**, antes de fazer.
Ferramenta do agente — subagente, plan mode, worktree, code review, busca paralela — é escolha
livre em qualquer ponto, e o agente propõe a que couber sem esperar autorização.

## O ciclo

**Demanda** (registro no estado "decidido" ou "incerto", ou ideia ainda não registrada) →
**entrevista**, que produz a spec → **implementação**, que a consome → **fechamento**, que é
`/aicf:fechar-demanda` — relatório, arquivamento e linha `Processo` vivem lá, e o agente o
aplica em qualquer caminho. Demanda que já nasceu de entrevista volta à mesa: o agente diz se o
registrado basta ou se vale outra rodada. Pular a entrevista é legítimo quando a demanda já diz
o suficiente — a demanda muda de estado para "pronta para implementar" como está, e a linha
`Processo` registra `entrevista: nenhuma`.

**Três palavras, uma unidade de trabalho.** _Demanda_ é a coisa a fazer. _Intent_ e _spec_ são
os dois estados do registro que a descreve: intent é a demanda decidida e ainda não entrevistada;
spec é a demanda pronta para implementar. No modo arquivo, a pasta diz o estado; no modo issue, o
label.

**Integração e fechamento são coisas diferentes.** _Integração_ é decidir o destino do código —
merge na base, PR, ou a branch fica. É o último passo da **implementação**, e pertence ao método
escolhido. _Fechamento_ é o registro da demanda — relatório, conclusão, promoção de
conhecimento. É `/aicf:fechar-demanda`, e nada além. **O método fecha o código, a
governança fecha a demanda — e a segunda só começa depois da primeira.**

**Entrevista e implementação são escolhas independentes. Na entrevista, o caminho é pergunta ao
usuário; na implementação, o agente segue a sugestão gravada na spec quando o caso é óbvio —
caminho aicf direto e diff que cabe numa frase — e pergunta com opções nos demais.** O agente
sugere pelo ponto forte que couber ao caso; a decisão é do usuário quando há escolha real, e o
caminho seguido vira a linha `Processo` na demanda.

**A governança escolhe o caminho de cada fase; dentro da fase, o encadeamento do framework roda
inteiro.** Skill que o método declara como passo seguinte dentro da mesma fase não se pula nem se
substitui — no Superpowers, `executing-plans` e `subagent-driven-development` declaram
`finishing-a-development-branch` como `REQUIRED SUB-SKILL`: ela roda automaticamente, sem
perguntar, e o agente conta em uma linha o que ficou decidido. Interferir ali degrada a qualidade
de um processo que não é nosso. Na **passagem entre fases** quem decide é a governança, mesmo
quando o framework recomenda continuar nele: o `brainstorming` declara `writing-plans` como estado
terminal, e ainda assim parar na fronteira é legítimo — o design doc dele vale como spec, e a
implementação é escolha nova.

## Governança — onde mora o quê

**A mídia do registro é escolha do projeto**, declarada numa linha do `CLAUDE.md`, na seção
"Processos de desenvolvimento":

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

`grep -m1 'Mídia do registro' CLAUDE.md` lê a escolha. **Linha ausente significa arquivo** —
compatibilidade com projeto anterior a essa escolha existir.
Os comandos concretos estão no arquivo da mídia que a linha nomeia —
[`references/midia-arquivo.md`](references/midia-arquivo.md) ou
[`references/midia-issues.md`](references/midia-issues.md); uma terceira mídia seria um terceiro
arquivo.

A governança é a mesma nas duas. Quatro estados:

| Estado | Modo arquivo | Modo issue |
| --- | --- | --- |
| Incerto — nem se sabe se será feito | `backlog/<nome>.md`, ou linha em `ROADMAP.md` → Backlog | issue aberta, `aicf:backlog` |
| Decidido, ainda não entrevistado | `intents/<nome>.md`, ou linha em `ROADMAP.md` → Próximas | issue aberta, `aicf:intent` |
| Pronta para implementar | `specs/<nome>.md` | issue aberta, `aicf:spec` |
| Concluída | `concluidas/<nome>.md`, com o relatório no fim | issue fechada, com o relatório em comentário |

**Um item, um lugar.** No modo arquivo, enquanto a demanda não tem arquivo ela é uma linha no
`ROADMAP.md`; quando vira arquivo, a pasta é o registro inteiro e **a linha sai do roadmap**. No
modo issue a demanda é **uma issue só, do nascimento ao fechamento** — o label troca, o número não,
e não existe `ROADMAP.md`. Nos dois casos nada aponta para nada, e não sobra índice para envelhecer.

O estado se decide por **certeza, não urgência**: decidido é o que já se resolveu fazer, mesmo que
não seja agora; incerto é o que ainda não se sustenta, depende de decisão não tomada, ou o usuário
nem sabe se quer — ideia que nunca sai de lá é uso legítimo. Importa mais quando a ideia surge no
meio de outra demanda: registrar o esboço, escolher o estado e voltar imediatamente ao que estava
sendo feito.

Um caminho só: toda demanda que vai ser feita vira spec — com entrevista ou sem —, e tudo termina
concluído, inclusive o que a entrevista concluiu não fazer.

Só governança de demanda entra aí, e isso não muda com a mídia. Doc que descreve o mundo em vez de
um trabalho a fazer — configuração, ID externo, decisão de marca, número de negócio, aprendizado —
vai para `docs/referencias/`, criada quando houver o primeiro arquivo. **PRD, ADR e `CONTEXT.md`
ficam em arquivo nos dois modos**; no modo issue, `docs/projeto/` existe com o `PRD.md` dentro, e só
ele. **Não existe modo misto:** a demanda inteira mora numa mídia só, relatório incluído. E o passo 3
do fechamento — promover para o repositório o que vale além da demanda — vale nas duas mídias; é o
que compensa o preço do modo issue, em que o relatório em comentário de issue fechada some do
`git clone`.

Se o repositório não tem a linha de mídia nem `docs/projeto/`, perguntar onde gravar em vez de
inventar pasta.

**O `docs/agents/issue-tracker.md` do Matt Pocock responde a mesma pergunta** — onde o trabalho
mora. O aicf lê para propor o default no setup, e não depende: a linha do `CLAUDE.md` é a única
fonte da verdade dele. Se as duas discordarem, avisar uma vez e seguir a linha — divergir é
legítimo, mas precisa ser escolha, não descoberta tardia. Os labels `aicf:*` classificam maturidade
do documento; os do `/triage` dele, o que fazer em seguida. Eixos diferentes: a mesma issue pode
carregar os dois, e nenhum lado enxerga o do outro.

## Entrevista — produz a spec

| Caminho         | Como                                | A spec fica em                                                                                                      |
| --------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Aicf**        | `/aicf:criar-spec`                  | o registro da própria demanda, no estado "pronta para implementar" — `specs/<nome>.md` no modo arquivo, a issue com `aicf:spec` no modo issue |
| **Superpowers** | `brainstorming`                     | `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md`, só no caminho _architectural_; ou `specs/<nome>.md`, se o projeto mandar |
| **Matt Pocock** | `grill-with-docs`, depois `to-spec` | issue no tracker, adotada por `/aicf:criar-spec #<n>` no modo issue; no modo arquivo, `.scratch/` do Matt, que o aicf não adota |

No Superpowers, só o caminho _architectural_ do `brainstorming` grava arquivo, e ele honra o
local que o `CLAUDE.md` do projeto mandar. No Matt, quem grava a spec é `to-spec`; emendar
direto no `implement` deixa a spec só na janela de contexto.

**No modo issue, `to-spec` publica e `/aicf:criar-spec #<n>` adota.** O `to-spec` cria issue nova e
não edita uma existente, então sem a adoção a mesma demanda terminaria com duas issues — a dele e a
do aicf. Adotada, é uma issue só, com o label do aicf por cima.

## Implementação — consome a spec

| Caminho            | Como                                                       | Plano de implementação                          | Integração                                          |
| ------------------ | ---------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Aicf direto**    | `/aicf:implementar-spec`                                   | depende do agente                               | o agente, pelo critério de workspace abaixo         |
| **Aicf plan mode** | plan mode ligado antes, ou escolhido no `implementar-spec` | depende do agente                               | o agente, pelo critério de workspace abaixo         |
| **Superpowers**    | `writing-plans`, depois `subagent-driven-development`      | `docs/superpowers/plans/YYYY-MM-DD-<topico>.md` | `finishing-a-development-branch`, encadeada e automática |
| **Matt Pocock**    | `to-tickets`, depois `implement`                           | tickets, com bloqueio declarado entre eles      | o próprio `implement`: `/code-review` e commit na branch atual |

Descer a tabela troca velocidade por rastro: nos caminhos aicf o plano vive na sessão e morre
com ela. As skills do Matt (`to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`)
exigem `/setup-matt-pocock-skills` rodado no repositório.

No Superpowers, os headings de tarefa do plano ficam em inglês (`## Task 3`) mesmo com o corpo em
português: `scripts/task-brief` procura `^#+ Task N` e responde `task N not found` para "Tarefa N".

**Branch, ou worktree.** O default é commitar direto na branch de trabalho — processo prático para
dev solo, com PR para o que a complexidade ou o risco justificarem. O agente **avalia** em vez de
herdar o default em silêncio: branch própria ou worktree quando a demanda é grande ou se quer poder
descartá-la em bloco; **contra worktree quando a verificação depende de estado local não
versionado** — banco, arquivo de dados, `.env`, qualquer coisa em pasta gitignored: a worktree
nasce sem eles. A avaliação acontece no `implementar-spec`, junto da escolha de caminho; o agente
diz numa linha o que decidiu e por quê, e sair do default é pergunta ao usuário.

## Trabalho recorrente não é demanda

Demanda tem começo e fim. Procedimento que se repete enquanto o projeto existir (publicar
conteúdo, subir versão, disparar email, liberar acesso) vira **skill** ou **command** em
`.claude/`. Gatilho: o mesmo passo a passo explicado pela terceira vez — quando acontecer, propor
a criação. Mas skill é conselho que o modelo pode não seguir: regra que precisa valer sem exceção
— formatar após editar, barrar escrita em pasta protegida — é **hook**, script que roda sempre. O
critério é a regra poder falhar sem ninguém perceber.

## Demanda grande, e demandas que andam juntas

Demanda grande demais para uma sessão é **uma spec só**, com as entregas em checkboxes no corpo:
a sessão faz o que cabe e fecha parcial — `/aicf:fechar-demanda` cobre o caso — e a próxima
continua pelo mesmo registro. Várias demandas independentes que andam juntas são **specs
separadas**, e a relação mora na prosa de cada uma — "bloqueia", "habilita", "depende de",
nomeando o outro lado: o arquivo, no modo arquivo; `#<n>`, no modo issue. Não em subpasta, e não
numa lista à parte, que envelheceria. O _porquê_ das decisões mora na demanda, não na conversa.
