# 0002 — A conferência do índice corre num sentido só

Data: 2026-09-09 · Status: aceita · Versão: `0.14.0`

## Contexto

O passo 5 do `/aicf:fechar-demanda` mandava "conferir se a execução criou item novo no checklist ou
tornou algum obsoleto". Num projeto que consome estas skills, o `CHECKLIST.md` derivou em três
lugares e o agente não achou nenhum sozinho — nem no ritual, nem nas duas vezes em que o titular
mandou conferir. A causa não era desatenção: *"está atualizado?"* devolve ao conferente a escolha
do que conferir, e ele inventa uma lista de suspeitas nova a cada passada.

A correção óbvia é trocar julgamento por enumeração: nomear pares `seção ↔ pasta` e comparar. Mas
comparar em que sentido? A primeira redação dizia "arquivo na pasta sem linha na seção, **ou linha
sem arquivo**, é a diferença a corrigir". A revisão de código apontou que essa frase dá uma
instrução só para dois casos com correções opostas, e que o segundo é perigoso: linha em `Entregue`
cujo arquivo não aparece — porque foi movido, renomeado, ou é anterior à estrutura atual — levaria
o agente a apagar a linha. Seria a mesma falta que o passo existe para impedir, invertida.

Pior, linha sem arquivo não é anomalia: é o estado normal de um projeto novo. O `README.md` e o
`criar-prd` mandam tirar o primeiro `CHECKLIST.md` do PRD, com cada coisa que o produto precisa ter
virando uma linha, e **só** o que precisa de contexto virando arquivo. Um checklist recém-nascido é
quase todo linhas sem arquivo. Uma conferência bidirecional as reportaria em bloco como defeito.

## Decisão

**A conferência é de inclusão, não de igualdade: todo arquivo da pasta tem linha na seção, e o
inverso não é exigido.**

- Arquivo sem linha é a falta a corrigir — é a deriva que motivou a demanda, e cobre também o item
  entregue que foi apagado em vez de movido.
- Linha sem arquivo é legítima e não se toca. O passo diz explicitamente para **nunca apagar linha
  por não achar arquivo**.
- Seção sem pasta correspondente — `Fundação`, `Backlog` — fica fora da enumeração.

## Alternativas descartadas

- **Igualdade nos dois sentidos.** Simétrica e fácil de descrever, mas transforma o estado normal
  de um projeto novo em lista de defeitos, e induz o agente a apagar item de `Entregue` — a falta
  que a demanda mais queria impedir.
- **Exigir arquivo para toda linha do checklist.** Tornaria a igualdade verdadeira, ao custo de
  matar a demanda que cabe numa linha — que é recurso do método, não descuido, e está escrito no
  `README.md` e no template desde o começo.
- **Cada projeto declara seus pares num arquivo.** Cobriria seção que o projeto inventou (o caso
  original era uma seção de ADRs criada por conta), mas a declaração é ela mesma um índice que
  envelhece — resolveria a deriva criando outra, e o lema do projeto marca "dois mecanismos
  coexistindo" como gatilho de revisão.

## Consequências

- **Linha órfã não é detectada.** Arquivo movido ou renomeado deixa uma linha apontando para o
  nada, e a enumeração não acusa. O contrapeso é o passo 2 do ritual, que ao mover a demanda manda
  rodar `grep -rn "<nome-do-arquivo>" --include="*.md" .` e corrigir as referências — a deriva é
  impedida na origem em vez de detectada depois.
- O link quebrado continua achável por ferramenta genérica de markdown, fora do ritual.
- Reverter significaria reescrever o passo 5 do `fechar-demanda`, as notas de seção dos dois
  checklists (template e instância) e a decisão sobre onde vive a linha que nunca vira arquivo, no
  `criar-prd` e nos dois READMEs.
