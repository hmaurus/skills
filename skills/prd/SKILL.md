---
name: prd
description: Cria ou atualiza o PRD do projeto. Vazio, entrevista o usuário sobre o produto — problema, público, escopo, sucesso — e escreve; preenchido, confere o PRD contra as demandas, os ADRs e o glossário antes de perguntar, e entrevista só o que o projeto não responde. Rodar no começo, e de novo quando uma decisão contrariar o que está escrito.
disable-model-invocation: true
argument-hint: "[arquivo, pasta ou texto de contexto]"
arguments: contexto
---

# Criar ou atualizar o PRD

O PRD responde o que nenhuma linha de código responde: para quem o produto existe, o que ele não
vai fazer, e o que conta como sucesso. É o documento do qual saem as primeiras demandas.

Rodar **fora do plan mode**: o passo final grava arquivo.

**Não confundir com `/aicf:criar-spec`** — a spec descreve uma mudança e tem um estado "pronto";
o PRD descreve o produto e é revisado toda vez que uma decisão o contraria, por isso esta skill
roda de novo, sem cerimônia de fechamento.

## Onde ele fica

`docs/projeto/PRD.md`. Se já existe preenchido, é **modo revisão**: ler antes de perguntar,
mostrar o que já está respondido e entrevistar só o que mudou ou ficou aberto — não reescrever
seção que continua válida. Sem `docs/projeto/`, perguntar onde gravar em vez de inventar pasta.

## Modo revisão: conferir o PRD contra o projeto

O PRD envelhece sem ninguém dizer: a demanda que contraria o escopo fecha, e o texto continua
afirmando o contrário. Antes da primeira pergunta, confrontar cada seção com o repositório. As
demandas moram onde a linha `**Mídia do registro:**` do `CLAUDE.md` diz — no modo arquivo,
`docs/projeto/` (`concluidas/`, `specs/`, `intents/`, `backlog/` e o `ROADMAP.md`); no modo issue,
`gh issue list --state all --label <aicf:spec|aicf:intent|aicf:backlog>`, fechada é concluída.

- **Escopo, Dentro** — item cuja demanda já está concluída; item que ainda não tem demanda nenhuma.
- **Escopo, Fora** — item que voltou como demanda aberta, ou que já foi concluído.
- **Riscos** — data ou condição que já passou.
- **Público e Modelo** — contra o `GLOSSARY.md` e os ADRs (`docs/adr/`): termo trocado, decisão de
  modelo registrada fora do PRD.
- **Afirmação verificável** — número, nome de comando ou lista que o repositório desmente.
- **Ponteiro antigo** — o cabeçalho que diz "revisar por `/aicf:criar-prd`" passa a dizer
  `/aicf:prd`, sem perguntar: é o nome anterior desta skill.

Mostrar o resultado antes da entrevista, seção por seção, cada divergência com a fonte — arquivo
da demanda, issue, ADR, commit — e separada em dois grupos:

- **Fato** — o agente corrige no texto proposto: contagem, nome, risco cuja data passou sem ter
  acontecido.
- **Decisão** — só o usuário responde, e é o que vai para a entrevista: se a mudança de escopo foi
  decisão ou deriva, o motivo de um item novo em Fora, as metas de Sucesso, o que fazer com um risco
  vencido.

Seção sem divergência e sem pergunta do usuário fica como está.

## Material de partida

Material passado na invocação: $contexto

Vazio, a entrevista começa do zero. Se for caminho de arquivo, ler o arquivo; se for pasta, ler
os arquivos de texto dentro dela; se for texto, o texto é o material. Ler antes da primeira pergunta, mostrar seção por seção do PRD o que ele já
responde, e entrevistar o resto — como no modo revisão, com uma diferença: o PRD existente foi
decidido, o material não. O que ele afirma **se confirma com o usuário** antes de entrar no PRD,
e o que ele não diz continua lacuna, não vira inferência.

## Como entrevistar

**Começar pelo problema, não pela solução.** Quem chega já sabendo o que quer construir começa
descrevendo a tela; puxar de volta uma vez — "e o que está errado hoje, para alguém que ainda
não tem isso?" — e seguir. Produto desenhado a partir da solução resolve o problema de ninguém.

Ordem que funciona: problema → quem sofre com ele → o que passa a existir → escopo → modelo →
sucesso → riscos.

Uma pergunta de cada vez: `AskUserQuestion` para escolha (o que fica fora, qual modelo, qual
sinal de sucesso), aberta para o descritivo (problema, público, proposta) — menu ancora quem
ainda não formou opinião sobre o próprio produto.

## As três armadilhas

**"Fora de escopo" respondido com vazio.** É a seção que mais se paga — a que impede a mesma
discussão de voltar em seis meses — e a que todo mundo pula. Diante de "nada por enquanto",
listar o que apareceu na conversa e não entrou, e perguntar de cada item: foi decisão ou
esquecimento? Decisão vai para a seção **com o motivo**; esquecimento volta para o escopo.

**Preencher o que ele não sabe.** Público sem resposta é "a definir", não um perfil plausível
inventado pelo agente. Documento com resposta inventada é pior que documento com lacuna: a
lacuna alguém preenche, a invenção alguém segue.

**Virar especificação técnica.** Stack, modelo de dados e biblioteca não entram aqui — viram ADR
em `docs/adr/` quando forem decididos. O PRD fala em linguagem de produto.

## O que o PRD precisa conter

- **Problema** — o que está errado hoje, do ponto de vista de quem sofre com isso
- **Público** — quem usa; se há mais de um perfil, o que cada um quer de diferente
- **Proposta** — o que passa a existir, em linguagem de produto
- **Escopo** — o que está dentro, e o que ficou fora por decisão, com o motivo
- **Modelo** — como se sustenta; se não se aplica, dizer que não se aplica
- **Sucesso** — o que dá para medir, ou o sinal que serve de prova
- **Riscos** — o que pode inviabilizar, e o que se faz se acontecer

Datar a última revisão no topo: o PRD é vivo, e saber quando parou de ser revisado importa.

## Ao terminar

1. Mostrar o PRD e pedir revisão antes de considerá-lo fechado. No modo revisão, mostrar só o texto
   novo de cada seção que muda, gravar com a aprovação e atualizar a **Última revisão**.
2. **Propor tirar dele as primeiras demandas** — cada coisa que a proposta exige vira uma; no modo
   revisão, cada item de Escopo que ainda não tem demanda. No
   **modo arquivo**, isso é o primeiro `ROADMAP.md`: uma linha em `Próximas` ou `Backlog` conforme
   a certeza, e o que precisar de contexto vira arquivo em `intents/`, e aí **a linha sai** — quem
   tem arquivo não tem linha. No **modo issue** não há roadmap: cada uma nasce como issue com
   `aicf:intent` ou `aicf:backlog`. A linha `**Mídia do registro:**` do `CLAUDE.md` diz qual
   arquivo de [`midia/`](../midia/) seguir — `arquivo.md` ou `issues.md`; sem linha, arquivo. Se `docs/agents/issue-tracker.md` discordar da
   linha, avisar uma vez e seguir a linha.
3. Se apareceu vocabulário já ambíguo — dois nomes para a mesma coisa, ou o mesmo nome para duas
   —, sugerir `domain-modeling` (Matt Pocock) para gravar o glossário em `GLOSSARY.md`, ao lado do
   PRD e não dentro dele.
4. Sugerir `/clear` antes da primeira demanda: o contexto da entrevista já cumpriu seu papel.
