---
name: criar-spec
description: Entrevista o usuário até a demanda estar madura e escreve a spec no repositório. Invocar quando o usuário pede entrevista, spec ou amadurecimento de uma demanda ou intent; não invocar para pergunta pontual, nem no meio de uma implementação sem o usuário pedir a volta à entrevista. Caminho aicf da fase de entrevista.
---

# Criar spec por entrevista

Transforma uma ideia ainda vaga na spec que a implementação vai consumir.

Rodar **fora do plan mode**: o passo final grava a demanda.

**Alvo opcional `#<n>`, no modo issue.** `/aicf:criar-spec #12` **adota** a issue 12 em vez de
abrir uma nova: reescreve o corpo dela e ajusta o label — **olhando antes o que ela já tem**, para
trocar em vez de acrescentar quando já houver um `aicf:*`. É assim que uma issue de fora da
governança entra nela, e é o que evita duas issues para a mesma demanda quando a entrevista veio
pelo `to-spec` do Matt Pocock, que cria issue nova em vez de editar a existente. No modo arquivo
não há alvo a adotar.

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

- **Problema** — o que está errado hoje, do ponto de vista de quem usa
- **Solução** — o que passa a existir, na mesma linguagem
- **Arquivos e interfaces** envolvidos, nomeados
- **Fora de escopo** — o que foi levantado e decidido não fazer, com o motivo
- **Verificação** — um passo ponta a ponta que prova que funcionou

Usar o vocabulário do domínio do projeto (`CONTEXT.md`, se existir). E **afirmação verificável
carrega o teste que a refuta** — número traz o comando que o remede, afirmação de estado traz a
condição que a encerra; a forma está no passo 3 do `/aicf:fechar-demanda`.

### Onde ela mora

A linha `**Mídia do registro:**` do `CLAUDE.md` diz qual arquivo de
[`midia/`](../midia/) seguir — `arquivo.md` ou `issues.md`; sem linha, arquivo. Se `docs/agents/issue-tracker.md` discordar da linha, avisar
uma vez e seguir a linha.

A demanda **muda de estado** para "pronta para implementar". Três casos, e só o terceiro cria
registro novo:

- **Já tem registro próprio** (arquivo em `intents/`, ou issue com label `aicf:*`) — é esse mesmo
  que vira a spec, nunca um segundo. No **modo arquivo**, `git mv` de `intents/` para `specs/` e o
  conteúdo reescrito: o nome fica, o histórico acompanha, nada sobra em `intents/`. O caminho muda,
  então **corrigir quem apontava para o arquivo**, pela receita da mídia. No **modo issue**, o corpo
  é reescrito e o label **troca** para `aicf:spec` — mesma issue, mesmo número, e o label anterior
  sai junto.
- **Era uma linha do `ROADMAP.md`** (só existe no modo arquivo) — vira arquivo em `specs/`, e **a
  linha sai**: quem tem arquivo não tem linha.
- **Nunca foi registrada** — a demanda nasce já no estado "pronta para implementar", numa escrita
  só: arquivo direto em `specs/`, ou `gh issue create --label aicf:spec`.

Sem mídia declarada e sem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

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
