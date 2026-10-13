# O caminho do Matt não oferece o implement-spec

Processo — entrevista: a definir · implementação: a definir

O `/aicf:implementar-spec` só conhece um jeito de trabalhar os tickets do Matt: `/implement`
ticket a ticket, com `/clear` entre eles (tabela de caminhos em `skills/implementar-spec/SKILL.md`,
linha do Matt Pocock). Nas skills do Matt (versão 1.3.1) também existe o **`/implement-spec`**: ele
lê os tickets como grafo de tarefas pelas linhas de bloqueio, roda subagentes implementadores
em background, cada um na sua worktree e pelo `/tdd`, junta tudo numa branch de integração com
um subagente de merge, faz um `/code-review` final e apaga as worktrees. Também é
`disable-model-invocation: true`. Num projeto real, com os 14 tickets de uma spec já criados, o
aicf entregou só o comando do `/implement`, e o titular foi descobrir o `/implement-spec` pelo
`/ask-matt`. Decidido: o aicf passa a oferecer o `implement-spec` como segunda forma do caminho
do Matt.

## O que já se sabe

- **Onde o aicf lista as skills do Matt:** a tabela e os comandos do passo 3 de
  `skills/implementar-spec/SKILL.md`, o critério de sugestão em `skills/criar-spec/SKILL.md` e a
  linha "Coleções de skills de workflow instaladas" do template `skills/setup/templates/claude-md.md`,
  que diz quais skills de caminho só o usuário invoca. Hoje essa linha cita `grill-with-docs`,
  `to-spec`, `to-tickets` e `implement`. Um projeto já acrescentou o `implement-spec` à mão.
- **Onde cada forma se encaixa, segundo o `/ask-matt`:** `/implement` por ticket quando o titular
  quer conduzir cada ticket; `/implement-spec` quando prefere orquestrar a construção inteira de
  uma vez.
- **A worktree nasce sem o estado que não está versionado:** `.env`, banco e pastas no gitignore.
  Isso bate de frente com a regra de workspace do próprio `implementar-spec` ("nunca quando a
  verificação depende de estado não versionado"). No projeto que motivou a intent, os testes de
  domínio funcionam na worktree, porque leem a conexão da configuração versionada e usam dados
  únicos num Postgres compartilhado. Já o servidor local e o e2e precisam do `.env` e têm de rodar
  no checkout principal, na branch de integração.
- **Paralelismo com banco compartilhado** só é seguro se nenhum ticket paralelo gerar migration.
  No projeto que motivou a intent, o `to-tickets` já concentrou toda a migration no primeiro
  ticket por esse motivo.
- **A integração muda de forma:** o `/implement` commita na branch atual; o `/implement-spec`
  cria uma branch de integração e, conforme o tracker, abre um PR em rascunho. O aicf precisa
  dizer o que acontece depois: merge na branch de origem, PR, e o commit de fechamento indo onde o
  código ficou, como já manda o passo "Verificar e fechar".

## Em aberto para a entrevista

- **Uma linha na tabela ou duas:** o Matt continua um caminho só, com duas formas de executar,
  ou o `implement-spec` vira uma linha própria da tabela, com o critério de sugestão dele.
- **Critério para sugerir cada forma:** tamanho do grafo, largura da fronteira, dependência de
  estado não versionado e migration concentrada num só ticket.
- **O que o aicf avisa antes do `/implement-spec`:** `.env` e banco nas worktrees, migration fora
  do ticket que a concentra, e onde rodar a verificação ponta a ponta.
- **Fechamento:** o `/aicf:fechar-demanda` depois do `implement-spec` roda uma vez só, sobre a
  branch de integração, e o merge dela na branch de trabalho é pergunta ao titular.
- **Setup:** o template do `CLAUDE.md` passa a citar o `implement-spec`, e o setup de projeto já
  rodando ([intent](o-setup-nao-serve-a-projeto-ja-rodando.md)) atualiza a linha em projetos que
  já existem.
