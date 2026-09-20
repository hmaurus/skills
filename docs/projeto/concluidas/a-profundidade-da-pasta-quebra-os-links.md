# A profundidade da pasta quebra os links da demanda

Processo — entrevista: criar-spec · implementação: aicf-plan

## Problema

O estado de uma demanda é a pasta onde ela mora, e **duas das quatro pastas estão um nível abaixo
das outras**: `intents/backlog/` e `specs/concluidas/`. O `git mv` do passo 2 do fechamento desce
um nível, e todo link relativo que **sai** do arquivo passa a resolver errado — `../../adr/` vira
`../../../adr/`, `../intents/` vira `../../intents/`.

O ritual só ensina o sentido contrário. O passo 2 do `/aicf:fechar-demanda` e a linha "Corrigir
referências após mover" do `midia-arquivo.md` dão `grep -rn '<nome-do-arquivo>'`, que acha quem
**aponta para** o arquivo movido e não enxerga nada do que sai dele.

O dano é real e já foi pago: o commit `07cb4a9` consertou dois links de saída da demanda *as
skills carregam o que não vão usar*, depois que o CI acusou — e a mensagem dele registra a causa,
"o passo 2 procura quem aponta para o arquivo movido; os links que saem dele mudaram de base".
Quem o pegou foi o `scripts/check_links.py`, que existe **neste** repositório; num projeto que
instala o plugin e não tem check de links, o mesmo `git mv` quebra em silêncio.

A exposição de hoje se mede: **33 links relativos moram dentro das pastas fundas**
(`grep -rno '](\.\./[^)]*)' docs/projeto/specs/concluidas/*.md docs/projeto/intents/backlog/*.md | wc -l`)
e **17 links apontam para elas de fora**
(`grep -rno '](\([^)]*\)\(specs/concluidas\|intents/backlog\)[^)]*)' --include='*.md' . | wc -l`).
Todo fechamento passa por essa transição.

**Nenhuma das duas coleções vizinhas tem esse problema, porque nenhuma move o registro.** No
Superpowers 5.0.0, `grep -rc 'git mv' --include='*.md' ~/.claude/plugins/cache/superpowers-marketplace/superpowers`
não devolve uma ocorrência sequer: o design doc nasce em
`docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md` e morre lá. No Matt Pocock 1.2.3 o estado é
um campo no corpo do arquivo, não o caminho dele —
`grep -n 'Status:' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.2.3/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md`
mostra `Status: claimed` para pegar o ticket e `Status: resolved` para encerrá-lo, com o arquivo
parado em `.scratch/<feature>/issues/NN-<slug>.md`.

O aicf é o único dos três que codifica o estado na profundidade do caminho, e é daí que o defeito
vem. A prova de que a profundidade é a causa, e não o movimento: `intents/` → `specs/` é o outro
`git mv` da governança, acontece na mesma frequência e **nunca quebrou um link de saída** — as duas
pastas estão no mesmo nível.

## Solução

As quatro pastas viram irmãs, sob `docs/projeto/`:

```
docs/projeto/
  backlog/      <- era intents/backlog/
  intents/
  specs/
  concluidas/   <- era specs/concluidas/
```

Com isso **nenhum `git mv` da governança muda de nível**, e todo `../` de dentro de uma demanda
continua resolvendo depois do movimento. A pasta segue sendo o estado, então o
[ADR 0003 — um item, um lugar](../../adr/0003-um-item-um-lugar.md) fica de pé: o que muda é o
aninhamento, não quem é a fonte da verdade.

O que sobra para o ritual é o sentido de entrada — quem apontava para o arquivo movido —, e para
esse o `grep -rn '<nome-do-arquivo>'` de hoje já serve. O parágrafo "Mover quebra link" do
`midia-arquivo.md` **encolhe** em vez de crescer: passa a falar de um sentido só, e some a frase
sobre a base mudar.

**A convenção de referência vira regra explícita.** A tabela do `midia-arquivo.md` já prescreve
`[título](../<pasta>/<nome>.md)`; achatado, é essa forma que garante a estabilidade — link para
irmão da mesma pasta escrito como `[título](<nome>.md)` continua quebrando no `git mv`, porque a
pasta de origem deixa de conter o alvo. A linha da tabela passa a dizer que a referência entre
demandas é **sempre** `../<pasta>/<nome>.md`, mesmo entre arquivos da mesma pasta.

**O `criar-spec` ganha a correção que nunca teve.** O `git mv` de `intents/` para `specs/` não
quebra link de saída, mas quebra quem apontava para `intents/<nome>.md` — e hoje a skill não manda
corrigir nada. Ela passa a apontar para a receita do `midia-arquivo.md`, que é onde o comando mora;
o passo 2 do `fechar-demanda` faz o mesmo, em vez de repetir o `grep` inline.

**Migração de quem já instalou:** as notas da versão explicam o layout novo e trazem os `git mv`
mais o `grep` de correção. O plugin é instrução, não código — projeto que não migrar continua
funcionando, com as skills falando de uma pasta que lá tem outro nome. O `/aicf:setup` não muda.

**Ponteiro dentro de arquivo imutável se reaponta; o texto não se toca.** O
[ADR 0005](../../adr/0005-a-documentacao-humana-e-um-arquivo-so.md) tem dois links relativos para
`../projeto/specs/concluidas/`, e o `CHANGELOG.md` tem um (linha 230). Nos três muda só o caminho
dentro dos parênteses — nenhuma palavra do texto. O que cita as pastas **em prosa ou dentro de
crase** fica como está: o comando `head -qn1` do ADR 0003 (linha 29) e as entradas antigas do
`CHANGELOG.md` descrevem o repositório da época, e o check de links não olha para dentro de crase.

A mudança pede **ADR próprio** — é difícil de reverter (16 arquivos movidos, convenção pública em
um plugin já na `0.19.0`) e tem trade-off real contra a alternativa do Matt. O ADR registra a
decisão, por que o estado continua na pasta em vez de virar campo, e que os ponteiros dos ADRs
anteriores foram reapontados sem o texto mudar.

## Arquivos e interfaces

| Arquivo | O que acontece |
|---|---|
| `docs/projeto/specs/concluidas/*.md` → `docs/projeto/concluidas/` | 12 arquivos, `git mv`; os `../` de dentro perdem um nível |
| `docs/projeto/intents/backlog/*.md` → `docs/projeto/backlog/` | 4 arquivos, `git mv`; idem |
| `skills/workflow-demanda/references/midia-arquivo.md` | tabela e parágrafo "Mover quebra link" reescritos: um sentido só, e a referência entre demandas sempre `../<pasta>/<nome>.md` |
| `skills/workflow-demanda/SKILL.md` | tabela dos quatro estados (linhas 73 e 76) com os caminhos novos |
| `skills/fechar-demanda/SKILL.md` | passo 2 com o caminho novo, apontando para a receita do `midia-arquivo.md` em vez de repetir o `grep` |
| `skills/criar-spec/SKILL.md` | o `git mv` de `intents/` para `specs/` passa a mandar corrigir quem apontava para o arquivo |
| `skills/setup/SKILL.md`, `skills/setup/templates/roadmap.md` | tabela de arquivos criados e o `head -qn1` do template com as quatro pastas |
| `README.md`, `README.en.md`, `docs/projeto/PRD.md`, `docs/projeto/ROADMAP.md` | a menção a `specs/concluidas/` vira `concluidas/`; no ROADMAP, também o `head -qn1` do topo |
| `CLAUDE.md` | dois links relativos para demandas concluídas |
| `docs/adr/0005-...md`, `CHANGELOG.md` | só o caminho dos ponteiros (2 + 1 links); texto intacto |
| `docs/referencias/governanca-nos-frameworks-vizinhos.md` | as menções ao layout |
| `docs/adr/000N-...md` | **novo.** O ADR do layout achatado |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | bump e entrada, pela sistemática de publicação |
| `docs/projeto/ROADMAP.md` | **já feito ao gravar esta spec:** a linha de `Próximas` saiu — quem tem arquivo não tem linha |

O `scripts/check_links.py` **não muda**: ele já resolve caminho relativo a partir do arquivo, e é o
juiz de cada passo da migração.

## Fora de escopo

- **O comando que confere os links de saída.** Foi escrito e testado nesta entrevista — `grep -o`
  dos destinos mais `test -e` — e cai com o achatamento: achatado, o único link de saída que ainda
  quebraria é o que aponta para irmão sem `../`, e a convenção da tabela cobre esse caso por
  escrito. Ele também carrega um custo medido: como não mascara bloco de código, acusou **3 falsos
  positivos** ao varrer os 14 arquivos de demanda, todos links de exemplo dentro de crase. Encerra
  se aparecer um movimento de pasta que a convenção não cubra.
- **Estado no corpo do arquivo, como o Matt.** Resolveria também o sentido de entrada, já que nada
  se moveria nunca. Descartado: tiraria "a pasta diz o estado" das skills, trocaria o `ls` de um
  estado por `grep`, e exigiria um ADR que supersedesse o 0003 — preço alto para o sentido que o
  `grep` de hoje já cobre.
- **O `/aicf:setup` detectar a estrutura antiga e propor migração.** As notas da versão bastam, e o
  `setup` tem `disable-model-invocation: true`: o comportamento não teria como ser verificado na
  sessão que o escrevesse.
- **Reescrever prosa histórica** no `CHANGELOG.md` e no comando do ADR 0003. Ponteiro se reaponta;
  relato do que uma versão fez fica como foi escrito.
- **Gerar check de links nos projetos que usam o aicf** — já fora de escopo por decisão de
  [nenhum teste acusa link morto](../concluidas/nenhum-teste-acusa-link-morto.md), e nada
  aqui muda isso.

## Verificação

1. **Provar que o defeito existe antes.** Medido nesta entrevista, e reproduzível enquanto o layout
   for o atual: `cp docs/projeto/specs/concluidas/as-skills-carregam-o-que-nao-vao-usar.md docs/projeto/specs/_teste-tmp.md`
   e rodar `python3 scripts/check_links.py` acusa **4 links quebrados** no arquivo copiado — os
   mesmos que o `git mv` do fechamento quebraria. Conferir que a cópia existe (`git status --porcelain`
   não vazio) antes de acreditar na saída, e `rm` no fim.
2. **Provar que o layout novo os elimina.** Com a migração feita, `git mv docs/projeto/specs/<qualquer>.md docs/projeto/concluidas/`
   seguido de `python3 scripts/check_links.py` devolve `0 quebrados` **sem editar um link sequer**,
   e `git diff --stat` mostra só o rename. Desfazer com `git mv` de volta.
3. `./scripts/check.sh` termina em `Tudo verde.`, com `N links conferidos, 0 quebrados` e os dois
   `✔ Validation passed`.
4. `grep -rn 'specs/concluidas\|intents/backlog' --include='*.md' .` devolve **apenas** o texto
   histórico deliberado: o comando do ADR 0003, as entradas antigas do `CHANGELOG.md` e a prosa das
   demandas em `concluidas/`. Qualquer outra linha é caminho esquecido. **As concluídas entraram
   nessa lista na implementação**: a spec as tinha esquecido, e elas caem no mesmo princípio que o
   `CHANGELOG.md` — ponteiro se reaponta, relato do que uma versão fez fica como foi escrito.
5. Depois do push, `gh run list --workflow=ci.yml --limit 1` → `completed success`.

## Relatório de implementação (2026-09-20)

**Status** — concluído, com **uma verificação de comportamento em aberto** (ver abaixo). CI run
`35493339756` → `completed success` (`gh run list --workflow=ci.yml --limit 1`).

**Causa raiz** — confirmada como a spec descrevia, e medida antes de tocar o disco: copiar
`as-skills-carregam-o-que-nao-vao-usar.md` de `specs/concluidas/` para `specs/` — a mesma mudança
de nível que o `git mv` do fechamento faz no sentido inverso — fez o `check_links.py` acusar **4
links quebrados**, todos de saída (`../../../adr/`, `../../intents/`). A cópia existia no
`git status --porcelain` antes de a saída ser lida.

**Arquivos alterados** — 38 no commit de código (`git show --stat 9be56e3`):

- `docs/projeto/specs/concluidas/` → `docs/projeto/concluidas/` e
  `docs/projeto/intents/backlog/` → `docs/projeto/backlog/` — 16 arquivos, `git mv`
- `docs/projeto/specs/.gitkeep` — novo: quem segurava `specs/` era o `.gitkeep` de `concluidas/`,
  que saiu de dentro dela
- `skills/workflow-demanda/references/midia-arquivo.md` — a tabela, o parágrafo das pastas irmãs e
  o "Mover quebra link" encolhido para um sentido só
- `skills/workflow-demanda/SKILL.md`, `skills/fechar-demanda/SKILL.md`,
  `skills/criar-spec/SKILL.md`, `skills/setup/SKILL.md`, `skills/setup/templates/roadmap.md`
- `README.md`, `README.en.md`, `docs/projeto/PRD.md`, `docs/projeto/ROADMAP.md`,
  `docs/projeto/intents/governanca-em-issues-neste-repo.md`, os 4 itens de `backlog/`
- [`docs/adr/0006-o-layout-das-demandas-e-achatado.md`](../../adr/0006-o-layout-das-demandas-e-achatado.md) — novo
- `.claude-plugin/plugin.json` → `0.22.0` e a entrada do `CHANGELOG.md`

**Commits** — `9be56e3` (código) e `cdf4a3e` (fechamento). Dois vieram depois, ao conferir o que o
`grep` do fechamento tinha deixado passar: `d30cfe9`, que corrige o `templates/readme.md` — ele
descrevia `concluidas/` dentro de `specs/`, e o check não o enxerga —, e `a191205`, que leva a
regra do comando executado para o passo 3 do `fechar-demanda` (onde alcança quem instala o plugin,
já que o `CLAUDE.md` fica neste repositório) e cria o `.gitignore`. Release `v0.22.0` publicada no
HEAD.

**Validação**

1. Defeito provado antes: 4 links quebrados na cópia, com `git status --porcelain` conferido antes
   da saída.
2. Layout novo provado depois: `git mv docs/projeto/specs/a-profundidade-...md docs/projeto/concluidas/`
   → `check_links.py` devolveu `0 quebrados` **sem editar um link sequer**. Desfeito com `git mv`.
3. `./scripts/check.sh` → `Tudo verde.`, `97 links conferidos, 0 quebrados`, dois `✔ Validation passed`.
4. `grep -rn 'specs/concluidas\|intents/backlog' --include='*.md' .` devolve só texto histórico
   deliberado — ver "Escopo efetivo".
5. `grep -rn 'passo [0-9]' --include='*.md' .` — a numeração não mudou; quem cita o passo 2 do
   fechamento de fora continua falando da mesma coisa.
6. Revisão de código **dispensada** por decisão do titular: o risco real (link morto) tem juiz
   automatizado no `check_links.py`, e a conferência de "destino existe mas é o alvo errado" foi do
   próprio autor, lendo a listagem antes/depois dos 46 links.
7. **O fechamento desta demanda é a prova final.** O `git mv` de `specs/` para `concluidas/` moveu
   este arquivo com dois links de saída para `../../adr/` e devolveu `0 quebrados` sem nenhuma
   edição — os dois caminhos são iguais nas duas pastas, porque elas estão no mesmo nível. Antes do
   achatamento, este mesmo movimento os teria quebrado.

**Escopo efetivo**

- **A verificação 4 da spec estava mal calibrada, e foi corrigida no próprio arquivo.** Ela exigia
  que o `grep` sobrasse apenas o comando do ADR 0003 e as entradas antigas do `CHANGELOG.md`, mas
  as demandas em `concluidas/` citam as pastas em prosa dezenas de vezes. Elas caem no mesmo
  princípio que a spec já enunciava — *"ponteiro se reaponta; o texto não se toca"* —, então os
  links dentro delas foram reapontados e a prosa ficou. Decisão do titular na abertura.
- **Dois arquivos que a spec não nomeava entraram, por serem instrução viva e não relato:** os 4
  itens de `backlog/`, cujo bloco de citação manda *"arquivar este arquivo em `specs/concluidas/`"*,
  e o intent aberto `governanca-em-issues-neste-repo.md`.
- **O caminho divergiu da sugestão da spec** (`aicf-direto` → `aicf-plan`). Motivo: o diff não cabia
  numa frase — 16 renames, 46 links recomputados, 13 arquivos editados à mão, ADR novo e bump.
- `docs/projeto/specs/.gitkeep` não estava previsto e foi necessário.

**Lições**

- **Achatar resolveu o sentido de saída, e só ele — e o teste da spec confundia os dois.** A
  Verificação 2 pedia `0 quebrados` depois de um `git mv` qualquer; rodada com um arquivo que
  tinha ponteiros de entrada, deu 2 quebrados, todos de **entrada**. Não era regressão: é o sentido
  que o `grep` do passo 2 sempre cobriu e continua cobrindo. O teste que prova esta demanda isola a
  origem — nenhum link **quebrado tem o arquivo movido como origem**.
- **A conta dos links não é uniforme, e `sed` teria errado.** De `concluidas/X.md`, `../../../adr/`
  vira `../../adr/`, mas `../a-primeira-tela-...md` vira `../specs/a-primeira-tela-...md`: o
  primeiro perde um nível, o segundo ganha um segmento. O script resolveu cada destino contra o
  caminho antigo e recomputou contra o novo, reaproveitando `mascarar_codigo()` do
  `check_links.py` para não tocar em link de exemplo dentro de crase.
- **Importar `scripts/check_links.py` de um script auxiliar cria `scripts/__pycache__/`**, que
  entrou no `git add -A` e precisou de `git rm --cached`. Rodar o check direto não gera o diretório
  — só o import gera. O repositório não tinha `.gitignore`; ganhou um com `__pycache__/` logo
  depois do fechamento, a pedido do titular (`cat .gitignore`).

**Verificação em aberto: o `/aicf:setup` num projeto novo**

Esta demanda tocou três arquivos do `setup` — `SKILL.md` (a tabela "O que criar" e a árvore),
`templates/roadmap.md` (o `head -qn1`) e `templates/readme.md` (a tabela das pastas). A skill tem
`disable-model-invocation: true`: nenhum agente consegue invocá-la nem imitar o roteiro por fora,
então **nada aqui provou que um projeto novo nasce com as quatro pastas no nível certo**. O que foi
verificado é só o texto dos arquivos.

- **Quem encerra:** o titular, rodando `/aicf:setup` em modo arquivo num diretório vazio.
- **Como:** `find docs/projeto -maxdepth 1 -type d | sort` deve devolver as quatro pastas irmãs —
  `backlog`, `concluidas`, `intents`, `specs` — e nenhuma aninhada. A tabela do `README.md` gerado
  deve trazer as quatro linhas, uma por pasta.
- **Encerrada em 2026-09-20, e passou** — a seção de encerramento no fim deste arquivo traz a saída
  dos comandos, o que a passada não cobriu e o achado que ela produziu.
- **O risco que ela existia para pegar** era o mesmo que o `templates/readme.md` materializou:
  texto de template que descreve o layout antigo e que o `./scripts/check.sh` não enxerga, porque
  `skills/setup/templates/**` está na lista de ignorados do `check_links.py`.

**O que este ritual abriu**

- [ADR 0006 — o layout das demandas é achatado](../../adr/0006-o-layout-das-demandas-e-achatado.md)
- Regra nova no `CLAUDE.md`, na seção `## Registro`: *"Comando que um doc escreve se roda antes de
  o doc fechar"* — promovida pela Verificação 4 desta spec, que previa a saída de um `grep` sem o
  ter executado. Segunda ocorrência do mesmo erro em dois dias.
- Nenhuma demanda nova nem obsoleta. A linha de `Próximas` do `ROADMAP.md` já tinha saído quando a
  spec foi gravada.

## Encerramento da verificação em aberto — o `/aicf:setup` num projeto novo (2026-09-20)

**Encerrada: passa.** O titular rodou `/aicf:setup` em modo arquivo num diretório vazio,
`~/dev/tmp/teste-aicf`, criado para isto. O modo arquivo não foi escolha: o diretório não é
repositório git e não tem remote no GitHub, então o setup ofereceu uma mídia só — o que também
exercitou o caminho "não aguentando, oferecer só arquivo e dizer em uma linha o que falta".

O critério, literal:

```
$ find docs/projeto -maxdepth 1 -type d | sort
docs/projeto
docs/projeto/backlog
docs/projeto/concluidas
docs/projeto/intents
docs/projeto/specs

$ find docs/projeto -mindepth 2 -type d
(vazio)
```

As quatro pastas irmãs, nenhuma aninhada. A tabela do `README.md` gerado traz as quatro linhas,
uma por pasta (linhas 18–21 do arquivo), e o `head -qn1` do `ROADMAP.md` gerado aponta para
`docs/projeto/concluidas/*.md`, não para a pasta funda.

**O que esta passada prova, e o que não prova.** A sessão começou com o plugin em **0.20.0** —
o cabeçalho do comando trouxe `cache/aicodingflow/aicf/0.20.0/skills/setup`, e a primeira árvore
que o agente imprimiu ao usuário foi a antiga, com `intents/backlog/` e `specs/concluidas/`. O
titular reconheceu o layout velho, atualizou o plugin no meio da conversa e perguntou se a causa
era a desatualização ou falta de ajuste. Era a desatualização: a **0.22.0** entrou no cache às
17:03, `diff -rq` entre `0.22.0/skills/setup` e `skills/setup` deste repositório deu vazio, e
`grep -rn 'specs/concluidas\|intents/backlog' 0.22.0/skills/` não devolveu nada — as únicas
ocorrências na versão estão no `CHANGELOG.md`, descrevendo a migração, e em relatórios antigos de
`docs/projeto/concluidas/`, que é onde devem estar. O agente releu o `SKILL.md` e os templates da
0.22.0 pelo disco e criou a estrutura por eles.

Então o que está provado é: **os arquivos da 0.22.0, seguidos à risca num diretório vazio,
produzem o layout achatado**. O que não está é uma invocação de ponta a ponta com a 0.22.0 já
carregada no início da sessão — na prática o mesmo texto, lido de um lugar diferente, mas a
distinção fica registrada por honestidade.

**O achado vale mais que a verificação: a versão que roda é a do início da sessão.** Skill é lida
quando a sessão abre; `/plugin update` no meio troca o cache e não recarrega o que já está em
contexto. Quem for encerrar uma verificação destas depois de atualizar o plugin **verifica a
versão anterior sem perceber** — foi exatamente o que quase aconteceu aqui, e só não aconteceu
porque o titular reconheceu a árvore velha de memória. É a mesma classe de risco que a spec
nomeou em "Verificação em aberto" — texto que descreve o layout antigo e que o
`./scripts/check.sh` não enxerga —, com origem diferente: não o arquivo do template, mas a versão
em cache. Mitigação, uma linha: **depois de `/plugin update`, reiniciar a sessão antes de
verificar**.

**O que esta passada não cobriu: o modo issue.** A pergunta da mídia não chegou a ser feita, e
por regra da própria skill — *"Só oferecer issues se o repositório aguentar. Conferir antes:
`gh auth status` passa, e `git remote -v` aponta para GitHub"*. Aqui o `gh` passou (conta
autenticada, token ativo) e o `git remote -v` devolveu `fatal: not a git repository`, então o
roteiro manda oferecer só arquivo e dizer em uma linha o que falta para a outra opção existir.
Foi o que aconteceu, e está correto para a sessão — mas deixa registrado o buraco: **o ramo issue
do setup continua sem nenhuma passada**, incluindo o `gh label create` dos três `aicf:*`, que o
`SKILL.md` destaca como a armadilha mais repetida do método (`gh issue create --label` com label
inexistente falha em vez de criar). Encerrar esse ramo pede um segundo diretório, com `git init` e
um repositório no GitHub antes de rodar o setup.

**Nota de conduta, na mesma passagem:** o agente anunciou a mídia como fato consumado — *"seguimos
com arquivos em `docs/projeto/`"* — em vez de apresentá-la como a decisão que ainda era do titular.
Com uma opção viável o efeito prático é o mesmo, mas a resposta *"espera, deixa eu criar o repo no
GitHub primeiro"* estava disponível e não foi oferecida. O roteiro diz **oferecer** só arquivo, não
declarar.

**Dois achados menores nos templates**, fora do escopo desta verificação e sem impacto no layout:

- `templates/claude-md.md` — o parêntese da linha das coleções (`_(Superpowers, Matt Pocock — são
  os caminhos que o implementar-spec pode oferecer além do aicf.)_`) existe para exemplificar
  quando o valor é "nenhuma". Quando o projeto tem as duas instaladas, a linha preenchida repete
  os mesmos dois nomes em seguida. O parêntese sem os nomes serve aos dois casos.
- `templates/readme.md` — as quatro linhas a acrescentar entram "na tabela acima", que termina na
  linha do `CLAUDE.md`. Inseridas ao fim, elas deixam o `CLAUDE.md` no meio do bloco
  `docs/projeto/*`. Cosmético; se a ordem importa, a instrução diria onde inserir.

Nada a mudar na 0.22.0 quanto ao objeto desta verificação.
