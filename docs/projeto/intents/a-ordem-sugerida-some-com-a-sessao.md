# A ordem sugerida some com a sessão

Processo — entrevista: a definir · implementação: a definir

O `/aicf:proxima-demanda` lê tudo o que está aberto e responde no chat: uma recomendação, até duas
alternativas e a pergunta que decide entre elas. A ordem que ele montou para chegar ali, com o que
depende de quê e quem destrava cada uma, morre com a sessão. A próxima vez que alguém pergunta
"qual a próxima?", a leitura recomeça do zero, e nada no repositório mostra a ordem que o projeto
vinha seguindo.

Num projeto privado que consome estas skills, o usuário pediu à mão que o resultado fosse gravado
num arquivo, `docs/projeto/proximas-demandas.md`, e passou a pedir a atualização a cada rodada. A
skill não conhece esse arquivo: `grep -rc 'proximas-demandas' skills/ | grep -vc ':0'` → 0. Decidido
registrar a mudança; a sugestão do usuário é o ponto de partida da entrevista.

## A sugestão do usuário

- **Na primeira vez**, a skill pergunta se o usuário quer o arquivo criado.
- **Se o arquivo já existe**, a skill o atualiza sempre depois de rodar, sem perguntar.

## O que já se sabe

- **O formato que se firmou no projeto**, em cinco seções, abertas por um cabeçalho com a data do
  retrato e a régua (o PRD de qual data, e o que ele diz da prioridade agora):
  - **Ordem sugerida** — tabela com número, demanda, onde está (arquivo ou linha do roadmap), por
    que nesta posição, de que depende e quem destrava;
  - **Operação que depende de outra pessoa** — pequenas, fora da ordem, cada uma com o estado e
    quem age;
  - **Gatilho disparado, à espera de decisão**;
  - **Aguardam gatilho** — decididas, com a condição ainda não disparada;
  - **Backlog** — cada item com o gatilho e a data em que foi conferido.
- **O arquivo se declara "não é registro"**: cada demanda continua no lugar dela, e a tabela
  envelhece quando uma delas fecha ou muda. Por isso gravá-lo não contradiz, em espírito, a frase
  "A skill só lê e sugere; o registro fica como está" do `SKILL.md`
  (`grep -c 'A skill só lê e' skills/proxima-demanda/SKILL.md` → 1), mas a frase, como está, proíbe
  escrever qualquer coisa.
- **O arquivo envelhece entre as rodadas.** No projeto, ele acumulou "conferido em …" com várias
  datas, e uma revisão do PRD mudou a meta de sucesso citada numa linha dele antes de a skill
  rodar de novo. Demanda concluída tem de sair da tabela, e quem fecha a demanda não sabe disso.
- **A ordem vale como insumo da própria skill:** a rodada seguinte pode partir do retrato anterior
  e dizer o que mudou de posição e por quê, em vez de remontar tudo.

## Em aberto para a entrevista

- **A pergunta da primeira vez:** onde fica guardado um "não", para a skill não perguntar a cada
  rodada (linha no `CLAUDE.md`, como a da mídia do registro, ou outra marca).
- **O nome e o lugar:** `docs/projeto/proximas-demandas.md` no modo arquivo; no modo issue, um
  arquivo do mesmo jeito, uma issue fixada, ou nada.
- **O formato:** as cinco seções acima como template da skill, ou mais curto.
- **Quem mais mexe no arquivo:** se o `/aicf:fechar-demanda` tira a linha da demanda que fechou, e
  se o `/aicf:prd` avisa que a régua mudou, ou se só a próxima rodada da skill corrige.
- **Commit:** se a skill commita o arquivo sozinha (só documentação) ou deixa para o usuário.
- **O setup e a ajuda:** se o `/aicf:setup` cria o arquivo vazio e se o `/aicf:ajuda` o explica.
