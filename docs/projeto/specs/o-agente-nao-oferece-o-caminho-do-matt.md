# O agente não oferece o caminho do Matt

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (só markdown, com o texto de cada trecho decidido aqui)

## Problema

Num projeto privado que consome estas skills, com Superpowers e Matt Pocock declarados na linha
"Coleções de skills de workflow instaladas", o agente recomendou o caminho aicf ou o Superpowers em
todas as demandas, e o Matt nenhuma vez. Quando o titular pediu o Matt, o agente levantou
impedimentos. São três causas, todas do aicf:

1. **As skills de caminho do Matt são só do usuário, e o aicf não diz isso.** `grill-with-docs`,
   `to-spec`, `to-tickets` e `implement` têm `disable-model-invocation: true`. Por isso não aparecem
   na lista de skills que o agente recebe, e ele não consegue invocá-las. Numa sessão, o agente
   concluiu que *"essas duas skills não aparecem entre as instaladas"*. O `implementar-spec` diz que
   o caminho de outra coleção "assume até o fim", o que o agente não tem como fazer com o Matt.
   Conferência:
   `grep -l 'disable-model-invocation: true' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/{to-spec,grill-with-docs,to-tickets,implement}/SKILL.md | wc -l`
   devolve 4. O Superpowers está no lado oposto: `brainstorming`, `writing-plans` e
   `subagent-driven-development` aparecem na lista e o agente pode invocá-las.
2. **No modo arquivo, a entrevista do Matt não tem para onde levar a spec.** O template promete
   "`grill-with-docs` → `to-spec`", e o `ajuda` diz que a spec do `to-spec` fica no `.scratch/` e
   que o aicf não a adota (`grep -c 'que o aicf não adota' skills/ajuda/SKILL.md` → 1). O
   `brainstorming` tem regra de passagem para a spec, e o Matt não tem. Arquivo é o modo padrão.
3. **O agente não tem critério para sugerir o Matt.** O template manda sugerir "pelo ponto forte",
   mas os pontos fortes só estão no `README.md`, que o agente não lê. O `criar-spec` cita como
   exemplo de sugestão só `aicf-direto` e `aicf-plan`.

Além disso, o README diz que `grill-me` e `grill-with-docs` "não gravam nada". O `grill-with-docs`
grava, porque invoca o `domain-modeling`, que cria o `GLOSSARY.md` no primeiro termo resolvido
(`grep -n 'create one when the first term' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/domain-modeling/SKILL.md`).

## Solução

O caminho do Matt passa a ser oferecido com o mesmo peso dos outros, conduzido pelo agente onde ele
pode e entregue ao usuário onde só o usuário pode:

| Passo do Matt | Como fica |
| --- | --- |
| `grill-with-docs` (entrevista) | o agente conduz, invocando `grilling` e `domain-modeling`, que é exatamente o que o comando faz |
| `to-spec` | sai, nos dois modos: o agente invoca o `/aicf:criar-spec`, que escreve a spec com `entrevista: grill-with-docs` |
| `to-tickets`, depois `implement` | o agente entrega os comandos, e o usuário os digita (ver abaixo). Os tickets ficam no tracker do Matt, como os planos do Superpowers ficam em `docs/superpowers/plans/` |

O `/aicf:criar-spec #<n>` continua adotando a issue de quem rodar `/to-spec` por conta própria no
modo issue. Isso deixa de ser o caminho oferecido, mas não é removido.

**Toda spec que sai de uma entrevista passa pelo `/aicf:criar-spec`, inclusive a do `brainstorming`.** Hoje a regra de
passagem do `brainstorming` manda o design aprovado virar spec "pela receita da mídia". A receita
(`midia/arquivo.md`, `midia/issues.md`) diz onde e como gravar, mas não o que a spec contém. As
seções, inclusive o item Testes de que o `/implement` do Matt depende, só existem no `criar-spec`,
que nesse momento não está carregado. Passa a ser assim: terminada a conversa do `brainstorming`
ou do `grill-with-docs`, o agente invoca o `/aicf:criar-spec`. Ele parte do que a conversa já
decidiu, pergunta só o que falta (tipicamente o ponto de teste), e grava com o caminho da entrevista
na linha `Processo`. O `criar-spec` ganha um parágrafo para esse caso. Hoje ele só diz para não
gastar rodada com pergunta óbvia, o que não basta para pular uma entrevista que já aconteceu.

Os dois atalhos do passo 1 do `implementar-spec` ficam como estão: spec vinda de
`docs/superpowers/specs/`, e intent que o usuário mandou implementar sem entrevista
(`entrevista: nenhuma`). Uma spec assim pode chegar ao Matt sem o item Testes, e isso não quebra o
fluxo, porque o `/tdd` combina os pontos de teste com o usuário antes de escrever o primeiro
(`grep -n 'confirm them with the user' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/tdd/SKILL.md`).

**Os comandos do Matt levam a spec junto.** O modelo de ticket local do `to-tickets` não tem
referência à spec; a seção `Parent` só existe no modelo de issue remota
(`sed -n '69,88p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/to-tickets/SKILL.md`).
Numa sessão nova, um ticket sozinho perde os pontos de teste combinados na spec, e várias sessões
são justamente o caso em que o Matt é recomendado. Por isso o agente entrega:

- `/to-tickets docs/projeto/specs/<nome>.md`; no modo issue, `/to-tickets #<n>`;
- `/implement docs/projeto/specs/<nome>.md .scratch/<feature>/issues/<NN>-<slug>.md`; no modo issue,
  `/implement #<n> #<ticket>`. O `implement` trabalha sobre "the spec or tickets" que o usuário
  descreve, então aceita os dois.

Terminar um ticket não conclui a demanda. O `/aicf:fechar-demanda` roda quando o último ticket
termina, ou de forma parcial ao fim de uma sessão que deixa tickets abertos, como ele já prevê.

Os critérios de sugestão moram onde são aplicados:

- **Entrevista** (template do `CLAUDE.md`, que é onde o agente decide antes de entrar em qualquer
  skill): `criar-spec` quando faltam decisões pontuais; `brainstorming` quando o desenho está aberto,
  com alternativas a comparar; `grill-with-docs` quando a demanda cria termo ou decisão de domínio,
  que ele grava no `GLOSSARY.md` e em ADR.
- **Implementação** (`criar-spec`, ao gravar a sugestão, e `implementar-spec`, ao perguntar):
  `aicf-direto` ou `aicf-plan` quando cabe numa sessão; Superpowers quando são muitos passos numa
  sessão, executados por subagente e com TDD; Matt quando o trabalho se divide em fatias verticais
  com dependência entre elas, que podem atravessar sessões.

O critério de implementação fica escrito duas vezes, em três linhas cada, porque as duas skills o
aplicam. Um ponteiro de uma para a outra repetiria o defeito da demanda [os critérios moram longe de
quem os usa](../concluidas/os-criterios-moram-longe-de-quem-os-usa.md).

Do `to-spec`, o `criar-spec` absorve dois critérios que não conflitam com o aicf:

- **ADRs da área.** "Antes de perguntar" passa a ler também os ADRs da área tocada.
- **Testes.** Item novo da spec, só quando a demanda toca código: em que ponto a mudança é testada
  (o mais alto que a pega, de preferência um que já existe, idealmente um só) e qual teste parecido
  já existe no repositório. Esse ponto é conferido com o usuário na entrevista.

## Arquivos e interfaces

- `skills/setup/templates/claude-md.md`:
  - a linha "Coleções de skills de workflow instaladas" ganha a nota de que as skills de caminho do
    Matt só o usuário invoca e não aparecem na lista do agente, e que instalado é o que essa linha
    diz;
  - a primeira regra troca "`grill-with-docs` → `to-spec`" por `grill-with-docs` e ganha o
    critério de entrevista;
  - a regra "A passagem entre fases é da governança" passa a cobrir os dois caminhos: terminada a
    conversa do `brainstorming` ou do `grill-with-docs`, o agente invoca o `/aicf:criar-spec`, e não
    grava em `docs/superpowers/specs/` nem pelo `to-spec`. Pelo Matt, o agente conduz a entrevista
    pelo `grilling` + `domain-modeling`.
- `skills/implementar-spec/SKILL.md`, passo 3: a linha do Matt na tabela diz que o usuário digita
  os comandos; o caso "outra coleção" diz que, no Matt, o agente entrega os comandos e espera; o
  critério de implementação vem logo abaixo da tabela; a lista "As skills do Matt (…) exigem
  `/setup-matt-pocock-skills`" deixa de citar o `to-spec`. Os comandos entregues são os da seção
  Solução, com a spec junto, e a skill diz que terminar um ticket não conclui a demanda.
- `skills/implementar-spec/SKILL.md`, seção "Implementar": logo depois da regra "Avaliar se a
  mudança merece teste", que não muda, entra o parágrafo que faz o item Testes valer nos caminhos
  aicf. Sem ele, o ponto de teste combinado na entrevista fica escrito na spec e nenhuma regra o
  aplica: a regra atual decide *se* a mudança leva teste, não *onde*. Com o Matt instalado, o *como*
  passa a ser o `/tdd`, que o agente pode invocar e que traz junto as próprias regras (seams
  confirmadas, ciclo vermelho → verde, antipadrões). Nos caminhos Superpowers e Matt nada muda,
  porque o `implementar-spec` passa a vez e o método testa do jeito dele. Texto:

  > Código que merece teste entra no ponto que o item Testes da spec nomeia. **Com o Matt Pocock
  > instalado** (linha "Coleções de skills de workflow instaladas" do `CLAUDE.md`), escreve-se pelo
  > `/tdd`; sem ele, pelas regras acima. Testar em outro ponto, ou não testar o que a spec previu,
  > se diz em uma linha antes de fazer.
- `skills/criar-spec/SKILL.md`: ADRs em "Antes de perguntar"; um parágrafo para a entrevista que
  já aconteceu por `brainstorming` ou `grill-with-docs` (partir do decidido, perguntar só o que
  falta, gravar o caminho na linha `Processo`); item **Testes** em "A spec"; e o critério de
  implementação no passo 2 de "Ao terminar". Cerca de 9 linhas a mais, sobre 82.
- `skills/ajuda/SKILL.md`: a frase "No modo arquivo, a spec do `to-spec` do Matt fica no `.scratch/`
  dele, que o aicf não adota" passa a dizer que a spec do Matt, como a do `brainstorming`, sai pelo
  `/aicf:criar-spec`.
- `skills/midia/issues.md`: o caso "O `to-spec` do Matt cria issue nova" passa a ser o de quem roda
  o `/to-spec` por conta própria.
- `README.md` e `README.en.md`: `grill-me` e `grill-with-docs` separados (o segundo grava glossário
  e ADR); "`grill-with-docs` + `to-spec`" vira `grill-with-docs` com a spec gravada pelo aicf.
- `.claude/CLAUDE.md` deste repositório: as mesmas três mudanças do template, porque ele declara
  as duas coleções e é o que o agente lê aqui antes de qualquer skill.
- `.claude-plugin/plugin.json` e `CHANGELOG.md`: `0.37.0`.

Projeto que já fez o setup recebe as mudanças das skills ao atualizar o plugin. A do template não
chega sozinha: as notas da release trazem o trecho do `CLAUDE.md` a trocar, e o titular aplica no
projeto privado que originou esta demanda.

## Fora de escopo

- **Mandar o agente ler o `to-spec` em runtime.** O caminho do cache muda a cada versão do Matt, e
  o critério deve morar na skill que o aplica. Foi absorvido o que serve.
- **User stories numeradas, do `to-spec`.** Para demanda pequena viram enchimento, e nenhuma skill
  de implementação do Matt as lê; o que o `/implement` e o `/tdd` exigem são os seams combinados,
  que o item Testes cobre.
  `grep -rn -i 'user stor' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/{to-tickets,implement,tdd,code-review}/`
  não devolve nada; trocando o padrão por `seam`, devolve o `implement` e o `/tdd`.
- **"Não incluir caminho de arquivo nem código", regra do `to-spec` do Matt.** O aicf pede o
  contrário: "Arquivos e interfaces, nomeados". A spec do aicf é implementada logo e arquivada com
  relatório, então o caminho não envelhece.
- **A exceção do `to-spec` para trecho de protótipo.** Ela só libera código vindo do `/prototype`
  dentro de uma spec que proíbe código. O `criar-spec` nunca proibiu, então não há o que liberar.
- **O viés do hook de início de sessão do Superpowers.** É do Superpowers, e o aicf não muda skill
  de outra coleção.
- **Apontar o tracker do Matt para `docs/projeto/`.** Já descartado em
  [o setup não avisa que o Matt pergunta o mesmo](../concluidas/o-setup-nao-avisa-que-o-matt-pergunta-o-mesmo.md).

## Verificação

1. Contagens, antes (medido nesta entrevista) → depois:
   - `grep -c 'entrevista: grill-with-docs' skills/setup/templates/claude-md.md`: 0 → 1
   - ``grep -c 'grill-with-docs` → `to-spec' skills/setup/templates/claude-md.md``: 1 → 0
   - `grep -c 'que o aicf não adota' skills/ajuda/SKILL.md`: 1 → 0
   - `grep -c 'ADR' skills/criar-spec/SKILL.md`: 0 → ≥ 1
   - `grep -c 'Testes' skills/criar-spec/SKILL.md`: 0 → 1
   - `grep -c '/to-tickets' skills/implementar-spec/SKILL.md`: 0 → ≥ 1
   - `grep -c '/tdd' skills/implementar-spec/SKILL.md`: 0 → ≥ 1
   - `grep -c 'item Testes' skills/implementar-spec/SKILL.md`: 0 → 1
   - `grep -c 'Não gravam nada' README.md`: 1 → 0
   - `grep -c 'vira a spec da demanda pela receita da mídia' skills/setup/templates/claude-md.md`: 1 → 0
   - `grep -c 'aicf:criar-spec' skills/setup/templates/claude-md.md`: 2 → ≥ 3
   - `grep -c 'vira a spec da demanda pela receita da mídia' .claude/CLAUDE.md`: 1 → 0
   - `grep -c 'aicf:criar-spec' .claude/CLAUDE.md`: 2 → ≥ 3
2. `./scripts/check.sh` termina em `Tudo verde.`
3. Comportamento, em aberto até o uso real: no projeto privado de origem, com o plugin atualizado,
   a sessão reiniciada e o trecho do template aplicado, a pergunta "por qual caminho entrevistamos
   esta demanda?" numa demanda de modelagem de domínio recomenda o `grill-with-docs` pelo critério,
   o agente conduz a entrevista sem pedir que o usuário digite o comando, invoca o
   `/aicf:criar-spec` ao terminar, e a spec aparece em `docs/projeto/specs/` com o item Testes,
   sem nada em `.scratch/`. Na implementação, os comandos entregues levam a spec, e um ticket
   retomado numa sessão nova chega aos pontos de teste da spec sem depender da conversa anterior.
   Encerra o titular, na primeira demanda que for pelo Matt.
