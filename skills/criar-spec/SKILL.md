---
name: criar-spec
description: Entrevista o usuário até a demanda estar madura e escreve a spec no repositório. Caminho nativo da fase de entrevista — par do `implementar-spec`.
disable-model-invocation: true
---

# Criar spec por entrevista

Transforma uma ideia ainda vaga na spec que a implementação vai consumir. O ciclo inteiro está
em `/aicf:workflow-demanda`.

Rodar **fora do plan mode**: o passo final grava arquivo.

## Como entrevistar

`AskUserQuestion` para o que é **escolha** (escopo, prioridade, trade-off entre abordagens — o
"Other" protege contra enquadramento errado); pergunta aberta para o que é **descritivo** (o
que incomoda hoje, como imagina usando). **Começar aberto** — menu ancora quem ainda não formou
opinião sobre o próprio problema.

Cobrir implementação técnica, UX, casos de borda e o que pode dar errado. **Não gastar rodada
com pergunta óbvia** — ir nas partes difíceis que o usuário talvez não tenha considerado. Fato
que dá para descobrir no repositório é trabalho do agente, não pergunta: ler o código antes de
perguntar sobre ele.

Continuar até não sobrar decisão em aberto, e só então escrever.

## A spec

Vai em `docs/projeto/demandas/<nome-em-kebab-case>.md` — no caminho nativo, spec e demanda são
o mesmo arquivo. Sem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

- **Problema** — o que está errado hoje, do ponto de vista de quem usa
- **Solução** — o que passa a existir, na mesma linguagem
- **Arquivos e interfaces** envolvidos, nomeados
- **Fora de escopo** — o que foi levantado e decidido não fazer, com o motivo
- **Verificação** — um passo ponta a ponta que prova que funcionou

Usar o vocabulário do domínio do projeto (`CONTEXT.md`, se existir).

## Ao terminar

1. Mostrar a spec e pedir revisão antes de considerar fechada.
2. Perguntar por qual caminho será implementada e registrar logo abaixo do título:
   `Processo: <entrevista> → <implementação>` — a recomendação é do agente; a decisão é do
   usuário.
3. Sugerir `/clear` ou sessão nova para implementar: o contexto da entrevista já cumpriu seu
   papel e a partir daqui só atrapalha.
