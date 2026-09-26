# O fechamento não diz se a sessão pode acabar

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

O `fechar-demanda` terminava com "sugerir `/clear` se estiver pesado — não a cada demanda por
reflexo". Sem contexto pesado, a sessão acabava sem sinal nenhum, e o titular passou a perguntar
"já posso fechar a sessão?" ao fim de toda demanda.

## Solução

A última mensagem do fechamento diz se a sessão pode acabar: com nada pendente (commit, push, CI
conferido quando o projeto tem), que já dá para fechar ou dar `/clear`; com algo pendente, o que
falta e quem faz. Fora do plugin, a mesma regra foi para o `~/.claude/CLAUDE.md` do titular, para
sessões sem demanda — decisão dele, entre plugin, global ou os dois.

## Relatório de implementação (2026-09-25)

- **Status** — concluído.
- **Arquivos alterados**
  - `skills/fechar-demanda/SKILL.md` — parágrafo "A última mensagem diz se a sessão pode acabar"
    no lugar da sugestão condicional de `/clear`.
  - `CHANGELOG.md`, `.claude-plugin/plugin.json` — `0.30.1`.
  - Fora do repositório: `~/.claude/CLAUDE.md`, seção "Comunicação com o usuário".
- **Commits** — `fabc1b5` feat(fechar-demanda): a última mensagem diz se a sessão pode acabar
- **Validação** — `./scripts/check.sh` → `Tudo verde.`;
  `grep -c 'A última mensagem diz se a sessão pode acabar' skills/fechar-demanda/SKILL.md` → 1.
  Comportamento: pela regra do `CLAUDE.md`, depende do titular atualizar o plugin e fica para o
  uso real — encerra no primeiro fechamento que termine com o sinal.
- **Escopo efetivo** — sem revisão de código: ajuste de texto de um parágrafo.
