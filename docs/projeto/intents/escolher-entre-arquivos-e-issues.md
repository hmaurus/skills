# O usuário escolhe se a governança mora em arquivos ou em issues

Processo — entrevista: a definir · implementação: a definir

> **Depende de [o `CHECKLIST.md` sai do método](../specs/concluidas/o-checklist-sai-do-metodo.md)**,
> entregue antes desta. Aquela demanda removeu o índice derivado, e com ele a maior parte do que
> aqui variava entre as duas mídias — esta encolheu de "refatorar seis skills" para "trocar quatro
> verbos". As seções abaixo já estão reescritas sob esse estado.

## Problema

O aicf hoje assume **arquivo**. Toda skill grava e lê em `docs/projeto/`: `criar-spec` escreve em
`specs/<nome>.md`, `implementar-spec` lê de lá, `fechar-demanda` move para `specs/concluidas/`.
Não há escolha — quem prefere issue tracker precisa customizar por fora, e
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
| Índice do que existe | gerado da pasta (`head -qn1`) | gerado da lista |
| Estado de uma demanda | a pasta | um label |
| Referência a outra demanda | link relativo, quebra ao mover | `#12`, estável |
| Busca e `grep` no repositório | direto | não |
| Relatório de fechamento achável anos depois | arquivo versionado | comentário em issue fechada |
| Depende de fornecedor | não | GitHub, Linear, … |

**O argumento de detecção saiu da tabela, e essa é a novidade.** Enquanto o `CHECKLIST.md` existia,
o lado do arquivo guardava o estado duas vezes — a pasta e a linha na seção — e dava para dizer que
a divergência entre as duas tornava o erro achável. A demanda que removeu o índice mostrou que o
argumento estava invertido: cópia mantida à mão não detecta erro na fonte, ela fabrica uma classe
de erro nova e depois gasta ritual achando o erro que criou.

Hoje as duas mídias guardam o estado **uma vez só**: a pasta de um lado, o label do outro. Nenhuma
das duas detecta estado errado — pasta errada e label errado são igualmente indistinguíveis de
pasta certa e label certo. O `triage` do Matt confirma pelo lado das issues: ele acha issue sem
label e issue com dois labels em conflito, e **não acha label errado**.

A escolha, então, não é mais entre erro detectável e erro silencioso. É só a tabela acima.

## O que decidir na entrevista

- **Onde a escolha é feita e onde ela mora.** Provavelmente uma pergunta do `/aicf:setup`, gravada
  em algum lugar que toda skill leia. O Matt resolve isso com um arquivo de vocabulário
  (`triage-labels.md`) gerado pelo setup dele — precedente que funciona.
- **Quanto do método muda, de fato.** A hipótese a testar é que **a governança é a mesma e só o
  substrato muda**: as quatro fases, o ritual de fechamento e a linha `Processo` seguem idênticos;
  o que troca é "mover arquivo para `concluidas/`" por "fechar a issue". A hipótese ficou mais
  forte depois que o índice saiu: o `- [x]` no checklist, que era o segundo item desta lista, não
  existe mais em mídia nenhuma.
- **Modo misto é permitido?** Spec em issue e relatório em arquivo, por exemplo. Tentador, e é
  exatamente o gatilho de revisão do lema — dois mecanismos coexistindo. Provável que a resposta
  certa seja não.
- **Qual tracker.** Só GitHub, ou uma camada fina que também sirva Linear? Cuidado com abstração
  antecipando o futuro: começar só com GitHub e ver se alguém pede o resto.
- **O que acontece com o `ROADMAP.md`.** É o que sobrou do índice: a lista do que ainda não tem
  arquivo. Com issues, `Próximas` e `Backlog` mapeiam em labels (`needs-triage` cobre o segundo),
  e o arquivo deixaria de existir — ou sobrevive, e aí é governança em duas mídias, que é o
  gatilho de revisão do lema.

## Relação com as outras demandas

- **Habilita** [governança em issues neste repositório](governanca-em-issues-neste-repo.md), que
  deve consumir esta opção em vez de customizar por fora — este repositório vende o método e não
  pode divergir dele em silêncio.
- **Não toca mais** [o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md),
  entregue na `0.14.0`. O mecanismo daquela demanda já saiu por outra via, e a decisão de mídia
  deixou de ter relação com ele.
- **Não toca a classe B.** Número e veredito no corpo da issue apodrecem igual, e sem `grep` no
  repositório remedir fica mais difícil. O Matt ataca isso evitando afirmação perecível
  (`AGENT-BRIEF.md`: "Don't reference file paths — they go stale"); o aicf ataca instrumentando-a.
  São estratégias diferentes para o mesmo problema, e a migração não dispensa nenhuma das duas.
- **Não bloqueia mais** [a conferência do índice vira script](../specs/concluidas/a-conferencia-do-indice-vira-script.md):
  aquela demanda foi cancelada, porque a comparação que ela scriptaria deixou de existir.
