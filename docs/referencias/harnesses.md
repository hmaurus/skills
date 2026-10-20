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
- **Instalar por cima limpa o que a versão nova não tem.** Na cópia 0.39.0 desta máquina, que
  veio de um import, `agy plugin install ~/aicf` levou a `0.41.1` e apagou a skill `criar-prd`,
  renomeada para `prd` na `0.40.0` (`ls ~/.gemini/config/plugins/aicf/skills | grep -c criar-prd`
  → 0), sem pedir para desinstalar antes.
- **Não há marketplace para o aicf.** `agy plugin install <plugin>@<marketplace>` só aceita um
  marketplace registrado, e o `agy plugin --help` não tem comando para registrar.
  `aicodingflow`, `claude`, `claude-code`, `gemini`, `antigravity`, `github`, `git`, `official` e
  `agent-marketplace` devolvem `unknown marketplace: <nome>`
  (`HOME=<pasta> agy plugin install aicf@<nome>`). O marketplace dele é o catálogo do Google,
  que instala por ID de listagem
  (`~/.gemini/antigravity-cli/builtin/skills/plugin/SKILL.md`, "Install").
- **`agy plugin import claude` não atualiza a partir do Claude Code.** No HOME real, com o aicf
  0.41.1 instalado no Claude Code, ele responde `No claude extensions found`. A cópia 0.39.0 veio
  de um import (`jq -r '.imports[] | select(.name=="aicf") | .source' ~/.gemini/config/import_manifest.json`
  → `claude-code`), feito por outro caminho que não esse comando.
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
- **Ler as skills de um clone:** `"skills": { "paths": ["~/aicf/skills"] }` no `opencode.json`,
  global ou do projeto. Ele acha as sete, expande o `~` e ignora `midia/`
  (`jq -r '.[] | select(.name=="prd") | .location' s.json` → `<home>/aicf/skills/prd/SKILL.md`).
  Aqui o link simbólico não atrapalha: com `~/aicf` sendo link para o clone, ele também acha as
  sete. A forma em lista, `"skills": ["..."]`, está no schema publicado
  (`curl -s https://opencode.ai/config.json | jq '.properties.skills.anyOf[0].type'` → `"array"`),
  mas o 1.17.11 recusa: `Expected object | undefined, got [...] skills`. O plugin do Superpowers
  soma o caminho dele a `config.skills.paths` sem apagar os que já estão
  (`grep -A6 'config: async' <pacote>/.opencode/plugins/superpowers.js`).
- **Não há como esconder skill do modelo:** o frontmatter só reconhece `name`, `description`,
  `license`, `compatibility` e `metadata`.
