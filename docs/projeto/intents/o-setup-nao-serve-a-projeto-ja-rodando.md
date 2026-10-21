# O setup não serve a projeto já rodando

Processo — entrevista: a definir · implementação: a definir

O `/aicf:setup` foi desenhado para rodar uma vez, no começo do projeto: a descrição diz "Rodar uma
vez, no começo do projeto", e o texto diz que trocar de mídia num projeto que já tem a estrutura
montada "não é dele" (`grep -c 'roda uma vez' skills/setup/SKILL.md` → 1). Quem adota o aicf num
projeto em andamento, ou quer refazer uma parte do setup depois de outra coleção mudar o ambiente,
não tem comando para isso. Decidido: o setup passa a servir também a projeto já rodando.

## O que já se sabe

- **A troca de vocabulário da `0.42.0` é o primeiro caso concreto.** O template do `CLAUDE.md`
  mudou de vocabulário: a camada do aicf passou a se chamar gestão de produto, a outra engenharia
  de software, e quem fecha a demanda é "o aicf" ([ADR 0009](../../adr/0009-o-aicf-integra-superpowers-e-matt.md)). Projeto
  montado antes segue com a prosa antiga, que não quebra nada; a atualização foi pelas notas da
  release, com um pedido para colar no agente. Comparar o `CLAUDE.md` existente com o template
  e propor o diff resolveria esta troca e as próximas.
- **A ordem entre os setups importa.** O `/setup-matt-pocock-skills` grava
  `docs/agents/issue-tracker.md`; o setup do aicf lê esse arquivo para propor a mídia, e só pode
  ler se o do Matt rodou antes. Hoje, quando o Matt rodou depois, nada no aicf volta a ler o
  tracker até a primeira spec entrevistada pelo `grill-with-docs`, ou até o
  `/aicf:implementar-spec` oferecer o caminho do Matt.
- **O setup só o usuário invoca** (`disable-model-invocation: true`), e a verificação de
  comportamento dele vive em [verificacao-do-setup.md](../../referencias/verificacao-do-setup.md).
  O que mudar aqui entra com a verificação em aberto até uma passada do titular.
- Surgiu na entrevista de
  [a spec do aicf não tem histórias para o caminho do Matt](../concluidas/a-spec-nao-tem-historias-para-o-matt.md),
  que decidiu gravar a convenção da spec no tracker do Matt pelo `criar-spec` e pelo
  `implementar-spec`, e não pelo setup.

## Em aberto para a entrevista

- **O que o setup faz com o que já existe:** PRD, `ROADMAP.md`, `CLAUDE.md`, `docs/projeto/`,
  labels `aicf:*`. Pular, comparar e propor diff, ou recusar a parte.
- **O mesmo comando ou outro:** o `/aicf:setup` detecta projeto montado e muda de modo, ou nasce um
  comando separado para conferir e completar.
- **Ordem recomendada com o setup do Matt** em projeto novo, e o que o aicf faz quando o do Matt
  roda depois do dele.
- **Commit e branch:** em repositório com histórico, o setup já faz um commit na branch ativa sem
  mexer em branch nem no remoto; ver se isso basta para um projeto em andamento.
