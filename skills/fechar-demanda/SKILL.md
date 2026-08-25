---
name: fechar-demanda
description: Ritual de fechamento de uma demanda — checks, revisão, relatório, arquivamento e promoção de conhecimento. Aplicar proativamente ao concluir qualquer demanda, por qualquer caminho de implementação.
---

# Fechar uma demanda

Não importa por onde a demanda começou, ela termina aqui — e o agente aplica o fechamento
proativamente, sem esperar pedido.

## Antes do relatório

Rodar o script de check do projeto (lint + format + typecheck) **no projeto inteiro, nunca só
nos arquivos tocados**, e propor revisão de código quando a mudança for além de ajuste de texto
— `/code-review`, subagente fresco que não viu a implementação, ou o code review do harness.
Reler o próprio diff na mesma sessão é a opção mais fraca: o agente defende o que acabou de
escrever.

## Os cinco passos

1. **Relatório** no arquivo da demanda. Se a demanda não tinha arquivo, criar agora.
2. **Mover** para `concluidas/`.
3. **Marcar `- [x]`** no checklist ou no PLANO.
4. **Reler o próprio relatório procurando o que vale além desta demanda** — decisão que outra
   sessão vai reencontrar, armadilha que vai morder de novo, ID externo — e promover, porque
   ninguém abre demanda concluída procurando informação: conhecimento operacional → doc de
   referência; regra que muda como o agente age → `CLAUDE.md`; decisão difícil de reverter,
   surpreendente e com trade-off real → ADR numerado e imutável em `docs/adr/` (`0001-slug.md`);
   termo ambíguo do domínio → glossário em `CONTEXT.md`. Os dois últimos saem de
   `/domain-modeling`, que o agente invoca em qualquer processo — não depende das skills do Matt.
5. **Conferir se a execução criou item novo no checklist/PLANO ou tornou algum obsoleto**, e
   ajustar inline.

O fechamento vai num commit próprio, separado do commit de código; quando o processo escolhido já
commitou por conta própria, cobre só o registro. Tarefa pequena (fix trivial, copy, renomeação)
cabe num commit, e a demanda pode nascer já no fechamento: o relatório registra o que foi feito
e o arquivo vai direto para `concluidas/`. Ao final, avaliar o peso do contexto e sugerir
`/clear` se estiver pesado — não a cada demanda por reflexo.

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

## A linha `Processo:`

Logo abaixo do título da demanda, na forma `entrevista → implementação`; **sem seta significa
que não houve entrevista**. Processo com pipeline próprio dos dois lados leva só o nome dele;
processo que publica fora do repositório carrega as referências na linha — issue fechada não se
perde, mas não aparece em `grep` nem em `git log -S`.

```
Processo: nativo-direto
Processo: grill-with-docs → nativo-plan
Processo: mattpocock — issues #12, #13, #14
```

## Prompt para a próxima sessão

Quando o usuário pedir o prompt para a próxima demanda (para copiar após `/clear`), entregar
**cercado por uma linha só com `---` acima e outra abaixo**, sem rótulos nem cercas de código, e
com **linha em branco entre cada `---` e o corpo** — senão o markdown transforma a última linha
em título e come o delimitador.

O corpo é autocontido: contexto, o que ler, escopo, fora de escopo, skills obrigatórias, checks,
DoD, branch, ritual de fechamento. O teste: a próxima sessão, fria, executa lendo só ele e o que
ele mandar ler — sem impedi-la de investigar mais se achar que precisa.
