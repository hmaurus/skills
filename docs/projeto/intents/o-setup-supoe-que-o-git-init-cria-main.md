# O setup supõe que o `git init` cria `main`

Processo — entrevista: a definir · implementação: a definir

Registrada em 2026-09-29, pela revisão de código de
[o setup não envia a main a um remoto que já existe](../concluidas/o-setup-nao-envia-a-main-a-um-remoto-que-ja-existe.md).

## O defeito

"O primeiro commit" do `skills/setup/SKILL.md` afirma que "`main` é a branch que o `git init`
cria". Sem `init.defaultBranch` configurado, o git cria `master`:

```bash
d=$(mktemp -d); HOME=$d git init -q $d/r && git -C $d/r symbolic-ref HEAD   # refs/heads/master (git 2.43)
```

Numa máquina nova, onde o setup costuma rodar o próprio `git init`, a branch de produção se chama
`master` e todo passo que cita `main` erra: `git push -u origin main` sai com 1 e
`error: src refspec main does not match any`, e o `CLAUDE.md` gerado descreve uma `main` que não
existe. As passadas de verificação não pegaram porque a máquina do titular tem
`init.defaultBranch = main` no global (`git config --global init.defaultBranch`).

## A decidir na entrevista

- O setup roda `git init -b main` quando é ele quem inicializa? E com repositório que o usuário já
  iniciou em `master` — renomear (`git branch -m master main`) antes do primeiro commit, perguntar,
  ou seguir o nome que existe?
