# O `/aicf:setup` não avisa que o Matt Pocock faz a mesma pergunta

Processo — entrevista: a definir · implementação: a definir

> **Encerra quando** o `/aicf:setup`, no momento da escolha de mídia, disser ao usuário que o
> `/setup-matt-pocock-skills` responde a mesma pergunta e que os dois podem apontar para o mesmo
> lugar — ou quando a entrevista concluir que o aviso não se paga, e este arquivo for para
> `concluidas/` com o motivo.
>
> **Não reabrir por divergência observada:** divergir é comportamento declarado, não defeito. O que
> falta é o usuário saber que está escolhendo.

## Problema

As duas coleções perguntam **onde o trabalho mora**, e as respostas vivem em arquivos diferentes: a
do aicf na linha `**Mídia do registro:**` do `CLAUDE.md`, a do Matt em `docs/agents/issue-tracker.md`.
Elas podem discordar, e discordar é legítimo — o que cada uma guarda não é a mesma coisa.

O aicf já faz o que dá sem tocar em nada alheio: no setup, lê o arquivo do Matt **se ele existir** e
propõe o default a partir dele; nas demais skills, avisa uma vez quando as duas discordam e segue a
linha do `CLAUDE.md` (`grep -rn "issue-tracker.md" skills/` mostra os cinco pontos).

**O que falta é a informação chegar a quem decide.** Três buracos:

1. **Quem roda o `/aicf:setup` primeiro** — o arquivo do Matt ainda não existe, então não há o que
   ler, e depois o `/setup-matt-pocock-skills` pergunta do zero sem olhar para o `CLAUDE.md`. As
   duas respostas nascem independentes, e ninguém disse que eram a mesma pergunta.
2. **Quem quer alinhar não sabe que dá.** O setup do Matt aceita um tracker "other" e escreve o
   `issue-tracker.md` a partir da descrição do usuário — dá para apontá-lo para a mesma pasta do
   aicf. O `workflow-demanda` já prevê o caso (*"ou `specs/<nome>.md`, se o tracker configurado no
   setup apontar para lá"*), mas essa frase está numa tabela que quem está no setup não lê.
3. **Divergir tem custo concreto.** Com o aicf em arquivo e o Matt em `.scratch/`, entrevistar pelo
   `to-spec` deixa a spec em dois lugares e nada reconcilia. A adoção por `/aicf:criar-spec #<n>`
   resolve só o caso em que **os dois** estão em issue no mesmo repositório.

## Restrição

**O aicf não escreve em configuração de coleção alheia.** Decidido em 2026-09-18, e é a mesma
posição do [ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md): ler para propor,
nunca gravar. A saída desta demanda é **instruir**, não configurar — e uma pergunta do tipo "quer
que eu escreva o `issue-tracker.md` apontando para cá?" está fora de escopo por essa decisão, não
por custo.

## O que decidir na entrevista

- **Onde o aviso entra, se entrar.** O candidato óbvio é junto da pergunta da mídia, que é onde a
  decisão acontece. Mas o setup acabou de ganhar uma apresentação curta em
  [a entrada de quem chega](../concluidas/a-entrada-de-quem-chega.md), cuja Restrição era
  não virar muro — e mais um parágrafo sobre coleção alheia, antes da primeira ação útil, é
  exatamente o defeito que aquela demanda consertou. A despedida é a alternativa: a decisão já foi
  tomada, mas ali o aviso chega tarde para mudá-la.
- **Só quando o Matt está instalado.** Explicar a interação com uma coleção que o usuário não tem é
  ruído garantido. O setup já pergunta quais coleções estão instaladas, então o dado existe — mas a
  pergunta das ferramentas vem **depois** da pergunta da mídia hoje
  (`grep -n '^## ' skills/setup/SKILL.md` mostra a ordem). Ou o aviso muda de lugar, ou as perguntas
  mudam de ordem, ou o aviso aceita sair sem saber.
- **Quem instala o Matt depois.** O setup já rodou, o `CLAUDE.md` já está escrito, e nada avisa
  nada. Vale aceitar esse caso como descoberto, ou o aviso pertence a outro lugar que não o setup?
- **O aviso instrui ou só informa?** "As duas coleções guardam coisas diferentes, e divergir é
  normal" é informação. "Se quiser os dois no mesmo lugar, o setup do Matt aceita um caminho
  próprio" é instrução, e é a parte que hoje ninguém descobre sozinho.

## Origem

Levantado em 2026-09-18, numa pergunta sobre o funcionamento atual: *"se no setup o usuário escolher
issue, isso já padroniza também para o Matt Pocock?"* A resposta é não, e a decisão de manter assim
foi confirmada na mesma conversa. O que sobrou foi a lacuna de comunicação, que virou este item.
