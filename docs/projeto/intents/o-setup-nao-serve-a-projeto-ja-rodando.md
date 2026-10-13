# O setup não serve a projeto já rodando

Processo — entrevista: a definir · implementação: a definir

O `/aicf:setup` foi desenhado para rodar uma vez, no começo do projeto: a descrição diz "Rodar uma
vez, no começo do projeto", e o texto diz que trocar de mídia num projeto que já tem governança
montada "não é dele" (`grep -c 'roda uma vez' skills/setup/SKILL.md` → 1). Quem adota o aicf num
projeto em andamento, ou quer refazer uma parte do setup depois de outra coleção mudar o ambiente,
não tem comando para isso. Decidido: o setup passa a servir também a projeto já rodando.

## O que já se sabe

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
