# AGENT — Projeto aicf

## O que é

Plugin de skills para Claude Code que cuida da governança e do planejamento macro de um projeto de software: PRD, checklist de entregas e demandas versionadas, e o ciclo que leva cada demanda da ideia ao registro do que foi feito.

Este repositório é a fonte editável do plugin, publicado no marketplace `aicodingflow`.

## Lema

**Simplicidade e manutenibilidade acima de tudo.** Havendo trade-off entre a solução mais completa e a mais direta, escolher a direta — desde que entregue o resultado. Gatilho de revisão: dois mecanismos coexistindo, sincronização entre estados, ou abstração antecipando o futuro.

**Refatoração contínua:** trecho que ficou mais complexo com o tempo se simplifica antes de receber feature nova.

## Registro

**Memory é atalho do agente — quem precisa saber é o repositório.** Decisões, IDs, gotchas e lições vivem em `docs/`, no `CLAUDE.md` e no código. Memory pode sumir ou ficar desatualizada; validar contra o repositório antes de confiar.

**Exceção:** credenciais ficam em `.env` (não commitado) ou no gerenciador de senhas. Nunca no repositório, nunca em memory.

**Glossário do domínio** (`CONTEXT.md`) e **decisões difíceis de reverter** (ADR em `docs/adr/`, numerado e imutável) nascem quando houver o primeiro termo ambíguo ou a primeira decisão a registrar — o passo 4 do ritual de fechamento manda escrever nos dois.

**Este arquivo é lido inteiro em toda sessão.** O alvo que a documentação do Claude Code publica é abaixo de 200 linhas; regra que só vale para uma parte do código vai para `.claude/rules/<tema>.md` com `paths:` no frontmatter, e procedimento de vários passos vira skill. `/doctor` propõe cortes do que o agente já deduz do código.

## Processos de desenvolvimento

Duas camadas: a **governança** registra o que será feito e o que foi feito, e é sempre a mesma; a **implementação** é como o código sai, e tem caminhos à escolha. Uma demanda passa por quatro fases: demanda → entrevista → implementação → fechamento.

**O mapa do workflow está na skill `/aicf:workflow-demanda`** — ciclo, caminhos de cada fase e nomenclatura; invocar ao começar ou registrar uma demanda. **O fechamento — relatório e ritual — está em `/aicf:fechar-demanda`**, que o agente aplica ao concluir qualquer demanda, por qualquer caminho.

**Coleções de skills de workflow instaladas:** Superpowers, Matt Pocock. _(São os caminhos que o `implementar-spec` pode oferecer além do aicf.)_

Quatro regras valem antes de abrir qualquer doc:

- **Na entrevista, o caminho é pergunta ao usuário; na implementação, o agente segue a sugestão gravada na spec quando o caso é óbvio — caminho aicf direto e diff que cabe numa frase — e pergunta com opções nos demais.** O agente sugere pelo ponto forte que couber ao caso; a decisão é do usuário quando há escolha real.
- **O método escolhido fecha o código; a governança fecha a demanda.** Rodar o processo de implementação inteiro — inclusive o passo de integração que ele encadeia — e só então `/aicf:fechar-demanda`.
- **Bug de causa desconhecida** → depurar de forma sistemática antes de propor correção; se `systematic-debugging` (Superpowers) ou `/diagnosing-bugs` (Matt Pocock) estiverem instalados, usar.
- Operação que se repete vira **skill** em `.claude/skills/`, não improviso na hora.

## Verificação

> A preencher quando houver código. Comando por comando, e o que conta como saída saudável.

- Build: `<comando>` (termina com "...")
- Testes: `<comando>` (tudo verde; nunca pular nem apagar teste que falha)
- Lint, formatação e tipos: `<comando>` (zero avisos)

Rodar tudo antes de dar qualquer tarefa por concluída, e colar a saída. Se um teste falha, corrigir o código, não o teste.

## Git

- **`main`** — única branch. Não há `develop` aqui.
- Commitar direto na branch de trabalho por padrão; branch + PR só para mudança grande ou a pedido.
- O fechamento de uma demanda vai em commit próprio, separado do commit de código.
