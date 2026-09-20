# Changelog

## 0.21.0 — 2026-09-20

- **A comparação do README para de errar sobre o tracker do Matt Pocock.** Os três lugares que
  diziam "GitHub, Linear ou markdown local" — `README.md`, `README.en.md` e a própria regra do
  `CLAUDE.md` que manda conferir afirmação sobre ferramenta de terceiro — passam a dizer GitHub,
  GitLab ou markdown local, e outro tracker descrito em prosa. Linear não é opção do setup dele:
  entra como exemplo dentro de "Other (Jira, Linear, etc.)", que o usuário preenche em texto livre
  (`sed -n 44,47p $R/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`). A frase errada
  tinha sido escrita justamente para corrigir outro erro na mesma seção, em 2026-09-18.
- **Três frases da seção "Por que este" ganham a nuance que faltava.** "Nada pede que sejam
  revistos contra o que saiu" virou "o código é revisto contra o plano durante a execução, mas o
  plano e a spec ficam como foram escritos": o `subagent-driven-development` faz "task review (spec
  compliance + code quality) after each"
  (`sed -n 8p $R/superpowers/skills/subagent-driven-development/SKILL.md`); o que não acontece é o
  documento ser atualizado, e a issue [obra/superpowers#1075](https://github.com/obra/superpowers/issues/1075)
  segue aberta (`gh issue view 1075 -R obra/superpowers --json state`). "O Superpowers grava spec e
  plano em arquivo" ganhou "no caminho _architectural_" — nos caminhos _bounded_ e _spike_ é "No
  spec file, no implementation plan document"
  (`grep -n 'No spec file' $R/superpowers/skills/brainstorming/SKILL.md`). E o absoluto "nenhuma das
  duas tem o documento ... com o que ficou fora por decisão" ganhou a ressalva do Matt, que guarda o
  pedido recusado em `.out-of-scope/<conceito>.md`
  (`sed -n 1,10p $R/skills/skills/engineering/triage/OUT-OF-SCOPE.md`).
- **A seção passa a responder "por que não o GSD?".** GSD Core e BMAD têm os quatro critérios da
  governança do aicf, em forma quase idêntica, e o README só comparava com Superpowers e Matt. O
  parágrafo novo — único acréscimo da demanda; o resto é substituição — diz que a camada deles vem
  grudada num loop de execução próprio (72 comandos, `ls $R/gsd-core/commands/gsd | wc -l`; 30
  skills e `uv` obrigatório, `ls $R/bmad-method/skills | wc -l` e `sed -n 18,19p $R/bmad-method/README.md`),
  e que é esse loop que o aicf deixa de fora por decisão
  ([ADR 0001](docs/adr/0001-fronteira-de-fase.md)). O título dos dois READMEs passa a cobrir os
  quatro.
- **A fonte de tudo isto é a pesquisa** [governança macro nos frameworks vizinhos](docs/referencias/governanca-nos-frameworks-vizinhos.md),
  de 2026-09-19, que lê sete frameworks em fonte primária com sha e comando por afirmação. Os shas
  reconferidos nesta demanda: `obra/superpowers` `5bf4e78`, `mattpocock/skills` `c55ee46`,
  `open-gsd/gsd-core` `6dcc042`, `bmad-code-org/bmad-method` `f033e70`.

## 0.20.0 — 2026-09-19

- **A referência de mídia vira um arquivo por mídia.** `midia.md` trazia as duas receitas lado a
  lado, e a mídia é escolhida uma vez no setup: quem abria a referência no modo arquivo carregava
  5.666 bytes de seções que só existem para issue, num arquivo de 12.747. Agora são
  `references/midia-arquivo.md` (1.585 bytes, `wc -c < skills/workflow-demanda/references/midia-arquivo.md`)
  e `references/midia-issues.md`; o que é comum às duas — a linha de configuração, os quatro
  estados, "um item, um lugar", a divergência com o tracker do Matt — fica só no
  `/aicf:workflow-demanda`, que já tinha a configuração e os estados e agora ganha a divergência. As medições que provaram os dois comportamentos do
  `gh` saem da referência: são evidência para quem mantém o plugin, e já estão na entrada da
  `0.17.0` deste arquivo. O [ADR 0004](docs/adr/0004-midia-do-registro-e-config-propria.md) fica de
  pé — config na linha do `CLAUDE.md`, skills neutras, comando concreto num lugar só por mídia —;
  onde ele diz que uma terceira mídia entra como coluna nova, entra como arquivo novo.
- **As skills apontam, em vez de repetir.** O parágrafo de mídia que `criar-spec`,
  `implementar-spec` e `fechar-demanda` carregavam quase idêntico vira duas frases: qual arquivo
  seguir, e o aviso de divergência com `docs/agents/issue-tracker.md`. O aviso continua dentro das
  três de propósito — a revisão da `0.17.0` mostrou que no modo arquivo a referência não é aberta;
  só a justificativa dele mudou para o `workflow-demanda`. O conjunto das skills e referências cai
  de 60.080 bytes no `745d9a0` para 56.556
  (`wc -c skills/*/SKILL.md skills/workflow-demanda/references/*.md | tail -1`; para o valor antigo,
  o mesmo `wc` num checkout de `745d9a0`).
- **Três casos ganham operador.** Pular a entrevista era legítimo no `workflow-demanda` e nenhuma
  skill o executava: o passo 1 do `implementar-spec` passa a virar spec um intent que o usuário
  mandou implementar sem entrevista, com `entrevista: nenhuma`. No `/aicf:setup`, as perguntas
  sobre gerenciador de senhas e fonte de documentação só acontecem se os padrões de engenharia vão
  para algum lugar — quem escolheu "nenhum dos dois" não tinha onde guardar as respostas. E a
  apresentação prometia "cerca de seis" perguntas, que eram sete; agora diz "entre cinco e sete".
- **Três trechos voltam para perto do que explicam.** Em `criar-spec`, a lista das cinco seções da
  spec abre a seção "A spec", e o material de mídia e de estado desce para "Onde ela mora". Em
  `setup`, o parágrafo de cópia dos templates fica logo abaixo da tabela de templates, em três
  frases, e não mais depois da subseção dos labels. Em `implementar-spec`, a linha solta sobre plan
  mode sai do topo e entra no ramo `aicf-plan` do passo 3, onde o plan mode se decide.

## 0.19.0 — 2026-09-19

- **O repositório ganha verificação, e o GitHub a roda depois do push.** `./scripts/check.sh` é o
  comando único que a regra *"antes de commitar, rodar no projeto inteiro"* passa a ter aqui, e o
  `.github/workflows/ci.yml` executa **esse mesmo script** — o YAML não repete comando nenhum. São
  três checks: link relativo de markdown que aponta para arquivo inexistente (53 conferidos, 0
  quebrados no commit desta versão — `python3 scripts/check_links.py`), `claude plugin validate
  --strict` nos manifestos de `.claude-plugin/` e no frontmatter das skills, e a versão do
  `plugin.json` sendo a entrada do topo do changelog. A falta tem dano
  medido: oito links quebrados em duas demandas (2026-09-14 e 2026-09-18), achados só porque alguém
  lembrou de rodar o `grep` do passo 2 do ritual.
- **O check de links não enxerga código, e ignora `skills/setup/templates/**`.** Link de exemplo
  dentro de bloco cercado ou de crase é ilustração, não link — num repositório que existe para
  ensinar a escrever markdown com link relativo, conferi-lo deixaria o check vermelho por um
  não-defeito. Nos templates o link fala do projeto que vai receber a cópia: sem essa exclusão o
  check nasceria com 6 falsos positivos, e check que nasce vermelho não é lido. O ponto cego —
  link quebrado dentro de um template passa batido — encerra quando um chegar ao projeto de um
  usuário.
- **A entrada do `CHANGELOG.md` passa a subir junto com o bump da versão**, e não mais no commit de
  fechamento. O check as confere em par: separá-las deixaria o CI vermelho em todo commit de
  release, que é exatamente a hora em que o check é rodado. O commit de fechamento ainda ajusta o
  texto da entrada com o que descobriu.
- **A linha `Repositório, branch de trabalho e CI mínimo` sai do `ROADMAP.md`** — quem tem arquivo
  não tem linha. Ela nunca foi decidida: era o item de exemplo do template, copiado junto quando o
  roadmap nasceu (`git show a6276e7 -- docs/projeto/ROADMAP.md skills/setup/templates/roadmap.md`).

## 0.18.0 — 2026-09-18

- **O `README.md` se reorganiza por quem chega, e não por assunto.** O público do aicf é aluno,
  parceiro e indicado: entra pelo GitHub, lê o README e só entende de verdade rodando o
  `/aicf:setup`. O arquivo estava escrito para quem já sabe o que é isso — um quarto do texto era
  comparação com Superpowers e Matt Pocock, citando `brainstorming`, `grill-with-docs` e
  `to-tickets` como se fossem óbvios, antes de qualquer "como eu começo". Agora a abertura é o
  problema que o método resolve, vem um diagrama Mermaid do ciclo, e cada um dos três problemas
  termina na skill que o corrige. O que é para quem já usa **dobra em `<details>`, não muda de
  arquivo**. Texto visível: 105 linhas, contra 115 antes
  (`awk '/^<details/{d=1} /^<\/details>/{d=0;next} !d' README.md | wc -l`).
- **Não haverá `MANUAL.md`, e isso virou decisão escrita.** O manual em runtime já existe e se
  chama `/aicf:workflow-demanda`; um terceiro arquivo com o mesmo conteúdo seria a cópia que
  envelhece sem nada que a cutuque, que é o que este repositório já pagou para aprender duas vezes.
  O [ADR 0005](docs/adr/0005-a-documentacao-humana-e-um-arquivo-so.md) registra o porquê, o que
  fica de fora e o que reverter custaria. O desenho vem do repositório do Matt Pocock, que cabe num
  README de 231 linhas organizado por modo de falha do leitor; o `spec-kit` do GitHub é o
  contraexemplo, e separou em site inteiro porque tem dezenas de páginas. São seis skills aqui.
- **A tabela de skills troca de eixo: quem pode chamar.** Das seis, duas só existem quando você as
  digita (`setup`, `criar-prd`); as outras quatro você digita **ou** o agente alcança sozinho. O
  eixo antigo — invocável × não-invocável — tinha deixado de fechar na `0.17.0`, quando
  `/aicf:criar-spec #12` e `/aicf:fechar-demanda #12` ganharam forma digitável e passaram a estar
  dos dois lados. O eixo novo é o do repositório do Matt e acomoda as duas sem categoria nova,
  porque separa quem **pode** chamar, não quem costuma.
- **Duas afirmações erradas sobre ferramenta de terceiro, as duas na mesma seção.** (1) *"o Matt
  publica spec e tickets no issue tracker"* — o `setup-matt-pocock-skills` oferece GitHub Issues,
  Linear ou markdown local em `.scratch/<feature>/`, este recomendado por ele para projeto solo e
  repositório sem remote. A frase piorou na `0.17.0`: agora que o aicf também pergunta arquivo ou
  issue, ela anunciava uma diferença que não existe em nenhum dos dois lados. (2) *"o Superpowers
  apaga a pasta de trabalho"* — ele remove a **worktree**, e só quando foi ele quem a criou e em
  duas das quatro opções; plano e design doc ficam commitados em `docs/superpowers/`, com o
  `brainstorming` mandando "save ... and commit". Vale nas versões 5.0.0 e 6.1.1. O contraste real
  é outro e mais forte: `grep -rliE "diverge|what actually shipped|retrospective|final report"
  skills/*/SKILL.md` no Superpowers 6.1.1 não devolve arquivo nenhum — o registro deles é escrito
  **antes** de executar e nada pede que seja revisto contra o que saiu.
- **O substituto que o intent propunha também não passou no teste.** Ele sugeria *"o tracker dele é
  descartável por declaração dele"*; a declaração não existe —
  `grep -rniE "throwaway|disposable|ephemeral"` nas skills dele devolve só o `wizard` falando de si
  mesmo e o `ask-matt` falando do contexto da sessão. O nome `.scratch/` sugere descarte, nenhuma
  skill declara. Virou regra no `CLAUDE.md`: **afirmação sobre ferramenta de terceiro carrega o
  comando que a confere, no texto que a propõe.** Errar sobre o próprio repositório é barato;
  errar sobre a ferramenta do vizinho derruba o crédito da comparação inteira.
- **O `/aicf:setup` se apresenta antes da primeira pergunta.** Ele abria em "1. Nome do projeto", e
  quem rodava pela primeira vez respondia antes de saber o que estava sendo montado. Agora vêm três
  a cinco linhas — o que vai ser montado, que são cerca de seis perguntas, e que nada é criado
  antes de confirmar — e nada além disso, porque abrir com três parágrafos sobre governança seria o
  mesmo muro em lugar novo.
- **E se despede apresentando o método, não um ponteiro.** O fim tinha quatro passos, todos
  apontando para outras skills. Agora são cinco, e o segundo manda **carregar o
  `/aicf:workflow-demanda` e contar o que ele diz em linguagem comum**, com as quatro fases em uma
  frase cada e um exemplo concreto de primeira demanda usando o nome real do projeto e a mídia que
  o usuário acabou de escolher. O roteiro mora na skill; o texto se compõe na hora, da fonte da
  verdade — um mecanismo, não dois.
- **O `README.en.md` acompanha inteiro**, seção por seção (`grep -c '^## ' README.md README.en.md`
  devolve 6 nos dois). Encolher o inglês para um stub foi considerado e recusado na entrevista: o
  custo de manter os dois em dia é aceito.

## 0.17.0 — 2026-09-17

- **A mídia do registro vira escolha do projeto: arquivos ou issues do GitHub.** O aicf assumia
  arquivo em toda skill, e quem preferia issue tracker customizava por fora, sem suporte e sem
  documentação — o último trilho único de um método que já oferece três caminhos de entrevista e
  quatro de implementação. Agora a demanda pode nascer e morrer como issue, e a governança não muda:
  as quatro fases, o ritual de fechamento e a linha `Processo` são as mesmas nos dois modos. A
  configuração é **uma linha do `CLAUDE.md`**, ao lado da que já declara as coleções instaladas —
  nenhum mecanismo novo, porque o arquivo já carrega inteiro em toda sessão. O desenho vem do
  conjunto do Matt Pocock, que já provou em produção que a mídia cabe numa resposta de setup lida em
  runtime; o [ADR 0004](docs/adr/0004-midia-do-registro-e-config-propria.md) registra por que o aicf
  lê o `docs/agents/issue-tracker.md` dele, mas não depende.
- **Nada quebra em projeto que já usa o plugin: linha ausente significa arquivo.** Não há migração e
  não haverá skill de migração — trocar a mídia vale do ponto em diante, o que está em arquivo fica
  onde está, e demanda nova nasce na mídia nova. Código para um evento que acontece no máximo uma vez
  por projeto não se paga.
- **As cinco skills ficam neutras de mídia; o comando concreto mora num lugar só.**
  `skills/workflow-demanda/references/midia.md` (221 linhas,
  `wc -l < skills/workflow-demanda/references/midia.md`) traz as duas receitas lado a lado, operação
  por operação. Uma terceira mídia no futuro acrescenta coluna em vez de espalhar condicional por
  quatro arquivos. É a primeira pasta `references/` do plugin.
- **Seis gavetas viram quatro estados.** No modo issue, "Próximas" e `intents/` deixam de se
  distinguir — a diferença entre elas era o custo de criar arquivo, que a issue não tem. Sobram três
  labels exclusivos (`aicf:backlog`, `aicf:intent`, `aicf:spec`) mais a issue fechada, e **uma
  demanda é uma issue só, do nascimento ao fechamento**: o label troca, o número não. Por isso não
  existe `ROADMAP.md` no modo issue, e o critério *certeza, não urgência* que ele explicava passa a
  viver na descrição do label `aicf:backlog` — que tem limite de 100 caracteres.
- **O `/aicf:setup` cria os labels, e não deixa isso para a primeira demanda.** `gh issue create
  --label` com label inexistente falha em vez de criar; é a reclamação mais repetida sobre setups
  que só gravam o mapeamento. Criação idempotente, com `|| true`. O setup também confere
  `gh auth status` e o remote **antes** de oferecer issues: deixar o usuário escolher um caminho que
  falha no primeiro comando é pior que não oferecer.
- **`/aicf:criar-spec #12` e `/aicf:fechar-demanda #12` adotam uma issue que já existe**, em vez de
  abrir outra. Sem isso, quem entrevista pelo `to-spec` do Matt — que cria issue nova e não edita a
  existente — terminaria com duas issues para a mesma demanda, e a issue crua de um contribuidor
  viraria duplicata em vez de virar a spec no lugar onde nasceu.
- **Mídia issue com `gh` indisponível é parada, não fallback.** A skill mostra o erro e para. Gravar
  em `docs/projeto/` "só desta vez" é como um repositório acaba com governança em duas mídias sem
  ninguém ter escolhido isso.
- **Dois comportamentos do `gh` medidos antes de entrarem no doc.** (1) `--label` repetido filtra por
  **todos** os labels, não por qualquer um: com uma issue de cada label, os três flags juntos
  devolvem 0 e `--search "label:aicf:backlog,aicf:intent,aicf:spec"` devolve 3. Reproduz em
  repositório público, sem depender de nada nosso:
  `gh issue list --repo denoland/deno --state open --label node:http --label node:sqlite --json number -q length`
  devolve 0, e a forma `--search` equivalente devolve 6, que é 2 + 4. (2) **O índice de label atrasa
  depois de um `edit`** — 4 defasagens em 6 rodadas alternando o label da mesma issue. A consulta
  devolve o estado anterior à troca enquanto a coluna exibida mostra o atual, o que produz uma linha
  aparentemente impossível. Troca de estado se confirma com `gh issue view`, que lê a issue direto.
- **Oito achados de revisão de código, todos procedentes, corrigidos antes do release.** Os dois
  graves não eram erro de escrita, e sim de alcance — instrução certa, num lugar por onde não passa
  quem precisa dela. O template do `CLAUDE.md` trazia a linha de mídia com o valor do modo arquivo
  escrito por extenso e sem marcador de preenchimento, cem linhas depois da pergunta que decide o
  valor: setup em modo issue criaria os labels e copiaria a linha dizendo "arquivos". E o aviso de
  divergência com o tracker do Matt vivia só no `midia.md`, que no modo arquivo nenhuma skill tem
  motivo para abrir — era falha declarada da própria Verificação da spec. A lição virou regra em
  [`.claude/rules/templates.md`](.claude/rules/templates.md), que carrega só ao tocar
  `skills/setup/templates/**`.
- **O template de `README.md` ganhou um bloco por mídia.** O README gerado listava `ROADMAP.md`,
  `intents/` e `specs/` na tabela "Onde ficam as coisas" — três links mortos em todo projeto novo
  que escolhesse issues. Achado pela varredura de links do fechamento, depois da revisão.
- **`/aicf:criar-prd` ganhou um qualificador, embora a spec o pusesse fora de escopo.** O passo 2
  dele mandava tirar do PRD o primeiro `ROADMAP.md` — arquivo que não existe no modo issue. A skill
  não foi reestruturada; a redação fica para a demanda da entrada de quem chega.
- **Os READMEs registram que a escolha existe, e só.** A reestruturação dos dois é da demanda
  [a entrada de quem chega](docs/projeto/specs/concluidas/a-entrada-de-quem-chega.md), que os toca inteiros.

## 0.16.0 — 2026-09-14

- **O índice derivado sai do método: um item, um lugar.** O `CHECKLIST.md` tinha três seções
  espelhando três pastas, e toda demanda existia duas vezes — arquivo na pasta, linha na seção. O
  método defendia a duplicação como detecção de erro, e o argumento estava invertido: o
  [ADR 0002](docs/adr/0002-conferencia-do-indice-por-inclusao.md) decidiu que a conferência corre
  **num sentido só**, o que não é partida dobrada — é a declaração formal de que a pasta é a fonte e
  o checklist uma cópia mantida à mão. Cópia manual não detecta erro na fonte; ela fabrica uma
  classe de erro nova e depois gasta ritual achando o erro que criou. A regra que muda cabe em três
  palavras: onde se lia *"a linha vira ponteiro"*, agora **a linha sai** — enquanto a demanda não
  tem arquivo ela é uma linha no roadmap; quando vira arquivo, a pasta é o registro inteiro, e
  nunca as duas coisas. O índice que se perde volta por
  `head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'`, gerado e sempre
  correto, com os títulos de verdade em vez dos slugs.
- **`CHECKLIST.md` → `ROADMAP.md`, com as duas seções que nunca tiveram pasta.** `Próximas` (o que
  já foi decidido e ainda não tem arquivo, onde entram as linhas que eram `Fundação`) e `Backlog`
  (o que ainda não é certeza). `Decidido`, `Em andamento` e `Entregue` não têm substituto porque não
  precisavam existir. O nome mudou de propósito: num arquivo chamado `CHECKLIST` alguém
  eventualmente recria uma seção `Entregue`, porque é o que checklists fazem. Arquivo próprio e não
  seção do `PRD.md`, por ritmo de escrita oposto — nos 44 commits até
  `ddc7477`, o último antes desta demanda, o checklist mudou 6 vezes e o PRD mudou 1, a de criação.
  Os três números reproduzem com `git log --oneline ddc7477 [-- <arquivo>] | wc -l`.
- **O `fechar-demanda` perde um passo inteiro e encolhe 15 linhas** — de 130 para 115
  (`wc -l < skills/fechar-demanda/SKILL.md`). O passo 3 (`- [x]`, mover a linha entre seções) morre:
  sem ponteiro não há o que marcar. O passo 5 vira 4 e cai de 16 para 4 linhas
  (`awk '/^4\. \*\*Fechar o que este ritual abriu/,/^$/' skills/fechar-demanda/SKILL.md | grep -c .`)
  — sai a conferência
  dos três pares, ficam as duas partes que nunca foram sobre o checklist: o ADR recém-criado entra
  como link no relatório da própria demanda, e a pergunta sobre item novo passa a olhar o roadmap.
  São cinco passos que viram quatro, em todo projeto que usa o plugin.
- **A demanda "a conferência do índice vira script" foi cancelada, não implementada.** Ela existia
  para transformar aquela comparação em código; sem duas fontes não há comparação, nem em prosa nem
  em script. O diagnóstico dela continua valendo em geral — *prosa que descreve operação sem
  julgamento é código disfarçado* —, mas aqui a resposta certa era remover a operação. Fica
  arquivada em `docs/projeto/specs/concluidas/` com o relatório do cancelamento.
- **Migração de projeto que já usa o plugin**, à mão e em três passos, porque uma skill de migração
  seria código novo para uma operação única por projeto: (1) conferir uma última vez que todo
  arquivo de `intents/`, `specs/` e `specs/concluidas/` tem linha no `CHECKLIST.md` — o que faltar
  não existe em lugar nenhum e precisa ser criado como arquivo; (2) copiar `Fundação` e `Backlog`
  para um `ROADMAP.md` novo, `Fundação` virando linhas de `Próximas`; (3) apagar o `CHECKLIST.md`.
  As seções `Decidido`, `Em andamento` e `Entregue` não migram — a pasta já as contém, e o histórico
  de entregas vive em `specs/concluidas/` e no `CHANGELOG.md` do projeto.

## 0.15.0 — 2026-09-09

- **ADR passa a ser artefato do `/domain-modeling` (Matt Pocock); a governança fica só com o gatilho.** O aicf tinha herdado o conceito de ADR por assimilação — os três critérios da tabela do passo 4 são cópia literal dos dele — e depois desenvolveu um formato próprio muito mais pesado: os dois ADRs deste repositório têm quatro seções e ~57 linhas cada (`wc -l docs/adr/*.md`), enquanto o `ADR-FORMAT.md` do Matt prescreve "an ADR can be a single paragraph" com Considered Options e Consequences como seções **opcionais**, usadas só quando a rejeição vale ser lembrada. A frase "podem sair de `/domain-modeling`, quando instalado" prometia uma delegação que nunca aconteceu na prática. Agora formato e numeração são dele, e sem ele instalado o mínimo basta — um parágrafo, imutável. O que a governança fornece é o momento de perguntar "esta demanda produziu decisão difícil de reverter?", que é barato e é o que o `domain-modeling` não cobre: ele é invocado ao modelar domínio, não a cada fechamento.
- **A pasta de conhecimento operacional ganha nome: `docs/referencias/`.** O `workflow-demanda` já dizia que doc descrevendo o mundo — configuração, ID externo, número de negócio, aprendizado — não entra em `docs/projeto/`, e parava em "a raiz de `docs/` basta até haver arquivo suficiente para uma pasta de domínio", deixando o destino por conta de cada projeto. Sem nome, o material acaba no `CLAUDE.md`, que carrega inteiro em toda sessão — foi o que aconteceu num projeto que consome estas skills, onde IDs de agregador e regras de variável de ambiente moram no arquivo mais caro do repositório. O nome casa com a palavra que a tabela do passo 4 já usava ("doc de referência"), então destino e pasta deixam de precisar de tradução. Criada preguiçosamente, como `docs/adr/` e `CONTEXT.md`.
- Nenhuma das duas mudanças cresce as skills: `fechar-demanda` e `workflow-demanda` seguem em 130 e 132 linhas (`wc -l skills/fechar-demanda/SKILL.md skills/workflow-demanda/SKILL.md`). A linha do ADR na tabela encolheu, e a justificativa que sobrava na delegação pagou o texto novo.

## 0.14.0 — 2026-09-09

- **O passo 5 do fechamento deixa de pedir julgamento e passa a enumerar.** Num projeto que consome estas skills, o checklist ficou desatualizado em três lugares e o agente não achou nenhum sozinho — nem no ritual, nem nas duas vezes em que o titular mandou conferir. A causa não era desatenção: *"está atualizado?"* devolve ao conferente a escolha do que conferir, e ele inventa uma lista de suspeitas nova a cada passada. Agora o passo nomeia três pares — `Decidido`↔`intents/`, `Em andamento`↔`specs/`, `Entregue`↔`specs/concluidas/` — e a conferência corre num sentido só: **todo arquivo da pasta tem linha na seção**. Cai junto a falta em que um item entregue foi **apagado** em vez de movido. O sentido importa: linha sem arquivo é legítima e comum — o primeiro checklist sai do PRD quase todo em linhas sem arquivo —, então o passo diz explicitamente para nunca apagar linha por não achar arquivo, e deixa `Fundação` e `Backlog` fora da enumeração por não terem pasta.
- **O passo 5 passa a olhar para o passo 4, que é quem cria o que o índice precisa listar.** A falta original era um ADR novo ausente do índice, e a raiz era textual: o passo 5 mandava conferir se "a execução" criou item, e "a execução" foi lida como a implementação — o código recém-escrito —, nunca como o passo que tinha acabado de rodar. Os dois passos não se falavam, embora o 4 exista justamente para produzir ADR, regra e doc de referência. Agora a saída dos passos 1 a 4 entra na conferência, e o ADR criado aparece como link no item de `Entregue` da demanda: um par a conferir no arquivo que o ritual já está editando, em vez de um segundo índice para sincronizar.
- **O `CHECKLIST.md` ganha a seção `Decidido`, o par que faltava existir.** `intents/` não era espelhado por seção nenhuma — `Em andamento` espelha `specs/`, e intent não-entrevistada não é "demanda ativa" pela definição escrita. Não era item esquecido: nada no índice apontava para a pasta, e demanda decidida ficava invisível para quem abria o checklist. Instrução que manda enumerar não tem o que enumerar se o par nunca foi declarado. As notas das três seções passam a dizer qual pasta cada uma espelha, e o `criar-spec` move a linha de `Decidido` para `Em andamento` junto com o `git mv` do arquivo.
- **Afirmação verificável passa a carregar o teste que a refuta.** A falta mais grave do episódio foi um item de backlog que descrevia como pendente uma decisão já tomada e aplicada havia commits — e nenhum número estava errado, só o veredito. Uma regra de "número vem com o comando que o reproduz" não a pegaria: remedir devolveria o mesmo número e a frase passaria. O objeto da regra é a afirmação, não o número: número traz o comando que o remede (`919 linhas` (`wc -l < arquivo`, 2026-09-08)), afirmação de estado traz a condição que a encerra (`— encerra quando houver workflow em .github/workflows/`). Entra no passo 4, no formato do relatório e no `criar-spec`, para valer quando a frase nasce e não só quando o ritual passa por ela.
- **Mover a demanda para `specs/concluidas/` passa a incluir os links que apontavam para ela.** Achado da própria implementação: o `git mv` do intent quebrou cinco links relativos em outras demandas de uma vez. É a mesma classe de deriva num par que ninguém tinha nomeado, e todo fechamento a reproduzia. O passo 2 agora traz o `grep` que acha as referências.
- Fora de escopo, com motivo registrado na spec: skill de auditoria do registro e hook para a classe A (redundantes com o acima, e o hook exigiria o plugin gerar script no projeto consumidor); índice de ADRs no checklist (o link no item de `Entregue` já dá o par, e um índice a menos é um índice a menos para derivar); espelho para `intents/backlog/`; e a regra da classe B no `CLAUDE.md`, que daria a maior cobertura e custa linhas no arquivo lido inteiro em toda sessão.

## 0.13.5 — 2026-09-08

- **Integração e fechamento deixam de ser a mesma palavra.** Numa execução com três coleções no mesmo projeto, o agente concluiu a demanda sem rodar o `finishing-a-development-branch` que o `subagent-driven-development` encadeia: leu "o fechamento continua sendo `/aicf:fechar-demanda`" — uma garantia de que o registro sobrevive a qualquer caminho — como exclusão, "só o aicf fecha". O código ficou parado numa branch 40 commits atrás da base, com a decisão de destino nunca tomada, e o registro dizendo "concluído". A raiz era textual: uma palavra nomeava fechar o *branch* e fechar a *demanda*. Agora _integração_ é o destino do código e o último passo da **implementação**, que pertence ao método escolhido; _fechamento_ é só o registro da demanda. A frase que resolve a leitura errada — **o método fecha o código, a governança fecha a demanda** — sobe para as quatro regras do `CLAUDE.md`, porque o caso real foi um agente que não abriu a skill certa.
- **A borda entre governança e framework ganha critério: fronteira de fase.** A governança escolhe o caminho de cada fase; dentro da fase, o encadeamento do framework roda inteiro, automático, sem pedir licença — interferir ali degrada a qualidade de um processo que não é nosso. Na passagem entre fases quem decide é a governança, mesmo quando o framework recomenda continuar nele: o `brainstorming` declara `writing-plans` como estado terminal, e parar na fronteira continua legítimo. Sem esse critério, "não interferir" não tinha borda — e a tabela de implementação passa a dizer, por caminho, quem faz a integração.
- **Branch e worktree passam a ser avaliados, não herdados.** O default continua o mesmo (commitar direto na branch de trabalho, PR pelo que o risco justificar), mas o agente decide com critério escrito e conta em uma linha, em vez de aplicar o default em silêncio e chamar de decisão. O critério que faltava: **contra worktree quando a verificação depende de estado local não versionado** — banco, `.env`, pasta gitignored —, porque a worktree nasce sem eles.
- **Exigência já satisfeita pelo caminho escolhido não se repete.** O `fechar-demanda` pede revisão por subagente fresco e o `subagent-driven-development` já revisa o branch inteiro no fim; sem ressalva, a regra literal manda rodar duas revisões de tudo. O relatório passa a declarar, em uma linha na Validação, qual passo cobriu qual exigência.
- Correções menores no `fechar-demanda`: a linha que dizia que ADR e glossário "saem de `/domain-modeling`, que o agente invoca em qualquer processo — não depende das skills do Matt" errava o fato (a skill **é** da coleção do Matt) e descrevia um comportamento que não acontece; afrouxa para "quando instalado, e escrever direto pela tabela também serve". E o `workflow-demanda` registra a armadilha do `scripts/task-brief` do Superpowers, que procura `^#+ Task N` e não acha "Tarefa N": os headings de tarefa do plano ficam em inglês, com o corpo em português.

## 0.13.4 — 2026-09-06

- O `## Idioma` do template de preferências ganha **a exceção para domínio regulado brasileiro**. A regra dizia "código em inglês" sem ressalva, o que é o padrão certo para a maioria dos projetos — mas o público do plugin é dev brasileiro, e em domínio fiscal, contábil, jurídico ou bancário os termos não têm equivalente honesto em inglês: "competência" não é _accrual basis_, "estorno" cobre o que em inglês são três coisas. Nomear em inglês ali cria uma camada de tradução entre a conversa e o código, exatamente o que o glossário em português existe para evitar; sem regra escrita, quem enfrentava isso decidia por gosto, projeto a projeto, e decidia de novo no seguinte. O parágrafo dá **o teste, não a permissão** — a maioria dos projetos continua em inglês depois de aplicá-lo —, delimita o que fica em inglês sempre (convenção de ecossistema: `feat`/`fix`, scripts, env vars, `src`/`dist`), proíbe acento e cedilha em identificador (`transacao`, nunca `transação`: acento em nome de coluna estraga `grep`) e manda a decisão para um ADR do projeto. A regra fica só no `preferencias.md`, que é onde o usuário escolhe entre global e projeto — repetir no template do `CLAUDE.md` criaria duas fontes para a mesma regra.

## 0.13.3 — 2026-09-05

- O `workflow-demanda` passa a dizer o que **não** entra em `docs/projeto/`. A árvore de pastas listava o que mora lá e parava aí, e o nome da pasta não carrega a exclusão: doc que descreve o mundo em vez de um trabalho a fazer — configuração, ID externo, decisão de marca, número de negócio, aprendizado — ia parar na pasta de governança porque era "do projeto" e porque o agente já estava com ela aberta. A regra não pede que ninguém crie pasta de domínio: a raiz de `docs/` basta até haver arquivo suficiente para uma.

## 0.13.2 — 2026-09-02

- Corrige o exemplo da linha `Processo` no `fechar-demanda`: `entrevista: to-spec` vira `entrevista: grill-with-docs`. Na coleção do Matt Pocock quem entrevista é `grill-with-docs`; `to-spec` só sintetiza a conversa e publica ("no interview, just synthesis"), e o exemplo contradizia o de duas linhas acima.

## 0.13.1 — 2026-09-01

- **Poda das quatro skills que carregam a cada demanda**, sem regra nova nem regra removida. O que saiu foi justificativa depois da instrução já dada (por que a sugestão fica na spec, por que não reler o próprio diff, por que a issue vai no fim da linha), duplicata (`/clear` estava em três lugares e fica nos dois em que se aplica) e conhecimento sobre as outras coleções que envelhece com a versão delas. Os passos 3 e 4 do `implementar-spec`, que usavam o mesmo critério duas vezes, viraram um; o passo 4 do `fechar-demanda` virou tabela — destino por gatilho — em vez de um item de vinte linhas.
- A premissa de tamanho das skills ("dizem o que o agente não teria como inferir e param aí") sai do `workflow-demanda` e vai para o README: é critério para quem mantém o plugin, não instrução para o agente.
- Sai a linha do `Shift+Tab` e `Ctrl+G` do `workflow-demanda` — detalhe de interface que o agente não executa, e que ficou pela metade desde que o `implementar-spec` entra no plan mode quando o usuário escolhe `aicf-plan`. A tabela de implementação diz isso agora.
- As descriptions de `criar-spec` e `implementar-spec` perdem o "par do …", que era para leitor humano e custava contexto em toda sessão.

## 0.13.0 — 2026-09-01

- **`criar-spec` e `implementar-spec` passam a ser invocáveis pelo agente.** Sai o `disable-model-invocation: true` das duas. Com a flag, "me entreviste sobre X" e "pode implementar a spec" não carregavam a skill: a documentação diz que o Claude Code bloqueia a chamada e o agente deveria pedir que o usuário digitasse o comando, mas na prática ele fazia o trabalho como tarefa comum, sem a skill. A flag existia pelo critério "side effect ou timing", e o pedido explícito do usuário já resolve o timing — o `fechar-demanda`, que também escreve e commita, nunca a teve. Deixar cada projeto escolher não era opção: `skillOverrides` não afeta skill de plugin. Como a description agora conta para a auto-ativação, as duas passam a dizer **quando não** invocar — pergunta pontual, implementação em curso, tarefa sem spec. `criar-prd` e `setup` mantêm a flag: rodam uma vez ou raramente, e o comando digitado basta.
- **A decisão do caminho de implementação ganha dono e momento.** A regra de que o caminho era sempre pergunta ao usuário morava em três lugares e nenhuma skill estava carregada na hora em que se aplica — entre a spec pronta e a primeira skill de implementação —, então o agente deduzia e ninguém notava, porque a linha `Processo` só era completada no fechamento. Agora o `criar-spec` grava a sugestão ao lado de `a definir` (`sugestão: aicf-direto (motivo)`), porque a entrevista é quando o agente mais sabe sobre a demanda e o usuário a vê ao revisar a spec; o `implementar-spec` ganha o passo de decisão, depois de ler a spec e o código: segue a sugestão quando o caso é óbvio (caminho aicf direto e diff que cabe numa frase), pergunta com `AskUserQuestion` nos demais, para e passa o bastão se a resposta for outra coleção, e entra no plan mode se for `aicf-plan` — plano em sessão com plan mode desligado continua `aicf-direto`. O template do `CLAUDE.md` ganha a linha "Coleções de skills de workflow instaladas", de onde a pergunta tira as opções; e o `fechar-demanda` substitui `a definir · sugestão: ...` pelo caminho seguido, registrando no relatório se divergiu. A regra reescrita — entrevista é pergunta; implementação segue a sugestão no caso óbvio e é pergunta com opções nos demais — vale igual no `workflow-demanda`, no template do `CLAUDE.md` e nos READMEs.
- **"Nativo" vira "aicf".** A palavra queria dizer duas coisas: o caminho próprio do plugin (`nativo-direto`, `nativo-plan`) e ferramenta do Claude Code (plan mode, `/code-review`), às vezes a quatro linhas de distância. "Nativo" fica reservado ao que é do Claude Code; o caminho do plugin passa a ser **caminho aicf**, com os valores `aicf-direto` e `aicf-plan` na linha `Processo`. Demandas já arquivadas não são reescritas.
- **O template do `CLAUDE.md` ganha `## Verificação`**, no formato que o playbook da Anthropic publica: comando por comando, com o que conta como saída saudável, e "se um teste falha, corrigir o código, não o teste". O `fechar-demanda` lia "do `CLAUDE.md`" qual era o comando de check, mas o template não tinha seção para isso; agora o fechamento procura essa seção pelo nome, e o fallback (scripts do projeto, ou registrar a ausência) continua igual. A seção fica no `claude-md.md`, não no `preferencias.md`: o comando é do projeto, e o `preferencias.md` pode ir para o global.
- **O passo 4 do `fechar-demanda` fica completo.** A página `memory` lista quatro gatilhos para escrever no `CLAUDE.md`; a skill conhecia um (o erro pela segunda vez) e submetia o achado de revisão de código ao mesmo limiar, que a documentação não exige. Entram os dois que faltavam — achado de revisão que o agente deveria saber sobre este código, sem esperar a segunda vez, e contexto que um colega novo precisaria — e o destino que não existia em skill nenhuma: regra que só vale para uma parte do código vai para `.claude/rules/<tema>.md` com `paths:`, e carrega só quando o agente toca arquivo daquele padrão. O contrapeso ganha número: o alvo publicado é abaixo de 200 linhas por arquivo `CLAUDE.md`, e o template repete o alvo na seção "Registro".
- **O `implementar-spec` nomeia o subagente no passo 2.** "Ler o que já existe de parecido no repositório" é o ponto do plugin onde o padrão de falha _infinite exploration_ morde; a documentação tem gatilho nomeado para ele — investigação sai do contexto principal — e a skill passa a dizê-lo ali, e só ali. Nas demais fases vale a escolha livre do `workflow-demanda`.
- **O `setup` prova e aponta.** Ao terminar, pede que o usuário rode `/context` na próxima sessão e confira o `CLAUDE.md` em **Memory files** — o arquivo carrega no início da sessão, e a lista é a prova em vez da suposição. Em projeto que já tem código, sugere `/init` com `CLAUDE_CODE_NEW_INIT=1` para a parte do `CLAUDE.md` que se deduz do código (comandos, layout, convenções); o setup segue dono da governança. E o caso Windows sem Developer Mode deixa de "seguir sem `AGENTS.md`": a documentação indica o import `@AGENTS.md` no lugar do link, que preserva o objetivo de um arquivo com dois nomes.

## 0.12.0 — 2026-09-01

- **`intents/` e `specs/` substituem `demandas/`.** A pasta passa a dizer a maturidade do documento, não a certeza de fazer: `intents/<nome>.md` é a demanda decidida e ainda não entrevistada, `intents/backlog/` é o que ainda não se sabe se será feito, `specs/<nome>.md` é a spec pronta para implementar, `specs/concluidas/` é o arquivo morto. Antes, `demandas/<nome>.md` podia ser um parágrafo cru ou uma spec entrevistada, e só abrindo o arquivo dava para saber. A spec é o intent movido com `git mv` — mesmo nome, histórico junto —, e tudo termina em `specs/concluidas/`, inclusive o que a entrevista concluiu não fazer. "Demanda" continua sendo a unidade de trabalho; por isso `workflow-demanda` e `fechar-demanda` mantêm o nome. **Migração:** `git mv demandas/backlog intents/backlog`, `git mv demandas/concluidas specs/concluidas`, o que estava ativo em `demandas/` vai para `specs/`, e `intents/` nasce vazia.
- **A linha `Processo` ganha rótulos** — `Processo — entrevista: <skill> · implementação: <skill>` — e o valor é sempre escrito: `nenhuma` quando não houve entrevista, nome da skill nos outros casos (`criar-spec`, `nativo-direto`, `nativo-plan`, `brainstorming`, `to-spec`…). O formato antigo tinha duas leituras para a mesma forma: `Processo: nativo-direto` significava "sem entrevista" e `Processo: mattpocock` significava "pipeline completo", ambos sem seta. As demandas já arquivadas não são reescritas.
- **`implementar-spec` ganha as duas decisões que se tomam com o código à vista.** Planejar ou ir direto, com o critério que a documentação da Anthropic publica — se dá para descrever o diff em uma frase, não planeje; e, indo direto, dizer a frase antes de editar, que é o gate mais barato que existe. E avaliar se a mudança merece teste e se merece começar pelo teste que falha: correção de bug é o caso claro dos dois; texto e configuração não pedem nenhum; no meio, onde o projeto já testa, a mudança entra testada. Nenhuma das seis skills mencionava teste.
- **O check do `fechar-demanda` passa a incluir a suíte de testes**, quando existe. Só lint, format e typecheck deixavam o teste novo protegendo só a sessão em que nasceu.
- **`criar-spec` ganha o passo zero**: ler o que a demanda toca no repositório, se ainda não tiver lido nesta sessão — a cláusula que evita reler quando a sessão emendou de outra fase. A instrução existia, mas dentro do parágrafo sobre como formular perguntas.
- **Sai o `PLANO-<titulo>.md`.** Ele dizia quais demandas andam juntas, e o `CHECKLIST.md` já diz isso com um título de seção. Demanda grande demais para uma sessão é uma spec só, com as entregas em checkboxes no corpo e fechamento parcial entre sessões; demandas independentes que andam juntas são specs separadas agrupadas no checklist.
- **Sai a recomendação de escrever as diferenças do projeto num `CLAUDE.md` dentro de `docs/projeto/`.** `CLAUDE.md` de subpasta só entra no contexto quando o agente lê um arquivo daquela pasta, e registrar uma demanda nova não exige isso — a recomendação apontava para um lugar que carrega tarde demais, e a frase no `workflow-demanda` mandando procurar esse arquivo existia para compensar. O README passa a dizer o contrário: diferença vai no `CLAUDE.md` da raiz ou em `.claude/rules/`. **Se você seguiu a recomendação antiga, mova o conteúdo de `docs/projeto/CLAUDE.md` para a raiz.**
- A tabela de entrevista do `workflow-demanda` registra que o `brainstorming` do Superpowers só grava arquivo no caminho _architectural_ e que o projeto pode mandá-lo gravar direto em `specs/<nome>.md`; a linha do Matt Pocock ganha a mesma opção via tracker configurado no setup.

## 0.11.0 — 2026-08-30

- O passo 4 do `fechar-demanda` ganha **fonte, limiar e contrapeso**. Fonte: além do relatório, o agente relê os achados da revisão de código — o material com maior chance de virar regra útil (o caso de borda que faltou, a suposição que não se sustentava) vivia na sessão ou nos comentários do PR e evaporava no `/clear`. Limiar: a rota `CLAUDE.md` deixa de aceitar qualquer regra e passa a exigir que o erro tenha aparecido duas vezes, porque uma vez é caso isolado. Contrapeso: promover para o `CLAUDE.md` obriga a olhar o que de lá saiu de validade. Sem esses dois últimos, a skill produzia exatamente o padrão de falha que a documentação da Anthropic nomeia — o `CLAUDE.md` sobre-especificado, longo o bastante para o agente ignorar metade dele. Não havia limiar de entrada, teto de tamanho, nem saída.
- `workflow-demanda` ganha a outra metade da regra de trabalho recorrente. A seção dizia que procedimento repetido vira skill ou command e parava aí. Faltava a distinção: skill é conselho que o modelo pode não seguir, **hook** é script que roda sempre. Regra que precisa valer sem exceção — formatar após editar, barrar escrita em pasta protegida — escrita como linha de skill é regra que vai falhar em silêncio algum dia, e o critério é justamente esse, se a falha passaria despercebida.
- O passo 2 do `criar-spec` para de gravar o que ainda não aconteceu. Ele mandava perguntar o caminho de implementação e fechar a linha `Processo:` inteira, enquanto o passo 3 logo abaixo recomendava `/clear` — e dava o argumento que derruba o 2: se a spec deve bastar sozinha, a escolha do caminho pertence a quem vai lê-la, não a quem a escreveu. Agora a linha nasce como `<entrevista> → a definir` e o fechamento a completa, que é onde ela já mora. Perguntar continua certo no outro ramo do passo 3, quando a implementação emenda na mesma sessão.

## 0.10.1 — 2026-08-29

- O check do fechamento ganha default: o `CLAUDE.md` continua sendo a fonte de qual é o comando, mas na ausência dele o agente usa os scripts que o projeto expõe, e não havendo nenhum registra o fato no relatório. Antes a instrução era só "rodar o script de check do projeto" — sem `CLAUDE.md`, o agente adivinhava ou pulava calado. Skill precisa funcionar sozinha; o `CLAUDE.md` refina, não habilita.

## 0.10.0 — 2026-08-29

- Sai do `fechar-demanda` a instrução **"prompt para a próxima sessão"**. Ela mandava montar um bloco autocontido com contexto, escopo, fora de escopo, DoD, skills, checks e branch — e todos esses campos já moram no arquivo da demanda e no `CLAUDE.md` do projeto. O prompt era uma cópia manual dos dois, criando uma terceira fonte que diverge das outras: uma skill que existe para tirar o porquê da conversa terminava mandando exportar o repositório de volta para a conversa. Com o registro em dia, a retomada é `implementa a próxima demanda do checklist` numa sessão limpa; se isso não basta, o defeito está no checklist ou na demanda, e é lá que se corrige. Some junto a regra de cercar o bloco com `---`, que só existia para proteger o formato dele.
- Entra no lugar a seção **"Sessão que acaba antes da demanda"**, o caso que faltava: os cinco passos assumiam demanda concluída (mover para `concluidas/`, marcar `- [x]`) e não havia caminho para "parei no meio". Agora contexto no fim com demanda aberta também é fechamento, só que parcial — o arquivo fica em `demandas/`, o checklist não é marcado, e o que a sessão descobriu vai para `## Estado em andamento` no próprio doc. O critério do que entra ali: se a frase serve para qualquer demanda, ela é do `CLAUDE.md`.
- Dois disparos, com donos diferentes: quando o usuário sinaliza a parada, o agente registra sem perguntar — é execução de ritual, igual ao fechamento normal, e é o caso que hoje falha em silêncio (dá-se `/clear` e o estado evapora); quando é o agente que percebe o aperto, ele avisa e a decisão de continuar, compactar ou cortar é do usuário. Encerrar o trabalho por conta própria para registrar continua fora.
- `workflow-demanda` ganha a premissa de tamanho: **estas skills dizem o que o agente não teria como inferir e param aí**. Ausência de instrução é liberdade, não lacuna — o que a ferramenta nativa já faz bem e o que se decide melhor no caso concreto ficam com o agente. Serve como critério de edição: quanto mais a skill descreve, mais ela precisa ser reescrita a cada evolução do modelo.
- O gatilho do caso novo mora na **description** do `fechar-demanda`, não num template de `CLAUDE.md`. Regra de "quando invocar" colocada no template só chega a quem rodou o `/aicf:setup` nesta versão, e não acompanha upgrade do plugin — a description viaja com a skill. Dependência do `CLAUDE.md` continua legítima para o que só o projeto sabe (qual é o comando de check, qual é a branch); para gatilho, não.

## 0.9.2 — 2026-08-25

- O fim do `setup` e o template do PRD passam a apontar para `/aicf:criar-prd` em vez de mandar "preencher o `PRD.md`" na mão — texto anterior à skill, nunca atualizado. Como ela é manual (`disable-model-invocation`), só é descoberta se alguém apontar, e o setup é o lugar natural desse ponteiro.

## 0.9.1 — 2026-08-24

- A sugestão de `/clear` ao fim do `criar-spec` vira condicional: entrevista curta e demanda pequena podem emendar a implementação na mesma sessão; entrevista longa mantém a sugestão, porque a spec deve bastar sozinha — implementar pela memória da conversa esconde spec incompleta.

## 0.9.0 — 2026-08-24

- Nova arquitetura de carregamento: o corte agora é **por fase, não por tema**. A poda por escrita tinha esgotado o ganho — o custo restante era material de fim de sessão (fechamento, relatório, prompt da próxima sessão) viajando desde o turno 1, porque o `implementar-spec` mandava carregar o `workflow-demanda` inteiro logo no passo 2.
- Nasce **`fechar-demanda`** (model-invoked): os cinco passos, o relatório, a linha `Processo:` e o prompt para a próxima sessão saem do `workflow-demanda` para cá. Por ter description própria, o agente a dispara proativamente ao concluir qualquer demanda — inclusive nos caminhos Superpowers e Matt Pocock, que não passam pelo `implementar-spec`.
- `workflow-demanda` vira só o mapa (−41%): ciclo, tabelas de caminho, governança, trabalho recorrente e PLANOs — material de início e triagem, carregado quando é a hora dele. `implementar-spec` deixa de invocá-lo e passa a invocar `/aicf:fechar-demanda` ao final: a sessão de implementação começa com ~250 palavras e só recebe as ~700 do fechamento quando chega lá.
- Custo novo: uma description a mais sempre em contexto (a do `fechar-demanda`). Duplicações deliberadas de 1 linha: a regra do desvio de roteiro ecoa no `implementar-spec`, e o formato `Processo: <entrevista> → <implementação>` fica inline no `criar-spec` — carregar uma skill inteira para recuperar uma linha custa mais do que a repetição.

## 0.8.1 — 2026-08-24

- Segunda rodada de poda nas quatro skills de workflow (−6%, 18.216 → 17.141 chars), desta vez **entre arquivos**: cada regra passou a ter um dono único, e quem precisa dela aponta em vez de reexplicar. O `workflow-demanda` é dono da governança (estrutura, linha `Processo:`, fechamento, "o `CLAUDE.md` do projeto manda"); `criar-spec` e `implementar-spec` ficam só com a técnica da sua fase. O `implementar-spec` encolheu 22% — apontava para o ritual duas vezes no mesmo arquivo e reexplicava a forma do `Processo:` que já morava no `workflow-demanda`.
- Regra de 1 linha repetida ficou repetida de propósito ("rodar fora do plan mode", "perguntar onde gravar"): obrigar o agente a carregar outra skill inteira para recuperar duas linhas custa mais contexto do que economiza. Ponteiro é para bloco, não para frase.
- Os `description` do frontmatter — os únicos caracteres carregados em toda sessão — também encolheram, preservando os substantivos que disparam a auto-invocação do `workflow-demanda`.
- Verificação por inventário: 77 regras normativas extraídas antes da edição e conferidas uma a uma depois. Nenhuma removida.

## 0.8.0 — 2026-08-17

- `workflow-demanda` ganha a seção **O que esta skill não decide**: a governança é obrigatória, o resto é roteiro. Ferramenta do agente (subagente, plan mode, worktree, code review) é escolha livre em qualquer ponto, e sair do roteiro só exige dizer numa linha o que vai fazer e por quê. Existia o risco oposto — um conjunto de skills chamado "workflow" ser lido como trilho, e o agente perder a iniciativa que teria num prompt natural.
- O ritual de fechamento passa a **nomear as opções de revisão de código** (`/code-review`, subagente fresco, code review do harness) em vez de só "propor revisão": instrução sem alternativa nomeada cai na opção mais fraca, que é o agente reler o próprio diff na mesma sessão.
- As quatro skills encolhem 17% no total, sem perder regra. O maior ganho veio de duplicação: o `implementar-spec` mandava não presumir o ritual "pela memória desta skill" e em seguida repetia o ritual inteiro — agora aponta para o `workflow-demanda` e para. O check do projeto também morava em dois lugares e ficou só onde é executado.

## 0.7.1 — 2026-08-17

- Corrige duplicação entre os templates do `setup`: `## Validação` estava no `claude-md.md` **e** no `preferencias.md`, então o `CLAUDE.md` nascia com ela mesmo quando o usuário respondia que o global já cobre os padrões. Achado rodando o `setup` num projeto de verdade.
- O `CLAUDE.md` gerado passa a citar `CONTEXT.md` e `docs/adr/`, que o passo 4 do ritual de fechamento já mandava alimentar.

## 0.7.0 — 2026-08-17

- `setup` passa a criar um `README.md` simples (o que é, status, onde ficam as coisas) e o link simbólico `AGENTS.md -> CLAUDE.md`, para que agentes que leem `AGENTS.md` vejam o mesmo arquivo em vez de uma cópia que envelhece sozinha.

## 0.6.0 — 2026-08-17

- `criar-prd` — entrevista sobre o produto (problema, público, escopo, sucesso, riscos) e escreve o `PRD.md`. Roda de novo em modo revisão, porque o PRD é vivo. Fecha a lacuna que o kit tinha: ele cobria da demanda em diante, não do produto em diante.

## 0.5.0 — 2026-08-17

- A entrevista de ferramentas do `setup` cai de nove categorias para três — gerenciador de senhas, fonte de documentação de biblioteca, coleções de skills de workflow —, as únicas que mudam o comportamento do agente. O catálogo em `references/` sai, e as respostas passam a ser registradas onde já havia lugar, sem seção nova no `CLAUDE.md`.

## 0.4.0 — 2026-08-17

- `setup` passa a levantar **as ferramentas que o projeto usa** — gerenciador de senhas, hospedagem, banco, CI, e as demais conforme o caso — explicando para que cada categoria serve a quem ainda não usa nenhuma. O resultado vira a seção `## Stack e serviços` do `CLAUDE.md`, com o nome da variável de ambiente e nunca o valor. Catálogo em `skills/setup/references/ferramentas.md`.

## 0.3.0 — 2026-08-17

- `setup` passa a oferecer os **padrões de engenharia** (idioma, KISS/YAGNI, validação antes do commit, testes, acessibilidade, tratamento de credencial), perguntando se vão para o `CLAUDE.md` global da máquina ou o do projeto. O global nunca é sobrescrito: quando já existe, a skill mostra o que falta e propõe.

## 0.2.0 — 2026-08-17

- `setup` — cria a base de um projeto novo: `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz. Só invocável pelo usuário.
- README reposicionado: o plugin é a **camada de governança** que falta às coleções focadas na demanda individual, e funciona sozinho ou por cima delas.
- README em inglês.

## 0.1.0 — 2026-08-17

Primeira versão pública.

- `workflow-demanda` — o ciclo de uma demanda: quatro fases, os caminhos de cada uma (nativo, Superpowers, Matt Pocock), nomenclatura, formato do relatório e ritual de fechamento.
- `criar-spec` — a fase de entrevista no caminho nativo: interroga até não sobrar decisão em aberto e escreve a spec no repositório.
- `implementar-spec` — a fase de implementação no caminho nativo: lê a spec, implementa, verifica no projeto inteiro e conduz o fechamento.
