# O índice envelhece sem avisar, e pedir atenção não conserta

Processo — entrevista: a definir · implementação: a definir

## Problema

Num projeto privado que consome estas skills, o `CHECKLIST.md` ficou desatualizado em três lugares diferentes, e o agente
**não percebeu nenhum deles sozinho** — nem rodando o ritual de fechamento, nem quando o titular
perguntou "tem certeza que o checklist tá atualizado?", nem na terceira vez, quando a pergunta já
apontava para a seção certa.

Cada falta foi achada só quando o titular estreitou a pergunta. Sem isso, as três teriam ficado.

### As três faltas

| # | O que estava errado | Achado quando |
| --- | --- | --- |
| 1 | ADR 0004 e 0005 ausentes da seção que lista todos os ADRs | o titular perguntou "tá atualizado?" |
| 2 | Item entregue **apagado** do backlog em vez de movido para Entregue | o agente reviu por conta, depois de cobrado |
| 3 | Item de backlog descrevendo como pendente uma decisão **já tomada e aplicada** | o titular perguntou "e o backlog?" |

A #3 é a mais grave: o backlog descrevia um efeito indesejado nos números como se ainda
acontecesse, e propunha a regra que o corrigiria. Essa regra já estava em vigor havia commits, e o
efeito era zero havia o mesmo tempo. O texto continuava plausível — a medição citada ainda batia,
era só o **veredito** que tinha virado mentira.

### Por que o ritual não pegou

O passo 5 do `/aicf:fechar-demanda` diz:

> **Conferir se a execução criou item novo no checklist ou tornou algum obsoleto**, e ajustar
> inline.

O agente leu "a execução" como **a implementação** — o código que acabou de escrever — e conferiu
se o trabalho feito criava ou encerrava itens de trabalho. Não conferiu a saída do **passo 4, que
tinha acabado de rodar** e que criou um ADR novo. O passo 5 audita o que veio antes do ritual, e é
cego para o que o próprio ritual produziu, embora o passo 4 exista justamente para produzir ADR,
regra e doc de referência — exatamente as coisas que um índice precisa listar.

**Os passos 4 e 5 não se falam.** É o mesmo formato de defeito da
[orquestração entre governança e framework](../specs/concluidas/orquestrar-o-framework-escolhido.md):
não é falta de zelo, é texto que aponta para o lado errado.

### Por que as duas conferências extras também não pegaram

Aqui está o achado que descarta a solução fácil. Nas duas vezes em que o titular mandou conferir,
o agente **conferiu de verdade** — e mesmo assim errou, porque *"está atualizado?"* devolve ao
conferente a escolha do que conferir. Ele inventou uma lista de suspeitas a cada passada:

- 1ª passada: ADRs, contagem de comandos, número de contas, o número `919`. Achou a #1. A lista
  não incluía os vereditos do backlog.
- 2ª passada: só quando a pergunta disse "backlog" é que cada item foi medido contra os dados.

Três listas ad-hoc, três recortes diferentes, e cada recorte deixou algo de fora. **A instrução
precisa dizer o que enumerar, não pedir um julgamento sobre estar em dia.** Instrução mais enfática
já foi testada duas vezes neste episódio e falhou as duas.

## As duas classes de deriva

Elas têm causas diferentes e não se corrigem com o mesmo mecanismo.

**Classe A — índice × diretório.** A seção Fundação tem que espelhar `docs/adr/`. A ajuda do CLI
tem que espelhar o mapa de comandos. É **diferença de conjunto**: mecânica, barata, sem julgamento
nenhum. Falta #1 é desta classe, e nunca deveria depender de alguém reparar.

**Classe B — afirmação × dado medido.** "919 linhas", "nenhuma marcada", "bloqueado por fora",
"sai como gasto e volta como entrada". São **medições congeladas em prosa**. Nada liga o texto ao
dado: quando o dado muda, a frase continua bem escrita e passa a mentir. Falta #3 é desta classe, e
é a que sobrevive a qualquer releitura atenta — reler não remede.

A falta #2 é de terceira natureza, e a mais irônica: o próprio checklist diz *"não apagar item
entregue"*. A regra estava escrita, no arquivo, uma linha acima de onde o agente apagou.

## Direções possíveis

Sem decidir — é o que a entrevista resolve.

1. **Reescrever o passo 5 para nomear o que enumerar**, incluindo a saída dos passos 1 a 4 do
   próprio ritual. Menor mudança possível, e teria pego a falta #1. Não pega a #3.
2. **Regra de escrita: afirmação medida carrega como remedir.** Número que entra em doc de
   governança vem com o comando que o reproduz. Transforma "lembrar de conferir" em "executar". É
   o que pega a #3, e o projeto em questão já faz isso pela metade — escreve a data da medição sem
   dizer o comando que a reproduz.
3. **Skill de auditoria do registro**, que enumera as afirmações verificáveis dos docs de
   governança e roda a checagem de cada uma. Mais pesada, e talvez redundante se 1 e 2 entrarem.
4. **Hook para a classe A**, que é puro conjunto e não precisa de modelo nenhum para decidir.

## Restrição de desenho

**A solução não pode ser "conferir com mais atenção".** Esse caminho já foi percorrido três vezes
neste episódio — uma pelo ritual e duas por ordem direta do titular — e falhou as três. O que
distingue uma correção boa aqui é ela **não depender de o agente escolher o que olhar**.

## Evidência

Projeto privado, 2026-09-08. As três correções foram commits separados, e **os três vieram depois**
do commit que declarou o ritual de fechamento cumprido. O titular do projeto tem os hashes.

> Exemplo mantido genérico de propósito: este repositório é público e o projeto de origem é
> privado. Detalhe que identifique o domínio dele não entra aqui.
