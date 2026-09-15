# O usuário escolhe se a governança mora em arquivos ou em issues

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-plan (toca cinco skills, dois templates e o README, e cria um doc de referência novo — plano na mesa antes de editar)

## Problema

O aicf hoje assume **arquivo**. Toda skill grava e lê em `docs/projeto/`: `criar-spec` escreve em
`specs/<nome>.md`, `implementar-spec` lê de lá, `fechar-demanda` move para `specs/concluidas/`.
Não há escolha — quem prefere issue tracker precisa customizar por fora, e a customização não é
suportada nem descrita.

Isso destoa do resto do próprio método. O `workflow-demanda` já oferece **três caminhos de
entrevista e quatro de implementação**, e diz que "a implementação é roteiro, não trilho". A mídia
do registro é a única coisa que continua trilho único.

### E o vizinho já resolveu isto

O conjunto do Matt Pocock **já trata a mídia como configuração**. O `/setup-matt-pocock-skills`
pergunta onde as issues deste repositório vivem e grava a resposta em `docs/agents/issue-tracker.md`
— GitHub, GitLab, markdown local em `.scratch/<feature>/`, ou qualquer outro tracker descrito em
prosa —, e `to-spec`, `to-tickets`, `triage` e `wayfinder` leem esse arquivo em runtime. Nenhum
`SKILL.md` dele nomeia um tracker. O aicf faz o contrário: a mídia está escrita dentro de cada
skill.

O precedente, então, não é "o vizinho usa issues e nós usamos arquivo" — ele oferece as duas, e a de
arquivo é declarada opção de primeira classe, não fallback. O precedente é que **a mídia cabe numa
resposta de setup lida em runtime**, e alguém já provou isso em produção. É de lá que sai o desenho
desta demanda.

A consequência prática de o aicf não ter essa resposta aparece em repositório que roda as duas
coleções: a config do Matt pode dizer GitHub enquanto o aicf, sem ter o que dizer, grava em arquivo
— a spec sai numa mídia e o registro noutra. Esta demanda torna o acordo **possível**; não o torna
automático, porque as duas configs seguem independentes (ver Fora de escopo).

### Por que a escolha existe, e por que o default é arquivo

Cada mídia ganha e perde coisas diferentes:

| | Arquivo `.md` | Issue |
| --- | --- | --- |
| Setup para começar | nenhum | `gh` instalado, autenticado, remote GitHub |
| Sobrevive ao `git clone` sem rede | sim | não |
| Custo de o agente ler | `cat` | chamada de rede por listagem |
| Contribuição de quem não é mantenedor | fork + PR | dois cliques |
| Conversa sobre a demanda | exige commit, ou morre no PR | comentário, menção, notificação |
| Referência a outra demanda | link relativo, quebra ao mover | `#12`, estável |
| Fechar como efeito do merge | não | `Fixes #12` |
| Busca e `grep` no repositório | direto | não |
| Relatório achável anos depois | arquivo versionado | comentário em issue fechada |
| Depende de fornecedor | não | GitHub |

**O argumento de detecção não está na tabela, e isso é decisão tomada.** Enquanto o `CHECKLIST.md`
existia, o lado do arquivo guardava o estado duas vezes — a pasta e a linha na seção — e dava para
dizer que a divergência tornava o erro achável. [O `CHECKLIST.md` sai do
método](concluidas/o-checklist-sai-do-metodo.md) mostrou que o argumento estava invertido: cópia
mantida à mão não detecta erro na fonte, ela fabrica uma classe de erro nova. Hoje as duas mídias
guardam o estado uma vez só — a pasta de um lado, o label do outro — e **nenhuma das duas detecta
estado errado**. O `triage` do Matt confirma pelo lado das issues: ele acha issue sem label e issue
com dois labels em conflito, e não acha label errado.

O default é **arquivo** por duas razões, e a segunda é a mais forte: é o modo que um usuário novo
entende sem explicação, e é o único que funciona com zero setup — repositório local, sem remote, sem
`gh`, sem login, sem fornecedor.

## Solução

A mídia do registro vira **uma escolha do projeto**, perguntada no `/aicf:setup` e lida em runtime
por toda skill. A governança não muda: as quatro fases, o ritual de fechamento e a linha `Processo`
seguem idênticas. O que troca é o substrato.

### A configuração: uma linha no `CLAUDE.md`

Na seção "Processos de desenvolvimento", ao lado da linha "Coleções de skills de workflow
instaladas" que o `implementar-spec` já lê:

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

Nenhum mecanismo novo: o `CLAUDE.md` já carrega inteiro em toda sessão, já é o lugar onde o método
guarda configuração de projeto, e o usuário troca a mídia editando uma linha.

**Linha ausente significa arquivo.** Não é sinalização por ausência de propósito — é
compatibilidade com todo projeto criado antes desta demanda. O `/aicf:setup` **sempre grava a
linha**, nos dois modos, para que em projeto novo a escolha seja explícita.

### Quando o vizinho já respondeu a mesma pergunta

O `/setup-matt-pocock-skills` grava em `docs/agents/issue-tracker.md` a resposta para **onde o
trabalho mora** — a mesma pergunta que a linha de mídia responde. Num repositório com as duas
coleções, as duas respostas existem e podem discordar.

O aicf **não delega e não depende**: a linha do `CLAUDE.md` segue a única fonte da verdade dele, e o
modo issue funciona em repositório que nunca ouviu falar do Matt. Mas quando aquele arquivo existe:

- **No setup**, o aicf o lê e propõe o default a partir dele — "o tracker do Matt aponta para
  GitHub; usar issues aqui também?" — em vez de perguntar do zero o que já foi respondido ao lado.
- **Nas skills**, ao operar sobre a demanda, se as duas discordarem o agente **avisa uma vez** e
  segue pela linha do `CLAUDE.md`. Divergência é legítima — dá para querer o tracker dele em GitHub
  e o registro do aicf em arquivo —, mas precisa ser escolha, não descoberta tardia.

É o padrão que o método já usa duas vezes: o passo 3 do fechamento delega ADR e glossário ao
`/domain-modeling` e funciona sem ele; o `implementar-spec` oferece os caminhos das coleções
instaladas e só o aicf quando não há nenhuma. Usa o vizinho quando ele está lá, funciona sozinho
quando não.

O que **não** se unifica são os vocabulários de estado. Os três labels `aicf:*` classificam
maturidade do documento; os cinco do `/triage` classificam o que fazer em seguida. Eixos diferentes,
e a mesma issue pode carregar os dois — o prefixo existe para que não colidam. Nenhum dos dois lados
enxerga os labels do outro, e isso fica assim.

### Os quatro estados

No modo issue, duas distinções de hoje deixam de existir. "Próximas" é o que já foi decidido e ainda
não tem arquivo; `intents/` é o que já foi decidido e tem arquivo — a diferença entre as duas é o
custo de criar arquivo, que a issue não tem. O mesmo para "Backlog" e `intents/backlog/`. As seis
gavetas de hoje colapsam em quatro estados:

| Estado | Modo arquivo | Modo issue |
| --- | --- | --- |
| Incerto — nem se sabe se será feito | `intents/backlog/<nome>.md`, ou linha em `ROADMAP.md` → Backlog | issue aberta, `aicf:backlog` |
| Decidido, ainda não entrevistado | `intents/<nome>.md`, ou linha em `ROADMAP.md` → Próximas | issue aberta, `aicf:intent` |
| Pronta para implementar | `specs/<nome>.md` | issue aberta, `aicf:spec` |
| Concluída | `specs/concluidas/<nome>.md`, com o relatório no fim | issue fechada, com o relatório em comentário |

**Uma demanda é uma issue só, do nascimento ao fechamento.** O label troca, o número não. Os três
labels são exclusivos entre si: mudar de estado é
`gh issue edit <n> --remove-label aicf:intent --add-label aicf:spec`. "Concluída" não tem label — é
a issue fechada.

**No modo issue não existe `ROADMAP.md`**, e não existe substituto para ele: ele só fazia sentido
onde criar arquivo custa mais que ter a ideia. O critério **certeza, não urgência** que ele
explicava passa a viver na descrição do label `aicf:backlog`.

### O índice do que existe

| | Como se lê |
| --- | --- |
| Arquivo | `head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md \| sed 's/^# //'` |
| Issue | `gh issue list --state open --label aicf:spec` (um estado por vez) |

**Cuidado com `--label` repetido:** na API do GitHub, dois `--label` filtram por issue que tem
**todos** eles, não qualquer um — `gh issue list --label aicf:intent --label aicf:spec` devolve
vazio, porque os labels são exclusivos. Para ver os três estados de uma vez, a sintaxe é a de busca:
`gh issue list --search "label:aicf:backlog,aicf:intent,aicf:spec"`. A implementação **confere isso
antes de escrever o comando no doc** — os dois comandos, num repositório com uma issue de cada
label, e o resultado é o que decide.

### O que não muda com a mídia

PRD, ADR, `CONTEXT.md` e `docs/referencias/` ficam em **arquivo nos dois modos**. Nenhum deles é
demanda: o PRD é documento vivo, revisado toda vez que uma decisão o contraria, e ADR é imutável por
definição. No modo issue, `docs/projeto/` continua existindo com o `PRD.md` dentro, e só ele.

O `/aicf:criar-prd` não é tocado por esta demanda.

### Onde mora a receita de cada mídia

As skills ficam **neutras de mídia** — "gravar a demanda", "arquivar a demanda" — e um doc de
referência novo traz as duas receitas lado a lado, operação por operação. Um lugar para manter, e
terceira mídia no futuro acrescenta coluna em vez de espalhar condicional por quatro arquivos.

O doc vive em `skills/workflow-demanda/references/midia.md`, porque o `workflow-demanda` é o mapa —
é ele que já descreve onde mora o quê. Cada skill que opera sobre a demanda diz, no ponto onde
difere, para ler a linha do `CLAUDE.md` e seguir a coluna correspondente do doc.

### O `/aicf:setup`

Ganha a pergunta da mídia, **antes** de criar qualquer coisa — é ela que decide o que criar.
`AskUserQuestion`, default arquivo, com a explicação curta de por que cada uma.

**Só oferece issues se o repositório aguentar:** o setup confere `gh auth status` e se o remote é
GitHub antes de perguntar. Não aguentando, oferece só arquivo e diz em uma linha o que falta para a
outra opção existir — em vez de deixar o usuário escolher um caminho que falha no primeiro comando.

O que o setup cria em cada modo:

| | Modo arquivo | Modo issue |
| --- | --- | --- |
| `CLAUDE.md`, `AGENTS.md`, `README.md` | sim | sim |
| Linha `**Mídia do registro:**` | sim | sim |
| `docs/projeto/PRD.md` | sim | sim |
| `docs/projeto/ROADMAP.md` | sim | não |
| `intents/`, `intents/backlog/`, `specs/concluidas/` | sim | não |
| Os três labels, via `gh label create` | não | sim |

**O setup cria os labels.** É a reclamação mais repetida sobre o setup do Matt, que só grava o
mapeamento: em repositório novo o label não existe, e `gh issue create --label` falha em vez de
criar. Criação idempotente — label que já existe vira aviso, não erro.

### Adotar uma issue que já existe

No modo issue, `/aicf:criar-spec #12` e `/aicf:fechar-demanda #12` aceitam um número de issue como
alvo: em vez de criar issue nova, a skill reescreve o corpo daquela e ajusta o label. Issue que
nunca teve label `aicf:*` ganha um agora — é assim que uma issue **de fora da governança** entra
nela.

Isso existe por dois motivos concretos:

- **O `to-spec` do Matt cria issue nova, não edita uma existente.** Quem entrevista pelo Matt com os
  dois apontando para o GitHub terminaria com duas issues para a mesma demanda. Com adoção, o
  caminho é: `to-spec` publica, `/aicf:criar-spec #<n>` adota — uma issue só, com o label do aicf.
- **Contribuição de fora.** Alguém abre uma issue crua propondo algo; o mantenedor roda
  `/aicf:criar-spec #<n>` e a issue vira spec no lugar onde nasceu, com o histórico da conversa
  junto. É o argumento que motiva a demanda vizinha, e sem adoção ele não se realiza: o aicf abriria
  uma issue paralela e a do contribuidor viraria duplicata.

No modo arquivo não há o que adotar — o equivalente já existe e é o `git mv` de `intents/` para
`specs/`.

### Quando o `gh` falha

Mídia issue configurada e `gh` indisponível — sem rede, token expirado, sem permissão — a skill
**mostra o erro e para**. Não grava em arquivo, não grava em rascunho: o usuário resolve o acesso e
retoma. Gravar em `docs/projeto/` "só desta vez" é como um repositório acaba com governança em duas
mídias sem ninguém ter escolhido isso.

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `skills/workflow-demanda/references/midia.md` | **novo.** As duas receitas, operação por operação: gravar demanda, mudar de estado, listar, arquivar, referenciar outra demanda. Os comandos `gh` concretos ficam aqui, e também o aviso de divergência com `docs/agents/issue-tracker.md` |
| `skills/workflow-demanda/SKILL.md` | "Governança — onde mora o quê" passa a ter as duas mídias; a árvore de pastas vira a tabela de estados; aponta para `references/midia.md`. Na tabela de entrevista, a linha do Matt ganha a terceira saída: no modo issue, `to-spec` publica e `/aicf:criar-spec #<n>` adota |
| `skills/setup/SKILL.md` | pergunta da mídia, checagem de `gh` e remote, `gh label create`, e o que criar em cada modo. Lê `docs/agents/issue-tracker.md` quando existe, para propor o default |
| `skills/setup/templates/claude-md.md` | a linha `**Mídia do registro:**` na seção "Processos de desenvolvimento" |
| `skills/setup/templates/roadmap.md` | passa a ser template só do modo arquivo (o texto não muda; muda quem o usa) |
| `skills/criar-spec/SKILL.md` | "A spec" fica neutra: onde hoje manda `git mv` de `intents/` para `specs/`, passa a mandar mudar o estado da demanda, com ponteiro para `midia.md`. Ganha o alvo opcional `#<n>`, que adota issue existente |
| `skills/implementar-spec/SKILL.md` | passo 1 (de onde vem a spec) e a escolha entre specs abertas ficam neutros |
| `skills/fechar-demanda/SKILL.md` | passos 1, 2 e 4 ficam neutros; aceita o alvo opcional `#<n>`. O `grep` que corrige links relativos é **só do modo arquivo** — `#12` não quebra. A linha `Processo` não muda em nenhum dos dois |
| `README.md` | a seção da estrutura de pastas ganha a existência da escolha; a tabela de skills descreve o `setup` nos dois modos |
| `README.en.md` | a nota sobre nomes em português menciona os labels `aicf:*` |
| `CLAUDE.md` (deste repositório) | ganha a linha `**Mídia do registro:** arquivos em docs/projeto/` — declarar o estado atual, não adotar issues |
| `CHANGELOG.md`, `.claude-plugin/plugin.json` | entrada e versão nova |

**Precede [a entrada de quem chega](../intents/a-entrada-de-quem-chega.md)**, que vai reestruturar
`README.md`, `README.en.md` e a abertura do `/aicf:setup` — os três tocados aqui. Nesta demanda, o
mínimo neles: registrar que a escolha existe. A redação fica para lá.

**Interface pública desta demanda** — o que outro projeto passa a poder depender:

- a linha `**Mídia do registro:**` no `CLAUDE.md`, com dois valores possíveis;
- os labels `aicf:backlog`, `aicf:intent`, `aicf:spec`;
- a linha `Processo` como primeira linha do corpo da issue, no mesmo formato que hoje ocupa a linha
  abaixo do título do arquivo. Referência externa continua entrando no fim dela; o número da própria
  issue não, porque a demanda **é** a issue.

## Fora de escopo

- **Modo misto** — spec em issue e relatório em arquivo, ou qualquer combinação. É o gatilho de
  revisão do lema: dois mecanismos coexistindo. A demanda inteira mora numa mídia só, relatório
  incluído. O preço está assumido: o relatório em comentário de issue fechada some do `git clone` e
  é menos achável anos depois. O que compensa já existe e não muda — o **passo 3 do fechamento**
  continua promovendo para o repositório o que vale além da demanda (ADR, regra no `CLAUDE.md`,
  `docs/referencias/`), nas duas mídias.
- **Linear, Jira, GitLab, markdown local.** Só GitHub via `gh`. Abstração antecipando o futuro é o
  outro gatilho do lema; o segundo tracker entra quando alguém pedir.
- **Skill de migração.** Trocar a mídia vale do ponto em diante: o que já está em arquivo fica onde
  está, inclusive `specs/concluidas/`, e demanda nova nasce na mídia nova. Código de migração para
  um evento que acontece no máximo uma vez por projeto não se paga.
- **Depender do setup do Matt.** Considerado: o modo issue exigir `/setup-matt-pocock-skills` e
  usar `docs/agents/issue-tracker.md` como config, sem config própria. Descartado — feature central
  do aicf não pode depender do formato de um plugin de terceiro, que pode mudar sem aviso e quebrar
  em silêncio um repositório que já funcionava, e quem quer só o aicf não deve precisar instalar
  outra coleção. Fica a deferência descrita na Solução: lê para propor e para avisar, nunca para
  decidir.
- **Unificar a declaração dos domain docs.** `CONTEXT.md` e `docs/adr/` estão declarados no
  `docs/agents/domain.md` dele e na seção "Registro" do nosso template de `CLAUDE.md`. É duplicação
  real e **anterior a esta demanda** — vive em
  [o layout dos domain docs está declarado duas vezes](../intents/backlog/layout-dos-domain-docs-declarado-duas-vezes.md).
- **Adotar issues neste repositório.** É a demanda vizinha, [a governança deste repositório passa a
  viver em issues](../intents/governanca-em-issues-neste-repo.md), que consome esta opção. Aqui só
  se cria a opção.
- **Detectar mídia errada.** Nenhuma das duas detecta estado errado, e esta demanda não tenta
  inventar detecção — pasta errada e label errado seguem indistinguíveis de pasta certa e label
  certo.

## Verificação

Um ciclo completo em cada mídia, num repositório de teste com remote GitHub e `gh` autenticado.

**Modo issue, ponta a ponta:**

1. `/aicf:setup`, escolhendo issues. Conferir: `grep 'Mídia do registro' CLAUDE.md` traz a linha com
   `issues (GitHub)`; `gh label list | grep '^aicf:'` traz três; `ls docs/projeto/` traz só
   `PRD.md`; `ls docs/projeto/intents docs/projeto/specs 2>&1` falha, porque as pastas não existem.
2. `/aicf:criar-spec` sobre uma ideia qualquer. Conferir: `gh issue list --label aicf:spec` traz uma
   issue, e `gh issue view <n> --json body -q .body | head -3` mostra a linha `Processo —` logo no
   começo do corpo.
3. Implementar algo trivial e deixar o `/aicf:fechar-demanda` rodar. Conferir:
   `gh issue view <n> --json state -q .state` devolve `CLOSED`, e
   `gh issue view <n> --json comments -q '.comments[-1].body' | head -1` traz
   `## Relatório de implementação (AAAA-MM-DD)`.

**Adoção:** abrir uma issue crua à mão (`gh issue create --title '...' --body 'ideia solta'`, sem
label), rodar `/aicf:criar-spec #<n>` e conferir que `gh issue list --label aicf:spec` traz aquele
número — e que `gh issue list --state open | wc -l` não aumentou, isto é, nenhuma issue paralela
nasceu.

**Deferência ao vizinho:** com `docs/agents/issue-tracker.md` dizendo GitHub e a linha do `CLAUDE.md`
dizendo arquivos, pedir uma demanda nova. O agente avisa da divergência **uma vez** e grava em
`docs/projeto/` — a linha do `CLAUDE.md` é que decide. Rodando o `/aicf:setup` no mesmo repositório,
a opção proposta por default é issues.

**Falha do `gh`:** com `GH_TOKEN=invalido`, pedir uma demanda nova. A skill mostra o erro e para;
`git status --short` sai vazio — nada foi gravado no repositório.

**Não-regressão do modo arquivo:** neste repositório, rodar o ciclo de uma demanda pequena e
conferir que o comportamento é o de hoje — arquivo em `intents/`, `git mv` para `specs/`, relatório
no fim do arquivo, `specs/concluidas/` no fim. O `git log --stat` do fechamento não pode citar
comando `gh` nenhum.

**Neutralidade do texto das skills:** `grep -rn 'docs/projeto/specs\|intents/' --include='SKILL.md' skills`
só pode devolver ocorrência dentro de bloco que declare "modo arquivo", ou ponteiro para
`references/midia.md`. Caminho de pasta solto no meio de uma instrução é o que esta demanda existe
para tirar.
