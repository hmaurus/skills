# O Antigravity e o opencode estão sem o aicf atual

Processo — entrevista: criar-spec · implementação: aicf-direto

Vem depois de [o aicf quebra fora do Claude Code](../concluidas/o-ciclo-nunca-rodou-em-outro-agente.md),
que escreveu no README os comandos de instalar e atualizar em cada harness. Rodá-los nesta máquina
é o que os prova. Decidido pelo titular em 2026-10-20.

## Problema

Nesta máquina, o Claude Code e o Codex já estão na `0.41.1`. Foram atualizados em 2026-10-20 pelos
comandos do README (`claude plugin list --json | jq -r '.[] | select(.id=="aicf@aicodingflow") | .version'`
e `codex plugin list | grep aicf@`). Os outros dois ficaram para trás:

- **Antigravity:** a cópia está na `0.39.0`
  (`agy plugin list --json | jq -r '.[] | select(.name=="aicf") | .version'`). Ela veio de um
  `agy plugin import` a partir do Claude Code
  (`jq -r '.imports[] | select(.name=="aicf") | .source' ~/.gemini/config/import_manifest.json` →
  `claude-code`, importada em 2026-10-19T14:55:32Z) e ainda tem a skill `criar-prd`, que na `0.40.0`
  passou a se chamar `prd` (`ls ~/.gemini/config/plugins/aicf/skills | grep -c criar-prd` → 1).
- **opencode:** não tem o aicf. `opencode debug skill > s.json` lista 46 skills, nenhuma do aicf
  (`jq -r '.[].name' s.json | grep -cxE 'ajuda|criar-spec|fechar-demanda|implementar-spec|prd|proxima-demanda|setup'` → 0).

Atualizar os dois pelo README de hoje é cópia de arquivos ou reinstalação a partir de um clone.
Antes da entrevista, a pesquisa conferiu se cada harness instala por um mecanismo próprio:

- **Antigravity (`agy` 1.4.2):** `agy plugin install` aceita uma pasta ou `plugin@marketplace`
  de um marketplace registrado. `aicodingflow`, `claude`, `claude-code`, `gemini`, `antigravity`,
  `github`, `git`, `official` e `agent-marketplace` devolvem todos `unknown marketplace: <nome>`
  (rodado com `HOME` isolado), e o `agy plugin --help` não tem comando para registrar marketplace.
  O marketplace dele é o catálogo do Google (Agent Marketplace), que instala por ID de listagem.
  Sobra o `agy plugin import claude`, que puxaria do Claude Code a cópia que ele já tem. Com `HOME`
  isolado e o `installed_plugins.json`, o `settings.json` e a cache do aicf copiados, ele respondeu
  `No claude extensions found`, e não ficou claro o que ele lê.
- **opencode (1.17.11):** a chave `skills` do `opencode.json` aceita uma lista de caminhos
  (`curl -s https://opencode.ai/config.json | jq '.properties.skills.anyOf[0].description'` →
  `"Additional paths or URLs to discover skills from"`). Com ela, o opencode lê as skills direto
  de um clone, e atualizar vira `git pull`. O Superpowers usa outro caminho, um plugin git com um
  arquivo JS que registra a pasta `skills/`
  (`jq .plugin` na saída de `opencode debug config` →
  `superpowers@git+https://github.com/obra/superpowers.git`). Esse caminho foi descartado (ver
  Fora de escopo).

## Solução

As duas cópias chegam à versão do `main`, e o README passa a ensinar o caminho que funcionou.

**opencode — clone e chave `skills`.** O README troca a cópia por:

```bash
git clone https://github.com/hmaurus/skills ~/aicf
```

e uma linha no `~/.config/opencode/opencode.json` (ou `.jsonc`): `"skills": ["~/aicf/skills"]`.
Para atualizar, só `git -C ~/aicf pull`. Antes de o README dizer isso, testar:

- se o opencode acha as sete skills e ignora `midia/`, como acontece com a pasta copiada;
- se o `~` se expande. Se não se expandir, o README usa o caminho absoluto e diz isso;
- se o aviso **"Copie, não crie link simbólico"** continua valendo. Ele só faz sentido para quem
  copia, então provavelmente sai junto com a cópia.

O aviso de que o opencode não esconde `setup`, `prd` e `ajuda` do agente fica.

**Antigravity — testar o import e, se ele falhar, ficar com o install.** Na implementação,
descobrir se `agy plugin import claude` leva a cópia do Antigravity à versão que o Claude Code tem.
Se levar, o README o recomenda como o jeito de atualizar, porque o titular já atualiza o Claude
Code pelo `claude plugin update`: o Antigravity passa a seguir o Claude Code, sem clone. Se não
levar, fica o `git -C ~/aicf pull && agy plugin install ~/aicf` de hoje.

**Resto da versão velha.** Pode acontecer de o install (ou o import) por cima deixar a pasta
`criar-prd/` ou recusar com `another plugin is already installed in the folder <pasta>; uninstall it first`
(mensagem que existe no binário do `agy`, porque a cópia atual veio de import e não de install).
Nesse caso, `agy plugin uninstall aicf` antes, e o README passa a mandar desinstalar antes de
atualizar. Se o comando limpar sozinho, o README não muda nesse ponto.

O que a pesquisa da entrevista e a implementação descobrirem sobre os dois harnesses vai para o
[`harnesses.md`](../../referencias/harnesses.md), com o comando ao lado de cada afirmação.

## Arquivos e interfaces

- `README.md` e `README.en.md` — seções **Antigravity (alvo)** e **opencode (compatível)**: o
  comando de instalar, o de atualizar e os avisos.
- `docs/referencias/harnesses.md` — o que se achou: marketplaces que o `agy` não reconhece, o que
  o `agy plugin import` faz, a chave `skills` do opencode.
- `docs/referencias/verificacao-do-setup.md`, passada no Antigravity — cita
  `git -C ~/aicf pull && agy plugin install ~/aicf` como jeito de atualizar. Muda junto, se o
  README mudar.
- Nesta máquina, fora do repositório: `~/aicf` (clone novo), `~/.config/opencode/opencode.jsonc`
  (ganha a chave `skills`, ao lado do plugin do Superpowers que já está lá) e
  `~/.gemini/config/plugins/aicf/`.

Nenhuma skill muda, então não há bump de versão. A entrada do `CHANGELOG.md` também não é
obrigatória: o README não vai para o contexto do agente.

## Fora de escopo

- **Plugin git para o opencode, como o do Superpowers.** Exigiria um `package.json` e um arquivo
  JS no repositório, código de runtime que ninguém mantém hoje. A atualização também é menos
  previsível: a doc do Superpowers avisa que às vezes é preciso limpar a cache de pacotes do
  opencode. A chave `skills` resolve o mesmo sem nada novo no repositório.
- **Publicar o aicf no Agent Marketplace do Antigravity.** É o catálogo do Google, por ID de
  listagem, e já tinha ficado fora em
  [o aicf quebra fora do Claude Code](../concluidas/o-ciclo-nunca-rodou-em-outro-agente.md).
- **A passada do setup no Antigravity** ([verificacao-do-setup.md](../../referencias/verificacao-do-setup.md)).
  Só o titular invoca o `setup`. Com a cópia atualizada ela fica possível, mas continua sendo dele.
- **Instalar no opencode por projeto** (`.opencode/skills/`). O README fica só com o global, que é
  o que esta máquina usa. A chave `skills` também vale no `opencode.json` de um projeto, e o README
  pode dizer isso numa frase, sem um segundo bloco de comandos.

## Verificação

1. **Antigravity:** `agy plugin list --json | jq -r '.[] | select(.name=="aicf") | .version'` →
   a versão do topo do `CHANGELOG.md` (hoje `0.41.1`), e
   `ls ~/.gemini/config/plugins/aicf/skills | grep -c criar-prd` → 0.
2. **opencode:** `opencode debug skill > s.json` (rodado fora de um repositório que tenha
   `.opencode/skills/` ou `.agents/skills/`) e
   `jq -r '.[].name' s.json | grep -cxE 'ajuda|criar-spec|fechar-demanda|implementar-spec|prd|proxima-demanda|setup'`
   → 7. As 46 de antes continuam (`jq -r '.[].name' s.json | wc -l` → 53).
3. **Atualização pelo opencode:** depois de `git -C ~/aicf pull`, o `SKILL.md` que o opencode lê é
   o do clone: `jq -r '.[] | select(.name=="prd") | .location' s.json` aponta para `~/aicf/skills/prd/`.
4. **README:** cada comando de instalar e atualizar das duas seções, nos dois idiomas, foi
   executado nesta máquina na forma em que está escrito. O relatório lista os que rodaram e a
   saída de cada um.
5. `./scripts/check.sh` termina em `Tudo verde.`

## Relatório de implementação (2026-10-20)

**Status:** concluído. As duas cópias desta máquina estão na `0.41.1`, e o README ensina o caminho
que funcionou. Sem bump de versão, porque nenhuma skill mudou.

**Arquivos alterados**

- `README.md` e `README.en.md`: a seção do opencode troca a cópia de `skills/` pelo clone mais
  `"skills": { "paths": ["~/aicf/skills"] }`, e atualizar vira `git -C ~/aicf pull`. Saem o aviso
  "copie, não crie link simbólico" e a frase sobre `midia/`. A seção do Antigravity não muda.
- `docs/referencias/harnesses.md`: quatro achados, cada um com o comando que o confere. São eles:
  o install por cima limpa skill removida, não há marketplace para o aicf, o `agy plugin import
  claude` não atualiza, e a chave `skills` do opencode tem uma forma que funciona e outra que é
  recusada.
- Fora do repositório: clone em `~/aicf`, a chave `skills` em `~/.config/opencode/opencode.jsonc`
  e a cópia do `agy` em `~/.gemini/config/plugins/aicf/`. O backup da config do `agy` feito antes
  do import ficou na pasta temporária da sessão.

**Commits**

- `3efc169` docs(projeto): spec de atualizar o aicf no Antigravity e no opencode
- `6a07887` docs: o opencode lê o aicf direto do clone, pela chave skills

**Validação**

1. `agy plugin list --json | jq -r '.[] | select(.name=="aicf") | .version'` → `0.41.1`;
   `ls ~/.gemini/config/plugins/aicf/skills | grep -c criar-prd` → 0; `diff -rq ~/aicf/skills
   ~/.gemini/config/plugins/aicf/skills` sem saída. `mattpocock-skills` e `superpowers`
   continuam `enabled`.
2. `opencode debug skill > s.json` fora de repositório: as sete do aicf (`grep -cxE ...` → 7) e
   53 no total (`jq -r '.[].name' s.json | wc -l`).
3. `jq -r '.[] | select(.name=="prd") | .location' s.json` → `/home/mh/aicf/skills/prd/SKILL.md`.
4. Rodados como estão escritos: `git clone https://github.com/hmaurus/skills ~/aicf`, a chave
   `skills` no `opencode.jsonc`, `agy plugin install ~/aicf` e `git -C ~/aicf pull && agy plugin
   install ~/aicf` (`Already up to date.` e `[ok] aicf`, `7 processed`). Com `HOME` isolado, a
   chave também funcionou no `opencode.json` de um projeto, com `~` e com caminho absoluto.
5. `./scripts/check.sh` → `Tudo verde.`

A revisão de código não rodou, porque a mudança é só texto de documentação.

**Escopo efetivo**

- **O README do Antigravity não mudou.** O `agy plugin import claude` respondeu
  `No claude extensions found` no HOME real, com o aicf 0.41.1 instalado no Claude Code, e também
  em quatro HOMEs isolados. O install por cima não precisou de `uninstall` antes: ele levou a cópia
  à `0.41.1` e apagou `criar-prd/`. Por isso o `verificacao-do-setup.md`, que cita o mesmo comando,
  também não mudou.
- **A forma da chave no opencode divergiu da spec.** A spec previa `"skills": ["~/aicf/skills"]`,
  que é a forma em lista do schema publicado. O opencode 1.17.11 recusa a config com
  `Expected object | undefined, got ["~/aicf/skills"] skills`, e a forma que entrou é
  `{ "paths": [...] }`. Ela também é a que o plugin do Superpowers preenche.

**Lições**

- O schema publicado em `opencode.ai/config.json` acompanha a versão mais nova do opencode, não a
  instalada. Antes de escrever no README o que ele diz, a forma se testa no binário local.

**Saída do ritual:** o conhecimento operacional foi para o
[`harnesses.md`](../../referencias/harnesses.md) no commit de código. Nada foi para o
`CLAUDE.md`, ADR ou glossário. A regra sobre ferramenta de terceiro, que o `CLAUDE.md` já tem,
cobre a lição do schema. Esta demanda não cria nem torna obsoleta outra demanda, e não contraria o
PRD.
