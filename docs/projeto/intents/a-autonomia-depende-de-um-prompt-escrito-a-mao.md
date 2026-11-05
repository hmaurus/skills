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
  acrescenta os casos dele.
- **A autorização de publicar:** se o aicf traz a ordem dos passos (merge, CI no mesmo SHA,
  deploy) como modelo, ou se ela é só do projeto.
- **As perguntas das skills:** se cada skill que pergunta ganha uma frase ("com o usuário
  ausente, escolher a recomendada e registrar"), ou se o contrato cobre todas de uma vez.
- **Onde ficam as decisões tomadas sem o usuário:** seção do relatório do `fechar-demanda`, a
  linha `Processo` da spec, ou os dois.
