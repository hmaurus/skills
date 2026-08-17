---
name: criar-prd
description: Entrevista o usuário sobre o produto — problema, público, escopo, sucesso — e escreve o PRD do projeto. Rodar no começo, e de novo quando uma decisão contrariar o que está escrito.
disable-model-invocation: true
---

# Criar o PRD por entrevista

O PRD responde o que nenhuma linha de código responde: para quem o produto existe, o que ele
não vai fazer, e o que conta como sucesso. É o documento do qual sai o primeiro checklist.

Rodar **fora do plan mode**: o passo final grava arquivo.

**Não confundir com `/aicf:criar-spec`.** A spec descreve uma mudança, tem escopo e um estado
"pronto". O PRD descreve o produto e é revisado toda vez que uma decisão o contraria — por
isso esta skill roda de novo, sem cerimônia de fechamento.

## Onde ele fica

`docs/projeto/PRD.md`. Se o arquivo já existe:

- **Vazio ou só com o esqueleto de seções** (o que `/aicf:setup` cria): preencher.
- **Já preenchido**: modo revisão. Ler antes de perguntar, mostrar o que já está respondido e
  entrevistar só o que mudou ou ficou aberto. Não reescrever seção que continua válida.

Se o repositório não tem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

## Como entrevistar

**Começar pelo problema, não pela solução.** Quem chega já sabendo o que quer construir vai
começar descrevendo a tela; puxar de volta uma vez — "e o que está errado hoje, para alguém
que ainda não tem isso?" — e seguir. Produto desenhado a partir da solução costuma resolver o
problema de ninguém.

Ordem que funciona: problema → quem sofre com ele → o que passa a existir → escopo → modelo →
sucesso → riscos.

Dois formatos de pergunta:

- **Pergunta aberta** para o que é descritivo — o problema, o público, a proposta. Abrir com
  menu de opções ancora quem ainda não formou opinião sobre o próprio produto.
- **`AskUserQuestion`** para o que é escolha — o que fica fora, qual modelo, qual sinal conta
  como sucesso.

Uma pergunta de cada vez. Cobrir o que o usuário talvez não tenha considerado, e não gastar
rodada com o que ele já disse.

## As três armadilhas

**"Fora de escopo" respondido com vazio.** É a seção que mais se paga — a que impede a mesma
discussão de voltar em seis meses — e a que todo mundo pula. Se o usuário disser "nada por
enquanto", listar o que apareceu na conversa e não entrou, e perguntar de cada item: foi
decisão ou foi esquecimento? Decisão vai para a seção **com o motivo**; esquecimento volta para
o escopo.

**Preencher o que ele não sabe.** Público sem resposta é "a definir", não um perfil plausível
inventado pelo agente. Métrica de sucesso sem resposta é "a definir". Documento com resposta
inventada é pior que documento com lacuna: a lacuna alguém preenche, a invenção alguém segue.

**Virar especificação técnica.** Stack, modelo de dados e biblioteca não entram aqui — viram
ADR em `docs/adr/` quando forem decididos. O PRD fala em linguagem de produto.

## O que o PRD precisa conter

- **Problema** — o que está errado hoje, do ponto de vista de quem sofre com isso
- **Público** — quem usa; se há mais de um perfil, o que cada um quer de diferente
- **Proposta** — o que passa a existir, em linguagem de produto
- **Escopo** — o que está dentro, e o que ficou fora **por decisão**, com o motivo
- **Modelo** — como se sustenta; se não se aplica, dizer que não se aplica
- **Sucesso** — como saber que deu certo, com o que dá para medir ou o sinal que serve de prova
- **Riscos** — o que pode inviabilizar, e o que se faz se acontecer

Datar a última revisão no topo. O PRD é vivo, e saber quando ele parou de ser revisado importa.

## Ao terminar

1. Mostrar o PRD e pedir revisão antes de considerá-lo fechado.
2. **Propor tirar dele o primeiro `CHECKLIST.md`** — cada coisa que a proposta exige vira uma
   linha; o que precisar de contexto vira arquivo em `demandas/`.
3. Se apareceu vocabulário próprio que já se mostrou ambíguo — dois nomes para a mesma coisa,
   ou o mesmo nome para duas —, sugerir `domain-modeling` (Matt Pocock) para gravar o glossário
   em `CONTEXT.md`, ao lado do PRD e não dentro dele.
4. Sugerir `/clear` antes da primeira demanda: o contexto da entrevista já cumpriu seu papel.
