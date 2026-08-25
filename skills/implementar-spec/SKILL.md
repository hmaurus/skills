---
name: implementar-spec
description: Implementa uma demanda a partir da spec e conduz o fechamento até o registro. Caminho nativo da fase de implementação — par do `criar-spec`.
disable-model-invocation: true
---

# Implementar a partir da spec

Funciona igual com o plan mode ligado ou desligado. **Ligar é decisão do usuário, não desta
skill:** se estiver ligado, montar o plano e esperar aprovação antes de tocar o disco.

## Antes de escrever código

1. **Ler a spec inteira** — venha de `docs/projeto/demandas/<nome>.md`, de
   `docs/superpowers/specs/` ou de uma issue. Se o usuário não disse qual, perguntar em vez de
   adivinhar entre as demandas abertas.
2. **Ler os arquivos que a spec nomeia**, e o que já existe de parecido no repositório.

Se a spec não diz o suficiente para implementar, dizer isso e propor uma rodada de
`/aicf:criar-spec` — não preencher a lacuna por conta própria.

## Implementar

A spec é roteiro, não trilho: ao sair dela (pular etapa, trocar de abordagem, ferramenta que
ela não cita), dizer em uma linha o que vai fazer e por quê, antes de fazer.

Código novo se parece com o código vizinho. Não ampliar o escopo: o que a spec pôs fora de
escopo fica fora, e ideia nova que aparecer no caminho vira registro para depois, não código
agora.

## Verificar e fechar

Rodar o passo de verificação ponta a ponta que a spec descreve — **só afirmar que funciona
depois de ver a saída do comando** — e daí invocar `/aicf:fechar-demanda`, que conduz o ritual
até o registro. **Não presumir o ritual pela memória desta skill.**
