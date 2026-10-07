# O `validate` do Claude Code 2.1.292 reprova o `CLAUDE.md` da raiz

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

O `./scripts/check.sh` sai com 1 na máquina de quem desenvolve, com o repositório intacto, e o CI
continua verde. Enquanto isso durar, o check local fica sempre vermelho, e uma falha de verdade
passa despercebida no meio. Vem antes de [o Matt renomeou o glossário](../specs/o-matt-renomeou-o-glossario.md),
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
- `AGENTS.md` — deixa de ser symlink e vira um arquivo de uma linha, com o link para
  `.claude/CLAUDE.md`. Decidido na implementação: como symlink para `.claude/CLAUDE.md`, quem lê o
  `AGENTS.md` na raiz recebe links escritos a partir de `.claude/` (`../docs/...`), que dali apontam
  para fora do repositório — o `check_links.py` acusou os 6. O validador não reclama do `AGENTS.md`
  hoje; se um dia reclamar, é demanda nova.
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
3. `test -L AGENTS.md` e `test -f CLAUDE.md` falham, e `grep -c '.claude/CLAUDE.md' AGENTS.md` devolve 1.
4. Depois do push, `gh run list --workflow=ci.yml --limit 1` → `completed success`, rodando com o
   2.1.292.
5. O `CLAUDE.md` continua carregando: numa sessão nova neste repositório, `/memory` lista
   `.claude/CLAUDE.md` como memória do projeto. Depende do titular abrir a sessão; encerra no
   próximo uso real, e o relatório diz isso em vez de prometer o teste.

## Relatório de implementação (2026-10-06)

- **Status** — concluído. CI run `37556277712` → `completed success`, rodando o Claude Code 2.1.292
  (`gh run view 37556277712 --log | grep 'Claude Code: '`).
- **Causa raiz** — o `marketplace.json` declara o plugin com `"source": "./"`, então o `CLAUDE.md`
  deste repositório estava na raiz do plugin, e o 2.1.292 passou a avisar que ali ele não é
  carregado como contexto; o `--strict` transforma o aviso em erro. Nenhuma mudança do repositório
  causou a falha.
- **Arquivos alterados**
  - `CLAUDE.md` → `.claude/CLAUDE.md`, com os 6 links relativos prefixados por `../`.
  - `AGENTS.md` — de symlink para arquivo de uma linha com o link para `.claude/CLAUDE.md`.
  - `docs/projeto/concluidas/anonimizar-as-referencias-ao-projeto-privado.md` — o link para o
    `CLAUDE.md` passa a apontar para `.claude/CLAUDE.md`.
  - `.github/workflows/ci.yml` — pin de `2.1.278` para `2.1.292`.
- **Commits**
  - `430ed1a` docs(projeto): spec do validate que reprova o CLAUDE.md da raiz
  - `de58acf` fix(ci): o CLAUDE.md vai para .claude/ e o pin do CI sobe para 2.1.292
- **Validação**
  - Passo 1: `./scripts/check.sh` com o 2.1.292 → `161 links conferidos, 0 quebrados`, os dois
    `✔ Validation passed`, `Tudo verde.`, saída 0.
  - Passo 2: com `"bogus": 1` no `plugin.json` (`git diff --stat` mostrou o arquivo alterado),
    `claude plugin validate . --strict` saiu com 1 e acusou `Unknown field 'bogus'`; arquivo
    restaurado com `git checkout`.
  - Passo 3: `test -L AGENTS.md` e `test -f CLAUDE.md` saem com 1; `grep -c '.claude/CLAUDE.md' AGENTS.md` → 1.
  - Passo 4: o run acima, com `Tudo verde.` no log.
  - Passo 5, **em aberto**: conferir numa sessão nova que `/memory` lista `.claude/CLAUDE.md` como
    memória do projeto. Depende do titular abrir a sessão; encerra no próximo uso real deste
    repositório.
  - Sem revisão de código: a mudança move um arquivo, troca um symlink por uma linha de texto e
    altera um número de versão no CI, sem lógica nova. O `check.sh` cobre os links.
- **Escopo efetivo** — o `AGENTS.md` divergiu da spec. Ela previa reapontar o symlink, mas o
  `check_links.py` acusou os 6 links do `CLAUDE.md` lidos pelo caminho do `AGENTS.md`: quem o lê na
  raiz recebe `../docs/...`, que dali sai do repositório. Por decisão do usuário, ele virou um
  arquivo-ponteiro. As outras duas opções eram links a partir da raiz (`/docs/...`) ou fazer o
  check pular symlink, e a segunda escondia um defeito real.
- **Lições** — symlink para arquivo de outra pasta carrega os links relativos da pasta de origem.
  Isso vale para qualquer markdown que se lê por um symlink.
- **Promoção (passo 3)** — um parágrafo no [`.claude/CLAUDE.md`](../../../.claude/CLAUDE.md),
  seção "O que é": onde o arquivo mora, por quê, e por que o `AGENTS.md` não é symlink.
