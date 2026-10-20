# O fechamento só mede o CLAUDE.md em linhas

Processo — entrevista: nenhuma · implementação: aicf-direto

Achado pela revisão de código de [o aicf quebra fora do Claude Code](../concluidas/o-ciclo-nunca-rodou-em-outro-agente.md),
registrado no Backlog do `ROADMAP.md` no fechamento dela e corrigido no mesmo dia, a pedido do
titular.

## Problema

O passo 3 do `/aicf:fechar-demanda` e o template do `CLAUDE.md` mandavam conferir o tamanho do
`CLAUDE.md` pelo alvo de 200 linhas do Claude Code. O Antigravity lê o mesmo arquivo pelo
`AGENTS.md` e carrega só os primeiros 24.000 bytes, descartando o resto sem avisar
(`~/.gemini/antigravity-cli/builtin/skills/agy-customizations/docs/rules.md`, seção "Size
Limits"). As duas medidas não andam juntas: o `.claude/CLAUDE.md` deste repositório tem 16.697
bytes em 85 linhas (`wc -lc .claude/CLAUDE.md`), e nesse ritmo 200 linhas dariam uns 39.000 bytes.
Quem seguisse o plugin ao pé da letra podia passar do corte sem perceber.

Nenhum `AGENTS.md` desta máquina passa do corte hoje; o maior, num projeto privado, tem 20.858
bytes (`wc -c ~/dev/*/AGENTS.md | sort -rn | sed -n 2p`, cuja primeira linha é o total).

## Relatório de implementação (2026-10-20)

- **Status** — concluído na `0.41.1`.
- **Arquivos alterados**
  - `skills/fechar-demanda/SKILL.md` — o passo 3 cita os dois limites e o comando que mede os dois
  - `skills/setup/templates/claude-md.md` — a mesma frase no parágrafo "Este arquivo é lido inteiro"
  - `docs/projeto/ROADMAP.md` — o item sai do Backlog
  - `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.41.1`
- **Commits** — o desta demanda, código e fechamento juntos, por ser tarefa pequena.
- **Validação** — `grep -c '24.000 bytes' skills/fechar-demanda/SKILL.md
  skills/setup/templates/claude-md.md` → 1 e 1; `./scripts/check.sh` → `Tudo verde.`
- **Escopo efetivo** — o `.claude/CLAUDE.md` deste repositório ficou como estava: o `AGENTS.md`
  da raiz é uma linha com um link para ele, não o mesmo arquivo, então o corte não o alcança.
- **Lições** — a condição de encerramento escrita no Backlog ("quando um `CLAUDE.md` passar de
  20.000 bytes") dizia quando o item ficava urgente, não quando acabava; quem fechou foi a
  correção, que era uma frase.
