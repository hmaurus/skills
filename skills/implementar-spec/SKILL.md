---
name: implementar-spec
description: Implementa uma demanda a partir da spec e conduz o fechamento até o registro. Caminho nativo da fase de implementação — par do `criar-spec`.
disable-model-invocation: true
---

# Implementar a partir da spec

Pega a spec produzida pela entrevista, implementa, verifica e fecha o registro. É a fase de
**implementação** no caminho nativo — sem plugin, só Claude Code. O ciclo inteiro está em
`/aicf:workflow-demanda`.

Funciona igual com o plan mode ligado ou desligado. **Ligar o plan mode é decisão do
usuário, não desta skill:** se estiver ligado, montar o plano e esperar aprovação antes de
tocar o disco; se não estiver, implementar direto.

## Entrada

A spec, venha de onde vier — `docs/projeto/demandas/<nome>.md`, `docs/superpowers/specs/`
ou uma issue. Se o usuário não disse qual, perguntar em vez de adivinhar entre as demandas
abertas.

## Antes de escrever código

1. Ler a spec inteira.
2. Invocar `/aicf:workflow-demanda` — governança, formato do relatório e ritual de
   fechamento vivem lá. Se o projeto tiver `CLAUDE.md` próprio que diverge, ele manda.
   **Não presumir o ritual pela memória desta skill.**
3. Ler os arquivos que a spec nomeia, e o que já existe de parecido no repositório. Código
   novo se parece com o código vizinho.

Se a spec não diz o suficiente para implementar, dizer isso e propor uma rodada de
`/aicf:criar-spec` — não preencher a lacuna por conta própria.

## Implementar

Seguir os padrões que já existem. Não ampliar o escopo: o que a spec pôs fora de escopo
fica fora, e ideia nova que aparecer no caminho vira registro para depois, não código agora.

## Verificar

Rodar o check do projeto — o script do `package.json` (`check`, ou lint + format +
typecheck), **no projeto inteiro, nunca só nos arquivos tocados**. Corrigir o que falhar.

Rodar o passo de verificação ponta a ponta que a spec descreve. Se a mudança foi além de
ajuste de texto, propor revisão de código.

Só afirmar que funciona depois de ver a saída do comando.

## Fechar

Conduzir o ritual de fechamento como `/aicf:workflow-demanda` o define —
tipicamente: relatório no arquivo da demanda, arquivar em `concluidas/`, marcar no
checklist, reler o relatório procurando o que vale além desta demanda, e conferir se a
execução criou ou tornou obsoleto algum item.

Projeto que diverge diz isso no próprio `CLAUDE.md`. Ler, não presumir.

Preencher a linha `Processo:` com o caminho realmente usado, na forma
`entrevista → implementação` (sem seta quando não houve entrevista).

O fechamento vai em commit próprio, separado do commit de código.
