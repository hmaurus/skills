# O repositório no GitHub, e a `main` no remoto

## O repositório no GitHub, e os labels

Só no modo issue, e **depois do commit**. O comando de criar o repositório serve também à oferta do
modo arquivo, em "A `main` no remoto".

### Criar o repositório, se faltar

`gh repo create` cria algo fora do disco local, então vai com
**confirmação explícita — nome e visibilidade**, e `--private` como sugestão.

```bash
gh repo create <nome> --private --source=. --remote=origin --push
```

**A ordem é o que esta skill fixa.** O `--push` empurra commits locais, e o `gh` confere isso
**antes** de chamar a API: sem commit nenhum ele sai com 1 e
``--push` enabled but no commits found``, sem criar repositório nenhum. Fora de um repositório
git, recusa com `current directory is not a git repository`. Nada quebra pela metade, mas o
onboarding para com um erro — e criar o remoto antes de os arquivos existirem é exatamente como se
chega lá.

**Fora dessa ordem, pesquisar em vez de improvisar.** O comando acima cobre o caso comum;
organização em vez de conta pessoal, SSH em vez de HTTPS, GitHub Enterprise, escopo de token
faltando, nome já em uso — cada um tem resposta na documentação do `gh`, e consultá-la na hora é o
certo. O que não se faz é copiá-la para cá: ela envelheceria sozinha dentro desta skill, enquanto
`gh repo create --help` está sempre atual.

**Em repositório com histórico, sem `--push`:** `gh repo create <nome> --private --source=. --remote=origin`
cria o repositório e o `origin` sem enviar nada. O `--push` enviaria a branch ativa, e a primeira
branch enviada vira a default no GitHub — uma `feature` ativa viraria a default do repositório. As
issues e os labels não dependem de código no remoto; o resumo diz para enviar primeiro a produção.

### Os três labels

Criar com `gh label create`. **Label que já existe faz o comando sair com 1** —
`label with name "X" already exists; use --force to update its color and description` —, e é o
`|| true` que deixa a sequência seguir. A idempotência é da sequência, não do comando: quem
conferir o exit code, ou rodar sob `set -e`, precisa saber disso. Os comandos, com as descrições,
estão em
[`midia/issues.md`](../midia/issues.md), na
seção "Criar os labels".

**O setup é quem cria os labels**, e não a primeira demanda: `gh issue create --label` com label
inexistente **falha em vez de criar**. É a armadilha mais repetida sobre setups que só gravam o
mapeamento e deixam os labels para depois.

## A `main` no remoto

**Não roda em repositório com histórico** — ver "O repositório local"; a oferta de criar o
repositório no modo arquivo também não.

**Nos dois modos, antes de a `develop` existir — e só com o primeiro commit feito.** Sem `.git`
(o usuário recusou o `git init`) ou sem commit (a identidade do git faltou e o commit ficou para
depois), não há `main` para enviar: pular a seção, e o resumo diz para enviar a `main` antes da
`develop` quando o remoto existir. No GitHub, a primeira branch enviada a um
repositório vazio vira a default dele; se for a `develop`, produção deixa de ser a default, e
desfazer isso é mexer em configuração do repositório. Se o `gh repo create --push` acabou de rodar,
a `main` já subiu e esta seção não tem o que fazer.

**Com `origin` configurado**, ler o remoto pelo código de saída, não pela mensagem:

```bash
git ls-remote --exit-code --heads origin main
```

| Saída | Significado | O setup |
| --- | --- | --- |
| `2` | o remoto responde e não tem `main` — vazio, ou só com outras branches | `git push -u origin main`, com **confirmação explícita**: no modo arquivo é a primeira ação que sai do disco local |
| `0` | o remoto já tem `main` | não envia — o push seria recusado, e reconciliar histórico que o setup não criou não é dele. Uma linha no resumo: a `main` remota tem histórico próprio, e juntar as duas fica com o usuário |
| outro (`128`) | o remoto não responde — URL errada, sem rede, sem credencial | mostrar a saída do git e seguir sem push. Uma linha no resumo: enviar a `main` antes da `develop` quando o remoto responder |

No modo arquivo a tabela vale para qualquer provedor: é `git push`, não `gh`.

**Modo arquivo, sem `origin`.** Com `gh` instalado **e** `gh auth status` passando, oferecer criar o
repositório agora, ainda com a `main` ativa — opcional, com o mesmo comando e a mesma confirmação
de "Criar o repositório, se faltar". Sem `gh` ou sem login, não conduzir login para uma etapa
opcional.

**Toda vez que a `main` não sobe** — recusa de qualquer das duas confirmações, sem `gh`, sem login —,
uma linha no resumo diz que, ao criar ou alcançar o remoto, a `main` sobe primeiro:
`git push -u origin main` antes de qualquer push da `develop`. Quem cria o repositório depois com
`gh repo create --push` envia a branch ativa, que ao fim do setup é a `develop`.
