---
name: implementar-spec
description: Implementa uma demanda a partir da spec e conduz o fechamento até o registro. Invocar quando o usuário pede para implementar uma spec pronta — arquivo em specs/, ou issue com o label aicf:spec; não invocar durante entrevista, nem para tarefa que não tem spec. Caminho aicf da fase de implementação.
---

# Implementar a partir da spec

## Antes de escrever código

1. **Ler a spec inteira.** A linha `**Mídia do registro:**` do `CLAUDE.md` diz qual arquivo de
   [`workflow-demanda/references/`](../workflow-demanda/references/) seguir — `midia-arquivo.md`
   ou `midia-issues.md`; sem linha, arquivo. Se `docs/agents/issue-tracker.md` discordar da linha,
   avisar uma vez e seguir a linha. A spec também pode vir de fora da governança do aicf, de
   `docs/superpowers/specs/`. Se o usuário não disse qual, **listar as specs abertas pela receita
   da mídia** e perguntar, em vez de adivinhar. Alvo que ainda é intent — arquivo em `intents/`,
   linha do `ROADMAP.md`, ou issue `aicf:intent` — que o usuário mandou implementar sem entrevista:
   virar spec pela receita da mídia, com `entrevista: nenhuma` na linha `Processo`, e seguir.
2. **Ler os arquivos que a spec nomeia**, e o que já existe de parecido no repositório. A
   segunda parte vai para subagente: procurar o que já existe é leitura ampla, e feita no
   contexto principal ela gasta o que a implementação vai precisar.
3. **Decidir o caminho, com a spec e o código à vista.** A linha `Processo` da spec pode trazer
   `sugestão: <caminho> (motivo)`. Se a sugestão é `aicf-direto` e o diff cabe numa frase, dizer
   a frase e ir — o caso é óbvio e a decisão é do agente. Em qualquer outro caso — sugestão de
   plano ou de outra coleção, spec sem sugestão, demanda que toca vários arquivos ou código
   desconhecido —, perguntar com `AskUserQuestion`, oferecendo só os caminhos instalados (a linha
   "Coleções de skills de workflow instaladas" do `CLAUDE.md` diz quais). Conforme a resposta:
   outra coleção, esta skill para aqui e o caminho escolhido assume **até o fim, inclusive a
   integração que ele encadeia** — o aicf não interrompe nem substitui passo interno de método; ao
   terminar, `/aicf:fechar-demanda` registra a demanda. `aicf-plan`, entrar no plan mode, montar o
   plano, esperar aprovação antes de tocar o disco, e seguir por esta skill; `aicf-direto`,
   planejar em sessão antes de editar — o plano não vai para arquivo, e na linha `Processo` o
   valor continua `aicf-direto`, porque `aicf-plan` é só com o
   plan mode ligado.

   **Junto do caminho, decidir o workspace.** O default é o da seção `## Git` do `CLAUDE.md`; sem
   ela, a branch atual. Sair dele é pergunta ao usuário, e o agente propõe quando couber:
   **branch própria** quando vale poder descartar em bloco ou revisar antes de entrar — mais de um
   commit de código, ou área onde erro custa dinheiro ou dado (migration, auth, pagamento);
   **worktree** — outra pasta, com a própria branch — só quando o checkout atual precisa continuar
   em uso (outra sessão, servidor rodando), e nunca quando a verificação depende de estado não
   versionado (`.env`, banco, pasta gitignored): a worktree nasce sem ele. Dizer numa linha o que
   decidiu e por quê — em qualquer caminho, inclusive o de outra coleção, antes de passar a vez.

Se a spec não diz o suficiente para implementar, dizer isso e propor uma rodada de
`/aicf:criar-spec` — não preencher a lacuna por conta própria.

## Implementar

A spec é roteiro, não trilho: ao sair dela (pular etapa, trocar de abordagem, ferramenta que
ela não cita), dizer em uma linha o que vai fazer e por quê, antes de fazer.

**Avaliar se a mudança merece teste, e se merece começar pelo teste.** Correção de bug é o caso
claro dos dois: escrever primeiro o teste que falha, confirmar que falha pelo motivo certo, e
corrigir o código sem tocar no teste. Mudança de texto ou de configuração não pede nenhum dos
dois. No meio, a régua do vizinho: onde o projeto já testa, a mudança entra testada.

Código novo se parece com o código vizinho. Não ampliar o escopo: o que a spec pôs fora de
escopo fica fora, e ideia nova que aparecer no caminho vira registro para depois, não código
agora.

## Verificar e fechar

Rodar o passo de verificação ponta a ponta que a spec descreve — **só afirmar que funciona
depois de ver a saída do comando** — e daí invocar `/aicf:fechar-demanda`, que conduz o ritual
até o registro. **Não presumir o ritual pela memória desta skill.**

**Em branch própria ou worktree, integrar antes do relatório:** checks e revisão do fechamento
rodam na branch; depois, `AskUserQuestion` — merge na branch de origem, PR, ou deixar a branch. O
commit de fechamento vai onde o código ficou.
