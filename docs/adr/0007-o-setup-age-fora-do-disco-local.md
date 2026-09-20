# 0007 — O setup age fora do disco local, com confirmação

Data: 2026-09-20 · Status: aceita · Versão: `0.23.0`

## Decisão

O `/aicf:setup` **executa** quatro comandos que mudam estado, e **conduz** um:

| Comando | Categoria | Quem roda |
| --- | --- | --- |
| `git init` | cria repositório local | o agente, com o sim do usuário |
| `git commit` | escreve no histórico | o agente |
| `gh repo create` | **cria recurso fora da máquina** | o agente, com confirmação explícita de nome e visibilidade |
| `gh label create` | escreve num recurso remoto existente | o agente |
| `gh auth login` | autenticação interativa | **o usuário** — o agente mostra o comando e espera |

`grep -n 'git init\|gh repo create\|gh label create\|gh auth login' skills/setup/SKILL.md` lista
onde cada um está escrito.

O critério que separa as duas colunas: **o agente executa o que é determinístico e confirmável, e
conduz o que é interativo.** `gh auth login` abre navegador ou pede código de dispositivo — não é
uma decisão de etiqueta, é que o agente não tem como completar esse fluxo sozinho.

## Por quê

Até a `0.22.0` o setup só escrevia arquivos no diretório corrente e criava labels num repositório
que já existia. Duas coisas o empurraram para fora disso.

**A primeira é que a governança não funciona sem repositório.** A demanda muda de estado por
`git mv`, o relatório vive no histórico, e `.gitkeep` num diretório sem git não segura pasta
nenhuma. O setup montava a estrutura inteira sem `.git` e sem dizer nada — aconteceu nos dois
diretórios de teste de 2026-09-20 —, e o usuário só descobria no primeiro fechamento de demanda.
Entregar a estrutura sem repositório é entregar um método que não funciona.

**A segunda é que a regra antiga descartava o que sabia resolver.** Ela conferia `gh auth status` e
`git remote -v` e, faltando qualquer coisa, oferecia só o modo arquivo. Nas duas passadas o `gh`
estava autenticado e só faltava o repositório no GitHub — uma condição de um comando. A regra
estava certa sobre o que evitava (deixar o usuário escolher um caminho que falha no primeiro
comando) e errada sobre o que fazia com a sobra.

**Por que executar, e não só conduzir.** A alternativa era o setup montar o `gh repo create` com os
valores certos e esperar o usuário rodar — foi a primeira opção considerada, e ela preserva a
propriedade de que nada sai da máquina por ação do agente. Descartada porque o custo recai onde o
método é mais frágil: o primeiro contato. Quem roda `/aicf:setup` está montando o projeto agora, já
autorizou a criação de uma dúzia de arquivos, e mandá-lo para outro terminal no meio do roteiro é
onde o onboarding se perde. A confirmação de nome e visibilidade cobre o risco real — criar o
repositório errado, ou público sem querer.

**O preço que isso tem.** O setup deixa de ser reversível com `rm -rf`: um repositório criado no
GitHub só some com `gh repo delete`, e um commit feito no projeto de outra pessoa entra num
histórico que não é do aicf. É por isso que o commit vai **por caminhos nomeados e nunca
`git add -A`** — num diretório que já tem código não commitado, o `-A` varreria um `.env` que ainda
não tem `.gitignore` para segurá-lo, e o setup não decide o que vai para o histórico de arquivo que
ele não criou.

## Consequências

- **A ordem dos passos passa a ser parte da decisão, não detalhe de implementação.** O `--push` do
  `gh repo create` empurra commits locais, e o `gh` confere isso **antes** de chamar a API: sem
  commit nenhum ele sai com 1 e ``--push` enabled but no commits found``, sem criar repositório
  nenhum — `git init && GH_TOKEN=invalido gh repo create <nome> --private --source=. --push`
  reproduz, e o token inválido nunca chega a ser usado. Não há estado meio criado a limpar; o que
  há é o onboarding parando com um erro. Por isso a criação do remoto é a penúltima coisa que o
  setup faz, depois do commit.
- **A pergunta da mídia passa a ser feita sempre que o ambiente permita resolvê-la**, e a opção
  issue só some nos dois estados que o setup não resolve — `gh` ausente, e `remote` apontando para
  outro provedor.
- **O precedente vale para as outras skills.** Nenhuma outra do aicf cria recurso remoto hoje
  (`grep -rln 'gh repo create\|gh api.*-X POST' skills/` devolve só `skills/setup/SKILL.md`), e uma
  que venha a criar segue o mesmo critério: confirmação explícita com os parâmetros à vista, e
  condução quando o fluxo for interativo.
- **Reverter** significaria voltar a skill à regra de `0.22.0` e aceitar de novo os dois sintomas
  que este ADR resolve. Os projetos que já rodaram o setup ficam com repositório e commit — nada
  neles precisa ser desfeito.
