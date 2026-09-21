# O setup entrega projeto sem repositório, e esconde o modo issue em vez de habilitá-lo

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

O `/aicf:setup` monta a governança inteira num diretório que não é repositório git, sem dizer uma
palavra sobre isso. **A skill não menciona `git init` em lugar nenhum** — `grep -rn 'git init'
skills/` não devolve um hit, e `git ` aparece três vezes no `setup/SKILL.md`, todas conferindo
estado alheio, nunca criando.

O método inteiro assume versionamento. A demanda muda de estado por `git mv`; o relatório vive no
histórico; "sobrevive ao `git clone` sem rede" é o argumento com que o próprio setup vende o modo
arquivo. Entregar a estrutura sem repositório entrega um método que não funciona, e o usuário só
descobre no primeiro fechamento de demanda.

**Aconteceu duas vezes em 2026-09-20**, nos dois diretórios criados para verificar o layout
achatado — `~/dev/tmp/teste-aicf` e `~/dev/tmp/teste-aicf2`. Nos dois o setup rodou até o fim, criou
`docs/projeto/` com as quatro pastas e os `.gitkeep`, e em nenhum avisou que `.gitkeep` num
diretório sem git não segura pasta nenhuma.

O segundo sintoma tem a mesma raiz. A skill manda oferecer issues só se `gh auth status` passar e
`git remote -v` apontar para GitHub, e, não aguentando, dizer em uma linha o que falta. A regra está
certa sobre o que evita, e errada sobre o que faz com a sobra: nas duas passadas o `gh` estava
autenticado e só faltava o repositório — uma condição que o setup **sabe criar** e escolhe apenas
relatar. O usuário nunca chegou a ver a pergunta da mídia.

## Solução

O setup passa a **remover o que falta** em vez de esconder a opção, e a entregar o projeto
versionado. A ordem dos passos é o que resolve, e ela é fixa.

### A ordem

1. **Apresentação**, sem número de perguntas (ver abaixo).
2. **Nome e descrição do projeto**, como hoje.
3. **Repositório local.** Se não existe `.git`, explicar **em uma linha** por que o método depende
   de versionamento — a demanda muda de estado por `git mv`, o relatório vive no histórico, e
   `.gitkeep` sem repositório não segura pasta nenhuma — e perguntar. Sim → `git init`. É local,
   barato e desfeito com `rm -rf .git`.
4. **Ler o ambiente**, em silêncio: `command -v gh`, `gh auth status`, `git remote -v`. Nada é
   executado aqui; a leitura só decide o que a pergunta seguinte oferece.
5. **A pergunta da mídia**, com a nota do estado na opção issue (tabela abaixo).
6. **Login**, se a mídia escolhida foi issue e falta. Ver "executar e conduzir".
7. **Resto do questionário** — padrões de engenharia, ferramentas —, como hoje.
8. **Criar os arquivos**, como hoje.
9. **Primeiro commit**, nos dois modos.
10. **Criar o repositório remoto**, só no modo issue e só se faltar.
11. **Criar os três labels**, só no modo issue.
12. **Fechamento**, como hoje.

**A criação do remoto vem depois do commit, e é por isso que ela está no passo 10.** O `--push` do
`gh repo create` empurra commits locais, e o `gh` confere isso antes de chamar a API:

```
git init && GH_TOKEN=invalido gh repo create <nome> --private --source=. --remote=origin --push
→ `--push` enabled but no commits found in <dir>    (exit 1)
```

O token inválido nunca chega a ser usado — a checagem é local, e **nada é criado no GitHub**. Fora
de um repositório git, a recusa é `current directory is not a git repository`. Não há estado meio
criado a limpar; o que há é o onboarding parando com um erro. Inverter os dois passos é o conserto,
e a ordem é a parte que a skill fixa.

### Os quatro estados de ambiente

Hoje `gh auth status` decide tudo e os casos são indistinguíveis entre si. Cada um passa a ter
saída própria:

| Estado | Detectado por | O setup faz |
| --- | --- | --- |
| Tudo pronto | `gh` presente, autenticado, `git remote -v` aponta para GitHub | oferece as duas mídias, como hoje |
| Autenticado, sem repositório no GitHub | `git remote -v` vazio | oferece as duas; escolhida a issue, **cria o repositório** no passo 10 |
| `gh` presente, deslogado | `gh auth status` falha | oferece as duas; escolhida a issue, **conduz o login** no passo 6 |
| `gh` ausente | `command -v gh` falha | oferece só arquivo, e uma linha: o modo issue precisa do GitHub CLI (<https://cli.github.com>); instalado, `/aicf:setup` numa sessão nova passa a oferecê-lo |
| `remote` que não é GitHub | `git remote -v` aponta para outro provedor | oferece só arquivo, e uma linha: o modo issue é GitHub por decisão registrada na [ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md) |

Os dois últimos são os únicos em que a opção some — e somem porque o setup não os resolve, que é a
regra original aplicada ao que de fato sobrou dela.

### O que o setup executa, e o que ele conduz

**Executa:** `git init`, o commit, `gh repo create`, `gh label create`. Os três primeiros mexem no
disco local; `gh repo create` é a primeira ação do setup que cria algo fora da máquina, e por isso
vai com **confirmação explícita, nome e visibilidade** — `--private` é o sugerido.

```
gh repo create <nome> --private --source=. --remote=origin --push
```

**Conduz:** `gh auth login`. É interativo — abre navegador ou pede código de dispositivo —, então o
agente mostra o comando, pede que o usuário rode (pelo `!` na própria sessão) e reconfere com
`gh auth status` antes de seguir. Conduzir aqui não é escrúpulo: é que o agente não tem como
completar esse fluxo.

### O primeiro commit

Depois de criar os arquivos, nos dois modos. **Só os caminhos que o setup escreveu, nomeados** —
`CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/projeto/` e o que a mídia pedir —, nunca `git add -A`:
num diretório que já tem código não commitado, `-A` varreria tudo, inclusive um `.env` que ainda não
tem `.gitignore` para segurá-lo. O setup não decide o que vai para o histórico de arquivos que ele
não criou.

A mensagem fica em pt-BR, no padrão do repositório que está nascendo:
`chore: estrutura de governança do projeto`.

### A promessa das perguntas

A apresentação promete hoje "entre cinco e sete perguntas". O ramo issue passa disso, então o
número sai e a promessa vira qualitativa: poucas perguntas, nenhuma resposta definitiva, nada criado
antes de o usuário confirmar. Número que o próprio roteiro desmente é pior que nenhum número.

### Pesquisa dentro do setup

A skill fixa **a ordem acima e o comando canônico**, e nada mais sobre o `gh` — `gh repo create` é
estável e traz a própria documentação (`gh repo create --help` descreve o modo interativo e os flags
de visibilidade, conferido no gh 2.100.0). Para qualquer caso que a ordem não cubra — organização em
vez de conta pessoal, SSH em vez de HTTPS, GitHub Enterprise, escopo de token faltando, nome já em
uso — a skill **autoriza o agente a pesquisar** e resolver. Distrinchar o `gh` aqui seria copiar a
doc dele para dentro de uma skill que envelheceria sozinha; deixar a ordem por conta do agente da
vez é como a armadilha do push chega ao usuário.

## Arquivos e interfaces

- **`skills/setup/SKILL.md`** — o alvo. Muda a apresentação (sai o número de perguntas), nasce a
  seção do repositório local, a regra "só oferecer issues se o repositório aguentar" é reescrita na
  tabela dos quatro estados, e nascem os passos de commit, de criação do remoto e a autorização de
  pesquisa.
- **`.claude-plugin/plugin.json`** e **`CHANGELOG.md`** — versão e entrada sobem juntas, no commit
  de código, pela regra de publicação do `CLAUDE.md`.
- `skills/setup/templates/**` não muda: o que muda é o roteiro, não o que ele copia.
- `skills/workflow-demanda/references/midia-issues.md` não muda: a seção "Criar os labels" já diz
  que criar label é passo do setup, e continua sendo.

## Fora de escopo

- **Migrar projeto existente entre mídias.** Quem já rodou o setup e quer trocar de arquivo para
  issue é outra demanda; esta é sobre o primeiro contato.
- **Provedores além do GitHub.** O modo issue é GitHub por decisão registrada na
  [ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md), e nada aqui muda isso.
- **Criar remoto no modo arquivo.** Quem escolheu arquivo fica com o repositório local; backup no
  GitHub é decisão dele, não do onboarding.
- **Criar `.gitignore`.** O setup não sabe o que o projeto vai usar, e o commit por caminhos
  nomeados já protege o caso que motivaria a criação.

## Verificação

A skill tem `disable-model-invocation: true`: nenhum agente a invoca nem imita o roteiro por fora,
então **os passos 1 e 2 são do titular**, e a demanda fecha com eles nomeados como pendentes se não
acontecerem. Reiniciar a sessão depois do `/plugin update` antes de verificar, e conferir a versão
no cabeçalho do comando (`cache/aicodingflow/aicf/<versão>/skills/setup`) antes de acreditar no
resultado — a skill que roda é a do início da sessão.

1. **Ramo arquivo**, em diretório novo sem `.git`: `/aicf:setup`, escolhendo arquivo. Encerra
   quando o setup tiver oferecido o `git init` antes da pergunta da mídia, e ao fim:

   ```bash
   git log --oneline | wc -l                    # 1
   git show --stat --name-only HEAD             # só CLAUDE.md, AGENTS.md, README.md, docs/projeto/
   ```

2. **Ramo issue**, em outro diretório novo: `/aicf:setup`, escolhendo issues e deixando o setup
   criar um repositório privado. É a passada que o ramo issue **nunca teve** — condição herdada de
   [a profundidade da pasta quebra os links](../concluidas/a-profundidade-da-pasta-quebra-os-links.md).
   Encerra com:

   ```bash
   gh label list | grep -c '^aicf:'             # 3
   git log origin/main --oneline | wc -l        # 1 — o --push funcionou
   gh issue create --title t --label nao-existe # falha: é o que obriga o setup a criar os labels
   gh repo delete <nome> --yes                  # descartável: some depois de provar
   ```

   A terceira linha é a única forma segura de conferir a afirmação de que `gh issue create` com
   label inexistente falha em vez de criar — num repositório descartável, uma issue criada por
   engano não custa nada.

3. **O grep que refutava o problema passa a devolver hit:**

   ```bash
   grep -c 'git init' skills/setup/SKILL.md     # hoje 0; depois ≥ 1
   ```

4. `./scripts/check.sh` termina em `Tudo verde.` e sai com 0.


## Relatório de implementação (2026-09-20)

**Status** — concluído, com **a verificação de comportamento em aberto e nomeada**. A skill tem
`disable-model-invocation: true`: nenhum agente a invoca nem imita o roteiro por fora, então as
Verificações 1 e 2 (as duas passadas do `/aicf:setup` em diretório novo) são do titular. Quem as
encerra é ele, numa sessão reiniciada depois do `/plugin update` — a skill que roda é a do início da
sessão, e conferir a versão no cabeçalho do comando (`cache/aicodingflow/aicf/0.23.0/skills/setup`)
vem antes de acreditar no resultado. As Verificações 3 e 4 rodaram e passaram. O estado das Verificações 1 e 2 vive em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md).

**Causa raiz** — não é bug de código, é lacuna de roteiro, e as duas metades têm a mesma origem: a
skill sabia **conferir** estado de git e de `gh`, e não sabia **criar** nenhum dos dois. As três
menções a `git ` no arquivo eram todas de leitura. Disso saíam os dois sintomas: a estrutura nascia
sem repositório, e o modo issue era escondido justamente no caso — falta o repositório no GitHub —
em que um comando o habilitaria.

**Arquivos alterados**

| Arquivo | O quê |
| --- | --- |
| `skills/setup/SKILL.md` | o alvo: nasce "O repositório local" (com a rota do "não"), "O que o ambiente permite" (sequência que acumula, no lugar da regra de esconder), "O primeiro commit" e "O repositório no GitHub, e os labels"; a apresentação perde o número de perguntas; os labels mudam de seção |
| `skills/workflow-demanda/references/midia-issues.md` | `gh label create` com label existente sai com 1, não vira aviso — a frase estava errada desde que a receita nasceu |
| `README.md`, `README.en.md` | a descrição do comando listava o que ele monta sem `git init`, sem commit e sem criação de repositório |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.23.0`, em par |
| `CLAUDE.md` | a regra sobre ferramenta de terceiro ganha a emenda do passo 3 |
| `docs/adr/0007-o-setup-age-fora-do-disco-local.md` | novo, saída do passo 3 |

**Commits**

| Sha | O quê |
| --- | --- |
| `13a3c4b` | a entrevista promove o intent a spec |
| `4c1c143` | o código: skill, versão e CHANGELOG |
| `ba84832` | as correções da revisão, incluindo o erro factual que o próprio `4c1c143` carregava |

**Validação**

- `./scripts/check.sh` — `Tudo verde.`, com `104 links conferidos, 0 quebrados` e os dois
  `✔ Validation passed`.
- `grep -c 'git init' skills/setup/SKILL.md` — `0` antes de `4c1c143`, `2` depois. É a Verificação 3.
- Revisão de código por subagente fresco, que não viu a implementação, com os comandos do `gh`
  rodados por ele e reconferidos aqui: 14 achados, todos aceitos e aplicados em `ba84832`.
- `git init && GH_TOKEN=invalido gh repo create <nome> --private --source=. --push` →
  ``--push` enabled but no commits found``, exit 1, nada criado.
- `gh label create <label-existente>` → `already exists; use --force`, exit 1.
- `git remote -v` em diretório sem `.git` → `fatal: not a git repository`, exit 128.

**Escopo efetivo** — passou da spec em dois pontos, os dois por consequência direta. Os **dois
READMEs** descreviam o comando e ficariam mentindo sobre ele. E o **`midia-issues.md`** carregava a
mesma frase errada sobre `gh label create` que a revisão achou no setup — corrigir num lugar só
deixaria a contradição dentro do repositório.

**Lições**

- **O comando que se roda é o que a frase cita, não um parente dele.** A afirmação de que
  `gh repo create --push` falha com `error: src refspec HEAD does not match any` foi para quatro
  arquivos — skill, CHANGELOG, spec e ADR — com um teste ao lado que de fato rodava, e provava, o
  `git push` cru. O `gh` valida a ausência de commit **antes** de chamar a API e devolve outra
  mensagem, o que só aparece rodando o `gh`. A regra de ordem estava certa; a consequência descrita
  estava errada (não sobra repositório órfão, sobra um onboarding parado). Promovido para o
  `CLAUDE.md`, emendando a regra sobre ferramenta de terceiro.
- **Skill é texto que o check não lê.** `./scripts/check.sh` ficou verde o tempo todo: ele confere
  link, formato de plugin e par versão/CHANGELOG, e não tem como ver que os estados de um roteiro
  não são exclusivos, que o "não" de uma pergunta não tem rota, ou que um parágrafo de ação está
  antes do parágrafo que alimenta a pergunta. Dos 14 achados, 13 eram invisíveis para o check. Num
  repositório cujo produto **é** a instrução, a revisão fresca não é opcional — é o único teste que
  existe.
- **A ordem dos passos foi a parte difícil, e ela não estava no intent.** O intent tratava
  `gh repo create` como decisão de política (executar ou conduzir), e a decisão de política levou
  dez minutos. O que custou foi descobrir que o comando só funciona depois do primeiro commit — e
  isso só apareceu porque a entrevista rodou o comando em vez de descrevê-lo.

**Saída do passo 3** — [ADR 0007 — O setup age fora do disco local, com confirmação](../../adr/0007-o-setup-age-fora-do-disco-local.md),
mais a emenda no `CLAUDE.md`. Nenhuma demanda nova nasceu, e nenhuma ficou obsoleta: a
[governança em issues neste repositório](../intents/governanca-em-issues-neste-repo.md) continua
aberta e independente — o que esta demanda lhe dá é a primeira passada real do modo issue, quando a
Verificação 2 rodar.
