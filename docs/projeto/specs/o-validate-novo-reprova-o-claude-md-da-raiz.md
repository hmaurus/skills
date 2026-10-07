# O `validate` do Claude Code 2.1.292 reprova o `CLAUDE.md` da raiz

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (um `git mv`, um symlink, sete links e uma linha do CI, sem decisão de abordagem em aberto)

## Problema

O `./scripts/check.sh` sai com 1 na máquina de quem desenvolve, com o repositório intacto, e o CI
continua verde. Enquanto isso durar, o check local fica sempre vermelho, e uma falha de verdade
passa despercebida no meio. Vem antes de [o Matt renomeou o glossário](../intents/o-matt-renomeou-o-glossario.md),
por escolha do usuário: aquela demanda vai precisar do check confiável.

A causa é um aviso novo do validador. Com o Claude Code 2.1.292, `claude plugin validate . --strict`
(linha 44 do `scripts/check.sh`) devolve:

```
❯ root: CLAUDE.md at the plugin root is not loaded as project context. To ship context with your plugin, use a skill (skills/<name>/SKILL.md) instead.
✘ Validation failed (--strict treats warnings as errors)
```

O `marketplace.json` declara o plugin com `"source": "./"`, então a raiz do repositório é a raiz do
plugin, e o `CLAUDE.md` de quem desenvolve o aicf fica nela. O CI passa porque fixa o
`@anthropic-ai/claude-code@2.1.278` (linha 26 do `.github/workflows/ci.yml`), que não tem o aviso.
Não é efeito de mudança do repositório: em 2026-10-06, com as mudanças do `920851a` desfeitas, o
check saiu com 1 do mesmo jeito.

## Solução

O `CLAUDE.md` passa a morar em `.claude/CLAUDE.md`, caminho que o Claude Code também carrega como
contexto do projeto no início da sessão. O validador só olha a raiz do plugin, então o aviso some e
o `--strict` continua valendo para tudo o mais.

Testado numa cópia do repositório em 2026-10-06, com o 2.1.292:

- depois do `git mv`, `claude plugin validate . --strict` sai com 0;
- o `--strict` continua pegando o `plugin.json`: com um campo `bogus` acrescentado, o mesmo comando
  sai com 1 e acusa `plugins[0] plugin.json → bogus: Unknown field 'bogus'`;
- `python3 scripts/check_links.py` acusa 7 links quebrados, todos listados abaixo.

O pin do CI sobe para `2.1.292` no mesmo commit, como manda a seção de verificação do `CLAUDE.md`
(quando o check local reprova com uma versão mais nova que a pinada, o pin sobe).

## Arquivos e interfaces

- `CLAUDE.md` → `.claude/CLAUDE.md`, por `git mv`. Os 6 links relativos dele (linhas 23, 25, 27, 29,
  31 e 39 hoje) ganham `../` na frente, porque a base mudou de pasta.
- `AGENTS.md` — continua symlink, agora para `.claude/CLAUDE.md` (`ln -sfn .claude/CLAUDE.md AGENTS.md`).
  O validador não reclama dele hoje; se um dia reclamar, é demanda nova.
- `docs/projeto/concluidas/anonimizar-as-referencias-ao-projeto-privado.md:137` — o link
  `../../../CLAUDE.md` passa a apontar para `../../../.claude/CLAUDE.md`.
- `.github/workflows/ci.yml:26` — `@anthropic-ai/claude-code@2.1.278` vira `@2.1.292`.
- Sem bump de versão nem entrada no `CHANGELOG.md`: nada muda para quem instala o plugin, e as
  mudanças anteriores só no `CLAUDE.md` (`9538332`, `7373eea`) também não tiveram bump.

As menções a "`CLAUDE.md` da raiz" no `README.md`, no `README.en.md` e nas skills falam do projeto de
quem usa o plugin, não deste repositório, e ficam como estão.

## Fora de escopo

- **Plugin numa subpasta** (`"source": "./plugin"`). Também resolveria, e ainda deixaria de instalar
  `docs/` no cache de quem usa, mas muda o caminho de `skills/` em muita coisa. Descartado por custo.
- **Filtrar o aviso no `check.sh`** lendo `--json`. O aviso vem com `"code": null`, então o filtro
  casaria pelo texto da mensagem e quebraria quando o validador mudasse a frase.
- **Tirar o `--strict` da linha 44.** Perderia os avisos de campo desconhecido e de metadado faltando
  nos manifestos.

## Verificação

1. `./scripts/check.sh` com o Claude Code 2.1.292 termina em `Tudo verde.` e sai com 0, com
   `N links conferidos, 0 quebrados` e os dois `✔ Validation passed`.
2. O `--strict` ainda morde: acrescentar `"bogus": 1` ao `.claude-plugin/plugin.json`, conferir que
   `git diff --stat` mostra o arquivo alterado, rodar `claude plugin validate . --strict` e ver a
   saída 1 com `Unknown field 'bogus'`; depois `git checkout .claude-plugin/plugin.json`.
3. `readlink AGENTS.md` devolve `.claude/CLAUDE.md`, e `test -f CLAUDE.md` falha.
4. Depois do push, `gh run list --workflow=ci.yml --limit 1` → `completed success`, rodando com o
   2.1.292.
5. O `CLAUDE.md` continua carregando: numa sessão nova neste repositório, `/memory` lista
   `.claude/CLAUDE.md` como memória do projeto. Depende do titular abrir a sessão; encerra no
   próximo uso real, e o relatório diz isso em vez de prometer o teste.
