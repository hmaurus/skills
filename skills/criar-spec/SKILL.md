---
name: criar-spec
description: Entrevista o usuário até a demanda estar madura e escreve a spec no repositório. Caminho nativo da fase de entrevista — alternativa ao `brainstorming` (Superpowers) e ao `grill-with-docs` (Matt Pocock).
disable-model-invocation: true
---

# Criar spec por entrevista

Transforma uma ideia ainda vaga na spec que a implementação vai consumir. É a fase de
**entrevista** no caminho nativo — sem plugin, só Claude Code. O ciclo inteiro está em
`/aicf:workflow-demanda`.

Rodar **fora do plan mode**: o passo final grava arquivo.

## Onde a spec fica

`docs/projeto/demandas/<nome-em-kebab-case>.md`, salvo se o `CLAUDE.md` do projeto disser
outra coisa. No caminho nativo, spec e demanda são o mesmo arquivo.

Se o repositório não tem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

## Como entrevistar

Dois formatos de pergunta, misturados conforme o que se está buscando:

- **`AskUserQuestion`** para o que é escolha — escopo, prioridade, trade-off entre
  abordagens. Cada rodada estreita o espaço, e o "Other" protege contra enquadramento errado.
- **Pergunta aberta** para o que é descritivo — o que incomoda hoje, como imagina usando.

**Começar aberto.** Abrir com menu de opções ancora quem ainda não formou opinião sobre o
próprio problema.

Cobrir implementação técnica, UX, casos de borda e o que pode dar errado. **Não gastar
rodada com pergunta óbvia** — ir nas partes difíceis que o usuário talvez não tenha
considerado. Fato que dá para descobrir no repositório é trabalho do agente, não pergunta:
ler o código antes de perguntar sobre ele.

Continuar até não sobrar decisão em aberto, e só então escrever.

## O que a spec precisa conter

- **Problema** — o que está errado hoje, do ponto de vista de quem usa
- **Solução** — o que passa a existir, na mesma linguagem
- **Arquivos e interfaces** envolvidos, nomeados
- **Fora de escopo** — o que foi levantado na entrevista e decidido não fazer, com o motivo
- **Verificação** — um passo ponta a ponta que prova que funcionou

Usar o vocabulário do domínio do projeto (`CONTEXT.md`, se existir).

## Ao terminar

1. Mostrar a spec e pedir revisão antes de considerar fechada.
2. Perguntar por qual caminho ela será implementada — nativo direto, nativo plan mode,
   Superpowers ou Matt Pocock — e registrar na linha `Processo:` logo abaixo do título.
   A recomendação é do agente; a decisão é do usuário.
3. Sugerir `/clear` ou sessão nova para implementar: o contexto da entrevista já cumpriu
   seu papel e a partir daqui só atrapalha.
