# A entrada de quem chega: o README se reorganiza por problema, e o setup se apresenta

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (só prosa em três arquivos, e toda a estrutura ficou decidida na entrevista)

## Problema

O material de entrada do aicf está escrito para quem já sabe o que é isso. **Quem chega é aluno do
curso, parceiro ou pessoa indicada** — entra pelo GitHub, lê o `README.md`, entende um pouco, e só
entende de verdade quando está rodando o `/aicf:setup`. As duas peças desse percurso falham em
lugares diferentes.

**O `README.md` gasta o começo com uma comparação.** A segunda seção ("Onde ele entra", 8 das 115
linhas e cerca de um quarto do texto corrido) é análise contra Superpowers e Matt Pocock. Ela
responde *"por que este e não aquele"* — pergunta de quem já está decidindo entre ferramentas, não
de quem está entendendo a primeira — e cita `brainstorming`, `grill-with-docs`,
`subagent-driven-development` e `to-tickets` como se fossem óbvios. O primeiro parágrafo abre com
"governança", "planejamento macro" e "agnóstico quanto ao caminho de implementação".

**Uma afirmação dessa seção está errada.** *"O Matt publica spec e tickets no issue tracker"*
aparece no `README.md` e no `README.en.md` ("publish spec and tickets to an issue tracker"), e
induz a conclusão de que ele força issues enquanto o aicf dá arquivos. O
`setup-matt-pocock-skills` oferece três destinos como escolha de setup — GitHub Issues, Linear, ou
markdown local em `.scratch/<feature>/`. A frase ficou pior desde a `0.17.0`, porque agora o aicf
também oferece as duas mídias: ela sugere uma diferença que não existe em nenhum dos dois lados.

**Comando útil aparece de passagem.** O `grilling` do Matt — que contesta a ideia antes de você
escrevê-la — é citado uma vez, dentro do passo 2 de "Começando um projeto novo", numa linha de
lista. Quem não leu aquele parágrafo não sabe que existe. Não há diagrama nenhum no arquivo.

**A tabela de skills mistura duas coisas.** Das seis, só `setup` e `criar-prd` dependem de ser
digitadas (`disable-model-invocation: true`); as outras quatro o agente alcança sozinho ao
reconhecer a intenção, e também aceitam ser digitadas — inclusive na forma `/aicf:criar-spec #12`,
que adota uma issue existente. A tabela lista as seis em pé de igualdade, e o iniciante conclui que
precisa decorar seis comandos quando precisa de dois.

**O `/aicf:setup` não se apresenta.** A skill abre em "Perguntar, em pergunta aberta: 1. Nome do
projeto". Quem roda o comando pela primeira vez começa a responder antes de saber o que está sendo
montado, para que serve, ou o que muda no jeito de trabalhar. O fim tem quatro passos, e todos
apontam para outras skills — nenhum diz como o método funciona nem por onde continuar.

## Solução

Cinco mudanças, em três arquivos. Nenhum arquivo novo.

### 1. O `README.md` se reorganiza por problema, e continua sendo um arquivo só

Não há `MANUAL.md`. O manual em runtime já existe e é o `/aicf:workflow-demanda`; um terceiro
arquivo com o mesmo conteúdo seria a cópia que envelhece. O que é para quem já usa **dobra em
`<details>`, não muda de arquivo** — é a técnica que o repositório do Matt usa para caber tudo num
README de 231 linhas sem virar muro.

O esqueleto:

```
# aicf — governança de projeto para desenvolver com agentes

  Abertura: "vinte specs não dizem onde o projeto está"

## Instalação                      ← logo no topo, ~6 linhas

## O ciclo
  [diagrama Mermaid] — as quatro fases

## O problema que isso resolve
  ### A conversa some no /clear
  ### Ninguém sabe onde o projeto está
  ### O que saiu de fato não fica escrito
  cada um terminando na skill que corrige

## Começando um projeto novo        ← 1, 2, 3, 4

## As skills
  **Você digita** — setup, criar-prd
  **Você digita, ou o agente alcança** — as outras quatro

<details> Onde as coisas ficam (a árvore, ou os labels)
<details> Comandos vizinhos que valem conhecer
<details> Por que este, e não o Superpowers ou o Matt Pocock

## Sobre
```

**O alvo é não crescer.** O arquivo tem 115 linhas hoje; o texto **visível** continua nessa ordem
de grandeza, e o que entra de novo cabe porque a comparação, a árvore de pastas e a digressão sobre
o PRD saem do caminho de leitura.

**Um diagrama só, em Mermaid**, que o GitHub renderiza nativamente e o git versiona como texto:

```mermaid
flowchart LR
  D[Demanda<br/>o que se quer, ainda cru]
  E[Entrevista<br/>produz a spec]
  I[Implementação<br/>consome a spec]
  F[Fechamento<br/>relatório do que saiu]
  D --> E --> I --> F
  F -.-> D
```

Um segundo diagrama, com os caminhos de cada fase, fica **fora**: ele é a comparação entre coleções
desenhada, ou seja, exatamente o que esta demanda tira do caminho de quem chega.

**A abertura fala do nível do produto**, porque é a falta que o método preenche: vinte specs bem
escritas não respondem "onde o projeto está". As coleções de skills de engenharia começam na ideia
já formulada e terminam no commit; o aicf é a camada de cima.

**A prosa nova é escrita em linguagem comum, e não pode soar como texto de IA.** Critério
acionável, porque "mais amigável" não se verifica: frase curta e direta; nada de antítese como
recurso de repetição ("não é X, é Y"); nada de listas de três em cadência; exemplo concreto no
lugar de substantivo abstrato — "a decisão que você tomou some no `/clear`" em vez de "volatilidade
do contexto". Vale para o texto novo; o resto do arquivo não é reescrito por estilo.

Cada um dos três problemas termina apontando a skill que o resolve, que é o padrão do README do
Matt ("The Fix is to use: ...") e o que faz a tabela de skills parar de ser uma lista a decorar.

### 2. A tabela de skills passa a ter o eixo "quem pode chamar"

As seis continuam na tabela, em dois grupos, com a frase que explica o critério — sem ela a tabela
volta a ser lista:

- **Você digita** — `/aicf:setup` e `/aicf:criar-prd`. Só existem quando você as chama; a função
  delas é conduzir uma sessão inteira.
- **Você digita, ou o agente alcança sozinho** — `workflow-demanda`, `criar-spec`,
  `implementar-spec`, `fechar-demanda`. Respondem ao pedido em linguagem natural ("me entreviste
  sobre X") e o agente as carrega ao reconhecer a intenção.

É o eixo do repositório do Matt ("User-invoked" × "Model-invoked"), e ele acomoda
`/aicf:criar-spec #12` sem precisar de eixo novo: a forma digitável não move a skill de grupo,
porque o grupo é sobre quem **pode** chamar, não sobre quem costuma chamar.

### 3. A comparação é corrigida, depois desce e dobra

**Corrigir antes de mover.** A seção vai para dentro de um `<details>`, e conteúdo dobrado é
conteúdo que ninguém reabre para revisar: frase errada que desce dobrada fica errada até alguém de
fora reclamar. São **dois erros**, um sobre cada coleção, e os dois valem nos dois idiomas.

**Erro 1 — a mídia não distingue as ferramentas.** A frase de abertura opõe *"o Superpowers grava
spec e plano em arquivo; o Matt publica spec e tickets no issue tracker"*, e daí o leitor conclui
que escolher uma coleção é escolher um lado. O `setup-matt-pocock-skills` oferece três destinos na
pergunta de setup — GitHub Issues, Linear, ou markdown local em `.scratch/<feature>/`, este último
recomendado por ele para projeto solo e repositório sem remote (linha 46) — mais um "outro" que ele
escreve sob medida (linha 112). A frase piorou na `0.17.0`: agora que o aicf também pergunta
arquivo ou issue, ela anuncia uma diferença que não existe em nenhum dos dois lados. A correção é
dizer que ele publica no tracker **que você escolheu no setup dele**.

**Erro 2 — o Superpowers não apaga o registro.** O terceiro bullet diz que ele *"apaga a pasta de
trabalho, porque a partir dali o histórico do git é o registro"*. O que o
`finishing-a-development-branch` remove é a **worktree**, e só quando foi ele quem a criou, sob
`.worktrees/`, e só em duas das quatro opções (merge local e descartar; PR e "manter como está"
preservam). Plano e design doc ficam versionados em `docs/superpowers/plans/` e
`docs/superpowers/specs/`, com o `brainstorming` mandando "save ... and commit". Conferido nas
versões 5.0.0 e 6.1.1 instaladas — não é frase que envelheceu, nasceu errada.

**O contraste do "depois" continua de pé, por outro motivo:** o que falta lá não é permanência, é
o registro escrito **depois**. `grep -rliE "diverge|what actually shipped|retrospective|final
report" skills/*/SKILL.md` no Superpowers 6.1.1 não devolve arquivo nenhum. Plano e design doc
dizem o que se pretendia e foram escritos antes de executar; nada pede que sejam revistos contra o
que saiu. É o buraco que o relatório do `/aicf:fechar-demanda` preenche, e sobrevive à conferência
de quem for verificar. Do lado do Matt vale o que já está escrito e já foi conferido: o `implement`
termina no commit e não fecha o ticket nem marca critérios de aceite.

**Não usar o contraste "o tracker dele é descartável por declaração dele"**, que o intent propunha:
a declaração não existe. `grep -rniE "throwaway|disposable|ephemeral"` sobre
`skills/engineering/{to-tickets,to-spec,setup-matt-pocock-skills}/SKILL.md` no repositório dele não
devolve nada sobre o tracker — só o `wizard` chamando a si mesmo de efêmero e o `ask-matt` chamando
o contexto da sessão de descartável. O nome da pasta sugere descarte; nenhuma skill declara.

**A regra geral que os dois erros ensinam:** afirmação sobre ferramenta de terceiro carrega o
comando que a confere, no próprio texto da spec, e quem implementar roda esse comando antes de
escrever a frase. Erra-se barato no nosso repositório e caro no texto que compara o nosso trabalho
com o dos outros.

### 4. O `<details>` dos comandos vizinhos ganha uma linha por comando

O que falta hoje no caso do `grilling` — saber que existe, e para que serve. Uma linha cada,
agrupado por fase, e só o que estiver de fato instalado no ecossistema que o README descreve:
`grill-me` e `grill-with-docs`, `brainstorming`, `domain-modeling`, `writing-plans` +
`subagent-driven-development`, `to-tickets` + `implement`, `code-review`.

### 5. O `/aicf:setup` se apresenta e se despede

**A abertura fica dentro do `SKILL.md`**, não num arquivo à parte: arquivo solto envelhece sem nada
que o cutuque, e a rede que existia contra isso saiu do método em
[o `CHECKLIST.md` sai do método](o-checklist-sai-do-metodo.md). O custo é de três a
cinco linhas num arquivo de 205.

Antes da primeira pergunta, três coisas e nada mais: o que vai ser montado, quantas perguntas vêm,
e que nada é criado antes de confirmar. A Restrição vale aqui — abrir o setup com três parágrafos
sobre governança seria o mesmo defeito em lugar novo.

**A despedida explica o método em linguagem comum e mostra como começar.** Não um ponteiro seco
para `/aicf:workflow-demanda`, e sim o agente apresentando o ciclo com exemplo antes de dizer onde
reler. Para isso não virar uma segunda cópia do `workflow-demanda`, **o `SKILL.md` do setup guarda
o roteiro, não o texto**: uma lista curta do que a despedida precisa cobrir, e a instrução de
carregar o `/aicf:workflow-demanda` e apresentá-lo em linguagem comum. O texto se compõe na hora, a
partir da skill que já é a fonte da verdade do ciclo — um mecanismo, não dois.

O roteiro cobre: o que foi criado e onde; o ciclo das quatro fases numa frase cada; **um exemplo
concreto de primeira demanda**, do pedido ao arquivo (ou à issue) fechado; `/aicf:criar-prd` como
próximo passo; e `/aicf:workflow-demanda` como o lugar de reler. O `/context` na próxima sessão
continua onde está.

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `README.md` | Reorganizado por problema; diagrama Mermaid do ciclo; tabela de skills no eixo "quem pode chamar"; três `<details>`; a frase sobre o Matt corrigida |
| `README.en.md` | **Tradução idêntica**, seção por seção, incluindo o diagrama e os `<details>` |
| `skills/setup/SKILL.md` | Abertura de 3 a 5 linhas antes de "Antes de criar"; "Ao terminar" reescrito como roteiro de despedida |

O `/aicf:workflow-demanda` **não muda** — é ele que a despedida do setup passa a apresentar, e
qualquer coisa que se quisesse acrescentar ali é escopo de outra demanda.

**Ao mexer em "Ao terminar", conferir quem cita passo por número**: `grep -rn 'passo [0-9]'
--include='*.md' .` antes de fechar. Renumerar passo quebra em silêncio quem cita o número de fora,
e nenhum grep pelo assunto pega essas referências.

## Fora de escopo

- **`MANUAL.md` ou `TUTORIAL.md`.** O manual em runtime é o `/aicf:workflow-demanda`, e o percurso
  guiado é o próprio `/aicf:setup`. Um terceiro arquivo repetiria os dois e envelheceria sozinho.
- **Um segundo diagrama, com os caminhos de cada fase.** É a comparação entre coleções em forma de
  desenho, e vai para dentro do `<details>` da comparação se um dia fizer falta.
- **Reescrever o `README.md` inteiro por estilo.** O critério de linguagem comum vale para o texto
  novo e para o que for movido de lugar, não para o arquivo todo.
- **Mexer no `/aicf:workflow-demanda`.** Ele é a fonte que a despedida apresenta; mudá-lo na mesma
  demanda embaralharia as duas coisas.
- **Site de documentação, como o spec-kit tem.** Ele separou por volume — dezenas de páginas,
  vários agentes, extensões. São seis skills aqui, e o README dá conta.
- **Encolher ou congelar o `README.en.md`.** Decidido na entrevista: ele acompanha inteiro, e o
  custo de manter dois arquivos em dia é aceito.

## Verificação

Um passo ponta a ponta, na ordem:

1. **A comparação saiu do caminho e as duas frases erradas morreram:**
   `grep -n "publica spec e tickets no issue tracker" README.md`,
   `grep -n "publish spec and tickets to an issue tracker" README.en.md`,
   `grep -n "apaga a pasta de trabalho" README.md` e
   `grep -niE "deletes? the (working|work) (folder|directory)" README.en.md` não devolvem nada; a
   comparação aparece depois da tabela de skills, dentro de um `<details>`.
2. **O README não cresceu.** Linhas fora dos blocos dobrados:
   `awk '/^<details/{d=1} /^<\/details>/{d=0;next} !d' README.md | wc -l` fica na ordem das 115
   linhas de hoje (`git show HEAD:README.md | wc -l` dá a base de comparação).
3. **O diagrama renderiza.** Abrir o `README.md` na página do repositório no GitHub e ver o
   fluxograma das quatro fases desenhado — Mermaid quebrado no GitHub aparece como bloco de código
   cru, não como erro.
4. **O percurso de quem chega, do começo ao fim.** Numa pasta vazia, com o plugin instalado: ler o
   `README.md` renderizado, rodar `/aicf:setup`, e conferir que (a) antes da primeira pergunta veio
   a apresentação de três a cinco linhas, (b) ao terminar o agente explicou o ciclo em linguagem
   comum, deu um exemplo de primeira demanda e apontou `/aicf:criar-prd` e
   `/aicf:workflow-demanda`, e (c) nada foi criado antes da confirmação.
5. **Os dois idiomas dizem a mesma coisa.** `grep -c '^## ' README.md README.en.md` devolve o mesmo
   número nos dois, e as seções estão na mesma ordem.
6. **Nenhum ponteiro por número quebrou:** `grep -rn 'passo [0-9]' --include='*.md' .` — cada
   ocorrência confere com a numeração atual do arquivo citado.

## Relatório de implementação (2026-09-18)

- **Status** — concluído. Os seis passos da Verificação rodaram; dois deles só se **confirmam**
  depois do release, e a condição que encerra cada um está em "Validação".

- **Arquivos alterados**
  - `README.md` — reorganizado por problema do leitor: abertura pelo nível do produto, diagrama
    Mermaid do ciclo, três problemas terminando cada um na skill que o resolve, tabela de skills no
    eixo "quem pode chamar", e quatro `<details>` com o que é para quem já usa.
  - `README.en.md` — traduzido inteiro, seção por seção.
  - `skills/setup/SKILL.md` — nova seção `## A apresentação` antes de `## Antes de criar`, e
    `## Ao terminar` reescrito como despedida que apresenta o método (4 passos → 5).
  - `.claude-plugin/plugin.json` — versão `0.17.0` → `0.18.0`.
  - `docs/adr/0005-a-documentacao-humana-e-um-arquivo-so.md` — a decisão de não ter `MANUAL.md`.
  - `CLAUDE.md` — a regra promovida no passo 3 (ver abaixo).

- **Commits**
  - `698ddab` — `docs(governanca): entrevista de "a entrada de quem chega"`
  - `ae7fb15` — `feat(entrada): o README se reorganiza por problema, e o setup se apresenta`

- **Validação**
  - **Checks do projeto: não existem.** A seção `## Verificação` do `CLAUDE.md` segue com "a
    preencher quando houver código", e não há lint, testes ou typecheck a rodar. Encerra quando
    houver comando naquela seção.
  - **Revisão de código: não pedida.** A mudança é texto de ponta a ponta, que é o caso que o
    ritual dispensa. A conferência que importava aqui foi de **fato**, contra os repositórios
    citados, e está registrada abaixo.
  - Verificação 1 (frases erradas) — os quatro greps devolvem vazio, e as duas correções aparecem
    nos dois idiomas.
  - Verificação 2 (tamanho) — 105 linhas visíveis
    (`awk '/^<details/{d=1} /^<\/details>/{d=0;next} !d' README.md | wc -l`), contra 115 antes
    (`git show 698ddab:README.md | wc -l`).
  - Verificação 3 (o diagrama renderiza) — **pendente.** Encerra ao abrir a página do repositório
    no GitHub e ver o fluxograma das quatro fases desenhado; Mermaid quebrado aparece como bloco
    de código cru.
  - Verificação 4 (percurso de quem chega) — **parcial.** Conferido no conteúdo: a apresentação
    está antes da primeira pergunta e a despedida no fim (`grep -n '^## ' skills/setup/SKILL.md`).
    O comportamento encerra ao rodar `/aicf:setup` numa pasta vazia, em sessão nova, com a `0.18.0`
    instalada — a sessão que implementou roda a skill da cópia em cache, que ainda é a `0.17.0`.
  - Verificação 5 (os dois idiomas) — `grep -c '^## '` devolve 6 nos dois, na mesma ordem.
  - Verificação 6 (ponteiros por número) — `## Ao terminar` foi de 4 para 5 passos, e
    `grep -rn 'passo [0-9]' --include='*.md' .` não acha nenhuma citação a passo do `setup`.

- **Escopo efetivo** — um `<details>` além dos três do esqueleto: *"Por que o PRD não passa pelo
  ciclo da demanda"*, dobrado dentro do passo 2 em vez de apagado. A spec mandava tirar a digressão
  do caminho de leitura, e dobrar no lugar faz isso sem perder o argumento. Fora isso, a entrega
  bate com a spec.

- **Saída do ritual**
  - [`docs/adr/0005-a-documentacao-humana-e-um-arquivo-so.md`](../../../adr/0005-a-documentacao-humana-e-um-arquivo-so.md)
    — por que não há `MANUAL.md`, com o que fica de fora por decisão e o que reverter custaria.
  - `CLAUDE.md`, seção `## Registro` — **afirmação sobre ferramenta de terceiro carrega o comando
    que a confere, no texto que a propõe.** Entra pelo gatilho do erro que apareceu duas vezes, e
    as duas vezes foram nesta demanda.
  - Nenhuma skill nova, nenhuma regra em `.claude/rules/`, nenhum termo novo em glossário.
  - Nenhuma demanda nova, e nenhuma tornada obsoleta. O `ROADMAP.md` não muda.

- **Lições**
  - **Conteúdo dobrado é conteúdo que ninguém revisa.** As duas frases erradas iam descer para
    dentro de um `<details>` junto com a seção; se tivessem descido antes da conferência, ficariam
    erradas até alguém de fora reclamar. Corrigir antes de dobrar virou passo explícito da spec, e
    a regra geral foi promovida ao `CLAUDE.md`.
  - **O substituto proposto pelo intent também não passou.** Ele sugeria contrastar com *"o tracker
    dele é descartável por declaração dele"*; a declaração não existe
    (`grep -rniE "throwaway|disposable|ephemeral"` nas skills dele não devolve nada sobre o
    tracker). Frase de posicionamento herdada de um intent tem o mesmo direito à conferência que
    uma frase nova.
  - **Perguntar "o manual não existe já?" mudou a demanda.** O intent pedia um `MANUAL.md`; a
    entrevista achou que ele já existia em runtime (`/aicf:workflow-demanda`) e o arquivo deixou
    de ser escrito. O que o intent chamava de falta de manual era falta de **renderização** e de
    **comparação**, e as duas cabiam no `README.md`.
