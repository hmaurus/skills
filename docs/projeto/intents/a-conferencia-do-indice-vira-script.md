# A conferência do índice vira script, e a skill encolhe

Processo — entrevista: a definir · implementação: a definir

## Problema

O passo 5 do `/aicf:fechar-demanda` descreve, em prosa, uma operação que não tem julgamento
nenhum: comparar o conteúdo de três pastas com as linhas de três seções de um arquivo. São **15
linhas** (`awk '/^5\. \*\*Conferir/,/^O fechamento vai/' skills/fechar-demanda/SKILL.md | head -n -2 | wc -l`,
2026-09-09) num arquivo de **130** (`wc -l < skills/fechar-demanda/SKILL.md`) que carrega em toda
demanda fechada, de todo projeto que usa o plugin.

E é prosa que descreve exatamente o que um `for` faz. Durante a implementação da demanda que criou
o passo, a conferência foi executada quatro vezes — sempre por um script de ~20 linhas escrito na
hora, nunca lendo a instrução e comparando à mão. O script foi descartado ao fim de cada uso.

A instrução em prosa tem dois custos que o script não tem:

- **Contexto em toda demanda**, mesmo nas que não derivaram nada.
- **Uma tradução a cada uso.** O agente lê a descrição, escreve o código que a implementa e roda.
  A tradução pode sair diferente a cada vez — e a primeira versão do passo 5 já provou que a
  descrição em prosa comportava uma leitura destrutiva, que só a revisão pegou.

## Por que agora, e por que não antes

A intent original ([o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md))
tinha isso como **direção 4** e descartou: hook mora no projeto que consome o plugin, então o aicf
teria que gerar e manter um script lá, e a lista fechada em prosa cobria a classe A sem código
nenhum. O descarte foi certo para aquela decisão. Duas coisas mudaram depois:

1. **O custo em linhas ficou medido.** O `fechar-demanda` cresceu 23% naquela versão — de 106 para
   130 linhas, já depois de uma poda de 7. Na hora do descarte, "mais pesada" era estimativa.
2. **A semântica virou contrato.** O [ADR 0002](../../adr/0002-conferencia-do-indice-por-inclusao.md)
   fixou que a conferência é de inclusão num sentido só, com `Fundação` e `Backlog` fora. Isso é
   especificação executável — antes dele, um script teria que adivinhar a regra que a prosa ainda
   estava descobrindo.

## O que decidir na entrevista

- **Onde o script mora, e como a skill o alcança.** Um arquivo no plugin, invocado por caminho
  absoluto, é um arquivo só para todos os projetos — mas depende de a skill conseguir referenciar
  o próprio diretório de instalação, o que precisa ser verificado na documentação do Claude Code
  antes de virar desenho. A alternativa é o `/aicf:setup` copiar o script para o projeto, e aí são
  N cópias que derivam entre si — o gatilho de revisão do lema, na demanda que existe para
  combater deriva.
- **Em que linguagem, e o que isso exige do projeto.** `python3` está presente aqui e nos dois
  ambientes de desenvolvimento do mantenedor, mas o plugin é distribuído e não pode assumir. Bash
  puro é mais portável e menos legível para esta tarefa. Node exige o runtime.
- **O que o script faz fora do layout padrão.** Hoje o passo 5 diz "no layout padrão, sob
  `docs/projeto/`" e para aí. Um script precisa decidir: falha, avisa e passa, ou aceita os
  caminhos por argumento.
- **O que sobra na skill.** A regra que impede o passo de destruir o checklist ("nunca apagar linha
  por não achar arquivo") descreve o que fazer com o **resultado**, não como obtê-lo — provavelmente
  fica, mesmo com script. O que sai é a descrição da comparação.
- **Script invocado pela skill, ou hook.** O critério do `/aicf:workflow-demanda`: hook é para regra
  que precisa valer sem exceção e pode falhar sem ninguém perceber. Esta pode — foi o que aconteceu
  três vezes no episódio original. Mas hook roda em gatilho de ferramenta, e a conferência quer
  rodar no fechamento; o encaixe precisa ser verificado, não presumido.
- **Se o script também confere links relativos.** O passo 2 ganhou um `grep` para os links que o
  `git mv` quebra, e o mesmo script cobriria os dois — ou isso é escopo se expandindo.

## Restrição de desenho

**O script não pode exigir manutenção paralela à skill.** A demanda que originou esta é sobre dois
mecanismos que descrevem a mesma coisa e derivam um do outro. Trocar prosa por prosa+script sem
que um seja claramente a fonte é criar o defeito num lugar novo — se a skill continuar descrevendo
a comparação *e* mandando rodar o script, não houve poda, houve duplicação.

## Relação com as outras demandas

- **Depende de** [escolher entre arquivos e issues](escolher-entre-arquivos-e-issues.md) não estar
  em curso ao mesmo tempo: se a governança puder morar em issues, o script conferiria pares que
  talvez não existam mais. Fazer as duas em paralelo é retrabalho garantido.
- **Encolhe** o arquivo que [a entrada de quem chega](a-entrada-de-quem-chega.md) vai ter que
  descrever para iniciante, o que ajuda aquela demanda — mas não a bloqueia.
