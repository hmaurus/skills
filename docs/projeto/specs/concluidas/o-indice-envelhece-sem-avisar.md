# O índice envelhece sem avisar, e pedir atenção não conserta

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

Num projeto privado que consome estas skills, o `CHECKLIST.md` ficou desatualizado em três
lugares diferentes, e o agente **não percebeu nenhum deles sozinho** — nem rodando o ritual de
fechamento, nem quando o titular perguntou "tem certeza que o checklist tá atualizado?", nem na
terceira vez, quando a pergunta já apontava para a seção certa.

| # | O que estava errado | Achado quando |
| --- | --- | --- |
| 1 | ADR 0004 e 0005 ausentes da seção que listava todos os ADRs | o titular perguntou "tá atualizado?" |
| 2 | Item entregue **apagado** do backlog em vez de movido para Entregue | o agente reviu por conta, depois de cobrado |
| 3 | Item de backlog descrevendo como pendente uma decisão **já tomada e aplicada** | o titular perguntou "e o backlog?" |

### Por que o ritual não pegou

O passo 5 do `/aicf:fechar-demanda` manda "conferir se **a execução** criou item novo no checklist
ou tornou algum obsoleto". O agente leu "a execução" como a **implementação** — o código recém
escrito — e não conferiu a saída do **passo 4, que tinha acabado de rodar** e criado um ADR novo.
O passo 5 audita o que veio antes do ritual e é cego para o que o próprio ritual produziu, embora
o passo 4 exista justamente para produzir ADR, regra e doc de referência — exatamente as coisas
que um índice precisa listar. Os passos 4 e 5 não se falam.

### Por que conferir de novo também não pegou

Nas duas vezes em que o titular mandou conferir, o agente conferiu de verdade e errou assim mesmo:
*"está atualizado?"* devolve ao conferente a escolha do que conferir, e ele inventou uma lista de
suspeitas nova a cada passada — três recortes, três lacunas diferentes. **A instrução precisa
dizer o que enumerar, não pedir um julgamento sobre estar em dia.**

### As duas classes de deriva

**Classe A — índice × diretório.** Diferença de conjunto: mecânica, barata, sem julgamento. É a
falta #1, e nunca deveria depender de alguém reparar.

**Classe B — afirmação × mundo.** "919 linhas", "nenhuma marcada", "bloqueado por fora" são
verdades congeladas em prosa. Nada liga o texto ao que o sustenta: quando o mundo muda, a frase
continua bem escrita e passa a mentir. É a falta #3, e reler não remede.

A falta #2 é de terceira natureza: o próprio checklist diz *"não apagar item entregue"*, uma linha
acima de onde o agente apagou.

### O que a entrevista descobriu, além do diagnóstico

**1. No aicf padrão, o par que falhou no caso original nem existe.** O template de checklist do
`/aicf:setup` não tem seção que liste ADRs — aquele projeto criou a seção por conta. Instrumentar
um par ausente seria consertar um defeito que só um projeto tinha.

**2. Este repositório tem a mesma deriva numa terceira forma: par que nunca foi declarado.** Há
arquivos em `docs/projeto/intents/` e nenhuma seção do `CHECKLIST.md` os menciona — `Em andamento`
espelha `specs/` e intent não-entrevistada não é "demanda ativa" pela definição escrita. Não é item
esquecido: nada no índice aponta para `intents/`, e as demandas decididas são invisíveis para quem
abre o checklist. Uma instrução que mande enumerar não tem o que enumerar se o par não existe.

**3. A regra da classe B, como a intent a formulava, não pegaria a falta #3.** A formulação era
"número que entra em doc de governança vem com o comando que o reproduz" — mas na falta #3 *a
medição ainda batia*. O que apodreceu foi o veredito: o item dizia "decisão pendente, e esta regra
a corrigiria", com a regra já em vigor havia commits. Remedir devolveria o mesmo número e a frase
passaria. O objeto da regra precisa ser a afirmação, não o número.

## Solução

Três mudanças, duas para a classe A e uma para a classe B. Nenhuma pede mais atenção do agente:
todas trocam julgamento por enumeração ou execução.

### 1. O passo 5 do `fechar-demanda` passa a nomear o que enumerar

Lista fechada dentro da skill, e não declaração mantida por projeto: cobre 100% do que é padrão
sem o projeto configurar nada, e não cria um segundo índice — a declaração — para envelhecer junto.

O passo confere **pares de conjunto**, um a um:

| Seção do `CHECKLIST.md` | Espelha |
| --- | --- |
| Decidido | `intents/` |
| Em andamento | `specs/` |
| Entregue | `specs/concluidas/` |

E confere **a saída dos passos 1 a 4 deste mesmo ritual** — o ADR, a regra, a skill ou o doc de
referência que o passo 4 acabou de criar aparecem como link no item de `Entregue` desta demanda.
É a correção direta da causa raiz: o passo 5 deixa de ser cego para o passo anterior.

A auditoria antiga — a execução criou item novo ou tornou algum obsoleto — continua, como item
separado e nomeado, em vez de ser a única coisa que o passo pedia.

Consequências desenhadas de propósito:

- **A falta #1 fica coberta sem índice de ADR.** Como o ADR aparece como link no item de
  `Entregue` da demanda que o gerou, não há segunda lista a sincronizar; a conferência acontece no
  arquivo que o ritual já está editando.
- **A falta #2 cai no par `Entregue` × `specs/concluidas/`.** Arquivo na pasta sem linha na seção
  aparece na diferença de conjunto, sem depender de ninguém lembrar a regra de não apagar.

### 2. O `CHECKLIST.md` ganha a seção `Decidido`

Espelha `intents/`, e fica antes de `Em andamento`. Mantém a distinção que o workflow já faz entre
os dois estados do arquivo — decidida e ainda não entrevistada × pronta para implementar — e dá ao
passo 5 dois pares limpos em vez de um par e um buraco. O item sai da seção quando o arquivo migra
para `specs/`.

`intents/backlog/` continua sem espelho: a seção `Backlog` segue aceitando linha solta, e criar um
terceiro par para o que ainda não é certeza custa mais do que rende.

### 3. Afirmação verificável carrega o teste que a refuta

Regra de escrita, não instrução de conferência. Duas formas, conforme o que a frase afirma:

- **Número** vem com o comando que o remede: `54 linhas` (`wc -l < CLAUDE.md`, 2026-09-09).
- **Afirmação de estado** — item de backlog, "bloqueado por", "ainda não existe" — vem com a
  condição que a encerra: `— encerra quando houver workflow em .github/workflows/`.

Conferir passa a ser executar, não julgar; e a frase deixa de depender de alguém reparar que
envelheceu, porque ela mesma diz o que provaria que envelheceu.

A regra entra em dois lugares, para valer no momento em que o texto nasce e não só quando o ritual
passa por ele depois:

- **`fechar-demanda`** — no passo 4, que escreve nos docs de governança, e no bloco `## O
  relatório`, que é onde `919 linhas` e `bloqueado por fora` nasceram no episódio.
- **`criar-spec`** — na seção `## A spec`, pelo mesmo motivo.

## Arquivos e interfaces

| Arquivo | Mudança |
| --- | --- |
| `skills/fechar-demanda/SKILL.md` | passo 5 reescrito com a lista fechada e a saída dos passos 1–4; regra da classe B no passo 4 e em `## O relatório` |
| `skills/criar-spec/SKILL.md` | regra da classe B em `## A spec` |
| `skills/setup/templates/checklist.md` | seção `Decidido` antes de `Em andamento`, com a nota de uma linha do que ela espelha |
| `docs/projeto/CHECKLIST.md` | mesma seção, e as intents deste repositório listadas nela |
| `CHANGELOG.md` + `.claude-plugin/plugin.json` | entrada e bump de versão |

O passo 5 nomeia os caminhos do layout padrão (`docs/projeto/`). Projeto que gravou a governança
noutro lugar troca os caminhos, não os pares — uma frase na skill diz isso, para o texto não virar
mentira em projeto fora do padrão.

## Fora de escopo

- **Skill de auditoria do registro** (direção 3 da intent) — enumera afirmações verificáveis e
  roda a checagem de cada uma. Fica redundante com as direções 1 e 2 juntas, e é o mecanismo mais
  pesado das quatro.
- **Hook para a classe A** (direção 4) — hook mora no projeto que consome o plugin, então o aicf
  teria que gerar e manter um script no setup. A lista fechada cobre a classe A sem código.
- **Seção de ADRs no checklist** — decidido não criar índice separado: o link no item de `Entregue`
  já dá o par, e um índice a menos é um índice a menos para derivar.
- **Espelho para `intents/backlog/`** — motivo na seção 2 acima.
- **A regra da classe B no template de `CLAUDE.md` e no `CLAUDE.md` deste repositório** — daria a
  maior cobertura, e custa linhas no arquivo que é lido inteiro em toda sessão e tem alvo abaixo de
  200. Fica para quando houver evidência de que a regra escapa pelos lugares onde ela não está.

## Verificação

Ponta a ponta, no fechamento desta própria demanda — que é o primeiro a rodar o passo 5 reescrito:

1. Rodar `/aicf:fechar-demanda` nesta spec.
2. Para cada par, comparar seção e diretório e confirmar que batem exatamente:
   - `ls docs/projeto/intents/*.md` × as linhas de `Decidido`
   - `ls docs/projeto/specs/*.md` × as linhas de `Em andamento`
   - `ls docs/projeto/specs/concluidas/*.md` × as linhas de `Entregue`
3. Confirmar que o passo 5 apontou a saída do passo 4 desta demanda — se o fechamento gerar ADR,
   regra ou doc de referência, o link aparece no item de `Entregue`; se não gerar nenhum, o passo
   registra isso em vez de passar em silêncio.
4. Conferir que a linha desta demanda saiu de `Decidido` e entrou em `Entregue`, e que as demais
   intents seguem listadas.

O teste real da classe B é esta spec: se ela carrega número ou afirmação de estado sem o teste que
a refuta, a regra não pegou nem no documento que a cria.

## Relatório de implementação (2026-09-09)

**Status** — concluído. Não há CI neste repositório; a validação é o script de conferência dos
pares, transcrito abaixo, e uma revisão de código por subagente.

**Causa raiz** — o passo 5 do ritual pedia um julgamento (*"a execução criou item novo?"*) em vez
de nomear o que enumerar, e a palavra "a execução" foi lida como a implementação, nunca como o
passo 4, que roda segundos antes e existe justamente para criar ADR, regra e doc de referência.
Somaram-se dois defeitos que o diagnóstico da intent não previa: `intents/` não era espelhado por
seção nenhuma — o par não existia para ser conferido — e a regra proposta para a classe B mirava o
número, quando na falta mais grave o número estava certo e quem mentiu foi o veredito.

**Arquivos alterados** — 18 no total entre os commits `4eb4002` (código) e o de fechamento;
recontar com `git show --name-only --format= <sha> | sort -u | grep -c .`:

| Arquivo | O quê |
| --- | --- |
| `skills/fechar-demanda/SKILL.md` | passo 5 reescrito (três pares, conferência por inclusão, saída dos passos 1–4); regra da classe B no passo 4 e no relatório; passo 2 ganha o `grep` dos links; passo 3 cobre demanda que nasce no fechamento |
| `skills/criar-spec/SKILL.md` | a linha do checklist acompanha o `git mv`; regra da classe B por referência |
| `skills/workflow-demanda/SKILL.md` | o checklist descrito como índice; agrupamento vira subtítulo dentro de `Em andamento`, não seção nova |
| `skills/criar-prd/SKILL.md` | diz em que seção entra a linha que nunca vira arquivo |
| `skills/setup/templates/checklist.md` | seção `Decidido`; cabeçalho e notas de seção declarando os pares; regra da classe B na nota do `Backlog` |
| `skills/setup/templates/readme.md` | descrição do checklist |
| `docs/projeto/CHECKLIST.md` | mesma estrutura, e as demandas deste repositório listadas |
| `README.md`, `README.en.md` | descrição do checklist na árvore e no passo 3 |
| `CLAUDE.md` | a regra da classe B, promovida no passo 4 do ritual |
| `docs/adr/0002-conferencia-do-indice-por-inclusao.md` | novo |
| `CHANGELOG.md`, `.claude-plugin/plugin.json` | entrada e bump para `0.14.0` |
| 3 arquivos em `intents/` | links relativos quebrados pelo `git mv`, e uma afirmação que esta demanda tornou falsa |

**Commits** — `e38a68c` (spec), `4eb4002` (implementação, com `--amend` duas vezes: a primeira
incorporou as correções da revisão, a segunda corrigiu o número de arquivos na própria mensagem),
e o commit de fechamento.

**Validação** — o script de conferência dos três pares, que é o passo de verificação da spec:

```
OK  Decidido       3 arquivo(s) -> 3 linha(s)
OK  Em andamento   1 arquivo(s) -> 1 linha(s)
OK  Entregue       2 arquivo(s) -> 2 linha(s)
links quebrados: 0
```

Revisão de código por subagente fresco que não viu a implementação — 12 achados, todos aplicados.
Não há script de lint, format ou typecheck neste repositório (sem `package.json`, `Makefile` ou
`pyproject.toml`); o passo fica registrado como não aplicável em vez de sumir.

**Escopo efetivo** — maior que o previsto, em três frentes:

1. **Onze arquivos com descrição do checklist, contra os seis que a tabela da spec previa.** Um subagente mapeou toda descrição do checklist
   no repositório e achou cinco que a spec não previa — `workflow-demanda`, os dois READMEs,
   `templates/readme.md` e `criar-prd`. Deixá-los seria o defeito da demanda se reproduzindo na
   própria correção.
2. **Os links relativos quebrados pelo `git mv`.** Achado da implementação: mover o intent para
   `specs/` quebrou cinco links de uma vez em outras demandas, e o passo 2 do ritual reproduzia
   isso em todo fechamento. Virou instrução no passo 2.
3. **A regra da classe B no `CLAUDE.md`**, que a spec pôs explicitamente fora de escopo. Revertido
   com base em evidência posterior à decisão: errei o número de arquivos duas vezes na mesma
   mensagem de commit. É o gatilho "erro que apareceu duas vezes" do passo 4. O template do
   `CLAUDE.md` continua fora — a evidência é sobre este repositório.

**Lições**

- **A primeira redação do passo 5 podia causar a falta que ele existe para impedir.** "Arquivo sem
  linha, ou linha sem arquivo, é a diferença a corrigir" dá uma instrução só para dois casos com
  correções opostas; linha órfã em `Entregue` levaria a apagar o item entregue. Só a revisão pegou.
  Corrigir uma instrução ambígua com outra instrução ambígua é o modo de falha desta classe de
  demanda, e ele não aparece relendo o próprio texto.
- **A verificação da spec não pôde ser executada como escrita.** Ela mandava rodar
  `/aicf:fechar-demanda` para provar o passo 5 novo, mas o Claude Code carrega a skill da cópia
  instalada do plugin — `0.13.5`, com o passo antigo. O conteúdo da regra foi provado por script; o
  que só a reinstalação prova é que a instrução nova chega ao agente. Spec deste repositório que
  verifica comportamento de skill precisa contar com essa defasagem.
- **Escrever a regra não basta para segui-la.** O commit que institui "afirmação carrega o teste
  que a refuta" trouxe dois números errados em prosa, e a spec trouxe um exemplo cujo comando
  devolvia outro valor. Número anotado com o comando ao lado só ajuda quem roda o comando.
