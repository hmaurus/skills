# O setup entrega projeto sem repositório, e esconde o modo issue em vez de habilitá-lo

Processo — entrevista: a definir · implementação: a definir

## Problema

O `/aicf:setup` monta a governança inteira num diretório que não é repositório git, sem dizer uma
palavra sobre isso. **A skill não menciona `git init` em lugar nenhum** — `grep -rn 'git init'
skills/` não devolve um hit, e `git ` aparece três vezes no `setup/SKILL.md`, todas conferindo
estado alheio, nunca criando.

O método inteiro assume versionamento. A demanda muda de estado por `git mv`; o relatório vive no
histórico; "sobrevive ao `git clone` sem rede" é o argumento com que o próprio setup vende o modo
arquivo (linha 42 do `SKILL.md`). Entregar a estrutura sem repositório entrega um método que não
funciona, e o usuário só descobre no primeiro fechamento de demanda.

**Aconteceu duas vezes em 2026-09-20**, nos dois diretórios criados para verificar o layout
achatado — `~/dev/tmp/teste-aicf` e `~/dev/tmp/teste-aicf2`. Nos dois o setup rodou até o fim, criou
`docs/projeto/` com as quatro pastas e os `.gitkeep`, e em nenhum avisou que `.gitkeep` num
diretório sem git não segura pasta nenhuma.

O segundo sintoma tem a mesma raiz. A skill manda:

> **Só oferecer issues se o repositório aguentar.** Conferir antes: `gh auth status` passa, e
> `git remote -v` aponta para GitHub. Não aguentando, oferecer só arquivo e dizer **em uma linha** o
> que falta para a outra opção existir — deixar o usuário escolher um caminho que falha no primeiro
> comando é pior que não oferecer.

A regra está certa sobre o que evita, e errada sobre o que faz com a sobra. Nas duas passadas o
`gh` estava autenticado e só faltava o repositório — uma condição que o setup **sabe criar** e
escolhe apenas relatar. O usuário nunca chegou a ver a pergunta da mídia; no primeiro teste ele
perguntou depois por que ela não tinha vindo.

## Direção proposta

Dois níveis, separados pelo custo e pela reversibilidade:

- **`git init` é local, barato e desfeito com `rm -rf .git`** — entra **sempre**, como sugestão
  antes da pergunta da mídia, independente da mídia escolhida.
- **`gh repo create` sai da máquina** — só entra se o usuário escolher issues, com confirmação
  explícita, nome e visibilidade. É a primeira ação do setup que cria algo fora do disco local.

Com o repositório local resolvido antes, a pergunta da mídia passa a ser feita **sempre**, e a
regra acima muda de forma: em vez de esconder a opção, o setup remove o que falta para ela existir.

## O que a entrevista precisa decidir

- **A promessa das "cinco a sete perguntas"** da apresentação (linha 23 do `SKILL.md`). O caminho
  issue com criação de repositório passa de dez. Ou a promessa vira uma faixa por caminho, ou a
  criação do remoto sai do setup e vira instrução para o usuário rodar.
- **Até onde o setup cria coisa fora da máquina.** Hoje ele escreve arquivos locais e cria labels
  num repositório que já existe. Criar o repositório é categoria nova, e pode ser que o certo seja
  o setup **conduzir** (mostrar o comando, esperar o usuário rodar) em vez de **executar**.
- **Se cabe pesquisa dentro do setup.** A ideia original previa o agente pesquisar o que for
  preciso para configurar o modo issue. Contra: `gh repo create` é estável e já traz a própria
  documentação (`gh repo create --help` descreve o modo interativo e os flags de visibilidade), e
  busca no meio de um comando de onboarding é onde ele fica lento e imprevisível. A favor: o
  usuário pode ter um caso que o roteiro não cobre — organização em vez de conta pessoal, SSH em
  vez de HTTPS, GitHub Enterprise.
- **O que fazer com `gh` ausente**, que é diferente de `gh` deslogado. A skill hoje só chama
  `gh auth status` e trata os dois casos como um.
- **Projeto que já tem git mas não tem remote** — o caso mais comum de todos, e hoje indistinguível
  de "não tem nada".

## Fora de escopo, por ora

- **Migrar projeto existente entre mídias.** Quem já rodou o setup e quer trocar de arquivo para
  issue é outra demanda; esta é sobre o primeiro contato.
- **Provedores além do GitHub.** O modo issue é GitHub por decisão registrada em
  [ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md), e nada aqui muda isso.

## Verificação, quando virar spec

Os dois ramos do `setup` têm que rodar num diretório novo, **e a skill tem
`disable-model-invocation: true`**: nenhum agente a invoca nem imita o roteiro por fora, então a
verificação é do titular e a spec já nasce sabendo disso. O ramo issue **nunca teve uma passada** —
condição que o encerra em
[a profundidade da pasta quebra os links](../concluidas/a-profundidade-da-pasta-quebra-os-links.md),
e que esta demanda herda: `gh label list` devolvendo os três `aicf:*` num repositório criado pelo
próprio setup.
