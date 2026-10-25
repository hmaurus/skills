# O pitch do README põe na frente o que o titular ainda não validou

Processo — entrevista: a definir · implementação: a definir

A abertura do `README.md` organiza o argumento em três perguntas: "Onde o projeto está?", "Por que
decidimos não fazer aquilo?" e "O que saiu de fato?". A terceira apresenta o relatório do
`/aicf:fechar-demanda` como um dos três pilares do plugin
(`grep -n 'O que saiu de fato' README.md`).

Em 2026-10-25, preparando um vídeo sobre o workflow, o titular disse que não vê o relatório como a
virtude central do aicf e que ainda não validou o quanto ele importa. A ordem que ele dá às
virtudes, da mais para a menos importante:

1. gestão de produto (PRD, roadmap, registro de demandas);
2. Superpowers e Matt Pocock juntos;
3. skills escritas a partir das recomendações oficiais da Anthropic;
4. o agente sugere o caminho de implementação de cada demanda;
5. a última mensagem diz se há pendência antes de fechar ou limpar a sessão, o que ajuda a limpar
   o contexto entre um trabalho e outro;
6. feitas pelo titular, que pode ajustá-las sem receio porque conhece o funcionamento;
7. leves de propósito, sem motor de execução: são só skills, interferem pouco no harness e podem
   ser combinadas ou usadas em parte;
8. não depende do Claude Code;
9. `/aicf:setup`;
10. `/aicf:proxima-demanda`;
11. registro em arquivo ou em issue do GitHub;
12. fechamento com relatório.

Ficou de fora da lista e vale considerar na entrevista: as skills são em português, o que o
titular citou como virtude na mesma conversa.

## O que já se sabe

- **"Por que decidimos não fazer aquilo?" tem estudo a favor.** Entender o motivo por trás do
  código existente foi o problema sério mais citado por devs da Microsoft (66%) em LaToza, Venolia
  & DeLine, ICSE 2006 ([PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p492-latoza.pdf));
  Ko, DeLine & Venolia, ICSE 2007, chegam ao mesmo ponto
  ([PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf)). Essa pergunta
  sustenta a gestão de produto, que é a virtude número 1.
- **"O que saiu de fato?" não tem.** Nenhum estudo encontrado mede o valor de registrar, depois de
  cada demanda, o que saiu diferente do planejado. A pesquisa achou só opinião de praticante e o
  playbook da Anthropic, que pede para atualizar o `plan.md` no mesmo commit quando a implementação
  se desvia ([AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)).
- **O relatório nasceu depois do fechamento.** Num projeto privado que deu origem ao aicf, o
  fechamento começou como mudança de estado (marcar a spec como concluída) e revisão do checklist;
  o relatório entrou dias depois, a partir de um bug com duas causas encadeadas, junto com a
  promoção das lições para um doc de aprendizado.
- **O custo do relatório é baixo, mas não é zero.** Nas 46 demandas concluídas deste repositório
  que têm relatório, a mediana é de 495 palavras (mínimo 107, máximo 2.011), e a skill
  `fechar-demanda` tem 1.758 palavras, carregadas só no fim da sessão. Remedir:

  ```bash
  for f in docs/projeto/concluidas/*.md; do awk '/^## Relatório de implementação/{f=1} f' "$f" | wc -w; done | awk '$1>0' | sort -n | awk '{a[NR]=$1} END {print NR, a[int((NR+1)/2)], a[1], a[NR]}'
  wc -w skills/fechar-demanda/SKILL.md
  ```

- **A comparação com os vizinhos tem demanda própria:**
  [a comparação com os vizinhos envelheceu no pós-demanda](a-comparacao-com-os-vizinhos-envelheceu-no-pos-demanda.md).
  Se as duas forem feitas juntas, a seção "Por que este" muda nas duas.

## Perguntas para a entrevista

- A abertura troca as três perguntas por outra estrutura, ou mantém as perguntas e muda quais
  são? "O que saiu de fato?" sai, desce ou fica como algo em teste?
- Quantas virtudes cabem na primeira tela, e em que ordem?
- "Motor de execução" precisa de explicação em palavras comuns no README: as skills do aicf dizem o
  que registrar e quando, e quem executa o código é o agente ou o framework escolhido.
- O `README.en.md` acompanha na mesma demanda.
