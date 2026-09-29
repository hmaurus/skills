# O setup supõe que o `git init` cria `main`

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (toca dois arquivos da skill `setup` e um doc de referência, sem decisão de abordagem)

Registrada em 2026-09-29, pela revisão de código de
[o setup não envia a main a um remoto que já existe](../concluidas/o-setup-nao-envia-a-main-a-um-remoto-que-ja-existe.md).

## Problema

"O primeiro commit" do `skills/setup/SKILL.md` (`:332`) afirma que "`main` é a branch que o
`git init` cria". Sem `init.defaultBranch` configurado, o git cria `master`:

```bash
d=$(mktemp -d); HOME=$d git init -q $d/r && git -C $d/r symbolic-ref HEAD   # refs/heads/master (git 2.43)
```

Numa máquina nova, onde o setup costuma rodar o próprio `git init`, a branch de produção se chama
`master` e todo passo que cita `main` erra: `git push -u origin main` sai com 1 e
`error: src refspec main does not match any`, e o `CLAUDE.md` gerado descreve uma `main` que não
existe. As passadas de verificação não pegaram porque a máquina do titular tem
`init.defaultBranch = main` no global (`git config --global init.defaultBranch`).

O mesmo vale para o repositório que o usuário já iniciou antes do setup: sem commit, está em
`master` pelo mesmo motivo; com histórico, a branch de produção pode ter qualquer nome e já estar
num remoto.

## Solução

A branch de produção passa a ser decidida em "O repositório local", antes de qualquer commit, em
três casos:

| Estado do repositório | O setup | Produção |
| --- | --- | --- |
| não existe, e o usuário aceita o `git init` | `git init -b main` | `main` |
| existe, sem commit (`git rev-parse --verify -q HEAD` sai com 1) | `git branch -m main` se a branch ativa não for `main` — não há histórico para perder | `main` |
| existe, com commit | nada — não renomeia o que não criou | `main` se ela existe localmente; senão, a branch ativa |

Os dois comandos foram conferidos no git 2.43 com `HOME` vazio: `git init -b main` deixa
`refs/heads/main`, e `git branch -m main` numa branch sem commit sai com 0 e o primeiro commit cai
em `main`.

No terceiro caso, quando a produção não se chama `main`, **a skill não é reescrita com variável**:
uma frase em "O repositório local" diz que, dali em diante, `main` em comando, tabela e resumo é a
branch de produção, e se troca pelo nome real. O resumo final diz o nome em uma linha.

A frase de `:332` passa a dizer que o commit cai na branch de produção decidida em "O repositório
local", em vez de atribuir o nome ao `git init`.

No template do `CLAUDE.md`, a linha da seção Git (`templates/claude-md.md:52`) continua com `main`
— é o caso comum, e o `diff` da verificação continua mostrando só as quatro diferenças de hoje. No
terceiro caso, a tabela de "O que criar" manda trocar `main` pelo nome real nessa linha, junto com
`<NOME>`. "O setup criou as duas" deixa de ser verdade quando a produção já existia: vira "O setup
deixou as duas, e você em `develop`".

## Arquivos e interfaces

- `skills/setup/SKILL.md` — "O repositório local" (`:42`–`:54`: `git init -b main`, a tabela dos
  três casos, a frase sobre o nome), "O primeiro commit" (`:332`), a instrução de cópia dos
  templates (`:257`), e "Ao terminar" (a linha do nome, quando não é `main`)
- `skills/setup/templates/claude-md.md:52` — "criou as duas" → "deixou as duas"
- `docs/referencias/verificacao-do-setup.md:21`–`:25` — o item 4 de "Antes de qualquer passada"
  deixa de dizer que o caso da máquina nova não se cobre, e passa a dizer como cobri-lo nesta
  máquina: rodar a passada com `init.defaultBranch` desligado, e a condição que encerra é
  `git branch --format='%(refname:short)'` devolver `develop` e `main`, sem `master`
- `CHANGELOG.md` e `.claude-plugin/plugin.json` — versão de correção

## Fora de escopo

- **Renomear branch com histórico para `main`.** Decidido na entrevista: se ela já está num remoto,
  a antiga fica órfã lá e continua default; o setup mexeria em algo que não criou.
- **Perguntar se renomeia.** Acrescentaria uma pergunta e ainda precisaria do caminho "seguir o
  nome" para quem recusa — dois mecanismos para o mesmo caso.
- **Placeholder `<PRODUCAO>` no template.** Obrigaria toda passada a substituir uma linha que no
  caso comum já está certa, e mudaria o `diff` esperado da verificação.
- **Repositório com histórico que já tem `develop`.** `git branch develop` sai com 128
  (`fatal: a branch named 'develop' already exists`). É outro defeito, do projeto que ganha
  governança depois; se aparecer em uso, vira intent própria.
- **git anterior à 2.28**, que não conhece `git init -b`. O Ubuntu 22.04 já traz 2.34.

## Verificação

1. **Os comandos que a spec prescreve**, numa máquina sem `init.defaultBranch` (simulada por `HOME`
   vazio):

   ```bash
   d=$(mktemp -d); export HOME=$d GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x
   git init -q -b main $d/a && git -C $d/a symbolic-ref HEAD                  # refs/heads/main
   git init -q $d/b && git -C $d/b rev-parse --verify -q HEAD; echo $?        # 1 — sem commit
   git -C $d/b branch -m main && git -C $d/b commit -q --allow-empty -m x \
     && git -C $d/b branch --format='%(refname:short)'                        # main
   ```

2. **O texto:** ``grep -c 'que o `git init` cria' skills/setup/SKILL.md`` passa de 1 (hoje, `:332`)
   a 0, e `grep -c 'git init -b main' skills/setup/SKILL.md` passa de 0 a ao menos 1.
3. `./scripts/check.sh` termina em `Tudo verde.`
4. **Comportamento do setup** — a skill tem `disable-model-invocation: true`, então o agente não a
   roda. Fica em aberto até uma passada do titular com `init.defaultBranch` desligado, pelo item 4
   de [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md).
