# O setup não envia a `main` a um remoto que já existe

Processo — entrevista: a definir · implementação: a definir

Registrada em 2026-09-28, ao preparar um projeto novo cujo repositório no GitHub foi criado vazio
antes do setup (`git init` + `git remote add origin` na mão).

## O defeito

O setup só envia a `main` pelo `gh repo create --push` (`skills/setup/SKILL.md:344`), e esse passo
só roda quando o `git remote -v` está vazio (`:66`). Com um `origin` já configurado, os dois modos
terminam sem a `main` no remoto:

- **Modo arquivo** — o setup não envia nada. O usuário faz o primeiro push por conta própria, e se
  começar pela `develop`, que é a branch ativa ao fim do setup, é ela que vira a default do
  repositório no GitHub.
- **Modo issue** — o passo "A branch de trabalho" envia só a `develop` (`:383`). É exatamente a
  inversão que aquela seção existe para evitar: `develop` sobe primeiro e vira a default, com a
  `main` nem existindo no remoto.

**Terceiro caso, sem remoto nenhum, no modo arquivo.** O setup termina com a `develop` ativa e
nada no GitHub. Quando o usuário cria o repositório depois, por conta própria, o caminho natural —
`gh repo create <nome> --source=. --remote=origin --push` — envia a branch ativa, que é a
`develop`, e ela vira a default. O defeito é o mesmo, só que acontece dias depois do setup, quando
o resumo dele já saiu da tela.

Caso real: o repositório anterior do mesmo projeto ficou com `develop` como default e `main` nunca
mergeada, e `gh repo view <repo> --json defaultBranchRef` devolvia `develop`.

## O que se decidiu

**A correção fica só no setup, não no template do `CLAUDE.md`.** O `CLAUDE.md` carrega em toda
sessão, para sempre; uma instrução que vale uma única vez, no primeiro push, viraria contexto
permanente sem uso — e ainda chegaria tarde, porque quem a lê é o agente das sessões seguintes, não
o setup. O setup é o momento em que o problema acontece e o único que o resolve.

Direção: com `origin` configurado e sem `main` no remoto, o setup oferece enviar a `main` antes de
criar a `develop` — `git push -u origin main`, com confirmação explícita, porque é a primeira ação
que sai do disco local —, nos dois modos. No modo issue, isso substitui o `--push` do
`gh repo create` que não rodou.

## A decidir na entrevista

- **O terceiro caso: fazer ou orientar.** Fazer: no modo arquivo, com `gh` disponível e sem
  remoto, oferecer criar o repositório no GitHub ainda com a `main` ativa, antes da `develop` —
  opcional, com confirmação. Orientar: uma linha no resumo final dizendo para enviar a `main`
  primeiro. Orientar é mais simples, mas chega tarde pelo mesmo motivo que tirou a instrução do
  template do `CLAUDE.md`
- Como detectar "remoto vazio" sem depender de mensagem de erro (`git ls-remote --heads origin`
  vazio?)
- Remoto que já tem `main` com histórico próprio: fora de escopo, avisar e não enviar?
- Remoto em outro provedor no modo arquivo: o push é o mesmo `git push`, então o caso cabe aqui
