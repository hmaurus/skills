# O mapa pesa em toda demanda

Processo — entrevista: criar-spec · implementação: aicf-plan

## Problema

O `/aicf:workflow-demanda` entra no contexto no começo de toda demanda. O `CLAUDE.md` do projeto
manda *"invocar ao começar ou registrar uma demanda"* (`grep -c 'invocar ao começar ou registrar'
skills/setup/templates/claude-md.md` → 1), e a description dele diz o mesmo. São 11.229 bytes
(`wc -c < skills/workflow-demanda/SKILL.md`, em `0b3ce9a`), uns 3 mil tokens, dos quais o fluxo
usa um ponto: que a entrevista tem três caminhos e a escolha é do usuário. Na sessão de 2026-09-25
que abriu esta demanda, o agente carregou o mapa por causa dessa linha e não usou o resto.

Duas causas deixam o mapa no caminho:

- **Conteúdo de fase mora nele.** A tabela de implementação é usada pelo `implementar-spec`, que
  oferece os caminhos sem ter o que cada um significa — o defeito que a regra "Critério mora na
  skill que o aplica" do `CLAUDE.md` descreve. As portas de entrada da entrevista e a regra de
  registrar ideia fora de hora também só estão nele.
- **Os anexos de mídia dependem dele.** `midia-arquivo.md` e `midia-issues.md` abrem dizendo que
  os quatro estados e o "um item, um lugar" estão no `/aicf:workflow-demanda`, e o
  `midia-issues.md` remete a ele o critério "certeza, não urgência".

E o mapa ainda mistura as duas mídias: a tabela de estados tem uma coluna para cada, e há linhas
que só valem para um modo.

## Solução

**O mapa vira `/aicf:ajuda`, que só o usuário invoca.** Pasta `skills/workflow-demanda/` →
`skills/ajuda/`, `name: ajuda`, e `disable-model-invocation: true` no frontmatter. Pela doc oficial
(`curl -sL https://code.claude.com/docs/en/skills.md | grep -n 'Description not in context'`), com
essa flag a description sai do contexto e a skill só carrega quando o usuário digita o comando — o
harness garante, não uma frase que o agente pode não seguir. É o desenho do `ask-matt` do Matt
Pocock (`grep -n disable-model-invocation
~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.2.3/skills/engineering/ask-matt/SKILL.md`).
A description passa a falar com o usuário: o ciclo, os caminhos e as convenções, para reler como o
método funciona.

**O que o fluxo usava sai do mapa para quem o aplica:**

| Conteúdo | Vai para |
| --- | --- |
| Tabela de implementação, "descer a tabela troca velocidade por rastro", o gotcha do `task-brief` do Superpowers, o `/setup-matt-pocock-skills` que as skills do Matt exigem | passo 3 do `implementar-spec`, que oferece os caminhos |
| Portas de entrada da entrevista: `/aicf:criar-spec`, e, se instaladas, `brainstorming` (Superpowers) e `grill-with-docs` → `to-spec` (Matt) | a regra "Na entrevista, o caminho é pergunta ao usuário" do `CLAUDE.md` (repositório e template), no padrão que a regra do bug já usa para skill de outra coleção |
| Ideia que surge no meio de outra demanda: registrar pela receita da mídia, estado por **certeza, não urgência**, e voltar ao que estava | regra nova no `CLAUDE.md` (repositório e template): "Quatro regras" vira "Cinco regras" (`grep -rn 'Quatro regras' --include='*.md' . --exclude-dir=.git` só acha os dois arquivos e esta spec) |
| A ressalva do Matt no modo arquivo — a spec do `to-spec` fica em `.scratch/`, e o aicf não a adota | fica no `/aicf:ajuda`: no template pesaria em todo projeto, inclusive sem o Matt, e o setup já avisa isso na pergunta da mídia desde a `0.29.3` |
| Os quatro estados como cada mídia os representa, e o "um item, um lugar" de cada mídia | o anexo da mídia |

**Os anexos saem do mapa:** `skills/workflow-demanda/references/midia-arquivo.md` →
`skills/midia/arquivo.md`, e `midia-issues.md` → `skills/midia/issues.md`. Pasta sem `SKILL.md`,
fora da skill que só o usuário invoca — o agente não tem motivo para hesitar em ler arquivo de
uma skill que ele não pode invocar. `claude plugin validate --strict` aceita a pasta (testado numa
worktree temporária em `0b3ce9a`). Cada anexo passa a bastar sozinho: o cabeçalho que remetia ao
mapa sai, e entram os estados e o "um item, um lugar" daquela mídia.

**O mapa fica com o que é comum e só serve a quem quer entender:** o ciclo e o vocabulário, a
governança comum às mídias (quatro estados sem coluna de mídia, "certeza, não urgência", um
caminho só, `docs/referencias/`, sem modo misto, a divergência com o `issue-tracker.md` do Matt),
"Trabalho recorrente não é demanda" e "Demanda grande". Nada é reescrito além do que sai.

**O `/aicf:setup` apresenta o método lendo o arquivo.** A despedida hoje invoca o mapa pela
ferramenta Skill, o que a flag passa a recusar. O passo troca para `Read` de `../ajuda/SKILL.md`,
e o resumo em linguagem comum com o exemplo concreto continua igual. A proibição antiga era de
`cat`, que despejava as 167 linhas na tela; a saída do `Read` fica recolhida. O passo 5 da
despedida aponta para `/aicf:ajuda`.

**Ponteiros que mudam:** `CLAUDE.md` (repositório; `AGENTS.md` é symlink) e template — *"O mapa do
workflow está na skill `/aicf:workflow-demanda` … invocar ao começar ou registrar uma demanda"*
vira *"O mapa do método está em `/aicf:ajuda`, que só o usuário invoca"*, e a linha das coleções
deixa de dizer que são os caminhos "que o `implementar-spec` pode oferecer" — os de entrevista não
passam por ele; `criar-spec` perde a
linha "O ciclo inteiro está em"; os caminhos dos anexos em `criar-spec`, `implementar-spec`,
`fechar-demanda`, `criar-prd` e `setup`; os READMEs (pt e en), onde a skill passa para a tabela
"Você digita"; a regra do `CLAUDE.md` sobre skill com `disable-model-invocation`, que passa a
listar `ajuda`; e `docs/referencias/verificacao-do-setup.md`, cuja condição do passo 2 da despedida
("Skill, e nenhum `cat` ou `Read`") vira "`Read`, e nenhum `cat`".

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `skills/workflow-demanda/SKILL.md` → `skills/ajuda/SKILL.md` | nome, flag, description; saem as tabelas de entrevista e implementação e as linhas por mídia |
| `skills/workflow-demanda/references/*` → `skills/midia/{arquivo,issues}.md` | cabeçalho sem ponteiro; ganham estados e "um item, um lugar" da própria mídia |
| `skills/implementar-spec/SKILL.md` | tabela de implementação e notas no passo 3; caminho do anexo |
| `skills/criar-spec/SKILL.md`, `skills/fechar-demanda/SKILL.md`, `skills/criar-prd/SKILL.md` | caminho do anexo; `criar-spec` perde o ponteiro para o mapa |
| `skills/setup/SKILL.md` | despedida com `Read` e `/aicf:ajuda`; caminhos dos anexos; menção ao mapa nas coleções |
| `skills/setup/templates/claude-md.md`, `CLAUDE.md` | linha do mapa; linha das coleções; portas de entrada na regra da entrevista; regra nova de ideia fora de hora ("Cinco regras"). Só o `CLAUDE.md` do repositório: `ajuda` na regra do `disable-model-invocation`, que é de quem mantém o plugin |
| `.claude-plugin/plugin.json` | `./skills/workflow-demanda` → `./skills/ajuda`; `0.30.1` → `0.31.0` |
| `README.md`, `README.en.md` | comando novo, na tabela das skills que o usuário digita |
| `docs/referencias/verificacao-do-setup.md` | condição do passo 2 da despedida; passada nova em aberto |
| `CHANGELOG.md` | entrada `0.31.0` |

## Fora de escopo

- **Reescrever o mapa como roteador** ("estou em tal situação, qual comando uso?"), no modelo do
  `ask-matt`. Seria reescrita inteira; se o mapa enxuto não servir a quem pede ajuda, vira
  demanda própria.
- **Uma skill por mídia.** A governança comum às duas existiria duas vezes e divergiria; os
  anexos já separam o que é de cada mídia.
- **Manter `/aicf:workflow-demanda` como apelido.** Dois nomes para a mesma skill; a nota da
  release diz o nome novo.
- **Atualizar o `CLAUDE.md` de projetos já configurados.** O plugin não escreve fora do setup. A
  nota da release traz a linha nova para quem quiser trocar; enquanto não troca, o agente tenta
  invocar o mapa, o harness recusa, e ele segue sem o mapa.
- **Histórico** (`docs/projeto/concluidas/`, `docs/adr/`, entradas antigas do `CHANGELOG.md`) guarda
  o nome antigo: descreve o que era verdade na época.

## Verificação

Os valores de "hoje" foram medidos em `0b3ce9a`.

1. **O nome antigo sumiu do que está vivo.**
   `grep -rln 'workflow-demanda' skills README.md README.en.md CLAUDE.md .claude-plugin | wc -l`
   → hoje 13; depois 0.
2. **Só o usuário invoca.** `grep -c '^disable-model-invocation: true' skills/ajuda/SKILL.md` → 1.
3. **Os anexos bastam sozinhos.** `grep -c 'ajuda\|workflow-demanda' skills/midia/arquivo.md skills/midia/issues.md`
   → 0 nos dois.
4. **O mapa encolheu.** `wc -c < skills/ajuda/SKILL.md` → abaixo de 8.000 (hoje 11.229 no nome
   antigo).
5. **O implementar-spec conhece os caminhos.** `grep -c 'to-tickets' skills/implementar-spec/SKILL.md`
   → hoje 0; depois 1 ou mais.
6. **O template carrega o que o fluxo usa.**
   `grep -c 'certeza, não urgência\|grill-with-docs\|/aicf:ajuda' skills/setup/templates/claude-md.md`
   → hoje 0; depois 3 ou mais.
7. **O repositório passa.** `./scripts/check.sh` → `Tudo verde.`
8. **Comportamento, no uso real.** Depende do titular atualizar o plugin e reiniciar a sessão
   (regra do `CLAUDE.md`), então não tem passada dedicada. Encerra: na primeira demanda com a
   `0.31.0`, o agente não carrega `/aicf:ajuda`; `/aicf:ajuda` digitado mostra o mapa; e o próximo
   `/aicf:setup` apresenta o método sem invocar skill.

## Relatório de implementação (2026-09-26)

- **Status** — concluído. Sem push nem CI conferido até este commit; a verificação 8
  (comportamento) fica para o uso real, como a spec previa.
- **Arquivos alterados**
  - `skills/workflow-demanda/SKILL.md` → `skills/ajuda/SKILL.md`: `name: ajuda`, a flag, e a
    description falando com o usuário. Saíram as tabelas de entrevista e de implementação, e a
    tabela de estados perdeu as colunas de mídia. Uma seção curta, "Os caminhos de cada fase", diz
    quem oferece cada caminho e guarda a ressalva do `.scratch/` do Matt.
  - `skills/workflow-demanda/references/midia-*.md` → `skills/midia/{arquivo,issues}.md`, com os
    quatro estados, "certeza, não urgência" resumido e o "um item, um lugar" da própria mídia.
  - `skills/implementar-spec/SKILL.md`: a tabela de implementação e as notas do Matt e do
    Superpowers no passo 3.
  - `criar-spec`, `fechar-demanda`, `criar-prd` e `setup`: caminho novo do anexo. O setup lê o mapa
    com `Read` e aponta `/aicf:ajuda`.
  - `CLAUDE.md` e o template: a linha do mapa, a linha das coleções, as portas de entrada na regra
    da entrevista e a regra nova da ideia fora de hora ("Cinco regras").
  - `plugin.json` (`0.31.0`), os READMEs, `CHANGELOG.md`, `docs/referencias/verificacao-do-setup.md`
    (a passada nova em aberto) e `docs/projeto/PRD.md:56`.
- **Commits** — `1150be5 feat(ajuda): o mapa vira /aicf:ajuda, que só o usuário invoca`; o
  fechamento vai no commit seguinte.
- **Validação** — as sete verificações da spec, rodadas depois do commit de código:
  1 → `0`; 2 → `1`; 3 → `0` e `0`; 4 → `7900`; 5 → `2`; 6 → `3`; 7 → `Tudo verde.`
  A 8 fica aberta: ela encerra na primeira demanda com a `0.31.0`, se o agente não carregar
  `/aicf:ajuda`; também quando `/aicf:ajuda` digitado mostrar o mapa; e na próxima passada do setup,
  pela condição registrada em `verificacao-do-setup.md`. Revisão por um subagente que não viu a
  implementação, sem bloqueio. Três achados foram corrigidos antes do commit: `PRD.md:56` apontava
  para o arquivo antigo; a regra nova não dizia onde fica a receita da mídia; e o
  `midia/issues.md` se contradizia sobre onde está o critério inteiro.
- **Escopo efetivo** — além da tabela da spec, mudaram o `docs/projeto/PRD.md`, que citava o
  arquivo antigo num comando de conferência, e a frase dos READMEs sobre as skills que você
  digita "conduzirem uma sessão inteira", que não vale para `/aicf:ajuda`. O título interno do
  mapa continua "Workflow de uma demanda".
- **Lições** — ao tirar uma skill do alcance do agente, sai também o que só ela dizia. A spec
  mapeou o que o fluxo usava, e a revisão achou três notas sobre entrevista por outra coleção que
  ficaram sem leitor. Viraram
  [o agente não vê o que só o mapa diz da entrevista](../backlog/o-agente-nao-ve-o-que-so-o-mapa-diz-da-entrevista.md).
  Promoção: nada para o `CLAUDE.md` além do que a própria demanda escreveu. A regra "Critério mora
  na skill que o aplica" já cobre a lição.
