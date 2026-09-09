# O usuário escolhe se a governança mora em arquivos ou em issues

Processo — entrevista: a definir · implementação: a definir

## Problema

O aicf hoje assume **arquivo**. Toda skill grava e lê em `docs/projeto/`: `criar-spec` escreve em
`specs/<nome>.md`, `implementar-spec` lê de lá, `fechar-demanda` move para `specs/concluidas/` e
marca o `CHECKLIST.md`. Não há escolha — quem prefere issue tracker precisa customizar por fora, e
a customização não é suportada nem descrita.

Isso destoa do resto do próprio método. O `workflow-demanda` já oferece **três caminhos de
entrevista e quatro de implementação**, e diz que "a implementação é roteiro, não trilho". A mídia
do registro é a única coisa que continua trilho único.

E destoa do vizinho: o `to-spec` do Matt Pocock publica a spec **no issue tracker do projeto**, e
o `to-tickets` cria issues-filhas com relação nativa de bloqueio. Hoje, quem entrevista pelo Matt e
governa pelo aicf tem a spec num lugar e o registro noutro.

## Por que isso importa mais do que parece

Arquivo e issue não são só dois lugares de guardar. Cada um ganha e perde algo diferente:

| | Arquivo `.md` | Issue |
| --- | --- | --- |
| Sobrevive ao `git clone` sem rede | sim | não |
| Contribuição de quem não é mantenedor | fork + PR | dois cliques |
| Índice do que existe | mantido à mão | gerado |
| Busca e `grep` no repositório | direto | não |
| Relatório de fechamento achável anos depois | arquivo versionado | comentário em issue fechada |
| Depende de fornecedor | não | GitHub, Linear, … |

A linha do índice gerado importa para além da conveniência: índice mantido à mão é a causa da
deriva descrita em [o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md).

## O que decidir na entrevista

- **Onde a escolha é feita e onde ela mora.** Provavelmente uma pergunta do `/aicf:setup`, gravada
  em algum lugar que toda skill leia. O Matt resolve isso com um arquivo de vocabulário
  (`triage-labels.md`) gerado pelo setup dele — precedente que funciona.
- **Quanto do método muda, de fato.** A hipótese a testar é que **a governança é a mesma e só o
  substrato muda**: as quatro fases, o ritual de fechamento e a linha `Processo` seguem idênticos;
  o que troca é "mover arquivo para `concluidas/`" por "fechar a issue", e "marcar `- [x]`" por
  "aplicar o label". Se for isso, a mudança é rasa e vale. Se a entrevista descobrir que meia dúzia
  de comportamentos mudam junto, o custo é outro.
- **Modo misto é permitido?** Spec em issue e relatório em arquivo, por exemplo. Tentador, e é
  exatamente o gatilho de revisão do lema — dois mecanismos coexistindo. Provável que a resposta
  certa seja não.
- **Qual tracker.** Só GitHub, ou uma camada fina que também sirva Linear? Cuidado com abstração
  antecipando o futuro: começar só com GitHub e ver se alguém pede o resto.
- **O que acontece com o `CHECKLIST.md`.** Com issues ele perde a parte de demandas, mas a seção
  Fundação não tem equivalente em issue.

## Relação com as outras demandas

- **Habilita** [governança em issues neste repositório](governanca-em-issues-neste-repo.md), que
  deve consumir esta opção em vez de customizar por fora — este repositório vende o método e não
  pode divergir dele em silêncio.
- **Resolve parcialmente** [o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md), mas
  só para quem escolher issues. Quem ficar em arquivo continua com o problema inteiro, então as
  duas demandas são independentes e nenhuma substitui a outra.
