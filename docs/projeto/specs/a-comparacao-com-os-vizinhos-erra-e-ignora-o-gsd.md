# A comparação com os vizinhos erra sobre o Matt e ignora o GSD

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (só prosa em três arquivos, e cada frase nova já vem com o comando que a confere)

## Problema

Em 2026-09-19 uma pesquisa em fonte primária leu sete frameworks de desenvolvimento com agente
contra os quatro critérios da governança do aicf. O resultado inteiro, com sha e comando por
afirmação, está em [governança macro nos frameworks vizinhos](../../referencias/governanca-nos-frameworks-vizinhos.md).
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

- [ ] **A frase sobre o tracker do Matt fica certa nos três arquivos.** `README.md` e `README.en.md`
      passam a dizer "GitHub, GitLab ou markdown local, e outro tracker descrito em prosa". No
      `CLAUDE.md`, a regra "Afirmação sobre ferramenta de terceiro carrega o comando que a confere"
      ganha, além da correção, o registro de que a própria frase errou uma segunda vez: é a prova de
      que a regra vale, e o texto novo carrega o comando do Matt.
- [ ] **As três frases da seção "Por que este" ganham a nuance.** "O código é revisto contra o plano
      durante a execução, mas o plano e a spec ficam como foram escritos: nada os atualiza com o que
      saiu"; "no caminho _architectural_"; e "o Matt guarda o que foi recusado por pedido, não o que
      o produto é". Cada frase nova vem com o comando de conferência entre parênteses ou em nota, no
      formato que o `README.md` já usa.
- [ ] **A seção "Por que este" ganha um parágrafo sobre GSD e BMAD.** Diz que eles têm a mesma
      camada, que a diferença é serem donos da implementação, e que é isso que o aicf deixa de fora
      por decisão ([ADR 0001](../../adr/0001-fronteira-de-fase.md)). O título da seção passa a
      cobrir os quatro, ou ganha um segundo `<details>`; a implementação escolhe o que fica mais
      curto. Nenhuma afirmação sobre GSD ou BMAD entra sem o comando que a confere.
- [ ] **O `README.en.md` acompanha, seção por seção**, como a demanda
      [a entrada de quem chega](concluidas/a-entrada-de-quem-chega.md) estabeleceu
      (`grep -c '^## ' README.md README.en.md` devolve o mesmo número).
- [ ] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código, como manda a seção Publicação
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
3. `grep -c 'GSD' README.md README.en.md` devolve pelo menos 1 em cada, e cada frase sobre GSD ou
   BMAD tem um comando de conferência ao lado.
4. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois.
5. `./scripts/check.sh` termina em `Tudo verde.`, e a versão do `plugin.json` é a entrada do topo do
   `CHANGELOG.md`.
