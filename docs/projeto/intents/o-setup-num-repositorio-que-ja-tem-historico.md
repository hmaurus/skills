# O setup num repositório que já tem histórico

Processo — entrevista: a definir · implementação: a definir

Registrada em 2026-09-29, pela revisão de código de
[o setup supõe que o git init cria main](../concluidas/o-setup-supoe-que-o-git-init-cria-main.md),
que passou a nomear o caso "já existia, com commit em qualquer branch" em "O repositório local" do
`skills/setup/SKILL.md` sem resolver o que vem depois dele.

## Os defeitos

Os três aparecem quando o setup roda num projeto que já tem código versionado:

1. **O commit cai na branch ativa, não na produção.** A tabela diz que a produção é a `main`, se
   ela existe, mas nenhum passo manda trocar para ela antes do commit. Com uma `feature` ativa, a
   governança vai para `feature`, e a `develop` nasce de lá. Na variante sem `main` (`master` +
   `feature` ativa), a regra "senão, a branch ativa" elege a `feature` como produção.
2. **O código de saída `0` de "A `main` no remoto" não significa histórico próprio.** Num
   repositório com histórico, o remoto costuma ser o upstream da própria `main`, e o push do commit
   de governança é fast-forward e passa. O setup não envia, a `develop` fica local, e a linha do
   resumo ("a `main` remota tem histórico próprio") é falsa.
3. **`git branch develop` sai com 128** (`fatal: a branch named 'develop' already exists`) quando
   o projeto já tem `develop`.

Reprodução dos três, com git 2.43:

```bash
d=$(mktemp -d); export HOME=$d GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x
git init -q --bare $d/remoto.git; git init -q -b main $d/r; cd $d/r
git commit -q --allow-empty -m a; git remote add origin $d/remoto.git; git push -q -u origin main
git switch -q -c feature; git commit -q --allow-empty -m gov; git branch --show-current   # 1: feature
git switch -q main; git commit -q --allow-empty -m gov2
git ls-remote --exit-code --heads origin main >/dev/null; echo $?; git push -q origin main; echo $?   # 2: 0 e 0
git branch develop; git branch develop; echo $?                                          # 3: 128
```

## A decidir na entrevista

- O setup atende projeto com histórico, ou declara que é para projeto novo e, com commit, para e diz
  isso? A descrição dele já diz "Rodar uma vez, no começo do projeto".
- Se atende: perguntar qual branch é a produção e `git switch` para ela antes do commit (e o que
  fazer com mudança não commitada na árvore)? No código `0`, conferir fast-forward
  (`git merge-base --is-ancestor origin/main main`, depois de `git fetch`) antes de desistir do
  push? `develop` existente: usar a que está lá, ou perguntar?
