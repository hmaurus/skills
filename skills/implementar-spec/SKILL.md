---
name: implementar-spec
description: Implementa uma demanda a partir da spec e conduz o fechamento até o registro. Invocar quando o usuário pede para implementar uma spec pronta em docs/projeto/specs/; não invocar durante entrevista, nem para tarefa que não tem spec. Caminho aicf da fase de implementação.
---

# Implementar a partir da spec

Com o plan mode ligado, montar o plano e esperar aprovação antes de tocar o disco.

## Antes de escrever código

1. **Ler a spec inteira** — venha de `docs/projeto/specs/<nome>.md`, de
   `docs/superpowers/specs/` ou de uma issue. Se o usuário não disse qual, perguntar em vez de
   adivinhar entre as specs abertas.
2. **Ler os arquivos que a spec nomeia**, e o que já existe de parecido no repositório. A
   segunda parte vai para subagente: procurar o que já existe é leitura ampla, e feita no
   contexto principal ela gasta o que a implementação vai precisar.
3. **Decidir o caminho, com a spec e o código à vista.** A linha `Processo` da spec pode trazer
   `sugestão: <caminho> (motivo)`. Se a sugestão é `aicf-direto` e o diff cabe numa frase, dizer
   a frase e ir — o caso é óbvio e a decisão é do agente. Em qualquer outro caso — sugestão de
   plano ou de outra coleção, spec sem sugestão, demanda que toca vários arquivos ou código
   desconhecido —, perguntar com `AskUserQuestion`, oferecendo só os caminhos instalados (a linha
   "Coleções de skills de workflow instaladas" do `CLAUDE.md` diz quais). Conforme a resposta:
   outra coleção, esta skill para aqui e o caminho escolhido assume, e o fechamento continua
   sendo `/aicf:fechar-demanda`; `aicf-plan`, entrar no plan mode e seguir por esta skill;
   `aicf-direto`, planejar em sessão antes de editar — o plano não vai para arquivo, e na linha
   `Processo` o valor continua `aicf-direto`, porque `aicf-plan` é só com o plan mode ligado.

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
