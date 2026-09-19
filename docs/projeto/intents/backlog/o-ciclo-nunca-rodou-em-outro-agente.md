# O ciclo nunca rodou em outro agente além do Claude Code

Processo — entrevista: a definir · implementação: a definir

> **Encerra quando** alguém rodar o ciclo inteiro — setup, entrevista, implementação, fechamento —
> num agente que lê o padrão Agent Skills (Codex, OpenCode, Cursor) e registrar aqui o que quebrou
> e o que passou; ou quando a revisão do PRD concluir que a porta se fecha, e este arquivo for
> para `specs/concluidas/` com o motivo.
>
> **Não é pendência.** O [PRD](../../PRD.md) deixa outros agentes fora do escopo, com a porta
> aberta. Este arquivo registra que a porta nunca foi testada, para que ninguém afirme que o plugin
> funciona lá, nem que não funciona.

## O que se sabe sem testar

Levantado em 2026-09-19, na entrevista do PRD.

- **O formato é portável.** `SKILL.md` com `name` e `description` é o padrão aberto Agent Skills;
  `curl -s https://agentskills.io/llms.txt` lista os clientes que o leem. Copiar `skills/` para a
  pasta que o agente lê é o caminho de instalação lá.
- **O empacotamento não é.** `.claude-plugin/` e o marketplace são do Claude Code. Fora dele não
  há `/plugin install`.
- **`disable-model-invocation: true`** (`setup`, `criar-prd`) está fora do mínimo do padrão. Outro
  agente pode invocar as duas sozinho.
- **A prosa cita ferramentas do Claude Code** em 20 pontos
  (`grep -rnoE 'AskUserQuestion|plan mode|/clear|\.claude/rules|hooks?' skills/ --include='*.md' | wc -l`),
  e toda referência cruzada usa a sintaxe `/aicf:nome`, que cada agente escreve de outro jeito.
- **`CLAUDE.md` já está coberto:** o setup gera `AGENTS.md` como link simbólico, e o caso em que o
  `AGENTS.md` já existe está tratado na skill.

## O que decidir na entrevista, se ela acontecer

- Se o teste passar com ajustes pequenos, neutralizar a prosa vale o custo, ou basta uma nota no
  README dizendo o que copiar e o que ignorar?
- Se falhar em algo estrutural, a porta se fecha no PRD, e o motivo entra lá.
