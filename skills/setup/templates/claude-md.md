# AGENT — Projeto \<NOME\>

## O que é

> A preencher.

## Lema

**Simplicidade e manutenibilidade acima de tudo.** Havendo trade-off entre a solução mais completa e a mais direta, escolher a direta — desde que entregue o resultado. Gatilho de revisão: dois mecanismos coexistindo, sincronização entre estados, ou abstração antecipando o futuro.

**Refatoração contínua:** trecho que ficou mais complexo com o tempo se simplifica antes de receber feature nova.

## Registro

**Memory é atalho do agente — quem precisa saber é o repositório.** Decisões, IDs, gotchas e lições vivem em `docs/`, no `CLAUDE.md` e no código. Memory pode sumir ou ficar desatualizada; validar contra o repositório antes de confiar.

**Exceção:** credenciais ficam em `.env` (não commitado) ou no gerenciador de senhas. Nunca no repositório, nunca em memory.

**Glossário do domínio** (`CONTEXT.md`) e **decisões difíceis de reverter** (ADR em `docs/adr/`, numerado e imutável) nascem quando houver o primeiro termo ambíguo ou a primeira decisão a registrar — o passo 4 do ritual de fechamento manda escrever nos dois.

## Processos de desenvolvimento

Duas camadas: a **governança** registra o que será feito e o que foi feito, e é sempre a mesma; a **implementação** é como o código sai, e tem caminhos à escolha. Uma demanda passa por quatro fases: demanda → entrevista → implementação → fechamento.

**O workflow completo está na skill `/aicf:workflow-demanda`** — ciclo, caminhos de cada fase, nomenclatura, formato do relatório e ritual de fechamento. Invocar ao começar, rodar ou fechar uma demanda.

Três regras valem antes de abrir qualquer doc:

- **Qual caminho usar na entrevista e na implementação é pergunta ao usuário, não dedução.** O agente sugere pelo ponto forte que couber ao caso; a decisão é do usuário.
- **Bug de causa desconhecida** → depurar de forma sistemática antes de propor correção; se `systematic-debugging` (Superpowers) ou `/diagnosing-bugs` (Matt Pocock) estiverem instalados, usar.
- Operação que se repete vira **skill** em `.claude/skills/`, não improviso na hora.

## Git

- **`develop`** — branch de trabalho. **`main`** — produção.
- Commitar direto na branch de trabalho por padrão; branch + PR só para mudança grande ou a pedido.
- O fechamento de uma demanda vai em commit próprio, separado do commit de código.
