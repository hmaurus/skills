# A autonomia depende de um prompt escrito à mão

Processo — entrevista: a definir · implementação: a definir

Quando o usuário vai deixar a implementação rodando sozinha ("autônomo até o deploy", "vou
dormir"), o aicf não diz o que essa autonomia cobre. O agente que monta o comando da sessão
seguinte escreve as regras do zero a cada vez:
- o que decidir sem perguntar;
- quando parar;
- o que a autorização de publicar inclui;
- o que entra no relatório.

Escritas do zero, elas saem cautelosas demais. O resultado é um agente que para diante de um
problema que não era perigoso e deixa a noite perdida. O aicf não tem texto sobre autonomia
(`grep -rliE 'autônom|autonom' skills/ | wc -l` → 0, na 0.45.0). E nove arquivos de skill fazem
pergunta com opções ao usuário no caminho, entre eles o `implementar-spec`, o `matt.md` e o
`fechar-demanda`, sem dizer o que fazer quando ele não está
(`grep -rlE 'pergunta com opções|AskUserQuestion' skills/ | wc -l` → 9).

Num projeto privado que consome estas skills, o agente montou o comando de uma execução autônoma
do `/implement-spec` até o deploy em produção. O primeiro rascunho mandava parar e relatar em três
casos:
- **"CI vermelho repetido":** o e2e do projeto tem falha intermitente conhecida, e duas seguidas
  por acaso parariam tudo;
- **um registro cujo texto antigo não casou numa conversão de dados:** publicar mesmo assim
  não perdia nada, porque o texto antigo seguia no banco até a limpeza;
- **"migration a mais":** a referência do projeto manda o implementador "parar e avisar".

O usuário pediu para afrouxar: "Aja com autonomia, em decisões tome a mais recomendada e no final,
informe ao usuário". Decidido registrar como regra, para não depender de o usuário lembrar a
cada vez.

## A regra que o usuário pediu

- **Decidir pela recomendação.** Em toda decisão que a spec e os tickets não resolvem, inclusive
  as perguntas com opções das próprias skills (`/code-review`, `/aicf:fechar-demanda`, a escolha
  de caminho), o agente escolhe a opção recomendada, segue, e registra a decisão e o motivo.
- **Parar só diante do perigo.** As regras de parada de uma execução autônoma não incluem
  problema que não é perigoso. Falha intermitente se repete uma vez. Falha real se depura e se
  corrige no código, nunca no teste. Pendência que é do usuário vai para o relatório, com o
  trabalho seguindo até onde não a toca.
- **Informar no fim.** O relatório final traz o que foi ao ar, as decisões tomadas sem o usuário e
  o que ficou para ele.

## Uma área para o que é de cada usuário e projeto

Pedido do usuário (2026-11-05): a solução deve **reservar um lugar para as especificidades do
usuário e do projeto**, preenchido de preferência numa entrevista. O contrato genérico do aicf é o
padrão, e cada projeto o afrouxa ou o aperta ali.

O exemplo do projeto de origem: o usuário assume que, numa execução autônoma, o agente **pode
editar os termos de uso, os contratos e a documentação**, desde que **mostre as mudanças na tela
ao fim**, para ele ler quando voltar. É um afrouxamento da segunda lista candidata abaixo (termos
e licença voltam ao usuário), e mostra por que a lista não pode ser fixa: o que é perigo num
projeto em produção com clientes é rotina num projeto ainda não divulgado.

Na entrevista:
- **Onde a área mora:** o `CLAUDE.md` do projeto, que o agente lê em toda sessão, ou um arquivo
  próprio que o contrato cita.
- **Quem a preenche e quando:** o `/aicf:setup`, a primeira execução autônoma ou uma skill própria.
- **O formato:** o que o agente pode fazer sozinho, o que volta ao usuário e como as mudanças
  aparecem no fim. No exemplo: "registrar em tela", o trecho de cada texto publicado no relatório
  final, não só o nome do arquivo.

## O que já se sabe

- **No caso de origem, o que sobrou como parada de verdade:**
  - migration que falha em produção;
  - job de deploy vermelho depois de uma nova tentativa;
  - em ambos, sem consertar produção à mão.

  O limite de uso virou pausa: retomar o subagente parado com uma mensagem, não decidir. A
  pendência do usuário (os registros que não casaram) deixou de bloquear o deploy. Bloqueou só o passo
  que de fato perderia dado: a limpeza que apagaria o texto antigo deles.
- **A autorização de publicar precisa ser explícita e ordenada.** O projeto de origem exige pedido
  do usuário para publicar. O comando autônomo levou a autorização por escrito, com data, e a
  ordem completa:
  1. merge na branch de trabalho;
  2. push;
  3. CI verde no mesmo SHA;
  4. push para produção;
  5. job de deploy verde, não só o run.
- **A sessão autônoma precisa abrir sem pedido de permissão:** o subagente em segundo plano para
  até alguém responder. O projeto de origem documenta `claude --permission-mode bypassPermissions`
  na referência de implementação paralela. O aicf não fala disso
  (`grep -c 'bypassPermissions' skills/implementar-spec/matt.md` → 0).
- **Relacionada:** a intent [O critério de caminho ignora a presença do usuário e o
  porte](../intents/o-criterio-de-caminho-ignora-presenca-e-porte.md) trata de como a presença
  muda a *escolha* do caminho e registra o resto que a execução autônoma deixa (shells e
  subagentes abertos). Esta trata do *contrato* da execução depois de escolhido o caminho.
  Entrevistar as duas juntas pode ser o mais simples.

## O histórico do projeto de origem

O projeto de origem teve cerca de dez demandas com autonomia dada pelo usuário em um mês
(2026-10-11 a 2026-11-05). Elas estão registradas nos relatórios de fechamento, no registro
jurídico e nas memórias do agente. O que serve ao contrato, por tema:

### Decisões que o agente tomou sozinho

- **Deu errado: ampliar uma regra de domínio além da história da spec.** Uma decisão autônoma
  tratou como não removível um caso que a história não restringia. A revisão não pegou, e o
  usuário achou o problema dias depois. **Regra candidata:** a decisão pela recomendação vale
  para o *como*, nunca para estender o *o quê* do domínio. Diante de uma lacuna de regra de
  negócio, ficar com a leitura mais estreita da spec e registrar a dúvida.
- **Deu certo: desviar da spec com o motivo escrito.** Três exemplos:
  - um nome mudado para cumprir um ADR;
  - um teto criado a partir de um alerta de segurança, registrado como risco aceito;
  - fatias delegadas a subagentes, uma por vez.

  O que os fez dar certo foi a seção "o que mudou em relação à spec" no relatório.
- **Troca de caminho pela ausência do usuário:** o plan mode pede aprovação, e com o usuário
  dormindo o agente foi pelo caminho direto e registrou o motivo. Num outro caso, o plano foi
  commitado sem aprovação.
- **Texto publicado sem a revisão que o projeto pede:** em três demandas, um texto jurídico foi ao
  ar sem a revisão prevista, com a justificativa de que só havia contas de teste. Os três ficaram
  registrados como risco aceito "a confirmar pelo usuário".
- **Onde a autonomia parou, com acerto:**
  - uma revisão mostrou que a mudança exigia alterar a licença dos termos de uso, e o deploy
    esperou a escolha do usuário;
  - uma resposta inesperada do serviço de pagamento também voltou para ele.

  **Regra candidata:** além do perigo técnico, volta ao usuário o que o compromete juridicamente
  ou com quem usa o produto: mudança de licença ou de termos, novo aceite, aviso por e-mail aos
  usuários, dinheiro.

### Travas que não eram perigo

- **Contexto cheio:** uma execução parou de madrugada porque a sessão vinha de uma entrevista
  longa. Começar a execução autônoma numa sessão nova.
- **Permissão:** o pedido de permissão de um subagente em segundo plano para tudo até alguém
  responder. A sessão abre sem pedidos.
- **Limite de uso:** o subagente parado volta com uma mensagem; não se relança do zero.
- **Pergunta no meio:** um implementador parou para perguntar e, ao voltar, achou a worktree
  apagada. Quem para para perguntar commita antes.
- **Credencial inacessível ao agente** (o `.env` bloqueado): conferir a produção virou pendência
  do usuário no relatório, sem parar o resto.

### Higiene das esperas

Em duas de três madrugadas, ficaram shells e subagentes abertos ao fim. As armadilhas estão
registradas nas memórias do agente:
- `until ! pgrep -f "<cmd>"` casa com o próprio laço e nunca termina;
- `gh run list -c <sha>` com o SHA curto devolve lista vazia, sem erro, e a espera do CI nunca
  acaba;
- `pkill -f` com o padrão do comando derruba o próprio shell.

A regra que ficou: esperar pelo `run_in_background` ou pelo exit code num arquivo, usar o SHA
completo, matar pelo PID e, no fim, encerrar os servidores, os laços e as worktrees que
sobrarem.

### Publicação

- **O run do CI fica verde com o job de deploy pulado:** confirmar a publicação pelo job, não
  pelo run.
- **Dois runs vermelhos antes do verde** (memória estourada no lint e um teste instável), ambos
  corrigidos sem o usuário. Isso sustenta a regra "falha intermitente se repete; falha real se
  corrige".
- **Script de dados em produção roda primeiro em modo de ensaio** (`--dry-run`). Num caso, o
  ensaio mostrou um formato de arquivo que o script não esperava.
- **Depois do deploy, conferir a produção** com uma requisição real, não só o CI.

### O relatório no fim

O formato que se firmou:
- um status com os runs, o SHA e a conferência em produção;
- "o que mudou em relação à spec";
- "pendências do usuário";
- os riscos aceitos "a confirmar", cada um com o gatilho de revisão;
- quando a demanda não fecha, um "estado em andamento" com o próximo passo do usuário;
- o que o agente revisou sozinho (capturas de tela, o caminho que não perguntou).

## Em aberto para a entrevista

- **Onde a regra mora:**
  - um arquivo de referência do aicf (um "contrato de autonomia") que o `implementar-spec`, o
    `matt.md` e o `fechar-demanda` citam;
  - uma seção no template do `CLAUDE.md` que o `/aicf:setup` instala;
  - ou um bloco que o agente cola no comando da sessão seguinte.
- **Como a autonomia se declara:** pela leitura do prompt ("autônomo", "vou dormir"), por uma
  pergunta explícita ao entregar o comando, ou pelos dois.
- **O que é "perigoso"** numa lista genérica, que valha para qualquer projeto: dano em produção,
  perda de dado, credencial, ação irreversível fora do que foi autorizado. E onde o projeto
  acrescenta os casos dele. O histórico acima sugere uma segunda lista, do que volta ao usuário
  mesmo sem perigo técnico: termos e licença, novo aceite, aviso a quem usa, dinheiro e regra de
  domínio além da spec. As duas listas são o padrão, que a área do projeto (acima) afrouxa ou
  aperta.
- **Texto publicado sem a revisão prevista:** se a autonomia cobre, como risco aceito "a
  confirmar", ou se publicar texto jurídico entra na segunda lista.
- **A higiene das esperas:** se vai no contrato ou fica na intent da presença, que já registra o
  resto.
- **A autorização de publicar:** se o aicf traz a ordem dos passos (merge, CI no mesmo SHA,
  deploy) como modelo, ou se ela é só do projeto.
- **As perguntas das skills:** se cada skill que pergunta ganha uma frase ("com o usuário
  ausente, escolher a recomendada e registrar"), ou se o contrato cobre todas de uma vez.
- **Onde ficam as decisões tomadas sem o usuário:** seção do relatório do `fechar-demanda`, a
  linha `Processo` da spec, ou os dois.
