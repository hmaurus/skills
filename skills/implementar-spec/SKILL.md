---
name: implementar-spec
description: Implementa uma demanda a partir da spec e conduz o fechamento até o registro. Caminho nativo da fase de implementação — par do `criar-spec`.
disable-model-invocation: true
---

# Implementar a partir da spec

Pega a spec produzida pela entrevista, implementa, verifica e fecha o registro. É a fase de
**implementação** no caminho nativo — sem plugin, só Claude Code.

Funciona igual com o plan mode ligado ou desligado. **Ligar é decisão do usuário, não desta
skill:** se estiver ligado, montar o plano e esperar aprovação antes de tocar o disco.

## Antes de escrever código

1. **Ler a spec inteira.** Ela vem de onde vier — `docs/projeto/demandas/<nome>.md`,
   `docs/superpowers/specs/` ou uma issue. Se o usuário não disse qual, perguntar em vez de
   adivinhar entre as demandas abertas.
2. **Invocar `/aicf:workflow-demanda`** — governança, formato do relatório e ritual de fechamento
   vivem lá, e este arquivo não os repete. **Não presumir o ritual pela memória desta skill.**
3. **Ler os arquivos que a spec nomeia**, e o que já existe de parecido no repositório. Código
   novo se parece com o código vizinho.

Se a spec não diz o suficiente para implementar, dizer isso e propor uma rodada de
`/aicf:criar-spec` — não preencher a lacuna por conta própria.

## Implementar

Seguir os padrões que já existem. Não ampliar o escopo: o que a spec pôs fora de escopo fica
fora, e ideia nova que aparecer no caminho vira registro para depois, não código agora.

## Verificar e fechar

Rodar o passo de verificação ponta a ponta que a spec descreve, e daí em diante seguir o ritual
de fechamento do `/aicf:workflow-demanda` — é ele que define o check do projeto, a revisão de
código, o relatório e o arquivamento. Projeto que diverge diz isso no próprio `CLAUDE.md`: ler,
não presumir.

**Só afirmar que funciona depois de ver a saída do comando.**

Preencher a linha `Processo:` com o caminho realmente usado, na forma `entrevista →
implementação` (sem seta quando não houve entrevista).
