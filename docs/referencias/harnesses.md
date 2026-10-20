# Testar o aicf em cada harness

Como exercitar o plugin fora do Claude Code sem mexer nas cópias instaladas, e os limites que cada
harness impõe. Alvo e compatível estão no [`GLOSSARY.md`](../../GLOSSARY.md). Comandos rodados em
2026-10-20 com `agy` 1.4.2, `codex` 0.163.0 e `opencode` 1.17.11 (`<cli> --version`).

## Antigravity (`agy`)

- **Limite:** os primeiros 24.000 bytes de cada `SKILL.md` e de cada arquivo de regra
  (`AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md`); o resto se descarta sem erro. Doc em
  `~/.gemini/antigravity-cli/builtin/skills/agy-customizations/docs/rules.md`, seção "Size Limits".
  O `scripts/check.sh` cobre o `SKILL.md`; o arquivo de regra, não.
- **Validar o plugin como o `agy` o vê** — ele converte o plugin do Claude Code ao instalar, e o
  `validate` na raiz do repositório só diz isso:

  ```bash
  T=$(mktemp -d); mkdir $T/aicf; cp -r skills .claude-plugin $T/aicf/
  echo '{"name":"aicf"}' > $T/aicf/plugin.json; agy plugin validate $T/aicf
  ```

- **Instalar sem tocar no `agy` de verdade:** `HOME=<pasta> agy plugin install <clone>`. Instalar
  de novo por cima atualiza (a versão sobe para a do clone), e a pasta `midia/` vai junto.
  `agy plugin install aicf@aicodingflow` falha com `unknown marketplace`: ele não lê o marketplace
  do Claude Code.
- **Coleções e MCPs:** `agy plugin list --json` traz `name`, `enabled` e `version`; `agy mcp list`
  traz o nome do servidor (`context7`).

## Codex

- **Esconder skill do modelo:** `agents/openai.yaml` na pasta da skill, com
  `policy:` / `allow_implicit_invocation: false`. Ele ignora o `disable-model-invocation`.
- **Listar o que o modelo vê:** num repositório git com as skills em `.agents/skills/`,
  `codex exec -s read-only "Sem executar comandos: liste os nomes das skills do seu contexto cujo caminho fica em .agents/skills. Só a lista."`
- **Instalar sem tocar no Codex de verdade:** `CODEX_HOME=<pasta>`, com `codex plugin marketplace
  add hmaurus/skills` e `codex plugin add aicf@aicodingflow`. O `codex exec` nessa pasta não tem
  login; só os comandos de plugin funcionam.
- **Testar a atualização:** `marketplace add --ref vX.Y.Z` instala uma versão antiga; tirar a
  linha `ref` do `config.toml` e rodar `codex plugin marketplace upgrade aicodingflow` leva a cópia
  instalada à versão do `main`. Marketplace por caminho local ou `file://` não serve para isso: o
  `upgrade` só aceita marketplace git.

## opencode

- **Achar as skills:** `opencode debug skill > s.json; jq -r '.[].name' s.json` — direto num pipe
  a saída sai cortada e o `jq` acusa `parse error` —, num repositório git com as skills
  copiadas em `.opencode/skills/` ou `.agents/skills/`, ou com `HOME=<pasta>` e
  `XDG_CONFIG_HOME=<pasta>/.config` para o global `~/.config/opencode/skills/`. Com link simbólico
  ele acha zero; a pasta sem `SKILL.md` (`midia/`) ele ignora.
- **Não há como esconder skill do modelo:** o frontmatter só reconhece `name`, `description`,
  `license`, `compatibility` e `metadata`.
