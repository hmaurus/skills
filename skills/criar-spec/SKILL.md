---
name: criar-spec
description: Entrevista o usuário até a demanda estar madura e escreve a spec no repositório. Invocar quando o usuário pede entrevista, spec ou amadurecimento de uma demanda ou intent; não invocar para pergunta pontual, nem no meio de uma implementação sem o usuário pedir a volta à entrevista. Caminho aicf da fase de entrevista.
---

# Criar spec por entrevista

Transforma uma ideia ainda vaga na spec que a implementação vai consumir. O ciclo inteiro está
em `/aicf:workflow-demanda`.

Rodar **fora do plan mode**: o passo final grava a demanda.

**Alvo opcional `#<n>`, no modo issue.** `/aicf:criar-spec #12` **adota** a issue 12 em vez de
abrir uma nova: reescreve o corpo dela e põe o label. É assim que uma issue de fora da governança
entra nela, e é o que evita duas issues para a mesma demanda quando a entrevista veio pelo
`to-spec` do Matt Pocock, que cria issue nova em vez de editar a existente. No modo arquivo não há
alvo a adotar.

## Antes de perguntar

Ler o que a demanda toca no repositório — o intent, se existe, e o código, os docs e os commits
recentes da área —, **se ainda não tiver lido nesta sessão**. O que se descobre lendo não é
pergunta: fato do repositório é trabalho do agente; decisão é do usuário.

## Como entrevistar

`AskUserQuestion` para o que é **escolha** (escopo, prioridade, trade-off entre abordagens — o
"Other" protege contra enquadramento errado); pergunta aberta para o que é **descritivo** (o
que incomoda hoje, como imagina usando). **Começar aberto** — menu ancora quem ainda não formou
opinião sobre o próprio problema.

Cobrir implementação técnica, UX, casos de borda e o que pode dar errado. **Não gastar rodada
com pergunta óbvia** — ir nas partes difíceis que o usuário talvez não tenha considerado.

Continuar até não sobrar decisão em aberto, e só então escrever.

## A spec

**Onde ela mora depende da mídia do registro** — a linha `**Mídia do registro:**` do `CLAUDE.md`
diz qual, e linha ausente significa arquivo. As duas receitas estão em
[`references/midia.md`](../workflow-demanda/references/midia.md) do `workflow-demanda`.

A demanda **muda de estado** para "pronta para implementar", e o registro é o mesmo de antes, não
um novo: no **modo arquivo**, o intent vai de `intents/` para `specs/` com `git mv` e o conteúdo é
reescrito — o nome fica, o histórico acompanha, nada sobra em `intents/`; se ela ainda era uma
linha do `ROADMAP.md`, **a linha sai**, porque quem tem arquivo não tem linha. No **modo issue**, o
corpo da issue é reescrito e o label troca para `aicf:spec` — mesma issue, mesmo número.

Sem mídia declarada e sem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

- **Problema** — o que está errado hoje, do ponto de vista de quem usa
- **Solução** — o que passa a existir, na mesma linguagem
- **Arquivos e interfaces** envolvidos, nomeados
- **Fora de escopo** — o que foi levantado e decidido não fazer, com o motivo
- **Verificação** — um passo ponta a ponta que prova que funcionou

Usar o vocabulário do domínio do projeto (`CONTEXT.md`, se existir). E **afirmação verificável
carrega o teste que a refuta** — número traz o comando que o remede, afirmação de estado traz a
condição que a encerra; a forma está no passo 3 do `/aicf:fechar-demanda`.

## Ao terminar

1. Mostrar a spec e pedir revisão antes de considerar fechada.
2. Registrar logo abaixo do título — no modo issue, na primeira linha do corpo — o que já é fato,
   mais a sugestão de caminho: um dos instalados (`aicf-direto`, `aicf-plan`, ou a skill de outra
   coleção), com o motivo numa frase:
   `Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (toca dois arquivos, sem decisão de abordagem)`.
   Quem decide é o `/aicf:implementar-spec`, inclusive quando a implementação emenda nesta
   sessão (passo 3).
3. Entrevista curta e demanda pequena → seguir na mesma sessão, se o usuário quiser emendar a
   implementação. Entrevista longa → sugerir `/clear` ou sessão nova: a spec deve bastar
   sozinha, e o resíduo da conversa ancora a implementação na memória em vez do texto.
