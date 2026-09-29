# O setup não envia a `main` a um remoto que já existe

Processo — entrevista: criar-spec · implementação: aicf-direto

Registrada em 2026-09-28, ao preparar um projeto novo cujo repositório no GitHub foi criado vazio
antes do setup (`git init` + `git remote add origin` na mão).

## Problema

No GitHub, a primeira branch enviada a um repositório vazio vira a default dele. O setup só envia a
`main` pelo `gh repo create --push` (`skills/setup/SKILL.md:344`), e esse passo só roda no modo
issue e quando o `git remote -v` está vazio (`:66`). Nos outros casos, o projeto termina com a
`develop` ativa e sem a `main` no remoto:

- **Modo arquivo, com `origin` configurado.** O setup não envia nada. Se o primeiro push do
  usuário for da branch ativa, a `develop` vira a default.
- **Modo issue, com `origin` configurado.** O passo "A branch de trabalho" envia só a `develop`
  (`:383`) — exatamente a inversão que aquela seção descreve como o que a ordem evita.
- **Modo arquivo, sem remoto.** O setup termina sem nada no GitHub. Quando o usuário cria o
  repositório depois, `gh repo create <nome> --source=. --remote=origin --push` envia a branch
  ativa, que é a `develop`. O defeito aparece dias depois do setup, quando o resumo dele já saiu da
  tela.

Caso real: o repositório anterior do mesmo projeto ficou com `develop` como default e `main` nunca
mergeada; `gh repo view <repo> --json defaultBranchRef` devolvia `develop`.

## Solução

A correção fica **só no setup**, não no template do `CLAUDE.md`: o `CLAUDE.md` carrega em toda
sessão, e uma instrução que vale uma vez, no primeiro push, viraria contexto permanente sem uso — e
chegaria tarde, porque quem a lê é o agente das sessões seguintes. O setup é o momento em que o
problema acontece.

### A `main` vai ao remoto antes da `develop` existir

Uma seção nova no roteiro, **depois do primeiro commit e antes de "A branch de trabalho"**, nos dois
modos. No modo issue ela vem depois de "O repositório no GitHub, e os labels"; se o `gh repo create
--push` acabou de rodar, a `main` já subiu e a seção não tem o que fazer.

**Com `origin` configurado**, ler o remoto pelo código de saída, não pela mensagem:

```bash
git ls-remote --exit-code --heads origin main
```

| Saída | Significado | O setup |
| --- | --- | --- |
| `2` | o remoto responde e não tem `main` (vazio, ou só com outras branches) | oferece `git push -u origin main`, com **confirmação explícita** — é a primeira ação do modo arquivo que sai do disco local |
| `0` | o remoto já tem `main` | não envia. Uma linha no resumo: a `main` remota tem histórico próprio, e reconciliar as duas é do usuário |
| outro (`128`) | o remoto não responde — URL errada, sem rede, sem credencial | mostra a saída do git e segue sem push. Uma linha no resumo: enviar a `main` antes da `develop` quando o remoto responder |

A tabela vale para qualquer provedor no modo arquivo: é `git push`, não `gh`. O modo issue já não
oferece remoto de outro provedor (`:67`).

Conferido em 2026-09-29 num repositório bare local — o bloco abaixo imprime `2`, `0` e `128`, nessa
ordem, e se roda em qualquer diretório descartável:

```bash
git init -q --bare r.git && git init -q -b main w && cd w && git commit -q --allow-empty -m x
git remote add origin ../r.git
git ls-remote --exit-code --heads origin main >/dev/null; echo $?
git push -q origin main; git ls-remote --exit-code --heads origin main >/dev/null; echo $?
git remote set-url origin ../nao-existe.git; git ls-remote --exit-code --heads origin main 2>/dev/null; echo $?
```

**Modo arquivo, sem `origin`.** Com `gh` instalado **e** `gh auth status` passando, oferecer criar o
repositório agora, ainda com a `main` ativa — opcional, com a mesma confirmação de nome e
visibilidade do modo issue (`--private` como sugestão) e o mesmo comando:
`gh repo create <nome> --private --source=. --remote=origin --push`. Sem `gh` ou sem login, o setup
não conduz login para uma etapa opcional: uma linha no resumo diz que, ao criar o remoto, a `main`
sobe primeiro — `git push -u origin main` antes de qualquer push da `develop`.

### A `develop` só sobe se a `main` acabou de subir

Em "A branch de trabalho", o comentário `# só no modo issue` do `git push -u origin develop` vira
**só quando a `main` foi enviada neste setup** — pelo `gh repo create --push` ou pela seção nova,
nos dois modos. Nos casos em que a `main` não sobe (remoto já tem `main`, remoto não responde,
usuário recusou), a `develop` também não sobe e o remoto fica como o usuário o deixou.

O parágrafo "A posição na ordem é o que importa" passa a valer para os dois caminhos de envio, não
só para o `gh repo create --push`.

### O resumo diz o estado do remoto

"Ao terminar", item 1, inclui o remoto: o que foi enviado, ou a linha do caso que ficou sem envio.

## Arquivos e interfaces

- `skills/setup/SKILL.md` — seção nova entre "O repositório no GitHub, e os labels" e "A branch de
  trabalho"; o comentário do push e o parágrafo da ordem em "A branch de trabalho"; o item 1 de "Ao
  terminar". "O repositório no GitHub" passa a ser citado também pelo modo arquivo, para o comando e
  a confirmação não existirem duas vezes.
- `docs/referencias/verificacao-do-setup.md` — as condições novas, em "O que está em aberto".
- `CHANGELOG.md` e `.claude-plugin/plugin.json` — `0.33.0`.

## Fora de escopo

- **Template do `CLAUDE.md`.** Motivo na Solução.
- **Remoto que já tem `main` com histórico próprio** (repositório criado no GitHub com README ou
  licença). A `main` já é a default, então o defeito não acontece; o `git push` seria recusado como
  non-fast-forward, e reconciliar histórico que o setup não criou não é dele. Só o aviso.
- **Conduzir `gh auth login` no modo arquivo.** Quem escolheu o modo sem fornecedor não ganha login
  no caminho de uma etapa opcional.
- **Corrigir a default de um repositório que já a tem errada** (`gh repo edit --default-branch`). O
  setup roda uma vez, em projeto novo.

## Verificação

`setup` tem `disable-model-invocation: true`: o agente não roda a passada. Ela é do titular, com o
roteiro de [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md) (plugin atualizado,
sessão nova, versão `0.33.0` no cabeçalho), em diretório novo. Cada ramo termina com:

```bash
git ls-remote --heads origin | awk '{print $2}'                 # refs/heads/develop e refs/heads/main
gh repo view --json defaultBranchRef -q .defaultBranchRef.name  # main
git branch --show-current                                       # develop
```

1. **Modo arquivo, `origin` vazio** — repositório criado vazio no GitHub e `git remote add origin`
   antes do setup. O setup pergunta antes do `git push -u origin main`.
2. **Modo issue, `origin` vazio** — o mesmo preparo, escolhendo issues. Sem `gh repo create`.
3. **Modo arquivo, sem remoto, `gh` logado** — aceitar a oferta de criar o repositório.

E um ramo negativo, sem os três comandos acima: **modo arquivo, sem remoto, sem `gh` no `PATH`** —
nenhuma oferta, e o resumo traz a linha de enviar a `main` primeiro.

Os repositórios de teste são privados e saem com `gh repo delete <nome> --yes` depois de a passada
ser avaliada. A demanda fecha com essa verificação em aberto, registrada em "O que está em aberto".

## Relatório de implementação (2026-09-29)

**Status** — concluído no roteiro; verificação de comportamento em aberto. O `setup` tem
`disable-model-invocation: true`, então a passada é do titular. As quatro condições estão em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), em "O que está em aberto", e
se encerram quando a passada da `0.33.0` for registrada em "O que já passou".

**Arquivos alterados**

- `skills/setup/SKILL.md` — seção nova "A `main` no remoto", entre os labels e a branch de trabalho;
  o push da `develop` passa a depender de a `main` ter subido; o resumo final traz o estado do remoto.
- `docs/referencias/verificacao-do-setup.md` — as condições da passada da `0.33.0`.
- `CHANGELOG.md` e `.claude-plugin/plugin.json` — `0.33.0`.

**Commits**

- `789072d` docs(projeto): entrevista do setup que não envia a main vira spec
- `73688f0` feat(setup): envia a main antes da develop quando o origin já existe
- `6daa1b8` fix(setup): a main no remoto cobre recusa, diretório sem commit e o caso 0

**Validação**

- `./scripts/check.sh` → `Tudo verde.` depois de cada commit de código.
- Os códigos de saída do `git ls-remote --exit-code --heads origin main` (`2`, `0`, `128`), pelo
  bloco da Solução, rodado num repositório bare local.
- Revisão de código por subagente que não viu a implementação, sobre o `73688f0`. Os achados
  viraram o `6daa1b8`, menos um, que virou demanda própria (abaixo).

**Escopo efetivo** — a revisão achou quatro casos que a spec não previa, e o `6daa1b8` os cobre:

- **Recusa sem linha no resumo.** A spec só previa a linha de "enviar a `main` primeiro" para quem
  não tem `gh`. Quem recusa uma das duas confirmações e cria o repositório depois reproduzia o
  defeito original. Agora a linha sai toda vez que a `main` não sobe.
- **Diretório sem `.git` ou sem commit.** O usuário recusou o `git init`, ou a identidade do git
  faltou. A seção agora pula esses casos, em vez de oferecer um `gh repo create --push` que recusaria.
- **A linha do código `0`**, que tinha conteúdo na spec e não no roteiro.
- **Os pontos que diziam "só no modo issue"** ("O que o ambiente permite" e a seção do repositório
  no GitHub) agora dizem que servem também à oferta do modo arquivo.

**Lições** — a revisão confirmou em
`pkg/cmd/repo/create/create.go:683` do `gh` v2.101.0 que o `gh repo create --push` envia `HEAD`,
isto é, a branch ativa. Esse é o mecanismo do terceiro caso. Achou também que o `git init` sem
`init.defaultBranch` cria `master`, o que quebra todo passo do setup que cita `main`: virou
[o setup supõe que o git init cria main](../specs/o-setup-supoe-que-o-git-init-cria-main.md).

**O que o fechamento gerou** — a demanda
[o setup supõe que o git init cria main](../specs/o-setup-supoe-que-o-git-init-cria-main.md), e o
passo 4 de "Antes de qualquer passada" em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), que avisa que a configuração
global do git desta máquina esconde o caso `master`.
