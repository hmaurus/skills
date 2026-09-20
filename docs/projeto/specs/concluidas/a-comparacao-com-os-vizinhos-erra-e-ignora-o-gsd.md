# A comparação com os vizinhos erra sobre o Matt e ignora o GSD

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

Em 2026-09-19 uma pesquisa em fonte primária leu sete frameworks de desenvolvimento com agente
contra os quatro critérios da governança do aicf. O resultado inteiro, com sha e comando por
afirmação, está em [governança macro nos frameworks vizinhos](../../../referencias/governanca-nos-frameworks-vizinhos.md).
Ela achou três problemas na prosa deste repositório.

**Uma afirmação errada sobre o Matt Pocock, em três lugares.** O `README.md`, o `README.en.md` e o
`CLAUDE.md` dizem que o setup dele oferece "GitHub, Linear ou markdown local". No sha `c55ee46`
de `mattpocock/skills` as opções são **GitHub, GitLab, markdown local e Other**; Linear só entra
como "Other (Jira, Linear, etc.)", descrito em prosa livre pelo usuário
(`sed -n 44,47p $R/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`). O erro está na
própria frase do `CLAUDE.md` que manda conferir afirmação sobre ferramenta de terceiro, e foi
escrita para corrigir um erro anterior na mesma seção do README
(`grep -n 'GitHub, Linear ou markdown local' CLAUDE.md README.md; grep -n 'GitHub Issues, Linear or local markdown' README.en.md`).

**Duas frases sobre o Superpowers e o Matt precisam de nuance.** Na seção "Por que este, e não o
Superpowers ou as skills do Matt Pocock":

- "nada pede que sejam revistos contra o que saiu" — o código **é** revisto contra o plano a cada
  tarefa no `subagent-driven-development` ("task review (spec compliance + code quality) after
  each", `sed -n 8p $R/superpowers/skills/subagent-driven-development/SKILL.md`). O que não
  acontece é o documento ser atualizado com o que saiu: a issue
  [obra/superpowers#1075](https://github.com/obra/superpowers/issues/1075), "Plans and specs have no
  completion status after execution", segue aberta (`gh issue view 1075 -R obra/superpowers --json state`).
- "o Superpowers grava spec e plano em arquivo" — só no caminho _architectural_. Nos caminhos
  _bounded_ e _spike_: "No spec file, no implementation plan document"
  (`grep -n 'No spec file' $R/superpowers/skills/brainstorming/SKILL.md`). A seção "Comandos
  vizinhos" já diz isso; a seção "Por que este" não.
- "Nenhuma das duas tem o documento que diz ... o que ficou fora por decisão" — o Matt tem casa
  parcial para isso: `.out-of-scope/<conceito>.md`, escrito pelo `triage` quando um pedido é
  `wontfix` (`sed -n 1,10p $R/skills/skills/engineering/triage/OUT-OF-SCOPE.md`), e o `wayfinder`
  tem seção "Not yet specified" para ideia que ainda não dá para ticketar
  (`grep -n 'Not yet specified' $R/skills/skills/engineering/wayfinder/SKILL.md`). É por esforço,
  não por produto, mas a frase absoluta está errada.

**A comparação só responde "por que não o Superpowers ou o Matt".** GSD Core e BMAD têm os quatro
critérios da governança do aicf, e em forma quase idêntica: o `PROJECT.md` do GSD tem "What This
Is", "Core Value", "Out of Scope" com motivo e "Key Decisions"
(`sed -n 1,60p $R/gsd-core/gsd-core/templates/project.md`); `complete-milestone` e
`extract-learnings` fazem o que `fechar-demanda` faz. Quem conhece o GSD lê o README e pergunta
"por que não o GSD?", e o README não responde. A resposta existe: GSD e BMAD são donos da
implementação (72 comandos, `ls $R/gsd-core/commands/gsd | wc -l`; 30 skills e `uv` obrigatório,
`ls $R/bmad-method/skills | wc -l`), e nenhum aceita rodar o Superpowers ou o Matt dentro da fase.
O aicf é a camada de governança do GSD sem o loop de execução, e plugável a qualquer caminho. Isso
é a posição do PRD, e não está escrito onde o leitor procura.

## Solução

- [x] **A frase sobre o tracker do Matt fica certa nos três arquivos.** `README.md` e `README.en.md`
      passam a dizer "GitHub, GitLab ou markdown local, e outro tracker descrito em prosa". No
      `CLAUDE.md`, só o parêntese da regra muda; nada se acrescenta.
- [x] **As três frases da seção "Por que este" ganham a nuance.** "O código é revisto contra o plano
      durante a execução, mas o plano e a spec ficam como foram escritos: nada os atualiza com o que
      saiu"; "no caminho _architectural_"; e "o Matt guarda o que foi recusado por pedido, não o que
      o produto é". Troca de frase por frase, sem comando na prosa: os comandos ficam nesta spec e
      no relatório em `docs/referencias/`, como o README já faz na seção inteira.
- [x] **A seção "Por que este" ganha um parágrafo sobre GSD e BMAD.** Diz que eles têm a mesma
      camada, que a diferença é serem donos da implementação, e que é isso que o aicf deixa de fora
      por decisão ([ADR 0001](../../../adr/0001-fronteira-de-fase.md)). O título da seção passa a
      cobrir os quatro, ou ganha um segundo `<details>`; a implementação escolhe o que fica mais
      curto. É o único acréscimo da demanda; o resto é substituição.
- [x] **O `README.en.md` acompanha, seção por seção**, como a demanda
      [a entrada de quem chega](a-entrada-de-quem-chega.md) estabeleceu
      (`grep -c '^## ' README.md README.en.md` devolve o mesmo número).
- [x] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código, como manda a seção Publicação
      do `CLAUDE.md`; a `0.18.0` foi só README e subiu versão. A entrada cita a pesquisa em
      `docs/referencias/` e o sha de cada repositório usado.

## Arquivos e interfaces

- `README.md` — seção "Por que este, e não o Superpowers ou as skills do Matt Pocock" (linhas
  159 a 171 em `07cb4a9`) e, se necessário, a seção "Comandos vizinhos" logo acima.
- `README.en.md` — a seção equivalente.
- `CLAUDE.md` — o parágrafo "Afirmação sobre ferramenta de terceiro carrega o comando que a
  confere", seção Registro.
- `docs/referencias/governanca-nos-frameworks-vizinhos.md` — a fonte; não muda nesta demanda.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump e entrada.

## Fora de escopo

- **Comparar com spec-kit, openspec e task-master no README.** Eles têm o registro por demanda e
  pedaços do "depois", mas não o documento de produto vivo; a pergunta "por que não eles" não se
  coloca da mesma forma, e cada frase a mais é uma afirmação de terceiro a manter. A pesquisa em
  `docs/referencias/` responde a quem perguntar.
- **Adotar o que os outros têm e o aicf não** — requisitos com ID rastreável, verificação separada
  do relatório, decisões em tabela append-only, estado legível por máquina. Cada um é uma demanda
  própria, se algum dia doer; a pesquisa lista os seis com o mecanismo de origem.
- **Reescrever o PRD.** A seção Problema do PRD já diz que as coleções resolvem uma demanda por vez;
  a existência do GSD não contradiz o PRD, só o README.
- **O PRD sobre `docs/referencias/`.** A pesquisa expôs que a seção Escopo do PRD dizia a pasta
  inteira fora de escopo enquanto `workflow-demanda` e o passo 3 do `fechar-demanda` mandam
  conhecimento para lá. Corrigido no PRD na mesma sessão, 2026-09-19, fora desta demanda: o que
  fica fora é só a organização interna da pasta.

## Verificação

1. `grep -rn 'Linear' README.md README.en.md CLAUDE.md` não devolve nenhuma linha que apresente
   Linear como opção do setup do Matt.
2. `sed -n 44,47p $R/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md` no sha
   `c55ee46` lista as quatro opções que o README passa a citar.
3. `grep -c 'GSD' README.md README.en.md` devolve pelo menos 1 em cada, e cada afirmação sobre GSD
   ou BMAD no README tem correspondente com comando no relatório em `docs/referencias/`.
4. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois.
5. `./scripts/check.sh` termina em `Tudo verde.`, e a versão do `plugin.json` é a entrada do topo do
   `CHANGELOG.md`.

## Relatório de implementação (2026-09-20)

**Status** — concluído. `./scripts/check.sh` termina em `Tudo verde.` com `76 links conferidos, 0
quebrados` e os dois `✔ Validation passed`; versão `0.21.0` é a entrada do topo do `CHANGELOG.md`.
CI: conferir `gh run list --workflow=ci.yml --limit 1` → `completed success` para o push que leva o
commit de fechamento.

**Arquivos alterados**

- `README.md` — título da seção passa a cobrir os quatro frameworks; três frases substituídas; um
  parágrafo novo sobre GSD e BMAD, com link para o [ADR 0001](../../../adr/0001-fronteira-de-fase.md).
- `README.en.md` — as mesmas cinco mudanças, seção por seção.
- `CLAUDE.md` — o parêntese da regra sobre ferramenta de terceiro, e (no fechamento) a oração que
  diz que o comando se roda, não só se cita.
- `CHANGELOG.md` e `.claude-plugin/plugin.json` — entrada `0.21.0` e bump, no commit de código.
- `docs/projeto/specs/a-primeira-tela-do-readme-esconde-o-argumento.md` e
  `docs/referencias/governanca-nos-frameworks-vizinhos.md` — o link para esta demanda passa a
  apontar para `concluidas/`.

**Commits** — `e106962` (código: prosa, CHANGELOG e bump) e o commit de fechamento que carrega este
relatório. `git log --oneline e106962~1..HEAD` lista os dois.

**Validação**

Cada afirmação sobre terceiro foi conferida **rodando** o comando contra o clone no sha pinado, não
só citando-o. Os quatro clones, reproduzíveis pelo bloco do
[relatório de pesquisa](../../../referencias/governanca-nos-frameworks-vizinhos.md):
`mattpocock/skills` `c55ee46`, `obra/superpowers` `5bf4e78` (era o `HEAD` do dia),
`open-gsd/gsd-core` `6dcc042`, `bmad-code-org/bmad-method` `f033e70`. O menu do setup do Matt
(`sed -n 44,47p`) lista GitHub, GitLab, Local markdown e Other; `ls $R/gsd-core/commands/gsd | wc -l`
devolveu 72 e `ls $R/bmad/skills | wc -l` devolveu 30; `sed -n 18,19p $R/bmad/README.md` mostra o
`uv` como requisito declarado; a issue `obra/superpowers#1075` seguia `OPEN`
(`gh issue view 1075 -R obra/superpowers --json state`).

**Revisão de código** — subagente fresco, que não viu a implementação, reconferiu cada afirmação
sobre terceiro contra os mesmos clones. Nenhuma errada. Duas imprecisões por omissão, as duas sobre
o Matt e as duas já registradas na pesquisa:

1. A ressalva que esta demanda escreveu no bullet do nível do produto dizia "o que ficou fora por
   pedido, não o que o produto é", e o eixo certo — o que a própria spec usa — é **esforço, não
   produto**: além do `.out-of-scope/` do `triage`, o `wayfinder` tem seção `## Out of scope`,
   "work you've consciously ruled out of _this_ effort"
   (`sed -n 95,101p $R/skills/skills/engineering/wayfinder/SKILL.md`). Corrigido nos dois READMEs
   antes do commit de fechamento.
2. O bullet do **planejamento macro** afirma que registro de ideia ainda não madura é do aicf, e o
   `wayfinder` tem `## Not yet specified` para isso. Linha que esta demanda não tocou e quarta
   frase, fora das três que a spec nomeou: virou intent,
   [o bullet do planejamento macro ignora o `wayfinder` do Matt](../o-wayfinder-do-matt-faz-o-planejamento-macro.md).

O revisor também notou que o `README.md` do próprio Matt ainda diz "GitHub, Linear, or local files"
(linha 78 em `c55ee46`), divergindo da skill de setup dele. A skill é a fonte de verdade, e é o que
os dois READMEs passam a citar.

Os quatro passos de verificação que a spec pediu: `grep -rn 'Linear' README.md README.en.md
CLAUDE.md` não devolve nada; `grep -c 'GSD' README.md README.en.md` devolve 2 em cada;
`grep -c '^## ' README.md README.en.md` devolve 6 nos dois; `./scripts/check.sh` termina verde.

**Escopo efetivo** — igual ao planejado. Para o ponto que a spec deixava à implementação escolher,
o parágrafo sobre GSD e BMAD entrou no mesmo `<details>`, com o título ampliado para os quatro
nomes: ficou mais curto do que um segundo bloco. Três ajustes de prosa não previstos, todos por
clareza e não por fato: o parágrafo de abertura passou a nomear Superpowers e Matt (o título agora
cita quatro, e "as duas coleções" ficava ambíguo), e duas frases perderam a metáfora.

**Lições**

- **A regra existia e a frase passou mesmo assim.** O `CLAUDE.md` já mandava toda afirmação sobre
  ferramenta de terceiro carregar o comando que a confere, e a frase errada sobre o tracker do Matt
  foi escrita **com o comando ao lado** — que ninguém executou. Carregar o comando e rodá-lo são
  coisas diferentes; a oração que diz isso entrou no mesmo parágrafo do `CLAUDE.md`, no passo 3
  deste fechamento.
- **O `git mv` da demanda quebrou os links nos dois sentidos, de novo.** Saem daqui três links
  relativos (`../../` → `../../../`, e `concluidas/x.md` → `x.md`) e entram dois. O item de
  `Próximas` no [ROADMAP.md](../../ROADMAP.md) que prevê isso continua de pé; o
  `./scripts/check.sh` pega, mas só depois de quebrado.
- **Corrigir três frases de uma seção deixa a quarta de pé.** A spec nomeou três, e a revisão de
  código achou uma quarta no mesmo bloco, sobre o mesmo terceiro, pelo mesmo motivo — o `wayfinder`
  não tinha sido lido. Quando a demanda é "conferir a seção X contra o repositório Y", a unidade
  certa é a seção inteira, não a lista de frases que a entrevista já suspeitava.
- **A pesquisa em `docs/referencias/` pagou o próprio custo.** Reproduzir os quatro clones nos shas
  certos custou minutos porque a tabela de shas e o bloco de `git clone` estavam escritos. Sem eles,
  conferir oito afirmações sobre terceiros seria caro o bastante para ser pulado — que foi como o
  erro de 2026-09-18 nasceu.

**Promoção de conhecimento** — uma oração no `CLAUDE.md`, no parágrafo "Afirmação sobre ferramenta
de terceiro", e uma intent nova ([o `wayfinder`](../o-wayfinder-do-matt-faz-o-planejamento-macro.md)).
Nenhum ADR, skill, regra ou doc de referência novo: o [ADR 0001](../../../adr/0001-fronteira-de-fase.md)
já sustentava o argumento do parágrafo sobre GSD e BMAD, e a pesquisa em `docs/referencias/` já
existia.

**Demanda desbloqueada** — [a primeira tela do README esconde o argumento](../a-primeira-tela-do-readme-esconde-o-argumento.md),
que declarava rodar depois desta. Ela cita `grep -n '^## O problema' README.md` → linha 43, e a
linha continua 43 depois desta demanda; as linhas 5 a 9 que ela reescreve não foram tocadas aqui.
