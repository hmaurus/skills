# O Matt com e sem o aicf

Leitura da spec [o agente não oferece o caminho do Matt](../projeto/concluidas/o-agente-nao-oferece-o-caminho-do-matt.md),
feita em 2026-10-07 sobre o commit `dfd4606`, antes da implementação. Responde três perguntas: quais
arquivos a spec toca, se ela acopla mais ou menos o aicf às outras coleções, e se o aicf pode
prejudicar o funcionamento do Matt. No fim estão os ajustes sugeridos para a spec. Nenhum foi
aplicado.

As afirmações sobre o Matt valem para `mattpocock-skills` `1.3.1`. Os comandos de conferência partem
de:

```bash
M=~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering
```

## O que a spec muda

Hoje o agente não oferece o Matt, por três causas:

| # | Causa | Mecanismo |
| --- | --- | --- |
| 1 | O agente não enxerga as skills de caminho do Matt | `grill-with-docs`, `to-spec`, `to-tickets` e `implement` têm `disable-model-invocation: true`, ficam fora da lista de skills do agente e não podem ser invocadas por ele |
| 2 | No modo arquivo, a spec do Matt não tem destino | o `to-spec` grava no tracker do Matt (`.scratch/`), que o aicf não adota, e não há regra de passagem como a do `brainstorming` |
| 3 | Falta critério para sugerir o Matt | os pontos fortes de cada caminho só estão no `README.md`, que o agente não lê |

Conferência da causa 1: `grep -l 'disable-model-invocation: true' $M/{grill-with-docs,to-spec,to-tickets,implement}/SKILL.md | wc -l` → 4.

O fluxo proposto:

```
                 ENTREVISTA                          SPEC                      IMPLEMENTAÇÃO
┌──────────────────────────────────┐
│ criar-spec (aicf)                │──┐
│ faltam decisões pontuais         │  │
├──────────────────────────────────┤  │     ┌──────────────────────┐    ┌─────────────────────────────┐
│ brainstorming (Superpowers)      │──┼───▶ │  /aicf:criar-spec    │──▶ │ aicf-direto / aicf-plan     │ cabe em 1 sessão
│ desenho aberto, alternativas     │  │     │  parte do que já foi │    ├─────────────────────────────┤
├──────────────────────────────────┤  │     │  decidido, pergunta  │    │ Superpowers                 │ muitos passos,
│ grill-with-docs (Matt)           │──┘     │  só o que falta      │    │ (o agente executa)          │ subagente + TDD
│ termo ou decisão de domínio      │        │  (tipicamente Testes)│    ├─────────────────────────────┤
│ o agente conduz por grilling +   │        └──────────────────────┘    │ Matt: o agente ENTREGA      │ fatias verticais,
│ domain-modeling                  │          docs/projeto/specs/       │ /to-tickets <spec>          │ várias sessões
└──────────────────────────────────┘                                    │ /implement <spec> <ticket>  │
                                          ✗ .scratch/ (to-spec sai)     │ e o USUÁRIO os digita       │
                                          ✗ docs/superpowers/specs/     └─────────────────────────────┘
```

1. **Toda spec sai pelo `/aicf:criar-spec`**, venha a entrevista de onde vier. Isso inclui o
   `brainstorming`, cuja regra atual manda gravar "pela receita da mídia". A receita diz onde gravar,
   não quais seções a spec tem.
2. **O agente faz do Matt o que pode.** A entrevista ele conduz pelas duas skills que o
   `grill-with-docs` chama, que o agente consegue invocar. O `to-tickets` e o `implement` ele entrega
   como comando, já com a spec no argumento, e o usuário digita.
3. **Cada critério de escolha fica na skill que o aplica.** O de entrevista vai para o template do
   `CLAUDE.md`. O de implementação vai, repetido, para o `criar-spec` e o `implementar-spec`.
4. **O `criar-spec` absorve duas regras do `to-spec`:** ler os ADRs da área tocada e o item
   **Testes** (em que ponto a mudança é testada).

## Arquivos tocados

```
skills/
├── setup/templates/claude-md.md   ← nota "skills do Matt são só do usuário", critério de entrevista,
│                                     regra de passagem cobrindo brainstorming e grill-with-docs
├── criar-spec/SKILL.md            ← ADRs em "Antes de perguntar", parágrafo "entrevista já aconteceu",
│                                     item Testes, critério de implementação (~9 linhas)
├── implementar-spec/SKILL.md      ← linha do Matt: o usuário digita; comandos com a spec junto;
│                                     critério de implementação; tira o to-spec da lista do setup-matt
├── ajuda/SKILL.md                 ← "spec do to-spec fica no .scratch/" → "sai pelo /aicf:criar-spec"
└── midia/issues.md                ← "to-spec cria issue" vira o caso de quem roda /to-spec por conta própria

README.md / README.en.md           ← separa grill-me (não grava) de grill-with-docs (grava glossário e ADR)
.claude/CLAUDE.md                  ← as mesmas 3 mudanças do template
.claude-plugin/plugin.json         ← 0.37.0
CHANGELOG.md                       ← entrada 0.37.0
```

O template não chega sozinho aos projetos que já fizeram o setup. As notas da release precisam
trazer o trecho do `CLAUDE.md` para o titular trocar à mão.

## Acoplamento

A spec aumenta um tipo de acoplamento e reduz outro.

**Aumenta o quanto o aicf sabe do Matt.** Hoje as skills do aicf citam dois nomes do Matt
(`grill-with-docs` e `to-spec`). Depois da mudança, passam a depender destes detalhes:

| O aicf passa a depender de | Fica velho se o Matt… | Conferência em `1.3.1` |
| --- | --- | --- |
| `grill-with-docs` ser `grilling` + `domain-modeling` | mudar a composição ou os nomes | `cat $M/grill-with-docs/SKILL.md` → *"Call the Skill tool twice, for "grilling" and "domain-modeling""* |
| `/to-tickets` aceitar um caminho de spec | mudar a entrada | `grep -n 'If the user passes a reference' $M/to-tickets/SKILL.md` |
| o layout `.scratch/<feature-slug>/issues/<NN>-<slug>.md` | mudar o tracker local | `grep -n 'scratch/<feature-slug>' $M/to-tickets/SKILL.md` |
| `/implement` trabalhar sobre spec ou tickets | restringir a entrada | `grep -n 'spec or tickets' $M/implement/SKILL.md` |
| as quatro skills serem só do usuário | liberá-las para o agente | o `grep -l … wc -l` acima, → 4 |

O aicf também passa a comparar as coleções ("Superpowers quando…, Matt quando…"), e esse critério
precisa acompanhar a evolução das duas.

**Reduz a dependência do formato da spec.** Hoje a spec pode sair do `to-spec`, no formato e na
pasta do Matt, ou de `docs/superpowers/specs/`, no formato do Superpowers. Depois da mudança, a spec é
sempre um arquivo do aicf. Os outros caminhos conversam com o usuário antes e consomem a spec depois.

**Em tempo de execução, nada muda.** A spec rejeita mandar o agente ler o `to-spec` do cache, porque o
caminho muda a cada versão do Matt. O que servia foi copiado (ADRs e Testes), e não referenciado.

**Saldo:** o acoplamento sai do arquivo da spec, onde quebrava em silêncio, e vai para os nomes de
skills e os argumentos de comando, onde fica escrito e pode ser conferido por `grep`. O custo é revisar
o aicf quando o Matt mudar o `to-tickets`, o `implement` ou o layout do `.scratch/`.

## O Matt sozinho e com o aicf

```
MATT SOZINHO (o usuário digita os 4 comandos)
/grill-with-docs ──▶ /to-spec ─────────────────────▶ /to-tickets ──────────▶ /implement
 entrevista,          sintetiza a conversa,           fatias verticais,        /tdd nos seams,
 grava GLOSSARY       NÃO entrevista; só confere      usuário aprova,          /code-review,
 e ADR                os seams; publica no tracker    .scratch/<f>/issues/     commit
                      (.scratch/ ou issue)

MATT COM AICF (proposta da spec)
agente conduz ──────▶ /aicf:criar-spec ────────────▶ usuário digita ────────▶ usuário digita ──▶ /aicf:fechar-demanda
 grilling +           pergunta só o que falta,        /to-tickets <spec>       /implement         relatório, arquivamento,
 domain-modeling      grava em docs/projeto/specs/                             <spec> <ticket>    promoção de conhecimento
```

| Passo | Matt sozinho | Com aicf | Diferença |
| --- | --- | --- | --- |
| Entrevista | `/grill-with-docs` | o agente invoca `grilling` e `domain-modeling` | nenhuma: é o que o `grill-with-docs` faz |
| Spec | `to-spec`: Problem, Solution, User Stories numeradas e extensas, Implementation e Testing Decisions, sem caminho de arquivo | `criar-spec`: Problema, Solução, Arquivos e interfaces nomeados, Testes, Fora de escopo, Verificação | o formato muda e o `to-spec` sai |
| Tickets | `/to-tickets` lê a conversa ou o argumento | `/to-tickets docs/projeto/specs/<nome>.md` | igual |
| Implementação | `/implement` sobre o que o usuário descrever | `/implement <spec> <ticket>` | acrescenta a spec, que o ticket local não referencia |
| Depois | commit | `fechar-demanda` | camada a mais, sem trocar nada do Matt |

O ticket local não tem campo de referência à spec. A seção `Parent` só existe no modelo de issue
remota: `grep -n 'Parent' $M/to-tickets/SKILL.md` aponta só para o `<issue-template>`.

As skills do Matt continuam intocadas. O aicf muda quem digita a entrevista e troca o `to-spec` pelo
`criar-spec`.

## O aicf pode prejudicar o Matt?

Na entrevista, nos tickets e na implementação, não: rodam as mesmas skills, com a mesma entrada ou com
mais entrada. Os riscos estão no passo da spec, do mais ao menos sério:

1. **Reentrevistar o usuário.** Esse é o risco principal. O `to-spec` proíbe entrevistar:
   `grep -n 'Do NOT interview' $M/to-spec/SKILL.md`. O `criar-spec` foi feito para entrevistar. Se o
   parágrafo novo ("partir do decidido, perguntar só o que falta") ficar fraco, o usuário sai de um
   grill exaustivo para uma segunda rodada de perguntas. A Verificação 3 da spec não testa isso: ela
   confere onde a spec foi parar, não quantas perguntas se repetiram.
2. **Saem as user stories.** O `to-spec` pede uma lista longa:
   `grep -n 'extremely extensive' $M/to-spec/SKILL.md`. A spec justifica o corte porque nenhuma skill
   de implementação do Matt as lê. Mas o `to-tickets` fatia por comportamento *"from the user's
   perspective"* (`grep -n "user's perspective" $M/to-tickets/SKILL.md`), e as stories são
   matéria-prima para isso. Em demanda pequena não faz diferença. Em demanda grande, que é o caso em
   que a spec recomenda o Matt, o fatiamento pode ficar mais pobre. Ainda não foi medido.
3. **Entram caminhos de arquivo.** O Matt os proíbe porque envelhecem:
   `grep -n 'Do NOT include specific file paths' $M/to-spec/SKILL.md`. O argumento do aicf é que a
   spec vive pouco, mas no caso do Matt (várias sessões) ela vive mais. O efeito é limitado, porque o
   `to-tickets` também tira os caminhos dos tickets.
4. **Revisão em dobro.** O `/implement` termina com `/code-review`
   (`grep -n 'code-review' $M/implement/SKILL.md`), e o `fechar-demanda` propõe outra revisão. A regra
   geral já cobre isso: *"Exigência já satisfeita por um passo do caminho escolhido não se repete"*
   (`grep -n 'não se repete' skills/fechar-demanda/SKILL.md`). Mas o único exemplo dado é o
   `subagent-driven-development`, e o agente pode não reconhecer o caso do Matt.

**Avaliação:** o aicf não prejudica o núcleo do Matt e resolve uma lacuna dele (o ticket local sem
link para a spec). O ponto em que pode piorar a experiência é o `criar-spec` reentrevistar depois do
grill.

## Ajustes sugeridos para a spec

Nenhum foi aplicado. Os dois primeiros são os que recomendo antes de implementar.

1. **Verificação contra reentrevista** (risco 1). Acrescentar ao item 3 da Verificação: *"o
   `/aicf:criar-spec`, chamado depois do grill, não repete pergunta que a conversa já respondeu. As
   perguntas dele se limitam ao que falta na spec, tipicamente o ponto de teste."* Reforçar no texto
   do parágrafo novo do `criar-spec`, em Arquivos e interfaces: *"não repetir pergunta já respondida
   na conversa"*. Hoje a spec fala em "perguntar só o que falta", o que deixa a reentrevista implícita.
2. **Revisão do `/implement` como exemplo** (risco 4). Em Arquivos e interfaces, incluir
   `skills/fechar-demanda/SKILL.md`: ao lado do exemplo do `subagent-driven-development`, citar o
   `/implement` do Matt, que termina com `/code-review` por ticket. Esse arquivo não está na lista da
   spec hoje.
3. **Pinar a versão do Matt no texto que cita detalhes dele.** Nas skills que nomeiam `grilling`,
   `domain-modeling`, os argumentos de `/to-tickets` e `/implement` ou o layout do `.scratch/`,
   registrar *"conferido no Matt `1.3.1`"*, para quem mantém saber o que reconferir quando o Matt
   subir de versão. Fica a decidir se isso vai no texto da skill (que o agente carrega) ou só no
   `CHANGELOG.md`, conforme a regra do `.claude/CLAUDE.md` sobre evidência fora da referência que o
   agente carrega.
4. **User stories: observar, não mudar** (risco 2). Não incluir agora. Na primeira demanda grande pelo
   Matt, comparar o fatiamento do `/to-tickets` sobre a spec do aicf com o que ele faria sobre uma do
   `to-spec`. Se ficar pobre, o item Solução do `criar-spec` pode pedir os comportamentos do ponto de
   vista do usuário, sem o formato de stories numeradas.

O risco 3 (caminhos de arquivo) fica sem ajuste. O `to-tickets` já os remove, e a spec do aicf é
arquivada no fechamento.
