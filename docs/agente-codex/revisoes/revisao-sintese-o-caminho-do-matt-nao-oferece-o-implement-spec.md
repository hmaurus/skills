# Revisão da síntese — O caminho do Matt não oferece o implement-spec

Data: 2026-10-24. Parecer consultivo sobre a proposta de síntese apresentada na
conversa, ainda não aplicada à
[spec](../../projeto/specs/o-caminho-do-matt-nao-oferece-o-implement-spec.md).
Base: `19ec7c66b4209b8a84d2b2ca4700418385d0bf2d`.
Identificação: `sha256sum docs/projeto/specs/o-caminho-do-matt-nao-oferece-o-implement-spec.md`
→ `6cce2106a9098903eb8a2013b79be309cd31b23cad3e8b55bf298af8be41d4b7`.
A revisão anterior está no [parecer da spec](revisao-spec-o-caminho-do-matt-nao-oferece-o-implement-spec.md),
já presente na base. O hash acima identifica a versão ajustada no disco, não o
conteúdo que está no index por causa do `git mv`.

Resultado: a divisão em dois arquivos é adequada, com dois ajustes P2 antes da
implementação: preservar expressamente a exceção de workspace e adaptar os
aceites estáticos à nova distribuição. Não foi identificado achado P1.
P2 significa correção necessária para preservar o comportamento ou tornar o
aceite compatível com a solução. Não há necessidade de mudar o desenho decidido.

## 1. P2 — A frase de workspace precisa manter a exceção à regra geral

**Local:** proposta, item 2, frase de workspace; spec, linhas 126–129;
`skills/implementar-spec/SKILL.md`, linhas 72–79.

A spec atual resolve expressamente a relação entre duas regras: o aicf não
escolhe o workspace do `/implement-spec`, e a restrição de worktree com estado
não versionado continua valendo para a escolha do próprio aicf. No Matt, entram
a marcação do ticket e a instrução ao orquestrador.

A frase proposta — “Com o `/implement-spec`, a branch de integração e as
worktrees são do método” — informa quem cria os recursos, mas deixa implícita a
exceção. O texto vigente ainda manda decidir o workspace em qualquer caminho,
inclusive de outra coleção, e diz “nunca” usar worktree quando a verificação
depende de estado não versionado. Saber quem cria a worktree não dispensa essa
decisão nem delimita aquela proibição.

**Consequência:** um agente pode vetar a forma paralela pelo estado local,
mesmo com o tratamento de verificação já previsto em `matt.md`, ou perguntar
novamente sobre um workspace que pertence ao método. A síntese perde uma
ressalva normativa da spec, embora preserve a descrição dos recursos.

**Ajuste sugerido:** formular a nota como exceção explícita, junto da regra de
workspace: “Com `/implement-spec`, não escolher workspace: branch e worktrees
são do método; a restrição acima vale para a escolha do aicf, e o estado não
versionado segue o tratamento de `matt.md`.” Ajustar “acima” à posição final da
nota. O procedimento continua na referência; a delimitação da regra geral fica
no passo que a aplica. O saldo de linhas é uma estimativa, subordinada a
preservar esse contrato.

Encerra quando a leitura do passo 3 distingue a escolha de workspace do aicf
da preparação do Matt, inclusive com um ticket cujo teste depende de estado
local.

## 2. P2 — As Verificações 2 e 3 reprovam o texto proposto

**Local:** proposta, itens 1 e 2; spec, Verificação 2 e 3, linhas 222–229.

O primeiro comando da Verificação 2 exige que
`grep -l 'O critério para sugerir' skills/*/SKILL.md` não encontre nada. O
ponteiro proposto começa exatamente com “O critério para sugerir está em”.
Logo, a presença da frase deixa de significar que o critério continua embutido.
Mesmo uma implementação correta devolve pelo menos o `implementar-spec/SKILL.md`.

A Verificação 3 exige uma ocorrência de `implement-spec` em `caminhos.md`.
Pela síntese, esse arquivo contém somente os quatro caminhos, dos quais o Matt
é `to-tickets`; a escolha `/implement` × `/implement-spec` muda para `matt.md`.
Um `caminhos.md` sem essa ocorrência cumpre a proposta e falha no aceite.

**Consequência:** o implementador precisa contrariar a síntese, introduzindo
texto desnecessário, ou entregar uma verificação que acusa defeito inexistente.
O segundo comando da Verificação 2, que conta os consumidores de `caminhos.md`,
continua esperando 2 e não precisa mudar de resultado.

**Ajuste sugerido:** na Verificação 2, procurar um trecho específico do
parágrafo antigo, por exemplo `subagente e com TDD`, em vez da
abertura reutilizada pelo ponteiro. Manter a contagem dos dois consumidores.
Na Verificação 3, trocar `skills/implementar-spec/caminhos.md` por
`skills/implementar-spec/matt.md` na lista de arquivos que devem mencionar
`implement-spec`. Conferir também o novo ponteiro no `implementar-spec` e sua
ausência no `criar-spec`; isso verifica a separação dos consumidores sem exigir
que o arquivo de caminhos conheça as duas formas.

**Contraprova executada:** numa árvore temporária mínima, foram escritos o
ponteiro literal da proposta e um `caminhos.md` contendo apenas os quatro
caminhos. O primeiro `grep -l` encontrou o `SKILL.md` (saída 0); o
`grep -c 'implement-spec'` em `caminhos.md` imprimiu `0` (saída 1). A árvore foi
removida ao final; nenhum arquivo de skill do repositório foi alterado.

Encerra quando os aceites descrevem a distribuição em dois arquivos, com os
comandos e resultados conferidos na implementação.

## O que a síntese preserva

**Regras e carregamento.** O ponteiro dentro do passo, com ordem expressa de
leitura antes de recomendar, satisfaz “critério mora na skill que o aplica”.
Ele carrega a referência necessária; não manda aplicar de memória o critério
de outra skill. É o mesmo mecanismo de
[`skills/midia/`](../../../skills/midia/) e da demanda
[as skills carregam o que não vão usar](../../projeto/concluidas/as-skills-carregam-o-que-nao-vao-usar.md).
A demanda [os critérios moram longe de quem os usa](../../projeto/concluidas/os-criterios-moram-longe-de-quem-os-usa.md)
rejeitava uma referência compartilhada para critérios com consumidor único;
aqui o critério dos caminhos tem dois consumidores reais.

**Entradas.** O gatilho proposto nomeia tanto a volta do `/to-tickets` quanto a
sessão nova com tickets, e nesta última proíbe repetir o comando. Não depende
da mídia, portanto cobre arquivo e issue. Ao transpor a spec, manter em
`matt.md` a identificação dos tickets por `**Spec:**` ou `## Parent`, a exceção
expressa à parada da skill e a ordem de medir antes de recomendar a forma.
O anúncio no `criar-spec` de retomar por `/aicf:implementar-spec <spec>`
continua necessário: ele atende quem chamou `/to-tickets` diretamente depois
de limpar a sessão. O ponteiro deve ser uma instrução do passo 3, fora de um
ramo exclusivo de quem acabou de criar tickets.

Com isso, não identifiquei uma entrada prevista pela spec que precise chegar
ao fluxo novo sem encontrar o ponteiro. Quem invoca `/implement-spec`
diretamente, por conta própria, não passa pelo aicf; garantir a preparação
nesse caso ampliaria o comportamento decidido.

**Itens 1 a 7.** O item 1 permanece na tabela. No item 2, o gatilho fica na
skill e o reconhecimento dos tickets, as quatro medidas e a pergunta com
opções ficam em `matt.md`. Os itens 3 a 7 cabem integralmente na referência:
aceite e diff das edições, bloqueio conforme a mídia, nova medição depois das
arestas, instruções persistentes no argumento, avisos ao titular, ressalva do
Antigravity e entrega de `/clear` com o comando. Não cortar a opção serial,
o padrão `/implement`, o limiar de quatro tickets com pelo menos dois prontos
em algum ponto, nem os custos de revisão e cota hoje descritos nas linhas
53–64. Eles também passam a `matt.md`.

**Regra versus prova.** Podem ficar só na spec e no changelog o exemplo
`blockedSince` × `blockedOn`, a citação do resumo com o `curl` e a citação da
CLI. Permanecem em runtime a regra de fixar nomes ou acrescentar bloqueio,
o critério numérico e o aviso do Antigravity com a condição que o encerra.
As quatro medidas sobre os tickets da demanda são operações do fluxo, não
evidência histórica descartável. A dependência nativa do GitHub e o
procedimento do tracker também permanecem; retirar a prova não retira o
comando operacional. Os caminhos absolutos dos tickets locais, a verificação
serial depois do merge na integração e o cálculo da fronteira pelo código
incorporado devem sobreviver ao `/clear` no argumento, como a spec já decidiu.

**Nome, cabeçalho e fechamento.** `matt.md` é um nome suficiente dentro de
`implementar-spec/`; não há ganho concreto em criar uma pasta de referências
compartilhadas. Recomendo abrir com título e uma frase de contrato:
“Lido pelo `implementar-spec`, no passo 3, ao voltar do `/to-tickets` ou retomar
uma spec com tickets, antes de escolher a forma.” Isso delimita consumidor e
momento sem criar outra skill ou repetir o procedimento no cabeçalho.

O `fechar-demanda` não precisa ler `matt.md`: suas regras novas são as da
seção de fechamento da spec e continuam no próprio `SKILL.md`; o tratamento
da issue já fechada continua em `midia/issues.md`. Mover essas regras para a
referência de preparação criaria uma dependência desnecessária na retomada
direta do fechamento.

## Alterações necessárias na spec

- **Solução:** declarar os dois arquivos; substituir a frase “A parte do Matt
  traz também o critério da forma” pela localização em `matt.md`. No critério
  dos caminhos, trocar “pelos sinais abaixo” por uma formulação que não
  dependa de seção retirada. Indicar os destinos dos itens 1 a 7, mantendo a
  retomada anunciada no `criar-spec` e a exceção do achado 1.
- **Arquivos e interfaces:** limitar `caminhos.md` aos quatro caminhos e
  acrescentar `matt.md` com seu consumidor e gatilho. O fluxo detalhado deixa
  de constar como conteúdo do `SKILL.md`; permanecem tabela, ponteiros e
  delimitação de workspace. A linha do `criar-spec` deve usar o destino
  relativo `../implementar-spec/caminhos.md`.
- **Testes:** registrar os três links novos: dos dois consumidores para
  `caminhos.md` e do `implementar-spec` para `matt.md`. O script confere a
  existência dos destinos e o tamanho dos `SKILL.md`; não prova que a ordem
  de leitura foi obedecida nem que os contratos foram preservados.
- **Verificação:** corrigir 2 e 3 conforme o achado 2. A 1 continua sendo o
  check integral. A 4 não muda por causa desta síntese. A 5 continua em
  aberto para o uso real e deve explicitar ambas as mídias nas duas entradas,
  além das escolhas serial/paralela e do fechamento já previstos. No uso
  aicf direto, observar que não se abre `matt.md`; isso confere o benefício
  de carregamento, que um grep não mede.

O limite automatizado continua sendo 24.000 bytes por `SKILL.md`, não por
soma da pasta nem por número de linhas. Na base, `wc -lc` devolveu 112 linhas
e 8.598 bytes para `implementar-spec/SKILL.md`; há margem. Os saldos de +2
linhas e cerca de 20 linhas em `matt.md` ainda são estimativas: sem os textos
finais não há medição dessas promessas. Avaliar também bytes e conteúdo lido
em cada caminho, sem comprimir várias obrigações numa linha só para atingir
uma contagem.

## Alternativas e custo

- **Dois arquivos, como proposto:** uma leitura adicional no caminho do Matt,
  sem levar o critério da forma ao `criar-spec` ou ao aicf direto. É a opção
  recomendada; separa consumidores sem acrescentar um mecanismo novo.
- **Um arquivo só, com seções:** reduz um arquivo e um acesso no Matt, mas a
  leitura inteira carrega o procedimento da forma em todas as decisões de
  caminho. Mandar ler somente uma seção pode evitar parte disso, ao custo
  de definir e manter a seleção do trecho; o check atual não valida âncoras.
  Não é mais simples para este objetivo.
- **Cortar itens inteiros:** tirar colisões, mídia, estado local ou argumento
  elimina remédios decididos na revisão anterior; muda comportamento. Cortar
  só prova histórica e repetições é compatível e já está na proposta. Deixar
  tudo no `SKILL.md` evita uma referência, mas mantém o custo em toda invocação.

## Validação e limites

Foram lidos `AGENTS.md`, `.claude/CLAUDE.md`, a spec ajustada, os dois pareceres
citados, as skills consumidoras, as receitas de mídia, os dois precedentes e
os verificadores. A revisão é estática da proposta; não foi aplicada uma
implementação presumida à spec nem executada uma skill de implementação.
As fontes externas não foram reavaliadas: o objeto é a distribuição do texto
e a preservação das regras já decididas.

O verificador real de links foi executado sobre uma árvore mínima temporária
com os três links propostos: `3 links conferidos, 0 quebrados`, saída 0.
Ele resolve o destino a partir da pasta do arquivo de origem; atravessar para
a pasta irmã não tem restrição especial. Os links atuais para `../midia/` e
`../ajuda/SKILL.md` também dão precedente à navegação entre pastas de skills.

Os comandos atuais das Verificações 2 e 3 foram executados: o primeiro
encontra as duas skills, a contagem de ponteiros é 0, e a lista da Verificação
3 retorna 0 nos arquivos existentes e erro para `caminhos.md`, ainda ausente,
como previsto para antes da implementação. O padrão alternativo
`grep -lF 'subagente e com TDD' skills/criar-spec/SKILL.md skills/implementar-spec/SKILL.md`
encontra as duas skills na base; o resultado esperado depois é nenhuma.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, com Claude Code
`2.1.310`, 236 links conferidos e nenhum quebrado, as duas validações
aprovadas, versão `0.43.2` no topo do changelog e 7 skills abaixo do limite.
O validador também emitiu aviso de ícone ausente no plugin, sem reprovar.
O whitespace do parecer é conferido antes do commit. Nenhum teste de
comportamento foi executado; a Verificação 5 permanece para o titular no uso
real da futura implementação.

O fechamento de `aicf:fechar-demanda` limita-se a este parecer, conforme
“Agente Codex: só revisa”. A demanda permanece aberta. O commit deve conter
somente este arquivo; a aplicação das sugestões fica com o agente líder e o
titular. Não há push nesta tarefa.
