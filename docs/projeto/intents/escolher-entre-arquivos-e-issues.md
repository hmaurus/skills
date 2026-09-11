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
| Estado de uma demanda | pasta **e** linha no checklist | um label |
| Erro de estado | detectável: as duas fontes divergem | silencioso: o label é fonte única |
| Referência a outra demanda | link relativo, quebra ao mover | `#12`, estável |
| Busca e `grep` no repositório | direto | não |
| Relatório de fechamento achável anos depois | arquivo versionado | comentário em issue fechada |
| Depende de fornecedor | não | GitHub, Linear, … |

As três linhas do meio são a mesma moeda, e a leitura fácil delas é errada. Índice gerado **não
quer dizer estado correto**: o que a lista de issues gera é a lista, não a correção dos labels, e
label se aplica à mão como arquivo se move de pasta. O `triage` do Matt detecta issue sem label e
issue com dois labels de estado em conflito; **não detecta label errado** — issue marcada
`ready-for-agent` que já foi implementada é indistinguível de uma que não foi.

O arquivo guarda o estado duas vezes (a pasta, e a linha na seção). Isso parece puro custo, e é o
que torna o erro **detectável**: duas fontes divergem de forma mecânica de achar, que é o que o
passo 5 do fechamento explora desde a `0.14.0`. A issue guarda uma vez só — menos chance de errar,
e nenhuma chance de perceber.

Então a escolha real não é entre "erra" e "não erra": é entre **erro detectável com ritual** e
**erro silencioso sem ritual**.

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
- **O que acontece com o `CHECKLIST.md`.** Com issues ele perde as três seções que espelham pastas
  (`Decidido`, `Em andamento`, `Entregue`, desde a `0.14.0`); `Fundação` e `Backlog` não têm
  equivalente em issue e são o que sobraria.

## Relação com as outras demandas

- **Habilita** [governança em issues neste repositório](governanca-em-issues-neste-repo.md), que
  deve consumir esta opção em vez de customizar por fora — este repositório vende o método e não
  pode divergir dele em silêncio.
- **Trocaria o mecanismo** de [o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md),
  entregue na `0.14.0`, por nenhum: o passo 5 não teria dois conjuntos para comparar. Isso **não é
  o problema resolvido** — é o problema ficando indetectável. Quem ficar em arquivo continua com o
  passo 5, e a entrevista precisa decidir se as duas mídias coexistem na mesma skill.
- **Não toca a classe B.** Número e veredito no corpo da issue apodrecem igual, e sem `grep` no
  repositório remedir fica mais difícil. O Matt ataca isso evitando afirmação perecível
  (`AGENT-BRIEF.md`: "Don't reference file paths — they go stale"); o aicf ataca instrumentando-a.
  São estratégias diferentes para o mesmo problema, e a migração não dispensa nenhuma das duas.
- **Bloqueia** [a conferência do índice vira script](a-conferencia-do-indice-vira-script.md)
  enquanto estiver em curso: um script que compara seções com pastas não se desenha sem saber se
  as pastas continuam existindo.
