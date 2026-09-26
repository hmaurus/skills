# O brainstorming atravessa a fronteira da entrevista

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

Quando a entrevista roda pelo `brainstorming` do Superpowers, o agente segue para a implementação
sem parar, e a spec não fica onde o aicf a procura.

- **Caminho _architectural_:** o `brainstorming` grava `docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md`
  e manda chamar o `writing-plans` — *"Do NOT invoke any other skill. writing-plans is the next
  step."* (`grep -n 'writing-plans is the next step' ~/.claude/plugins/cache/superpowers-marketplace/superpowers/6.4.2/skills/brainstorming/SKILL.md`).
- **Caminho _bounded_:** design curto na conversa, aprovação, e implementação ali mesmo, *"no plan
  document"* (`grep -n 'no plan document' …/brainstorming/SKILL.md`). A spec nunca vai para arquivo.
- **A regra do `CLAUDE.md` empurra no mesmo sentido.** *"Rodar o processo de implementação
  inteiro — inclusive o passo de integração que ele encadeia"* faz a chamada do `writing-plans`
  parecer encadeamento dentro de uma fase. A frase que separava as fases — *"parar na fronteira é
  legítimo"* — ficou só no `/aicf:ajuda`, que desde a `0.31.0` o agente não carrega
  (`grep -c 'parar na fronteira é legítimo' skills/ajuda/SKILL.md` → 1; em `CLAUDE.md` → 0).
- **Dois registros para a mesma demanda.** Com o design em `docs/superpowers/specs/` e o intent em
  `docs/projeto/intents/`, o "um item, um lugar" quebra.

A tabela de implementação do `implementar-spec` também cita só o `subagent-driven-development`,
embora o `writing-plans` ofereça o `executing-plans` como alternativa (`grep -n 'REQUIRED SUB-SKILL' …/writing-plans/SKILL.md`
→ as duas) — as duas terminam no `finishing-a-development-branch`.

## Solução

**Uma regra nova no `CLAUDE.md`, do repositório e do template**, logo depois de "O método escolhido
fecha o código; a governança fecha a demanda". É o único texto do aicf que o agente tem na frente
enquanto o `brainstorming` roda:

> **A passagem entre fases é da governança.** Pelo `brainstorming` (Superpowers), o design aprovado
> — o arquivo do caminho _architectural_ ou o design curto do _bounded_ — vira a spec da demanda
> pela receita da mídia, com `entrevista: brainstorming` na linha `Processo`, e não em
> `docs/superpowers/specs/`; então o agente para e pergunta o caminho da implementação. O
> `writing-plans` que o `brainstorming` chama é passagem de fase, não encadeamento.

"Pela receita da mídia" cobre os dois modos e o intent que já existe: no modo arquivo, `git mv` do
intent para `specs/` (ou arquivo novo em `specs/<nome>.md`, sem data no nome); no modo issue, o
corpo da issue com `aicf:spec`. A doc do Superpowers aceita o desvio de local — *"User preferences
for spec location override this default"* (`grep -n 'spec location override' …/brainstorming/SKILL.md`).

A regra conta como uma das regras da lista: "Cinco regras" vira "Seis regras" nos dois arquivos.

**O `/aicf:ajuda`** troca "parar na fronteira é legítimo — o design doc dele vale como spec" por
"o agente para na fronteira, grava o design como spec e pergunta o caminho da implementação" —
o mapa passa a descrever a regra, em vez de uma permissão.

**O `implementar-spec`**, na tabela do passo 3: a linha do Superpowers vira `writing-plans`,
depois `subagent-driven-development` ou `executing-plans`.

**Versão `0.32.0`**: regra nova no template muda o comportamento de projetos novos. A nota da
release traz a regra para quem quiser colar no `CLAUDE.md` de um projeto já configurado.

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `CLAUDE.md`, `skills/setup/templates/claude-md.md` | regra nova depois de "O método escolhido fecha o código"; "Cinco regras" → "Seis regras" |
| `skills/ajuda/SKILL.md` | a frase da fronteira passa de permissão a regra |
| `skills/implementar-spec/SKILL.md` | linha do Superpowers na tabela do passo 3 |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.32.0` e a entrada |

## Fora de escopo

- **Matt Pocock.** `grill-with-docs`, `to-spec`, `to-tickets` e `implement` têm
  `disable-model-invocation: true` (`grep -l '^disable-model-invocation: true' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.2.3/skills/engineering/{grill-with-docs,to-spec,to-tickets,implement}/SKILL.md`
  → os quatro): o agente não encadeia nada, e cada passagem de fase é o usuário digitando o próximo
  comando. A nota do backlog sobre "emendar o `to-spec` no `implement`" descrevia uma escolha do
  usuário, não do agente.
- **Caminho _spike_ do `brainstorming`.** Termina numa recomendação, sem código que fique; não é
  demanda a implementar.
- **Mudar o `brainstorming`.** Não é nosso; a regra fica do lado do aicf.
- **Atualizar o `CLAUDE.md` de projetos já configurados** — a nota da release traz o texto.

## Verificação

Valores de hoje medidos em `d3b4fd1`.

1. **A regra está nos dois `CLAUDE.md`.**
   `grep -c 'passagem de fase' CLAUDE.md skills/setup/templates/claude-md.md` → hoje 0 e 0;
   depois 1 e 1. Mesmo resultado para `grep -c 'entrevista: brainstorming'`.
2. **A contagem da lista acompanha.** `grep -c 'Seis regras' CLAUDE.md skills/setup/templates/claude-md.md`
   → 1 e 1; `grep -rn 'Cinco regras' --include='*.md' . --exclude-dir=.git` só acha
   `docs/projeto/concluidas/` e esta spec (hoje acha também os dois `CLAUDE.md`).
3. **O mapa descreve a regra.** `grep -c 'parar na fronteira é legítimo' skills/ajuda/SKILL.md`
   → hoje 1; depois 0.
4. **A tabela cita as duas execuções.** `grep -c 'executing-plans' skills/implementar-spec/SKILL.md`
   → hoje 0; depois 1.
5. `./scripts/check.sh` → `Tudo verde.`
6. **Comportamento, no uso real.** Depende de atualizar o plugin e começar sessão nova, então não
   tem passada dedicada (regra do `CLAUDE.md`). Encerra na primeira demanda entrevistada pelo
   `brainstorming` num projeto com a regra no `CLAUDE.md`: a spec aparece em `docs/projeto/specs/`
   (ou no corpo da issue), nada novo em `docs/superpowers/specs/`, e o agente pergunta o caminho
   da implementação em vez de invocar o `writing-plans`.

## Relatório de implementação (2026-09-26)

- **Status** — concluído. O CI é conferido depois do push, se você pedir o envio. A verificação 6
  (comportamento) fica para o uso real, como a spec previa.
- **Arquivos alterados**
  - `CLAUDE.md` e `skills/setup/templates/claude-md.md`: a regra "A passagem entre fases é da
    governança", depois de "O método escolhido fecha o código", e "Seis regras".
  - `skills/ajuda/SKILL.md`: a fronteira do `brainstorming` descrita como regra, não como permissão.
  - `skills/implementar-spec/SKILL.md`: a linha do Superpowers com `executing-plans`.
  - `.claude-plugin/plugin.json` (`0.32.0`) e `CHANGELOG.md`.
- **Commits** — `4eded3f feat(governanca): a passagem entre fases é da governança`; o fechamento vai no
  commit seguinte.
- **Validação** — as verificações 1 a 5 da spec, depois das edições: 1 → `1` e `1` nos dois
  comandos; 2 → `Seis regras` `1` e `1`, e `Cinco regras` só em `docs/projeto/concluidas/` e nesta
  demanda; 3 → `0`; 4 → `1`; 5 → `Tudo verde.`. Não houve revisão de código: a mudança é só texto,
  com as frases decididas na entrevista. A verificação 6 encerra na primeira demanda entrevistada
  pelo `brainstorming` num projeto com a regra: a spec aparece em `docs/projeto/specs/` (ou no
  corpo da issue), nada novo em `docs/superpowers/specs/`, e o agente pergunta o caminho em vez de
  invocar o `writing-plans`.
- **Escopo efetivo** — o previsto. A entrada do `CHANGELOG.md` foi reescrita para não repetir
  "Cinco regras", que a verificação 2 acusou na primeira passada.
- **Lições** — nenhuma promoção. Esta demanda nasceu como backlog "esperar tropeçar" e foi
  promovida quando a leitura dos dois frameworks mostrou que a regra "processo inteiro" empurrava o
  agente a não parar. É a regra "Critério mora na skill que o aplica" do `CLAUDE.md`, agora com o
  `CLAUDE.md` como o texto que o agente tem na frente dentro de outra coleção.
