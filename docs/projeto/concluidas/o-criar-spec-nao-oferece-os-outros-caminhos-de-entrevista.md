# O criar-spec invocado direto não oferece os outros caminhos de entrevista

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

A regra da entrevista do `CLAUDE.md` diz que o caminho da entrevista é pergunta ao usuário, com
o critério para sugerir `criar-spec`, `brainstorming` ou `grill-with-docs`. Quem digitava
`/aicf:criar-spec` como porta de entrada nunca via esse critério: a skill era o caminho aicf e
entrevistava direto. Em 2026-10-25, o titular rodou o comando numa demanda do `ROADMAP.md` e não
soube dizer se o agente tinha escolhido o aicf ou só seguido a skill.

## Solução

Um parágrafo no "Antes de perguntar" do `criar-spec`: invocado sem conversa anterior, depois de
ler o que a demanda toca, se o critério do `CLAUDE.md` apontar com clareza para `brainstorming` ou
`grill-with-docs` e a coleção estiver na linha "Coleções de skills de workflow instaladas", a
skill diz qual e por quê numa frase e pergunta se troca. No caso que não é claro, ou sem a
coleção, segue sem comentar.

## Relatório de implementação (2026-10-25)

- **Status** — concluído; CI run `40166648513` → `completed success`; release `v0.45.0`
  (`gh release list --limit 1`). `agy plugin validate` → `✔ Validation passed`.
- **Arquivos alterados**
  - `skills/criar-spec/SKILL.md` — parágrafo "Invocado sem conversa anterior, conferir o caminho
    da entrevista".
  - `CHANGELOG.md`, `.claude-plugin/plugin.json` — `0.45.0`.
- **Commits** — `c49201b` feat(criar-spec): 0.45.0 — invocado direto, confere o caminho da
  entrevista
- **Validação** — `./scripts/check.sh` → `Tudo verde.`;
  `grep -c 'conferir o caminho da entrevista' skills/criar-spec/SKILL.md` → 1. Comportamento,
  por subagente que leu o `.claude/CLAUDE.md` e a skill: num pedido de desenho aberto ("não sei
  qual desenho"), a primeira mensagem ofereceu o `brainstorming`; num pedido de decisão pontual,
  seguiu sem comentar. A sessão real numa `0.45.0` instalada fica para o uso: encerra o primeiro
  `/aicf:criar-spec` invocado direto numa demanda de desenho aberto que ofereça o `brainstorming`
  antes da primeira pergunta.
- **Escopo efetivo** — sem revisão de código: ajuste de texto de um parágrafo, coberto pelo teste
  de comportamento. O passo 3 não promoveu nada: a regra vive na própria skill.
