# 0001 — A fronteira entre governança e framework é a fase

Data: 2026-09-08 · Status: aceita · Versão: `0.13.5`

## Contexto

O aicf é governança: registra o que será feito e o que foi feito, e convive no mesmo projeto com
coleções de skills de terceiros (Superpowers, Matt Pocock) que fazem a implementação. Essas
coleções encadeiam skills entre si, às vezes declarando o encadeamento como obrigatório.

Numa execução real (`hmaurus/mh-fin`), o agente pulou o `finishing-a-development-branch` — passo
que o `subagent-driven-development` declara `REQUIRED SUB-SKILL` — porque leu uma garantia do aicf
como exclusão. A demanda foi dada por concluída com o código parado numa branch.

Ao corrigir, apareceu a pergunta que a correção precisava responder: **até onde a governança pode
mandar num processo que não é dela?** Sem critério, "não interferir no framework" não tem borda —
e o texto de terceiro não ajuda a traçá-la: o `brainstorming` do Superpowers declara
`writing-plans` como estado terminal obrigatório, do mesmo jeito que o
`subagent-driven-development` declara o `finishing-a-development-branch`.

## Decisão

**A governança escolhe o caminho de cada fase; dentro da fase, o encadeamento do framework roda
inteiro, automático, sem pedir licença.**

- Passo que um método encadeia **dentro da mesma fase** é interno: não se pula, não se substitui,
  não se pergunta ao usuário. Interferir ali degrada a qualidade de um processo que não é nosso.
- Passo que atravessa **a fronteira entre fases** é da governança, mesmo quando o framework
  recomenda continuar nele. Parar depois do `brainstorming` sem seguir para `writing-plans` é
  legítimo: o design doc dele vale como spec, e a implementação é escolha nova.

Como consequência direta, a **integração** — decidir o destino do código: merge, PR, ou a branch
fica — é o último passo da fase de implementação, e pertence ao método escolhido. O **fechamento**
é só o registro da demanda.

## Alternativas descartadas

- **Entrou num framework, herdou toda a cadeia dele, atravessando fases.** Mais fiel ao texto de
  terceiro, mas escolher `brainstorming` na entrevista comprometeria a implementação com o
  Superpowers, e a independência entre as fases — que é a razão de a governança existir —
  desapareceria na prática.
- **Respeitar só o que a skill marca como `REQUIRED`.** Critério textual, e por isso frágil:
  depende de cada coleção marcar isso, muda a cada versão de terceiro, e obrigaria o agente a
  reler o texto da skill para saber o que pode escolher.
- **Criar uma quinta fase, "integração", no ciclo.** Devolveria a fronteira à governança e
  reintroduziria o bug: a integração voltaria a ser negociável entre fases, quando ela é interna
  ao método.

## Consequências

- O vocabulário do plugin passa a distinguir integração e fechamento, e a distinção é carregada em
  toda sessão pela quarta regra do `CLAUDE.md`, não só pela skill.
- Exigência da governança já satisfeita por um passo do caminho escolhido não se repete — o
  relatório declara qual passo cobriu qual exigência.
- Reverter significaria reescrever o vocabulário das três skills de ciclo e o template do `setup`,
  além de invalidar os relatórios que já declararam equivalências.
