---
name: fechar-demanda
description: Ritual de fechamento de uma demanda — checks, revisão, relatório, arquivamento e promoção de conhecimento. Aplicar proativamente ao concluir qualquer demanda, por qualquer caminho de implementação, e também ao interromper uma demanda por falta de contexto, para registrar o estado parcial antes do /clear.
---

# Fechar uma demanda

Não importa por onde a demanda começou, ela termina aqui — e o agente aplica o fechamento
proativamente, sem esperar pedido.

**Antes de qualquer coisa: a implementação terminou inteira?** Caminho de outra coleção termina no
passo que ele encadeia — no Superpowers, `finishing-a-development-branch`, que decide o destino do
código. Fechar a demanda com essa decisão não tomada é o erro que este parágrafo existe para
evitar: o registro diz "concluído" e o código fica parado numa branch. Se o método tem passo de
integração e ele não rodou, rodar antes.

## Antes do relatório

Rodar o script de check do projeto (lint + format + typecheck) e a suíte de testes, quando
existe, **no projeto inteiro, nunca só nos arquivos tocados**. Qual é o comando, a seção
`## Verificação` do `CLAUDE.md` diz — é a que o `/aicf:setup` gera; quando não existe, vale o que
os scripts do projeto expõem, e não havendo nenhum o relatório registra isso — o passo não some
em silêncio. Propor revisão de código quando a mudança for além de ajuste de texto —
`/code-review`, subagente fresco que não viu a implementação, ou o code review do harness; não
reler o próprio diff na mesma sessão. **Exigência já satisfeita por um passo do caminho escolhido
não se repete** — o `subagent-driven-development` termina com revisão do branch inteiro, e pedir
outra é pagar duas vezes pela mesma leitura; o relatório declara em uma linha, na Validação, qual
passo cobriu qual exigência.

## Os cinco passos

1. **Relatório** no arquivo da demanda. Se a demanda não tinha arquivo, criar agora.
2. **Mover** para `specs/concluidas/`, e corrigir os links relativos que apontavam para o
   arquivo — `grep -rn "<nome-do-arquivo>" --include="*.md" .` acha todos.
3. **Marcar `- [x]`** no checklist: a linha sai de `Em andamento` e entra em `Entregue` —
   demanda que nasceu já no fechamento entra direto em `Entregue`.
4. **Reler o próprio relatório e os achados da revisão de código procurando o que vale além
   desta demanda** — decisão que outra sessão vai reencontrar, armadilha que vai morder de novo,
   ID externo — e promover, porque ninguém abre demanda concluída procurando informação:

   | O que é | Vai para |
   | --- | --- |
   | Conhecimento operacional — manual, ID, gotcha | doc de referência |
   | Regra que muda como o agente age: erro que já apareceu duas vezes; achado da revisão que o agente deveria saber sobre este código (esse não espera a segunda vez); contexto que um colega novo precisaria | `CLAUDE.md` |
   | Regra que só vale para uma parte do código | `.claude/rules/<tema>.md` com `paths:` no frontmatter — carrega só ao tocar arquivo daquele padrão |
   | Procedimento que já se repetiu | skill — gatilho e critério skill×hook no `/aicf:workflow-demanda` |
   | Decisão difícil de reverter, surpreendente e com trade-off real | ADR numerado e imutável em `docs/adr/` (`0001-slug.md`) |
   | Termo ambíguo do domínio | glossário em `CONTEXT.md` |

   **Afirmação verificável carrega o teste que a refuta.** Número vem com o comando que o
   remede — `<N> linhas` (`wc -l < <arquivo>`, `<AAAA-MM-DD>`); afirmação de estado — item de
   backlog, "bloqueado por", "ainda não existe" — vem com a condição que a encerra. Sem isso
   conferir vira julgar em vez de executar.

   ADR e glossário podem sair de `/domain-modeling`, quando instalado; escrever direto pela
   tabela também serve. Escrever no `CLAUDE.md` obriga a olhar o que de lá saiu de
   validade e o tamanho: ele é lido inteiro em toda sessão, o alvo que a documentação do Claude
   Code publica é abaixo de 200 linhas por arquivo, e `/doctor` propõe cortes do que o agente já
   deduz do próprio código.
5. **Conferir o índice — enumerando, não julgando se está em dia.** No layout padrão, sob
   `docs/projeto/`, três pares seção↔pasta: `Decidido`↔`intents/`, `Em andamento`↔`specs/`,
   `Entregue`↔`specs/concluidas/`.

   **A conferência corre num sentido só: todo arquivo da pasta tem linha na seção.** Arquivo sem
   linha é a falta a corrigir — inclusive o item entregue que foi apagado em vez de movido. Linha
   sem arquivo é legítima e comum: demanda que coube numa linha e nunca virou arquivo. **Nunca
   apagar linha por não achar arquivo.** `Fundação` e `Backlog` não têm pasta e ficam fora.

   **E a saída dos passos 1 a 4 deste mesmo ritual** — ADR, regra, skill ou doc de referência que
   o passo 4 acabou de criar entra como link no item de `Entregue` desta demanda; não tendo gerado
   nada, o registro diz isso.

   Por fim, **o que esta demanda escreveu fora de `docs/projeto/`** — código, doc de referência,
   `.claude/rules/` — criou item novo no checklist ou tornou algum obsoleto? Ajustar inline.

O fechamento vai num commit próprio, separado do commit de código; quando o processo escolhido já
commitou por conta própria, cobre só o registro. Tarefa pequena (fix trivial, copy, renomeação)
cabe num commit, e a demanda pode nascer já no fechamento: o relatório registra o que foi feito
e o arquivo vai direto para `specs/concluidas/`. Ao final, avaliar o peso do contexto e sugerir
`/clear` se estiver pesado — não a cada demanda por reflexo.

## Sessão que acaba antes da demanda

Contexto no fim com a demanda aberta também é fechamento, parcial: o arquivo fica em `specs/`,
a linha segue em `Em andamento` e o checklist não é marcado, e o que a sessão descobriu vai para
o próprio arquivo sob
`## Estado em andamento` — decisão tomada, caminho descartado com o motivo, onde parou e o
próximo passo. **Se a frase serve para qualquer demanda, ela é do `CLAUDE.md`, não do arquivo.**
O teste é a retomada caber em `continue a demanda <arquivo>`. Commit próprio; no fechamento
definitivo o bloco some, absorvido pelo relatório.

Quando o usuário sinaliza a parada, o agente registra sem perguntar. Quando é o agente que
percebe o aperto, ele avisa e a decisão é do usuário — encerrar o trabalho por conta própria
para registrar, não.

## O relatório

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

Vale aqui a regra do passo 4: número e afirmação de estado entram com o teste que os refuta — é
neste bloco que a medição congelada em prosa costuma nascer.

## A linha `Processo`

Logo abaixo do título da demanda: dois campos nomeados, valor sempre escrito — nada é
sinalizado por ausência. O valor é o nome da skill usada, ou `nenhuma`; no caminho aicf,
`criar-spec`, `aicf-direto` ou `aicf-plan`. Enquanto a implementação está `a definir`, a linha
pode trazer um terceiro campo, `sugestão: <valor> (motivo)`, gravado pelo `criar-spec`; ao
fechar, o caminho seguido substitui `a definir · sugestão: ...` inteiro, e a sugestão some. Se o
caminho seguido divergiu da sugestão, o relatório diz por quê em "Escopo efetivo" ou "Lições";
seguir a sugestão no caso óbvio, sem perguntar, é o comportamento certo e não recebe marca.
Referências externas (issues, tickets, PRs) entram no fim da mesma linha.

```
Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (toca dois arquivos, sem decisão de abordagem)
Processo — entrevista: nenhuma · implementação: aicf-direto
Processo — entrevista: grill-with-docs · implementação: aicf-plan
Processo — entrevista: brainstorming · implementação: subagent-driven-development
Processo — entrevista: grill-with-docs · implementação: implement · issues #12, #13
```
