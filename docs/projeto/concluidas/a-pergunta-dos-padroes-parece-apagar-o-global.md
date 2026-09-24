# A pergunta dos padrões parece apagar o global, e a detecção se anuncia tarde

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

Dois achados da passada da `0.28.0` no ramo arquivo, em 2026-09-23
(`~/.claude/projects/-home-mh-dev-tmp-app2/*.jsonl`), registrados em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md):

1. **"Nenhum dos dois" lê como remoção.** A pergunta dos padrões de engenharia oferecia *No global*,
   *No projeto* e *Nenhum dos dois*. Para quem já tem o `~/.claude/CLAUDE.md` pronto, a escolha certa
   era a terceira — e o rótulo dizia o contrário: parecia que o projeto ficaria sem padrão. A
   pergunta falava de *onde colar*, quando o que o usuário decide é *o que acontece com o que já
   existe*. Crítica do titular, vendo a tela da passada.
2. **A detecção se anunciou depois do commit.** O agente detectou as coleções certas e não
   perguntou — mas só as citou no resumo final. A linha existe para o usuário corrigir antes de os
   arquivos nascerem, e o roteiro não dizia em que momento ela vai.

## Solução

A pergunta dos padrões passa a ter duas formas, conforme o setup encontra ou não padrões no global
(seção equivalente a alguma de `templates/preferencias.md`):

- **Global com padrões:** *Manter o global como está* (default, nada é escrito), *Completar o global*
  (só as seções que faltam lá) e *Acrescentar no projeto* (o `CLAUDE.md` do projeto recebe só as
  seções que o global não tem).
- **Sem global:** *No global*, *No projeto* e *Não usar*.

E a linha do que a detecção achou vai no texto que acompanha a pergunta da mídia.

**Decidido:** *Acrescentar no projeto* soma ao global em vez de copiar tudo. Serve a quem trabalha
sozinho, que é o público do caso; para equipe, o global não viaja no `git clone` e o colega
receberia só metade do padrão — o roteiro diz isso numa linha, e quem precisa copia o resto à mão.
Uma quarta opção, "copiar tudo para o projeto", ficou de fora para a pergunta não crescer por um caso
que não é o de quem usa o método hoje.

## Relatório de implementação (2026-09-24)

**Status:** concluído no roteiro; a verificação de comportamento é do titular, pela passada da
`0.29.0` descrita em [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md) — o
`setup` tem `disable-model-invocation`.

**Arquivos alterados**

- `skills/setup/SKILL.md` — a pergunta dos padrões nas duas formas; "Os padrões de engenharia"
  reescrita pelas seis opções; a linha da detecção presa à pergunta da mídia.
- `README.md`, `README.en.md` — o setup procura as ferramentas na máquina em vez de perguntar.
- `.claude-plugin/plugin.json`, `CHANGELOG.md` — `0.29.0`.

**Commits**

- `90f5f7b` feat(setup): a pergunta dos padrões fala do que já existe, e a detecção se anuncia antes do commit

**Validação** — `./scripts/check.sh` → `Tudo verde.`; nenhuma ocorrência de "Nenhum dos dois" no
roteiro (`grep -ci 'nenhum dos dois' skills/setup/SKILL.md` → 0). Mudança de texto, sem revisão
por subagente.

**Promoção (passo 3):** nada além do doc de verificação, que recebeu as condições da passada.
